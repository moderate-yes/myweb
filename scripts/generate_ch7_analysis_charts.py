import os
import tempfile
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(tempfile.gettempdir()) / "fashion-course-matplotlib"))

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap


OUT_DIR = Path(__file__).resolve().parents[1] / "templates" / "01_fashion_bigdata" / "lectures_korean" / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Segoe UI", "Arial", "DejaVu Sans"],
        "axes.unicode_minus": False,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "axes.edgecolor": "#777773",
        "axes.labelcolor": "#333331",
        "xtick.color": "#555552",
        "ytick.color": "#555552",
        "text.color": "#292927",
    }
)

GRAY = "#777773"
LIGHT_GRAY = "#b7b7b2"
DARK = "#383836"
ACCENT = "#a85443"


def finish(fig, filename):
    fig.tight_layout()
    fig.savefig(OUT_DIR / filename, dpi=180, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# 1. Characterization and comparison
segments = ["New customers", "Repeat customers", "Loyal customers"]
average_order_value = [58, 83, 112]  # KRW 1,000
sample_size = [842, 516, 204]

fig, ax = plt.subplots(figsize=(8.4, 4.6))
bars = ax.bar(segments, average_order_value, color=[LIGHT_GRAY, GRAY, ACCENT], width=0.58)
ax.set_title("Average Order Value by Customer Group", loc="left", fontsize=15, fontweight="bold", pad=14)
ax.set_ylabel("Average order value (KRW 1,000)")
ax.set_ylim(0, 130)
ax.grid(axis="y", color="#e3e3df", linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
for bar, value, n in zip(bars, average_order_value, sample_size):
    ax.text(bar.get_x() + bar.get_width() / 2, value + 3, f"{value}K KRW\n(n={n:,})", ha="center", fontsize=10)
finish(fig, "analysis-characterization-comparison.png")


# 1-1. Monthly net sales and moving average
months = np.arange(1, 13)
monthly_sales = np.array([82, 86, 94, 91, 105, 112, 108, 117, 125, 142, 168, 196])
moving_average = np.convolve(monthly_sales, np.ones(3) / 3, mode="valid")

fig, ax = plt.subplots(figsize=(9.2, 4.8))
ax.plot(months, monthly_sales, color=GRAY, linewidth=2, marker="o", label="Monthly net sales")
ax.plot(months[2:], moving_average, color=ACCENT, linewidth=2.5, label="3-month moving average")
ax.set_title("Monthly Net Sales", loc="left", fontsize=15, fontweight="bold", pad=14)
ax.set_xlabel("Month")
ax.set_ylabel("Net sales (KRW million)")
ax.set_xticks(months)
ax.grid(axis="y", color="#e3e3df", linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc="upper left")
finish(fig, "analysis-monthly-sales-trend.png")


# 1-2. Sales by age group and gender
age_groups = ["20s", "30s", "40s", "50s+"]
women_sales = np.array([128, 176, 121, 74])
men_sales = np.array([72, 109, 96, 68])
x = np.arange(len(age_groups))
width = 0.34

fig, ax = plt.subplots(figsize=(8.8, 4.8))
ax.bar(x - width / 2, women_sales, width, color=ACCENT, label="Women")
ax.bar(x + width / 2, men_sales, width, color=GRAY, label="Men")
ax.set_title("Net Sales by Age Group and Gender", loc="left", fontsize=15, fontweight="bold", pad=14)
ax.set_xlabel("Age group")
ax.set_ylabel("Net sales (KRW million)")
ax.set_xticks(x, age_groups)
ax.grid(axis="y", color="#e3e3df", linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=9)
finish(fig, "analysis-demographic-sales.png")


# 1-3. Product price distribution with mean and median
rng_price = np.random.default_rng(29)
regular_prices = rng_price.lognormal(mean=np.log(7.2), sigma=0.42, size=280)
premium_prices = rng_price.normal(loc=27, scale=3.4, size=20)
prices = np.clip(np.concatenate([regular_prices, premium_prices]), 1.5, 40)
mean_price = prices.mean()
median_price = np.median(prices)

fig, ax = plt.subplots(figsize=(8.8, 4.8))
ax.hist(prices, bins=np.arange(0, 42, 2), color=LIGHT_GRAY, edgecolor="white")
ax.axvline(mean_price, color=ACCENT, linewidth=2.2, label=f"Mean {mean_price:.1f}")
ax.axvline(median_price, color=DARK, linewidth=2, linestyle="--", label=f"Median {median_price:.1f}")
ax.set_title("Price Distribution of Sold Products", loc="left", fontsize=15, fontweight="bold", pad=14)
ax.set_xlabel("Product price (KRW 10k)")
ax.set_ylabel("Number of products")
ax.grid(axis="y", color="#e3e3df", linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=9)
finish(fig, "analysis-price-distribution.png")


# 1-4. Pivot table heatmap: orders by weekday and hour
weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
hours = [9, 12, 15, 18, 21, 24]
order_matrix = np.array(
    [
        [31, 47, 42, 66, 84, 28],
        [29, 44, 40, 63, 79, 25],
        [33, 46, 43, 68, 82, 27],
        [35, 49, 45, 72, 88, 30],
        [38, 55, 51, 81, 102, 39],
        [46, 67, 62, 91, 113, 48],
        [51, 73, 68, 96, 119, 44],
    ]
)
heat_cmap = LinearSegmentedColormap.from_list("course_heat", ["#f1f1ee", "#aaa9a3", ACCENT])

fig, ax = plt.subplots(figsize=(8.8, 5.2))
image = ax.imshow(order_matrix, cmap=heat_cmap, aspect="auto")
ax.set_title("Orders by Weekday and Hour", loc="left", fontsize=15, fontweight="bold", pad=14)
ax.set_xlabel("Hour of day")
ax.set_ylabel("Weekday")
ax.set_xticks(np.arange(len(hours)), [f"{hour}:00" for hour in hours])
ax.set_yticks(np.arange(len(weekdays)), weekdays)
for row in range(order_matrix.shape[0]):
    for col in range(order_matrix.shape[1]):
        value = order_matrix[row, col]
        text_color = "white" if value >= 85 else DARK
        ax.text(col, row, str(value), ha="center", va="center", color=text_color, fontsize=9)
fig.colorbar(image, ax=ax, label="Orders", fraction=0.035, pad=0.03)
ax.spines[:].set_visible(False)
finish(fig, "analysis-order-heatmap.png")


# 2. Classification and regression
order_amount = np.array([3.2, 4.1, 4.8, 5.6, 6.0, 6.8, 7.2, 8.1, 8.8, 9.6, 10.4, 11.2])
size_gap = np.array([0.0, 0.5, 0.0, 1.0, 0.5, 1.5, 0.0, 2.0, 1.0, 2.5, 1.5, 3.0])
returned = np.array([0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 1], dtype=bool)

discount_rate = np.array([0, 5, 8, 10, 12, 15, 18, 20, 25, 30])
weekly_sales = np.array([31, 35, 38, 42, 44, 52, 57, 61, 70, 78])
slope, intercept = np.polyfit(discount_rate, weekly_sales, 1)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.8, 4.6))
ax1.scatter(order_amount[~returned], size_gap[~returned], s=58, c=GRAY, marker="o", label="Kept")
ax1.scatter(order_amount[returned], size_gap[returned], s=64, c=ACCENT, marker="^", label="Returned")
x_line = np.linspace(3, 11.5, 100)
ax1.plot(x_line, 0.30 * x_line - 1.1, color=DARK, linestyle="--", linewidth=1.4, label="Example decision boundary")
ax1.set_title("Classification: returned or kept", loc="left", fontsize=13, fontweight="bold")
ax1.set_xlabel("Order amount (KRW 10k)")
ax1.set_ylabel("Difference from usual size (steps)")
ax1.legend(frameon=False, fontsize=9)

ax2.scatter(discount_rate, weekly_sales, s=58, c=GRAY, marker="o", label="Observed")
ax2.plot(discount_rate, slope * discount_rate + intercept, color=ACCENT, linewidth=2, label="Regression line")
ax2.set_title("Regression: next week's sales", loc="left", fontsize=13, fontweight="bold")
ax2.set_xlabel("Discount rate (%)")
ax2.set_ylabel("Weekly sales (units)")
ax2.legend(frameon=False, fontsize=9)

for ax in (ax1, ax2):
    ax.grid(color="#e3e3df", linewidth=0.8)
    ax.set_axisbelow(True)
    ax.spines[["top", "right"]].set_visible(False)
finish(fig, "analysis-classification-regression.png")


# 3. Customer clustering with a small NumPy k-means implementation
rng = np.random.default_rng(17)
points = np.vstack(
    [
        rng.normal([2.2, 4.5], [0.7, 0.9], size=(14, 2)),
        rng.normal([5.8, 8.7], [0.9, 1.1], size=(16, 2)),
        rng.normal([10.5, 13.2], [1.0, 1.2], size=(13, 2)),
    ]
)
centroids = points[[0, 14, 30]].copy()
for _ in range(20):
    distances = ((points[:, None, :] - centroids[None, :, :]) ** 2).sum(axis=2)
    cluster = distances.argmin(axis=1)
    centroids = np.vstack([points[cluster == k].mean(axis=0) for k in range(3)])

fig, ax = plt.subplots(figsize=(8.4, 5.2))
colors = [LIGHT_GRAY, GRAY, ACCENT]
markers = ["o", "s", "^"]
for k in range(3):
    ax.scatter(points[cluster == k, 0], points[cluster == k, 1], s=52, c=colors[k], marker=markers[k], label=f"Cluster {k + 1}")
ax.scatter(centroids[:, 0], centroids[:, 1], s=170, c=DARK, marker="X", label="Centroids")
ax.set_title("Customer Clusters from Purchase Behavior", loc="left", fontsize=15, fontweight="bold", pad=14)
ax.set_xlabel("Purchases in the last 90 days")
ax.set_ylabel("Average order value (KRW 10k)")
ax.grid(color="#e3e3df", linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, ncol=4, fontsize=9, loc="upper left")
finish(fig, "analysis-customer-clusters.png")


# 4. Anomaly detection candidate
products = np.array([f"P{i:02d}" for i in range(1, 19)])
past_average = np.array([22, 31, 27, 45, 39, 52, 61, 48, 34, 57, 42, 66, 29, 54, 73, 36, 63, 76])
today_sales = np.array([24, 29, 31, 43, 42, 55, 58, 53, 32, 60, 39, 70, 33, 51, 77, 40, 65, 168])
residual = today_sales - past_average
z_score = (residual - residual.mean()) / residual.std(ddof=1)
anomaly = z_score > 2

fig, ax = plt.subplots(figsize=(8.4, 5.2))
ax.scatter(past_average[~anomaly], today_sales[~anomaly], s=58, c=GRAY, marker="o", label="Normal range")
ax.scatter(past_average[anomaly], today_sales[anomaly], s=90, c=ACCENT, marker="^", label="Investigation candidate")
limit = max(today_sales.max(), past_average.max()) + 10
ax.plot([0, limit], [0, limit], color=DARK, linestyle="--", linewidth=1.3, label="Same as past average")
idx = np.where(anomaly)[0][0]
ax.annotate(
    f"{products[idx]}  {today_sales[idx]} units",
    (past_average[idx], today_sales[idx]),
    xytext=(-98, -12),
    textcoords="offset points",
    arrowprops={"arrowstyle": "->", "color": ACCENT},
    fontsize=10,
)
ax.set_title("Today's Sales Far from the Past Average", loc="left", fontsize=15, fontweight="bold", pad=14)
ax.set_xlabel("Average daily sales in the last 28 days (units)")
ax.set_ylabel("Today's sales (units)")
ax.set_xlim(0, 100)
ax.set_ylim(0, 185)
ax.grid(color="#e3e3df", linewidth=0.8)
ax.set_axisbelow(True)
ax.spines[["top", "right"]].set_visible(False)
ax.legend(frameon=False, fontsize=9, loc="upper left")
finish(fig, "analysis-sales-outlier.png")

print(f"Generated 8 charts: {OUT_DIR}")
