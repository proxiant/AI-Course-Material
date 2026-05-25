"""Additional diagrams for the textbook beyond the interview-prep set."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle, Polygon
import numpy as np

OUT = "/Users/pkr465/work/AI-Course-Material/AI_ML_GenAI_Textbook/Diagrams"
os.makedirs(OUT, exist_ok=True)

NAVY = "#1E2761"
ACCENT = "#2C5FF5"
LIGHT = "#F4F6FB"
GRAY = "#6B7280"
RED = "#D43F3F"
GREEN = "#3DA86D"
ORANGE = "#E89A3C"


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("WROTE", path)


# --- 21. AI/ML/DL/GenAI Venn diagram ---
def ai_taxonomy_venn():
    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
    circles = [
        (5, 5.2, 4.5, "Artificial Intelligence", "#E8ECF7", NAVY),
        (5, 4.6, 3.4, "Machine Learning", "#D4DEF2", NAVY),
        (5, 4.2, 2.4, "Deep Learning", ACCENT, "white"),
        (5, 4.0, 1.3, "Gen AI", NAVY, "white"),
    ]
    for cx, cy, r, label, fc, tc in circles:
        ax.add_patch(Circle((cx, cy), r, facecolor=fc, edgecolor=NAVY,
                            linewidth=1.5, alpha=0.85))
    for cx, cy, r, label, fc, tc in circles:
        ax.text(cx, cy + r - 0.4, label, ha="center", color=tc,
                fontsize=12, fontweight="bold")
    ax.set_title("Hierarchy of AI fields", color=NAVY, fontsize=14, fontweight="bold")
    save(fig, "21_ai_taxonomy.png")


# --- 22. Supervised vs unsupervised vs RL ---
def learning_paradigms():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    for ax in axes:
        ax.set_xlim(0, 5); ax.set_ylim(0, 4); ax.axis("off")

    # Supervised
    ax = axes[0]
    ax.set_title("Supervised Learning", color=NAVY, fontweight="bold", fontsize=12)
    np.random.seed(1)
    cls0 = np.random.randn(20, 2) * 0.4 + [1.5, 1.5]
    cls1 = np.random.randn(20, 2) * 0.4 + [3.5, 2.5]
    ax.scatter(cls0[:, 0], cls0[:, 1], color=ACCENT, s=40, label="Class A")
    ax.scatter(cls1[:, 0], cls1[:, 1], color=RED, s=40, label="Class B")
    ax.plot([1.0, 4.5], [3.5, 0.5], color=NAVY, linestyle="--", linewidth=2)
    ax.text(2.5, 0.3, "labeled pairs (x, y)", ha="center", color=NAVY, fontsize=10)
    ax.legend(loc="upper left", fontsize=9)

    # Unsupervised
    ax = axes[1]
    ax.set_title("Unsupervised Learning", color=NAVY, fontweight="bold", fontsize=12)
    np.random.seed(2)
    c1 = np.random.randn(15, 2) * 0.3 + [1.5, 3.0]
    c2 = np.random.randn(15, 2) * 0.3 + [3.5, 2.5]
    c3 = np.random.randn(15, 2) * 0.3 + [2.5, 1.0]
    for c, col in zip([c1, c2, c3], [ACCENT, ORANGE, GREEN]):
        ax.scatter(c[:, 0], c[:, 1], color=col, s=40)
    ax.text(2.5, 0.3, "unlabeled x; find structure", ha="center", color=NAVY, fontsize=10)

    # RL
    ax = axes[2]
    ax.set_title("Reinforcement Learning", color=NAVY, fontweight="bold", fontsize=12)
    ax.add_patch(FancyBboxPatch((0.4, 2.0), 1.6, 1.0, boxstyle="round,pad=0.05",
                                facecolor=ACCENT, edgecolor=NAVY))
    ax.text(1.2, 2.5, "Agent", ha="center", va="center", color="white", fontweight="bold")
    ax.add_patch(FancyBboxPatch((3.0, 2.0), 1.6, 1.0, boxstyle="round,pad=0.05",
                                facecolor=NAVY, edgecolor=NAVY))
    ax.text(3.8, 2.5, "Environment", ha="center", va="center", color="white", fontweight="bold")
    ax.annotate("", xy=(3.0, 2.7), xytext=(2.0, 2.7),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))
    ax.text(2.5, 2.95, "action", color=NAVY, fontsize=9)
    ax.annotate("", xy=(2.0, 2.3), xytext=(3.0, 2.3),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))
    ax.text(2.5, 1.95, "state, reward", color=RED, fontsize=9)
    ax.text(2.5, 0.3, "maximize cumulative reward", ha="center", color=NAVY, fontsize=10)

    save(fig, "22_learning_paradigms.png")


# --- 23. Bias-variance tradeoff ---
def bias_variance():
    fig, ax = plt.subplots(figsize=(9, 5))
    complexity = np.linspace(0, 10, 100)
    bias = 6 / (1 + complexity * 0.3)
    variance = 0.5 + 0.15 * complexity
    total = bias + variance
    ax.plot(complexity, bias, color=ACCENT, linewidth=2.5, label="Bias²")
    ax.plot(complexity, variance, color=RED, linewidth=2.5, label="Variance")
    ax.plot(complexity, total, color=NAVY, linewidth=3, label="Total error")
    sweet = complexity[np.argmin(total)]
    ax.axvline(sweet, color=GRAY, linestyle="--")
    ax.text(sweet + 0.2, 5.5, "sweet spot", color=NAVY, fontsize=10)
    ax.set_xlabel("Model complexity")
    ax.set_ylabel("Error")
    ax.set_title("Bias-variance tradeoff", color=NAVY, fontweight="bold", fontsize=13)
    ax.legend(); ax.grid(alpha=0.25)
    save(fig, "23_bias_variance.png")


# --- 24. Linear regression geometry ---
def linear_regression():
    fig, ax = plt.subplots(figsize=(8, 5))
    rng = np.random.default_rng(7)
    x = np.linspace(0, 10, 25)
    y = 0.7 * x + 1.5 + rng.normal(0, 0.8, 25)
    ax.scatter(x, y, color=ACCENT, s=50, zorder=3, label="data")
    slope, intercept = np.polyfit(x, y, 1)
    ax.plot(x, slope * x + intercept, color=NAVY, linewidth=2.5, label=f"y = {slope:.2f}x + {intercept:.2f}")
    for xi, yi in zip(x, y):
        ax.plot([xi, xi], [yi, slope * xi + intercept], color=RED, alpha=0.4, linewidth=1)
    ax.set_xlabel("x"); ax.set_ylabel("y")
    ax.set_title("Linear regression: minimize sum of squared residuals",
                 color=NAVY, fontweight="bold", fontsize=12)
    ax.legend(); ax.grid(alpha=0.25)
    save(fig, "24_linear_regression.png")


# --- 25. Logistic / softmax ---
def logistic_softmax():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    x = np.linspace(-6, 6, 200)
    axes[0].plot(x, 1/(1+np.exp(-x)), color=ACCENT, linewidth=2.5)
    axes[0].axhline(0.5, color=GRAY, linestyle="--")
    axes[0].set_title("Logistic (binary)", color=NAVY, fontweight="bold")
    axes[0].set_xlabel("z = wᵀx + b"); axes[0].set_ylabel("σ(z)")
    axes[0].grid(alpha=0.25)
    z = np.array([2.0, 1.0, 0.5, -0.3])
    soft = np.exp(z) / np.exp(z).sum()
    axes[1].bar(["class A", "class B", "class C", "class D"], soft,
                color=[NAVY, ACCENT, ORANGE, GREEN])
    axes[1].set_ylim(0, 1)
    axes[1].set_title("Softmax (multiclass)", color=NAVY, fontweight="bold")
    axes[1].set_ylabel("probability")
    for i, v in enumerate(soft):
        axes[1].text(i, v + 0.02, f"{v:.2f}", ha="center", color=NAVY, fontweight="bold")
    save(fig, "25_logistic_softmax.png")


# --- 26. Train/val/test split + cross validation ---
def data_splits():
    fig, axes = plt.subplots(2, 1, figsize=(11, 4.5))

    ax = axes[0]
    ax.set_xlim(0, 10); ax.set_ylim(0, 1.2); ax.axis("off")
    ax.add_patch(Rectangle((0, 0), 7, 0.6, facecolor=ACCENT, edgecolor=NAVY))
    ax.add_patch(Rectangle((7, 0), 1.5, 0.6, facecolor=ORANGE, edgecolor=NAVY))
    ax.add_patch(Rectangle((8.5, 0), 1.5, 0.6, facecolor=NAVY, edgecolor=NAVY))
    ax.text(3.5, 0.3, "Train (70%)", color="white", ha="center", va="center", fontweight="bold")
    ax.text(7.75, 0.3, "Val (15%)", color="white", ha="center", va="center", fontweight="bold")
    ax.text(9.25, 0.3, "Test (15%)", color="white", ha="center", va="center", fontweight="bold")
    ax.text(5, 0.9, "Standard hold-out split", ha="center", fontsize=12,
            color=NAVY, fontweight="bold")

    ax = axes[1]
    ax.set_xlim(0, 10); ax.set_ylim(-0.5, 5); ax.axis("off")
    ax.text(5, 4.5, "5-fold cross-validation", ha="center", fontsize=12,
            color=NAVY, fontweight="bold")
    for fold in range(5):
        y = 3.5 - fold * 0.7
        for k in range(5):
            color = ORANGE if k == fold else ACCENT
            ax.add_patch(Rectangle((k * 2, y), 1.9, 0.5,
                                   facecolor=color, edgecolor=NAVY))
        ax.text(-0.5, y + 0.25, f"Fold {fold+1}", ha="right",
                va="center", fontsize=9, color=NAVY)
    ax.add_patch(Rectangle((-0.5, -0.4), 0.4, 0.3, facecolor=ORANGE, edgecolor=NAVY))
    ax.text(0.05, -0.25, "= validation fold", va="center", fontsize=9, color=NAVY)
    ax.add_patch(Rectangle((3.5, -0.4), 0.4, 0.3, facecolor=ACCENT, edgecolor=NAVY))
    ax.text(4.0, -0.25, "= training fold", va="center", fontsize=9, color=NAVY)
    save(fig, "26_data_splits.png")


# --- 27. Confusion matrix ---
def confusion_matrix():
    fig, ax = plt.subplots(figsize=(6, 5.5))
    cm = np.array([[42, 8], [5, 45]])
    im = ax.imshow(cm, cmap="Blues")
    for i in range(2):
        for j in range(2):
            ax.text(j, i, str(cm[i, j]), ha="center", va="center",
                    fontsize=18, fontweight="bold",
                    color="white" if cm[i, j] > 25 else NAVY)
    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xticklabels(["Pred Neg", "Pred Pos"], fontsize=11)
    ax.set_yticklabels(["Actual Neg", "Actual Pos"], fontsize=11)
    ax.set_title("Confusion matrix (binary)", color=NAVY, fontweight="bold", fontsize=13)
    save(fig, "27_confusion_matrix.png")


# --- 28. ROC curve ---
def roc_curve():
    fig, ax = plt.subplots(figsize=(6, 6))
    fpr = np.linspace(0, 1, 100)
    for auc, name, c in [(0.95, "Excellent (AUC 0.95)", ACCENT),
                          (0.80, "Good (AUC 0.80)", NAVY),
                          (0.65, "Fair (AUC 0.65)", ORANGE)]:
        tpr = fpr ** ((1 - auc) / auc * 4 + 0.1)
        ax.plot(fpr, tpr, linewidth=2.5, color=c, label=name)
    ax.plot([0, 1], [0, 1], color=GRAY, linestyle="--", label="Random (AUC 0.5)")
    ax.set_xlabel("False Positive Rate")
    ax.set_ylabel("True Positive Rate")
    ax.set_title("ROC curves and AUC", color=NAVY, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.25)
    save(fig, "28_roc_curve.png")


# --- 29. Word2Vec skip-gram architecture ---
def word2vec_skipgram():
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.5, 2.5), 1.6, 1.4, boxstyle="round,pad=0.05",
                                facecolor=LIGHT, edgecolor=NAVY))
    ax.text(1.3, 3.2, "Input\n(center word)", ha="center", va="center", color=NAVY, fontsize=10)
    ax.add_patch(FancyBboxPatch((3.5, 2.5), 2.0, 1.4, boxstyle="round,pad=0.05",
                                facecolor=ACCENT, edgecolor=NAVY))
    ax.text(4.5, 3.2, "Projection\n(hidden)\nlookup", ha="center", va="center", color="white",
            fontweight="bold", fontsize=10)
    for i, name in enumerate(["w-2", "w-1", "w+1", "w+2"]):
        y = 0.5 + i * 1.3
        ax.add_patch(FancyBboxPatch((8.5, y), 1.6, 1.0, boxstyle="round,pad=0.05",
                                    facecolor=NAVY, edgecolor=NAVY))
        ax.text(9.3, y + 0.5, name, ha="center", va="center", color="white", fontweight="bold")
        ax.annotate("", xy=(8.5, y + 0.5), xytext=(5.5, 3.2),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1, alpha=0.6))
    ax.annotate("", xy=(3.5, 3.2), xytext=(2.1, 3.2),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.6))
    ax.text(11, 5.6, "Predict context words", color=NAVY, fontsize=11, fontweight="bold")
    ax.set_title("Word2Vec Skip-Gram: predict context from center",
                 color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "29_word2vec.png")


# --- 30. RoPE rotation ---
def rope_diagram():
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect("equal")
    ax.axhline(0, color=GRAY, linewidth=0.5); ax.axvline(0, color=GRAY, linewidth=0.5)
    angles_q = [0.3, 0.6, 0.9]
    angles_k = [0.3 + 0.4, 0.6 + 0.4, 0.9 + 0.4]
    for ang, c, lab in zip(angles_q, [ACCENT, ACCENT, ACCENT], ["Q@pos0", "Q@pos1", "Q@pos2"]):
        x, y = 2.5 * np.cos(ang), 2.5 * np.sin(ang)
        ax.arrow(0, 0, x, y, head_width=0.12, color=c, length_includes_head=True)
        ax.text(x*1.1, y*1.1, lab, color=c, fontsize=9)
    for ang, c, lab in zip(angles_k, [NAVY, NAVY, NAVY], ["K@pos0", "K@pos1", "K@pos2"]):
        x, y = 2.0 * np.cos(ang), 2.0 * np.sin(ang)
        ax.arrow(0, 0, x, y, head_width=0.12, color=c, length_includes_head=True)
        ax.text(x*1.15, y*1.15, lab, color=c, fontsize=9)
    ax.set_title("RoPE: position rotates Q and K in 2D subspaces",
                 color=NAVY, fontweight="bold")
    ax.grid(alpha=0.25)
    save(fig, "30_rope.png")


# --- 31. Diffusion forward and reverse ---
def diffusion_process():
    fig, axes = plt.subplots(2, 5, figsize=(13, 5.5))
    rng = np.random.default_rng(42)
    img = np.zeros((40, 40))
    cx, cy = 20, 20
    yy, xx = np.mgrid[:40, :40]
    img = np.exp(-((xx - cx)**2 + (yy - cy)**2) / 60)

    for i, t in enumerate([0, 0.25, 0.5, 0.75, 1.0]):
        noise = rng.normal(0, 1, (40, 40))
        noised = (1 - t)**0.5 * img + t**0.5 * noise
        axes[0, i].imshow(noised, cmap="Blues")
        axes[0, i].set_title(f"t={t:.2f}", color=NAVY, fontsize=10)
        axes[0, i].axis("off")
    axes[0, 0].set_ylabel("Forward (add noise)", color=NAVY, fontweight="bold")
    fig.text(0.05, 0.71, "Forward (add noise)", color=NAVY, fontweight="bold",
             rotation=90, fontsize=11)

    for i, t in enumerate([1.0, 0.75, 0.5, 0.25, 0.0]):
        noise = rng.normal(0, 1, (40, 40))
        noised = (1 - t)**0.5 * img + t**0.5 * noise
        axes[1, i].imshow(noised, cmap="Oranges")
        axes[1, i].set_title(f"t={t:.2f}", color=NAVY, fontsize=10)
        axes[1, i].axis("off")
    fig.text(0.05, 0.27, "Reverse (denoise)", color=NAVY, fontweight="bold",
             rotation=90, fontsize=11)
    fig.suptitle("Diffusion model: forward adds noise, reverse denoises",
                 color=NAVY, fontsize=13, fontweight="bold", y=1.02)
    plt.tight_layout()
    save(fig, "31_diffusion.png")


# --- 32. PPO clipped objective ---
def ppo_clip():
    fig, ax = plt.subplots(figsize=(9, 5))
    r = np.linspace(0, 2.5, 200)
    eps = 0.2
    adv_pos = 1.0
    adv_neg = -1.0
    # positive advantage
    pos_unclipped = r * adv_pos
    pos_clipped = np.clip(r, 1-eps, 1+eps) * adv_pos
    pos_obj = np.minimum(pos_unclipped, pos_clipped)
    ax.plot(r, pos_obj, color=ACCENT, linewidth=2.5, label="positive advantage (A > 0)")
    # negative advantage
    neg_unclipped = r * adv_neg
    neg_clipped = np.clip(r, 1-eps, 1+eps) * adv_neg
    neg_obj = np.minimum(neg_unclipped, neg_clipped)
    ax.plot(r, neg_obj, color=RED, linewidth=2.5, label="negative advantage (A < 0)")
    ax.axvline(1-eps, color=GRAY, linestyle="--")
    ax.axvline(1+eps, color=GRAY, linestyle="--")
    ax.axvline(1.0, color="black", linestyle="-", linewidth=0.5)
    ax.set_xlabel("probability ratio r = π_θ(a|s) / π_old(a|s)")
    ax.set_ylabel("clipped objective")
    ax.set_title("PPO clipped surrogate objective", color=NAVY, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.25)
    save(fig, "32_ppo_clip.png")


# --- 33. HNSW graph layers ---
def hnsw_diagram():
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    rng = np.random.default_rng(11)
    layers = [
        (5.0, 12, "Layer 2 (sparse)"),
        (3.0, 30, "Layer 1 (denser)"),
        (1.0, 60, "Layer 0 (all points)"),
    ]
    for y, n, name in layers:
        pts = rng.uniform(0.5, 9.5, (n, 1))
        ys = rng.uniform(y - 0.4, y + 0.4, n)
        ax.scatter(pts[:, 0], ys, color=ACCENT, s=18, alpha=0.6)
        ax.text(10.2, y, name, color=NAVY, fontsize=10, va="center", fontweight="bold")
    # search path
    ax.plot([3.0, 4.0, 4.5, 5.0], [5.0, 3.0, 2.0, 1.0], "o-",
            color=RED, linewidth=2, markersize=8, label="search path")
    ax.text(5.3, 5.6, "Query enters at top layer", color=RED, fontsize=10)
    ax.text(5.3, 0.5, "drops to denser layers as it gets closer",
            color=RED, fontsize=10)
    ax.set_title("HNSW: hierarchical navigable small world graph",
                 color=NAVY, fontweight="bold", fontsize=13)
    save(fig, "33_hnsw.png")


# --- 34. MoE diagram ---
def moe_diagram():
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 6); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.5, 2.3), 1.4, 1.4, boxstyle="round,pad=0.05",
                                facecolor=LIGHT, edgecolor=NAVY))
    ax.text(1.2, 3.0, "Input\ntoken", ha="center", va="center", color=NAVY, fontweight="bold")
    ax.add_patch(FancyBboxPatch((2.5, 2.3), 1.6, 1.4, boxstyle="round,pad=0.05",
                                facecolor=ORANGE, edgecolor=NAVY))
    ax.text(3.3, 3.0, "Router\n(gating)", ha="center", va="center", color="white", fontweight="bold")
    experts = ["Expert 1", "Expert 2", "Expert 3", "Expert 4", "...", "Expert N"]
    active = [True, False, True, False, False, False]
    for i, (e, a) in enumerate(zip(experts, active)):
        y = 5.4 - i * 0.85
        c = ACCENT if a else "#C0C0C0"
        ax.add_patch(FancyBboxPatch((5.5, y), 1.6, 0.7, boxstyle="round,pad=0.05",
                                    facecolor=c, edgecolor=NAVY))
        ax.text(6.3, y + 0.35, e, ha="center", va="center", color="white", fontweight="bold")
        lw = 2 if a else 0.5
        ax.annotate("", xy=(5.5, y + 0.35), xytext=(4.1, 3.0),
                    arrowprops=dict(arrowstyle="->", color=NAVY if a else GRAY,
                                    lw=lw, alpha=1 if a else 0.4))
    ax.add_patch(FancyBboxPatch((8.5, 2.3), 1.6, 1.4, boxstyle="round,pad=0.05",
                                facecolor=NAVY, edgecolor=NAVY))
    ax.text(9.3, 3.0, "Combine\n(weighted)", ha="center", va="center", color="white", fontweight="bold")
    ax.add_patch(FancyBboxPatch((10.5, 2.3), 1.4, 1.4, boxstyle="round,pad=0.05",
                                facecolor="#3D4A8C", edgecolor=NAVY))
    ax.text(11.2, 3.0, "Output", ha="center", va="center", color="white", fontweight="bold")
    for x0, x1 in [(1.9, 2.5), (4.1, 5.5), (7.1, 8.5), (10.1, 10.5)]:
        if x0 == 4.1: continue
        ax.annotate("", xy=(x1, 3.0), xytext=(x0, 3.0),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))
    ax.set_title("Mixture of Experts: router activates top-k experts per token",
                 color=NAVY, fontweight="bold", fontsize=13)
    save(fig, "34_moe.png")


# --- 35. Tokenization comparison ---
def tokenization_comparison():
    fig, axes = plt.subplots(3, 1, figsize=(11, 4.5))
    schemes = [
        ("Word-level", ["The", "transformer", "revolutionized", "NLP", "."], NAVY),
        ("Character-level", list("The transformer.")[:14], ACCENT),
        ("BPE (subword)", ["The", " transform", "er", " revol", "ution", "ized", " NLP", "."], ORANGE),
    ]
    for ax, (name, toks, col) in zip(axes, schemes):
        ax.set_xlim(0, 12); ax.set_ylim(0, 1); ax.axis("off")
        ax.text(0, 0.5, name, color=NAVY, fontsize=11, fontweight="bold", va="center")
        x = 2.4
        for tok in toks:
            w = min(0.4 + len(tok) * 0.18, 2.0)
            ax.add_patch(FancyBboxPatch((x, 0.2), w, 0.6, boxstyle="round,pad=0.03",
                                        facecolor=col, edgecolor=NAVY))
            ax.text(x + w/2, 0.5, repr(tok), ha="center", va="center",
                    color="white", fontsize=9, fontweight="bold")
            x += w + 0.1
            if x > 11.5: break
    plt.suptitle("Tokenization schemes compared", color=NAVY,
                 fontweight="bold", fontsize=13)
    save(fig, "35_tokenization_compare.png")


# --- 36. Loss landscape ---
def loss_landscape():
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(121, projection="3d")
    x = np.linspace(-3, 3, 60)
    y = np.linspace(-3, 3, 60)
    X, Y = np.meshgrid(x, y)
    Z = (X**2 + Y**2) * 0.3 + np.sin(X * 2) * 0.5 + np.cos(Y * 2) * 0.4
    ax.plot_surface(X, Y, Z, cmap="Blues", alpha=0.85, edgecolor="none")
    ax.set_title("Non-convex loss surface", color=NAVY, fontweight="bold")
    ax.set_xlabel("w₁"); ax.set_ylabel("w₂"); ax.set_zlabel("L")

    ax2 = fig.add_subplot(122)
    ax2.contour(X, Y, Z, levels=20, colors=GRAY, alpha=0.5, linewidths=0.7)
    # Path with momentum
    path = [(-2.5, 2.5)]
    v = np.array([0.0, 0.0])
    pos = np.array([-2.5, 2.5])
    for _ in range(25):
        grad = np.array([2 * 0.3 * pos[0] + 2 * np.cos(pos[0] * 2),
                         2 * 0.3 * pos[1] - 2 * np.sin(pos[1] * 2)])
        v = 0.7 * v - 0.1 * grad
        pos = pos + v
        path.append(tuple(pos))
    path = np.array(path)
    ax2.plot(path[:, 0], path[:, 1], "o-", color=RED, linewidth=2,
             markersize=4, label="SGD + momentum")
    ax2.set_xlabel("w₁"); ax2.set_ylabel("w₂")
    ax2.set_title("Optimization trajectory", color=NAVY, fontweight="bold")
    ax2.legend(); ax2.grid(alpha=0.25)
    save(fig, "36_loss_landscape.png")


# --- 37. Diffusion latent space concept ---
def latent_space_concept():
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    np.random.seed(3)
    for ax, title in zip(axes, ["Pixel space (high-dim, sparse)",
                                "Encoder",
                                "Latent space (low-dim, dense)"]):
        ax.set_title(title, color=NAVY, fontweight="bold")

    # Pixel space
    ax = axes[0]
    pts = np.random.randn(80, 2) * 2
    ax.scatter(pts[:, 0], pts[:, 1], alpha=0.4, color=GRAY)
    ax.set_xlim(-6, 6); ax.set_ylim(-6, 6); ax.set_aspect("equal")
    ax.text(0, 5.0, "many irrelevant dims", color=NAVY, ha="center", fontsize=9, fontstyle="italic")
    ax.grid(alpha=0.25)

    # Encoder
    ax = axes[1]
    ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.axis("off")
    ax.add_patch(FancyBboxPatch((1, 1.5), 3, 2, boxstyle="round,pad=0.05",
                                facecolor=ACCENT, edgecolor=NAVY))
    ax.text(2.5, 2.5, "Encoder\n(neural net)", ha="center", va="center",
            color="white", fontweight="bold", fontsize=12)

    # Latent space
    ax = axes[2]
    cl1 = np.random.randn(25, 2) * 0.4 + [1.5, 1.5]
    cl2 = np.random.randn(25, 2) * 0.4 + [-1.5, -1.0]
    cl3 = np.random.randn(25, 2) * 0.4 + [1.0, -1.5]
    for c, col, lab in zip([cl1, cl2, cl3], [ACCENT, RED, GREEN], ["A", "B", "C"]):
        ax.scatter(c[:, 0], c[:, 1], color=col, s=40, alpha=0.7, label=f"class {lab}")
    ax.set_xlim(-3, 3); ax.set_ylim(-3, 3); ax.set_aspect("equal")
    ax.legend(loc="upper right", fontsize=9)
    ax.grid(alpha=0.25)
    save(fig, "37_latent_space.png")


# --- 38. Chinchilla scaling ---
def chinchilla():
    fig, ax = plt.subplots(figsize=(8, 5))
    params = np.array([0.5, 1, 3, 7, 13, 30, 70, 175])
    tokens = params * 20  # Chinchilla rule
    ax.loglog(params, tokens, "o-", color=ACCENT, linewidth=2.5,
              markersize=10, label="Chinchilla-optimal: 20 tokens/param")
    annotations = {0.5: "GPT-2 small", 7: "LLaMA-7B", 70: "LLaMA-70B",
                   175: "GPT-3 175B"}
    for p, lab in annotations.items():
        idx = list(params).index(p)
        ax.annotate(lab, (params[idx], tokens[idx]),
                    xytext=(8, 8), textcoords="offset points",
                    fontsize=9, color=NAVY)
    ax.set_xlabel("Parameters (billions)")
    ax.set_ylabel("Training tokens (billions)")
    ax.set_title("Chinchilla scaling: parameters vs tokens",
                 color=NAVY, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.25, which="both")
    save(fig, "38_chinchilla.png")


# --- 39. Production RAG architecture ---
def production_rag_arch():
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis("off")

    # Ingestion (top)
    ax.text(2, 7.4, "INGESTION PIPELINE", color=NAVY, fontweight="bold", fontsize=11)
    blocks_ing = [("Sources\n(S3, DBs, APIs)", 0.3, "#E8ECF7"),
                  ("Document\nLoader", 2.3, ACCENT),
                  ("Chunker", 4.3, ACCENT),
                  ("Embedder", 6.3, NAVY),
                  ("Vector\nStore", 8.3, "#3D4A8C")]
    for name, x, c in blocks_ing:
        ax.add_patch(FancyBboxPatch((x, 5.5), 1.7, 1.4, boxstyle="round,pad=0.05",
                                    facecolor=c, edgecolor=NAVY))
        tc = "white" if c != "#E8ECF7" else NAVY
        ax.text(x + 0.85, 6.2, name, ha="center", va="center", color=tc, fontweight="bold", fontsize=9)
    for i in range(len(blocks_ing) - 1):
        x0 = blocks_ing[i][1] + 1.7; x1 = blocks_ing[i+1][1]
        ax.annotate("", xy=(x1, 6.2), xytext=(x0, 6.2),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))

    # Query path (bottom)
    ax.text(2, 4.4, "QUERY PIPELINE", color=NAVY, fontweight="bold", fontsize=11)
    blocks_q = [("User\nQuery", 0.3, "#E8ECF7"),
                ("Query\nRewriter", 2.3, "#6B7AE0"),
                ("Embedder", 4.3, NAVY),
                ("Retrieval\n+ Rerank", 6.3, ACCENT),
                ("Prompt\nBuilder", 8.3, "#6B7AE0"),
                ("LLM\nGenerator", 10.3, NAVY),
                ("Response", 12.3, "#3D4A8C")]
    for name, x, c in blocks_q:
        ax.add_patch(FancyBboxPatch((x, 2.5), 1.7, 1.4, boxstyle="round,pad=0.05",
                                    facecolor=c, edgecolor=NAVY))
        tc = "white" if c != "#E8ECF7" else NAVY
        ax.text(x + 0.85, 3.2, name, ha="center", va="center", color=tc, fontweight="bold", fontsize=9)
    for i in range(len(blocks_q) - 1):
        x0 = blocks_q[i][1] + 1.7; x1 = blocks_q[i+1][1]
        ax.annotate("", xy=(x1, 3.2), xytext=(x0, 3.2),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))
    # link store -> retrieval
    ax.annotate("", xy=(7.0, 3.9), xytext=(9.0, 5.5),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    ax.text(7.5, 4.8, "lookup", color=RED, fontsize=9, fontweight="bold")

    # Cross-cutting
    ax.text(2, 1.4, "CROSS-CUTTING: caching • observability • guardrails • evaluation",
            color=NAVY, fontstyle="italic", fontsize=11)
    ax.add_patch(Rectangle((0.2, 0.7), 13.5, 1.0, facecolor="#F4F6FB",
                           edgecolor=GRAY, linestyle="--"))

    ax.set_title("Production RAG: ingestion plus query plus cross-cutting concerns",
                 color=NAVY, fontweight="bold", fontsize=14)
    save(fig, "39_production_rag.png")


# --- 40. RLHF detailed three-stage ---
def rlhf_detailed():
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 7); ax.axis("off")

    stages = [
        (0.5, "Stage 1: SFT",
         ["Base LLM", "(prompt, ideal\nresponse) pairs",
          "Fine-tune\nwith CE loss", "SFT model"],
         ACCENT),
        (4.7, "Stage 2: Reward Model",
         ["SFT model\n(generator)", "Generate N\nresponses",
          "Human\npairwise ranking", "Train RM"],
         "#6B7AE0"),
        (8.9, "Stage 3: PPO",
         ["SFT model\n(reference)", "Generate response",
          "Score with RM\n+ KL penalty", "Update via PPO"],
         NAVY),
    ]
    for x0, title, items, col in stages:
        ax.text(x0 + 1.6, 6.4, title, color=NAVY, fontweight="bold", fontsize=12,
                ha="center")
        for i, item in enumerate(items):
            y = 5.5 - i * 1.3
            ax.add_patch(FancyBboxPatch((x0, y), 3.2, 1.0,
                                        boxstyle="round,pad=0.05",
                                        facecolor=col, edgecolor=NAVY))
            ax.text(x0 + 1.6, y + 0.5, item, ha="center", va="center",
                    color="white", fontweight="bold", fontsize=10)
            if i < len(items) - 1:
                ax.annotate("", xy=(x0 + 1.6, y - 0.05), xytext=(x0 + 1.6, y - 0.25),
                            arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.5))

    # Inter-stage arrows
    ax.annotate("", xy=(4.6, 0.55), xytext=(3.8, 0.55),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2))
    ax.annotate("", xy=(8.8, 0.55), xytext=(8.0, 0.55),
                arrowprops=dict(arrowstyle="->", color=RED, lw=2))

    ax.set_title("RLHF in three stages", color=NAVY, fontweight="bold", fontsize=14)
    save(fig, "40_rlhf_detailed.png")


if __name__ == "__main__":
    ai_taxonomy_venn()
    learning_paradigms()
    bias_variance()
    linear_regression()
    logistic_softmax()
    data_splits()
    confusion_matrix()
    roc_curve()
    word2vec_skipgram()
    rope_diagram()
    diffusion_process()
    ppo_clip()
    hnsw_diagram()
    moe_diagram()
    tokenization_comparison()
    loss_landscape()
    latent_space_concept()
    chinchilla()
    production_rag_arch()
    rlhf_detailed()
    print("All textbook diagrams generated.")
