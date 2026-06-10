"""Master builder for the AI/ML/GenAI textbook. Produces DOCX, PDF, TXT."""

import os
import sys
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from helpers import (
    new_doc, add_title, add_subtitle, chapter_heading, section_heading,
    subsection_heading, subsubsection_heading, body, callout, bullet,
    numbered, code, equation, image, add_divider, page_break,
    cover_page, copyright_page, about_author,
)

# Import all chapters
from chapter_01_introduction import CHAPTER as CH01
from chapter_02_math import CHAPTER as CH02
from chapter_03_neural_networks import CHAPTER as CH03
from chapter_04_nlp_basics import CHAPTER as CH04
from chapter_05_transformers import CHAPTER as CH05
from chapter_06_embeddings import CHAPTER as CH06
from chapter_07_pretrained_lms import CHAPTER as CH07
from chapter_08_vision_multimodal import CHAPTER as CH08
from chapter_09_prompts import CHAPTER as CH09
from chapter_10_finetuning import CHAPTER as CH10
from chapter_11_alignment import CHAPTER as CH11
from chapter_12_vector_db import CHAPTER as CH12
from chapter_13_rag import CHAPTER as CH13
from chapter_14_llmops import CHAPTER as CH14
from chapter_15_evaluation import CHAPTER as CH15
from chapter_16_ethics_frontier import CHAPTER as CH16

CHAPTERS = [CH01, CH02, CH03, CH04, CH05, CH06, CH07, CH08,
            CH09, CH10, CH11, CH12, CH13, CH14, CH15, CH16]

_HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(_HERE, "..", "Output")
DIAGRAMS = os.path.join(_HERE, "..", "Diagrams")
os.makedirs(OUT, exist_ok=True)

TITLE = "Artificial Intelligence, Machine Learning, and Generative AI"
SUBTITLE = "A Comprehensive Textbook for Engineers, Researchers, and Architects"
AUTHOR = "Pavan R"
PUBLISHER = "Proxiant Academy"
EDITION = "First Edition"
YEAR = "2026"
RID = "PA-AIMLGEN-2026-01"
AUTHOR_BIO = (
    "Pavan R is the lead instructor at Proxiant Academy, where he designs and "
    "delivers the full curriculum across AI fundamentals, agents, fine-tuning, "
    "and retrieval-augmented generation. He works at the intersection of "
    "applied research and production engineering, with a focus on making "
    "frontier AI techniques practical for working teams. His work spans "
    "enterprise RAG systems, multi-agent architectures, alignment "
    "engineering, and the operational practices that turn impressive demos "
    "into reliable products."
)

PARTS = [
    ("Part I", "Foundations", [1, 2, 3]),
    ("Part II", "Natural Language Processing and Transformers", [4, 5]),
    ("Part III", "Embeddings and Pretrained Models", [6, 7]),
    ("Part IV", "Vision and Multimodal AI", [8]),
    ("Part V", "Prompts, Fine-Tuning, and Alignment", [9, 10, 11]),
    ("Part VI", "Retrieval, Vectors, and RAG", [12, 13]),
    ("Part VII", "Production: LLMOps, Evaluation, Ethics", [14, 15, 16]),
]


def render_section(doc, sec, chapter_num):
    """Render a single section, recursively handling subsections."""
    section_heading(doc, sec["number"], sec["title"])

    # Top-level image right after section heading
    if "image" in sec:
        img_path = os.path.join(DIAGRAMS, sec["image"])
        if os.path.exists(img_path):
            image(doc, img_path,
                  caption=sec.get("caption", f"Figure for {sec['title']}"))

    # Main paragraphs
    for para in sec.get("paragraphs", []):
        body(doc, para)

    # Callouts at section level
    for label, text in sec.get("callouts", []):
        callout(doc, label, text)

    # Equation at section level
    if "equation" in sec:
        equation(doc, sec["equation"], sec.get("equation_label"))

    # Bullets at section level
    for b in sec.get("bullets", []):
        bullet(doc, b)

    # Subsections
    for subsec in sec.get("subsections", []):
        subsection_heading(doc, "", subsec["title"])

        if "image" in subsec:
            img_path = os.path.join(DIAGRAMS, subsec["image"])
            if os.path.exists(img_path):
                image(doc, img_path,
                      caption=subsec.get("caption", ""))

        for para in subsec.get("paragraphs", []):
            body(doc, para)

        if "equation" in subsec:
            equation(doc, subsec["equation"], subsec.get("equation_label"))

        for para in subsec.get("more_paragraphs", []):
            body(doc, para)

        for b in subsec.get("bullets", []):
            bullet(doc, b)


def render_chapter(doc, chapter):
    page_break(doc)
    chapter_heading(doc, chapter["label"], chapter["title"])

    # Intro image at top of chapter
    if "intro_image" in chapter:
        img_path = os.path.join(DIAGRAMS, chapter["intro_image"])
        if os.path.exists(img_path):
            image(doc, img_path,
                  caption=chapter.get("intro_caption", ""))

    # Sections
    for sec in chapter["sections"]:
        render_section(doc, sec, chapter["label"])

    # Further reading
    if chapter.get("further_reading"):
        section_heading(doc, "", "Further Reading")
        for ref in chapter["further_reading"]:
            bullet(doc, ref)


def build_docx():
    doc = new_doc(book_title=TITLE)

    # Cover page
    cover_page(doc, TITLE, SUBTITLE, AUTHOR, PUBLISHER, EDITION, YEAR, isbn=RID)
    page_break(doc)

    # Copyright page
    copyright_page(doc, TITLE, AUTHOR, PUBLISHER, EDITION, YEAR, isbn=RID)
    page_break(doc)

    # Preface
    chapter_heading(doc, "Preface", "About This Book")
    body(doc,
        "This textbook is a comprehensive guide to modern artificial "
        "intelligence: from the mathematical foundations of neural networks "
        "through the transformer-based foundation models that define the "
        "generative AI era, the engineering practice that puts them into "
        "production, and the ethical considerations that should shape that "
        "practice.")
    body(doc,
        "The book is structured into seven parts and sixteen chapters. Each "
        "chapter develops a topic from first principles, illustrates with "
        "diagrams and worked examples, grounds the discussion in production "
        "engineering practice, and points to further reading for those who "
        "want to go deeper.")
    body(doc,
        "The audience is engineers, researchers, and technical leaders who "
        "want a working command of modern AI. Prerequisites are honest: you "
        "should know calculus, linear algebra, and probability at an "
        "undergraduate level, plus have working Python skills. Chapter 2 "
        "provides a brisk math refresher.")
    body(doc,
        "Three principles guide the writing. First, theoretical "
        "understanding combined with production engineering produces the "
        "most useful work. Second, principles outlast specific tools; the "
        "book emphasizes durable principles and uses specific frameworks as "
        "illustrations. Third, AI engineering carries real ethical weight; "
        "Chapter 16 treats this seriously rather than as an afterthought.")
    body(doc,
        "The field moves fast. Specific model names, framework versions, and "
        "benchmark numbers will date. The structure of the material, the "
        "diagrams, the mathematical relationships, and the engineering "
        "patterns will not.")

    page_break(doc)

    # Table of contents
    chapter_heading(doc, "Contents", "Table of Contents")
    for part_label, part_title, chapter_nums in PARTS:
        subsection_heading(doc, part_label, part_title)
        for n in chapter_nums:
            ch = CHAPTERS[n - 1]
            body(doc, f"  Chapter {n}: {ch['title']}")
        body(doc, "")

    # Render each part with its chapters
    for part_label, part_title, chapter_nums in PARTS:
        page_break(doc)
        add_title(doc, part_label, size=20, center=True)
        add_title(doc, part_title, size=28, center=True)
        add_divider(doc)
        body(doc, "")
        body(doc,
            f"This part contains chapter(s) {', '.join(str(n) for n in chapter_nums)} "
            f"covering {part_title.lower()}.")

        for n in chapter_nums:
            render_chapter(doc, CHAPTERS[n - 1])

    # Appendices
    page_break(doc)
    chapter_heading(doc, "Appendix A", "Mathematical Notation")
    body(doc,
        "Symbols and conventions used throughout the book.")
    notations = [
        ("ℝⁿ", "n-dimensional real-valued vector space"),
        ("ℝᵐˣⁿ", "m-by-n matrix of real values"),
        ("x ∈ ℝⁿ", "x is a vector with n components"),
        ("xᵢ", "i-th component of vector x"),
        ("||x||", "norm of vector x (Euclidean unless otherwise specified)"),
        ("Aᵀ", "transpose of matrix A"),
        ("A⁻¹", "inverse of matrix A"),
        ("∇f(x)", "gradient of f at x"),
        ("∂f/∂x", "partial derivative of f with respect to x"),
        ("E[X]", "expected value of random variable X"),
        ("P(X = x)", "probability mass function (discrete)"),
        ("p(x)", "probability density function (continuous)"),
        ("σ(x)", "sigmoid function: 1 / (1 + exp(-x))"),
        ("softmax(z)", "exp(z) normalized to sum to 1"),
        ("D_KL(P || Q)", "Kullback-Leibler divergence from P to Q"),
        ("Q, K, V", "query, key, value matrices in attention"),
        ("d_k, d_model", "key dimension, model dimension"),
        ("θ", "model parameters (generic)"),
        ("η", "learning rate"),
        ("β (alignment)", "KL coefficient in PPO; temperature in DPO"),
    ]
    for sym, desc in notations:
        body(doc, f"{sym}     {desc}")

    page_break(doc)
    chapter_heading(doc, "Appendix B", "Glossary")
    glossary = [
        ("ANN", "Artificial Neural Network or Approximate Nearest Neighbor (context-dependent)"),
        ("Attention", "Mechanism weighting inputs by relevance to a query"),
        ("Backpropagation", "Algorithm for computing gradients in neural networks via the chain rule"),
        ("BERT", "Bidirectional Encoder Representations from Transformers (Devlin et al., 2018)"),
        ("BPE", "Byte Pair Encoding, a subword tokenization algorithm"),
        ("CLIP", "Contrastive Language-Image Pretraining (Radford et al., 2021)"),
        ("Chinchilla scaling", "Compute-optimal training: ~20 tokens per parameter"),
        ("CoT", "Chain-of-Thought prompting / reasoning"),
        ("Cross-entropy", "Standard classification loss; -log P(true class)"),
        ("DPO", "Direct Preference Optimization (Rafailov et al., 2023)"),
        ("Embedding", "Dense vector representation of a discrete object"),
        ("FAISS", "Facebook AI Similarity Search library"),
        ("Fine-tuning", "Continuing training of a pretrained model on task-specific data"),
        ("GAN", "Generative Adversarial Network"),
        ("GPT", "Generative Pretrained Transformer"),
        ("GRPO", "Group Relative Policy Optimization (Shao et al., 2024)"),
        ("HNSW", "Hierarchical Navigable Small World graph for ANN search"),
        ("IVF", "Inverted File index for ANN search"),
        ("KL divergence", "Kullback-Leibler divergence: D_KL(P||Q)"),
        ("LLM", "Large Language Model"),
        ("LoRA", "Low-Rank Adaptation; a parameter-efficient fine-tuning method"),
        ("MCP", "Model Context Protocol; standard for tool exposure to LLMs"),
        ("MoE", "Mixture of Experts"),
        ("Multi-Head Attention", "Parallel attention computations with different projections"),
        ("PEFT", "Parameter-Efficient Fine-Tuning"),
        ("Perplexity", "exp(per-token cross-entropy); a language model evaluation metric"),
        ("PPO", "Proximal Policy Optimization (Schulman et al., 2017)"),
        ("Product Quantization (PQ)", "Vector compression: split into subvectors, quantize each"),
        ("qLoRA", "Quantized LoRA: 4-bit base model with 16-bit adapters"),
        ("RAG", "Retrieval-Augmented Generation"),
        ("Ragas", "RAG evaluation framework with faithfulness/relevance metrics"),
        ("Reranking", "Re-scoring retrieval candidates with a stronger model"),
        ("ResNet", "Residual Network: deep network with skip connections (He et al., 2015)"),
        ("RLHF", "Reinforcement Learning from Human Feedback"),
        ("RLVR", "Reinforcement Learning with Verifiable Rewards"),
        ("RoPE", "Rotary Position Embeddings"),
        ("SFT", "Supervised Fine-Tuning"),
        ("Softmax", "exp(z) normalized to sum to 1; produces probability distribution"),
        ("Sparse retrieval", "Lexical retrieval (BM25, SPLADE)"),
        ("Transformer", "Attention-based neural architecture (Vaswani et al., 2017)"),
        ("Tokenization", "Splitting text into discrete units (tokens) for model input"),
        ("vLLM", "High-throughput LLM serving framework with PagedAttention"),
        ("ViT", "Vision Transformer"),
        ("Word2Vec", "Static word embedding method (Mikolov et al., 2013)"),
    ]
    for term, defn in sorted(glossary):
        body(doc, f"{term}: {defn}")

    page_break(doc)
    chapter_heading(doc, "Appendix C", "Bibliography")
    body(doc, "Selected references cited throughout the book, in alphabetical order.")
    refs = [
        "Anthropic, 'Building Effective Agents' engineering blog (2024).",
        "Bai et al., 'Constitutional AI: Harmlessness from AI Feedback' (2022).",
        "Bender et al., 'On the Dangers of Stochastic Parrots' (2021).",
        "Bishop, Pattern Recognition and Machine Learning (2006).",
        "Brown et al., 'Language Models are Few-Shot Learners' (2020). GPT-3.",
        "Chen et al., 'Benchmarking Large Language Models in Retrieval-Augmented Generation' (2023). RGB.",
        "Christiano et al., 'Deep Reinforcement Learning from Human Preferences' (2017).",
        "DeepSeek-AI, 'DeepSeek-R1' (2025).",
        "Dettmers et al., 'QLoRA: Efficient Finetuning of Quantized LLMs' (2023).",
        "Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers' (2018).",
        "Dosovitskiy et al., 'An Image is Worth 16x16 Words' (2020). ViT.",
        "Edge et al., 'From Local to Global: A Graph RAG Approach' (2024). Microsoft GraphRAG.",
        "Es et al., 'RAGAS: Automated Evaluation of Retrieval Augmented Generation' (2023).",
        "Gao et al., 'Precise Zero-Shot Dense Retrieval without Relevance Labels' (2022). HyDE.",
        "Gebru et al., 'Datasheets for Datasets' (2018).",
        "Goodfellow, Bengio, Courville, Deep Learning (2016).",
        "He et al., 'Deep Residual Learning for Image Recognition' (2015). ResNet.",
        "Ho et al., 'Denoising Diffusion Probabilistic Models' (2020).",
        "Hoffmann et al., 'Training Compute-Optimal Large Language Models' (2022). Chinchilla.",
        "Hu et al., 'LoRA: Low-Rank Adaptation of Large Language Models' (2021).",
        "Jurafsky and Martin, Speech and Language Processing (3rd ed. draft).",
        "Khattab and Zaharia, 'ColBERT' (2020).",
        "Khattab et al., 'DSPy: Compiling Declarative LM Calls' (2023).",
        "Kingma and Welling, 'Auto-Encoding Variational Bayes' (2013). VAE.",
        "Krizhevsky, Sutskever, Hinton, 'ImageNet Classification with Deep CNNs' (2012). AlexNet.",
        "Kwon et al., 'PagedAttention for LLM Serving' (2023). vLLM.",
        "Lewis et al., 'Retrieval-Augmented Generation for Knowledge-Intensive NLP' (2020).",
        "Li et al., 'BLIP-2' (2023).",
        "Liu et al., 'LLaVA: Visual Instruction Tuning' (2023).",
        "MacKay, Information Theory, Inference, and Learning Algorithms (2003).",
        "Malkov and Yashunin, 'Efficient ANN Search via Hierarchical Navigable Small World' (2016). HNSW.",
        "Mikolov et al., 'Distributed Representations of Words and Phrases' (2013). Word2Vec.",
        "Mitchell et al., 'Model Cards for Model Reporting' (2019).",
        "Murphy, Probabilistic Machine Learning (2022, 2023).",
        "Ouyang et al., 'Training Language Models to Follow Instructions' (2022). InstructGPT.",
        "Pennington, Socher, Manning, 'GloVe' (2014).",
        "Radford et al., 'Learning Transferable Visual Models from Natural Language' (2021). CLIP.",
        "Rafailov et al., 'Direct Preference Optimization' (2023).",
        "Raffel et al., 'Exploring the Limits of Transfer Learning with T5' (2020).",
        "Reimers and Gurevych, 'Sentence-BERT' (2019).",
        "Rombach et al., 'High-Resolution Image Synthesis with Latent Diffusion' (2022). Stable Diffusion.",
        "Russell and Norvig, Artificial Intelligence: A Modern Approach (4th ed., 2020).",
        "Schulman et al., 'Proximal Policy Optimization Algorithms' (2017).",
        "Shao et al., 'DeepSeekMath' (2024). GRPO.",
        "Su et al., 'RoFormer: Enhanced Transformer with Rotary Position Embedding' (2021).",
        "Touvron et al., 'LLaMA: Open and Efficient Foundation Language Models' (2023).",
        "Vaswani et al., 'Attention Is All You Need' (2017).",
        "Wei et al., 'Chain-of-Thought Prompting Elicits Reasoning' (2022).",
        "Zheng et al., 'Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena' (2023).",
    ]
    for ref in refs:
        bullet(doc, ref)

    # About the Author
    page_break(doc)
    about_author(doc, AUTHOR, AUTHOR_BIO)

    # Final note / colophon
    page_break(doc)
    for _ in range(8):
        doc.add_paragraph()
    add_title(doc, "Colophon", size=18, center=True)
    body(doc, "")
    add_subtitle(doc,
        f"{TITLE}", size=11, center=True)
    add_subtitle(doc,
        f"{EDITION}, {YEAR}", size=10, center=True)
    add_subtitle(doc,
        f"Set in Calibri 11pt body, Calibri 28pt chapter titles.",
        size=9, center=True)
    add_subtitle(doc,
        f"Diagrams produced with matplotlib. Layout assembled with python-docx.",
        size=9, center=True)
    add_subtitle(doc,
        f"PDF generated via LibreOffice headless conversion.",
        size=9, center=True)
    body(doc, "")
    add_subtitle(doc,
        f"Published by {PUBLISHER}. Reference identifier: {RID}.",
        size=9, center=True)
    add_subtitle(doc,
        f"© {YEAR} {PUBLISHER}. All rights reserved.",
        size=9, center=True)

    out_docx = os.path.join(OUT, "AI_ML_GenAI_Comprehensive_Textbook.docx")
    doc.save(out_docx)
    print(f"WROTE {out_docx}")
    return out_docx


def render_section_txt(lines, sec, depth=2):
    """Render a section to plain text."""
    lines.append("")
    lines.append("-" * 80)
    lines.append(f"{sec['number']} {sec['title']}".upper())
    lines.append("-" * 80)
    lines.append("")

    for para in sec.get("paragraphs", []):
        lines.append(_wrap(para, 78))
        lines.append("")

    for label, text in sec.get("callouts", []):
        lines.append(f"  [{label}] {text}")
        lines.append("")

    if "equation" in sec:
        eq_text = sec["equation"]
        if sec.get("equation_label"):
            eq_text += f"     ({sec['equation_label']})"
        lines.append("    " + eq_text)
        lines.append("")

    for b in sec.get("bullets", []):
        lines.append(f"  - {b}")
    if sec.get("bullets"):
        lines.append("")

    for subsec in sec.get("subsections", []):
        lines.append("")
        lines.append("  ~~~ " + subsec["title"] + " ~~~")
        lines.append("")
        for para in subsec.get("paragraphs", []):
            lines.append(_wrap(para, 76))
            lines.append("")
        if "equation" in subsec:
            eq_text = subsec["equation"]
            if subsec.get("equation_label"):
                eq_text += f"     ({subsec['equation_label']})"
            lines.append("      " + eq_text)
            lines.append("")
        for para in subsec.get("more_paragraphs", []):
            lines.append(_wrap(para, 76))
            lines.append("")
        for b in subsec.get("bullets", []):
            lines.append(f"    - {b}")
        if subsec.get("bullets"):
            lines.append("")


def render_chapter_txt(lines, chapter):
    lines.append("")
    lines.append("=" * 80)
    lines.append(chapter["label"].upper().center(80))
    lines.append(chapter["title"].upper().center(80))
    lines.append("=" * 80)

    for sec in chapter["sections"]:
        render_section_txt(lines, sec)

    if chapter.get("further_reading"):
        lines.append("")
        lines.append("  ## Further Reading ##")
        for ref in chapter["further_reading"]:
            lines.append(f"  - {ref}")
        lines.append("")


def _wrap(text, width):
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


def build_txt():
    lines = []
    lines.append("=" * 80)
    lines.append(TITLE.center(80))
    lines.append(SUBTITLE.center(80))
    lines.append("")
    lines.append(AUTHOR.center(80))
    lines.append(EDITION.center(80))
    lines.append("=" * 80)
    lines.append("")
    lines.append("PREFACE")
    lines.append("-" * 80)
    lines.append("This textbook is a comprehensive guide to modern AI.")
    lines.append("Diagrams in the DOCX/PDF versions are referenced inline; standalone")
    lines.append("PNG files are stored in the Diagrams/ folder.")
    lines.append("")
    lines.append("TABLE OF CONTENTS")
    lines.append("-" * 80)
    for part_label, part_title, chapter_nums in PARTS:
        lines.append("")
        lines.append(f"  {part_label}: {part_title}")
        for n in chapter_nums:
            ch = CHAPTERS[n - 1]
            lines.append(f"    Chapter {n}: {ch['title']}")

    for part_label, part_title, chapter_nums in PARTS:
        lines.append("")
        lines.append("=" * 80)
        lines.append(f"{part_label}: {part_title}".upper().center(80))
        lines.append("=" * 80)
        for n in chapter_nums:
            render_chapter_txt(lines, CHAPTERS[n - 1])

    lines.append("")
    lines.append("=" * 80)
    lines.append("END OF BOOK".center(80))
    lines.append("=" * 80)

    out_txt = os.path.join(OUT, "AI_ML_GenAI_Comprehensive_Textbook.txt")
    with open(out_txt, "w") as f:
        f.write("\n".join(lines))
    print(f"WROTE {out_txt}")
    return out_txt


def build_pdf(docx_path):
    soffice = "/opt/homebrew/bin/soffice"
    out_pdf = os.path.join(OUT, "AI_ML_GenAI_Comprehensive_Textbook.pdf")
    cmd = [soffice, "--headless", "--convert-to", "pdf",
           "--outdir", OUT, docx_path]
    print(f"Running LibreOffice headless: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
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
