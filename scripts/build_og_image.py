#!/usr/bin/env python3
"""Generate og-default.png — a 1200×630 social preview card.

Pure-stdlib PNG generation: no PIL, no Cairo, no external deps. Builds
a brand-coloured card with a centred title and a thin accent bar. The
output is referenced from every page's `<meta property="og:image">`.

Idempotent: only writes the file if its bytes differ from the current
file on disk.

Usage::

    python3 scripts/build_og_image.py
"""

from __future__ import annotations

import struct
import sys
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "og-default.png"

WIDTH = 1200
HEIGHT = 630

# Brand palette.
BG = (10, 11, 16)        # near-black background
ACCENT = (37, 99, 235)   # blue-600
INK = (245, 245, 248)    # near-white text
INK_MUTE = (160, 165, 180)

# 7×7 pixel font for ASCII glyphs. Each glyph is a list of 7 strings of
# length 7 ('#' = ink, '.' = bg). Subset is enough for the title/subtitle.
GLYPHS: dict[str, list[str]] = {
    "A": ["..###..", ".#...#.", "#.....#", "#######", "#.....#", "#.....#", "#.....#"],
    "B": ["######.", "#.....#", "#.....#", "######.", "#.....#", "#.....#", "######."],
    "C": [".#####.", "#.....#", "#......", "#......", "#......", "#.....#", ".#####."],
    "D": ["#####..", "#....#.", "#.....#", "#.....#", "#.....#", "#....#.", "#####.."],
    "E": ["#######", "#......", "#......", "#####..", "#......", "#......", "#######"],
    "F": ["#######", "#......", "#......", "#####..", "#......", "#......", "#......"],
    "G": [".#####.", "#.....#", "#......", "#..####", "#.....#", "#.....#", ".#####."],
    "H": ["#.....#", "#.....#", "#.....#", "#######", "#.....#", "#.....#", "#.....#"],
    "I": ["#######", "...#...", "...#...", "...#...", "...#...", "...#...", "#######"],
    "J": ["#######", "....#..", "....#..", "....#..", "....#..", "#...#..", ".###..."],
    "K": ["#....#.", "#...#..", "#..#...", "###....", "#..#...", "#...#..", "#....#."],
    "L": ["#......", "#......", "#......", "#......", "#......", "#......", "#######"],
    "M": ["#.....#", "##...##", "#.#.#.#", "#..#..#", "#.....#", "#.....#", "#.....#"],
    "N": ["#.....#", "##....#", "#.#...#", "#..#..#", "#...#.#", "#....##", "#.....#"],
    "O": [".#####.", "#.....#", "#.....#", "#.....#", "#.....#", "#.....#", ".#####."],
    "P": ["######.", "#.....#", "#.....#", "######.", "#......", "#......", "#......"],
    "Q": [".#####.", "#.....#", "#.....#", "#.....#", "#...#.#", "#....#.", ".####.#"],
    "R": ["######.", "#.....#", "#.....#", "######.", "#..#...", "#...#..", "#....#."],
    "S": [".#####.", "#......", "#......", ".#####.", "......#", "......#", "######."],
    "T": ["#######", "...#...", "...#...", "...#...", "...#...", "...#...", "...#..."],
    "U": ["#.....#", "#.....#", "#.....#", "#.....#", "#.....#", "#.....#", ".#####."],
    "V": ["#.....#", "#.....#", "#.....#", "#.....#", "#.....#", ".#...#.", "..###.."],
    "W": ["#.....#", "#.....#", "#.....#", "#..#..#", "#.#.#.#", "##...##", "#.....#"],
    "X": ["#.....#", ".#...#.", "..#.#..", "...#...", "..#.#..", ".#...#.", "#.....#"],
    "Y": ["#.....#", ".#...#.", "..#.#..", "...#...", "...#...", "...#...", "...#..."],
    "Z": ["#######", ".....#.", "....#..", "...#...", "..#....", ".#.....", "#######"],
    "0": [".#####.", "#....##", "#...#.#", "#..#..#", "#.#...#", "##....#", ".#####."],
    "1": [".###...", "#..#...", "...#...", "...#...", "...#...", "...#...", "#######"],
    "2": [".#####.", "#.....#", ".....#.", "....#..", "...#...", "..#....", "#######"],
    "3": ["######.", ".....#.", "....#..", "...##..", ".....#.", "#....#.", "######."],
    "4": ["....##.", "...#.#.", "..#..#.", ".#...#.", "#######", ".....#.", ".....#."],
    "5": ["#######", "#......", "######.", ".....#.", ".....#.", "#....#.", ".####.."],
    "6": [".####..", "#.....#", "#......", "######.", "#.....#", "#.....#", ".#####."],
    "7": ["#######", ".....#.", "....#..", "...#...", "..#....", ".#.....", "#......"],
    "8": [".#####.", "#.....#", "#.....#", ".#####.", "#.....#", "#.....#", ".#####."],
    "9": [".#####.", "#.....#", "#.....#", ".######", ".....#.", "#....#.", ".####.."],
    " ": [".......", ".......", ".......", ".......", ".......", ".......", "......."],
    ".": ["......", "......", "......", "......", "......", "..##..", "..##.."],
    "&": [".###...", "#...#..", "#...#..", ".###...", "#..#.#.", "#...#..", ".###.#."],
    "+": ["......", "...#..", "...#..", ".#####", "...#..", "...#..", "......"],
    "-": ["......", "......", "......", "######", "......", "......", "......"],
    "/": ["......", ".....#", "....#.", "...#..", "..#...", ".#....", "#....."],
    ":": ["......", "..##..", "..##..", "......", "..##..", "..##..", "......"],
}


def _scale_glyph(glyph: list[str], scale: int) -> list[str]:
    """Scale a glyph by integer factor (each pixel becomes a scale×scale square)."""
    out: list[str] = []
    for row in glyph:
        scaled_row = "".join(c * scale for c in row)
        out.extend([scaled_row] * scale)
    return out


def _draw_text(
    pixels: list[list[tuple[int, int, int]]],
    text: str,
    x: int,
    y: int,
    color: tuple[int, int, int],
    scale: int = 1,
) -> int:
    """Draw text starting at (x, y). Returns the next x position after the text."""
    cur_x = x
    glyph_w = 7
    glyph_h = 7
    space = max(1, scale)
    for ch in text.upper():
        glyph = GLYPHS.get(ch, GLYPHS[" "])
        scaled = _scale_glyph(glyph, scale)
        for row_idx, row in enumerate(scaled):
            for col_idx, c in enumerate(row):
                if c == "#":
                    px = cur_x + col_idx
                    py = y + row_idx
                    if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                        pixels[py][px] = color
        cur_x += glyph_w * scale + space * scale
    return cur_x


def _text_width(text: str, scale: int) -> int:
    glyph_w = 7
    space = max(1, scale)
    return len(text) * (glyph_w * scale + space * scale)


def build_png() -> bytes:
    pixels: list[list[tuple[int, int, int]]] = [
        [BG for _ in range(WIDTH)] for _ in range(HEIGHT)
    ]

    # Top accent bar.
    for y in range(0, 8):
        for x in range(WIDTH):
            pixels[y][x] = ACCENT

    # Logo dot + brand name.
    dot_x = 80
    dot_y = 88
    dot_r = 14
    for dy in range(-dot_r, dot_r + 1):
        for dx in range(-dot_r, dot_r + 1):
            if dx * dx + dy * dy <= dot_r * dot_r:
                px = dot_x + dx
                py = dot_y + dy
                if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                    pixels[py][px] = ACCENT
    _draw_text(pixels, "ALEX VALUEV", dot_x + 36, dot_y - 14, INK, scale=3)

    # Title — wrap at ~24 chars per line. We pre-split.
    title_lines = ["SENIOR AI", "PRODUCT MANAGER", "& CAREER COACH"]
    line_height = 7 * 8 + 18  # 7 px glyph * scale 8 + leading
    title_y = 200
    for i, line in enumerate(title_lines):
        scale = 8 if len(line) <= 18 else 7
        w = _text_width(line, scale)
        x = (WIDTH - w) // 2
        _draw_text(pixels, line, x, title_y + i * line_height, INK, scale=scale)

    # Subtitle.
    subtitle = "PORTFOLIO  +  RESEARCH  +  COACHING"
    sub_scale = 3
    sw = _text_width(subtitle, sub_scale)
    sx = (WIDTH - sw) // 2
    sy = HEIGHT - 100
    _draw_text(pixels, subtitle, sx, sy, INK_MUTE, scale=sub_scale)

    # Domain pin.
    domain = "AVALUEV.GITHUB.IO"
    d_scale = 2
    dw = _text_width(domain, d_scale)
    dx = (WIDTH - dw) // 2
    dy = sy + 50
    _draw_text(pixels, domain, dx, dy, ACCENT, scale=d_scale)

    return _encode_png(pixels)


def _encode_png(pixels: list[list[tuple[int, int, int]]]) -> bytes:
    """Encode an RGB pixel grid as a valid PNG."""
    raw_rows: list[bytes] = []
    for row in pixels:
        line = b"\x00"  # filter type: None
        for r, g, b in row:
            line += bytes((r, g, b))
        raw_rows.append(line)
    raw = b"".join(raw_rows)
    compressed = zlib.compress(raw, level=9)

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    header = b"\x89PNG\r\n\x1a\n"
    ihdr_data = struct.pack(">IIBBBBB", WIDTH, HEIGHT, 8, 2, 0, 0, 0)
    return (
        header
        + chunk(b"IHDR", ihdr_data)
        + chunk(b"IDAT", compressed)
        + chunk(b"IEND", b"")
    )


def main() -> int:
    data = build_png()
    if OUT.exists() and OUT.read_bytes() == data:
        print(f"[nochange] {OUT.name} ({len(data):,} bytes)")
        return 0
    OUT.write_bytes(data)
    print(f"[wrote] {OUT.name} ({len(data):,} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
