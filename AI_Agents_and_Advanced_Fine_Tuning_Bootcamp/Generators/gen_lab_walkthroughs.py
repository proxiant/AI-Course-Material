"""Generate lab walkthrough documents: 2 to 3 per week."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import (
    new_doc, add_title, add_subtitle, add_h1, add_h2, add_h3, add_body,
    add_bullet, add_numbered, add_code, add_table, add_divider,
)
from bootcamp_content import WEEKS

ROOT = "/Users/pkr465/work/AI-Course-Material/AI_Agents_and_Advanced_Fine_Tuning_Bootcamp"

# Extra detail per lab keyed by (week_num, lab_index).
LAB_DETAIL = {
    (1, 0): {
        "environment": "Local laptop with SSH key registered with cluster admin. Conda env 'pba-w1' from the cluster onboarding gist.",
        "concepts": [
            "Ray head node, worker nodes, dashboard URL",
            "Resource specs: num_cpus, num_gpus, memory",
            "Actor lifecycle: create, schedule, terminate",
        ],
        "starter_code": (
            "import ray\n"
            "ray.init(address='ray://head.cluster.proxiant:10001')\n\n"
            "@ray.remote(num_gpus=1)\n"
            "class TokenizerActor:\n"
            "    def __init__(self, model_id='bert-base-uncased'):\n"
            "        from transformers import AutoTokenizer\n"
            "        self.tok = AutoTokenizer.from_pretrained(model_id)\n"
            "    def summarize(self, text):\n"
            "        ids = self.tok(text, truncation=True)['input_ids']\n"
            "        return {'len': len(ids), 'first': ids[:5]}\n"
        ),
        "checks": [
            "ray status returns at least one GPU node",
            "actor handle resolves and the first remote call completes in under 30 seconds",
            "ten parallel calls finish in less than 3 times a single call",
            "actor termination releases the GPU (verify with nvidia-smi)",
        ],
    },
    (1, 1): {
        "environment": "n8n self-hosted instance with LLM credentials configured. Lab ships a docker-compose for local n8n.",
        "concepts": [
            "n8n workflow as a directed graph of nodes",
            "Switch node driven by structured JSON output",
            "Iteration cap to prevent runaway loops",
        ],
        "starter_code": (
            "// LLM node system prompt\n"
            "You are a routing agent. You have three tools:\n"
            "  web_search(query)\n"
            "  calculator(expression)\n"
            "  csv_lookup(table, key)\n"
            "Always reply with JSON: {\"tool\": <name>, \"args\": {...}} or\n"
            "{\"final\": <answer>}.\n"
        ),
        "checks": [
            "each tool node returns valid JSON in isolation",
            "switch node correctly dispatches on tool name",
            "workflow halts after five iterations even if no final emitted",
            "log shows tool selections for all five sample questions",
        ],
    },
}

from lab_detail_full import LAB_DETAIL_FULL
LAB_DETAIL.update(LAB_DETAIL_FULL)


def detail_for(n, i):
    return LAB_DETAIL.get((n, i), {
        "environment": "Cluster workspace from week 1 plus week-specific deps in the requirements.txt that ships with this lab.",
        "concepts": ["Concept list available in the class notes for this week.",
                     "Lab guide TA reviews the concepts in the first 15 minutes."],
        "starter_code": "# Starter code is in the lab repo: see lab_starter.py.",
        "checks": [
            "all deliverables present in the submission folder",
            "code runs end-to-end without modification",
            "results match the expected ranges in the rubric",
        ],
    })


def build_one(week, lab, idx):
    doc = new_doc()
    n = week["num"]
    add_title(doc, f"Week {n} | Lab {chr(65+idx)}", size=22)
    add_subtitle(doc, lab["title"], size=14)
    add_subtitle(doc,
                 f"Bootcamp week: {week['title']} | Session: {('Tuesday', 'Thursday', 'Sunday lab block')[min(idx, 2)]}",
                 size=11)
    add_divider(doc)

    d = detail_for(n, idx)

    add_h1(doc, "Lab Objective")
    add_body(doc, lab["objective"])

    add_h1(doc, "Prerequisites")
    add_body(doc, lab["prereqs"])

    add_h1(doc, "Environment Setup")
    add_body(doc, d["environment"])

    add_h1(doc, "Key Concepts")
    for c in d["concepts"]:
        add_bullet(doc, c)

    add_h1(doc, "Walkthrough")
    for step in lab["steps"]:
        add_numbered(doc, step)

    add_h1(doc, "Starter Code")
    add_code(doc, d["starter_code"])

    add_h1(doc, "Verification Checks")
    for c in d["checks"]:
        add_bullet(doc, c)

    add_h1(doc, "Deliverables")
    add_body(doc, lab["deliverables"])

    add_h1(doc, "Grading Rubric")
    rubric = [
        ("Code correctness", "30", "Code runs as specified; results in expected ranges"),
        ("Engineering quality", "20", "Readable, no dead code, sensible names"),
        ("Observability", "15", "Logs, traces, or charts as required by deliverables"),
        ("Analysis", "20", "Written reflection identifies real tradeoffs"),
        ("Reproducibility", "15", "Peer can re-run by following the README"),
    ]
    add_table(doc, ["Criterion", "Points", "Description"], rubric, col_widths=[2.0, 0.8, 4.2])

    add_h1(doc, "Common Pitfalls")
    add_bullet(doc, "Skipping the verification checks. Each one catches a frequent error.")
    add_bullet(doc, "Hard-coding paths. Use the lab repo's config.")
    add_bullet(doc, "Skipping the reflection. The TA grading uses it heavily.")

    fname = f"Week_{n:02d}_Lab_{chr(65+idx)}_{safe(lab['title'])}.docx"
    out = os.path.join(ROOT, "Lab_Walkthroughs", fname)
    doc.save(out)
    print(f"WROTE {out}")


def safe(t):
    out = []
    for c in t.lower():
        if c.isalnum():
            out.append(c)
        elif c in " -_":
            out.append("_")
    return "".join(out)[:80].strip("_")


if __name__ == "__main__":
    for w in WEEKS:
        for i, lab in enumerate(w["labs"]):
            build_one(w, lab, i)
