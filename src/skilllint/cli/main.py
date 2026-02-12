from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from skilllint.core.analyzer import analyze
from skilllint.core.file_handler import iter_candidate_files
from skilllint.core.policy import load_policy, should_fail
from skilllint.fixes.safe_fixes import apply_safe_fixes


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
    for f in result["findings"][:40]:
        loc = f"{f['file']}:{f['line_start']}" if f.get("line_start") else f["file"]
        lines.append(f"- **[{f['severity'].upper()}]** {f['title']} ({loc})")

    lines.append("\n## Metric Averages")
    by_name: dict[str, list[float]] = defaultdict(list)
    for m in result["metrics"]:
        by_name[m["name"]].append(float(m["score"]))
    for name in sorted(by_name):
        avg = sum(by_name[name]) / len(by_name[name])
        lines.append(f"- {name}: {avg:.2f}")
    return "\n".join(lines)


def _evaluate_quality(policy: dict, result: dict) -> list[str]:
    quality = policy.get("quality", {})
    by_name: dict[str, list[float]] = defaultdict(list)
    for m in result["metrics"]:
        by_name[m["name"]].append(float(m["score"]))

    avg = {k: (sum(v) / len(v) if v else 0.0) for k, v in by_name.items()}
    failures: list[str] = []

    def check_min(metric: str, key: str) -> None:
        if key in quality and avg.get(metric, 0.0) < float(quality[key]):
            failures.append(f"quality gate failed: {metric}={avg.get(metric, 0.0):.2f} < {quality[key]}")

    check_min("readability", "readability_min")
    check_min("structure", "structure_min")
    check_min("consistency", "consistency_min")
    check_min("completeness", "completeness_min")
    check_min("maintainability", "maintainability_min")
    check_min("precision", "precision_min")
    check_min("security_integration", "security_integration_min")

    # complexity policy expressed as max raw complexity; our normalized score inverts.
    if "complexity_max" in quality:
        # convert raw max threshold to normalized minimum score heuristic
        raw_max = float(quality["complexity_max"])
        normalized_min = max(0.0, min(100.0, 100.0 - (raw_max * 2.0)))
        if avg.get("complexity", 0.0) < normalized_min:
            failures.append(
                f"quality gate failed: complexity_score={avg.get('complexity', 0.0):.2f} < {normalized_min:.2f} (from complexity_max={raw_max})"
            )

    return failures


def cmd_scan(args: argparse.Namespace) -> int:
    target = Path(args.target)
    policy = load_policy(Path(args.policy) if args.policy else None)
    res_obj = analyze(target, policy=policy)
    res = res_obj.to_dict()

    quality_failures = _evaluate_quality(policy, res)
    sec_fail_on = policy.get("security", {}).get("fail_on", ["critical", "high"])
    sec_failure = should_fail(res["summary"]["by_severity"], sec_fail_on)

    if args.format == "json":
        out = json.dumps(
            {
                **res,
                "policy": {
                    "name": policy.get("name", "custom"),
                    "security_fail_on": sec_fail_on,
                    "intel": policy.get("security", {}).get("intel", {}),
                },
                "quality_failures": quality_failures,
            },
            indent=2,
        )
    elif args.format == "markdown":
        out = _to_markdown(res)
        if quality_failures:
            out += "\n\n## Quality Gate Failures\n" + "\n".join(f"- {x}" for x in quality_failures)
    else:
        out = f"SkillLint: scanned {res['summary']['files_scanned']} files, findings={res['summary']['findings_total']}, quality={res['summary']['quality_overall']}"
        if quality_failures:
            out += f" | quality_failures={len(quality_failures)}"

    if args.output:
        Path(args.output).write_text(out, encoding="utf-8")
    else:
        print(out)

    if not args.no_fail and (sec_failure or bool(quality_failures)):
        return 2
    return 0


def cmd_fix(args: argparse.Namespace) -> int:
    target = Path(args.target)
    changed = 0
    total_actions = 0
    for path in iter_candidate_files(target):
        actions = apply_safe_fixes(path)
        if actions:
            changed += 1
            total_actions += len(actions)
            if args.verbose:
                print(f"fixed {path}: {', '.join(actions)}")
    print(f"SkillLint fix: updated {changed} file(s), applied {total_actions} safe fix action(s)")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="skilllint", description="Offline quality + security linter for AI skills")
    sp = p.add_subparsers(dest="command", required=True)

    scan = sp.add_parser("scan", help="Scan a file or directory")
    scan.add_argument("target", help="File or directory to scan")
    scan.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    scan.add_argument("-o", "--output", help="Write output to file")
    scan.add_argument("--policy", help="Path to policy file (yaml/json)")
    scan.add_argument("--no-fail", action="store_true", help="Never return non-zero exit code")
    scan.set_defaults(func=cmd_scan)

    fix = sp.add_parser("fix", help="Apply safe auto-fixes")
    fix.add_argument("target", help="File or directory to fix")
    fix.add_argument("--verbose", action="store_true")
    fix.set_defaults(func=cmd_fix)
    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
