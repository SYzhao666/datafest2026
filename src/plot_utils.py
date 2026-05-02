import matplotlib.pyplot as plt
import seaborn as sns
from config import OUTPUTS_FIG

# Shared style — call once at the top of each notebook
def set_style():
    sns.set_theme(style="whitegrid", palette="muted", font_scale=1.1)
    plt.rcParams["figure.dpi"] = 130
    plt.rcParams["savefig.bbox"] = "tight"

def save_fig(fig, filename):
    """Save to outputs/figures/ as both PNG and PDF."""
    OUTPUTS_FIG.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUTS_FIG / f"{filename}.png")
    fig.savefig(OUTPUTS_FIG / f"{filename}.pdf")
    print(f"Saved: {filename}")