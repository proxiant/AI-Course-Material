"""Generate all the PNG diagrams embedded in the textbook."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle, Circle
import numpy as np

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Diagrams")
os.makedirs(OUT, exist_ok=True)

NAVY = "#1E2761"
ACCENT = "#2C5FF5"
LIGHT = "#F4F6FB"
GRAY = "#6B7280"


def save(fig, name):
    path = os.path.join(OUT, name)
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("WROTE", path)


# --- 1. ANN architecture ---
def ann_architecture():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    layers = [("Input\n(4 features)", 0.8, 4), ("Hidden 1\n(6 neurons)", 3.5, 6),
              ("Hidden 2\n(4 neurons)", 6.2, 4), ("Output\n(3 classes)", 8.9, 3)]
    centers = []
    for name, x, n in layers:
        ys = np.linspace(0.7, 5.3, n)
        nodes = []
        for y in ys:
            c = Circle((x, y), 0.22, facecolor=ACCENT, edgecolor=NAVY, linewidth=1.5, zorder=3)
            ax.add_patch(c); nodes.append((x, y))
        centers.append(nodes)
        ax.text(x, 5.8, name, ha="center", fontsize=10, color=NAVY, fontweight="bold")
    for a, b in zip(centers[:-1], centers[1:]):
        for p in a:
            for q in b:
                ax.plot([p[0], q[0]], [p[1], q[1]], color=GRAY, linewidth=0.4, alpha=0.5, zorder=1)
    ax.set_title("Feedforward Artificial Neural Network", color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "01_ann_architecture.png")


# --- 2. Neuron with activation ---
def neuron_with_activation():
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    inputs = [("x1", 1, 4), ("x2", 1, 3), ("x3", 1, 2), ("x4", 1, 1)]
    weights = ["w1", "w2", "w3", "w4"]
    for (name, x, y), w in zip(inputs, weights):
        ax.add_patch(Circle((x, y), 0.25, facecolor=LIGHT, edgecolor=NAVY))
        ax.text(x, y, name, ha="center", va="center", fontsize=10)
        ax.annotate("", xy=(4.2, 2.5), xytext=(x + 0.25, y),
                    arrowprops=dict(arrowstyle="->", color=GRAY, lw=1.2))
        ax.text((x + 4.2) / 2 + 0.3, (y + 2.5) / 2 + 0.05, w, color=NAVY, fontsize=9, fontweight="bold")
    ax.add_patch(FancyBboxPatch((4.2, 1.9), 1.4, 1.2,
                                boxstyle="round,pad=0.05", facecolor=ACCENT, edgecolor=NAVY))
    ax.text(4.9, 2.5, "Σ + b", ha="center", va="center", color="white", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(7.0, 2.5), xytext=(5.6, 2.5),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.8))
    ax.text(6.3, 2.8, "z", color=NAVY, fontsize=10)
    ax.add_patch(FancyBboxPatch((7.0, 1.9), 1.4, 1.2,
                                boxstyle="round,pad=0.05", facecolor=NAVY, edgecolor=NAVY))
    ax.text(7.7, 2.5, "f(z)", ha="center", va="center", color="white", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(9.5, 2.5), xytext=(8.4, 2.5),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.8))
    ax.text(9.0, 2.8, "a", color=NAVY, fontsize=10)
    ax.set_title("Single neuron: weighted sum, bias, activation", color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "02_neuron.png")


# --- 3. Activation functions ---
def activation_functions():
    fig, axes = plt.subplots(1, 4, figsize=(13, 3.5))
    x = np.linspace(-5, 5, 200)
    funcs = [
        ("Sigmoid", 1 / (1 + np.exp(-x))),
        ("Tanh", np.tanh(x)),
        ("ReLU", np.maximum(0, x)),
        ("Leaky ReLU", np.where(x > 0, x, 0.1 * x)),
    ]
    for ax, (name, y) in zip(axes, funcs):
        ax.plot(x, y, color=ACCENT, linewidth=2.4)
        ax.axhline(0, color=GRAY, linewidth=0.5)
        ax.axvline(0, color=GRAY, linewidth=0.5)
        ax.set_title(name, color=NAVY, fontweight="bold")
        ax.grid(alpha=0.25)
    fig.suptitle("Common activation functions", color=NAVY, fontsize=14, fontweight="bold")
    save(fig, "03_activations.png")


# --- 4. Backpropagation ---
def backprop_diagram():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    blocks = [("Input", 0.6), ("Layer 1", 2.3), ("Layer 2", 4.0), ("Output", 5.7), ("Loss", 7.4)]
    for name, x in blocks:
        ax.add_patch(FancyBboxPatch((x, 2.5), 1.2, 1.0, boxstyle="round,pad=0.05",
                                    facecolor=ACCENT, edgecolor=NAVY))
        ax.text(x + 0.6, 3.0, name, ha="center", va="center", color="white", fontweight="bold")
    for i in range(len(blocks) - 1):
        x0 = blocks[i][1] + 1.2
        x1 = blocks[i + 1][1]
        ax.annotate("", xy=(x1, 3.3), xytext=(x0, 3.3),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.6))
    ax.text(4.7, 3.9, "Forward pass", color=NAVY, fontsize=11, fontweight="bold")
    for i in range(len(blocks) - 1):
        x0 = blocks[i + 1][1]
        x1 = blocks[i][1] + 1.2
        ax.annotate("", xy=(x1, 2.7), xytext=(x0, 2.7),
                    arrowprops=dict(arrowstyle="->", color="#D43F3F", lw=1.6))
    ax.text(3.8, 1.9, "Backward pass: ∂L/∂w via chain rule",
            color="#D43F3F", fontsize=11, fontweight="bold")
    ax.set_title("Backpropagation: forward then backward",
                 color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "04_backprop.png")


# --- 5. Vanishing/exploding gradient ---
def vanishing_gradient():
    fig, ax = plt.subplots(figsize=(8, 4))
    layers = np.arange(1, 21)
    vanish = 0.5 ** (layers - 1)
    explode = 1.4 ** (layers - 1)
    ax.semilogy(layers, vanish, "o-", color=ACCENT, label="Vanishing (×0.5 per layer)", linewidth=2)
    ax.semilogy(layers, explode, "s-", color="#D43F3F", label="Exploding (×1.4 per layer)", linewidth=2)
    ax.axhline(1.0, color=GRAY, linestyle="--")
    ax.set_xlabel("Layer (depth)")
    ax.set_ylabel("Gradient magnitude (log scale)")
    ax.set_title("Vanishing and exploding gradients", color=NAVY, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.25)
    save(fig, "05_vanishing_gradient.png")


# --- 6. Gradient descent variants ---
def gradient_descent():
    fig, ax = plt.subplots(figsize=(7, 5))
    x = np.linspace(-3, 3, 80)
    y = np.linspace(-3, 3, 80)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + 2 * Y**2
    ax.contour(X, Y, Z, levels=15, colors=GRAY, alpha=0.4, linewidths=0.7)
    pts_gd = [(2.5, 2.5)]
    cur = np.array([2.5, 2.5])
    for _ in range(12):
        cur = cur - 0.1 * np.array([2 * cur[0], 4 * cur[1]])
        pts_gd.append(tuple(cur))
    pts_gd = np.array(pts_gd)
    ax.plot(pts_gd[:, 0], pts_gd[:, 1], "o-", color=NAVY, label="GD (smooth)", linewidth=2)
    cur = np.array([-2.7, 2.3])
    pts_sgd = [tuple(cur)]
    rng = np.random.default_rng(7)
    for _ in range(14):
        grad = np.array([2 * cur[0], 4 * cur[1]]) + rng.normal(scale=0.7, size=2)
        cur = cur - 0.1 * grad
        pts_sgd.append(tuple(cur))
    pts_sgd = np.array(pts_sgd)
    ax.plot(pts_sgd[:, 0], pts_sgd[:, 1], "s-", color=ACCENT, label="SGD (noisy)", linewidth=1.5)
    ax.plot(0, 0, "*", color="#D43F3F", markersize=18, label="Minimum")
    ax.set_title("Gradient descent vs SGD on a quadratic", color=NAVY, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.25)
    save(fig, "06_gradient_descent.png")


# --- 7. CNN structure ---
def cnn_structure():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4); ax.axis("off")
    stages = [("Input\n(image)", 0.5, LIGHT),
              ("Conv\n+ReLU", 2.2, ACCENT),
              ("Pool", 4.1, NAVY),
              ("Conv\n+ReLU", 5.7, ACCENT),
              ("Pool", 7.6, NAVY),
              ("Flatten", 9.0, "#6B7AE0"),
              ("FC + Softmax", 10.4, "#3D4A8C")]
    for name, x, c in stages:
        ax.add_patch(FancyBboxPatch((x, 1.4), 1.3, 1.6,
                                    boxstyle="round,pad=0.05", facecolor=c, edgecolor=NAVY))
        ax.text(x + 0.65, 2.2, name, ha="center", va="center",
                color="white" if c != LIGHT else NAVY, fontsize=10, fontweight="bold")
    for i in range(len(stages) - 1):
        x0 = stages[i][1] + 1.3; x1 = stages[i + 1][1]
        ax.annotate("", xy=(x1, 2.2), xytext=(x0, 2.2),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.6))
    ax.set_title("Typical CNN pipeline for image classification",
                 color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "07_cnn.png")


# --- 8. RNN unrolled ---
def rnn_unrolled():
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    for i, t in enumerate(["t-2", "t-1", "t", "t+1"]):
        x = 1 + i * 2.2
        ax.add_patch(Circle((x, 2.4), 0.45, facecolor=ACCENT, edgecolor=NAVY, linewidth=1.5))
        ax.text(x, 2.4, "h", ha="center", va="center", color="white", fontweight="bold")
        ax.text(x, 0.7, f"x[{t}]", ha="center", fontsize=10)
        ax.text(x, 4.1, f"y[{t}]", ha="center", fontsize=10)
        ax.annotate("", xy=(x, 1.95), xytext=(x, 1.05),
                    arrowprops=dict(arrowstyle="->", color=NAVY))
        ax.annotate("", xy=(x, 3.85), xytext=(x, 2.85),
                    arrowprops=dict(arrowstyle="->", color=NAVY))
        if i < 3:
            ax.annotate("", xy=(x + 1.75, 2.4), xytext=(x + 0.45, 2.4),
                        arrowprops=dict(arrowstyle="->", color="#D43F3F", lw=1.8))
            ax.text(x + 1.1, 2.7, "W_h", color="#D43F3F", fontsize=9, fontweight="bold")
    ax.set_title("Recurrent Neural Network unrolled in time",
                 color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "08_rnn.png")


# --- 9. Transformer architecture ---
def transformer_arch():
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")

    def block(x, y, w, h, text, color):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                    facecolor=color, edgecolor=NAVY))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center",
                color="white", fontsize=9, fontweight="bold")

    block(0.5, 0.5, 3.4, 0.7, "Input embedding + positional encoding", LIGHT)
    ax.patches[-1].set_facecolor("#E8ECF7")
    ax.texts[-1].set_color(NAVY)

    block(0.5, 1.8, 3.4, 0.9, "Multi-head self-attention", ACCENT)
    block(0.5, 3.0, 3.4, 0.7, "Add & Norm", NAVY)
    block(0.5, 4.0, 3.4, 0.9, "Feed Forward", ACCENT)
    block(0.5, 5.2, 3.4, 0.7, "Add & Norm", NAVY)
    ax.text(2.2, 6.3, "Encoder × N", ha="center", color=NAVY, fontsize=12, fontweight="bold")

    block(6.1, 0.5, 3.4, 0.7, "Output embedding + positional encoding", "#E8ECF7")
    ax.texts[-1].set_color(NAVY)
    block(6.1, 1.8, 3.4, 0.9, "Masked multi-head self-attention", ACCENT)
    block(6.1, 3.0, 3.4, 0.7, "Add & Norm", NAVY)
    block(6.1, 4.0, 3.4, 0.9, "Cross-attention (Q from dec, K/V from enc)", ACCENT)
    block(6.1, 5.2, 3.4, 0.7, "Add & Norm", NAVY)
    block(6.1, 6.2, 3.4, 0.9, "Feed Forward", ACCENT)
    block(6.1, 7.4, 3.4, 0.7, "Add & Norm", NAVY)
    ax.text(7.8, 8.5, "Decoder × N", ha="center", color=NAVY, fontsize=12, fontweight="bold")
    block(6.1, 8.9, 3.4, 0.7, "Linear + Softmax (output)", NAVY)

    ax.annotate("", xy=(6.1, 4.4), xytext=(3.9, 5.5),
                arrowprops=dict(arrowstyle="->", color="#D43F3F", lw=2))
    ax.text(4.9, 5.5, "K, V", color="#D43F3F", fontsize=10, fontweight="bold")

    ax.set_title("Transformer architecture (Vaswani et al. 2017)",
                 color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "09_transformer.png")


# --- 10. Attention (Q,K,V) ---
def attention_qkv():
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 5); ax.axis("off")
    inputs = [("X1", 0.7), ("X2", 0.7 + 0.9), ("X3", 0.7 + 1.8), ("X4", 0.7 + 2.7)]
    for name, x in inputs:
        ax.add_patch(Circle((x, 4.0), 0.27, facecolor=LIGHT, edgecolor=NAVY))
        ax.text(x, 4.0, name, ha="center", va="center", fontsize=9)
    for label, x_off, col in [("Q", 0, "#6B7AE0"), ("K", 1.5, ACCENT), ("V", 3.0, NAVY)]:
        for i, (_, x) in enumerate(inputs):
            ax.add_patch(Rectangle((4.5 + x_off, 0.5 + i * 0.6), 0.7, 0.45,
                                   facecolor=col, edgecolor=NAVY))
            ax.text(4.85 + x_off, 0.72 + i * 0.6, label, ha="center", va="center",
                    color="white", fontsize=9, fontweight="bold")
            ax.annotate("", xy=(4.85 + x_off, 0.95 + i * 0.6), xytext=(x, 3.75),
                        arrowprops=dict(arrowstyle="->", color=GRAY, lw=0.6))
    ax.text(5.1, 4.5, "Q = X·Wq", color="#6B7AE0", fontsize=10)
    ax.text(6.7, 4.5, "K = X·Wk", color=ACCENT, fontsize=10)
    ax.text(8.3, 4.5, "V = X·Wv", color=NAVY, fontsize=10)
    ax.add_patch(FancyBboxPatch((9.4, 1.5), 1.4, 1.2,
                                boxstyle="round,pad=0.05", facecolor=NAVY, edgecolor=NAVY))
    ax.text(10.1, 2.1, "softmax\n(QKᵀ/√d)·V", ha="center", va="center",
            color="white", fontsize=8.5, fontweight="bold")
    ax.set_title("Self-attention: Q, K, V from the same input",
                 color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "10_attention.png")


# --- 11. RAG pipeline ---
def rag_pipeline():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.5); ax.axis("off")
    stages = [("Query", 0.4, LIGHT),
              ("Embed\nquery", 2.0, ACCENT),
              ("Vector\nsearch", 3.7, NAVY),
              ("Retrieve\ntop-k docs", 5.5, ACCENT),
              ("Construct\nprompt", 7.4, "#6B7AE0"),
              ("LLM\ngenerate", 9.2, NAVY),
              ("Answer", 10.9, "#3D4A8C")]
    for name, x, c in stages:
        ax.add_patch(FancyBboxPatch((x, 1.5), 1.4, 1.8,
                                    boxstyle="round,pad=0.05", facecolor=c, edgecolor=NAVY))
        ax.text(x + 0.7, 2.4, name, ha="center", va="center",
                color="white" if c != LIGHT else NAVY,
                fontsize=10, fontweight="bold")
    for i in range(len(stages) - 1):
        x0 = stages[i][1] + 1.4; x1 = stages[i + 1][1]
        ax.annotate("", xy=(x1, 2.4), xytext=(x0, 2.4),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.6))
    ax.add_patch(Rectangle((3.6, 0.2), 2.0, 0.8, facecolor=LIGHT,
                           edgecolor=NAVY, linewidth=1))
    ax.text(4.6, 0.6, "Vector Database", ha="center", va="center",
            color=NAVY, fontsize=9, fontweight="bold")
    ax.set_title("Retrieval-Augmented Generation pipeline",
                 color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "11_rag.png")


# --- 12. Fine-tuning vs RAG vs Prompt ---
def adaptation_ladder():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.axis("off")
    rungs = [("Prompt engineering", 1.0, "#A8B0D9"),
             ("Few-shot / RAG", 2.2, ACCENT),
             ("LoRA / qLoRA (PEFT)", 3.4, "#3D4A8C"),
             ("Full fine-tuning", 4.5, NAVY)]
    for name, y, c in rungs:
        ax.add_patch(FancyBboxPatch((1.5, y), 6, 0.8,
                                    boxstyle="round,pad=0.05",
                                    facecolor=c, edgecolor=NAVY))
        ax.text(4.5, y + 0.4, name, ha="center", va="center",
                color="white", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(0.7, 5.1), xytext=(0.7, 1.1),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=2.2))
    ax.text(0.4, 5.4, "More cost\nMore control", color=NAVY, fontsize=9, fontweight="bold")
    ax.text(0.4, 0.4, "Less cost\nLess control", color=NAVY, fontsize=9, fontweight="bold")
    ax.set_title("Adaptation ladder for LLMs", color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "12_adaptation_ladder.png")


# --- 13. LoRA mechanics ---
def lora_diagram():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.set_xlim(0, 10); ax.set_ylim(0, 5); ax.axis("off")
    ax.add_patch(Rectangle((0.6, 1.5), 2.0, 2.0,
                           facecolor=LIGHT, edgecolor=NAVY, linewidth=1.5))
    ax.text(1.6, 2.5, "W\nd×d\n(frozen)", ha="center", va="center",
            color=NAVY, fontsize=11, fontweight="bold")
    ax.text(3.3, 2.5, "+", ha="center", va="center", fontsize=20, color=NAVY)
    ax.add_patch(Rectangle((3.9, 2.5), 1.6, 1.0,
                           facecolor=ACCENT, edgecolor=NAVY))
    ax.text(4.7, 3.0, "B\nd×r", ha="center", va="center", color="white", fontweight="bold")
    ax.add_patch(Rectangle((3.9, 1.5), 1.6, 1.0,
                           facecolor=ACCENT, edgecolor=NAVY))
    ax.text(4.7, 2.0, "A\nr×d", ha="center", va="center", color="white", fontweight="bold")
    ax.text(6.0, 2.5, "=", ha="center", va="center", fontsize=20, color=NAVY)
    ax.add_patch(Rectangle((6.5, 1.5), 2.0, 2.0,
                           facecolor="#3D4A8C", edgecolor=NAVY))
    ax.text(7.5, 2.5, "W + α/r · BA\n(adapted)", ha="center", va="center",
            color="white", fontsize=11, fontweight="bold")
    ax.text(5.0, 0.7, "rank r ≪ d  →  only B and A are trainable",
            ha="center", color=NAVY, fontsize=10, fontstyle="italic")
    ax.set_title("LoRA: low-rank adapter on a frozen weight",
                 color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "13_lora.png")


# --- 14. Vector DB ANN search ---
def ann_search():
    fig, ax = plt.subplots(figsize=(8, 5))
    rng = np.random.default_rng(3)
    pts = rng.uniform(-3, 3, (120, 2))
    query = np.array([0.5, 0.8])
    dists = np.linalg.norm(pts - query, axis=1)
    top = np.argsort(dists)[:8]
    ax.scatter(pts[:, 0], pts[:, 1], s=24, color=GRAY, alpha=0.6)
    ax.scatter(pts[top, 0], pts[top, 1], s=80, color=ACCENT, edgecolor=NAVY,
               linewidth=1.5, label="Top-k similar")
    ax.scatter(*query, s=200, marker="*", color="#D43F3F", edgecolor=NAVY,
               linewidth=1.5, label="Query")
    for i in top:
        ax.plot([query[0], pts[i, 0]], [query[1], pts[i, 1]],
                color=ACCENT, alpha=0.3, linewidth=1)
    ax.set_title("Approximate nearest neighbor search in embedding space",
                 color=NAVY, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.25); ax.set_aspect("equal")
    save(fig, "14_ann_search.png")


# --- 15. Embeddings space ---
def embedding_space():
    fig, ax = plt.subplots(figsize=(8, 5))
    np.random.seed(5)
    centers = [(2.0, 2.0, "Animals"), (-2.0, 2.0, "Vehicles"),
               (0.0, -2.0, "Foods")]
    colors = [ACCENT, NAVY, "#D43F3F"]
    for (cx, cy, lab), c in zip(centers, colors):
        pts = np.random.randn(30, 2) * 0.5 + np.array([cx, cy])
        ax.scatter(pts[:, 0], pts[:, 1], s=40, color=c, alpha=0.7, label=lab,
                   edgecolor=NAVY, linewidth=0.5)
    ax.set_title("Word embeddings cluster by meaning (2D projection)",
                 color=NAVY, fontweight="bold")
    ax.legend(); ax.grid(alpha=0.25); ax.set_aspect("equal")
    save(fig, "15_embeddings.png")


# --- 16. RLHF pipeline ---
def rlhf_pipeline():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4); ax.axis("off")
    stages = [("Pretrained\nLLM", 0.4, LIGHT),
              ("Supervised\nFine-Tuning (SFT)", 2.4, ACCENT),
              ("Reward Model\n(from human prefs)", 4.8, "#6B7AE0"),
              ("PPO / DPO / GRPO\noptimization", 7.4, NAVY),
              ("Aligned\nLLM", 10.0, "#3D4A8C")]
    for name, x, c in stages:
        ax.add_patch(FancyBboxPatch((x, 1.3), 1.8, 1.5,
                                    boxstyle="round,pad=0.05",
                                    facecolor=c, edgecolor=NAVY))
        ax.text(x + 0.9, 2.05, name, ha="center", va="center",
                color="white" if c != LIGHT else NAVY,
                fontsize=10, fontweight="bold")
    for i in range(len(stages) - 1):
        x0 = stages[i][1] + 1.8; x1 = stages[i + 1][1]
        ax.annotate("", xy=(x1, 2.05), xytext=(x0, 2.05),
                    arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.6))
    ax.set_title("RLHF: from pretrained base to aligned LLM",
                 color=NAVY, fontsize=13, fontweight="bold")
    save(fig, "16_rlhf.png")


# --- 17. Loss curves: under/overfit ---
def overfitting_curves():
    fig, ax = plt.subplots(figsize=(8, 4.5))
    epochs = np.arange(1, 51)
    train = 1.0 * np.exp(-epochs / 12) + 0.05
    val = 0.9 * np.exp(-epochs / 10) + 0.15 + 0.012 * np.maximum(epochs - 25, 0)
    ax.plot(epochs, train, color=ACCENT, linewidth=2.4, label="Train loss")
    ax.plot(epochs, val, color="#D43F3F", linewidth=2.4, label="Validation loss")
    ax.axvline(25, color=GRAY, linestyle="--")
    ax.text(25.5, 0.7, "early stopping point", color=NAVY, fontsize=10)
    ax.set_title("Overfitting: validation loss rises while train falls",
                 color=NAVY, fontweight="bold")
    ax.set_xlabel("Epoch"); ax.set_ylabel("Loss")
    ax.legend(); ax.grid(alpha=0.25)
    save(fig, "17_overfitting.png")


# --- 18. Dropout ---
def dropout_diagram():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))
    for ax, title, drop in zip(axes, ["Full network", "With dropout (p=0.5)"],
                               [False, True]):
        ax.set_xlim(0, 5); ax.set_ylim(0, 5); ax.axis("off")
        ax.set_title(title, color=NAVY, fontweight="bold", fontsize=12)
        layers = [(1, [1.0, 2.0, 3.0, 4.0]),
                  (2.5, [0.7, 1.6, 2.5, 3.4, 4.3]),
                  (4, [1.5, 2.5, 3.5])]
        rng = np.random.default_rng(2)
        kept_mask = {l: rng.random(len(ys)) > 0.5 for l, ys in layers[:-1]}
        for x, ys in layers:
            for i, y in enumerate(ys):
                visible = True
                if drop and x != 4:
                    visible = kept_mask[x][i]
                color = ACCENT if visible else "white"
                edge = NAVY if visible else GRAY
                ax.add_patch(Circle((x, y), 0.22, facecolor=color,
                                    edgecolor=edge, linewidth=1.2, zorder=3))
        for (xa, ya_list), (xb, yb_list) in zip(layers[:-1], layers[1:]):
            for i, ya in enumerate(ya_list):
                for j, yb in enumerate(yb_list):
                    show = True
                    if drop:
                        if xa != 4 and not kept_mask[xa][i]:
                            show = False
                    if show:
                        ax.plot([xa, xb], [ya, yb], color=GRAY,
                                alpha=0.5, linewidth=0.5, zorder=1)
    save(fig, "18_dropout.png")


# --- 19. Chain of generation: SFT -> RLHF (already covered); add Tokenization ---
def tokenization_diagram():
    fig, ax = plt.subplots(figsize=(11, 3.5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 3); ax.axis("off")
    text = "The quick brown fox."
    tokens = ["The", " quick", " brown", " fox", "."]
    ids = [464, 2068, 7586, 21831, 13]
    ax.text(0.2, 2.5, text, color=NAVY, fontsize=14, fontweight="bold")
    ax.annotate("", xy=(5.5, 2.4), xytext=(3.0, 2.4),
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.6))
    ax.text(4.2, 2.65, "tokenize", color=NAVY, fontsize=10, fontweight="bold")
    for i, (tok, tid) in enumerate(zip(tokens, ids)):
        x = 0.5 + i * 1.5
        ax.add_patch(FancyBboxPatch((x, 0.6), 1.3, 0.9,
                                    boxstyle="round,pad=0.05",
                                    facecolor=ACCENT, edgecolor=NAVY))
        ax.text(x + 0.65, 1.25, repr(tok), ha="center", va="center",
                color="white", fontsize=9)
        ax.text(x + 0.65, 0.85, str(tid), ha="center", va="center",
                color="white", fontsize=10, fontweight="bold")
    ax.set_title("Tokenization: text → subword tokens → integer IDs",
                 color=NAVY, fontweight="bold")
    save(fig, "19_tokenization.png")


# --- 20. Encoder-decoder for translation ---
def encoder_decoder():
    fig, ax = plt.subplots(figsize=(11, 4))
    ax.set_xlim(0, 12); ax.set_ylim(0, 4.5); ax.axis("off")
    ax.add_patch(FancyBboxPatch((0.5, 1.2), 4.5, 2.0,
                                boxstyle="round,pad=0.05",
                                facecolor=ACCENT, edgecolor=NAVY))
    ax.text(2.75, 2.2, "ENCODER\n(reads input sequence)", ha="center",
            va="center", color="white", fontsize=12, fontweight="bold")
    ax.add_patch(FancyBboxPatch((7.0, 1.2), 4.5, 2.0,
                                boxstyle="round,pad=0.05",
                                facecolor=NAVY, edgecolor=NAVY))
    ax.text(9.25, 2.2, "DECODER\n(generates output sequence)", ha="center",
            va="center", color="white", fontsize=12, fontweight="bold")
    ax.annotate("", xy=(7.0, 2.2), xytext=(5.0, 2.2),
                arrowprops=dict(arrowstyle="->", color="#D43F3F", lw=2.4))
    ax.text(6.0, 2.5, "Context\n(K, V)", ha="center",
            color="#D43F3F", fontsize=10, fontweight="bold")
    ax.text(2.75, 0.6, "Input: 'Bonjour le monde'", ha="center", color=NAVY, fontsize=10)
    ax.text(9.25, 0.6, "Output: 'Hello world'", ha="center", color=NAVY, fontsize=10)
    ax.set_title("Encoder–decoder transformer (translation example)",
                 color=NAVY, fontweight="bold")
    save(fig, "20_encoder_decoder.png")


if __name__ == "__main__":
    ann_architecture()
    neuron_with_activation()
    activation_functions()
    backprop_diagram()
    vanishing_gradient()
    gradient_descent()
    cnn_structure()
    rnn_unrolled()
    transformer_arch()
    attention_qkv()
    rag_pipeline()
    adaptation_ladder()
    lora_diagram()
    ann_search()
    embedding_space()
    rlhf_pipeline()
    overfitting_curves()
    dropout_diagram()
    tokenization_diagram()
    encoder_decoder()
    print("All diagrams generated.")
