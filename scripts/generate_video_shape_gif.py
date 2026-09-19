"""Generate the animated video-shape teaching asset used by chapter 4."""

from math import pi, sin
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


WIDTH, HEIGHT = 960, 420
SCALE = 2
FRAME_COUNT = 12
OUTPUT = (
    Path(__file__).resolve().parents[1]
    / "templates"
    / "01_fashion_bigdata"
    / "lectures_korean"
    / "images"
    / "video-shape-time-axis.gif"
)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    filename = "seguisb.ttf" if bold else "segoeui.ttf"
    path = Path("C:/Windows/Fonts") / filename
    if path.exists():
        return ImageFont.truetype(str(path), size * SCALE)
    return ImageFont.load_default()


def xy(values: tuple[float, ...]) -> tuple[int, ...]:
    return tuple(round(value * SCALE) for value in values)


def make_frame(index: int) -> Image.Image:
    phase = 2 * pi * index / FRAME_COUNT
    canvas = Image.new("RGB", (WIDTH * SCALE, HEIGHT * SCALE), "#f8fafc")
    draw = ImageDraw.Draw(canvas)

    draw.rounded_rectangle(xy((24, 22, 936, 394)), radius=22 * SCALE, fill="#ffffff", outline="#dbe4f0", width=2 * SCALE)
    draw.rounded_rectangle(xy((48, 46, 912, 318)), radius=16 * SCALE, fill="#eaf4ff", outline="#93c5fd", width=2 * SCALE)

    # Runway and spatial guide lines inside one RGB frame.
    draw.polygon([xy((48, 318)), xy((912, 318)), xy((760, 242)), xy((200, 242))], fill="#e2e8f0")
    draw.line([xy((200, 242)), xy((760, 242))], fill="#cbd5e1", width=2 * SCALE)
    draw.line([xy((480, 242)), xy((480, 318))], fill="#cbd5e1", width=2 * SCALE)

    # A walking figure wearing a coat; the pose and hem move every frame.
    cx = 480 + 12 * sin(phase)
    head_y = 91 + 3 * abs(sin(phase))
    stride = 34 * sin(phase)
    arm = 24 * sin(phase + pi / 2)
    hem = 13 * sin(phase)

    draw.ellipse(xy((cx - 21, head_y - 21, cx + 21, head_y + 21)), fill="#d6a77a")
    draw.line([xy((cx, head_y + 20)), xy((cx, 137))], fill="#8b5e3c", width=9 * SCALE)
    draw.polygon(
        [
            xy((cx - 53, 132)),
            xy((cx + 53, 132)),
            xy((cx + 77 + hem, 260)),
            xy((cx + 24, 277)),
            xy((cx, 253)),
            xy((cx - 24, 277)),
            xy((cx - 77 + hem, 260)),
        ],
        fill="#334155",
        outline="#1e293b",
    )
    draw.line([xy((cx - 40, 148)), xy((cx - 86 - arm, 225))], fill="#334155", width=24 * SCALE)
    draw.line([xy((cx + 40, 148)), xy((cx + 86 - arm, 225))], fill="#334155", width=24 * SCALE)
    draw.line([xy((cx - 19, 263)), xy((cx - 26 - stride, 316))], fill="#1e293b", width=15 * SCALE)
    draw.line([xy((cx + 19, 263)), xy((cx + 26 + stride, 316))], fill="#1e293b", width=15 * SCALE)

    draw.text(xy((66, 63)), f"FRAME {index + 1:02d}", fill="#1e3a5f", font=font(18, bold=True))
    draw.ellipse(xy((829, 61, 845, 77)), fill="#ef4444")
    draw.ellipse(xy((851, 61, 867, 77)), fill="#22c55e")
    draw.ellipse(xy((873, 61, 889, 77)), fill="#3b82f6")
    draw.text(xy((839, 83)), "RGB", fill="#475569", font=font(13, bold=True))

    # Time axis: the active dot advances with the animation.
    axis_y = 357
    left, right = 76, 872
    draw.line([xy((left, axis_y)), xy((right, axis_y))], fill="#64748b", width=3 * SCALE)
    draw.polygon([xy((right, axis_y)), xy((right - 14, axis_y - 8)), xy((right - 14, axis_y + 8))], fill="#64748b")
    for dot in range(FRAME_COUNT):
        x_pos = left + dot * (right - left - 26) / (FRAME_COUNT - 1)
        radius = 8 if dot == index else 5
        color = "#2563eb" if dot == index else "#cbd5e1"
        draw.ellipse(xy((x_pos - radius, axis_y - radius, x_pos + radius, axis_y + radius)), fill=color)
    draw.text(xy((891, 345)), "T", fill="#1d4ed8", font=font(18, bold=True))

    return canvas.resize((WIDTH, HEIGHT), Image.Resampling.LANCZOS)


def main() -> None:
    frames = [make_frame(index) for index in range(FRAME_COUNT)]
    frames[0].save(
        OUTPUT,
        save_all=True,
        append_images=frames[1:],
        duration=140,
        loop=0,
        disposal=2,
        optimize=True,
    )
    print(OUTPUT)


if __name__ == "__main__":
    main()
