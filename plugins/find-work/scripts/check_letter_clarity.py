#!/usr/bin/env python3
"""Deterministic clarity checks for a cover letter, run before presenting it for approval.

Reads a plain letter, or the cover-letter section of an application wording file such as
approved_application_wording.md. The body is the text between the salutation ("Dear ...") and the
sign-off ("Sincerely"). These checks back up, but never replace, the semantic drafting checks.

Errors (exit code 1):
- Body longer than the ceiling.
- Stock phrases that carry no evidence, such as "excited to apply" or "proven track record".
- Punctuation the candidate chose to avoid, only when its flag is passed.

Warnings:
- Body outside the target word range, or more paragraphs than allowed.
- Soft filler words such as "leverage" or "dynamic".
- Eight or more consecutive words shared with the resume in the same file, which suggests the letter
  is retelling a bullet.

Usage:
    check_letter_clarity.py applications/<Company>/approved_application_wording.md
    check_letter_clarity.py letter.txt --target 150 250 --ceiling 275 --no-em-dash --no-colon
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

BANNED = [
    "excited to apply", "thrilled to apply", "writing to apply", "writing to express my interest",
    "passionate about", "i am passionate", "i'm passionate", "proven track record", "results-driven",
    "results driven", "fast-paced environment", "thrive in fast-paced", "great fit", "perfect fit",
    "ideal candidate", "synergy", "synergies", "think outside the box", "hit the ground running",
    "team player", "detail-oriented", "self-starter", "go-getter", "wealth of experience",
]
SOFT = ["leverage", "leveraging", "dynamic", "seasoned", "robust", "cutting-edge", "world-class",
        "best-in-class", "innovative solutions", "utilize", "spearheaded"]
SHINGLE = 8


def section(text: str, names: tuple[str, ...]) -> str:
    """Return the text under the first heading whose title contains one of the names."""
    lines = text.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("#") and any(n in line.lower() for n in names):
            start = i + 1
            level = len(line) - len(line.lstrip("#"))
            break
    if start is None:
        return ""
    end = next((j for j in range(start, len(lines))
                if lines[j].startswith("#") and len(lines[j]) - len(lines[j].lstrip("#")) <= level), len(lines))
    return "\n".join(lines[start:end])


def letter_parts(text: str) -> tuple[str, str]:
    """The whole letter and its body, between the salutation and the sign-off."""
    letter = section(text, ("cover-letter", "cover letter")) or text
    lines = letter.splitlines()
    first = next((i for i, l in enumerate(lines) if re.match(r"\s*(dear|hello|hi)\b", l, re.I)), -1)
    last = next((i for i, l in enumerate(lines) if re.match(r"\s*(sincerely|best regards|regards|thank you),?\s*$", l, re.I)),
                len(lines))
    return letter, "\n".join(lines[first + 1:last]).strip()


def words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9][A-Za-z0-9'’%$.,-]*", text)


def plain_words(text: str) -> list[str]:
    return [re.sub(r"[^a-z0-9%$]", "", w.lower()) for w in words(text)]


def check(text: str, target=(175, 300), ceiling: int = 350, max_paragraphs: int = 4,
          avoid: frozenset[str] = frozenset()) -> tuple[list[str], list[str], dict]:
    low, high = target
    letter, body = letter_parts(text)
    errors, warnings = [], []
    if not body:
        return ["No letter body found between a salutation and a sign-off."], [], {}
    count = len(words(body))
    paragraphs = [p for p in re.split(r"\n\s*\n", body) if p.strip()]
    stats = {"body_words": count, "body_paragraphs": len(paragraphs)}
    if count > ceiling:
        errors.append(f"Body is {count} words, over the {ceiling}-word ceiling.")
    elif not low <= count <= high:
        warnings.append(f"Body is {count} words. The target is {low} to {high}.")
    if len(paragraphs) > max_paragraphs:
        warnings.append(f"Body has {len(paragraphs)} paragraphs. Use at most {max_paragraphs}.")
    lowered = letter.lower().replace("’", "'")
    for phrase in BANNED:
        if phrase in lowered:
            errors.append(f"Stock phrase '{phrase}'. Replace it with specific evidence or cut it.")
    for word in SOFT:
        if re.search(rf"\b{re.escape(word)}\b", lowered):
            warnings.append(f"Soft word '{word}'. Prefer a plain, specific word.")
    if "em-dash" in avoid and "—" in letter:
        errors.append("Em dash found. Use a comma or a period.")
    for line in letter.splitlines():
        visible = re.sub(r"\]\([^)]*\)", "]", line)  # link destinations are exempt
        visible = re.sub(r"https?://\S+", "", visible)
        if "semicolon" in avoid and ";" in visible:
            errors.append(f"Semicolon in '{line.strip()[:60]}'. Rewrite as two sentences or use a comma.")
        if "colon" in avoid and ":" in visible:
            errors.append(f"Colon in '{line.strip()[:60]}'.")
    resume = section(text, ("resume",))
    if resume:
        rw, bw = plain_words(resume), plain_words(body)
        shingles = {tuple(rw[i:i + SHINGLE]) for i in range(len(rw) - SHINGLE + 1)}
        repeated = sorted({" ".join(bw[i:i + SHINGLE]) for i in range(len(bw) - SHINGLE + 1)
                           if tuple(bw[i:i + SHINGLE]) in shingles})
        if repeated:
            warnings.append(f"{len(repeated)} eight-word runs repeat the resume, for example '{repeated[0]}'. "
                            "Explain the judgment behind the work instead of retelling the bullet.")
    return errors, warnings, stats


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("path", type=Path)
    parser.add_argument("--target", nargs=2, type=int, default=(175, 300), metavar=("LOW", "HIGH"),
                        help="target body word range, default 175 300")
    parser.add_argument("--ceiling", type=int, default=350, help="body word count that is an error, default 350")
    parser.add_argument("--max-paragraphs", type=int, default=4)
    for mark in ("em-dash", "semicolon", "colon"):
        parser.add_argument(f"--no-{mark}", action="append_const", const=mark, dest="avoid",
                            help=f"treat any {mark.replace('-', ' ')} as an error")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    errors, warnings, stats = check(args.path.read_text(encoding="utf-8-sig"), tuple(args.target), args.ceiling,
                                    args.max_paragraphs, frozenset(args.avoid or ()))
    print(f"Letter clarity: {stats.get('body_words', 0)} body words, "
          f"{stats.get('body_paragraphs', 0)} body paragraphs.")
    for e in errors:
        print(f"ERROR {e}")
    for w in warnings:
        print(f"WARNING {w}")
    if not errors and not warnings:
        print("No issues found.")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
