from __future__ import annotations

import argparse
import json
import sys
from typing import Sequence

from dsl2hillm.bus import dispatch


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="dsl2hillm")
    parser.add_argument("line", nargs="?", help="DSL line, e.g. 'HEALTH' or 'READ DEVICE camera-usb'")
    parser.add_argument("--file", help="Default project file for relative paths")
    args = parser.parse_args(list(argv) if argv is not None else None)
    if not args.line:
        parser.print_help()
        return 2
    result = dispatch(args.line, default_file=args.file)
    print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
