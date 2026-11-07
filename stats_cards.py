import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# 1. Διαβάζουμε το αρχείο με τα σύνολα του αγώνα
row = pd.read_csv("douvikas_match.csv").iloc[0]

# 2. Χρώματα (ίδια με το γήπεδο)
BACKGROUND = "#121212"
HIGHLIGHT = "#3d6be0"   # μπλε Κόμο
LIGHT = "#bdbdbd"       # ανοιχτό γκρι
DIVIDER = "#2a2a2a"     # λεπτές γραμμές
FAINT = "#262626"       # πολύ αχνές γραμμές

# 3. Νούμερα που θα χρειαστούμε
goals = int(row["goals"])
assists = int(row["assists"])
shots = int(row["shots"])
on_target = int(row["shots_on_target"])

# 4. Τα στατιστικά δεξιά, σε ομάδες: (τίτλος, τιμή, ποσοστό για μπάρα ή None)
sections = [
    ("ATTACKING", [
        ("Shots on target", f"{on_target}/{shots}", on_target / shots),
        ("Expected goals (xG)", f"{row['xg']:.2f}", None),
        ("Expected assists (xA)", f"{row['xa']:.2f}", None),
    ]),
    ("ON THE BALL", [
        ("Touches", f"{int(row['touches'])}", None),
        ("Passes completed", f"{int(row['passes_completed'])}/{int(row['passes_attempted'])}",
         row["passes_completed"] / row["passes_attempted"]),
        ("Dribbles won", f"{int(row['dribbles_won'])}/{int(row['dribbles_attempted'])}",
         row["dribbles_won"] / row["dribbles_attempted"]),
    ]),
    ("PHYSICAL", [
        ("Distance covered", f"{row['distance_km']} km", None),
        ("Top speed", f"{row['top_speed_kmh']} km/h", None),
    ]),
]

# 5. Η εικόνα
fig = plt.figure(figsize=(12, 7))
fig.patch.set_facecolor(BACKGROUND)

# 6. Αχνό σήμα πίσω από τα μεγάλα νούμερα (μόνο αν υπάρχει το αρχείο)
if os.path.exists("como_logo.png"):
    logo_bg = fig.add_axes([0.02, 0.08, 0.36, 0.72])
    logo_bg.imshow(Image.open("como_logo.png"), alpha=0.06)
    logo_bg.axis("off")
    logo_bg.set_zorder(0)

# 7. Ένας «καμβάς» σε όλη την εικόνα, με θέσεις από 0 έως 1
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")
ax.set_zorder(1)

# 8. Επικεφαλίδα: τίτλος αριστερά και γραμμή από κάτω
ax.text(0.12, 0.93, "Douvikas hat-trick | Lens 1-9 Como",
        ha="left", va="center", fontsize=20, fontweight="bold", color="white")
ax.text(0.12, 0.885, "UEFA Champions League · Matchday 4 · 4 Nov 2026",
        ha="left", va="center", fontsize=12, color=LIGHT)
ax.plot([0.04, 0.96], [0.84, 0.84], color=DIVIDER, lw=1)
ax.plot([0.04, 0.16], [0.84, 0.84], color=HIGHLIGHT, lw=3)

# 9. Αριστερά: τα μεγάλα νούμερα
ax.text(0.06, 0.76, "GOALS", fontsize=13, fontweight="bold", color=LIGHT, va="center")
ax.text(0.06, 0.73, f"{goals}", fontsize=120, fontweight="bold", color=HIGHLIGHT, va="top")
ax.text(0.17, 0.66, f"from {shots} shots", fontsize=12, color=LIGHT, va="center")
ax.text(0.17, 0.59, f"+{goals - row['xg']:.2f} vs xG", fontsize=12,
        fontweight="bold", color="white", va="center")

ax.text(0.06, 0.44, "ASSISTS", fontsize=13, fontweight="bold", color=LIGHT, va="center")
ax.text(0.06, 0.41, f"{assists}", fontsize=120, fontweight="bold", color="white", va="top")
ax.text(0.17, 0.34, "for Nico Paz", fontsize=12, color=LIGHT, va="center")
ax.text(0.17, 0.27, f"+{assists - row['xa']:.2f} vs xA", fontsize=12,
        fontweight="bold", color="white", va="center")

# 10. Κάθετη γραμμή που χωρίζει
ax.plot([0.40, 0.40], [0.10, 0.78], color=DIVIDER, lw=1)

# 11. Δεξιά: τα στατιστικά σε ομάδες
y = 0.76
for title, rows in sections:
    ax.text(0.45, y, title, fontsize=11, fontweight="bold", color=HIGHLIGHT, va="center")
    y -= 0.055
    for label, value, ratio in rows:
        ax.text(0.45, y, label, fontsize=12, color=LIGHT, va="center")
        ax.text(0.96, y, value, fontsize=15, fontweight="bold", color="white",
                ha="right", va="center")
        if ratio is not None:
            ax.plot([0.66, 0.84], [y, y], color=DIVIDER, lw=6, solid_capstyle="round")
            ax.plot([0.66, 0.66 + 0.18 * ratio], [y, y], color=HIGHLIGHT, lw=6,
                    solid_capstyle="round")
        ax.plot([0.45, 0.96], [y - 0.03, y - 0.03], color=FAINT, lw=0.8)
        y -= 0.06
    y -= 0.01

# 12. Σήμα του Champions League πάνω αριστερά (μόνο αν υπάρχει το αρχείο)
if os.path.exists("ucl_logo.png"):
    logo_ax = fig.add_axes([0.04, 0.86, 0.07, 0.11])
    logo_ax.imshow(Image.open("ucl_logo.png"))
    logo_ax.axis("off")
    logo_ax.set_zorder(2)

# 13. Πηγή και υπογραφή
ax.text(0.04, 0.03, "Data: Opta, ESPN, FotMob", fontsize=9, color=LIGHT)
ax.text(0.96, 0.03, "Analysis: Giorgos Drikos", ha="right", fontsize=9, color=LIGHT)

# 14. Αποθήκευση
plt.savefig("douvikas_stats.png", dpi=200, facecolor=BACKGROUND, bbox_inches="tight")
print("Η εικόνα αποθηκεύτηκε!")