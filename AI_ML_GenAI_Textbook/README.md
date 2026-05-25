# AI, ML, and Generative AI: A Comprehensive Textbook

**Author:** Pavan R, Proxiant Academy
**Edition:** 1 | 2026

A full-length textbook covering modern AI from mathematical foundations through production engineering. Sixteen chapters across seven parts, 36 embedded diagrams, ~32,000 words.

---

## Output Files

Located in `Output/`:

| File | Size | Purpose |
|---|---|---|
| `AI_ML_GenAI_Comprehensive_Textbook.docx` | 2.3 MB | Editable Word document with embedded diagrams |
| `AI_ML_GenAI_Comprehensive_Textbook.pdf` | 2.8 MB | Print-ready PDF |
| `AI_ML_GenAI_Comprehensive_Textbook.txt` | 243 KB | Plain text (no images) |

---

## Structure

**Part I — Foundations**
- Chapter 1: Introduction to AI and Modern Machine Learning
- Chapter 2: Mathematical Foundations
- Chapter 3: Neural Networks and Deep Learning

**Part II — Natural Language Processing and Transformers**
- Chapter 4: Classical Natural Language Processing
- Chapter 5: The Transformer Architecture

**Part III — Embeddings and Pretrained Models**
- Chapter 6: Word and Sentence Embeddings
- Chapter 7: Pretrained Language Models

**Part IV — Vision and Multimodal AI**
- Chapter 8: Computer Vision and Multimodal Models

**Part V — Prompts, Fine-Tuning, and Alignment**
- Chapter 9: Prompt Engineering and Optimization
- Chapter 10: Fine-Tuning Large Language Models
- Chapter 11: Alignment with Reinforcement Learning

**Part VI — Retrieval, Vectors, and RAG**
- Chapter 12: Vector Databases and Approximate Nearest Neighbor Search
- Chapter 13: Retrieval-Augmented Generation

**Part VII — Production: LLMOps, Evaluation, Ethics**
- Chapter 14: LLMOps and Production System Design
- Chapter 15: Evaluation Methodologies
- Chapter 16: Ethics, Safety, and the Path Ahead

**Appendices**
- A: Mathematical Notation
- B: Glossary (40+ terms)
- C: Bibliography (50+ references)

---

## Diagrams

40 PNG diagrams in `Diagrams/`, including:

- ANN architecture, single neuron, activation functions, backpropagation, vanishing/exploding gradients
- Gradient descent variants, bias-variance tradeoff, overfitting curves, dropout, data splits
- Confusion matrix, ROC curves, linear regression, logistic/softmax
- CNN pipeline, RNN unrolled, Transformer architecture, attention (Q/K/V)
- Word2Vec architecture, embedding space, tokenization comparison
- RoPE rotation, RLHF detailed pipeline, PPO clipped objective
- HNSW graph, MoE diagram, Production RAG architecture
- Diffusion process, latent space concept, Chinchilla scaling
- LoRA mechanics, adaptation ladder, AI taxonomy, learning paradigms
- Encoder-decoder, ANN search, loss landscape

---

## Building from Source

All chapters are Python modules under `Source/`. Each chapter defines a `CHAPTER` dict with sections, subsections, paragraphs, equations, callouts, and bullets. The build script reads the modules and produces DOCX → PDF → TXT.

```bash
cd Source

# Generate all diagrams (one-time)
python3 make_textbook_diagrams.py

# Build textbook in all three formats
python3 build_textbook.py
```

**Dependencies:**
- python-docx >= 1.0
- matplotlib >= 3.7
- LibreOffice (for DOCX → PDF; `/opt/homebrew/bin/soffice` on macOS)

---

## Adding Content

To add a new chapter:

1. Create `Source/chapter_NN_topic.py` with a `CHAPTER` dict.
2. Add a diagram script entry in `make_textbook_diagrams.py` if needed.
3. Import the chapter in `build_textbook.py`, append to `CHAPTERS`, and add to `PARTS`.
4. Rebuild.

To extend an existing chapter:

1. Edit the chapter module's `CHAPTER` dict.
2. Add sections, subsections, paragraphs, equations, callouts, bullets.
3. Reference diagrams by filename in the `image` field.
4. Rebuild.

---

## Notes on Style

The book follows the project writing rules:
- No em dashes; commas, parentheses, or sentence breaks instead.
- No AI cliches ("delve", "leverage", "underscore", "robust" as filler).
- Plain declarative prose; vary sentence rhythm.
- Spell out percentages in body text; tables use `%`.
- No exclamation points outside quotations.
- Citations point to original papers, not summaries.

---

© 2026 Proxiant Academy. All rights reserved.
