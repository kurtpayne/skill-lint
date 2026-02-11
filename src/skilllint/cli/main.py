from __future__ import annotations

import argparse
import json
from pathlib import Path

from skilllint.core.analyzer import analyze


def _to_markdown(result: dict) -> str:
    s = result["summary"]
    lines = [
        "# SkillLint Report",
        "",
        f"- Target: `{result['target']}`",
        f"- Files scanned: **{s['files_scanned']}**",
        f"- Findings: **{s['findings_total']}**",
        f"- Quality overall: **{s['quality_overall']}**",
        "",
        "## Severity",
    ]
    for k, v in s["by_severity"].items():
        lines.append(f"- {k}: {v}")

    lines.append("\n## Top Findings")
    for f in result["findings"][:20]:
        loc = f"{f['file']}:{f['line_start']}" if f.get("line_start") else f["file"]
        lines.append(f"- **[{f['severity'].upper()}]** {f['title']} ({loc})")
    return "\n".join(lines)


def cmd_scan(args: argparse.Namespace) -> int:
    target = Path(args.target)
    res = analyze(target).to_dict()

    if args.format == "json":
        out = json.dumps(res, indent=2)
    elif args.format == "markdown":
        out = _to_markdown(res)
    else:
        out = f"SkillLint: scanned {res['summary']['files_scanned']} files, findings={res['summary']['findings_total']}, quality={res['summary']['quality_overall']}"

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        print(out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="skilllint", description="Offline quality + security linter for AI skills")
    sp = p.add_subparsers(dest="command", required=True)

    scan = sp.add_parser("scan", help="Scan a file or directory")
    scan.add_argument("target", help="File or directory to scan")
    scan.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    scan.add_argument("-o", "--output", help="Write output to file")
    scan.set_defaults(func=cmd_scan)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
