#!/usr/bin/env python3
"""Write summary.html from summary.src.html by replacing each {{IMG:<name>}}
placeholder with a base64 data URI of <dir>/img/<name>.jpg.

usage: embed.py <video-dir>

Exits with an error when an image is missing or any {{...}} is left over.
"""
import base64
import pathlib
import re
import sys


def main(root):
    d = pathlib.Path(root)
    src = (d / "summary.src.html").read_text(encoding="utf-8")

    def sub(m):
        path = d / "img" / f"{m.group(1)}.jpg"
        if not path.is_file():
            sys.exit(f"missing image: {path}")
        return "data:image/jpeg;base64," + base64.b64encode(path.read_bytes()).decode()

    out = re.sub(r"\{\{IMG:([\w-]+)\}\}", sub, src)
    left = re.findall(r"\{\{[^}]*\}\}", out)
    if left:
        sys.exit(f"placeholders left: {left}")
    (d / "summary.html").write_text(out, encoding="utf-8")
    print(f"{len(out) // 1024} KB, {out.count('data:image/jpeg')} images")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: embed.py <video-dir>")
    main(sys.argv[1])
