"""Bulk import board games into BGaide via API.

Usage:
  python import_games.py template --output data/games_import_template.json
  python import_games.py run --input data/games_import.json --api-base https://bgaide.cloud --mode upsert

Input JSON format:
[
  {
    "game": {
      "id": "catan",
      "name": "Catan",
      "nameEn": "Catan",
      "gameType": "德式",
      "aliases": ["卡坦岛"],
      "cover": "https://bgaide.cloud/static/picture/catan.png",
      "thumb": "https://bgaide.cloud/static/picture/catan.png",
      "players": [3, 4],
      "duration": [60, 120],
      "difficulty": "中等",
      "bggScore": 7.2,
      "tags": ["策略", "交易"],
      "hot": true,
      "recommended": true,
      "visible": true,
      "description": "经典资源交易与扩张游戏。"
    },
    "rules": {
      "components": ["地图板块", "资源牌"],
      "setup": ["随机拼接地图"],
      "winCondition": "最先达到10分获胜",
      "turnFlow": ["掷骰", "产出资源", "交易/建造"]
    },
    "faq": [
      {"q": "资源不够怎么办？", "a": "可以与其他玩家交易。"}
    ]
]

"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


DIFFICULTY_ALLOWED = {"简单", "中等", "困难"}
GAME_TYPE_ALLOWED = {"德式", "美式", "毛线聚会"}


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"\s+", "-", value)
    value = re.sub(r"[^a-z0-9\-]", "", value)
    return value.strip("-") or "game"


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def request_json(method: str, url: str, payload: dict[str, Any] | None = None) -> tuple[int, Any]:
    data = None
    headers = {"Content-Type": "application/json"}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(url=url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as e:
        raw = e.read().decode("utf-8") if e.fp else ""
        try:
            body = json.loads(raw) if raw else {"detail": e.reason}
        except json.JSONDecodeError:
            body = {"detail": raw or e.reason}
        return e.code, body


def validate_item(item: dict[str, Any], index: int) -> list[str]:
    errs: list[str] = []
    game = item.get("game")
    if not isinstance(game, dict):
        return [f"item[{index}]: missing object 'game'"]

    name = str(game.get("name", "")).strip()
    if not name:
        errs.append(f"item[{index}]: game.name is required")

    players = game.get("players")
    if not (isinstance(players, list) and len(players) == 2 and all(isinstance(v, int) for v in players)):
        errs.append(f"item[{index}]: game.players must be [min,max] integers")

    duration = game.get("duration")
    if not (isinstance(duration, list) and len(duration) == 2 and all(isinstance(v, int) for v in duration)):
        errs.append(f"item[{index}]: game.duration must be [min,max] integers")

    difficulty = game.get("difficulty", "中等")
    if difficulty not in DIFFICULTY_ALLOWED:
        errs.append(f"item[{index}]: game.difficulty must be one of {sorted(DIFFICULTY_ALLOWED)}")

    game_type = game.get("gameType")
    if game_type is not None:
        game_type = str(game_type).strip()
        if game_type and game_type not in GAME_TYPE_ALLOWED:
            errs.append(f"item[{index}]: game.gameType must be one of {sorted(GAME_TYPE_ALLOWED)}")

    visible = game.get("visible", True)
    if not isinstance(visible, bool):
        errs.append(f"item[{index}]: game.visible must be boolean")

    rules = item.get("rules")
    if rules is not None and not isinstance(rules, dict):
        errs.append(f"item[{index}]: rules must be an object or omitted")

    faq = item.get("faq")
    if faq is not None:
        if not isinstance(faq, list):
            errs.append(f"item[{index}]: faq must be a list")
        else:
            for i, qa in enumerate(faq):
                if not isinstance(qa, dict) or not str(qa.get("q", "")).strip() or not str(qa.get("a", "")).strip():
                    errs.append(f"item[{index}].faq[{i}]: each entry needs non-empty q and a")

    return errs


def normalize_item(item: dict[str, Any]) -> dict[str, Any]:
    game = dict(item["game"])

    if not str(game.get("id", "")).strip():
        game["id"] = slugify(str(game.get("name", "")))

    game.setdefault("nameEn", "")
    game.setdefault("gameType", None)
    game.setdefault("aliases", [])
    game.setdefault("cover", "")
    game.setdefault("thumb", "")
    game.setdefault("difficulty", "中等")
    game.setdefault("bggScore", 0)
    game.setdefault("tags", [])
    game.setdefault("hot", False)
    game.setdefault("recommended", False)
    game.setdefault("visible", True)
    game.setdefault("description", "")

    payload: dict[str, Any] = {"game": game}

    rules = item.get("rules")
    if isinstance(rules, dict):
        payload["rules"] = {
            "components": rules.get("components", []),
            "setup": rules.get("setup", []),
            "winCondition": rules.get("winCondition", ""),
            "turnFlow": rules.get("turnFlow", []),
        }

    faq = item.get("faq")
    if isinstance(faq, list):
        payload["faq"] = [
            {
                "q": str(x.get("q", "")).strip(),
                "a": str(x.get("a", "")).strip(),
            }
            for x in faq
            if str(x.get("q", "")).strip() and str(x.get("a", "")).strip()
        ]

    return payload


def create_or_update(api_base: str, payload: dict[str, Any], mode: str) -> tuple[bool, str]:
    game_id = payload["game"]["id"]

    status, body = request_json("POST", f"{api_base}/api/games", payload)
    if 200 <= status < 300:
        return True, "created"

    if status != 409 or mode != "upsert":
        return False, f"create failed ({status}): {body}"

    # Upsert flow for existing game.
    status, body = request_json("PUT", f"{api_base}/api/games/{urllib.parse.quote(game_id)}", payload["game"])
    if not (200 <= status < 300):
        return False, f"update game failed ({status}): {body}"

    if "rules" in payload:
        status, body = request_json(
            "PUT",
            f"{api_base}/api/games/{urllib.parse.quote(game_id)}/rules",
            payload["rules"],
        )
        if not (200 <= status < 300):
            return False, f"update rules failed ({status}): {body}"

    if "faq" in payload:
        status, body = request_json(
            "PUT",
            f"{api_base}/api/games/{urllib.parse.quote(game_id)}/faq",
            payload["faq"],
        )
        if not (200 <= status < 300):
            return False, f"update faq failed ({status}): {body}"

    return True, "updated"


def cmd_template(output: Path) -> int:
    sample = [
        {
            "game": {
                "id": "",
                "name": "",
                "nameEn": "",
                "gameType": "德式",
                "aliases": [],
                "cover": "https://bgaide.cloud/static/picture/example.png",
                "thumb": "https://bgaide.cloud/static/picture/example.png",
                "players": [2, 4],
                "duration": [30, 60],
                "difficulty": "中等",
                "bggScore": 0,
                "tags": [],
                "hot": False,
                "recommended": False,
                "visible": True,
                "description": ""
            },
            "rules": {
                "components": [],
                "setup": [],
                "winCondition": "",
                "turnFlow": []
            },
            "faq": [
                {"q": "", "a": ""}
            ]
        }
    ]
    write_json(output, sample)
    print(f"Template written: {output}")
    return 0


def cmd_run(input_path: Path, api_base: str, mode: str) -> int:
    data = read_json(input_path)
    if not isinstance(data, list):
        print("Input JSON must be a list", file=sys.stderr)
        return 2

    errors: list[str] = []
    normalized: list[dict[str, Any]] = []

    for idx, item in enumerate(data):
        if not isinstance(item, dict):
            errors.append(f"item[{idx}] must be an object")
            continue
        item_errors = validate_item(item, idx)
        if item_errors:
            errors.extend(item_errors)
            continue
        normalized.append(normalize_item(item))

    if errors:
        print("Validation errors:")
        for e in errors:
            print(f"  - {e}")
        return 2

    created = 0
    updated = 0
    failed = 0

    for payload in normalized:
        ok, result = create_or_update(api_base=api_base.rstrip("/"), payload=payload, mode=mode)
        game_id = payload["game"]["id"]
        if ok:
            if result == "created":
                created += 1
            elif result == "updated":
                updated += 1
            print(f"[OK] {game_id}: {result}")
        else:
            failed += 1
            print(f"[FAIL] {game_id}: {result}")

    print("\nImport finished")
    print(f"  created: {created}")
    print(f"  updated: {updated}")
    print(f"  failed : {failed}")

    return 0 if failed == 0 else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Import games into BGaide")
    sub = parser.add_subparsers(dest="command", required=True)

    p_template = sub.add_parser("template", help="Generate JSON template")
    p_template.add_argument("--output", type=Path, default=Path("data/games_import_template.json"))

    p_run = sub.add_parser("run", help="Import from JSON file")
    p_run.add_argument("--input", type=Path, required=True)
    p_run.add_argument("--api-base", type=str, default="http://127.0.0.1:8000")
    p_run.add_argument("--mode", choices=["create", "upsert"], default="upsert")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "template":
        return cmd_template(args.output)
    if args.command == "run":
        return cmd_run(args.input, args.api_base, args.mode)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
