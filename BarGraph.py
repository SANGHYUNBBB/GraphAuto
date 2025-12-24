import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib import font_manager
from pathlib import Path

BASE_DIR = Path(__file__).parent
FONT_DIR = BASE_DIR / "fonts"
EXCEL_FILE = BASE_DIR / "Stock.xlsx"

FONT_PATH = FONT_DIR / "KOPUBDOTUM_PRO BOLD.OTF"
font = font_manager.FontProperties(fname=str(FONT_PATH))
plt.rcParams["axes.unicode_minus"] = False

df = pd.read_excel(EXCEL_FILE)
df = df[~df["구분"].isin(["기타", "계"])]
df = df.sort_values("비율", ascending=False).head(5).reset_index(drop=True)

df["비율_pct"] = df["비율"] * 100
max_value = df.loc[0, "비율_pct"]
df["bar_pct"] = df["비율_pct"] / max_value * 100

colors = ["#8AB6FF", "#7DD3FC", "#67E8F9", "#DCFCE7", "#FEF9C3"]
bg_color = "#F3F4F6"

bar_height = 0.72
corner_r = bar_height * 0.46   # ⭐ 핵심
MAX_BAR_WIDTH = 88
ROW_GAP = 0.82   # 1.0 → 기본 / 0.75~0.85 추천


LEFT_TEXT_X = 4.5
RIGHT_TEXT_X = 94.5

fig, ax = plt.subplots(figsize=(6.8, 4.2))
ax.set_xlim(0, 100)
ax.set_ylim(-0.5, len(df) - 0.5)
ax.axis("off")

for i, row in df.iterrows():
    y = (len(df) - 1 - i) * ROW_GAP

    # 회색 배경
    ax.add_patch(
        FancyBboxPatch(
            (0, y - bar_height / 2),
            100,
            bar_height,
            boxstyle=f"round,pad=0,rounding_size={corner_r}",
            linewidth=0,
            facecolor=bg_color
        )
    )

    bar_width = row["bar_pct"] / 100 * MAX_BAR_WIDTH

    # 컬러 바
    ax.add_patch(
        FancyBboxPatch(
            (0, y - bar_height / 2),
            bar_width,
            bar_height,
            boxstyle=f"round,pad=0,rounding_size={corner_r}",
            linewidth=0,
            facecolor=colors[i]
        )
    )

    ax.text(
        LEFT_TEXT_X, y,
        f"{i+1}위 {row['구분']}",
        va="center", ha="left",
        fontsize=11,
        fontproperties=font
    )

    ax.text(
        RIGHT_TEXT_X, y,
        f"{row['비율_pct']:.2f}%",
        va="center", ha="right",
        fontsize=11,
        fontproperties=font
    )

plt.subplots_adjust(left=0.02, right=0.98, top=0.98, bottom=0.02)
plt.show()
