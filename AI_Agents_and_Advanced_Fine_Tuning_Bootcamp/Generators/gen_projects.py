"""Generate the 12 weekly project briefs and solution sketches."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import (
    new_doc, add_title, add_subtitle, add_h1, add_h2, add_h3, add_body,
    add_bullet, add_numbered, add_code, add_table, add_divider, add_footer_brand,
)
from bootcamp_content import WEEKS
from projects_bank import PROJECTS

ROOT = "/Users/pkr465/work/AI-Course-Material/AI_Agents_and_Advanced_Fine_Tuning_Bootcamp"


def build_project(week, solution=False):
    n = week["num"]
    proj = PROJECTS[n]
    doc = new_doc()

    suffix = ": Reference Solution Sketch" if solution else ""
    add_title(doc, f"Week {n} Project Brief{suffix}", size=22)
    add_subtitle(doc, proj["title"], size=14)
    add_subtitle(doc, f"Bootcamp theme: {week['title']} | Due next Sunday before main session", size=11)
    add_divider(doc)

    add_h1(doc, "Project Summary")
    add_body(doc, proj["summary"])

    add_h1(doc, "Required Tools and Libraries")
    for t in proj["tools"]:
        add_bullet(doc, t)

    add_h1(doc, "Deliverables")
    for d in proj["deliverables"]:
        add_bullet(doc, d)

    add_h1(doc, "Grading Rubric")
    rubric = [
        ("Correctness", "30", "Code runs as specified; results meet the bar"),
        ("Engineering quality", "20", "Clean, readable, tested where it matters"),
        ("Evaluation rigor", "20", "Eval design is honest; numbers are reproducible"),
        ("Observability and reproducibility", "15", "README + traces let a peer rerun in under 30 minutes"),
        ("Written reflection", "15", "Tradeoffs explicit, failure cases owned"),
    ]
    add_table(doc, ["Criterion", "Points", "Description"], rubric, col_widths=[2.4, 0.8, 4.0])
    add_body(doc, proj["rubric_extra"])

    add_h1(doc, "Submission")
    add_bullet(doc, "Push to a private GitHub repo and add the TAs as collaborators.")
    add_bullet(doc, f"Tag the submission commit 'week-{n:02d}-submit'.")
    add_bullet(doc, "Post the repo link in the bootcamp Discord by Sunday 11 AM PT.")

    if solution:
        add_h1(doc, "Reference Solution Sketch")
        add_body(doc, SOLUTION_SKETCHES[n]["intro"])
        for h, body in SOLUTION_SKETCHES[n]["sections"]:
            add_h2(doc, h)
            add_body(doc, body)
        if "code" in SOLUTION_SKETCHES[n]:
            add_h2(doc, "Reference Code Skeleton")
            add_code(doc, SOLUTION_SKETCHES[n]["code"])
        add_h1(doc, "Common Failure Modes")
        for f in SOLUTION_SKETCHES[n].get("failures", []):
            add_bullet(doc, f)

    add_divider(doc)
    add_footer_brand(doc)

    folder = "Weekly_Projects"
    fname = f"Week_{n:02d}_Project{'_Solution' if solution else ''}.docx"
    out = os.path.join(ROOT, folder, fname)
    doc.save(out)
    print(f"WROTE {out}")


SOLUTION_SKETCHES = {
    1: {
        "intro": "A clean reference solution is ~250 lines of Python. The hardest part is making the eval honest.",
        "sections": [
            ("Architecture", "Single ReAct loop with a tool dispatcher. Iteration cap 8. Per-iteration log line in JSONL."),
            ("Eval design", "30 questions covering: pure lookup (10), multi-step (10), invalid-question refusal (5), out-of-scope refusal (5). Gold answers are exact-match or rubric-judged."),
            ("Gotchas", "Tool-call schema enforcement at the LLM level (JSON mode or tool-call). Failure to enforce causes 30% of common bugs."),
        ],
        "code": (
            "def react_loop(question, max_iter=8):\n"
            "    history = []\n"
            "    for step in range(max_iter):\n"
            "        action = llm.next_action(question, history)\n"
            "        if action.is_final():\n"
            "            return action.answer, step + 1\n"
            "        result = TOOLS[action.name](**action.args)\n"
            "        history.append((action, result))\n"
            "    return None, max_iter\n"
        ),
        "failures": [
            "Iteration cap missing or too low (turns 'tough question' into 'failure').",
            "Tool args validated by the LLM only (no schema check on the Python side).",
            "Eval set written after the agent (selection bias).",
        ],
    },
    2: {
        "intro": "Pattern is straightforward; the design effort is in the rubric the Critic uses.",
        "sections": [
            ("Architecture", "LangGraph nodes: Planner, Worker, Critic, Compose. Critic has a 5-item rubric and returns structured reasons on reject."),
            ("State schema", "TypedDict with question, plan (list), drafts (list), critique (Optional), final (Optional)."),
            ("Gotchas", "Critic that always accepts becomes a rubber stamp. Force a minimum-rejection rate during evaluation."),
        ],
        "failures": [
            "Critic accepts everything; eval has no signal.",
            "Compose node concatenates instead of synthesizing.",
            "Checkpoint store is in-memory (loses on crash).",
        ],
    },
    3: {
        "intro": "Tool design is the project. OAuth flow is more code than the tools themselves.",
        "sections": [
            ("Architecture", "FastMCP server with three @app.tool() functions. OAuth handled by an auth middleware that injects scoped tokens into the calendar tool only."),
            ("Tool docstrings", "Include argument types in ISO format, expected exceptions, and example calls."),
            ("Gotchas", "Token expiry handling. Refresh before the call, not in the error path."),
        ],
        "code": (
            "@app.tool(scopes=['calendar.read'])\n"
            "def list_events(start: date, end: date) -> list[dict]:\n"
            "    '''List calendar events in [start, end] inclusive.'''\n"
            "    token = ctx.token('calendar')\n"
            "    return calendar_api(token).list(start, end)\n"
        ),
        "failures": [
            "Hard-coded OAuth callback URL (breaks in deploy).",
            "Token refresh on error instead of pre-call.",
            "Returning raw exceptions instead of structured errors.",
        ],
    },
    4: {
        "intro": "Beating the baseline is the bar. The win usually comes from MIPRO finding non-obvious demonstrations.",
        "sections": [
            ("Baseline design", "Carefully written CO-STAR prompt with 3-5 diverse few-shot examples including a refusal."),
            ("DSPy design", "Signature with 7 labels + 'none'. ChainOfThought module. MIPRO with 50 candidate trials."),
            ("Gotchas", "Train/eval split contamination. Use a held-out set that MIPRO never sees."),
        ],
        "failures": [
            "Baseline too weak (artificially inflates the win).",
            "MIPRO budget too small (no improvement).",
            "Eval contaminated by training set.",
        ],
    },
    5: {
        "intro": "Reference solution shows full FT marginally winning quality but losing on cost/time. qLoRA is the practical default.",
        "sections": [
            ("Method matrix", "Full FT: highest quality, 8x GPU hours, 80GB peak. LoRA: 99% of quality, 1x time, 30GB peak. qLoRA: 97% of quality, 1.2x time, 14GB peak."),
            ("Eval", "50 instructions rated by an LLM judge against a rubric. Inter-rater agreement spot-checked."),
            ("Gotchas", "Inference latency includes adapter merge cost; bake LoRA into the base for prod."),
        ],
        "failures": [
            "Different hyperparameters across runs (apples to oranges).",
            "Forgot to set the same seed (variance dominates the signal).",
            "Eval too small to detect a 2-point difference.",
        ],
    },
    6: {
        "intro": "Reward shaping cuts wallclock to convergence by ~3x in the reference. Be honest about the shaping signal.",
        "sections": [
            ("Env", "10x10 with 15% obstacles, goal moves every 50 steps, observation is a 5x5 window around the agent."),
            ("Shaping", "Distance-to-goal potential function (Ng-Russell, well-defined potential keeps the optimal policy unchanged)."),
            ("Gotchas", "Bad shaping changes the optimal policy. Stick to potential-based shaping."),
        ],
        "failures": [
            "Non-potential shaping (changes optimal policy silently).",
            "PPO without entropy bonus (policy collapses to one action).",
            "Plot includes wallclock without averaging across seeds.",
        ],
    },
    7: {
        "intro": "GRPO wins on cost; DPO wins on simplicity; PPO wins on multi-turn quality. Document which matters for your task.",
        "sections": [
            ("Setup", "Same base model, same preference data, same eval. Three checkpoints, one trace per method."),
            ("Eval", "Pairwise win rate against base, judged by a separate LLM."),
            ("Gotchas", "DPO beta default (0.1) is not always right. Sweep at least 3 values."),
        ],
        "failures": [
            "Single beta for DPO (luck dominates the result).",
            "GRPO with group size 2 (advantage estimates too noisy).",
            "Eval judge is the same model as the policy (collusion).",
        ],
    },
    8: {
        "intro": "Bringing this together is mostly plumbing. The valuable artifacts are the canary policy and the rollback log.",
        "sections": [
            ("Serving stack", "vLLM (continuous batching) behind Ray Serve (autoscaling). OpenTelemetry exporter on every layer."),
            ("Airflow DAG", "extract -> features -> train -> eval -> gate -> deploy with explicit retry, alert, and timeout per task."),
            ("Gotchas", "Canary metric window too short -> false promotion. Use at least 30 minutes of traffic."),
        ],
        "failures": [
            "No rollback path (must rebuild prior version manually).",
            "Canary promoted on a single point estimate.",
            "Traces only at the top layer (cannot diagnose internal bottlenecks).",
        ],
    },
    9: {
        "intro": "The protocol is the project. Implementation is straightforward; the security argument is the artifact.",
        "sections": [
            ("Two ends", "ADK agent exposes A2A endpoint. Custom Python client uses async HTTP + JWT signing."),
            ("Discovery", "Registry stores Agent Cards as JSON. Both ends POST their cards on startup, GET to discover."),
            ("Gotchas", "Token TTL too long (longer-lived tokens = bigger blast radius)."),
        ],
        "failures": [
            "mTLS without scope checks (auth without authz).",
            "Registry as single point of failure (no caching client-side).",
            "Discovery on every call (latency hit).",
        ],
    },
    10: {
        "intro": "The artifact is the comparison. Pick a task where the three patterns produce different numbers, not similar ones.",
        "sections": [
            ("Task choice", "Pick something with both simple and hard inputs. Code review and competitive analysis both work."),
            ("Numbers", "Router wins on cost; Orchestrator wins on quality; Evaluator-Optimizer wins on quality but at 4x cost."),
            ("Gotchas", "Picking a task that does not differentiate the patterns (everything looks the same)."),
        ],
        "failures": [
            "Same task across patterns but different eval (incomparable).",
            "Evaluator-Optimizer with no stop condition (runs forever).",
            "Cost numbers exclude critic/orchestrator overhead.",
        ],
    },
    11: {
        "intro": "Student outperforms teacher on cost; teacher wins on hardest questions. The recommendation depends on tail behavior.",
        "sections": [
            ("RAG flow", "Router classifies query type -> {vector, BM25, SQL}. Vector path uses HyDE."),
            ("Trajectory training", "Keep top 30% of teacher runs by verifier score. Train 1B student with Agent Lightning."),
            ("Gotchas", "Student inherits teacher's biases. Add explicit diversity to the trajectory mix."),
        ],
        "failures": [
            "Vector-only retrieval (BM25 still helps).",
            "Trajectory filter too aggressive (small training set).",
            "Student never evaluated on tail (cost claim looks better than reality).",
        ],
    },
    12: {
        "intro": "Capstones vary widely. The rubric prioritizes honesty about limits over polish.",
        "sections": [
            ("Architecture", "Documented at the OSI-layer level. Patterns labeled explicitly."),
            ("Eval", "At least 50 examples; held-out from anything that touched training."),
            ("Reflection", "One concrete decision the team would make differently and why."),
        ],
        "failures": [
            "Demo polished, eval thin.",
            "No observability (cannot prove the claims).",
            "Reflection is generic, not specific to the project.",
        ],
    },
}


if __name__ == "__main__":
    for w in WEEKS:
        build_project(w, solution=False)
        build_project(w, solution=True)
