"""Generate the Course Catalogue and the Detailed Syllabus."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import (
    new_doc, add_title, add_subtitle, add_h1, add_h2, add_h3, add_body,
    add_bullet, add_table, add_divider, add_page_break, add_header_block,
)
from bootcamp_content import WEEKS, START_DATE, DURATION_WEEKS, TUITION, PREREQ

ROOT = "/Users/pkr465/work/AI-Course-Material/AI_Agents_and_Advanced_Fine_Tuning_Bootcamp"
COURSE_NAME = "AI Agents and Advanced Fine-Tuning Bootcamp"


def build_catalogue():
    doc = new_doc()
    add_title(doc, "Proxiant Academy", size=24)
    add_subtitle(doc, COURSE_NAME, size=16)
    add_subtitle(doc, "Course Catalogue", size=12)
    add_divider(doc)

    add_body(doc, f"Start date: {START_DATE}")
    add_body(doc, f"Duration: {DURATION_WEEKS} weeks")
    add_body(doc, "Format: Hybrid (in-person at Fremont campus, live Zoom, or both)")
    add_body(doc, f"Tuition: {TUITION}")
    add_body(doc, "Schedule: Sundays 11 AM PST (main session). Tuesday and Thursday 7 to 10 PM PST (labs). Wednesday 8:30 to 10 AM PST (summary and quiz).")
    add_body(doc, "")

    add_h1(doc, "Who This Is For")
    add_body(doc,
        "This bootcamp is built for AI engineers, ML platform engineers, applied "
        "researchers, and senior software engineers who already work with LLMs and "
        "want production-grade depth in agents and fine-tuning. It is not an "
        "introduction. Expect to read research papers, write training loops, and "
        "ship a real capstone project.")

    add_h1(doc, "Learning Outcomes")
    outcomes = [
        "Design and operate multi-agent systems that survive production traffic.",
        "Apply the agentic loop, escalation ladders, and nine architectural patterns from working code.",
        "Build MCP tool servers with strong schemas and clean error semantics.",
        "Optimize prompts programmatically with DSPy, GEPA, ORPO, and TextGrad.",
        "Fine-tune base models with full FT, LoRA, qLoRA, and contrastive objectives.",
        "Train aligned models with PPO, DPO, and GRPO; understand where each fits.",
        "Scale training and serving on Ray with vLLM and Airflow.",
        "Implement agent-to-agent communication using A2A, Agent Cards, and discovery registries.",
        "Build agentic RAG with multi-hop retrieval, HyDE, and trajectory-based training.",
        "Defend technical choices in front of peers in the capstone presentation.",
    ]
    for o in outcomes:
        add_bullet(doc, o)

    add_h1(doc, "Skills You Will Learn")
    skills = [
        ("Agentic engineering", "Agentic loops, design patterns, multi-agent communication, tool-use maximalism, agentic RAG."),
        ("Fine-tuning", "LoRA, qLoRA, full fine-tuning, contrastive embedders, soft prompting, steering vectors."),
        ("Alignment with RL", "PPO, DPO, GRPO, TRPO, reward shaping, KL control, RLVR."),
        ("Tooling and protocols", "MCP, FastMCP, Google ADK, LangGraph, A2A, Agent Cards, Nanda, Cisco Agency."),
        ("Distributed systems", "Ray Core, Ray Train, Ray Tune, Ray Serve, vLLM, Airflow MLOps."),
        ("Prompt optimization", "CO-STAR, DSPy (COPRO, MIPRO), GEPA, TextGrad, ORPO."),
    ]
    add_table(doc, ["Area", "Coverage"], skills, col_widths=[1.8, 5.0])

    add_h1(doc, "What Is Included")
    included = [
        "12 main lecture sessions (Sundays, full day) with theory and paper readings.",
        "24 guided lab sessions (Tuesday and Thursday evenings) with working code.",
        "12 weekly quizzes (Wednesday mornings) covering both theory and lab material.",
        "12 weekly take-home projects, each peer-reviewed.",
        "12 weekly research paper reading guides with annotated questions.",
        "Access to the Proxiant Ray cluster: 20+ GPU servers, 40+ NVIDIA GPUs (RTX PRO 6000 Blackwell, RTX 5090, RTX 4090).",
        "Discord access to instructors and TAs, plus office hours twice weekly.",
        "Full session recordings on the workshop portal, available indefinitely.",
        "Capstone presentation slot, peer review, and a written critique from faculty.",
        "PCAP-Agents certificate on passing the final exam (separate from the standard PCAP).",
    ]
    for x in included:
        add_bullet(doc, x)

    add_h1(doc, "Prerequisites")
    add_body(doc, PREREQ)

    add_h1(doc, "Faculty")
    add_body(doc,
        "Lead instructor: Pavan R. Teaching assistants provide 1-on-1 "
        "sessions and lab support throughout the bootcamp.")

    add_h1(doc, "Tuition and Registration")
    add_body(doc, TUITION)
    add_body(doc, "Register at proxiant.com/bootcamp or email info@proxiant.com. "
                  "Day 1 (June 7, 2026) is open to all interested participants free of charge.")

    add_h1(doc, "Twelve-Week Map")
    rows = [(f"Week {w['num']}", w["date"].split(", ")[1], w["title"], w["tagline"]) for w in WEEKS]
    add_table(doc, ["Week", "Date", "Title", "Theme"], rows, col_widths=[0.7, 1.4, 2.2, 2.6])

    out = os.path.join(ROOT, "Catalogue", "AI_Agents_Bootcamp_Course_Catalogue.docx")
    doc.save(out)
    print(f"WROTE {out}")


def build_syllabus():
    doc = new_doc()
    add_title(doc, "Proxiant Academy", size=24)
    add_subtitle(doc, COURSE_NAME, size=16)
    add_subtitle(doc, "Detailed Twelve-Week Syllabus", size=12)
    add_divider(doc)

    add_h1(doc, "Course Information")
    info = [
        ("Course title", COURSE_NAME),
        ("Start date", START_DATE),
        ("Duration", f"{DURATION_WEEKS} weeks"),
        ("Format", "Hybrid (in-person + live Zoom + recorded)"),
        ("Tuition", TUITION),
        ("Prerequisites", PREREQ),
        ("Lead instructor", "Pavan R"),
        ("Cohort size", "Capped at 60 to preserve hands-on time"),
    ]
    add_table(doc, ["Field", "Value"], info, col_widths=[1.6, 5.4])

    add_h1(doc, "Course Description")
    add_body(doc,
        "A twelve-week intensive that takes engineers from production LLM "
        "usage to production-grade agentic systems and aligned fine-tuned "
        "models. The curriculum interleaves theory (mornings) with labs and "
        "presentations (evenings). Weekly quizzes lock in concepts. Weekly "
        "take-home projects build the portfolio. The final two weeks are "
        "reserved for capstone work and peer review.")

    add_h1(doc, "Weekly Cadence")
    cadence = [
        ("Sunday morning", "Theory session and research paper reading", "11 AM to 1 PM PST"),
        ("Sunday evening", "Lab walkthrough and presentations", "5 PM to 9 PM PST"),
        ("Tuesday", "Guided lab session", "7 PM to 10 PM PST"),
        ("Thursday", "Guided lab session", "7 PM to 10 PM PST"),
        ("Wednesday", "Summary and weekly quiz", "8:30 AM to 10 AM PST"),
    ]
    add_table(doc, ["Day", "Activity", "Time"], cadence, col_widths=[1.4, 3.6, 2.0])

    add_h1(doc, "Grading and Assessment")
    grading = [
        ("Weekly quizzes (12)", "15%", "Multiple choice + short answer, drawn from theory and labs"),
        ("Weekly projects (12)", "30%", "Take-home, peer reviewed against a rubric"),
        ("Lab participation", "15%", "Attendance and submitted lab artifacts"),
        ("Paper presentations", "10%", "One per student over the cohort"),
        ("Capstone project", "25%", "Code, presentation, peer review"),
        ("Final certification exam", "5%", "PCAP-Agents written exam"),
    ]
    add_table(doc, ["Component", "Weight", "Description"], grading, col_widths=[1.8, 0.8, 4.2])
    add_body(doc, "Passing grade is 70%. PCAP-Agents certificate issued on pass.")

    add_h1(doc, "Required Tooling")
    tooling = [
        "Python 3.11+, conda or uv, PyTorch 2.4+, Hugging Face transformers and TRL",
        "DSPy, GEPA reference, TextGrad",
        "Ray 2.x, vLLM, Airflow 2.x",
        "Google ADK, LangGraph, n8n",
        "FastMCP and the MCP inspector",
        "Docker, kubectl (for the deployment labs)",
        "git, GitHub access, signed SSH key for the Ray cluster",
    ]
    for t in tooling:
        add_bullet(doc, t)

    add_page_break(doc)
    add_h1(doc, "Weekly Detail")

    for w in WEEKS:
        add_h2(doc, f"Week {w['num']}: {w['title']}")
        add_subtitle(doc, w["date"], size=11)
        add_body(doc, w["summary"])

        add_h3(doc, "Learning objectives")
        for o in w["objectives"]:
            add_bullet(doc, o)

        add_h3(doc, "Topics covered")
        for tname, tdesc in w["topics"]:
            add_bullet(doc, f"{tname}: {tdesc}")

        add_h3(doc, "Research papers")
        for ptitle, pnote in w["papers"]:
            add_bullet(doc, f"{ptitle}. {pnote}")

        add_h3(doc, "Labs this week")
        for lab in w["labs"]:
            add_bullet(doc, f"{lab['title']}: {lab['objective']}")

        add_divider(doc)

    out = os.path.join(ROOT, "Syllabus", "AI_Agents_Bootcamp_Syllabus.docx")
    doc.save(out)
    print(f"WROTE {out}")


if __name__ == "__main__":
    build_catalogue()
    build_syllabus()
