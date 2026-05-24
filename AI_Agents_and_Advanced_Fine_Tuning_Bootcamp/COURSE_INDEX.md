# AI Agents and Advanced Fine-Tuning Bootcamp

**12 weeks. Hybrid (in-person + live Zoom + recorded). Start: Sunday, June 7, 2026.**

Built for engineers who already work with LLMs and want production-grade depth in agents and fine-tuning. Reads research papers, writes training loops, ships a real capstone.

---

## Folder Layout

| Folder | Contents | Count |
|---|---|---|
| `Catalogue/` | Course catalogue, target audience, outcomes, faculty | 1 |
| `Syllabus/` | Full 12-week syllabus with objectives, topics, papers, labs | 1 |
| `Class_Notes/` | Deep technical notes per week (one per main session) | 12 |
| `Slides/` | PPTX deck per week (~16 to 22 slides) for the Sunday session | 12 |
| `Lab_Walkthroughs/` | Step-by-step lab guides, starter code, verification checks | 26 |
| `Weekly_Quizzes/` | 12 MCQ + 3 short-answer quizzes plus answer keys | 24 |
| `Weekly_Projects/` | Project briefs with rubrics plus reference solution sketches | 24 |
| `Research_Papers/` | Weekly paper reading guides with discussion questions | 12 |
| `Certification_Test/` | PCAP-Agents final exam (60 MCQ + 4 scenarios) plus key | 2 |
| `Generators/` | Python source for regenerating all materials | 9 |

---

## Weekly Map

| Week | Date | Title | Theme |
|---|---|---|---|
| 1 | Jun 7, 2026 | Introduction to AI Agents | The agentic loop and your first working agent |
| 2 | Jun 14, 2026 | Enterprise AI | Reasoning workflows, agentic RAG, multi-agent teams |
| 3 | Jun 21, 2026 | Model Context Protocol (MCP) | Tool servers, schemas, tool-use maximalism |
| 4 | Jun 28, 2026 | Prompt Engineering and Optimization | CO-STAR, DSPy, GEPA, TextGrad, ORPO |
| 5 | Jul 5, 2026 | Fine-Tuning Foundations and Economy | Embeddings, LoRA, qLoRA, Chinchilla |
| 6 | Jul 12, 2026 | Reinforcement Learning Fundamentals | MDPs, PPO, DPO, GRPO, alignment |
| 7 | Jul 19, 2026 | Multiple Agents and Deep RL | SRP, facades, RL on real LLMs |
| 8 | Jul 26, 2026 | Distributed Computing with Ray | Parallelism, vLLM, MLOps with Airflow |
| 9 | Aug 2, 2026 | Agent Communications | A2A, Agent Cards, discovery, cooperation |
| 10 | Aug 9, 2026 | Architecting Agentic Systems | Nine production patterns, ruthless simplification |
| 11 | Aug 16, 2026 | Agentic RAG and Agentic Training | Multi-hop, HyDE, trajectory-based training |
| 12 | Aug 23, 2026 | The Path Ahead (Capstone) | RAG vs fine-tune, RLVR, MARL, presentations |

---

## Weekly Cadence

- **Sunday 11 AM to 1 PM PST** — Theory and paper reading
- **Sunday 5 PM to 9 PM PST** — Lab walkthrough and presentations
- **Tuesday 7 PM to 10 PM PST** — Guided lab session
- **Thursday 7 PM to 10 PM PST** — Guided lab session
- **Wednesday 8:30 AM to 10 AM PST** — Summary and weekly quiz

---

## Grading

| Component | Weight |
|---|---|
| Weekly quizzes (12) | 15% |
| Weekly projects (12) | 30% |
| Lab participation | 15% |
| Paper presentations | 10% |
| Capstone project | 25% |
| Final certification exam | 5% |

Passing grade: 70%. PCAP-Agents certificate issued on pass.

---

## Regenerating Materials

All documents are generated from Python sources in `Generators/`:

```bash
cd Generators
python3 gen_catalogue_syllabus.py
python3 gen_class_notes.py
python3 gen_slides.py
python3 gen_lab_walkthroughs.py
python3 gen_quizzes.py
python3 gen_projects.py
python3 gen_papers.py
python3 gen_cert_test.py
```

Requirements: `python-docx>=1.0`, `python-pptx>=1.0`.

---

## Faculty

- **Pavan R** — Lead instructor
- Teaching assistants for 1-on-1 sessions and lab support

Questions: info@proxiant.com | 1.855.LEARN.AI

---

© 2026 Proxiant Academy.
