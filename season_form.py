import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from PIL import Image

# 1. Διαβάζουμε τη σεζόν
season = pd.read_csv("douvikas_season.csv")
n = len(season)
x = list(range(n))
lens = n - 1   # το ματς με τη Λανς είναι το τελευταίο

# 2. Χρώματα (ίδια με τις άλλες εικόνες)
BACKGROUND = "#121212"
HIGHLIGHT = "#3d6be0"
LIGHT = "#bdbdbd"
DIVIDER = "#2a2a2a"
GREY_BAR = "#3a3a3a"

# 3. Σύνολα και αθροιστικά
total_goals = int(season["goals"].sum())
total_xg = season["xg"].sum()
season["cum_goals"] = season["goals"].cumsum()
season["cum_xg"] = season["xg"].cumsum()

# 4. Κοινό στυλ για τα δύο γραφήματα
def style(a):
    a.set_facecolor(BACKGROUND)
    for side in ["top", "right", "left"]:
        a.spines[side].set_visible(False)
    a.spines["bottom"].set_color(DIVIDER)
    a.tick_params(colors=LIGHT, length=0)
    a.grid(axis="y", color=DIVIDER, lw=0.8)
    a.set_axisbelow(True)
    a.set_xlim(-0.6, n - 0.4)
    a.axvspan(lens - 0.5, lens + 0.5, color=HIGHLIGHT, alpha=0.08)  # τονίζουμε τη Λανς

fig = plt.figure(figsize=(12, 9))
fig.patch.set_facecolor(BACKGROUND)
top = fig.add_axes([0.07, 0.57, 0.90, 0.27])
bottom = fig.add_axes([0.07, 0.17, 0.90, 0.26])
style(top)
style(bottom)

# 5. Πάνω: xG και γκολ ανά ματς
top.bar([i - 0.2 for i in x], season["xg"], width=0.38, color=GREY_BAR, label="xG")
top.bar([i + 0.2 for i in x], season["goals"], width=0.38, color=HIGHLIGHT, label="Goals")
top.set_ylim(0, 3.8)
top.set_xticks(x)
top.set_xticklabels([f"{o} ({v})" for o, v in zip(season["opponent"], season["venue"])], rotation=40, ha="right", fontsize=10)
for lbl, comp in zip(top.get_xticklabels(), season["competition"]): lbl.set_color(HIGHLIGHT if comp == "UCL" else LIGHT)
top.text(0, 1.06, "PER MATCH", transform=top.transAxes,
         fontsize=11, fontweight="bold", color=HIGHLIGHT)
top.legend(loc="upper left", frameon=False, labelcolor=LIGHT, fontsize=10)

# 6. Κάτω: αθροιστικά γκολ και xG, με χρωματισμένη την απόσταση
bottom.plot(x, season["cum_xg"], color="white", lw=2.8, ls=(0, (4, 1.5)), marker="o", markersize=6)
bottom.plot(x, season["cum_goals"], color=HIGHLIGHT, lw=3, marker="o", markersize=6)
bottom.fill_between(x, season["cum_xg"], season["cum_goals"],
                    where=season["cum_goals"] >= season["cum_xg"],
                    color=HIGHLIGHT, alpha=0.15, interpolate=True)
bottom.text(lens, season["cum_goals"].iloc[-1] + 0.8, f"{total_goals} goals",
            ha="right", fontsize=11, fontweight="bold", color=HIGHLIGHT)
bottom.text(lens, season["cum_xg"].iloc[-1] - 2.2, f"{total_xg:.2f} xG",
            ha="right", fontsize=11, fontweight="bold", color=LIGHT)
bottom.set_ylim(0, total_goals + 2)
bottom.text(0, 1.06, "CUMULATIVE", transform=bottom.transAxes,
            fontsize=11, fontweight="bold", color=HIGHLIGHT)

# 7. Αντίπαλοι κάτω από τα γραφήματα (μπλε = Champions League)
bottom.set_xticks(x)
bottom.set_xticklabels([f"{o} ({v})" for o, v in zip(season["opponent"], season["venue"])],
                       rotation=40, ha="right", fontsize=10)
for label, comp in zip(bottom.get_xticklabels(), season["competition"]):
    label.set_color(HIGHLIGHT if comp == "UCL" else LIGHT)

# 8. Επικεφαλίδα: σήμα Κόμο, τίτλος αριστερά και γραμμή από κάτω
if os.path.exists("como_logo.png"):
    logo_ax = fig.add_axes([0.03, 0.885, 0.07, 0.09])
    logo_ax.imshow(Image.open("como_logo.png"))
    logo_ax.axis("off")

fig.text(0.11, 0.95, "Douvikas | Season form 2026/27",
         ha="left", va="center", fontsize=20, fontweight="bold", color="white")
fig.text(0.11, 0.915,
         f"{n} matches · {total_goals} goals · {total_xg:.2f} xG · "
         f"+{total_goals - total_xg:.2f} vs xG · All competitions",
         ha="left", va="center", fontsize=12, color=LIGHT)
fig.add_artist(Line2D([0.03, 0.97], [0.885, 0.885], color=DIVIDER, lw=1,
                      transform=fig.transFigure))
fig.add_artist(Line2D([0.03, 0.15], [0.885, 0.885], color=HIGHLIGHT, lw=3,
                      transform=fig.transFigure))

# 9. Πηγή και υπογραφή
fig.text(0.03, 0.02, "Data: Opta, ESPN, FotMob · Blue labels = Champions League · Grey labels = Serie A", fontsize=9, color=LIGHT)
fig.text(0.97, 0.02, "Analysis: Giorgos Drikos", ha="right", fontsize=9, color=LIGHT)
# 10. Αποθήκευση
plt.savefig("douvikas_season_form.png", dpi=200, facecolor=BACKGROUND, bbox_inches="tight")
print("Η φόρμα αποθηκεύτηκε!")