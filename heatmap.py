import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.lines import Line2D
from PIL import Image
from mplsoccer import Pitch

# 1. Διαβάζουμε τις επαφές και τα σουτ του ματς με τη Λανς
touches = pd.read_csv("douvikas_lens_touches.csv")
shots = pd.read_csv("douvikas_all_shots.csv")
shots = shots[shots["opponent"] == "Lens"]

# 2. Χρώματα (ίδια με τις άλλες εικόνες)
BACKGROUND = "#121212"
STRIPE = "#171717"
HIGHLIGHT = "#3d6be0"
LIGHT = "#bdbdbd"
LINES = "#8a8a8a"
DIVIDER = "#2a2a2a"

# 3. Χρώματα του heatmap: από το μαύρο, στο μπλε της Κόμο, στο ανοιχτό γαλάζιο
heat_colors = LinearSegmentedColormap.from_list(
    "como_heat", [BACKGROUND, "#1f3a80", HIGHLIGHT, "#9fb8ff"])

# 4. Θέση των σουτ σε οριζόντιο γήπεδο (η Κόμο επιτίθεται προς τα δεξιά)
shots["x"] = 105 - shots["depth_m"]
shots["y"] = 34 - shots["side_m"]
shots["end_x"] = 105 - shots["end_depth_m"]
shots["end_y"] = 34 - shots["end_side_m"]

# 5. Ολόκληρο γήπεδο, με τις γραμμές πάνω από το heatmap
fig = plt.figure(figsize=(12, 9.5))
fig.patch.set_facecolor(BACKGROUND)
pitch = Pitch(pitch_type="custom", pitch_length=105, pitch_width=68, goal_type="box",
              pitch_color=BACKGROUND, stripe=True, stripe_color=STRIPE,
              line_color=LINES, linewidth=1.5, line_zorder=2)
ax = fig.add_axes([0.03, 0.12, 0.94, 0.72])
pitch.draw(ax=ax)

# 6. Το heatmap από τις 17 επαφές
pitch.kdeplot(touches["x"], touches["y"], ax=ax, fill=True, levels=100, thresh=0.05,
                            cut=4, bw_adjust=0.5, cmap=heat_colors, zorder=1, alpha=0.85)

# 7. Κάθε επαφή σαν μικρή κουκκίδα
pitch.scatter(touches["x"], touches["y"], s=25, color="white", alpha=0.5, zorder=3, ax=ax)

# 8. Τα τρία γκολ από πάνω, με γραμμή προς το σημείο που μπήκε η μπάλα
pitch.lines(shots["x"], shots["y"], shots["end_x"], shots["end_y"],
            color="white", lw=2, alpha=0.8, zorder=3, ax=ax)
pitch.scatter(shots["x"], shots["y"], s=220, color=HIGHLIGHT, edgecolors="white",
              linewidth=2, zorder=4, ax=ax)
label_spots = {7: (103, 63), 32: (97, 56), 57: (91, 49)}   # πού μπαίνει η ετικέτα κάθε γκολ
for g in shots.itertuples():
    lx, ly = label_spots[g.minute]
    pitch.annotate(f"{g.minute}'  ·  xG {g.xg:.2f}", xy=(g.x, g.y), xytext=(lx, ly),
                   ha="right", va="center", color="white", fontsize=12, fontweight="bold",
                   bbox=dict(boxstyle="round,pad=0.4", facecolor="#1f1f1f", edgecolor=HIGHLIGHT),
                   arrowprops=dict(arrowstyle="-", color="white", lw=1.2),
                   zorder=5, ax=ax)

# 9. Κατεύθυνση επίθεσης και υπόμνημα
fig.text(0.5, 0.095, "Attacking direction  →", ha="center", fontsize=11, color=LIGHT)
legend_items = [
    Line2D([0], [0], marker="o", ls="none", markerfacecolor="white", alpha=0.5,
           markeredgecolor="none", markersize=6, label="Touch"),
    Line2D([0], [0], marker="o", ls="none", markerfacecolor=HIGHLIGHT,
           markeredgecolor="white", markersize=11, label="Goal"),
]
fig.legend(handles=legend_items, loc="lower center", bbox_to_anchor=(0.5, 0.03),
           ncol=2, frameon=False, labelcolor=LIGHT, fontsize=11)

# 10. Επικεφαλίδα: σήμα UCL, τίτλος αριστερά και γραμμή από κάτω
if os.path.exists("ucl_logo.png"):
    logo_ax = fig.add_axes([0.03, 0.885, 0.07, 0.09])
    logo_ax.imshow(Image.open("ucl_logo.png"))
    logo_ax.axis("off")

fig.text(0.11, 0.945, "Douvikas | Heatmap vs Lens",
         ha="left", va="center", fontsize=20, fontweight="bold", color="white")
fig.text(0.11, 0.91, f"Lens 1-9 Como · UCL Matchday 4 · {len(touches)} touches · 61 min",
         ha="left", va="center", fontsize=12, color=LIGHT)
fig.add_artist(Line2D([0.03, 0.97], [0.875, 0.875], color=DIVIDER, lw=1, transform=fig.transFigure))
fig.add_artist(Line2D([0.03, 0.15], [0.875, 0.875], color=HIGHLIGHT, lw=3, transform=fig.transFigure))

# 11. Πηγή και υπογραφή
fig.text(0.03, 0.005, "Data: FotMob · Heatmap approximate",
         fontsize=9, color=LIGHT)
fig.text(0.97, 0.005, "Analysis: Giorgos Drikos", ha="right", fontsize=9, color=LIGHT)

# 12. Αποθήκευση
plt.savefig("douvikas_heatmap.png", dpi=200, facecolor=BACKGROUND, bbox_inches="tight")
print("Το heatmap αποθηκεύτηκε!")