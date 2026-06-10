# AI, ML, and Generative AI Interview Questions

**Author:** Pavan R, Proxiant Academy
**Edition:** First Edition, Rev 1.1 | 2026

A comprehensive interview-preparation reference for engineers, researchers, and architects: 232 questions with full worked answers, from neural-network fundamentals through RAG, fine-tuning, and LLMOps. Suitable for candidates from junior through senior levels and for interviewers building question banks.

---

## Output Files

Located in `Output/`:

| File | Size | Purpose |
|---|---|---|
| `AI_ML_GenAI_Interview_Questions_Textbook.docx` | 1.5 MB | Editable Word document with embedded diagrams |
| `AI_ML_GenAI_Interview_Questions_Textbook.pdf` | 1.8 MB (127 pages) | Print-ready PDF |
| `AI_ML_GenAI_Interview_Questions_Textbook.txt` | 271 KB | Plain text (no images) |

---

## Contents

232 questions and answers across 12 chapters:

| Chapter | Topic | Questions |
|---|---|---|
| 1 | Artificial Neural Networks | 15 |
| 2 | Classical NLP | 13 |
| 3 | Transformers | 32 |
| 4 | LLM Fundamentals | 13 |
| 5 | Embeddings | 22 |
| 6 | RAG and Multimodal RAG | 34 |
| 7 | Fine-Tuning | 26 |
| 8 | Vector Databases | 10 |
| 9 | LLMOps | 11 |
| 10 | Evaluation | 22 |
| 11 | Miscellaneous and Advanced | 21 |
| 12 | Formulas and Deep Dives | 13 |

20 diagrams (37 placements) illustrate the answers: ANN architecture, backpropagation, gradient descent, CNN/RNN, transformer architecture, attention, embeddings, tokenization, RAG pipeline, LoRA, RLHF, overfitting, and more. All PNGs live in `Diagrams/`.

---

## Building from Source

Content lives in Python modules under `Source/` (`content_part1.py` through `content_part7.py`); `helpers.py` holds shared document builders.

```bash
cd Source

# Generate all diagrams (one-time)
python3 make_diagrams.py

# Build the book in all three formats
python3 build_textbook.py
```

**Dependencies:**
- python-docx >= 1.0
- matplotlib >= 3.7
- LibreOffice (for DOCX to PDF; `/opt/homebrew/bin/soffice` on macOS)

---

## Notes on Style

The book follows the project writing rules:
- No em dashes; commas, parentheses, or sentence breaks instead.
- No AI cliches ("delve", "leverage", "underscore", "robust" as filler).
- Plain declarative prose; vary sentence rhythm.
- Confident, specific answers with formulas where they help.

---

© 2026 Proxiant Academy. All rights reserved.
