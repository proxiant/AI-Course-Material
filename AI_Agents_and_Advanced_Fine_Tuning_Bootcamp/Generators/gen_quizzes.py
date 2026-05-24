"""Generate weekly quizzes (questions only) and solutions."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import (
    new_doc, add_title, add_subtitle, add_h1, add_h2, add_body,
    add_bullet, add_numbered, add_divider,
)
from bootcamp_content import WEEKS
from quiz_bank import QUIZZES

ROOT = "/Users/pkr465/work/AI-Course-Material/AI_Agents_and_Advanced_Fine_Tuning_Bootcamp"
LETTERS = ["A", "B", "C", "D"]


def build_quiz(week, with_answers=False):
    n = week["num"]
    doc = new_doc()
    qz = QUIZZES[n]

    suffix = " — Answer Key" if with_answers else ""
    add_title(doc, f"Week {n} Quiz{suffix}", size=22)
    add_subtitle(doc, week["title"], size=14)
    add_subtitle(doc, "Wednesday 8:30 to 10:00 AM PST | 30 minutes | 60 points", size=11)
    add_divider(doc)

    add_h1(doc, "Instructions")
    add_body(doc, "12 multiple-choice questions (3 points each) and 3 short-answer "
                  "questions (8 points each). Closed-notes for the MCQ portion; "
                  "short answers may reference the class notes.")

    add_h1(doc, "Part A: Multiple Choice")
    for i, (q, options, ans, expl) in enumerate(qz["mcq"], 1):
        add_h2(doc, f"Q{i}. {q}")
        for j, opt in enumerate(options):
            marker = LETTERS[j]
            text = f"{marker}. {opt}"
            if with_answers and j == ans:
                text += "   [correct]"
            add_bullet(doc, text)
        if with_answers:
            add_body(doc, f"Explanation: {expl}")

    add_h1(doc, "Part B: Short Answer")
    for i, sq in enumerate(qz["short"], 1):
        add_h2(doc, f"S{i}. {sq}")
        if with_answers:
            add_body(doc, model_answer(n, i))
        else:
            add_body(doc, "(Write 3 to 6 sentences in the space below.)")

    folder = "Weekly_Quizzes"
    fname = f"Week_{n:02d}_Quiz{'_Solution' if with_answers else ''}.docx"
    out = os.path.join(ROOT, folder, fname)
    doc.save(out)
    print(f"WROTE {out}")


SHORT_ANSWERS = {
    (1, 1): "An agent has a persistent goal, perceives an environment, selects from a discrete action space, and has a termination condition that is not user cancellation. A pure chat call lacks the goal persistence and tool-action loop.",
    (1, 2): "Static pipeline; retrieval-augmented call; tool-using single agent; multi-agent. For a simple FAQ-style internal bot, rung two (RAG over the knowledge base) is enough; the agent loop adds latency and failure modes without quality gain.",
    (1, 3): "Sandbox all fetched content as untrusted data; never let fetched text become an instruction; cap iterations; log every tool call; alert on anomalies (unexpected domains, sudden tool changes); rotate credentials regularly.",

    (2, 1): "Scratchpad: current ticket reasoning, cleared on send. Session: this customer's session, cleared on logout. Semantic: this customer's history and preferences, persists across sessions.",
    (2, 2): "Planner emits sub-tasks (find filing, extract MD&A, summarize risk factors, draft report). Worker runs each. Critic verifies coverage against a rubric; rejection loops back to the worker with a specific issue.",
    (2, 3): "Eviction policies conflict (scratchpad evicts on send, semantic never evicts). Retrieval costs balloon (semantic similarity over scratchpad is wasteful). Privacy boundaries blur (semantic memory leaks into other sessions).",

    (3, 1): "Use Pydantic-style type hints. Docstring should specify behavior, expected inputs (with examples), exception types, and return shape. For a calendar lookup: explicit timezone, ISO 8601 dates, error semantics for missing IDs.",
    (3, 2): "stdio: lowest latency for local subprocess, simplest to deploy, no auth needed but limited to local. HTTP: works across machines, supports OAuth, more complex (load balancer, TLS), higher latency. Choose stdio for IDE-style tools, HTTP for shared services.",
    (3, 3): "Client generates a UUID per send_email request and stores it locally. Server keeps a (key, message_id) table with TTL of 24 hours. Retries with the same key return the stored message_id; new keys send. Garbage-collect old entries on schedule.",

    (4, 1): "Context: HR policies for US/EU employees. Objective: answer FAQs accurately or escalate. Style: professional. Tone: warm but precise. Audience: employees with HR questions. Response: short answer plus the source policy reference, refuse if outside policy scope.",
    (4, 2): "Define signature (text -> label in {A,B,C}). Build module (ChainOfThought). Provide training data with labels. Run MIPRO with accuracy metric. MIPRO searches instructions and demonstrations jointly; report best compiled program.",
    (4, 3): "TextGrad excels when refining an existing prompt with concrete failure cases (the critic supplies targeted gradients). Struggles when starting from scratch (no signal to compute gradients against) and on tasks where the critic itself is the bottleneck.",

    (5, 1): "20 tokens per parameter is the Chinchilla optimum. 1B parameters and 20B tokens is exactly compliant. Deviation justified only if downstream task is narrow and over-training a smaller model improves transfer specifically for the target.",
    (5, 2): "Rank 16, alpha 32, target Q/V/O projections. Domain adaptation requires moderate capacity for semantic shifts; 16 is the practical default. Consider including MLP target if the domain has unusual syntactic patterns.",
    (5, 3): "Pull positive (query, code) pairs from a labeled subset. Mine hard negatives via BM25 high-overlap but wrong intent. Refresh negatives every epoch to prevent the model from memorizing them.",

    (6, 1): "Start from E[grad log pi(a|s) * Q(s,a)]. Use importance sampling for off-policy. Clip the importance ratio to [1-eps, 1+eps] to bound updates. Take min(clipped, unclipped) * advantage to keep the surrogate pessimistic.",
    (6, 2): "DPO: lower data needs (preferences only), no sampling at training, simpler implementation, less expressive for multi-turn. PPO: needs reward model or signal, on-policy sampling, more expressive but harder to stabilize.",
    (6, 3): "User asks for synthesis of an explosive. Helpful pushes toward answering; harmless toward refusal. Resolve via tiered refusal: refuse the operative content but explain why and offer safer alternatives (chemistry resources for legitimate education).",

    (7, 1): "Three remedies: lower learning rate, increase KL coefficient, reduce batch size to slow updates. Inspect reward distribution for hacking. Verify reference model is loaded correctly and is the same as base.",
    (7, 2): "An internal SQL-explainer with 40 tools (one per metric). Multi-agent adds coordination cost; tool-maximalist measured 3x lower latency and 2x lower cost at equal quality. The selection bandwidth held because tool names were highly distinguishable.",
    (7, 3): "Epistemic: model has not seen recent fraud patterns from a new payment method. More labeled data fixes it. Aleatoric: identical legitimate and fraudulent transactions differ only by intent (genuinely unobservable). Calibrate probability outputs; the model cannot become more confident than the underlying signal allows.",

    (8, 1): "Hybrid: tensor parallel within each node (8-way), pipeline parallel across nodes (2-way), data parallel for replication. Allows 70B with reasonable memory headroom and uses inter-node bandwidth efficiently.",
    (8, 2): "Min replicas 2 (always-on), max replicas 16. Scale-up trigger: average concurrent requests per replica > 4 for 30 seconds. Scale-down: < 1 for 5 minutes. Use Ray Serve's autoscaling config; tie metrics to OpenTelemetry.",
    (8, 3): "extract (pull from data lake) -> features (Spark step) -> train (Ray Train) -> eval (gated on F1 > baseline + 0.5pp) -> deploy (canary 5%, promote on 24h health). Each task has retries, alerts, and explicit timeouts.",

    (9, 1): "Card fields: name, version, capabilities ('competitor_summary', 'market_size_estimate'), cost ($0.20 fixed), latency (P50: 12s, P95: 30s), inputs (company URL, market), outputs (Markdown report), auth (OAuth 2.1), contact (email).",
    (9, 2): "Nanda: federated, low operational burden, low identity guarantees. Cisco Agency: central identity, higher trust, requires authority buy-in. Many production systems start Nanda for breadth, migrate to Agency for sensitive contexts.",
    (9, 3): "Rolling certificate authority issuance with overlapping validity windows. Clients accept both old and new CAs during transition. Use short-lived (24h) leaf certs. Automate rotation via cert-manager or similar; never manual.",

    (10, 1): "Delete: dead-code endpoints, duplicate logging, unused feature flags, optimization layers that never fire, defensive try-except blocks around code that cannot fail. Each deletion reduces failure surface.",
    (10, 2): "Router: classify into 'security review' or 'style review', dispatch to specialist. Fan-out: run both reviewers in parallel and merge. Fan-out wins on code where both dimensions matter; router wins when one dimension clearly dominates and latency matters.",
    (10, 3): "Failed tool call returned ambiguous error. OSI model: tool returned at execution layer; capability layer did not flag the failure; planning layer assumed success; the bug was at the capability layer's error contract.",

    (11, 1): "Query: 'How did Apple's R&D investment in 2023 compare to its product launch cadence?' Plan: fetch Apple 10-K 2023 -> extract R&D figures -> fetch IR press releases for launches -> count launches by quarter -> draft synthesis.",
    (11, 2): "Helps: highly technical queries where the question vocabulary differs from document vocabulary (e.g. clinical 'tachycardia' vs colloquial 'fast heartbeat'). Does not help: simple keyword lookups where query and docs already share vocabulary.",
    (11, 3): "schema: task_id, step_id, state(snapshot), action(tool_name, args), observation(result_or_error), reward(verifier_pass_fail), tokens_consumed, latency_ms.",

    (12, 1): "Task: customer service tone shift. RAG: no, retrieval cannot change tone. SFT with a small style corpus: yes, this is the right rung. RL: only if SFT does not consistently maintain the tone across contexts.",
    (12, 2): "Generate SQL. Verifier: execute against test DB, compare result rows to gold. Reward 1 for match, 0 for mismatch or runtime error. Penalty -0.1 for cost > budget. Augment with style penalty for unsafe patterns (no WHERE clause).",
    (12, 3): "Five tests: PII leakage probe, jailbreak via roleplay, sensitive topic refusal calibration, hallucinated source citation, harmful-instruction refusal. Each runs on every release; failure blocks deploy.",
}


def model_answer(week_num, q_num):
    return SHORT_ANSWERS.get((week_num, q_num),
                             "Model answer is reviewed live in the Wednesday quiz session.")


if __name__ == "__main__":
    for w in WEEKS:
        build_quiz(w, with_answers=False)
        build_quiz(w, with_answers=True)
