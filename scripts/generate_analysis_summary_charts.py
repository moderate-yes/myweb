from pathlib import Path
from statistics import mean, median
from PIL import Image, ImageDraw, ImageFont
import math
import random


OUT_DIR = Path(__file__).resolve().parents[1] / "templates" / "01_fashion_bigdata" / "lectures_korean" / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WIDTH, HEIGHT = 1500, 820
BG = "#ffffff"
TEXT = "#292927"
GRID = "#e3e3df"
GRAY = "#777773"
LIGHT = "#b7b7b2"
DARK = "#383836"
ACCENT = "#a85443"
FONT_CANDIDATES = [
    (Path("C:/Windows/Fonts/segoeui.ttf"), Path("C:/Windows/Fonts/segoeuib.ttf")),
    (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/arialbd.ttf")),
    (Path("C:/Windows/Fonts/malgun.ttf"), Path("C:/Windows/Fonts/malgunbd.ttf")),
]


def font(size, bold=False):
    for regular, heavy in FONT_CANDIDATES:
        path = heavy if bold and heavy.exists() else regular
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def text_width(draw, text, text_font):
    bounds = draw.textbbox((0, 0), text, font=text_font)
    return bounds[2] - bounds[0]


def draw_vertical_label(image, text, center_y=420):
    label_font = font(24)
    bounds = ImageDraw.Draw(image).textbbox((0, 0), text, font=label_font)
    label = Image.new("RGBA", (bounds[2] + 20, bounds[3] + 20), (255, 255, 255, 0))
    ImageDraw.Draw(label).text((10, 5), text, fill=TEXT, font=label_font)
    label = label.rotate(90, expand=True)
    image.paste(label, (28, int(center_y - label.height / 2)), label)


def canvas(title, xlabel, ylabel):
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.text((105, 58), title, fill=TEXT, font=font(40, True))
    left, top, right, bottom = 150, 145, 1400, 690
    draw.line((left, top, left, bottom), fill=DARK, width=3)
    draw.line((left, bottom, right, bottom), fill=DARK, width=3)
    xlabel_font = font(24)
    draw.text(((left + right) / 2 - text_width(draw, xlabel, xlabel_font) / 2, 750), xlabel, fill=TEXT, font=xlabel_font)
    draw_vertical_label(image, ylabel)
    return image, draw, (left, top, right, bottom)


def save(image, name):
    image.save(OUT_DIR / name, "PNG", optimize=True)


def monthly_sales():
    values = [82, 86, 94, 91, 105, 112, 108, 117, 125, 142, 168, 196]
    moving = [mean(values[i - 2:i + 1]) for i in range(2, len(values))]
    image, draw, box = canvas("Monthly Net Sales", "Month", "Net sales (KRW million)")
    left, top, right, bottom = box
    ymin, ymax = 60, 210
    for value in [60, 90, 120, 150, 180, 210]:
        y = bottom - (value - ymin) / (ymax - ymin) * (bottom - top)
        draw.line((left, y, right, y), fill=GRID, width=2)
        draw.text((85, y - 14), str(value), fill=GRAY, font=font(20))
    points = []
    for idx, value in enumerate(values):
        x = left + idx * (right - left) / 11
        y = bottom - (value - ymin) / (ymax - ymin) * (bottom - top)
        points.append((x, y))
        draw.ellipse((x - 6, y - 6, x + 6, y + 6), fill=GRAY)
        draw.text((x - 8, bottom + 12), str(idx + 1), fill=GRAY, font=font(18))
    draw.line(points, fill=GRAY, width=5, joint="curve")
    ma_points = []
    for idx, value in enumerate(moving, start=2):
        x = left + idx * (right - left) / 11
        y = bottom - (value - ymin) / (ymax - ymin) * (bottom - top)
        ma_points.append((x, y))
    draw.line(ma_points, fill=ACCENT, width=6, joint="curve")
    draw.line((900, 105, 960, 105), fill=GRAY, width=5)
    draw.text((975, 90), "Monthly net sales", fill=TEXT, font=font(20))
    draw.line((1150, 105, 1210, 105), fill=ACCENT, width=6)
    draw.text((1225, 90), "3-month moving average", fill=TEXT, font=font(20))
    save(image, "analysis-monthly-sales-trend.png")


def demographic_sales():
    labels = ["20s", "30s", "40s", "50s+"]
    women = [128, 176, 121, 74]
    men = [72, 109, 96, 68]
    image, draw, box = canvas("Net Sales by Age Group and Gender", "Age group", "Net sales (KRW million)")
    left, top, right, bottom = box
    ymax = 200
    for value in [0, 50, 100, 150, 200]:
        y = bottom - value / ymax * (bottom - top)
        draw.line((left, y, right, y), fill=GRID, width=2)
        draw.text((85, y - 14), str(value), fill=GRAY, font=font(20))
    group = (right - left) / len(labels)
    for idx, label in enumerate(labels):
        center = left + (idx + 0.5) * group
        for offset, value, color in [(-44, women[idx], ACCENT), (16, men[idx], GRAY)]:
            x1, x2 = center + offset, center + offset + 52
            y = bottom - value / ymax * (bottom - top)
            draw.rectangle((x1, y, x2, bottom), fill=color)
        draw.text((center - text_width(draw, label, font(21)) / 2, bottom + 14), label, fill=TEXT, font=font(21))
    draw.rectangle((1090, 94, 1120, 116), fill=ACCENT)
    draw.text((1135, 88), "Women", fill=TEXT, font=font(20))
    draw.rectangle((1240, 94, 1270, 116), fill=GRAY)
    draw.text((1285, 88), "Men", fill=TEXT, font=font(20))
    save(image, "analysis-demographic-sales.png")


def price_distribution():
    random.seed(29)
    regular = [min(40, max(1.5, random.lognormvariate(math.log(7.2), 0.42))) for _ in range(280)]
    premium = [min(40, max(1.5, random.gauss(27, 3.4))) for _ in range(20)]
    prices = regular + premium
    avg, med = mean(prices), median(prices)
    bins = [0] * 20
    for value in prices:
        bins[min(19, int(value // 2))] += 1
    image, draw, box = canvas("Price Distribution of Sold Products", "Product price (KRW 10k)", "Number of products")
    left, top, right, bottom = box
    ymax = max(bins) * 1.1
    bar_width = (right - left) / len(bins)
    for idx, value in enumerate(bins):
        x1 = left + idx * bar_width + 2
        x2 = left + (idx + 1) * bar_width - 2
        y = bottom - value / ymax * (bottom - top)
        draw.rectangle((x1, y, x2, bottom), fill=LIGHT)
        if idx % 2 == 0:
            draw.text((x1, bottom + 12), str(idx * 2), fill=GRAY, font=font(17))
    for value, color, dash in [(avg, ACCENT, False), (med, DARK, True)]:
        x = left + value / 40 * (right - left)
        if dash:
            for y in range(top, bottom, 18):
                draw.line((x, y, x, min(y + 9, bottom)), fill=color, width=4)
        else:
            draw.line((x, top, x, bottom), fill=color, width=5)
    draw.line((1000, 105, 1055, 105), fill=ACCENT, width=5)
    draw.text((1070, 90), f"Mean {avg:.1f}", fill=TEXT, font=font(19))
    draw.line((1210, 105, 1265, 105), fill=DARK, width=4)
    draw.text((1280, 90), f"Median {med:.1f}", fill=TEXT, font=font(19))
    save(image, "analysis-price-distribution.png")


def blend(low, high, ratio):
    def rgb(value):
        value = value.lstrip("#")
        return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))
    a, b = rgb(low), rgb(high)
    values = tuple(round(a[i] + (b[i] - a[i]) * ratio) for i in range(3))
    return "#" + "".join(f"{value:02x}" for value in values)


def order_heatmap():
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    hours = ["9:00", "12:00", "15:00", "18:00", "21:00", "24:00"]
    matrix = [
        [31, 47, 42, 66, 84, 28], [29, 44, 40, 63, 79, 25],
        [33, 46, 43, 68, 82, 27], [35, 49, 45, 72, 88, 30],
        [38, 55, 51, 81, 102, 39], [46, 67, 62, 91, 113, 48],
        [51, 73, 68, 96, 119, 44],
    ]
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.text((105, 58), "Orders by Weekday and Hour", fill=TEXT, font=font(40, True))
    left, top, right, bottom = 220, 155, 1350, 690
    cell_w, cell_h = (right - left) / len(hours), (bottom - top) / len(weekdays)
    low, high = min(map(min, matrix)), max(map(max, matrix))
    for row, day in enumerate(weekdays):
        draw.text((145, top + row * cell_h + 20), day, fill=TEXT, font=font(22))
        for col, hour in enumerate(hours):
            value = matrix[row][col]
            ratio = (value - low) / (high - low)
            color = blend("#f1f1ee", ACCENT, ratio)
            x1, y1 = left + col * cell_w, top + row * cell_h
            x2, y2 = x1 + cell_w - 3, y1 + cell_h - 3
            draw.rectangle((x1, y1, x2, y2), fill=color)
            text_color = "#ffffff" if ratio > 0.58 else DARK
            tw = text_width(draw, str(value), font(21, True))
            draw.text((x1 + (cell_w - tw) / 2, y1 + 20), str(value), fill=text_color, font=font(21, True))
    for col, hour in enumerate(hours):
        tw = text_width(draw, hour, font(21))
        draw.text((left + col * cell_w + (cell_w - tw) / 2, bottom + 18), hour, fill=TEXT, font=font(21))
    xlabel = "Hour of day"
    draw.text(((left + right) / 2 - text_width(draw, xlabel, font(24)) / 2, 755), xlabel, fill=TEXT, font=font(24))
    draw_vertical_label(image, "Weekday")
    save(image, "analysis-order-heatmap.png")


def cooccurrence_comparison():
    labels = ["product", "good", "size", "long", "return"]
    counts = [
        [0, 182, 146, 121, 98],
        [182, 0, 72, 66, 41],
        [146, 72, 0, 84, 57],
        [121, 66, 84, 0, 73],
        [98, 41, 57, 73, 0],
    ]
    npmi = [
        [0.00, 0.03, 0.02, 0.01, 0.00],
        [0.03, 0.00, 0.08, 0.06, 0.01],
        [0.02, 0.08, 0.00, 0.47, 0.28],
        [0.01, 0.06, 0.47, 0.00, 0.39],
        [0.00, 0.01, 0.28, 0.39, 0.00],
    ]
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)
    draw.text((105, 50), "Co-occurrence Adjusted for Common Words", fill=TEXT, font=font(40, True))

    def panel(x0, title, matrix, formatter, high_value):
        draw.text((x0 + 155, 120), title, fill=TEXT, font=font(27, True))
        grid_top = 205
        cell = 92
        for idx, label in enumerate(labels):
            tw = text_width(draw, label, font(18))
            draw.text((x0 + 108 + idx * cell + (cell - 4 - tw) / 2, 165), label, fill=TEXT, font=font(18))
            draw.text((x0 + 100 - text_width(draw, label, font(18)) - 8, grid_top + idx * cell + 30), label, fill=TEXT, font=font(18))
        for row in range(len(labels)):
            for col in range(len(labels)):
                value = matrix[row][col]
                ratio = 0 if row == col else min(1, value / high_value)
                color = "#eeeeeb" if row == col else blend("#f4f4f1", ACCENT, ratio)
                x1 = x0 + 108 + col * cell
                y1 = grid_top + row * cell
                draw.rectangle((x1, y1, x1 + cell - 4, y1 + cell - 4), fill=color)
                text = "-" if row == col else formatter(value)
                text_color = "#ffffff" if ratio > 0.55 else DARK
                bbox = draw.textbbox((0, 0), text, font=font(18, True))
                tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text((x1 + (cell - tw) / 2, y1 + (cell - th) / 2 - 4), text, fill=text_color, font=font(18, True))

    panel(70, "Co-occurrence count", counts, lambda value: str(value), 190)
    panel(790, "NPMI", npmi, lambda value: f"{value:.2f}", 0.5)
    save(image, "analysis-cooccurrence-filtering.png")


def hiking_water_regression():
    image, draw, box = canvas("Distance Climbed vs Water Price", "Distance climbed (m)", "Water price (KRW)")
    left, top, right, bottom = box
    xmax, ymax = 35, 350

    for value in range(0, 351, 50):
        y = bottom - value / ymax * (bottom - top)
        draw.line((left, y, right, y), fill=GRID, width=2)
        draw.text((82, y - 14), str(value), fill=GRAY, font=font(19))

    for value in range(0, 36, 5):
        x = left + value / xmax * (right - left)
        draw.text((x - 10, bottom + 12), str(value), fill=GRAY, font=font(18))

    line_points = []
    for value in range(0, 36):
        x = left + value / xmax * (right - left)
        y = bottom - (10 * value) / ymax * (bottom - top)
        line_points.append((x, y))
    draw.line(line_points, fill=GRAY, width=5)

    for distance, price in [(10, 100), (20, 200)]:
        x = left + distance / xmax * (right - left)
        y = bottom - price / ymax * (bottom - top)
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill=DARK)

    predicted_x = left + 30 / xmax * (right - left)
    predicted_y = bottom - 300 / ymax * (bottom - top)
    for y in range(int(predicted_y), bottom, 16):
        draw.line((predicted_x, y, predicted_x, min(y + 8, bottom)), fill=ACCENT, width=3)
    draw.ellipse((predicted_x - 13, predicted_y - 13, predicted_x + 13, predicted_y + 13), fill=ACCENT)

    draw.line((900, 104, 955, 104), fill=GRAY, width=5)
    draw.text((970, 89), "Regression y = 10x", fill=TEXT, font=font(20))
    draw.ellipse((1160, 94, 1180, 114), fill=DARK)
    draw.text((1193, 89), "Observed", fill=TEXT, font=font(20))
    draw.ellipse((1305, 91, 1331, 117), fill=ACCENT)
    draw.text((1343, 89), "Predicted", fill=TEXT, font=font(20))
    save(image, "analysis-hiking-water-regression.png")


if __name__ == "__main__":
    monthly_sales()
    demographic_sales()
    price_distribution()
    order_heatmap()
    cooccurrence_comparison()
    hiking_water_regression()
    print(f"Generated 6 analysis summary charts: {OUT_DIR}")
