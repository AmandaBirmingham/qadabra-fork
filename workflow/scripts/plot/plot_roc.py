from collections import defaultdict

import joblib
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


plt.style.use(snakemake.params[0])
tools = snakemake.config["tools"]
palette = dict(zip(
    tools, sns.color_palette("colorblind", len(tools))
))

pctile = snakemake.wildcards["pctile"]

models = defaultdict(dict)
for tool, model_loc in zip(tools, snakemake.input):
    models[tool] = joblib.load(model_loc)

fig, ax = plt.subplots(1, 1)
ax.set_aspect("equal")

best_tool = None
best_auc = 0
leg_lines = []
for tool in tools:
    this_model_data = models[tool]
    mean_fprs = this_model_data["fprs"]
    mean_tprs = np.mean(this_model_data["tprs"], axis=0)

    aucs = this_model_data["aucs"]
    mean_auc = np.mean(aucs)
    std_auc = np.std(aucs)

    if mean_auc > best_auc:
        best_auc = mean_auc
        best_tool = tool

    color = palette[tool]
    line = Line2D([0], [0], color=color, label=f"{tool} ({mean_auc:.2f} $\pm$ {std_auc:.2f})")
    leg_lines.append(line)

    ax.plot(mean_fprs, mean_tprs, lw=1, color=color)

leg = ax.legend(handles=leg_lines, loc="lower right", frameon=False)
for text in leg.get_texts():
    if best_tool in text._text:
        text.set_weight("bold")

ax.plot([0, 1], [0, 1], linestyle="--", lw=2, color="black")
ax.set_xlabel("False Positive Rate")
ax.set_ylabel("True Positive Rate")
ax.set_title(f"{pctile}% Features")

plt.savefig(snakemake.output[0])