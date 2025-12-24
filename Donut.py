import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.lines import Line2D
from pathlib import Path

# =========================
# 경로 / 폰트
# =========================
BASE_DIR = Path(__file__).parent
FONT_DIR = BASE_DIR / "fonts"
EXCEL_FILE = BASE_DIR / "sector.xlsx"

FONT_PATH = FONT_DIR / "KOPUBDOTUM_PRO BOLD.OTF"
font = font_manager.FontProperties(fname=str(FONT_PATH))
plt.rcParams["axes.unicode_minus"] = False

# =========================
# 데이터 로드
# =========================
df = pd.read_excel(EXCEL_FILE)

labels = df["구분"].tolist()
values = (df["비율"] * 100).tolist()

# =========================
# 색상
# =========================
colors = ["#8AB6FF", "#7DD3FC", "#67E8F9", "#DCFCE7", "#FEF9C3", "#FACC15"]

# =========================
# 도넛 차트
# =========================
fig, ax = plt.subplots(figsize=(8, 5))

ax.pie(
    values,
    colors=colors,
    startangle=90,
    counterclock=False,
    wedgeprops=dict(width=0.28, edgecolor="white")
)

ax.set(aspect="equal")

# =========================
# Legend 구성 (원 아이콘)
# =========================
legend_handles = []

# 헤더용 더미 (정렬용)
legend_handles.append(
    Line2D(
        [0], [0],
        marker="",
        linestyle="",
        label="Label      %"
    )
)

# 실제 범주
for label, value, color in zip(labels, values, colors):
    legend_handles.append(
        Line2D(
            [0], [0],
            marker="o",
            linestyle="",
            markerfacecolor=color,
            markeredgecolor="none",
            markersize=8,
            label=f"{label:<6} {value:>5.1f}%"
        )
    )

legend = ax.legend(
    handles=legend_handles,
    loc="center left",
    bbox_to_anchor=(1.05, 0.55),
    frameon=False,
    handletextpad=0.8,
    labelspacing=1.1,
    prop=font
)

# =========================

# legend bbox 좌표 가져오기 (figure 좌표계)
fig.canvas.draw()  # 반드시 필요 (렌더링 후 bbox 계산)
bbox = legend.get_window_extent(fig.canvas.get_renderer())
bbox_fig = bbox.transformed(fig.transFigure.inverted())

# 선 위치 계산
x_start = bbox_fig.x0
x_end   = bbox_fig.x1
y_line  = bbox_fig.y1 + 0.01   # ⭐ 헤더 바로 아래 (미세조정 포인트)

# 회색 구분선 추가
fig.lines.append(
    Line2D(
        [x_start, x_end],
        [y_line, y_line],
        transform=fig.transFigure,
        color="#E5E7EB",   # 연한 회색
        linewidth=1
    )
)
# =========================
# Legend 스타일 조정
# =========================
texts = legend.get_texts()

# 헤더 (Label %)
texts[0].set_color("#9CA3AF")   # 회색
texts[0].set_fontsize(11)

# 나머지 항목
for t in texts[1:]:
    t.set_fontsize(11)

plt.tight_layout()
plt.show()
