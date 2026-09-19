"""Generate the synthetic fashion-mall practice data used by the APPLICATION chapters.

Output: templates/01_fashion_bigdata/data/fashion_mall/
  products.csv, customers.csv, orders.csv, events.csv, clicks.csv, reviews.csv,
  product_names_past.csv, product_names_recent.csv, market_keywords.csv,
  campaigns.csv, price_history.csv, competitor_promos.csv, images/P###.png

Every value is synthetic. Seeds are fixed so the lecture outputs are reproducible.
"""
from __future__ import annotations

import csv
import math
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "templates" / "01_fashion_bigdata" / "data" / "fashion_mall"
IMG = OUT / "images"
OUT.mkdir(parents=True, exist_ok=True)
IMG.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(20260917)
START = date(2026, 1, 1)
END = date(2026, 6, 30)
DAYS = (END - START).days + 1
SNAPSHOT = datetime(2026, 7, 1)


def write_csv(name: str, header: list[str], rows: list[list]) -> None:
    with open(OUT / name, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(header)
        writer.writerows(rows)
    print(f"{name:26s} {len(rows):7d} rows")


# ---------------------------------------------------------------- products
CATEGORIES = {
    "outer": ["코트", "자켓", "패딩", "가디건"],
    "top": ["티셔츠", "니트", "셔츠", "후드"],
    "bottom": ["팬츠", "데님", "스커트", "슬랙스"],
    "dress": ["원피스", "점프수트"],
    "bag": ["토트백", "크로스백"],
}
COLORS = {
    "black": ("블랙", (30, 30, 34)),
    "white": ("화이트", (238, 238, 232)),
    "navy": ("네이비", (32, 46, 92)),
    "beige": ("베이지", (214, 192, 160)),
    "gray": ("그레이", (140, 140, 146)),
    "pink": ("핑크", (232, 150, 176)),
    "green": ("그린", (72, 120, 84)),
    "brown": ("브라운", (120, 84, 56)),
}
MATERIALS = ["코튼", "울", "린넨", "폴리", "니트", "데님"]
FITS = ["오버핏", "슬림핏", "레귤러핏", "와이드", "크롭"]
PRICE_BASE = {"outer": 189000, "top": 49000, "bottom": 69000, "dress": 89000, "bag": 79000}

products = []
pid = 0
for category, subs in CATEGORIES.items():
    per_cat = {"outer": 18, "top": 22, "bottom": 20, "dress": 12, "bag": 8}[category]
    for _ in range(per_cat):
        pid += 1
        sub = subs[rng.integers(len(subs))]
        color = list(COLORS)[rng.integers(len(COLORS))]
        material = MATERIALS[rng.integers(len(MATERIALS))]
        fit = FITS[rng.integers(len(FITS))]
        price = int(round(PRICE_BASE[category] * rng.uniform(0.7, 1.5) / 1000) * 1000)
        cost = int(price * rng.uniform(0.35, 0.55) / 100) * 100
        launch = START - timedelta(days=int(rng.integers(0, 240)))
        name = f"{COLORS[color][0]} {fit} {material} {sub}"
        # baseline daily demand differs a lot between products (long tail)
        base_daily = float(np.clip(rng.lognormal(-0.9, 0.9), 0.05, 6.0))
        products.append({
            "product_id": f"P{pid:03d}", "product_name": name, "category": category,
            "subcategory": sub, "color": color, "material": material, "fit": fit,
            "list_price": price, "cost_price": cost, "launch_date": launch.isoformat(),
            "image_file": f"images/P{pid:03d}.png", "_base": base_daily,
        })
N_PRODUCTS = len(products)
for pid_, base in {"P017": 3.0, "P042": 2.0, "P008": 4.0, "P055": 2.5}.items():
    products[int(pid_[1:]) - 1]["_base"] = base
write_csv("products.csv",
          ["product_id", "product_name", "category", "subcategory", "color", "material", "fit",
           "list_price", "cost_price", "launch_date", "image_file"],
          [[p[k] for k in ["product_id", "product_name", "category", "subcategory", "color", "material",
                          "fit", "list_price", "cost_price", "launch_date", "image_file"]] for p in products])


# ------------------------------------------------------------ product images
def draw_silhouette(draw: ImageDraw.ImageDraw, sub: str, rgb: tuple, size: int = 96) -> None:
    s = size
    outline = tuple(max(0, c - 40) for c in rgb)
    if sub in ("코트", "자켓", "패딩", "가디건"):
        draw.polygon([(s*.30, s*.18), (s*.70, s*.18), (s*.86, s*.30), (s*.80, s*.40), (s*.72, s*.36),
                      (s*.74, s*.86), (s*.26, s*.86), (s*.28, s*.36), (s*.20, s*.40), (s*.14, s*.30)],
                     fill=rgb, outline=outline)
        draw.line([(s*.5, s*.24), (s*.5, s*.86)], fill=outline, width=2)
    elif sub in ("티셔츠", "니트", "셔츠", "후드"):
        draw.polygon([(s*.32, s*.22), (s*.68, s*.22), (s*.88, s*.34), (s*.80, s*.46), (s*.72, s*.42),
                      (s*.72, s*.74), (s*.28, s*.74), (s*.28, s*.42), (s*.20, s*.46), (s*.12, s*.34)],
                     fill=rgb, outline=outline)
        draw.ellipse([s*.42, s*.16, s*.58, s*.28], fill=(245, 245, 245), outline=outline)
    elif sub in ("팬츠", "데님", "슬랙스"):
        draw.polygon([(s*.30, s*.14), (s*.70, s*.14), (s*.74, s*.88), (s*.56, s*.88), (s*.50, s*.40),
                      (s*.44, s*.88), (s*.26, s*.88)], fill=rgb, outline=outline)
    elif sub == "스커트":
        draw.polygon([(s*.36, s*.18), (s*.64, s*.18), (s*.80, s*.80), (s*.20, s*.80)], fill=rgb, outline=outline)
    elif sub in ("원피스", "점프수트"):
        draw.polygon([(s*.36, s*.14), (s*.64, s*.14), (s*.70, s*.34), (s*.62, s*.44), (s*.82, s*.90),
                      (s*.18, s*.90), (s*.38, s*.44), (s*.30, s*.34)], fill=rgb, outline=outline)
    else:  # bags
        draw.rounded_rectangle([s*.22, s*.40, s*.78, s*.86], radius=8, fill=rgb, outline=outline)
        draw.arc([s*.34, s*.16, s*.66, s*.52], 180, 360, fill=outline, width=3)


for p in products:
    image = Image.new("RGB", (96, 96), (250, 250, 248))
    draw_silhouette(ImageDraw.Draw(image), p["subcategory"], COLORS[p["color"]][1])
    # light texture noise so that pixels are not perfectly identical between products
    arr = np.asarray(image).astype(np.int16)
    arr += rng.integers(-6, 7, arr.shape, dtype=np.int16)
    Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(IMG / f"{p['product_id']}.png")
print(f"images/                    {N_PRODUCTS:7d} files")


# ---------------------------------------------------------------- customers
SEGMENTS = ["loyal", "frequent_small", "rare_big", "occasional", "one_time"]
SEG_P = [0.08, 0.14, 0.10, 0.28, 0.40]
customers = []
for i in range(1, 601):
    seg = SEGMENTS[rng.choice(len(SEGMENTS), p=SEG_P)]
    signup = date(2025, 7, 1) + timedelta(days=int(rng.integers(0, 335)))
    age = rng.choice(["20s", "30s", "40s", "50s"], p=[0.34, 0.36, 0.20, 0.10])
    gender = rng.choice(["F", "M"], p=[0.68, 0.32])
    region = rng.choice(["Seoul", "Gyeonggi", "Busan", "Daegu", "Other"], p=[0.38, 0.27, 0.10, 0.07, 0.18])
    channel = rng.choice(["organic", "paid_search", "sns", "referral"], p=[0.35, 0.28, 0.27, 0.10])
    app = bool(rng.random() < (0.75 if seg in ("loyal", "frequent_small") else 0.45))
    consent = bool(rng.random() < 0.85)
    push = bool(app and rng.random() < 0.7)
    fav = rng.choice(list(CATEGORIES), p=[0.25, 0.30, 0.25, 0.14, 0.06])
    customers.append({
        "customer_id": f"C{i:04d}", "signup_date": signup.isoformat(), "gender": gender, "age_band": age,
        "region": region, "acquisition_channel": channel, "app_installed": app,
        "push_opt_in": push, "marketing_consent": consent, "_seg": seg, "_fav": fav,
    })
write_csv("customers.csv",
          ["customer_id", "signup_date", "gender", "age_band", "region", "acquisition_channel",
           "app_installed", "push_opt_in", "marketing_consent"],
          [[c[k] for k in ["customer_id", "signup_date", "gender", "age_band", "region", "acquisition_channel",
                          "app_installed", "push_opt_in", "marketing_consent"]] for c in customers])
cust_by_id = {c["customer_id"]: c for c in customers}
prod_by_id = {p["product_id"]: p for p in products}
prods_by_cat = {cat: [p for p in products if p["category"] == cat] for cat in CATEGORIES}


# ------------------------------------------------------------- price history
# markdown schedule: some products get discounted from a date on; a few have flash sales
price_rows = []
markdown_start = {}
for p in products:
    if rng.random() < 0.35:
        markdown_start[p["product_id"]] = START + timedelta(days=int(rng.integers(60, 150)))
for p in products:
    for d in range(DAYS):
        day = START + timedelta(days=d)
        rate = 0.0
        if p["product_id"] in markdown_start and day >= markdown_start[p["product_id"]]:
            rate = 0.2 if day < markdown_start[p["product_id"]] + timedelta(days=30) else 0.3
        price_rows.append([p["product_id"], day.isoformat(), p["list_price"], rate,
                           int(p["list_price"] * (1 - rate))])
write_csv("price_history.csv", ["product_id", "date", "list_price", "discount_rate", "sale_price"], price_rows)

competitor_rows = []
for comp in ["Brand A", "Brand B", "Brand C"]:
    for cat in CATEGORIES:
        for _ in range(2):
            s = START + timedelta(days=int(rng.integers(10, 160)))
            e = s + timedelta(days=int(rng.integers(3, 12)))
            competitor_rows.append([comp, cat, s.isoformat(), e.isoformat(), float(rng.choice([0.15, 0.2, 0.3, 0.4]))])
write_csv("competitor_promos.csv", ["competitor", "category", "start_date", "end_date", "discount_rate"], competitor_rows)


# --------------------------------------------------------------- daily demand
# product x day expected sales with weekday effect, injected anomalies
weekday_effect = np.array([0.95, 0.9, 0.9, 0.95, 1.05, 1.25, 1.2])  # Mon..Sun
expected = np.zeros((N_PRODUCTS, DAYS))
for i, p in enumerate(products):
    for d in range(DAYS):
        day = START + timedelta(days=d)
        season = 1.0
        if p["category"] == "outer":
            season = 1.6 if day.month <= 2 else (0.6 if day.month >= 5 else 1.0)
        if p["category"] in ("dress", "top"):
            season = 0.8 if day.month <= 2 else (1.3 if day.month >= 5 else 1.0)
        rate = 0.0
        if p["product_id"] in markdown_start and day >= markdown_start[p["product_id"]]:
            rate = 0.2 if day < markdown_start[p["product_id"]] + timedelta(days=30) else 0.3
        expected[i, d] = p["_base"] * season * weekday_effect[day.weekday()] * (1 + 1.2 * rate)
ANOMALIES = {
    # product index (0-based) : list of (day offset from START, multiplier, label)
    "P017": [(d, 4.0, "promo") for d in range((date(2026, 5, 20) - START).days, (date(2026, 5, 23) - START).days)],
    "P042": [((date(2026, 6, 10) - START).days, 6.0, "influencer")],
    "P008": [(d, 0.0, "stockout") for d in range((date(2026, 4, 5) - START).days, (date(2026, 4, 10) - START).days)],
    "P055": [(d, 1.0 + 0.08 * k, "trend") for k, d in enumerate(range((date(2026, 6, 1) - START).days, DAYS))],
}
anomaly_rows = []
for pid_, items in ANOMALIES.items():
    idx = int(pid_[1:]) - 1
    for d, mult, label in items:
        expected[idx, d] *= mult
        anomaly_rows.append([pid_, (START + timedelta(days=d)).isoformat(), label])
write_csv("injected_anomalies.csv", ["product_id", "date", "label"], anomaly_rows)
daily_units = rng.poisson(expected)


# ------------------------------------------------------------------ orders
# assign each unit sale to a customer according to segment behaviour
seg_weight = {"loyal": 9.0, "frequent_small": 5.0, "rare_big": 1.2, "occasional": 1.0, "one_time": 0.25}
cust_ids = [c["customer_id"] for c in customers]
cust_w = np.array([seg_weight[cust_by_id[c]["_seg"]] for c in cust_ids])
cust_w = cust_w / cust_w.sum()
orders = []
order_counter = 0
for d in range(DAYS):
    day = START + timedelta(days=d)
    # group units into orders: pick customers, each order has 1-3 lines
    units_today = [(i, int(daily_units[i, d])) for i in range(N_PRODUCTS) if daily_units[i, d] > 0]
    pool = []
    for i, n in units_today:
        pool += [i] * n
    rng.shuffle(pool)
    while pool:
        cid = cust_ids[rng.choice(len(cust_ids), p=cust_w)]
        c = cust_by_id[cid]
        n_lines = 1 if c["_seg"] in ("one_time", "occasional") else int(rng.choice([1, 2, 3], p=[0.6, 0.3, 0.1]))
        order_counter += 1
        oid = f"O{order_counter:06d}"
        hour = int(np.clip(rng.normal(15, 4), 0, 23))
        ts = datetime(day.year, day.month, day.day, hour, int(rng.integers(0, 60)))
        status = rng.choice(["completed", "cancelled", "returned"], p=[0.90, 0.04, 0.06])
        channel = "app" if (c["app_installed"] and rng.random() < 0.8) else "web"
        for line in range(1, n_lines + 1):
            if not pool:
                break
            # customers lean toward their favourite category
            pick = None
            if rng.random() < 0.5:
                fav_idx = [k for k, i in enumerate(pool) if products[i]["category"] == c["_fav"]]
                if fav_idx:
                    pick = fav_idx[rng.integers(len(fav_idx))]
            if pick is None:
                pick = rng.integers(len(pool))
            i = pool.pop(pick)
            p = products[i]
            rate = 0.0
            if p["product_id"] in markdown_start and day >= markdown_start[p["product_id"]]:
                rate = 0.2 if day < markdown_start[p["product_id"]] + timedelta(days=30) else 0.3
            if p["product_id"] == "P017" and date(2026, 5, 20) <= day <= date(2026, 5, 22):
                rate = 0.4
            qty = 1 if c["_seg"] != "rare_big" else int(rng.choice([1, 2, 3], p=[0.5, 0.3, 0.2]))
            orders.append([oid, line, ts.isoformat(timespec="minutes"), cid, p["product_id"], qty,
                           int(p["list_price"] * (1 - rate)), rate, status, channel])
write_csv("orders.csv", ["order_id", "line_no", "order_time", "customer_id", "product_id", "quantity",
                         "unit_price", "discount_rate", "status", "channel"], orders)
purchases_by_cust: dict[str, list] = {}
for row in orders:
    purchases_by_cust.setdefault(row[3], []).append(row)


# ------------------------------------------------------------------ events
# sessions: known customers (70%) and anonymous; funnel with filters, wishlist, checkout A/B test in May
SEARCH_QUERIES = [("와이드 팬츠", 24), ("린넨 셔츠", 18), ("하객룩 원피스", 15), ("오버핏 코트", 12), ("크롭 니트", 9),
                  ("77사이즈 원피스", 0), ("빅사이즈 팬츠", 0), ("발레코어", 0), ("여름 하객룩", 7), ("블랙 슬랙스", 11),
                  ("가디건", 20), ("토트백", 6), ("반팔 티셔츠", 0), ("데님 스커트", 8), ("바라클라바", 0)]
FILTERS = [("category", ["outer", "top", "bottom", "dress", "bag"]), ("color", list(COLORS)),
           ("size", ["S", "M", "L", "XL", "FREE"]), ("price", ["under_50k", "50k_100k", "100k_200k", "over_200k"]),
           ("fit", FITS), ("sort", ["popular", "newest", "price_low"])]
events = []
clicks = []
event_counter = 0
session_counter = 0
ab_rows = []


def add_event(ts, sid, cid, etype, pid_=None, detail="", device="mobile", variant=""):
    global event_counter
    event_counter += 1
    events.append([f"E{event_counter:06d}", ts.isoformat(timespec="seconds"), sid, cid or "", etype,
                   pid_ or "", detail, device, variant])


CLICK_ELEMENTS = {
    # element: (x_center, y_center, sx, sy, weight) on a 1280x2600 product page
    "main_image": (420, 520, 120, 160, 0.30), "thumbnails": (150, 760, 40, 120, 0.06),
    "size_chart": (900, 700, 70, 20, 0.14), "add_to_cart": (1000, 920, 110, 24, 0.18),
    "wishlist": (1140, 920, 25, 18, 0.05), "reviews_tab": (640, 1250, 160, 20, 0.15),
    "coupon_banner": (640, 200, 300, 30, 0.04), "detail_text": (640, 1900, 300, 300, 0.08),
}
for d in range(DAYS):
    day = START + timedelta(days=d)
    n_sessions = int(rng.poisson(45 * weekday_effect[day.weekday()] * (1.15 if day.month >= 5 else 1.0)))
    for _ in range(n_sessions):
        session_counter += 1
        sid = f"S{session_counter:06d}"
        known = rng.random() < 0.7
        cid = cust_ids[rng.choice(len(cust_ids), p=cust_w)] if known else None
        c = cust_by_id[cid] if cid else None
        if c and datetime.fromisoformat(c["signup_date"]).date() > day:
            cid, c = None, None
        device = "app" if (c and c["app_installed"] and rng.random() < 0.8) else rng.choice(["mobile", "desktop"], p=[0.7, 0.3])
        ts = datetime(day.year, day.month, day.day, int(np.clip(rng.normal(15, 4), 0, 23)), int(rng.integers(0, 60)))
        variant = ""
        if date(2026, 5, 1) <= day <= date(2026, 5, 31):
            variant = "A" if (int(sid[1:]) % 2 == 0) else "B"
        add_event(ts, sid, cid, "session_start", detail=rng.choice(["direct", "search_ad", "sns", "organic", "push"],
                                                                     p=[0.3, 0.25, 0.2, 0.15, 0.1]), device=device, variant=variant)
        t = ts
        # search
        if rng.random() < 0.4:
            q, n_res = SEARCH_QUERIES[rng.integers(len(SEARCH_QUERIES))]
            t += timedelta(seconds=int(rng.integers(5, 40)))
            add_event(t, sid, cid, "search", detail=f"{q}|{n_res}", device=device, variant=variant)
            if n_res == 0 and rng.random() < 0.55:
                continue  # zero results: many leave
        # browse category (favourite when known)
        cat = c["_fav"] if (c and rng.random() < 0.6) else rng.choice(list(CATEGORIES))
        t += timedelta(seconds=int(rng.integers(5, 30)))
        add_event(t, sid, cid, "view_category", detail=cat, device=device, variant=variant)
        used_filter = False
        if rng.random() < 0.45:
            k, vals = FILTERS[rng.integers(len(FILTERS))]
            t += timedelta(seconds=int(rng.integers(3, 20)))
            add_event(t, sid, cid, "apply_filter", detail=f"{k}={vals[rng.integers(len(vals))]}", device=device, variant=variant)
            used_filter = True
        n_views = int(rng.choice([1, 2, 3, 4, 6], p=[0.35, 0.3, 0.18, 0.1, 0.07]))
        viewed = []
        for _ in range(n_views):
            cat_prods = prods_by_cat[cat]
            weights = np.array([q["_base"] for q in cat_prods])
            p = cat_prods[rng.choice(len(cat_prods), p=weights / weights.sum())]
            t += timedelta(seconds=int(rng.integers(10, 90)))
            add_event(t, sid, cid, "view_item", p["product_id"], device=device, variant=variant)
            viewed.append(p)
            # click heat on the product page
            for _ in range(int(rng.integers(0, 3))):
                names = list(CLICK_ELEMENTS)
                w = np.array([CLICK_ELEMENTS[n][4] for n in names])
                el = names[rng.choice(len(names), p=w / w.sum())]
                cx, cy, sx, sy, _ = CLICK_ELEMENTS[el]
                clicks.append([sid, "product_detail", el, int(np.clip(rng.normal(cx, sx), 0, 1279)),
                               int(np.clip(rng.normal(cy, sy), 0, 2599)), device])
        wish = rng.random() < 0.18
        if wish and viewed:
            t += timedelta(seconds=int(rng.integers(3, 15)))
            add_event(t, sid, cid, "wishlist_add", viewed[-1]["product_id"], device=device, variant=variant)
        p_cart = 0.22 + (0.08 if used_filter else 0) + (0.06 if wish else 0) + (0.05 if c and c["_seg"] in ("loyal", "frequent_small") else 0)
        if viewed and rng.random() < p_cart:
            t += timedelta(seconds=int(rng.integers(5, 40)))
            add_event(t, sid, cid, "add_to_cart", viewed[-1]["product_id"], device=device, variant=variant)
            if rng.random() < 0.7:
                t += timedelta(seconds=int(rng.integers(10, 60)))
                add_event(t, sid, cid, "begin_checkout", viewed[-1]["product_id"], device=device, variant=variant)
                p_buy = 0.55 if variant != "B" else 0.63   # variant B: fewer form fields
                if rng.random() < p_buy:
                    t += timedelta(seconds=int(rng.integers(30, 180)))
                    add_event(t, sid, cid, "purchase", viewed[-1]["product_id"], detail=str(viewed[-1]["list_price"]),
                              device=device, variant=variant)
write_csv("events.csv", ["event_id", "event_time", "session_id", "customer_id", "event_type", "product_id",
                         "detail", "device", "variant"], events)
write_csv("clicks.csv", ["session_id", "page", "element", "x", "y", "device"], clicks)


# ----------------------------------------------------------------- reviews
ASPECTS = {
    "size": {"pos": ["사이즈가 딱 맞아요", "정사이즈라 고민 없이 골랐어요", "핏이 예쁘게 떨어져요"],
             "neg": ["사이즈가 생각보다 작아요", "한 치수 크게 사야 해요", "기장이 너무 길어요"]},
    "material": {"pos": ["소재가 부드럽고 촉감이 좋아요", "두께감이 적당해요", "원단이 고급스러워요"],
                 "neg": ["소재가 얇고 비쳐요", "보풀이 금방 생겨요", "원단이 뻣뻣해요"]},
    "delivery": {"pos": ["배송이 빨라요", "포장이 꼼꼼했어요"], "neg": ["배송이 일주일 넘게 걸렸어요", "박스가 찌그러져 왔어요"]},
    "color": {"pos": ["색상이 화면과 똑같아요", "색감이 고급스러워요"], "neg": ["색상이 사진보다 어두워요", "화면과 색이 달라요"]},
    "price": {"pos": ["가격 대비 만족해요", "세일가에 잘 샀어요"], "neg": ["가격에 비해 아쉬워요", "이 가격이면 다른 데가 나아요"]},
}
reviews = []
completed_lines = [r for r in orders if r[8] == "completed"]
rng.shuffle(completed_lines)
for k, row in enumerate(completed_lines[:1400]):
    c = cust_by_id[row[3]]
    p = prod_by_id[row[4]]
    height = int(np.clip(rng.normal(163 if c["gender"] == "F" else 175, 6), 148, 195))
    weight = int(np.clip(rng.normal(55 if c["gender"] == "F" else 72, 8), 40, 110))
    size = rng.choice(["S", "M", "L", "XL"], p=[0.25, 0.4, 0.25, 0.1]) if p["category"] != "bag" else "FREE"
    # fit depends on size vs body (larger body & small size => small)
    body = (height - 150) / 10 + (weight - 45) / 8
    size_idx = {"S": 0, "M": 1, "L": 2, "XL": 3, "FREE": 1.5}[size]
    fit_score = body - 2.2 * size_idx + rng.normal(0, 1.0) + (1.0 if p["fit"] == "슬림핏" else -0.8 if p["fit"] in ("오버핏", "와이드") else 0)
    fit = "small" if fit_score > 2.6 else ("large" if fit_score < -0.4 else "true_to_size")
    n_asp = int(rng.choice([1, 2, 3], p=[0.45, 0.4, 0.15]))
    chosen = rng.choice(list(ASPECTS), n_asp, replace=False)
    sentences, labels, pos_count = [], [], 0
    for a in chosen:
        if a == "size":
            polarity = "neg" if fit != "true_to_size" else ("pos" if rng.random() < 0.85 else "neg")
        else:
            polarity = "pos" if rng.random() < 0.7 else "neg"
        pool = ASPECTS[a][polarity]
        sentences.append(pool[rng.integers(len(pool))] + ".")
        labels.append(f"{a}:{polarity}")
        pos_count += polarity == "pos"
    rating = int(np.clip(round(2 + 3 * pos_count / n_asp + rng.normal(0, 0.5)), 1, 5))
    created = datetime.fromisoformat(row[2]) + timedelta(days=int(rng.integers(3, 20)))
    reviews.append([f"R{k+1:05d}", p["product_id"], c["customer_id"], created.date().isoformat(), rating,
                    size, height, weight, fit, " ".join(sentences), ";".join(labels)])
write_csv("reviews.csv", ["review_id", "product_id", "customer_id", "created_at", "rating", "size_purchased",
                          "height_cm", "weight_kg", "fit", "text", "aspect_labels"], reviews)


# ------------------------------------------------- product name rankings (keyword)
BRANDS = ["무드라인", "코튼하우스", "에브리데이", "노르딕", "블랑", "세컨드", "루트", "포레스트"]
PAST_VOCAB = {"item": ["니트", "코트", "팬츠", "셔츠", "원피스", "가디건", "티셔츠", "스커트", "자켓", "후드"],
              "style": ["슬림핏", "크롭", "베이직", "오버핏", "루즈핏", "미니", "롱"],
              "material": ["울", "코튼", "캐시미어", "폴리", "데님"],
              "color": ["블랙", "네이비", "그레이", "베이지", "아이보리"],
              "extra": ["기본", "데일리", "겨울", "울혼방", "터틀넥", "하프집업", "라운드"]}
RECENT_VOCAB = {"item": ["니트", "팬츠", "셔츠", "원피스", "가디건", "티셔츠", "스커트", "자켓", "블라우스", "슬랙스"],
                "style": ["와이드", "오버핏", "크롭", "베이직", "루즈핏", "발레코어", "롱", "세미와이드"],
                "material": ["린넨", "코튼", "울", "레이온", "데님", "시어서커"],
                "color": ["블랙", "화이트", "베이지", "카키", "핑크", "버터"],
                "extra": ["여름", "데일리", "하객룩", "썸머", "반팔", "쿨", "라운드", "바라클라바", "세트"]}


def make_names(vocab, n, weights=None):
    rows = []
    for r in range(1, n + 1):
        parts = []
        if rng.random() < 0.5:
            parts.append(f"[{BRANDS[rng.integers(len(BRANDS))]}]")
        for key in ["color", "style", "material", "extra", "item"]:
            if key in ("color", "material", "extra") and rng.random() < 0.45:
                continue
            words = vocab[key]
            w = None
            if weights and key in weights:
                w = np.array([weights[key].get(x, 1.0) for x in words], dtype=float)
                w = w / w.sum()
            parts.append(words[rng.choice(len(words), p=w)])
        if rng.random() < 0.3:
            parts.append(f"({rng.integers(2, 8)}COLOR)")
        price = int(rng.integers(19, 260)) * 1000
        rows.append([r, " ".join(parts), f"{price:,}원"])
    return rows


write_csv("product_names_past.csv", ["rank", "product_name", "price"],
          make_names(PAST_VOCAB, 200, {"style": {"슬림핏": 2.5, "크롭": 2.0}}))
write_csv("product_names_recent.csv", ["rank", "product_name", "price"],
          make_names(RECENT_VOCAB, 200, {"style": {"와이드": 3.0, "발레코어": 1.8}, "material": {"린넨": 2.5}}))


# ------------------------------------------------------------- market keywords
KEYWORDS = ["와이드 팬츠", "린넨 셔츠", "하객룩 원피스", "오버핏 코트", "크롭 니트", "발레코어", "바라클라바",
            "여름 원피스", "슬림 팬츠", "롱 패딩", "토트백", "데님 스커트", "반팔 니트", "시어서커 셔츠", "가디건"]
mk_rows = []
for kw_i, kw in enumerate(KEYWORDS):
    base = float(rng.integers(800, 40000))
    trend = rng.choice([-0.06, -0.02, 0.0, 0.03, 0.08, 0.15])
    summer = kw in ("린넨 셔츠", "하객룩 원피스", "여름 원피스", "반팔 니트", "시어서커 셔츠", "와이드 팬츠", "발레코어")
    for w in range(26):
        week = START + timedelta(days=7 * w)
        season = (1 + 0.9 * math.sin((w - 4) / 26 * math.pi)) if summer else (1.6 - 0.9 * w / 26)
        vol = base * season * (1 + trend) ** w * rng.uniform(0.9, 1.1)
        mk_rows.append([week.isoformat(), kw, int(vol), int(rng.integers(50, 3000)), round(float(rng.uniform(0.2, 0.95)), 2)])
write_csv("market_keywords.csv", ["week_start", "keyword", "search_volume", "product_count", "competition"], mk_rows)


# ----------------------------------------------------------------- campaigns
CHANNELS = ["push", "kakao", "email", "sms"]
open_rate = {"push": 0.30, "kakao": 0.42, "email": 0.20, "sms": 0.26}
app_session_days: dict[str, list] = {}
for ev in events:
    if ev[4] == "session_start" and ev[7] == "app" and ev[3]:
        app_session_days.setdefault(ev[3], []).append(datetime.fromisoformat(ev[1]).date())
camp_rows = []
cid_counter = 0
for month in range(2, 7):
    for seg_name in ["vip", "regular", "dormant", "new"]:
        cid_counter += 1
        camp_id = f"CMP{cid_counter:03d}"
        sent_day = date(2026, month, int(rng.integers(3, 25)))
        for c in customers:
            if not c["marketing_consent"] or datetime.fromisoformat(c["signup_date"]).date() > sent_day:
                continue
            seg_of = {"loyal": "vip", "frequent_small": "regular", "rare_big": "regular", "occasional": "dormant", "one_time": "new"}[c["_seg"]]
            if seg_of != seg_name or rng.random() < 0.4:
                continue
            allowed = CHANNELS if c["push_opt_in"] else ["kakao", "email", "sms"]
            channel = allowed[rng.integers(len(allowed))]           # 채널은 무작위 배정 (선택 실험의 근거)
            sessions_30d = sum(1 for d in app_session_days.get(c["customer_id"], []) if 0 < (sent_day - d).days <= 30)
            factor = 1.0
            if channel == "push":
                factor = 0.5 + 0.12 * min(sessions_30d, 8)          # 최근 앱 사용이 많을수록 푸시를 본다
            elif channel == "email":
                factor = {"20s": 0.55, "30s": 0.8, "40s": 1.4, "50s": 1.6}[c["age_band"]]
            elif channel == "kakao":
                factor = {"20s": 1.35, "30s": 1.25, "40s": 0.95, "50s": 0.7}[c["age_band"]]
            elif channel == "sms":
                factor = 1.5 if seg_name == "dormant" else (0.8 if sessions_30d >= 4 else 1.0)
            opened = rng.random() < min(open_rate[channel] * factor, 0.92)
            clicked = opened and rng.random() < 0.35
            bought = clicked and rng.random() < (0.35 if seg_name == "vip" else 0.18)
            revenue = int(rng.integers(30, 260)) * 1000 if bought else 0
            camp_rows.append([camp_id, sent_day.isoformat(), seg_name, c["customer_id"], channel, True, opened, clicked, bought, revenue])
write_csv("campaigns.csv", ["campaign_id", "sent_date", "segment", "customer_id", "channel", "delivered", "opened",
                            "clicked", "purchased_7d", "revenue"], camp_rows)

readme = f"""# 가상 패션몰 실습 데이터 (fashion_mall)

APPLICATION 파트의 실습 장에서 사용하는 합성 데이터다. 실제 고객·상품 정보가 아니며 `scripts/generate_fashion_mall_data.py`로 재생성할 수 있다(난수 시드 고정). 기간은 2026-01-01~2026-06-30, 기준일(snapshot)은 2026-07-01이다.

| 파일 | 행 | 기본키 | 연결키 | 쓰는 장 |
| --- | ---: | --- | --- | --- |
| `products.csv` | {N_PRODUCTS} | `product_id` | — | 20·22·23·24·26·30·36·39 |
| `customers.csv` | {len(customers)} | `customer_id` | — | 21·25·27·31·39 |
| `orders.csv` | {len(orders)} | `order_id`+`line_no` | `customer_id`, `product_id` | 20·21·24·27·30·39 |
| `events.csv` | {len(events)} | `event_id` | `session_id`, `customer_id`, `product_id` | 21·24·25·31·36·38·39 |
| `clicks.csv` | {len(clicks)} | — | `session_id` | 31 |
| `reviews.csv` | {len(reviews)} | `review_id` | `product_id`, `customer_id` | 29·37 |
| `product_names_past.csv` / `product_names_recent.csv` | 200 / 200 | `rank` | — | 23 |
| `market_keywords.csv` | {len(mk_rows)} | `week_start`+`keyword` | — | 26 |
| `campaigns.csv` | {len(camp_rows)} | `campaign_id`+`customer_id` | `customer_id` | 21·25 |
| `price_history.csv` | {len(price_rows)} | `product_id`+`date` | `product_id` | 30 |
| `competitor_promos.csv` | {len(competitor_rows)} | — | — | 30 |
| `injected_anomalies.csv` | {len(anomaly_rows)} | — | `product_id` | 20 (정답 라벨) |
| `images/P###.png` | {N_PRODUCTS} | `product_id` | — | 22·39 |

주의 사항

- `orders.csv`의 `status`가 `cancelled`·`returned`인 행은 순매출 계산에서 제외한다.
- `orders.csv`에는 고객의 `signup_date`보다 앞선 주문이 일부 있다. 비회원 구매가 나중에 계정에 연결된 경우로 간주하며, 코호트 분석(31장)에서는 제외한다.
- `events.csv`의 익명 세션은 `customer_id`가 비어 있다. `variant`는 2026년 5월 결제 화면 A/B 테스트 배정(A/B)이며 그 외 기간은 빈값이다.
- `detail` 컬럼은 이벤트 유형마다 뜻이 다르다. `search`는 `검색어|결과수`, `apply_filter`는 `필터=값`, `view_category`는 카테고리, `session_start`는 유입 경로다.
- `reviews.csv`의 `aspect_labels`는 텍스트 분류 실습의 정답 라벨이다. 실제 리뷰 데이터에는 이런 라벨이 없다.
- `injected_anomalies.csv`는 20장에서 탐지 결과를 채점하기 위한 정답이다. 실제 판매 데이터에는 없다.
- 이미지는 카테고리별 실루엣과 색상만 다른 단순 그림이다. 실제 상품 사진은 19장의 벤치마크 데이터셋을 사용한다.
"""
(OUT / "README.md").write_text(readme, encoding="utf-8")
print("README.md written")
