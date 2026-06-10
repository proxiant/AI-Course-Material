"""Deep technical content per week for class notes. Keep prose plain and direct."""

DEEP = {
    1: {
        "intro": (
            "Today opens the bootcamp. The goal is not to teach you what an LLM is. "
            "The goal is to draw a sharp line between a model that answers and a "
            "program that acts. That program is what we will call an agent for the "
            "next twelve weeks. Everything else in the course depends on the "
            "definitions we lock in today."
        ),
        "sections": [
            {
                "h": "1. The shape of an agent",
                "body": (
                    "An agent has four properties that distinguish it from a "
                    "chat call. First, it has a goal that persists across turns. "
                    "Second, it acts in an environment that returns observations. "
                    "Third, it selects from a discrete action space (tool calls, "
                    "sub-tasks, refusals). Fourth, it has a termination condition "
                    "that is not 'the user pressed stop'. Strip any of these out "
                    "and you have a pipeline, not an agent."
                ),
                "code": (
                    "while not done:\n"
                    "    observation = perceive(state)\n"
                    "    plan = llm.plan(goal, observation, memory)\n"
                    "    if plan.is_final():\n"
                    "        done = True\n"
                    "        result = plan.answer\n"
                    "    else:\n"
                    "        action = plan.next_action\n"
                    "        outcome = tools[action.name](action.args)\n"
                    "        memory.append((action, outcome))\n"
                    "        state = update(state, outcome)\n"
                ),
            },
            {
                "h": "2. Autonomy is a dial, not a switch",
                "body": (
                    "Autonomy ranges from suggest-only (the agent proposes, a human "
                    "approves each step) to fully autonomous with audit (no human "
                    "in the loop, but every action is logged for review). The "
                    "right point on this dial is determined by three numbers: the "
                    "cost of a wrong action, the cost of human review, and the "
                    "frequency of edge cases. Most production systems sit between "
                    "approve-batches and approve-on-anomaly."
                ),
            },
            {
                "h": "3. The escalation ladder",
                "body": (
                    "Before reaching for an agent, walk the ladder. Rung one: a "
                    "static pipeline with deterministic steps. Rung two: a "
                    "retrieval-augmented single call. Rung three: a tool-using "
                    "single agent. Rung four: a multi-agent system. Each rung "
                    "trades determinism for capability. Stop at the lowest rung "
                    "that solves the problem. The number one mistake in agent "
                    "engineering is starting at rung four."
                ),
            },
            {
                "h": "4. Failure modes that bite first",
                "body": (
                    "Prompt injection through tool outputs is the easiest to "
                    "underestimate. If your agent reads a web page, that web page "
                    "can issue instructions. Sandboxing is not a flag, it is a "
                    "discipline. Context overflow is the second. Long-running "
                    "agents accumulate observations until the context window "
                    "saturates. Have an explicit eviction strategy from day one. "
                    "Runaway loops are the third. Cap iterations. Always."
                ),
            },
            {
                "h": "5. Security boundaries",
                "body": (
                    "Three boundaries matter. The credential boundary: tool "
                    "credentials live in a secret manager, not in the prompt. The "
                    "data boundary: the agent should not see data it has no "
                    "business seeing, even temporarily. The action boundary: "
                    "destructive tools require explicit confirmation, even from "
                    "an autonomous agent."
                ),
            },
            {
                "h": "6. Today's lab in context",
                "body": (
                    "By the end of the day every student will (a) have a working "
                    "session on the Proxiant Ray cluster, with GPU allocation "
                    "verified, and (b) have built a tool-using agent in n8n that "
                    "chooses between three tools on real input. Tomorrow's quiz "
                    "covers both."
                ),
            },
        ],
        "review": [
            "Name the four properties of an agent and give a one-sentence counter-example for each.",
            "On the escalation ladder, when does a single tool-using agent beat orchestrator-workers?",
            "Sketch a defense against prompt injection through a fetched web page.",
            "Why is iteration capping non-negotiable?",
        ],
    },
    2: {
        "intro": (
            "We move from one agent to teams of agents. The interesting design "
            "questions arrive: who decides, who executes, who critiques, and what "
            "the protocol between them looks like. Memory becomes a first-class "
            "concern. Agentic RAG appears for the first time."
        ),
        "sections": [
            {
                "h": "1. Reasoning workflows as programs",
                "body": (
                    "Chain-of-thought is a prompting trick that helps the model "
                    "think out loud. A reasoning workflow is a program: each "
                    "step has typed inputs, typed outputs, an associated tool, "
                    "and a verification rule. The verification rule is what "
                    "makes the workflow auditable. Without it you have a black "
                    "box that occasionally hallucinates."
                ),
            },
            {
                "h": "2. Top-down vs bottom-up decomposition",
                "body": (
                    "Top-down: a planner emits the full task tree before any "
                    "worker runs. Bottom-up: each worker discovers sub-tasks as "
                    "it goes. Top-down is observable and predictable. Bottom-up "
                    "handles tasks where the structure is unknown ahead of time. "
                    "Most production systems are hybrid: top-down for the "
                    "outer loop, bottom-up inside leaves."
                ),
            },
            {
                "h": "3. Memory as architecture",
                "body": (
                    "Treat memory as three stores with different lifetimes. "
                    "Scratchpad memory lasts one turn. Session memory lasts one "
                    "conversation. Semantic memory lasts forever. Each has a "
                    "different eviction policy, different retrieval strategy, "
                    "and different cost profile. Most failures we see in the "
                    "field come from collapsing all three into one store."
                ),
                "code": (
                    "class MemoryStack:\n"
                    "    scratchpad: List[Turn]      # cleared on response\n"
                    "    session:    DurableLog      # cleared on session end\n"
                    "    semantic:   VectorStore     # cleared by policy\n"
                    "\n"
                    "    def recall(self, query):\n"
                    "        return (self.scratchpad,\n"
                    "                self.session.recent(50),\n"
                    "                self.semantic.search(query, k=8))\n"
                ),
            },
            {
                "h": "4. Agentic RAG, the first pass",
                "body": (
                    "Static RAG retrieves once before the model runs. Agentic "
                    "RAG lets the model decide when to retrieve, what to "
                    "retrieve, and whether to retrieve again after a partial "
                    "answer. The cost is latency and tokens. The benefit is "
                    "answers to questions that need multi-hop reasoning."
                ),
            },
            {
                "h": "5. Game theory for multi-agent teams",
                "body": (
                    "When agents share a reward, the system is cooperative and "
                    "the failure mode is freeloading. When agents have private "
                    "rewards, the system is competitive and the failure mode is "
                    "defection. Most real systems are mixed-motive: aligned at "
                    "the goal but competing for shared resources (tokens, "
                    "tools, time). Design the protocol around the motive mix, "
                    "not around the technology."
                ),
            },
            {
                "h": "6. Evaluation rubric: four axes",
                "body": (
                    "Quality (rubric or human judgment). Cost (tokens + tool "
                    "calls). Latency (P50 and P95, never just the mean). Safety "
                    "(refusal correctness, jailbreak resistance, sensitive data "
                    "leakage). Track all four from day one. A system that "
                    "scores well on three and badly on one is not production-"
                    "ready."
                ),
            },
        ],
        "review": [
            "Give an example task where bottom-up decomposition beats top-down.",
            "Why should scratchpad and semantic memory not share an eviction policy?",
            "When does agentic RAG provide no benefit over static RAG?",
            "Define a mixed-motive setting using a multi-agent code review example.",
        ],
    },
    3: {
        "intro": (
            "MCP is the cleanest abstraction in the agent stack right now. Today "
            "we cover the protocol, build a real tool server, and connect it to a "
            "Google ADK agent. The lessons here are also about tool craft, which "
            "is what determines whether agents work in practice."
        ),
        "sections": [
            {
                "h": "1. The MCP architecture",
                "body": (
                    "Three pieces: a server (exposes tools, resources, prompts), "
                    "a client (the agent host, negotiates capabilities at "
                    "startup), and a transport (stdio, HTTP, WebSocket). The "
                    "wire format is JSON-RPC. Capability negotiation happens "
                    "once at the start of the session, so the agent knows what "
                    "is available before it starts planning."
                ),
            },
            {
                "h": "2. FastMCP",
                "body": (
                    "FastMCP wraps the protocol with decorator-style Python. A "
                    "tool is a typed function with a docstring. The schema is "
                    "generated automatically. The developer ergonomics are good "
                    "enough that this is the recommended starting point."
                ),
                "code": (
                    "from fastmcp import FastMCP\n\n"
                    "app = FastMCP('crm-tools')\n\n"
                    "@app.tool()\n"
                    "def lookup_customer(customer_id: str) -> dict:\n"
                    "    '''Look up a customer record by ID. Returns name, plan,\n"
                    "    and last login timestamp. Raises tool_unavailable if\n"
                    "    the CRM is down.'''\n"
                    "    return crm_api.get(customer_id)\n"
                ),
            },
            {
                "h": "3. Tool craft",
                "body": (
                    "Names matter. Use verbs that match user intent. "
                    "Docstrings matter more. The model reads the docstring at "
                    "call time; ambiguity in the docstring produces wrong tool "
                    "calls before any runtime error. Argument names are also "
                    "the prompt. 'date' is bad; 'start_date_iso8601' is good."
                ),
            },
            {
                "h": "4. The tool-use maximalist pattern",
                "body": (
                    "Give one agent every tool you have. It works further than "
                    "people expect, and it is cheaper to operate than a "
                    "multi-agent swarm. The failure mode is the catalog crossing "
                    "the model's selection bandwidth: somewhere between 20 and "
                    "60 tools the model starts confusing similar ones. Measure "
                    "this for your model before committing."
                ),
            },
            {
                "h": "5. AuthN and AuthZ",
                "body": (
                    "OAuth 2.1 with PKCE for user-delegated access. Service-"
                    "account tokens for system tools. Scopes per tool, not per "
                    "server. Token refresh handled in the runtime so the agent "
                    "never sees a credential. Log every consent grant."
                ),
            },
            {
                "h": "6. Errors and idempotency",
                "body": (
                    "Structured error returns (tool_unavailable, invalid_input, "
                    "rate_limited) let the agent reason about whether to retry "
                    "and how to back off. Idempotency keys on writes prevent "
                    "double-execution after retry. These two patterns together "
                    "are the difference between a demo and a production system."
                ),
            },
        ],
        "review": [
            "What does capability negotiation give you that runtime tool calls cannot?",
            "Sketch a tool docstring that minimizes ambiguity for a date-range argument.",
            "When does the tool-use maximalist pattern break down for your model?",
            "Why should idempotency keys be issued by the client, not the server?",
        ],
    },
    4: {
        "intro": (
            "We treat prompts as programs that can be compiled. Start with "
            "hand-crafted prompts (CO-STAR, few-shot, refusal). Then move to "
            "automatic optimization with DSPy. Then to evolutionary approaches "
            "(GEPA, TextGrad, OPRO) that search a much larger space."
        ),
        "sections": [
            {
                "h": "1. CO-STAR as a checklist",
                "body": (
                    "Context (what the model needs to know about the world). "
                    "Objective (what success looks like for this call). Style "
                    "(formal, casual, technical). Tone (calm, urgent, "
                    "neutral). Audience (who reads the output). Response format "
                    "(plain text, JSON, table). Six fields. Skipping any one "
                    "produces predictable failures."
                ),
            },
            {
                "h": "2. Few-shot prompting",
                "body": (
                    "Three to seven examples is the practical sweet spot. "
                    "Diversity beats count. Always include one boundary case "
                    "and one explicit refusal. Recency bias is real: the model "
                    "weights later examples more heavily, so put the most "
                    "representative example last."
                ),
            },
            {
                "h": "3. Hallucination mitigation",
                "body": (
                    "Three families. Grounding: retrieve evidence before the "
                    "answer. Structured output: refuse to emit invalid JSON. "
                    "Self-consistency: sample N answers and vote. Combine all "
                    "three for high-stakes tasks. None of them is a complete "
                    "fix on its own."
                ),
            },
            {
                "h": "4. DSPy: signatures, modules, optimizers",
                "body": (
                    "A Signature defines inputs and outputs. A Module composes "
                    "signatures into a callable. An Optimizer searches over "
                    "instructions and demonstrations. The Compiler freezes the "
                    "result into a deployable program. DSPy is opinionated; the "
                    "payoff is that you stop hand-tuning prompts."
                ),
                "code": (
                    "import dspy\n\n"
                    "class Classify(dspy.Signature):\n"
                    "    '''Classify the input into one of seven categories\n"
                    "    or refuse with 'none_of_the_above'.'''\n"
                    "    text: str = dspy.InputField()\n"
                    "    label: str = dspy.OutputField()\n\n"
                    "classifier = dspy.ChainOfThought(Classify)\n"
                    "optimizer = dspy.MIPRO(metric=accuracy)\n"
                    "compiled = optimizer.compile(classifier, trainset=train)\n"
                ),
            },
            {
                "h": "5. COPRO vs MIPRO",
                "body": (
                    "COPRO does coordinate ascent on instructions. Fast, "
                    "shallow. MIPRO jointly optimizes instructions and "
                    "demonstrations using Bayesian search. Slower, deeper. "
                    "Start with COPRO; promote to MIPRO when the gain plateaus."
                ),
            },
            {
                "h": "6. Prompt optimizers: GEPA, TextGrad, OPRO",
                "body": (
                    "GEPA is genetic with reflection: an LLM critiques each "
                    "candidate before mutation. TextGrad treats text as a "
                    "tensor and uses a critic LLM as the gradient. OPRO uses "
                    "an LLM as the optimizer: it reads the trajectory of "
                    "prior prompts and their scores, then proposes better "
                    "prompts. Each fits a different stage of the lifecycle: "
                    "GEPA for exploration, TextGrad for refinement, OPRO for "
                    "iterative scored search. A note on naming: ORPO unifies "
                    "preference optimization with reference-free training, "
                    "but ORPO itself is a preference fine-tuning method "
                    "(weights, not prompts); it pairs with DPO in Week 6."
                ),
            },
        ],
        "review": [
            "Write a CO-STAR specification for a tax-question answering agent.",
            "Why does recency bias argue for putting the canonical example last?",
            "When does COPRO suffice and when do you reach for MIPRO?",
            "Give a task where GEPA beats DSPy MIPRO. Why?",
        ],
    },
    5: {
        "intro": (
            "First fine-tuning week. We start with embeddings and contrastive "
            "objectives because every retrieval system depends on them. Then "
            "Chinchilla scaling for sizing decisions. Then the PEFT family with "
            "an emphasis on LoRA and qLoRA. The lab does a real three-way "
            "comparison: full FT, LoRA, qLoRA."
        ),
        "sections": [
            {
                "h": "1. Embedding geometry",
                "body": (
                    "An embedding is a point in a high-dimensional vector "
                    "space. The geometry is what gets used downstream: cosine "
                    "similarity for retrieval, k-means for clustering, "
                    "classifiers on top for classification. The objective you "
                    "train with shapes the geometry. Pick the objective with "
                    "the downstream use in mind."
                ),
            },
            {
                "h": "2. Contrastive objectives",
                "body": (
                    "Triplet loss uses an anchor, a positive, a negative, and "
                    "a margin. Simple but sensitive to triplet mining. InfoNCE "
                    "uses one positive and a batch of negatives, with a "
                    "softmax over similarities. Stable and the modern default. "
                    "SimCLR is InfoNCE with augmentation-derived positives, "
                    "useful when labels are scarce."
                ),
            },
            {
                "h": "3. Chinchilla scaling",
                "body": (
                    "For a fixed compute budget, optimal model size and "
                    "training tokens scale together at roughly 20 tokens per "
                    "parameter. A 7B model wants about 140B tokens. Knowing "
                    "your token budget tells you the right model size. "
                    "Over-trained smaller models often beat under-trained "
                    "larger ones."
                ),
            },
            {
                "h": "4. LoRA mechanics",
                "body": (
                    "Freeze W. Add a low-rank update BA where A is r-by-d, B "
                    "is d-by-r, and r is small (4 to 64 in practice). The "
                    "forward becomes Wx + alpha/r * BAx. Train only A and B. "
                    "Recover near-full-precision performance on most "
                    "downstream tasks with 0.5% to 2% of the trainable "
                    "parameters."
                ),
                "code": (
                    "from peft import LoraConfig, get_peft_model\n\n"
                    "config = LoraConfig(\n"
                    "    r=16, lora_alpha=32,\n"
                    "    target_modules=['q_proj', 'v_proj', 'o_proj'],\n"
                    "    lora_dropout=0.05,\n"
                    "    task_type='CAUSAL_LM',\n"
                    ")\n"
                    "model = get_peft_model(base_model, config)\n"
                ),
            },
            {
                "h": "5. Rank allocation",
                "body": (
                    "Higher rank helps when the task changes semantics "
                    "(domain shift, new language). Lower rank suffices for "
                    "style and format changes. Per-layer rank schedules "
                    "(higher in middle layers) sometimes beat uniform "
                    "allocation but are rarely worth the complexity."
                ),
            },
            {
                "h": "6. qLoRA",
                "body": (
                    "Quantize the base model to 4-bit (NF4 with double "
                    "quantization). Train LoRA adapters in 16-bit on top. "
                    "Memory drops by roughly four times. Accuracy stays within "
                    "1 to 2 points on most tasks. The free lunch is real, "
                    "with caveats: very small base models (under 1B) and very "
                    "long contexts can degrade more than expected."
                ),
            },
            {
                "h": "7. Soft prompting and steering",
                "body": (
                    "Soft prompting trains a small prefix of trainable "
                    "embeddings. Tiny parameter count, narrow control. "
                    "Steering vectors are activation edits at inference time, "
                    "computed from contrastive examples. Cheap, narrow, and "
                    "surprisingly effective for tone."
                ),
            },
        ],
        "review": [
            "Pick a downstream task and choose between Triplet, InfoNCE, and SimCLR. Justify.",
            "Given a 50B-token corpus and 1 GPU-week budget, what model size do you train?",
            "When does LoRA fail to match full fine-tuning, and why?",
            "Why does qLoRA degrade more on long contexts?",
        ],
    },
    6: {
        "intro": (
            "Reinforcement learning week one. Cover MDPs, value and advantage "
            "functions, and the policy gradient family. Then PPO, DPO, and "
            "GRPO. Tie the reward design back to the Helpful, Honest, Harmless "
            "framing. The lab implements value iteration, Q-learning, and PPO "
            "on a gridworld."
        ),
        "sections": [
            {
                "h": "1. MDP formalism applied to LLMs",
                "body": (
                    "State: the current context. Action: the next token (for "
                    "token-level RL) or the next tool call (for high-level "
                    "RL). Reward: sparse, often only at the end of an episode. "
                    "Transition: deterministic given the policy's sampling. "
                    "The formalism feels heavy for LLMs but it is what makes "
                    "the algorithms transferable."
                ),
            },
            {
                "h": "2. Value, Q, and advantage",
                "body": (
                    "V(s) is the expected return from state s under the "
                    "current policy. Q(s,a) is the expected return from "
                    "taking action a in state s. Advantage A(s,a) = Q(s,a) - "
                    "V(s) tells you how much better action a is than the "
                    "policy average. PPO uses A; DPO derives everything "
                    "implicitly and needs none of them."
                ),
            },
            {
                "h": "3. Policy gradients",
                "body": (
                    "The gradient of expected return with respect to policy "
                    "parameters is unbiased but high variance. Variance "
                    "reduction tricks (advantage estimation, baselines, "
                    "trust regions) are the difference between training and "
                    "diverging."
                ),
            },
            {
                "h": "4. PPO",
                "body": (
                    "Replace the hard KL constraint of TRPO with a clipped "
                    "ratio. The clip range (typically 0.2) prevents oversized "
                    "updates. Add a value loss to train V(s) jointly. Add an "
                    "entropy bonus to keep exploration alive. The default "
                    "settings work surprisingly often."
                ),
                "code": (
                    "ratio = exp(log_prob_new - log_prob_old)\n"
                    "obj_clipped = min(ratio * adv,\n"
                    "                  clip(ratio, 1-eps, 1+eps) * adv)\n"
                    "loss = -mean(obj_clipped) + 0.5 * value_loss\n"
                    "       - 0.01 * entropy\n"
                ),
            },
            {
                "h": "5. DPO",
                "body": (
                    "Take the closed-form solution to the RLHF problem and "
                    "rearrange it. The result is a classification loss over "
                    "preference pairs. No reward model, no sampling at "
                    "training time. Cheap and stable. Less expressive than "
                    "PPO for multi-turn tasks."
                ),
            },
            {
                "h": "6. GRPO",
                "body": (
                    "Sample N completions per prompt. Compute their average "
                    "reward and subtract from each. The result is a group-"
                    "relative advantage that does not need a value network. "
                    "Cuts memory roughly in half. Matches PPO on many tasks."
                ),
            },
            {
                "h": "7. Helpful, Honest, Harmless",
                "body": (
                    "Three reward axes. They often pull in different "
                    "directions. Helpful and harmless tension on requests for "
                    "dangerous information. Helpful and honest tension on "
                    "questions where the model does not know the answer. "
                    "Document the tradeoff explicitly in the reward design."
                ),
            },
        ],
        "review": [
            "Why does PPO use the clipped ratio instead of a hard KL constraint?",
            "When would you prefer DPO over PPO? When the opposite?",
            "Sketch a reward that tensions helpful against harmless. Suggest a resolution.",
            "What is the memory advantage of GRPO over PPO, and where does it come from?",
        ],
    },
    7: {
        "intro": (
            "We push from single-agent RL to multi-agent and from gridworld to "
            "actual LLMs. Engineering patterns become real: SRP, facades, "
            "idempotency. We confront the genuine tradeoffs between tool-"
            "maximalist agents and multi-agent architectures."
        ),
        "sections": [
            {
                "h": "1. Single Responsibility Principle for agents",
                "body": (
                    "An agent should do one thing. If you cannot describe its "
                    "responsibility in one sentence, split it. This sounds "
                    "obvious until you see a single 'general assistant' agent "
                    "that holds the entire system together. Such agents are "
                    "untestable and unobservable."
                ),
            },
            {
                "h": "2. Facade agents",
                "body": (
                    "A facade agent wraps a noisy sub-system and presents a "
                    "clean tool to the rest of the team. Useful when a legacy "
                    "API requires multiple calls, retries, and reconciliation. "
                    "The facade hides complexity; the rest of the system "
                    "stays simple."
                ),
            },
            {
                "h": "3. Epistemic vs aleatoric uncertainty",
                "body": (
                    "Epistemic: the model does not know but could learn with "
                    "more data. Aleatoric: the world is genuinely random. "
                    "More data fixes epistemic. Only calibration helps with "
                    "aleatoric. Confusing the two leads to over-collection "
                    "of training data that cannot improve the system."
                ),
            },
            {
                "h": "4. Idempotency is the difference between demo and prod",
                "body": (
                    "Every write tool accepts an idempotency key. Every retry "
                    "with the same key is a no-op if the prior call succeeded. "
                    "Without this, every transient failure becomes a "
                    "double-charge incident waiting to happen."
                ),
            },
            {
                "h": "5. Tool-maximalist vs multi-agent: pick one",
                "body": (
                    "The choice is empirical, not philosophical. Measure both "
                    "on your task: quality, cost, latency, observability. The "
                    "tool-maximalist single agent wins more often than "
                    "engineers expect. Multi-agent wins when responsibilities "
                    "are genuinely separable and the agents have different "
                    "reward functions."
                ),
            },
            {
                "h": "6. PPO on real LLMs",
                "body": (
                    "KL penalty against a reference model is non-negotiable. "
                    "Without it the policy drifts off the manifold and "
                    "reward hacking becomes inevitable. Reward scaling "
                    "matters: scale rewards so the median advantage is order "
                    "of magnitude 1. Use a small enough learning rate (1e-6 to "
                    "5e-6 for 7B models)."
                ),
            },
            {
                "h": "7. GRPO and DPO in practice",
                "body": (
                    "GRPO: sample group size 4 to 8 per prompt. Larger groups "
                    "give better advantage estimates but cost more. DPO: "
                    "beta in 0.05 to 0.2 is the practical range. Lower beta "
                    "follows preferences more aggressively but can overfit."
                ),
            },
        ],
        "review": [
            "Describe a system where SRP failure produced a debugging nightmare.",
            "Give a use case for a facade agent that beats a direct tool integration.",
            "Pick an example of aleatoric uncertainty that a junior engineer might mistake for epistemic.",
            "Why does PPO without KL penalty produce reward hacking?",
        ],
    },
    8: {
        "intro": (
            "Ray is the substrate. Today covers data, tensor, and pipeline "
            "parallelism, then the four Ray subsystems (Train, Tune, Serve, "
            "Core), then vLLM for inference, then Airflow for the full MLOps "
            "loop. The lab serves a fine-tuned model with full observability "
            "and wires the deploy step into Airflow."
        ),
        "sections": [
            {
                "h": "1. Three parallelism strategies",
                "body": (
                    "Data parallel: same model on every device, sharded data, "
                    "all-reduce on gradients. The default for everything that "
                    "fits. Tensor parallel: each matrix multiply is split "
                    "across devices. Needed when the model does not fit on "
                    "one device. Pipeline parallel: model layers split across "
                    "devices, micro-batches stream through. Needed for very "
                    "large models. Mix all three for the largest runs."
                ),
            },
            {
                "h": "2. Ray Core",
                "body": (
                    "Tasks: stateless functions decorated with @ray.remote. "
                    "Actors: stateful classes decorated the same way. Object "
                    "store: a distributed in-memory store that shares "
                    "immutable data zero-copy across workers on the same "
                    "node. The object store is the secret weapon."
                ),
                "code": (
                    "@ray.remote(num_gpus=1)\n"
                    "class Embedder:\n"
                    "    def __init__(self, model_id):\n"
                    "        self.model = load(model_id)\n"
                    "    def embed(self, batch):\n"
                    "        return self.model.encode(batch)\n\n"
                    "actors = [Embedder.remote('bge-large') for _ in range(8)]\n"
                    "futures = [a.embed.remote(b) for a, b in zip(actors, batches)]\n"
                    "results = ray.get(futures)\n"
                ),
            },
            {
                "h": "3. Ray Train",
                "body": (
                    "Wraps PyTorch DDP, FSDP, and Hugging Face Trainer with "
                    "cluster-aware placement, checkpointing, and fault "
                    "tolerance. The right call when you have a multi-node "
                    "training run."
                ),
            },
            {
                "h": "4. Ray Tune",
                "body": (
                    "Hyperparameter search with early stopping. ASHA (async "
                    "successive halving) is the default and works well. "
                    "Population Based Training for schedules that depend on "
                    "training dynamics. Bayesian search for expensive trials."
                ),
            },
            {
                "h": "5. Ray Serve and vLLM",
                "body": (
                    "Ray Serve provides routing, autoscaling, and traffic "
                    "shaping. vLLM provides continuous batching and "
                    "PagedAttention, which together raise throughput 5 to 24 "
                    "times over naive batching. Compose them: Ray Serve in "
                    "front, vLLM as the model server."
                ),
            },
            {
                "h": "6. Airflow MLOps loop",
                "body": (
                    "Pull data. Build features. Train (via Ray Train). "
                    "Evaluate. Gate on metric thresholds. Register the model. "
                    "Deploy behind a canary. Each step is a task, each gate "
                    "is explicit, each deploy is reversible. The DAG is the "
                    "documentation."
                ),
            },
        ],
        "review": [
            "Pick a 70B model and decide on parallelism strategy for 8 A100s.",
            "When does the Ray object store provide no benefit over explicit serialization?",
            "Describe the autoscaling policy you would set for a chat-style workload with bursty traffic.",
            "What gates belong on the deploy edge in the Airflow DAG?",
        ],
    },
    9: {
        "intro": (
            "Agent-to-agent communication is becoming a protocol problem. We "
            "cover A2A, Agent Cards, discovery (Nanda, Cisco's AGNTCY initiative), the "
            "security boundary, and three cooperation protocols (role-based, "
            "voting-based, debate-based). The lab connects Google ADK to a "
            "custom client over A2A with mTLS."
        ),
        "sections": [
            {
                "h": "1. A2A protocols",
                "body": (
                    "A2A is the emerging standard for agent-to-agent "
                    "messaging. The envelope is structured (task, message, "
                    "artifact). The handshake negotiates capabilities. The "
                    "transport is HTTP or gRPC. Different from MCP, which is "
                    "agent-to-tool. The two protocols are complementary, not "
                    "competing."
                ),
            },
            {
                "h": "2. Agent Cards",
                "body": (
                    "A self-describing manifest. Lists capabilities, cost "
                    "estimates, latency expectations, contact metadata, and "
                    "authentication requirements. Read by both humans (to "
                    "decide if an agent fits) and other agents (to plan a "
                    "call). Use JSON-LD or a similar structured format."
                ),
            },
            {
                "h": "3. Discovery: Nanda and Cisco's AGNTCY initiative",
                "body": (
                    "Nanda proposes a federated registry: anyone can publish, "
                    "anyone can query. Cisco's AGNTCY initiative proposes a directory "
                    "model with identity guarantees: agents have signed "
                    "identities verifiable by a central authority. Both compete "
                    "for the role DNS plays for hostnames. No winner yet; "
                    "expect a hybrid."
                ),
            },
            {
                "h": "4. AuthN and AuthZ",
                "body": (
                    "Transport layer: mTLS with rotated certificates or "
                    "signed JWTs. Message layer: scoped capabilities, so "
                    "agent B knows agent A is only allowed to call this one "
                    "tool with these arguments. Every hop is logged with "
                    "structured fields, not just text."
                ),
            },
            {
                "h": "5. Role-based cooperation",
                "body": (
                    "Each agent has a fixed role. The protocol is rigid: "
                    "planner emits plan, workers execute, critic verifies. "
                    "Cheap, predictable. Fails when the task shifts and "
                    "roles need to renegotiate."
                ),
            },
            {
                "h": "6. Voting-based cooperation",
                "body": (
                    "N agents propose solutions. A quorum votes on the best. "
                    "Useful when the verifier is weaker than the proposers. "
                    "Costs N times the inference. Pay it when correctness "
                    "matters more than latency."
                ),
            },
            {
                "h": "7. Debate-based cooperation",
                "body": (
                    "Two agents argue opposite positions. A judge agent "
                    "decides. Catches errors that any single agent (including "
                    "the judge) would miss. Most useful when answers are "
                    "easy to verify but hard to generate."
                ),
            },
        ],
        "review": [
            "Sketch an Agent Card for a competitive-analysis agent that costs $0.30 per call.",
            "When would you choose voting over debate?",
            "Why does mTLS alone not satisfy AuthZ requirements?",
            "Pick a task where role-based cooperation is the wrong default.",
        ],
    },
    10: {
        "intro": (
            "Step back. Today is the architecture week. Cover the agentic OSI "
            "model, nine production patterns, and the doctrine of ruthless "
            "simplification. The lab implements three patterns on the same "
            "task and compares them on real numbers."
        ),
        "sections": [
            {
                "h": "1. The agentic OSI model",
                "body": (
                    "Six layers, top to bottom. Presentation (how the user "
                    "sees results). Execution (the agent loop itself). "
                    "Planning (the model's reasoning trace). Capability (which "
                    "tools and which agents). Session (state across turns). "
                    "Transport (HTTP, MCP, A2A). Useful for debugging because "
                    "you can isolate which layer failed."
                ),
            },
            {
                "h": "2. Router pattern",
                "body": (
                    "A small classifier routes input to one of N specialized "
                    "agents. The classifier can be a small model or even "
                    "rules. Cheap, predictable, easy to test. The first "
                    "pattern to try."
                ),
            },
            {
                "h": "3. Fan-out / fan-in",
                "body": (
                    "Split work to N parallel agents. Merge results. Useful "
                    "for comparison, parallel search, and voting. The merge "
                    "step is where the design effort goes."
                ),
            },
            {
                "h": "4. Orchestrator-workers",
                "body": (
                    "One planner agent emits a task tree. Workers execute "
                    "leaves. The planner does not execute; the workers do not "
                    "plan. Standard pattern for non-trivial tasks."
                ),
            },
            {
                "h": "5. Evaluator-optimizer",
                "body": (
                    "One agent generates, another evaluates, the first "
                    "revises. Pair well with structured rubrics. Stop "
                    "condition is either a quality threshold or a max-"
                    "iteration cap."
                ),
            },
            {
                "h": "6. Autonomy ladder",
                "body": (
                    "Production deployments start at suggest-only and "
                    "ratchet up over time. Stages: suggest, approve-each, "
                    "approve-batch, approve-on-anomaly, autonomous-with-audit. "
                    "Never start at autonomous, no matter how good the model."
                ),
            },
            {
                "h": "7. Sandbox-then-act",
                "body": (
                    "Try the action in a sandbox first. Apply for real only "
                    "if the sandbox result matches expectations. Costs one "
                    "extra call per action. Required for destructive tools."
                ),
            },
            {
                "h": "8. Supervisor-with-veto, cache-and-skip, long-running task",
                "body": (
                    "Supervisor-with-veto: a small fast model can veto the "
                    "main agent's actions. Cache-and-skip: cache tool results "
                    "by argument and skip duplicate calls. Long-running task: "
                    "asynchronous pattern for tasks measured in minutes or "
                    "hours, with checkpointing and resume."
                ),
            },
            {
                "h": "9. Ruthless simplification",
                "body": (
                    "Delete components. If you cannot describe the system in "
                    "one page, simplify before adding. Most production "
                    "agent failures we see come from over-architecting, not "
                    "under-architecting. A pipeline you can describe at 3 AM "
                    "is a pipeline you can debug at 3 AM."
                ),
            },
        ],
        "review": [
            "Place a tool-call timeout failure on the agentic OSI model.",
            "When does fan-out / fan-in beat a single agent? When does it not?",
            "Where on the autonomy ladder should an agent that drafts customer emails sit?",
            "Pick a system you have built and apply ruthless simplification. What would you delete?",
        ],
    },
    11: {
        "intro": (
            "Agentic RAG done seriously. Multi-hop, HyDE, query decomposition, "
            "multi-source routing. Then trajectory-based training with "
            "Microsoft Agent Lightning. The lab pair builds a real agentic RAG "
            "system over a 100K-document corpus and trains a smaller agent on "
            "the successful trajectories."
        ),
        "sections": [
            {
                "h": "1. Multi-hop RAG",
                "body": (
                    "Hard questions need multiple retrievals chained together. "
                    "The agent decides what to retrieve next given partial "
                    "answers. The challenge is intermediate evaluation: when "
                    "is the partial answer good enough to query again, and "
                    "when has the chain gone off the rails."
                ),
            },
            {
                "h": "2. HyDE",
                "body": (
                    "Hypothetical Document Embeddings. Generate a plausible "
                    "answer first using only the query. Embed that. Retrieve "
                    "against the result. Closes the query-document distribution "
                    "gap that plain query embeddings suffer from. Cheap and "
                    "surprisingly effective. One extra LLM call per query."
                ),
                "code": (
                    "def hyde_retrieve(query, k=8):\n"
                    "    hypo = llm.generate(f'Write a passage answering: {query}')\n"
                    "    return vector_store.search(embed(hypo), k=k)\n"
                ),
            },
            {
                "h": "3. Query decomposition",
                "body": (
                    "Predetermined: planner emits all sub-queries up front. "
                    "Predictable but rigid. Adaptive: each sub-query depends "
                    "on prior results. Flexible but harder to evaluate. Pick "
                    "based on how often the planner can predict the full "
                    "path."
                ),
            },
            {
                "h": "4. Multi-source routing",
                "body": (
                    "Vector store for semantic queries. BM25 for keyword "
                    "queries. SQL for structured queries. APIs for live data. "
                    "A small router classifies the query and picks the source. "
                    "A fallback agent reconciles when sources disagree."
                ),
            },
            {
                "h": "5. Trajectory capture",
                "body": (
                    "Every successful agent run is a training example. "
                    "Capture (state, action, observation, reward) at each "
                    "step. Store the full trace. Filter for success, balance "
                    "by task type, and you have a training set."
                ),
            },
            {
                "h": "6. Microsoft Agent Lightning",
                "body": (
                    "A framework for trajectory-based agent training. Handles "
                    "the data shape, the bookkeeping, the loss design. Use it "
                    "to train smaller, faster students from larger, slower "
                    "teachers. The savings compound: faster inference, less "
                    "GPU time, lower cost per query."
                ),
            },
        ],
        "review": [
            "Give a question where HyDE helps. Give one where it does not.",
            "Pick a corpus where adaptive decomposition is mandatory. Justify.",
            "How do you balance training trajectories when some task types are over-represented?",
            "What is the largest student model that still benefits from this kind of training?",
        ],
    },
    12: {
        "intro": (
            "Wrap-up week. Cover the RAG-vs-fine-tuning escalation ladder, "
            "Reinforcement Learning with Verifiable Rewards (RLVR), evaluation "
            "of fine-tuned models, and MARL. The bulk of the week is capstone "
            "presentations and peer review."
        ),
        "sections": [
            {
                "h": "1. The RAG vs fine-tuning escalation ladder",
                "body": (
                    "Try RAG first. It is cheap and updates with the data. "
                    "Fine-tune for behavior change (persona, format, refusal "
                    "patterns). Combine when neither alone hits the bar. The "
                    "wrong default is to fine-tune first; the cost is real "
                    "and the gain is often illusory."
                ),
            },
            {
                "h": "2. RLVR",
                "body": (
                    "When the reward can be programmatically verified (unit "
                    "tests pass, code compiles, theorem checker accepts, "
                    "answer matches the gold), skip the reward model. The "
                    "verifier becomes the reward function. Faster training, "
                    "less reward hacking."
                ),
            },
            {
                "h": "3. Evaluation of fine-tuned models",
                "body": (
                    "Held-out eval set for the target task. Regression suite "
                    "for base capabilities (so fine-tuning has not broken "
                    "math, code, or reasoning). Drift checks over time as "
                    "your data distribution evolves. Harm test: explicit "
                    "probes for the bad behaviors your fine-tuning was "
                    "supposed to suppress."
                ),
            },
            {
                "h": "4. Multi-agent RL",
                "body": (
                    "Centralized training with decentralized execution is the "
                    "default. Reward shaping for credit assignment across "
                    "agents (who deserves credit when the team succeeds). "
                    "MARL beats single-agent approaches when the agents have "
                    "genuinely different observation spaces and the policy "
                    "would be a smaller program if specialized."
                ),
            },
            {
                "h": "5. Capstone presentations",
                "body": (
                    "Twenty minutes per team. Cover architecture, results, "
                    "failure modes, and the one decision you would make "
                    "differently. Peer review uses a written rubric. Bring "
                    "the rubric. Use it on yourself before the presentation."
                ),
            },
            {
                "h": "6. The path ahead",
                "body": (
                    "A reading list of twenty papers for the six months "
                    "after the bootcamp. Membership in the Proxiant alumni "
                    "Discord. A standing invitation to office hours for "
                    "production blockers. The work you do over the next "
                    "twelve months is the real result of this bootcamp."
                ),
            },
        ],
        "review": [
            "Give a task where RAG is sufficient and fine-tuning would be wrong.",
            "Sketch an RLVR setup for a math-tutoring agent.",
            "What is the smallest harm test you would ship with any aligned model?",
            "When does MARL definitely beat tool-maximalist single agents?",
        ],
    },
}
