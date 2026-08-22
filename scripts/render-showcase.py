#!/usr/bin/env python3
"""Render the Last Call wallpaper contact sheet and Base24 palette card."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BACKGROUNDS = ROOT / "backgrounds"
OUT_SIZE = (2560, 1440)

COLORS = {
    "ink": "#030e10",
    "panel": "#0b1d20",
    "panel_2": "#1e4147",
    "line": "#42686f",
    "muted": "#719398",
    "fg": "#94b3b5",
    "light": "#c8e3e2",
    "white": "#e0f5f2",
    "red": "#ed634c",
    "orange": "#d07a3f",
    "yellow": "#b79a54",
    "green": "#58ad73",
    "cyan": "#00c6c2",
    "blue": "#668ca9",
    "magenta": "#9c8499",
    "brown": "#967d6d",
}

FONT_DIR = Path("/usr/share/fonts/TTF")
FONT_REGULAR = FONT_DIR / "IBMPlexSansCondensed-Regular.ttf"
FONT_MEDIUM = FONT_DIR / "IBMPlexSansCondensed-Medium.ttf"
FONT_BOLD = FONT_DIR / "IBMPlexSansCondensed-Bold.ttf"
FONT_MONO = FONT_DIR / "JetBrainsMono-Regular.ttf"


def font(path: Path, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(path), size)


def cover(image: Image.Image, size: tuple[int, int], focus=(0.5, 0.5)) -> Image.Image:
    """Crop an image to fully cover size, respecting a normalized focus point."""
    image = image.convert("RGB")
    scale = max(size[0] / image.width, size[1] / image.height)
    resized = image.resize((round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS)
    max_x = resized.width - size[0]
    max_y = resized.height - size[1]
    left = round(max(0, min(max_x, focus[0] * resized.width - size[0] / 2)))
    top = round(max(0, min(max_y, focus[1] * resized.height - size[1] / 2)))
    return resized.crop((left, top, left + size[0], top + size[1]))


def tracked(draw: ImageDraw.ImageDraw, xy, text, face, fill, spacing=5):
    x, y = xy
    for char in text:
        draw.text((x, y), char, font=face, fill=fill)
        x += draw.textlength(char, font=face) + spacing


def rounded_image(image: Image.Image, size, radius=18, focus=(0.5, 0.5)) -> Image.Image:
    image = cover(image, size, focus)
    mask = Image.new("L", size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, size[0], size[1]), radius=radius, fill=255)
    image.putalpha(mask)
    return image


def glass_panel(canvas: Image.Image, box, radius=28, alpha=224, outline="#42686f", width=2):
    layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    x1, y1, x2, y2 = box
    draw.rounded_rectangle((x1 + 10, y1 + 18, x2 + 10, y2 + 18), radius=radius, fill=(1, 5, 6, 150))
    draw.rounded_rectangle(box, radius=radius, fill=(11, 29, 32, alpha), outline=outline, width=width)
    canvas.alpha_composite(layer)


def base_canvas(background: Path, blur=8, dim=176) -> Image.Image:
    image = cover(Image.open(background), OUT_SIZE).filter(ImageFilter.GaussianBlur(blur)).convert("RGBA")
    tint = Image.new("RGBA", OUT_SIZE, (3, 14, 16, dim))
    image.alpha_composite(tint)
    return image


def image_card(canvas, path, box, label, number, focus=(0.5, 0.5), hero=False):
    x1, y1, x2, y2 = box
    size = (x2 - x1, y2 - y1)
    tile = rounded_image(Image.open(path), size, 22 if hero else 14, focus)
    canvas.alpha_composite(tile, (x1, y1))

    overlay = Image.new("RGBA", OUT_SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    band_h = 96 if hero else 54
    d.rounded_rectangle((x1, y2 - band_h, x2, y2), radius=22 if hero else 14, fill=(3, 14, 16, 204))
    d.rectangle((x1, y2 - band_h, x2, y2 - (22 if hero else 14)), fill=(3, 14, 16, 204))
    d.line((x1, y1, x1, y2), fill=COLORS["cyan"] if hero else COLORS["line"], width=4 if hero else 2)
    canvas.alpha_composite(overlay)

    draw = ImageDraw.Draw(canvas)
    if hero:
        draw.text((x1 + 30, y2 - 74), label, font=font(FONT_MEDIUM, 36), fill=COLORS["white"])
        tracked(draw, (x2 - 150, y2 - 70), number, font(FONT_MONO, 20), COLORS["cyan"], 3)
    else:
        draw.text((x1 + 18, y2 - 43), label, font=font(FONT_MEDIUM, 21), fill=COLORS["light"])
        draw.text((x2 - 46, y2 - 42), number, font=font(FONT_MONO, 17), fill=COLORS["muted"])


def render_wallpapers():
    paths = [
        ("01-closing-hour.jpg", "CLOSING HOUR", (0.51, 0.5)),
        ("02-rain-shelter.jpg", "RAIN SHELTER", (0.5, 0.5)),
        ("03-midnight-table.jpg", "MIDNIGHT TABLE", (0.5, 0.5)),
        ("04-faded-storefront.jpg", "FADED STOREFRONT", (0.5, 0.5)),
        ("05-red-corner.jpg", "RED CORNER", (0.5, 0.5)),
        ("06-wet-passage.jpg", "WET PASSAGE", (0.5, 0.5)),
        ("07-ghost-signage.jpg", "GHOST SIGNAGE", (0.5, 0.5)),
        ("08-cold-connection.jpg", "COLD CONNECTION", (0.5, 0.48)),
        ("09-scarlet-signal.jpg", "SCARLET SIGNAL", (0.5, 0.48)),
        ("10-aquarium-call.jpg", "AQUARIUM CALL", (0.5, 0.48)),
        ("11-ember-call.jpg", "EMBER CALL", (0.5, 0.48)),
    ]
    canvas = base_canvas(BACKGROUNDS / paths[0][0], blur=18, dim=202)
    glass_panel(canvas, (80, 70, 2480, 1370), radius=34, alpha=224)
    draw = ImageDraw.Draw(canvas)

    tracked(draw, (128, 112), "OMARCHY / VISUAL ARCHIVE", font(FONT_MONO, 20), COLORS["cyan"], 4)
    draw.text((126, 148), "LAST CALL", font=font(FONT_BOLD, 84), fill=COLORS["white"])
    draw.text((130, 242), "ELEVEN RAIN-LIT SCENES BY DANIIL ALEKSEEV", font=font(FONT_MEDIUM, 25), fill=COLORS["muted"])
    draw.line((1134, 118, 1134, 265), fill=COLORS["line"], width=2)
    draw.text((1180, 140), "CLOSING HOUR", font=font(FONT_MEDIUM, 31), fill=COLORS["yellow"])
    draw.text((1180, 188), "Rain glass / phone glow / one red signal", font=font(FONT_REGULAR, 25), fill=COLORS["fg"])
    tracked(draw, (2170, 137), "11 FRAMES", font(FONT_MONO, 18), COLORS["light"], 3)
    tracked(draw, (2170, 186), "3840 × 1670", font(FONT_MONO, 18), COLORS["muted"], 3)

    y_top, y_bottom = 320, 1280
    image_card(canvas, BACKGROUNDS / paths[0][0], (128, y_top, 1210, y_bottom), paths[0][1], "01", paths[0][2], hero=True)

    x0, gap, tile_w = 1244, 18, 564
    tile_h = 177
    for i, (filename, label, focus) in enumerate(paths[1:], start=1):
        col, row = i % 2, (i - 1) // 2
        # Start in the left column for odd display indices.
        col = (i - 1) % 2
        x1 = x0 + col * (tile_w + gap)
        y1 = y_top + row * (tile_h + gap)
        image_card(canvas, BACKGROUNDS / filename, (x1, y1, x1 + tile_w, y1 + tile_h), label, f"{i + 1:02d}", focus)

    draw.text((130, 1311), "A quiet street after rain — every frame tuned for a working desktop.", font=font(FONT_REGULAR, 22), fill=COLORS["muted"])
    draw.text((2195, 1311), "LAST CALL", font=font(FONT_MEDIUM, 22), fill=COLORS["fg"])
    canvas.convert("RGB").save(ROOT / "wallpaper-contact-sheet.jpg", quality=94, subsampling=0)


def swatch_card(canvas, box, slot, name, hex_value):
    x1, y1, x2, y2 = box
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle(box, radius=16, fill="#10282c", outline="#42686f", width=2)
    draw.rounded_rectangle((x1 + 8, y1 + 8, x2 - 8, y1 + 139), radius=11, fill=hex_value)
    draw.text((x1 + 14, y1 + 155), slot.upper(), font=font(FONT_MONO, 17), fill=COLORS["muted"])
    draw.text((x1 + 14, y1 + 184), name, font=font(FONT_MEDIUM, 20), fill=COLORS["light"])
    draw.text((x1 + 14, y1 + 216), hex_value.upper(), font=font(FONT_MONO, 15), fill=COLORS["fg"])


def render_palette():
    palette = [
        ("base00", "Closing Hour", "#0B1D20"), ("base01", "Rain Glass", "#1E4147"),
        ("base02", "Wet Pavement", "#42686F"), ("base03", "Payphone Haze", "#719398"),
        ("base04", "Street Mist", "#82A3A6"), ("base05", "Clouded Neon", "#94B3B5"),
        ("base06", "Fluorescent Fog", "#C8E3E2"), ("base07", "Booth Light", "#E0F5F2"),
        ("base08", "Tail Light", "#ED634C"), ("base09", "Rusted Awning", "#D07A3F"),
        ("base0A", "Old Sign", "#B79A54"), ("base0B", "Bottle Glass", "#58AD73"),
        ("base0C", "Phone Glow", "#00C6C2"), ("base0D", "Rain Reflection", "#668CA9"),
        ("base0E", "Mauve Shadow", "#9C8499"), ("base0F", "Wet Brick", "#967D6D"),
        ("base10", "Alley Depth", "#030E10"), ("base11", "Blackout", "#010506"),
        ("base12", "Brake Flare", "#F47A64"), ("base13", "Sign Ash", "#B5B49B"),
        ("base14", "Bottle Mist", "#8FA99A"), ("base15", "Signal Fog", "#A9C2C1"),
        ("base16", "Rain Slate", "#899FA4"), ("base17", "Mauve Ash", "#A4939E"),
    ]
    canvas = base_canvas(BACKGROUNDS / "11-ember-call.jpg", blur=20, dim=206)
    glass_panel(canvas, (80, 70, 2480, 1370), radius=34, alpha=228)
    draw = ImageDraw.Draw(canvas)

    # Left editorial rail.
    tracked(draw, (128, 112), "BASE24 / NIGHT SYSTEM", font(FONT_MONO, 20), COLORS["cyan"], 4)
    draw.text((126, 160), "COLOR AFTER", font=font(FONT_BOLD, 73), fill=COLORS["white"])
    draw.text((126, 236), "THE LAST CALL", font=font(FONT_BOLD, 73), fill=COLORS["white"])
    draw.line((130, 340, 760, 340), fill=COLORS["cyan"], width=4)
    draw.text((128, 380), "A rain-cold working palette", font=font(FONT_MEDIUM, 31), fill=COLORS["light"])
    copy = [
        "Smoked blue-green neutrals hold the room.",
        "Phone-booth cyan marks focus and connection.",
        "Old-sign brass carries waiting and unread state.",
        "One red signal is reserved for urgency.",
    ]
    for i, line in enumerate(copy):
        draw.text((128, 438 + i * 43), line, font=font(FONT_REGULAR, 24), fill=COLORS["fg"])

    roles = [
        ("FOCUS", COLORS["cyan"]), ("WAIT", COLORS["yellow"]),
        ("LIVE", COLORS["green"]), ("URGENT", COLORS["red"]),
    ]
    for i, (label, value) in enumerate(roles):
        y = 660 + i * 94
        draw.rounded_rectangle((128, y, 202, y + 64), radius=12, fill=value)
        draw.text((230, y + 3), label, font=font(FONT_MEDIUM, 23), fill=COLORS["light"])
        draw.text((230, y + 34), value.upper(), font=font(FONT_MONO, 16), fill=COLORS["muted"])

    draw.line((128, 1082, 760, 1082), fill=COLORS["line"], width=2)
    draw.text((128, 1122), "24 individually authored colors", font=font(FONT_MEDIUM, 25), fill=COLORS["light"])
    draw.text((128, 1162), "No duplicated extension slots.", font=font(FONT_REGULAR, 22), fill=COLORS["muted"])
    tracked(draw, (128, 1247), "LAST-CALL / DARK", font(FONT_MONO, 17), COLORS["yellow"], 3)
    tracked(draw, (128, 1290), "OLDJOBOBO", font(FONT_MONO, 17), COLORS["muted"], 3)

    # Palette matrix.
    start_x, start_y = 824, 114
    card_w, card_h, gap_x, gap_y = 191, 252, 14, 30
    for i, (slot, name, value) in enumerate(palette):
        col, row = i % 8, i // 8
        x1 = start_x + col * (card_w + gap_x)
        y1 = start_y + row * (card_h + gap_y)
        swatch_card(canvas, (x1, y1, x1 + card_w, y1 + card_h), slot, name, value)

    # Footer classification strip.
    strip_y = 999
    sections = [
        ("00—07", "RAIN-GLASS NEUTRALS", COLORS["fg"]),
        ("08—0F", "COLD LINE / WARM SIGNAL", COLORS["yellow"]),
        ("10—17", "BASE24 EXTENSION", COLORS["cyan"]),
    ]
    for i, (slot_range, label, value) in enumerate(sections):
        x = start_x + i * 545
        draw.line((x, strip_y, x + 500, strip_y), fill=value, width=3)
        draw.text((x, strip_y + 23), slot_range, font=font(FONT_MONO, 18), fill=value)
        draw.text((x + 92, strip_y + 20), label, font=font(FONT_MEDIUM, 20), fill=COLORS["fg"])

    draw.text((824, 1112), "NEUTRALS FIRST", font=font(FONT_BOLD, 41), fill=COLORS["white"])
    draw.text((824, 1166), "Readable surfaces before luminous accents.", font=font(FONT_REGULAR, 25), fill=COLORS["muted"])
    draw.text((824, 1242), "The palette mirrors wet pavement: color appears as reflected signal, never decoration.", font=font(FONT_REGULAR, 25), fill=COLORS["fg"])
    draw.text((824, 1302), "LAST CALL · BASE24", font=font(FONT_MEDIUM, 21), fill=COLORS["cyan"])

    canvas.convert("RGB").save(ROOT / "palette-card.jpg", quality=95, subsampling=0)


if __name__ == "__main__":
    render_wallpapers()
    render_palette()
    print("Rendered wallpaper-contact-sheet.jpg and palette-card.jpg")
