import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from PIL import Image
from mplsoccer import VerticalPitch

# 1. Διαβάζουμε τα δύο αρχεία
goals = pd.read_csv("douvikas_goals.csv")
match = pd.read_csv("douvikas_match.csv").iloc[0]

# 2. Χρώματα: σκούρο γκρι/μαύρο με μπλε Κόμο για τα σημαντικά
BACKGROUND = "#121212"
STRIPE = "#171717"
CARD = "#1f1f1f"
HIGHLIGHT = "#3d6be0"
LIGHT = "#bdbdbd"
LINES = "#4d4d4d"
DIVIDER = "#2a2a2a"

# 3. Θέση κάθε σουτ στο γήπεδο (105 x 68 μ., εστία στο x = 105)
goals["depth"] = (goals["distance_m"] ** 2 - goals["side_m"] ** 2) ** 0.5
goals["x"] = 105 - goals["depth"]
goals["y"] = 34 - goals["side_m"]

# 4. Η εικόνα και το γήπεδο (με λωρίδες)
fig = plt.figure(figsize=(12, 10))
fig.patch.set_facecolor(BACKGROUND)

pitch = VerticalPitch(pitch_type="custom", pitch_length=105, pitch_width=68,
                      half=True, pad_bottom=-25, goal_type="box",
                      pitch_color=BACKGROUND, stripe=True, stripe_color=STRIPE,
                      line_color=LINES, linewidth=1.5)
ax = fig.add_axes([0.03, 0.36, 0.94, 0.50])
pitch.draw(ax=ax)

# 5. Αχνό σήμα της Κόμο στο φόντο του γηπέδου (μόνο αν υπάρχει το αρχείο)
if os.path.exists("como_logo.png"):
    logo_bg = ax.inset_axes([0.35, 0.10, 0.30, 0.80])
    logo_bg.imshow(Image.open("como_logo.png"), alpha=0.08)
    logo_bg.axis("off")
    logo_bg.set_zorder(1)

# 6. Γραμμές προς την εστία, λάμψη και κύκλοι (μέγεθος = xG)
pitch.lines(goals["x"], goals["y"], [105] * len(goals), [34] * len(goals),
            color=HIGHLIGHT, lw=2, alpha=0.5, zorder=2, ax=ax)
pitch.scatter(goals["x"], goals["y"], s=goals["xg"] * 3500,
              color=HIGHLIGHT, alpha=0.15, edgecolors="none", zorder=2.5, ax=ax)
pitch.scatter(goals["x"], goals["y"], s=goals["xg"] * 1300,
              color=HIGHLIGHT, edgecolors="white", linewidth=2, zorder=3, ax=ax)

# 7. Ετικέτα έξω από κάθε κύκλο, με γραμμούλα προς το σουτ
for g in goals.itertuples():
    label_y = 46 if g.y >= 30 else 12
    pitch.annotate(f"{g.minute}'  ·  xG {g.xg:.2f}", xy=(g.x, g.y), xytext=(g.x - 2, label_y),
                   ha="center", va="center", color="white", fontsize=12, fontweight="bold",
                   bbox=dict(boxstyle="round,pad=0.4", facecolor=CARD, edgecolor=HIGHLIGHT),
                   arrowprops=dict(arrowstyle="-", color=LIGHT, lw=1),
                   zorder=4, ax=ax)

# 8. Οδηγίες για μία κάρτα στο κάτω μέρος
def card(x, top, big, lines, highlight=False):
    a = fig.add_axes([x, 0.06, 0.22, 0.26])
    a.set_facecolor(HIGHLIGHT if highlight else CARD)
    a.set_xticks([])
    a.set_yticks([])
    for spine in a.spines.values():
        spine.set_visible(False)
    text_color = "white" if highlight else LIGHT
    a.text(0.5, 0.86, top, ha="center", va="center", fontsize=11,
           color=text_color, transform=a.transAxes)
    a.text(0.5, 0.62, big, ha="center", va="center", fontsize=30,
           fontweight="bold", color="white", transform=a.transAxes)
    for i, line in enumerate(lines):
        a.text(0.5, 0.36 - i * 0.13, line, ha="center", va="center",
               fontsize=11, color=text_color, transform=a.transAxes)

# 9. Κάρτα αποτελεσματικότητας (αριστερά, μπλε)
n_goals = len(goals)
n_shots = int(match["shots"])
total_xg = goals["xg"].sum()
card(0.03, "FINISHING", f"{n_goals}/{n_shots}",
     [f"Goals from {n_shots} shots", f"xG {total_xg:.2f}", f"+{n_goals - total_xg:.2f} above xG"],
     highlight=True)

# 10. Μία κάρτα για κάθε γκολ
foot = {"right": "Right foot", "left": "Left foot", "head": "Header"}
for i, g in enumerate(goals.itertuples()):
    card(0.27 + i * 0.24, f"GOAL {i + 1}", f"{g.minute}'",
         [f"Assist: {g.assist_by}", f"{foot[g.body_part]} · {g.distance_m:g} m", f"xG {g.xg:.2f}"])

# 11. Επικεφαλίδα: σήμα UCL, τίτλος αριστερά και γραμμή από κάτω
if os.path.exists("ucl_logo.png"):
    logo_ax = fig.add_axes([0.03, 0.895, 0.07, 0.085])
    logo_ax.imshow(Image.open("ucl_logo.png"))
    logo_ax.axis("off")

fig.text(0.11, 0.95, "Douvikas hat-trick | Shot map",
         ha="left", va="center", fontsize=20, fontweight="bold", color="white")
fig.text(0.11, 0.915, "Lens 1-9 Como · UEFA Champions League · Matchday 4 · Circle size = xG",
         ha="left", va="center", fontsize=12, color=LIGHT)
fig.add_artist(Line2D([0.03, 0.97], [0.885, 0.885], color=DIVIDER, lw=1,
                      transform=fig.transFigure))
fig.add_artist(Line2D([0.03, 0.15], [0.885, 0.885], color=HIGHLIGHT, lw=3,
                      transform=fig.transFigure))

# 12. Πηγή και υπογραφή
fig.text(0.03, 0.02, "Data: Opta, ESPN, FotMob · Shot locations approximate", fontsize=9, color=LIGHT)
fig.text(0.97, 0.02, "Analysis: Giorgos Drikos", ha="right", fontsize=9, color=LIGHT)
# 13. Αποθήκευση
plt.savefig("douvikas_shotmap.png", dpi=200, facecolor=BACKGROUND, bbox_inches="tight")
print("Το γήπεδο αποθηκεύτηκε!")