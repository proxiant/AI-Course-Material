# LLM and Enterprise RAG Bootcamp

**12 weeks. Hybrid (in-person + live Zoom + recorded). Start: Saturday, October 3, 2026.**

Hackathon-style, coding-centered bootcamp that bridges foundational ML theory with enterprise-scale engineering. Teams of 4-6 build production RAG systems in dedicated rooms with full multimedia setup and direct access to the Proxiant Datacenter.

---

## Folder Layout

| Folder | Contents | Count |
|---|---|---|
| `Catalogue/` | Course catalogue, target audience, outcomes, faculty | 1 |
| `Syllabus/` | Full 12-week syllabus with objectives, topics, papers, labs | 1 |
| `Class_Notes/` | Deep technical notes per week (one per main session) | 12 |
| `Slides/` | PPTX deck per week (~24 to 27 slides) for the Saturday session | 12 |
| `Lab_Walkthroughs/` | 25 guided lab walkthroughs: step-by-step guides, starter code, verification checks | 25 |
| `Weekly_Quizzes/` | 12 MCQ + 3 short-answer quizzes plus answer keys with model answers | 24 |
| `Weekly_Projects/` | Project briefs with rubrics plus reference solution sketches | 24 |
| `Research_Papers/` | Weekly paper reading guides with discussion questions | 12 |
| `Certification_Test/` | PCAIP-RAG final exam (60 MCQ + 4 scenarios) plus key | 2 |
| `Generators/` | Python source for regenerating all materials | 8 |

---

## Weekly Map

| Week | Date | Title | Theme |
|---|---|---|---|
| 1 | Oct 3, 2026 | Introduction to Language Models | From keyword search to semantic understanding |
| 2 | Oct 10, 2026 | High-Dimensional Geometry | BERT, contrastive loss, anisotropy |
| 3 | Oct 17, 2026 | Retrieval | Chunking strategies and hierarchical retrieval |
| 4 | Oct 24, 2026 | Retrieval Funnel | Sparse + dense, Matryoshka, ColBERT, cross-encoder |
| 5 | Oct 31, 2026 | Vision | CNNs, ViTs, CLIP, BLIP-2 |
| 6 | Nov 7, 2026 | Prompts | CO-STAR, DSPy, GEPA, TextGrad, ORPO |
| 7 | Nov 14, 2026 | Graph-Based Retrieval | RAPTOR, GraphRAG, LightRAG |
| 8 | Nov 21, 2026 | Overcoming RAG Challenges | Guardrails, grounding, P95 latency |
| 9 | Nov 28, 2026 | Towards Enterprise RAG | Derivative artifacts, HyDE, semantic cache |
| 10 | Dec 5, 2026 | Agentic RAG and Text2SQL | Agent lifecycles, MCP, SQL generation |
| 11 | Dec 12, 2026 | Fine-Tuning | Chinchilla, LoRA, RLHF, RLVR, GRPO |
| 12 | Dec 19, 2026 | Evals | Retrieval metrics, Ragas, LLM-as-judge, RGB |

---

## Weekly Cadence

- **Saturday 11 AM to 1 PM PT**: Morning theory session
- **Saturday 1 to 1:30 PM PT**: Lunch (served on-site)
- **Saturday 1:30 to 4 PM PT**: Afternoon labs and exercises
- **Saturday 4 to 5 PM PT**: Project presentations
- **Monday 7 to 10 PM PT**: Guided lab session
- **Wednesday 7 to 10 PM PT**: Guided lab session
- **Tuesday 8:30 to 10 AM PT**: Summary and weekly quiz

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

Passing grade: 70%. PCAIP-RAG certificate issued on pass.

Capstone = week 12 project, graded separately (25%). Weeks 1-11 projects count toward the 30% team-project component.

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

- **Pavan R**, Lead instructor
- Teaching assistants for 1-on-1 sessions and lab support

Questions: info@proxiant.com | proxiant.ai/training

---

© 2026 Proxiant Academy.
