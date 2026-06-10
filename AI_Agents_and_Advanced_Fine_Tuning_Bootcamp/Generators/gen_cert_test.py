"""Generate the final PCAP-Agents certification exam and solution."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import (
    new_doc, add_title, add_subtitle, add_h1, add_h2, add_body,
    add_bullet, add_divider, add_table, add_footer_brand,
)
from quiz_bank import QUIZZES

ROOT = "/Users/pkr465/work/AI-Course-Material/AI_Agents_and_Advanced_Fine_Tuning_Bootcamp"
LETTERS = ["A", "B", "C", "D"]


# Drawn from each week's quiz bank: top 5 per week = 60 questions total.
def sample_per_week():
    out = []
    for week_num in range(1, 13):
        mcqs = QUIZZES[week_num]["mcq"][:5]
        for i, (q, options, ans, expl) in enumerate(mcqs, 1):
            out.append({
                "week": week_num,
                "q": q,
                "options": options,
                "ans": ans,
                "expl": expl,
            })
    return out


SCENARIOS = [
    {
        "title": "Production agent design",
        "prompt": (
            "Your team is asked to build an agent that answers customer "
            "billing questions over 12 internal systems. Latency target P95 "
            "under 4 seconds. Cost ceiling $0.05 per query. The team proposes "
            "a 5-agent system with a planner and 4 specialists. Critique the "
            "proposal and recommend an alternative if appropriate."
        ),
        "rubric": [
            "Identifies escalation-ladder violation (jump to multi-agent without trying rungs below).",
            "Names the tool-maximalist alternative explicitly.",
            "Estimates token cost of the proposed design against the cost ceiling.",
            "Considers latency cost of inter-agent coordination.",
            "Recommends measurement (both architectures on the same eval) rather than asserting an answer.",
        ],
    },
    {
        "title": "Fine-tuning vs RAG",
        "prompt": (
            "A product wants the model to consistently follow a specific "
            "structured-JSON response format for 20 internal tools, while "
            "answering domain questions accurately. The team proposes "
            "fine-tuning a 7B model. Decide whether RAG, fine-tuning, or "
            "hybrid is right. Justify."
        ),
        "rubric": [
            "Recognizes format-following is a fine-tuning win, not a RAG win.",
            "Recognizes domain knowledge is a RAG win, not a fine-tuning win.",
            "Recommends a hybrid: fine-tune for format, RAG for knowledge.",
            "Notes evaluation strategy: separate format adherence from answer quality.",
            "Mentions PEFT (LoRA/qLoRA) as the right fine-tuning rung first.",
        ],
    },
    {
        "title": "Alignment method selection",
        "prompt": (
            "You have 50K preference pairs and access to a 13B base model. "
            "You also have a verifier for 30% of the task space (SQL queries "
            "where execution against a test DB validates correctness). Pick "
            "a training strategy and defend it."
        ),
        "rubric": [
            "Identifies RLVR is appropriate for the 30% with verifiers.",
            "Picks DPO or GRPO for the 70% (preference data only).",
            "Considers a hybrid pipeline: SFT first, then RLVR + preference RL.",
            "Notes evaluation isolation between the two task subspaces.",
            "Estimates compute and time honestly.",
        ],
    },
    {
        "title": "System architecture",
        "prompt": (
            "Sketch a production-grade agentic RAG system for legal "
            "research. Multi-hop queries are common. Constraints: P95 latency "
            "under 8 seconds, 99% uptime, audit log for every retrieval, no "
            "personally identifiable information leakage to logs."
        ),
        "rubric": [
            "Identifies the right patterns (router, orchestrator-workers, evaluator-optimizer).",
            "Calls out HyDE for the vector backend specifically.",
            "Defines the audit log schema (what gets logged, what does not).",
            "Sketches PII handling at the boundary, not in the agent.",
            "Plans evaluation: held-out multi-hop set with gold answers and rubrics.",
        ],
    },
]


def build_exam(with_answers=False):
    doc = new_doc()
    suffix = ": Answer Key" if with_answers else ""
    add_title(doc, f"PCAP-Agents Final Certification Exam{suffix}", size=22)
    add_subtitle(doc, "AI Agents and Advanced Fine-Tuning Bootcamp", size=14)
    add_subtitle(doc, "Duration: 3 hours | Total: 240 points | Pass: 168 (70%)", size=11)
    add_divider(doc)

    add_h1(doc, "Exam Structure")
    structure = [
        ("Part A", "60 multiple-choice questions", "3 points each = 180 points"),
        ("Part B", "4 scenario-based long-form responses", "15 points each = 60 points"),
        ("Total", "", "240 points"),
    ]
    add_table(doc, ["Part", "Questions", "Scoring"], structure, col_widths=[1.0, 3.8, 2.0])

    add_h1(doc, "Instructions")
    add_bullet(doc, "Closed-notes for Part A. Open-notes for Part B (course materials only).")
    add_bullet(doc, "Allocate roughly 90 minutes for Part A, 90 minutes for Part B.")
    add_bullet(doc, "Partial credit awarded on Part B based on the rubric for each scenario.")
    add_bullet(doc, "Calculators allowed. No external internet access.")

    add_h1(doc, "Part A: Multiple Choice (60 questions)")
    qs = sample_per_week()
    for i, q in enumerate(qs, 1):
        add_h2(doc, f"Q{i} (Week {q['week']}). {q['q']}")
        for j, opt in enumerate(q["options"]):
            text = f"{LETTERS[j]}. {opt}"
            if with_answers and j == q["ans"]:
                text += "   [correct]"
            add_bullet(doc, text)
        if with_answers:
            add_body(doc, f"Explanation: {q['expl']}")

    add_h1(doc, "Part B: Scenarios (4 questions)")
    for i, s in enumerate(SCENARIOS, 1):
        add_h2(doc, f"Scenario {i}: {s['title']}")
        add_body(doc, s["prompt"])
        if with_answers:
            add_body(doc, "Grading rubric (3 points per item):")
            for item in s["rubric"]:
                add_bullet(doc, item)

    add_h1(doc, "Certification")
    add_body(doc,
        "A passing grade earns the PCAP-Agents certificate, recognized "
        "across the Proxiant alumni network and partner employers. The "
        "certificate is valid for 3 years; renewal requires either a "
        "completed continuing-education credit or re-examination.")

    add_divider(doc)
    add_footer_brand(doc)

    fname = f"PCAP_Agents_Final_Exam{'_Solution' if with_answers else ''}.docx"
    out = os.path.join(ROOT, "Certification_Test", fname)
    doc.save(out)
    print(f"WROTE {out}")


if __name__ == "__main__":
    build_exam(with_answers=False)
    build_exam(with_answers=True)
