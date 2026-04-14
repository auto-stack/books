#!/usr/bin/env python3
"""
Sync listing code into book chapters.

For each <Listing number="X-Y"> tag in chapter .md/.cn.md files,
replaces the ```auto and ```typescript code blocks with content from
the corresponding listing directory.

Usage:
    python scripts/sync_ts_listings.py [--dry-run] [--chapters ch01 ch02 ...]

Source of truth: listings/chXX/listing-X-Y/main.at and main.expected.ts
"""

import os
import re
import sys
import argparse
from pathlib import Path

BOOK_DIR = Path(__file__).parent.parent / "typescript"
LISTINGS_DIR = BOOK_DIR / "listings"


def find_listing_dir(listing_number: str) -> Path | None:
    """Find listing directory for a given number like '01-01' or '2-1'."""
    # Normalize: "2-1" -> "02-01", "1-1" -> "01-01"
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


def read_listing_code(listing_dir: Path) -> tuple[str, str] | None:
    """Read Auto and expected TypeScript code from listing directory."""
    at_file = listing_dir / "main.at"
    ts_file = listing_dir / "main.expected.ts"

    if not at_file.exists():
        return None

    auto_code = at_file.read_text(encoding="utf-8").rstrip()
    # Strip comment lines from the top (listing metadata comments)
    lines = auto_code.split("\n")
    while lines and lines[0].startswith("//"):
        lines.pop(0)
    # Remove leading empty lines
    while lines and lines[0].strip() == "":
        lines.pop(0)
    auto_code = "\n".join(lines)

    ts_code = ""
    if ts_file.exists():
        ts_code = ts_file.read_text(encoding="utf-8").rstrip()

    return auto_code, ts_code


def replace_listing_block(content: str, dry_run: bool = False) -> tuple[str, list[str]]:
    """
    Find all <Listing number="X-Y" ...>...</Listing> blocks and replace
    the ```auto and ```typescript code blocks inside them.
    """
    changes = []
    result = content

    # Match <Listing number="X-Y" ...>...</Listing>
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
            # No matching listing, keep as-is
            return match.group(0)

        code = read_listing_code(listing_dir)
        if code is None:
            return match.group(0)

        auto_code, ts_code = code

        # Replace ```auto block
        new_body = re.sub(
            r"(```auto[^\n]*\n)(.*?)(```)",
            lambda m: f"{m.group(1)}{auto_code}\n{m.group(3)}",
            body,
            count=1,
            flags=re.DOTALL,
        )

        # Replace ```typescript block (if exists)
        if ts_code:
            new_body = re.sub(
                r"(```typescript[^\n]*\n)(.*?)(```)",
                lambda m: f"{m.group(1)}{ts_code}\n{m.group(3)}",
                new_body,
                count=1,
                flags=re.DOTALL,
            )

        if new_body != body:
            chapter_file = "unknown"
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
        # Find the chapter file
        pattern_match = None
        for f in BOOK_DIR.glob(f"ch{chapter}*"):
            # Match exact suffix: .md must NOT end with .cn.md
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
    parser = argparse.ArgumentParser(description="Sync listing code into book chapters")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without writing")
    parser.add_argument("--chapters", nargs="*", help="Chapter numbers to process (e.g., 01 02 03)")
    args = parser.parse_args()

    if args.chapters:
        chapters = args.chapters
    else:
        # Auto-detect chapters from listings directory
        chapters = sorted(
            d.name[2:]  # "ch01" -> "01"
            for d in LISTINGS_DIR.iterdir()
            if d.is_dir() and d.name.startswith("ch")
        )

    print(f"Syncing listings for chapters: {chapters}")
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
