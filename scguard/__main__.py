"""Command-line entry points for the public core implementation."""

from pathlib import Path
import argparse
import json
import sys
from .reference import DATA, read, tasks, verify_manifest


def main():
    parser = argparse.ArgumentParser(prog="python -m scguard")
    sub = parser.add_subparsers(dest="command", required=True)
    check = sub.add_parser("verify-data", help="Verify bundled reference hashes")
    check.add_argument("--data", type=Path, default=DATA)
    replay = sub.add_parser("replay", help="Replay saved native/guard records and certificates")
    replay.add_argument("--cohort", choices=["all", "writer", "cross-family"], default="all")
    replay.add_argument("--data", type=Path, default=DATA)
    replay.add_argument("--output", type=Path)
    figures = sub.add_parser(
        "figures", help="Render figures with the user-adjusted architecture layout"
    )
    figures.add_argument("--output", type=Path, default=Path("build/figures"))
    infer = sub.add_parser(
        "infer", help="Infer a cross-family candidate from bundled native observations"
    )
    infer.add_argument("--task", required=True)
    infer.add_argument("--output", type=Path, required=True)
    kernel = sub.add_parser(
        "kernel", help="Construct and independently replay an affine guard certificate"
    )
    for name in ["left", "right"]:
        kernel.add_argument("--" + name, required=True)
    kernel.add_argument("--left-cfg", type=int, default=8)
    kernel.add_argument("--right-cfg", type=int, default=8)
    kernel.add_argument(
        "--observer", default="return", choices=["return", "first4", "last4", "buffer8", "full"]
    )
    kernel.add_argument("--output", type=Path)
    export = sub.add_parser(
        "export", help="Export a C guard from recorded source-qualified mixed models"
    )
    export.add_argument("--left", required=True)
    export.add_argument("--right", required=True)
    export.add_argument("--cohort", choices=["writer", "cross-family"], default="cross-family")
    export.add_argument("--output", type=Path, required=True)
    harness = sub.add_parser("harness", help="Emit source/model verification obligations")
    harness.add_argument("--task", required=True)
    harness.add_argument("--cohort", choices=["writer", "cross-family"], default="cross-family")
    harness.add_argument(
        "--route",
        choices=[
            "direct",
            "integer-prefix",
            "typed-conditional",
            "typed-bridge",
            "crc-step",
            "crc-stream",
            "crc-frame",
            "crc-dfcc-step",
            "adler-ranges",
        ],
        default="direct",
    )
    harness.add_argument("--output", type=Path, required=True)
    fields = sub.add_parser("read-fields", help="Interpret bound raw field-checker results")
    fields.add_argument("--folder", type=Path, required=True)
    fields.add_argument("--label", required=True)
    fields.add_argument("--engine", choices=["cbmc", "esbmc"], required=True)
    args = parser.parse_args()
    if args.command == "verify-data":
        result = verify_manifest(args.data)
    elif args.command == "figures":
        from .plotting.figures import render

        result = render(args.output)
    elif args.command == "infer":
        from .inference.fit import infer_reference

        verify_manifest()
        result = infer_reference(args.task)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result["model"], indent=2) + "\n", encoding="utf-8")
        result = {key: value for key, value in result.items() if key != "model"}
        result["output"] = str(args.output)
    else:
        from . import core

        if args.command == "read-fields":
            result = core.field_reader.fields(args.folder, args.label, args.engine)
        elif args.command == "replay":
            from . import replay

            integrity = verify_manifest(args.data)
            result = {"reference_integrity": integrity, "source_checker_jobs_executed": 0}
            if args.cohort in ["all", "writer"]:
                result["writer"] = replay.writer(args.data)
            if args.cohort in ["all", "cross-family"]:
                result["cross_family"] = replay.cross_family(args.data)
        else:
            verify_manifest()
            sources = tasks(
                "writer"
                if args.command in ["harness", "export"] and args.cohort == "writer"
                else "cross_family"
            )
            if args.command == "kernel":
                result = core.build_kernel(
                    sources[args.left]["model"],
                    sources[args.right]["model"],
                    args.left_cfg,
                    args.right_cfg,
                    args.observer,
                )
            elif args.command == "export":
                code = core.export_guard(sources[args.left]["model"], sources[args.right]["model"])
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(code, encoding="utf-8")
                result = {
                    "output": str(args.output),
                    "source_admission": "recorded source admission in the selected cohort source_tasks.json",
                }
            else:
                task = sources[args.task]
                code = core.source_harness(task["target"], task["model"], args.route)
                args.output.parent.mkdir(parents=True, exist_ok=True)
                args.output.write_text(code, encoding="utf-8")
                result = {
                    "output": str(args.output),
                    "route": args.route,
                    "next_step": "check the emitted obligations and route premises with the recorded C checker configuration",
                }
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if getattr(args, "output", None) and args.command in ["kernel", "replay"]:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    print(text, end="")


if __name__ == "__main__":
    main()
