#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml"]
# ///
"""Validate a session-recipe recipe.yaml against references/recipe-format.md.

Usage:
    uv run scripts/validate-recipe.py <recipe.yaml> [--check-integrity] [--root DIR]

Checks (always):
    - top-level structure, recipe metadata, log_files entries
    - every step has all packet fields plus a complete provenance receipt
    - confidence gate: verified requires log_refs into a declared log file
    - log_refs syntax: <log basename>#L<start>-L<end>
    - dependencies reference earlier steps only; replay.order covers every step
      and respects dependencies; replay.mode exact requires commits on every step
    - heuristic secret scan over provenance strings (warning only)

Checks (--check-integrity, needs log files on disk):
    - re-hash each source.log_files entry and compare to its recorded sha256
    - log_refs line ranges fall within the referenced file

Exit codes: 0 clean, 1 errors, 2 integrity mismatch only (refs downgraded,
replay may proceed with the downgrade reported).
"""

import argparse
import hashlib
import re
import sys
from pathlib import Path

import yaml

PACKET_FIELDS = [
    "unit_id", "objective", "capability", "allowed_scope", "forbidden_scope",
    "non_goals", "dependencies", "acceptance_criteria", "verification",
    "return_contract",
]
PROVENANCE_FIELDS = [
    "prompt_excerpt", "changed_files", "commands", "commits", "log_refs",
    "validation", "confidence",
]
VALIDATION_FIELDS = {"command", "commit", "result"}
LOG_REF_RE = re.compile(r"^(?P<name>[^#]+)#L(?P<start>\d+)-L(?P<end>\d+)$")
SECRET_RE = re.compile(
    r"(?i)(api[_-]?key|secret|token|password|passwd|authorization|bearer)\s*[=:]\s*\S+"
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("recipe")
    ap.add_argument("--check-integrity", action="store_true")
    ap.add_argument("--root", default=".", help="directory log_files paths are relative to")
    opts = ap.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    integrity_failed = False

    try:
        doc = yaml.safe_load(Path(opts.recipe).read_text())
    except (OSError, yaml.YAMLError) as e:
        print(f"ERROR: cannot load recipe: {e}")
        return 1

    if not isinstance(doc, dict) or set(doc) != {"recipe", "steps", "replay"}:
        print(f"ERROR: top-level keys must be exactly recipe/steps/replay, got {sorted(doc) if isinstance(doc, dict) else type(doc).__name__}")
        return 1

    meta, steps, replay = doc["recipe"], doc["steps"], doc["replay"]
    if not isinstance(meta, dict):
        errors.append(f"recipe must be a mapping, got {type(meta).__name__}")
        meta = {}
    if not isinstance(replay, dict):
        errors.append(f"replay must be a mapping, got {type(replay).__name__}")
        replay = {}

    # --- recipe metadata ---
    for f in ["name", "created", "source", "environment"]:
        if f not in meta:
            errors.append(f"recipe.{f} missing")
    source = meta.get("source") if isinstance(meta.get("source"), dict) else {}
    for f in ["session_ids", "log_files", "repo", "base_commit"]:
        if f not in source:
            errors.append(f"recipe.source.{f} missing")
    log_files = source.get("log_files") if isinstance(source.get("log_files"), list) else []
    log_names: dict[str, dict] = {}
    for i, lf in enumerate(log_files):
        if not isinstance(lf, dict) or set(lf) != {"path", "sha256"}:
            errors.append(f"recipe.source.log_files[{i}] must be {{path, sha256}}, got {lf!r}")
            continue
        name = Path(lf["path"]).name
        if name in log_names:
            errors.append(f"recipe.source.log_files[{i}]: duplicate basename `{name}` — log_refs address files by basename, so each entry needs a unique one (rename merged copies, e.g. <id>.legacy.jsonl)")
            continue
        log_names[name] = lf

    # --- steps ---
    if not isinstance(steps, list) or not steps:
        errors.append("steps must be a non-empty list")
        steps = []
    seen: set[str] = set()
    for i, s in enumerate(steps):
        if not isinstance(s, dict):
            errors.append(f"steps[{i}] must be a mapping, got {type(s).__name__}")
            continue
        sid = s.get("unit_id", "<missing unit_id>")
        for f in PACKET_FIELDS:
            if f not in s:
                errors.append(f"{sid}: packet field `{f}` missing")
        if not re.fullmatch(r"R\d+", str(sid)):
            errors.append(f"{sid}: unit_id must match R<number>")
        for dep in s.get("dependencies") or []:
            if dep not in seen:
                errors.append(f"{sid}: dependency `{dep}` is not an earlier step")
        if sid in seen:
            errors.append(f"{sid}: duplicate unit_id")
        seen.add(sid)

        prov = s.get("provenance")
        if not isinstance(prov, dict):
            errors.append(f"{sid}: provenance block missing")
            continue
        for f in PROVENANCE_FIELDS:
            if f not in prov:
                errors.append(f"{sid}: provenance.{f} missing")
        val = prov.get("validation")
        if not isinstance(val, dict) or set(val) != VALIDATION_FIELDS:
            errors.append(f"{sid}: provenance.validation must have exactly {sorted(VALIDATION_FIELDS)}")
        conf = prov.get("confidence")
        if conf not in ("verified", "unverified"):
            errors.append(f"{sid}: confidence must be verified|unverified, got {conf!r}")
        refs = prov.get("log_refs") or []
        if not isinstance(refs, list):
            errors.append(f"{sid}: log_refs must be a list, got {type(refs).__name__}")
            refs = []
        if conf == "verified" and not refs:
            errors.append(f"{sid}: confidence verified requires log_refs (evidence gate)")
        for ref in refs:
            m = LOG_REF_RE.match(str(ref))
            if not m:
                errors.append(f"{sid}: log_ref `{ref}` not in <basename>#L<start>-L<end> form")
                continue
            if m["name"] not in log_names:
                errors.append(f"{sid}: log_ref `{ref}` points outside source.log_files")
            elif int(m["start"]) < 1:
                errors.append(f"{sid}: log_ref `{ref}` uses L0 — line refs are 1-based")
            elif int(m["start"]) > int(m["end"]):
                errors.append(f"{sid}: log_ref `{ref}` has start > end")
        val_fields = val if isinstance(val, dict) else {}
        for text in [*(prov.get("commands") or []), prov.get("prompt_excerpt") or "",
                     val_fields.get("command") or "", val_fields.get("result") or ""]:
            if SECRET_RE.search(str(text)):
                warnings.append(f"{sid}: possible secret value in provenance: `{str(text)[:60]}...`")

    # --- replay ---
    order = replay.get("order") or []
    ids = [s.get("unit_id") for s in steps]
    if sorted(map(str, order)) != sorted(map(str, ids)):
        errors.append(f"replay.order {order} does not cover exactly the step ids {ids}")
    else:
        pos = {sid: i for i, sid in enumerate(order)}
        for s in steps:
            for dep in s.get("dependencies") or []:
                if pos.get(dep, -1) > pos.get(s["unit_id"], -1):
                    errors.append(f"replay.order runs {s['unit_id']} before its dependency {dep}")
    mode = replay.get("mode")
    if mode not in ("intent", "exact"):
        errors.append(f"replay.mode must be intent|exact, got {mode!r}")
    if mode == "exact":
        for s in steps:
            if not (s.get("provenance") or {}).get("commits"):
                errors.append(f"{s.get('unit_id')}: replay.mode exact requires provenance.commits on every step")

    # --- integrity ---
    if opts.check_integrity:
        root = Path(opts.root)
        for lf in log_files:
            if not isinstance(lf, dict) or "path" not in lf:
                continue
            p = root / lf["path"]
            if not p.exists():
                warnings.append(f"integrity: {lf['path']} not on disk — skipped (refs unverifiable, not downgraded)")
                continue
            digest = hashlib.sha256(p.read_bytes()).hexdigest()
            if digest != lf.get("sha256"):
                integrity_failed = True
                warnings.append(f"integrity: {lf['path']} sha256 mismatch — downgrade every log_ref into this file to unverified")
                continue
            line_count = len(p.read_text(errors="replace").splitlines())
            for s in steps:
                for ref in (s.get("provenance") or {}).get("log_refs") or []:
                    m = LOG_REF_RE.match(str(ref))
                    if m and m["name"] == p.name and int(m["end"]) > line_count:
                        errors.append(f"{s.get('unit_id')}: log_ref `{ref}` exceeds file length {line_count}")

    for w in warnings:
        print(f"WARN: {w}")
    for e in errors:
        print(f"ERROR: {e}")
    if errors:
        print(f"FAIL: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1
    if integrity_failed:
        print("INTEGRITY-MISMATCH: schema valid, but ground-truth hash changed — report the downgrade before replay")
        return 2
    print(f"OK: {len(steps)} step(s), {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
