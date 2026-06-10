"""Generate research paper reading guides (one per week)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from helpers import (
    new_doc, add_title, add_subtitle, add_h1, add_h2, add_h3, add_body,
    add_bullet, add_divider, add_footer_brand,
)
from bootcamp_content import WEEKS, slug

ROOT = "/Users/pkr465/work/AI-Course-Material/AI_Agents_and_Advanced_Fine_Tuning_Bootcamp"

READING_NOTES = {
    1: {
        "framing": "These two papers established the agentic loop as a research object. Read ReAct first; then Toolformer for how tool-use signal can be self-supervised.",
        "questions": [
            "What was the dominant alternative to ReAct when it was published, and why did interleaved reasoning win?",
            "Toolformer self-supervises. Identify a failure mode of that supervision that you would expect.",
            "How would you modify ReAct for tasks where reasoning is far cheaper than action?",
        ],
    },
    2: {
        "framing": "Reflexion shows verbal RL works without gradient updates. AutoGen establishes the engineering vocabulary for multi-agent dialogue.",
        "questions": [
            "Reflexion treats verbal feedback as implicit reward. Where does that break down?",
            "AutoGen's conversation pattern is general. When would role-based be a poor fit?",
            "Design a hybrid: Reflexion-style critique inside an AutoGen team. What changes?",
        ],
    },
    3: {
        "framing": "Read the MCP spec like a paper: identify the design tradeoffs. Then Gorilla for empirical limits on tool selection.",
        "questions": [
            "MCP keeps capability negotiation per-session, not per-call. What does this rule out?",
            "Gorilla shows tool-selection accuracy degrades with catalog size. Sketch a mitigation that preserves single-agent simplicity.",
            "Where does the MCP design choice of JSON-RPC over a custom binary format cost you?",
        ],
    },
    4: {
        "framing": "DSPy reframes prompts as programs. GEPA brings evolutionary search; TextGrad brings gradients. Read all three for the contrast.",
        "questions": [
            "DSPy's compile step is one-shot. When would streaming optimization be better?",
            "GEPA uses an LLM critic as the mutation operator. What is the cost-benefit relative to random mutation?",
            "TextGrad's gradients are textual. Sketch a case where the gradient is misleading.",
        ],
    },
    5: {
        "framing": "LoRA is the original PEFT classic; QLoRA adds quantization. Chinchilla is the scaling law every fine-tuner needs.",
        "questions": [
            "LoRA's key insight is rank deficiency of weight updates. Where does this assumption fail?",
            "QLoRA uses NF4 quantization. Why is INT8 the wrong default?",
            "Chinchilla's recommendation is compute-optimal, not deployment-optimal. When do they diverge?",
        ],
    },
    6: {
        "framing": "PPO is the workhorse, DPO is the cheap modern alternative, GRPO is the production-friendly hybrid. Read all three; the differences are the whole point.",
        "questions": [
            "PPO's clip vs TRPO's hard KL: empirically what is the cost in sample efficiency?",
            "DPO derives its loss from the optimal RLHF policy. Identify an assumption that breaks in practice.",
            "GRPO's group-relative advantage works without a value head. Where does the value head still help?",
        ],
    },
    7: {
        "framing": "Constitutional AI shows AI-generated preferences scale further than human ones. Deep-read the GRPO portion of DeepSeekMath this week.",
        "questions": [
            "Constitutional AI generates preferences from a constitution. Pick a constitution clause that would be hard to operationalize.",
            "GRPO's group size affects variance. Derive a heuristic for picking it.",
            "If you had no preference data, would you reach for Constitutional AI or for RLVR? Why?",
        ],
    },
    8: {
        "framing": "Ray's foundational paper still reads well. vLLM's PagedAttention is the most important inference-side paper of the last two years.",
        "questions": [
            "Ray's distinction between tasks and actors maps to which classical CS concept?",
            "PagedAttention borrows from OS virtual memory. What is the analog of a page fault?",
            "Why does continuous batching enable higher throughput without higher latency?",
        ],
    },
    9: {
        "framing": "Debate is older than A2A but the design pressure is similar. Read both with an eye to incentive structures.",
        "questions": [
            "Irving et al. assume the judge is weaker than the debaters. When is this assumption right?",
            "A2A handshake patterns mirror older RPC protocols. What did they get right that A2A could borrow?",
            "Sketch a discovery protocol that does not require a central registry.",
        ],
    },
    10: {
        "framing": "Building Effective Agents is the production catalog. The Bitter Lesson is the counterweight: do not over-architect.",
        "questions": [
            "Which Anthropic patterns survive the Bitter Lesson? Which ones do not?",
            "Pick a pattern from the catalog and identify the failure mode the Bitter Lesson predicts.",
            "Apply ruthless simplification to a system you have shipped. List five components you would delete.",
        ],
    },
    11: {
        "framing": "HyDE is small and elegant; Self-RAG is bigger and more ambitious; Agent Lightning ties it back to training.",
        "questions": [
            "HyDE adds one LLM call per query. When is the latency hit unacceptable?",
            "Self-RAG adds critique tokens to the vocabulary. What does this rule out for some deployments?",
            "Agent Lightning trains on trajectories. Identify the smallest student that still benefits.",
        ],
    },
    12: {
        "framing": "RLVR is the newest of these and changes the cost equation for many tasks. MARL is older but still under-applied.",
        "questions": [
            "Which production tasks are good RLVR fits today? Pick three and justify.",
            "CTDE (centralized training, decentralized execution) is the MARL default. When does fully decentralized training make sense?",
            "What is one thing you will read next from the alumni reading list, and why?",
        ],
    },
}


def build_one(week):
    n = week["num"]
    doc = new_doc()
    add_title(doc, f"Week {n} Research Paper Reading Guide", size=22)
    add_subtitle(doc, week["title"], size=14)
    add_subtitle(doc,
                 "Read before Sunday's main session. Discussion lead rotates weekly.",
                 size=11)
    add_divider(doc)

    add_h1(doc, "Framing for This Week")
    add_body(doc, READING_NOTES[n]["framing"])

    add_h1(doc, "Papers")
    for ptitle, pnote in week["papers"]:
        add_h2(doc, ptitle)
        add_body(doc, pnote)
        add_h3(doc, "What to look for")
        add_bullet(doc, "Main claim in one sentence.")
        add_bullet(doc, "The experimental setup that supports the claim.")
        add_bullet(doc, "The one assumption you would challenge.")
        add_bullet(doc, "How the paper relates to this week's lab work.")

    add_h1(doc, "Discussion Questions")
    for q in READING_NOTES[n]["questions"]:
        add_bullet(doc, q)

    add_h1(doc, "Presenter Notes")
    add_body(doc,
        "The assigned presenter for this week leads a 15-minute walkthrough of "
        "one paper, followed by 20 minutes of group discussion against the "
        "questions above. Slides optional. Strong opinions welcome.")

    add_h1(doc, "Submission")
    add_bullet(doc, "Each student submits a 200-word reflection on Discord by Saturday EOD.")
    add_bullet(doc, "Reflections feed into the Sunday discussion and the Wednesday quiz.")

    add_divider(doc)
    add_footer_brand(doc)

    fname = f"Week_{n:02d}_Paper_Reading_{slug(week)}.docx"
    out = os.path.join(ROOT, "Research_Papers", fname)
    doc.save(out)
    print(f"WROTE {out}")


if __name__ == "__main__":
    for w in WEEKS:
        build_one(w)
