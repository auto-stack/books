#!/usr/bin/env python3
"""
Sync TAPL listing code into book chapters.

For each <Listing number="X-Y"> tag in chapter .md/.cn.md files,
replaces the ```auto, ```rust, ```python, ```c, and ```typescript code blocks
with content from the corresponding listing directory.

Usage:
    python scripts/sync_tapl_listings.py [--dry-run] [--chapters ch01 ch02 ...]

Source of truth: listings/chXX/listing-X-Y/main.at and main.expected.*
"""

import os
import re
import sys
import argparse
from pathlib import Path

BOOK_DIR = Path(__file__).parent.parent / "tapl"
LISTINGS_DIR = BOOK_DIR / "listings"

# Order matters — must match the order of code blocks in <Listing> tags
LANG_BLOCKS = [
    ("auto", None),                    # main.at (source, no .expected)
    ("rust", "main.expected.rs"),      # a2r transpiler output
    ("python", "main.expected.py"),    # a2p transpiler output
    ("c", "main.expected.c"),          # a2c transpiler output
    ("typescript", "main.expected.ts"), # a2ts transpiler output
]


def find_listing_dir(listing_number: str) -> Path | None:
    """Find listing directory for a given number like '01-01' or '2-1'."""
    parts = listing_number.split("-")
    if len(parts) != 2:
        return None
    ch = int(parts[0])
    num = int(parts[1])
    ch_dir = LISTINGS_DIR / f"ch{ch:02d}"
    listing_dir = ch_dir / f"listing-{ch:02d}-{num:02d}"
    if listing_dir.is_dir():
        return listing_dir
    return None


def read_listing_code(listing_dir: Path) -> dict[str, str]:
    """Read all code files from a listing directory.

    Returns dict mapping language name to code string.
    """
    result = {}

    # Read Auto source
    at_file = listing_dir / "main.at"
    if not at_file.exists():
        return result

    auto_code = at_file.read_text(encoding="utf-8").rstrip()
    # Strip comment lines from the top (listing metadata comments)
    lines = auto_code.split("\n")
    while lines and lines[0].startswith("//"):
        lines.pop(0)
    while lines and lines[0].strip() == "":
        lines.pop(0)
    result["auto"] = "\n".join(lines)

    # Read transpiler outputs
    for lang, filename in LANG_BLOCKS:
        if filename is None:
            continue  # auto already handled
        filepath = listing_dir / filename
        if filepath.exists():
            result[lang] = filepath.read_text(encoding="utf-8").rstrip()

    return result


def replace_listing_block(content: str, dry_run: bool = False) -> tuple[str, list[str]]:
    """Find all <Listing> blocks and replace code blocks inside them."""
    changes = []
    result = content

    pattern = re.compile(
        r'(<Listing\s+number="([^"]+)"[^>]*>\n)'
        r'(.*?)'
        r'(</Listing>)',
        re.DOTALL,
    )

    def replacer(match: re.Match) -> str:
        header = match.group(1)
        listing_num = match.group(2)
        body = match.group(3)
        footer = match.group(4)

        listing_dir = find_listing_dir(listing_num)
        if listing_dir is None:
            return match.group(0)

        code = read_listing_code(listing_dir)
        if not code:
            return match.group(0)

        new_body = body
        for lang, _ in LANG_BLOCKS:
            if lang not in code:
                continue
            lang_code = code[lang]
            new_body = re.sub(
                rf"(```{lang}[^\n]*\n)(.*?)(```)",
                lambda m, c=lang_code: f"{m.group(1)}{c}\n{m.group(3)}",
                new_body,
                count=1,
                flags=re.DOTALL,
            )

        if new_body != body:
            changes.append(
                f"  Updated Listing {listing_num} from {listing_dir.relative_to(LISTINGS_DIR.parent)}"
            )

        return f"{header}{new_body}{footer}"

    result = pattern.sub(replacer, content)
    return result, changes


def process_chapter(chapter: str, dry_run: bool = False) -> list[str]:
    """Process a chapter's .md and .cn.md files."""
    all_changes = []

    for suffix in [".md", ".cn.md"]:
        pattern_match = None
        for f in BOOK_DIR.glob(f"ch{chapter}*"):
            if suffix == ".md":
                if f.name.endswith(".md") and not f.name.endswith(".cn.md"):
                    pattern_match = f
                    break
            else:
                if f.name.endswith(suffix):
                    pattern_match = f
                    break

        if pattern_match is None:
            continue

        filepath = pattern_match
        content = filepath.read_text(encoding="utf-8")
        new_content, changes = replace_listing_block(content, dry_run)

        if changes:
            all_changes.extend([f"{filepath.name}:"] + changes)
            if not dry_run:
                filepath.write_text(new_content, encoding="utf-8")

    return all_changes


def main():
    parser = argparse.ArgumentParser(description="Sync TAPL listing code into book chapters")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--chapters", nargs="*", help="Chapter numbers to process (e.g., 01 02 03)")
    args = parser.parse_args()

    if args.chapters:
        chapters = args.chapters
    else:
        chapters = sorted(
            d.name[2:]
            for d in LISTINGS_DIR.iterdir()
            if d.is_dir() and d.name.startswith("ch")
        )

    print(f"Syncing TAPL listings for chapters: {chapters}")
    if args.dry_run:
        print("(DRY RUN - no files will be modified)")
    print()

    total_changes = 0
    for ch in chapters:
        changes = process_chapter(ch, args.dry_run)
        if changes:
            print("\n".join(changes))
            total_changes += len([c for c in changes if c.startswith("  Updated")])

    if total_changes == 0:
        print("All listings are already in sync.")
    else:
        action = "Would update" if args.dry_run else "Updated"
        print(f"\n{action} {total_changes} listing(s).")


if __name__ == "__main__":
    main()
