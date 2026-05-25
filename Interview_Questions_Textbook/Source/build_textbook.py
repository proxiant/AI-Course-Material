"""Master builder for the interview questions textbook.
Produces TXT, DOCX, and PDF (via LibreOffice headless)."""

import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helpers import (
    new_doc, add_title, add_subtitle, add_h1, add_h2, add_h3,
    add_body, add_bullet, add_image, add_divider, add_page_break,
    cover_page, copyright_page, about_author,
)
from content_part1 import ANN, CLASSICAL_NLP
from content_part2 import TRANSFORMERS
from content_part3 import LLM_FUNDAMENTALS, EMBEDDINGS
from content_part4 import RAG
from content_part5 import FINE_TUNING, VECTOR_DB
from content_part6 import LLMOPS, EVALUATION, MISC
from content_part7 import SUPPLEMENT

OUT = "/Users/pkr465/work/AI-Course-Material/Interview_Questions_Textbook/Output"
DIAGRAMS = "/Users/pkr465/work/AI-Course-Material/Interview_Questions_Textbook/Diagrams"
os.makedirs(OUT, exist_ok=True)

TITLE = "AI, ML, and Generative AI Interview Questions"
SUBTITLE = "A Comprehensive Reference for Engineers, Researchers, and Architects"
AUTHOR = "Pavan R"
PUBLISHER = "Proxiant Academy"
EDITION = "First Edition, Revision 1.1"
YEAR = "2026"
RID = "PA-AIMLIQ-2026-01"
AUTHOR_BIO = (
    "Pavan R is the lead instructor at Proxiant Academy. He designs and "
    "delivers the academy's curriculum across AI fundamentals, agents, "
    "fine-tuning, and retrieval-augmented generation. His work focuses on "
    "translating frontier AI techniques into reliable engineering practice "
    "for teams shipping production systems."
)

CHAPTERS = [
    ("Chapter 1", "Artificial Neural Networks", ANN),
    ("Chapter 2", "Classical Natural Language Processing", CLASSICAL_NLP),
    ("Chapter 3", "Transformers and Extended Architectures", TRANSFORMERS),
    ("Chapter 4", "Fundamentals of Large Language Models", LLM_FUNDAMENTALS),
    ("Chapter 5", "Word and Sentence Embeddings", EMBEDDINGS),
    ("Chapter 6", "Retrieval-Augmented Generation (RAG) and Multimodal RAG", RAG),
    ("Chapter 7", "Fine-Tuning Large Language Models", FINE_TUNING),
    ("Chapter 8", "Vector Databases", VECTOR_DB),
    ("Chapter 9", "LLMOps and System Design", LLMOPS),
    ("Chapter 10", "Evaluation Methods", EVALUATION),
    ("Chapter 11", "Miscellaneous and Advanced Topics", MISC),
    ("Chapter 12", "Supplementary Topics, Formulas, and Deep Dives", SUPPLEMENT),
]


# ---------- DOCX ----------

def build_docx():
    doc = new_doc(book_title=TITLE)

    # Cover page
    cover_page(doc, TITLE, SUBTITLE, AUTHOR, PUBLISHER, EDITION, YEAR, isbn=RID)
    add_page_break(doc)

    # Copyright page
    copyright_page(doc, TITLE, AUTHOR, PUBLISHER, EDITION, YEAR, isbn=RID)
    add_page_break(doc)

    # Preface
    add_h1(doc, "Preface")
    add_body(doc,
        "This textbook is a curated, deep reference for technical interview "
        "preparation across the modern AI stack: neural networks, classical NLP, "
        "transformers, large language models, embeddings, retrieval-augmented "
        "generation, fine-tuning, vector databases, LLMOps, and evaluation. The "
        "answers are written to interview depth: enough detail to demonstrate "
        "real understanding, with diagrams and code snippets where helpful.")
    add_body(doc,
        "Each chapter follows a question-and-answer format. Use it as a study "
        "companion, a quick reference during interview prep, or a daily reading "
        "for the working engineer.")
    add_body(doc,
        "How to read this book: pick a chapter, work through the questions, "
        "attempt your own answer first, then read the provided answer. Pay "
        "particular attention to the tradeoffs and design choices, which are "
        "the focus of senior-level interviews.")
    add_page_break(doc)

    # TOC
    add_h1(doc, "Table of Contents")
    for label, title, qs in CHAPTERS:
        add_body(doc, f"{label}: {title} ({len(qs)} questions)")
    add_page_break(doc)

    # Chapters
    for label, title, qs in CHAPTERS:
        add_title(doc, f"{label}", size=14)
        add_title(doc, title, size=22)
        add_divider(doc)
        add_body(doc, f"This chapter covers {len(qs)} questions on {title.lower()}.")
        add_body(doc, "")

        for i, entry in enumerate(qs, 1):
            if len(entry) == 2:
                question, answer = entry
                diagrams = []
            else:
                question, answer, diagrams = entry

            add_h2(doc, f"Q{i}. {question}")
            for para in answer:
                add_body(doc, para)
            for d in diagrams:
                path = os.path.join(DIAGRAMS, d)
                if os.path.exists(path):
                    add_image(doc, path, width_inches=5.5)
            add_body(doc, "")

        add_page_break(doc)

    # Appendix
    add_h1(doc, "Appendix A: Recommended Reading")
    papers = [
        "Attention Is All You Need (Vaswani et al., 2017).",
        "BERT: Pre-training of Deep Bidirectional Transformers (Devlin et al., 2018).",
        "Language Models are Few-Shot Learners (Brown et al., 2020). GPT-3.",
        "LoRA: Low-Rank Adaptation of Large Language Models (Hu et al., 2021).",
        "QLoRA: Efficient Finetuning of Quantized LLMs (Dettmers et al., 2023).",
        "Direct Preference Optimization (Rafailov et al., 2023).",
        "Training Compute-Optimal Large Language Models (Hoffmann et al., 2022). Chinchilla.",
        "Retrieval-Augmented Generation for Knowledge-Intensive NLP (Lewis et al., 2020).",
        "DSPy: Compiling Declarative LM Calls into Self-Improving Pipelines (Khattab et al., 2023).",
        "RAGAS: Automated Evaluation of Retrieval Augmented Generation (Es et al., 2023).",
        "ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction (Khattab and Zaharia, 2020).",
        "From Local to Global: A GraphRAG Approach (Edge et al., 2024).",
        "LLaMA: Open and Efficient Foundation Language Models (Touvron et al., 2023).",
        "DeepSeekMath: Pushing the Limits of Mathematical Reasoning (Shao et al., 2024). GRPO.",
        "Mixture of Experts Meets Instruction Tuning (Shen et al., 2024).",
    ]
    for p in papers:
        add_bullet(doc, p)

    add_h1(doc, "Appendix B: Suggested Interview Preparation Path")
    add_h3(doc, "For ML/AI Engineer roles (3-5 years experience)")
    add_bullet(doc, "Week 1: Chapters 1, 2, 3 (foundations).")
    add_bullet(doc, "Week 2: Chapters 4, 5 (LLMs and embeddings).")
    add_bullet(doc, "Week 3: Chapters 6, 7, 8 (RAG, fine-tuning, vector DB).")
    add_bullet(doc, "Week 4: Chapters 9, 10, 11 (LLMOps, evaluation, ethics).")
    add_body(doc, "Build a small project end-to-end (RAG over a personal document collection, or a fine-tuned classifier) to ground the concepts.")

    add_h3(doc, "For Senior/Staff/Principal AI roles")
    add_bullet(doc, "Focus on tradeoff discussions: when does each technique fail?")
    add_bullet(doc, "System design: production architectures for chat, search, RAG, agents.")
    add_bullet(doc, "Leadership: how do you choose models, evaluate vendors, manage costs?")
    add_bullet(doc, "Ethics and risk: bias, hallucination, safety, governance.")

    add_h1(doc, "Appendix C: Glossary of Key Terms")
    glossary = [
        ("ANN", "Artificial Neural Network or Approximate Nearest Neighbor depending on context."),
        ("Attention", "Mechanism that weights inputs by relevance to a query."),
        ("Backpropagation", "Algorithm for computing gradients in neural networks."),
        ("BPE", "Byte Pair Encoding, a subword tokenization algorithm."),
        ("Chinchilla scaling", "Compute-optimal: 20 tokens per parameter."),
        ("CoT", "Chain-of-Thought prompting / reasoning."),
        ("CLIP", "Contrastive Language-Image Pretraining."),
        ("DPO", "Direct Preference Optimization."),
        ("Embedding", "Dense vector representation of an object."),
        ("FAISS", "Facebook AI Similarity Search library."),
        ("GRPO", "Group Relative Policy Optimization."),
        ("HNSW", "Hierarchical Navigable Small World graph for ANN search."),
        ("KL", "Kullback-Leibler divergence."),
        ("LLM", "Large Language Model."),
        ("LoRA", "Low-Rank Adaptation, a PEFT method."),
        ("MoE", "Mixture of Experts."),
        ("PEFT", "Parameter-Efficient Fine-Tuning."),
        ("PPO", "Proximal Policy Optimization."),
        ("qLoRA", "Quantized LoRA: 4-bit base with 16-bit adapters."),
        ("RAG", "Retrieval-Augmented Generation."),
        ("RLHF", "Reinforcement Learning from Human Feedback."),
        ("RLVR", "Reinforcement Learning with Verifiable Rewards."),
        ("RoPE", "Rotary Position Embeddings."),
        ("SFT", "Supervised Fine-Tuning."),
        ("ViT", "Vision Transformer."),
    ]
    for term, defn in glossary:
        add_body(doc, f"{term}: {defn}")

    # About the Author
    add_page_break(doc)
    about_author(doc, AUTHOR, AUTHOR_BIO)

    # Colophon
    add_page_break(doc)
    for _ in range(8):
        doc.add_paragraph()
    add_title(doc, "Colophon", size=18, center=True)
    add_body(doc, "")
    add_subtitle(doc, TITLE, size=11, center=True)
    add_subtitle(doc, f"{EDITION}, {YEAR}", size=10, center=True)
    add_subtitle(doc,
        "Set in Calibri 11pt body, navy chapter titles.",
        size=9, center=True)
    add_subtitle(doc,
        "Diagrams produced with matplotlib. Layout assembled with python-docx.",
        size=9, center=True)
    add_subtitle(doc,
        "PDF generated via LibreOffice headless conversion.",
        size=9, center=True)
    add_body(doc, "")
    add_subtitle(doc,
        f"Published by {PUBLISHER}. Reference identifier: {RID}.",
        size=9, center=True)
    add_subtitle(doc,
        f"© {YEAR} {PUBLISHER}. All rights reserved.",
        size=9, center=True)

    out_docx = os.path.join(OUT, "AI_ML_GenAI_Interview_Questions_Textbook.docx")
    doc.save(out_docx)
    print(f"WROTE {out_docx}")
    return out_docx


# ---------- TXT ----------

def build_txt():
    out_txt = os.path.join(OUT, "AI_ML_GenAI_Interview_Questions_Textbook.txt")
    lines = []
    lines.append("=" * 80)
    lines.append(TITLE.center(80))
    lines.append(SUBTITLE.center(80))
    lines.append("")
    lines.append(AUTHOR.center(80))
    lines.append("Edition 1 | 2026".center(80))
    lines.append("=" * 80)
    lines.append("")

    lines.append("PREFACE")
    lines.append("-" * 80)
    lines.append("This textbook is a curated, deep reference for technical interview")
    lines.append("preparation across the modern AI stack. Each chapter follows a")
    lines.append("question-and-answer format. Diagrams referenced in the DOCX/PDF")
    lines.append("versions are stored separately as PNG files under Diagrams/.")
    lines.append("")

    lines.append("TABLE OF CONTENTS")
    lines.append("-" * 80)
    for label, title, qs in CHAPTERS:
        lines.append(f"  {label}: {title} ({len(qs)} questions)")
    lines.append("")

    for label, title, qs in CHAPTERS:
        lines.append("")
        lines.append("=" * 80)
        lines.append(f"{label}: {title}".upper())
        lines.append("=" * 80)
        lines.append("")
        for i, entry in enumerate(qs, 1):
            if len(entry) == 2:
                question, answer = entry
                diagrams = []
            else:
                question, answer, diagrams = entry
            lines.append("-" * 80)
            lines.append(f"Q{i}. {question}")
            lines.append("-" * 80)
            for para in answer:
                lines.append(_wrap(para, 78))
                lines.append("")
            if diagrams:
                lines.append(f"  [Diagrams: {', '.join(diagrams)}]")
                lines.append("")

    lines.append("")
    lines.append("=" * 80)
    lines.append("END OF TEXTBOOK".center(80))
    lines.append("=" * 80)

    with open(out_txt, "w") as f:
        f.write("\n".join(lines))
    print(f"WROTE {out_txt}")
    return out_txt


def _wrap(text, width):
    """Simple paragraph word-wrap."""
    words = text.split()
    out = []
    cur = []
    cur_len = 0
    for w in words:
        if cur_len + len(w) + (1 if cur else 0) > width:
            out.append(" ".join(cur))
            cur = [w]
            cur_len = len(w)
        else:
            cur.append(w)
            cur_len += len(w) + (1 if cur_len > 0 else 0)
    if cur:
        out.append(" ".join(cur))
    return "\n".join(out)


# ---------- PDF ----------

def build_pdf(docx_path):
    soffice = "/opt/homebrew/bin/soffice"
    out_pdf = os.path.join(OUT, "AI_ML_GenAI_Interview_Questions_Textbook.pdf")
    cmd = [soffice, "--headless", "--convert-to", "pdf",
           "--outdir", OUT, docx_path]
    print(f"Running LibreOffice headless: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    if result.returncode != 0:
        print("STDERR:", result.stderr)
        raise RuntimeError(f"PDF conversion failed: {result.returncode}")
    print(f"WROTE {out_pdf}")
    return out_pdf


if __name__ == "__main__":
    docx_path = build_docx()
    build_txt()
    build_pdf(docx_path)
    print("\nAll three formats generated.")
