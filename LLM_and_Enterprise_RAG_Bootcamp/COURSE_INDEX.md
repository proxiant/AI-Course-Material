# LLM and Enterprise RAG Bootcamp

**12 weeks. Hybrid (in-person + live Zoom + recorded). Start: Saturday, June 6, 2026.**

Hackathon-style, coding-centered bootcamp that bridges foundational ML theory with enterprise-scale engineering. Teams of 4-6 build production RAG systems in dedicated rooms with full multimedia setup and direct access to the Proxiant Datacenter.

---

## Folder Layout

| Folder | Contents | Count |
|---|---|---|
| `Catalogue/` | Course catalogue, target audience, outcomes, faculty | 1 |
| `Syllabus/` | Full 12-week syllabus with objectives, topics, papers, labs | 1 |
| `Class_Notes/` | Deep technical notes per week (one per main session) | 12 |
| `Slides/` | PPTX deck per week (~16 to 22 slides) for the Saturday session | 12 |
| `Lab_Walkthroughs/` | Step-by-step lab guides, starter code, verification checks | 25 |
| `Weekly_Quizzes/` | 12 MCQ + 3 short-answer quizzes plus answer keys | 24 |
| `Weekly_Projects/` | Project briefs with rubrics plus reference solution sketches | 24 |
| `Research_Papers/` | Weekly paper reading guides with discussion questions | 12 |
| `Certification_Test/` | PCAP-RAG final exam (60 MCQ + 4 scenarios) plus key | 2 |
| `Generators/` | Python source for regenerating all materials | 5 |

---

## Weekly Map

| Week | Date | Title | Theme |
|---|---|---|---|
| 1 | Jun 6, 2026 | Introduction to Language Models | From keyword search to semantic understanding |
| 2 | Jun 13, 2026 | High-Dimensional Geometry | BERT, contrastive loss, anisotropy |
| 3 | Jun 20, 2026 | Retrieval | Chunking strategies and hierarchical retrieval |
| 4 | Jun 27, 2026 | Retrieval Funnel | Sparse + dense, Matryoshka, ColBERT, cross-encoder |
| 5 | Jul 4, 2026 | Vision | CNNs, ViTs, CLIP, BLIP-2 |
| 6 | Jul 11, 2026 | Prompts | CO-STAR, DSPy, GEPA, TextGrad, ORPO |
| 7 | Jul 18, 2026 | Graph-Based Retrieval | RAPTOR, GraphRAG, LightRAG |
| 8 | Jul 25, 2026 | Overcoming RAG Challenges | Guardrails, grounding, P95 latency |
| 9 | Aug 1, 2026 | Towards Enterprise RAG | Derivative artifacts, HyDE, semantic cache |
| 10 | Aug 8, 2026 | Agentic RAG and Text2SQL | Agent lifecycles, MCP, SQL generation |
| 11 | Aug 15, 2026 | Fine-Tuning | Chinchilla, LoRA, RLHF, RLVR, GRPO |
| 12 | Aug 22, 2026 | Evals | Retrieval metrics, Ragas, LLM-as-judge, RGB |

---

## Weekly Cadence

- **Saturday 11 AM to 1 PM PST** — Morning theory session
- **Saturday 1 to 1:30 PM PST** — Lunch (served on-site)
- **Saturday 1:30 to 4 PM PST** — Afternoon labs and exercises
- **Saturday 4 to 5 PM PST** — Project presentations
- **Monday 7 to 10 PM PST** — Guided lab session
- **Wednesday 7 to 10 PM PST** — Guided lab session
- **Tuesday 8:30 to 10 AM PST** — Summary and weekly quiz

---

## Grading

| Component | Weight |
|---|---|
| Weekly quizzes (12) | 15% |
| Weekly team projects (12) | 30% |
| Lab participation | 15% |
| Paper presentations | 10% |
| Capstone project | 25% |
| Final certification exam | 5% |

Passing grade: 70%. PCAP-RAG certificate issued on pass.

---

## Regenerating Materials

All documents are generated from Python sources in `Generators/`:

```bash
cd Generators
python3 gen_all.py
```

Requirements: `python-docx>=1.0`, `python-pptx>=1.0`.

---

## Faculty

- **Pavan R** — Lead instructor
- Teaching assistants for 1-on-1 sessions and lab support

Questions: info@proxiant.com | 1.855.LEARN.AI

---

© 2026 Proxiant Academy.
