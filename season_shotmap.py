import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from PIL import Image
from mplsoccer import VerticalPitch

# 1. Διαβάζουμε όλα τα σουτ και τα ματς της σεζόν
shots = pd.read_csv("douvikas_all_shots.csv")
season = pd.read_csv("douvikas_season.csv")

# 2. Χρώματα (ίδια με τις άλλες εικόνες)
BACKGROUND = "#121212"
STRIPE = "#171717"
HIGHLIGHT = "#3d6be0"
LIGHT = "#bdbdbd"
LINES = "#4d4d4d"
DIVIDER = "#2a2a2a"

# 3. Αρχή και τέλος κάθε σουτ στο γήπεδο (105 x 68 μ., εστία στο x = 105)
shots["x"] = 105 - shots["depth_m"]
shots["y"] = 34 - shots["side_m"]
shots["end_x"] = 105 - shots["end_depth_m"]
shots["end_y"] = 34 - shots["end_side_m"]

# 4. Η εικόνα και το στυλ του γηπέδου
fig = plt.figure(figsize=(12, 5.5))
fig.patch.set_facecolor(BACKGROUND)
pitch = VerticalPitch(pitch_type="custom", pitch_length=105, pitch_width=68,
                      half=True, pad_bottom=-25, goal_type="box",
                      pitch_color=BACKGROUND, stripe=True, stripe_color=STRIPE,
                      line_color=LINES, linewidth=1.5)

# 5. Δύο γήπεδα: Serie A αριστερά, Champions League δεξιά
panels = [("Serie A", "SERIE A", 0.03), ("UCL", "CHAMPIONS LEAGUE", 0.51)]
for comp, title, left in panels:
    ax = fig.add_axes([left, 0.28, 0.46, 0.44])
    pitch.draw(ax=ax)

    s = shots[shots["competition"] == comp]
    misses = s[s["result"] != "goal"]
    goals = s[s["result"] == "goal"]

    # γραμμές: από το σημείο του σουτ μέχρι εκεί που κατέληξε η μπάλα
    pitch.lines(misses["x"], misses["y"], misses["end_x"], misses["end_y"],
                color=LIGHT, lw=1.2, alpha=0.35, zorder=1.5, ax=ax)
    pitch.lines(goals["x"], goals["y"], goals["end_x"], goals["end_y"],
                color=HIGHLIGHT, lw=2, alpha=0.8, zorder=1.6, ax=ax)

    # κουκκίδες: γκρι για τα άστοχα, μπλε για τα γκολ
    pitch.scatter(misses["x"], misses["y"], s=90, facecolors=BACKGROUND, edgecolors=LIGHT,
                  linewidth=1.5, zorder=2, ax=ax)
    pitch.scatter(goals["x"], goals["y"], s=170, color=HIGHLIGHT, edgecolors="white",
                  linewidth=1.8, zorder=3, ax=ax)

    # σύνολα από το αρχείο της σεζόν
    games = season[season["competition"] == comp]
    n_shots = int(games["shots"].sum())
    n_goals = int(games["goals"].sum())
    xg = games["xg"].sum()
    fig.text(left, 0.75, title, fontsize=12, fontweight="bold", color=HIGHLIGHT)
    fig.text(left + 0.46, 0.75, f"{len(games)} matches", ha="right", fontsize=11, color=LIGHT)
    fig.text(left + 0.23, 0.21,
             f"{n_shots} shots  ·  {n_goals} goals  ·  {xg:.2f} xG  ·  {n_goals / n_shots:.0%} conversion",
             ha="center", fontsize=12, color="white")

# 6. Υπόμνημα
legend_items = [
    Line2D([0], [0], marker="o", color=HIGHLIGHT, markerfacecolor=HIGHLIGHT,
           markeredgecolor="white", markersize=10, lw=2, label="Goal"),
    Line2D([0], [0], marker="o", color=LIGHT, alpha=0.6, markerfacecolor=BACKGROUND,
           markeredgecolor=LIGHT, markersize=9, lw=1.2, label="No goal"),
]
fig.legend(handles=legend_items, loc="lower center", bbox_to_anchor=(0.5, 0.06),
           ncol=2, frameon=False, labelcolor=LIGHT, fontsize=11)

# 7. Επικεφαλίδα: σήμα Κόμο, τίτλος αριστερά και γραμμή από κάτω
if os.path.exists("como_logo.png"):
    logo_ax = fig.add_axes([0.03, 0.835, 0.06, 0.14])
    logo_ax.imshow(Image.open("como_logo.png"))
    logo_ax.axis("off")

total_shots = int(season["shots"].sum())
total_goals = int(season["goals"].sum())
total_xg = season["xg"].sum()
fig.text(0.10, 0.93, "Douvikas | Season Shot Map 2026/27",
         ha="left", va="center", fontsize=20, fontweight="bold", color="white")
fig.text(0.10, 0.875, f"{total_shots} shots · {total_goals} goals · {total_xg:.2f} xG",
         ha="left", va="center", fontsize=12, color=LIGHT)
fig.add_artist(Line2D([0.03, 0.97], [0.82, 0.82], color=DIVIDER, lw=1, transform=fig.transFigure))
fig.add_artist(Line2D([0.03, 0.15], [0.82, 0.82], color=HIGHLIGHT, lw=3, transform=fig.transFigure))

# 8. Πηγή και υπογραφή
fig.text(0.03, 0.02, "Data: Opta, ESPN, FotMob · Shot locations approximate", fontsize=9, color=LIGHT)
fig.text(0.97, 0.02, "Analysis: Giorgos Drikos", ha="right", fontsize=9, color=LIGHT)

# 9. Αποθήκευση
plt.savefig("douvikas_season_shotmap.png", dpi=200, facecolor=BACKGROUND, bbox_inches="tight")
print("Το shot map της σεζόν αποθηκεύτηκε!")