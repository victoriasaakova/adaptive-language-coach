"""Validate public configuration and, optionally, a local private configuration."""
import argparse
import json
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

def validate_config(data, public=False):
    schema = json.loads((ROOT / "config/schema.json").read_text())
    Draft202012Validator.check_schema(schema)
    errors = [".".join(map(str, e.absolute_path)) or "root"
              for e in Draft202012Validator(schema).iter_errors(data)]
    if errors:
        raise ValueError("Invalid configuration fields: " + ", ".join(sorted(set(errors))))
    if public and "notion" in data:
        raise ValueError("Notion configuration is private-only")
    if data["native_language"].strip().casefold() == data["target_language"].strip().casefold():
        raise ValueError("Native and target languages must differ")
    try:
        ZoneInfo(data["session"]["timezone"])
    except (ZoneInfoNotFoundError, ValueError):
        raise ValueError("Invalid session.timezone") from None
    return data

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--private", type=Path)
    args = parser.parse_args()
    validate_config(json.loads((ROOT / "config/example.json").read_text()), public=True)
    print("Public example: valid")
    if args.private:
        validate_config(json.loads(args.private.read_text()))
        print("Private configuration: valid (values not printed)")

if __name__ == "__main__":
    main()
