from __future__ import annotations

import re
from pathlib import Path


KEY_LINE_RE = re.compile(r"^(\s*)([^\s:#][^:#]*?)\s*:(\s*)(.*)$")
HAS_INDEX_RE = re.compile(r"^\d+\s")


def sanitize_loc_file(*, src: Path, dst: Path, force_index: bool) -> None:
    """
    - Read as utf-8-sig (tolerates BOM)
    - Strip stray BOM chars (handles double-BOM files)
    - Optionally force ':0' index where missing
    - Write as utf-8-sig
    """
    text = src.read_text(encoding="utf-8-sig", errors="replace")
    text = text.lstrip("\ufeff")

    out_lines: list[str] = []
    for raw in text.splitlines():
        line = raw.lstrip("\ufeff")
        m = KEY_LINE_RE.match(line)
        if not m:
            out_lines.append(line)
            continue

        indent, key, sp, rest = m.groups()

        # keep header like: l_russian:
        if indent == "" and key.startswith("l_") and rest.strip() == "":
            out_lines.append(f"{key}:")
            continue

        if force_index:
            if HAS_INDEX_RE.match(rest):
                out_lines.append(line)
            else:
                out_lines.append(f"{indent}{key}:0{sp}{rest}")
        else:
            out_lines.append(line)

    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("\n".join(out_lines) + "\n", encoding="utf-8-sig")


def main() -> int:
    repo = Path(__file__).resolve().parents[1]  # .../vic3_mods
    repo_out = repo.parent / "vic3_mods_out"

    bpm_ru = repo_out / "BPM" / "localization" / "russian"
    compatch_ru = repo / "_bpm" / "bpm+tgr done" / "localization" / "russian"

    src_cab = bpm_ru / "bpm_cab_l_russian.yml"
    src_mods = bpm_ru / "BPM_cab_modifiers_l_russian.yml"
    if not src_cab.exists():
        raise SystemExit(f"Missing BPM source file: {src_cab}")
    if not src_mods.exists():
        raise SystemExit(f"Missing BPM source file: {src_mods}")

    # Overwrite-by-path (so the broken BPM RU files are never parsed)
    sanitize_loc_file(
        src=src_cab,
        dst=compatch_ru / "bpm_cab_l_russian.yml",
        force_index=True,
    )
    sanitize_loc_file(
        src=src_mods,
        dst=compatch_ru / "BPM_cab_modifiers_l_russian.yml",
        force_index=False,
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
