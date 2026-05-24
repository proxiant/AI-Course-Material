"""Generate the 12 class notes documents."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import (
    new_doc, add_title, add_subtitle, add_h1, add_h2, add_h3, add_body,
    add_bullet, add_code, add_divider, add_page_break,
)
from bootcamp_content import WEEKS, slug
from class_notes_deep import DEEP

ROOT = "/Users/pkr465/work/AI-Course-Material/AI_Agents_and_Advanced_Fine_Tuning_Bootcamp"


def build_one(week):
    doc = new_doc()
    n = week["num"]

    add_title(doc, f"Week {n}: {week['title']}", size=22)
    add_subtitle(doc, week["tagline"], size=14)
    add_subtitle(doc, f"Main session date: {week['date']}", size=11)
    add_subtitle(doc, "AI Agents and Advanced Fine-Tuning Bootcamp | Proxiant Academy", size=11)
    add_divider(doc)

    add_h1(doc, "Session Overview")
    add_body(doc, DEEP[n]["intro"])

    add_h2(doc, "Learning Objectives")
    for o in week["objectives"]:
        add_bullet(doc, o)

    add_page_break(doc)
    add_h1(doc, "Detailed Notes")
    for sec in DEEP[n]["sections"]:
        add_h2(doc, sec["h"])
        add_body(doc, sec["body"])
        if "code" in sec:
            add_body(doc, "Reference snippet:")
            add_code(doc, sec["code"])

    add_page_break(doc)
    add_h1(doc, "Topics at a Glance")
    for tname, tdesc in week["topics"]:
        add_h3(doc, tname)
        add_body(doc, tdesc)

    add_h1(doc, "Research Papers")
    for ptitle, pnote in week["papers"]:
        add_h3(doc, ptitle)
        add_body(doc, pnote)

    add_h1(doc, "This Week's Labs")
    for lab in week["labs"]:
        add_h3(doc, lab["title"])
        add_body(doc, f"Objective: {lab['objective']}")
        add_body(doc, f"Deliverables: {lab['deliverables']}")

    add_h1(doc, "Review Questions")
    for q in DEEP[n]["review"]:
        add_bullet(doc, q)
    add_body(doc, "Answers are reviewed live during the Wednesday quiz session.")

    add_h1(doc, "Further Reading")
    add_body(doc, "Listed in the dedicated paper reading guide for this week (see Research_Papers folder).")

    out = os.path.join(ROOT, "Class_Notes",
                       f"Week_{n:02d}_{slug(week)}_Notes.docx")
    doc.save(out)
    print(f"WROTE {out}")


if __name__ == "__main__":
    for w in WEEKS:
        build_one(w)
