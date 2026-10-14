#!/usr/bin/env python3
"""Turn a YouTube json3 caption file into a transcript with one line per
30-second block, each prefixed with [MM:SS] or [H:MM:SS]."""
import json
import sys

BLOCK = 30


def stamp(seconds):
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def main(src, dst):
    events = json.load(open(src, encoding="utf-8")).get("events", [])
    blocks = {}
    for event in events:
        text = "".join(seg.get("utf8", "") for seg in event.get("segs", []))
        text = text.replace("\n", " ").strip()
        if text:
            key = event["tStartMs"] // 1000 // BLOCK
            blocks.setdefault(key, []).append(text)
    lines = [f"[{stamp(k * BLOCK)}] " + " ".join(v) for k, v in sorted(blocks.items())]
    open(dst, "w", encoding="utf-8").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: transcript.py <captions.json3> <transcript.txt>")
    main(sys.argv[1], sys.argv[2])
