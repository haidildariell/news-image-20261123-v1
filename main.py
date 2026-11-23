#!/usr/bin/env python3
"""Entrypoint for news-image-20261123 v1.

The broadsheet was drawn at build time by render.py (Pillow) and shipped in
this repository as entry.png. This program only copies that image to the
output directory, using the standard library alone, so both runs write the
same bytes.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
