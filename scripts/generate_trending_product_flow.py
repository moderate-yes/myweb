from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math


OUT = (
    Path(__file__).resolve().parents[1]
    / "templates"
    / "01_fashion_bigdata"
    / "lectures_korean"
    / "images"
    / "app-ch20-trending-product-flow.png"
)

W, H = 1600, 1040
BG = "#FFFFFF"
INK = "#20252B"
MUTED = "#66717D"
LINE = "#CBD2D9"
PALE = "#F5F7F8"
BLUE = "#356E93"
BLUE_PALE = "#EAF3F8"
RED = "#B24A3B"
RED_PALE = "#FAECE9"
GREEN = "#2E6B50"
GREEN_PALE = "#EAF4EE"


def font(size, bold=False):
    candidates = [
        Path("C:/Windows/Fonts/malgunbd.ttf" if bold else "C:/Windows/Fonts/malgun.ttf"),
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
    ]
    for path in candidates:
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def centered(draw, box, text, text_font, fill=INK):
    x1, y1, x2, y2 = box
    bounds = draw.textbbox((0, 0), text, font=text_font)
    tw, th = bounds[2] - bounds[0], bounds[3] - bounds[1]
    draw.text(((x1 + x2 - tw) / 2, (y1 + y2 - th) / 2 - 2), text, font=text_font, fill=fill)


def arrow(draw, start, end, fill=LINE, width=4):
    draw.line((*start, *end), fill=fill, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    length = 13
    for delta in (2.55, -2.55):
        point = (
            end[0] + length * math.cos(angle + delta),
            end[1] + length * math.sin(angle + delta),
        )
        draw.line((*end, *point), fill=fill, width=width)


def pill(draw, x, y, text, fill=PALE, outline=LINE, text_fill=INK):
    f = font(20)
    bounds = draw.textbbox((0, 0), text, font=f)
    width = bounds[2] - bounds[0] + 34
    draw.rounded_rectangle((x, y, x + width, y + 42), radius=8, fill=fill, outline=outline, width=2)
    centered(draw, (x, y, x + width, y + 42), text, f, text_fill)
    return width


def stage(draw, number, title, y, color=BLUE, fill=BLUE_PALE):
    draw.ellipse((54, y + 34, 104, y + 84), fill=color)
    centered(draw, (54, y + 34, 104, y + 84), str(number), font(22, True), "#FFFFFF")
    draw.text((126, y + 36), title, font=font(27, True), fill=INK)
    draw.line((126, y + 78, 340, y + 78), fill=color, width=4)
    draw.rounded_rectangle((370, y, 1530, y + 120), radius=10, fill=fill, outline=color, width=2)


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

d.text((54, 42), "급상승 상품 분석 파이프라인", font=font(42, True), fill=INK)
d.text((54, 102), "주문 원천 데이터에서 이상 신호를 찾아 서비스 조치로 연결하는 다섯 단계", font=font(23), fill=MUTED)
d.line((54, 148, 1530, 148), fill=INK, width=3)

ys = [184, 344, 504, 664, 824]
for a, b in zip(ys, ys[1:]):
    arrow(d, (79, a + 86), (79, b + 28), fill=LINE, width=4)

# 1. Source checks
stage(d, 1, "데이터 확인", ys[0])
x, y = 410, ys[0] + 20
d.rectangle((x, y, x + 280, y + 78), fill="#FFFFFF", outline=LINE, width=2)
for xx in (x + 72, x + 170):
    d.line((xx, y, xx, y + 78), fill=LINE, width=2)
for yy in (y + 26, y + 52):
    d.line((x, yy, x + 280, yy), fill=LINE, width=2)
d.text((x + 9, y + 4), "시각", font=font(15, True), fill=MUTED)
d.text((x + 82, y + 4), "상품", font=font(15, True), fill=MUTED)
d.text((x + 181, y + 4), "주문 상태", font=font(15, True), fill=MUTED)
arrow(d, (718, y + 39), (780, y + 39), fill=BLUE)
pw = pill(d, 804, y + 5, "기간·컬럼 점검", "#FFFFFF", BLUE)
pill(d, 804, y + 54, "취소·반품 제외", "#FFFFFF", BLUE)
d.text((1135, y + 14), "OUTPUT", font=font(16, True), fill=BLUE)
d.text((1135, y + 43), "분석 가능한 주문 범위", font=font(22, True), fill=INK)

# 2. Aggregation
stage(d, 2, "데이터 구축", ys[1])
x, y = 410, ys[1] + 19
d.text((x, y), "주문 기록", font=font(19, True), fill=MUTED)
d.text((x, y + 34), "한 주문 = 한 행", font=font(22, True), fill=INK)
arrow(d, (620, y + 45), (706, y + 45), fill=BLUE)
d.text((735, y), "상품 × 기간", font=font(19, True), fill=MUTED)
d.text((735, y + 34), "판매량 행렬", font=font(22, True), fill=INK)
arrow(d, (938, y + 45), (1024, y + 45), fill=BLUE)
px = 1054
for label in ("1일", "12시간", "1시간"):
    px += pill(d, px, y + 24, label, "#FFFFFF", BLUE) + 12
d.text((1054, y + 2), "분석 속도에 맞는 집계 단위", font=font(17, True), fill=BLUE)

# 3. Model and decision
stage(d, 3, "신호 판정", ys[2], RED, RED_PALE)
x, y = 410, ys[2] + 17
d.text((x, y), "상품별 과거 분포", font=font(18, True), fill=MUTED)
curve = []
for i in range(180):
    xx = x + i
    z = (i - 86) / 31
    yy = y + 76 - 58 * math.exp(-0.5 * z * z)
    curve.append((xx, yy))
d.line(curve, fill=BLUE, width=4)
d.line((x, y + 76, x + 180, y + 76), fill=LINE, width=2)
d.line((x + 86, y + 14, x + 86, y + 78), fill=LINE, width=2)
d.text((x + 72, y + 80), "평균", font=font(14), fill=MUTED)
arrow(d, (620, y + 47), (700, y + 47), fill=RED)
d.text((730, y + 2), "표준화", font=font(17, True), fill=RED)
d.text((730, y + 37), "z = (오늘 - 평균) / 표준편차", font=font(24, True), fill=INK)
arrow(d, (1080, y + 47), (1158, y + 47), fill=RED)
pill(d, 1186, y + 2, "z > 3  급상승", "#FFFFFF", RED, RED)
pill(d, 1186, y + 53, "z < -3  급하락", "#FFFFFF", RED, RED)

# 4. Validation
stage(d, 4, "성능 평가", ys[3])
x, y = 410, ys[3] + 18
d.text((x, y), "탐지 결과", font=font(18, True), fill=MUTED)
d.text((x, y + 34), "모델이 낸 경보", font=font(22, True), fill=INK)
arrow(d, (620, y + 46), (700, y + 46), fill=BLUE)
d.text((730, y), "확인된 사건", font=font(18, True), fill=MUTED)
d.text((730, y + 34), "프로모션·노출·이슈", font=font(22, True), fill=INK)
arrow(d, (1000, y + 46), (1080, y + 46), fill=BLUE)
d.rectangle((1110, y, 1492, y + 82), fill="#FFFFFF", outline=BLUE, width=2)
d.text((1140, y + 15), "Precision", font=font(18, True), fill=MUTED)
d.text((1140, y + 45), "경보의 정확성", font=font(20, True), fill=INK)
d.line((1300, y + 10, 1300, y + 72), fill=LINE, width=2)
d.text((1330, y + 15), "Recall", font=font(18, True), fill=MUTED)
d.text((1330, y + 45), "사건의 포착률", font=font(20, True), fill=INK)

# 5. Operational handoff
stage(d, 5, "서비스 연동", ys[4], GREEN, GREEN_PALE)
x, y = 410, ys[4] + 17
d.rectangle((x, y, x + 240, y + 82), fill="#FFFFFF", outline=GREEN, width=2)
centered(d, (x, y, x + 240, y + 40), "경보 발송", font(20, True), GREEN)
centered(d, (x, y + 35, x + 240, y + 82), "이메일 · 메신저", font(19), INK)
arrow(d, (675, y + 41), (760, y + 41), fill=GREEN)
d.rectangle((790, y, 1030, y + 82), fill="#FFFFFF", outline=GREEN, width=2)
centered(d, (790, y, 1030, y + 40), "담당자 확인", font(20, True), GREEN)
centered(d, (790, y + 35, 1030, y + 82), "원인 · 재고 · 마진", font(19), INK)
arrow(d, (1055, y + 41), (1140, y + 41), fill=GREEN)
d.rectangle((1170, y, 1492, y + 82), fill="#FFFFFF", outline=GREEN, width=2)
centered(d, (1170, y, 1492, y + 40), "쇼핑몰 API", font(20, True), GREEN)
centered(d, (1170, y + 35, 1492, y + 82), "진열 위치 · 노출 조정", font(19), INK)

d.text((54, 992), "※ 급상승 신호는 자동 결론이 아니라 확인이 필요한 운영 후보이다.", font=font(18), fill=MUTED)

OUT.parent.mkdir(parents=True, exist_ok=True)
img.save(OUT, "PNG", optimize=True)
print(OUT)
