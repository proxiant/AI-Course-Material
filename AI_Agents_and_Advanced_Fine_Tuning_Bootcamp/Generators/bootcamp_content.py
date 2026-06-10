"""
Master content map for AI Agents & Advanced Fine-Tuning Bootcamp.
12 weeks. Sundays = main session. Tuesday/Thursday = labs. Wednesday = quiz.
Style rules (project CLAUDE.md): no em dashes, no AI cliches, plain declarative prose.
"""

START_DATE = "Sunday, October 4, 2026"
DURATION_WEEKS = 12
TUITION = "$3,700 (or $3,600 if paid by check or Zelle upfront)"

PREREQ = ("Working Python (3.10+), comfort with PyTorch or TensorFlow basics, "
          "prior exposure to LLM APIs, and familiarity with classical NLP "
          "(tokenization, embeddings, transformer attention).")

WEEKS = [
    {
        "num": 1,
        "date": "Sunday, October 4, 2026",
        "title": "Introduction to AI Agents",
        "tagline": "The agentic loop, autonomy, and your first working agent",
        "summary": (
            "Open day for the bootcamp. Establish what an agent actually is (and is "
            "not), introduce the agentic loop, and contrast tool-using LLM patterns "
            "with traditional pipelines. The lab gets every student onto the Ray "
            "cluster and building a working agent in n8n by the end of the day."
        ),
        "objectives": [
            "Define agency, autonomy, and contextual reasoning in operational terms",
            "Trace a single iteration of the agentic loop (perceive, plan, act, observe)",
            "Identify failure modes: prompt drift, tool misuse, context overflow, and runaway loops",
            "Apply an escalation ladder when deciding between a static pipeline, a single agent, and a multi-agent system",
            "Provision a workspace on the Ray cluster and run a first agent on n8n",
        ],
        "topics": [
            ("1. What is an agent?",
             "An agent is a program that (a) perceives its environment through inputs, "
             "(b) reasons over a goal, (c) selects and calls tools, and (d) observes "
             "results to update its plan. The defining feature is the loop, not the LLM."),
            ("2. The agentic loop in detail",
             "Perceive: collect observations from prior steps and external inputs. "
             "Plan: produce the next action (a tool call, a sub-task, a final answer). "
             "Act: invoke the tool and capture structured results. "
             "Observe: feed results back into context and decide whether to terminate."),
            ("3. Tradeoffs of agency",
             "Higher autonomy raises capability and lowers determinism. The cost shows "
             "up in latency, token spend, and harder evaluation. Pick the smallest "
             "amount of agency that solves the problem."),
            ("4. The escalation ladder",
             "Static pipeline first. Then a retrieval-augmented call. Then a single "
             "tool-using agent. Then a multi-agent system. Only step up when the lower "
             "rung visibly fails on real tasks."),
            ("5. Security and failure modes",
             "Prompt injection through tool outputs, accidental shell access, "
             "credential leakage in traces, infinite tool loops, and memory poisoning "
             "from long-running sessions. Each has a concrete countermeasure."),
            ("6. The course platform",
             "Tour of the Ray cluster, GPU allocation policy, shared object store, "
             "and the n8n workflow runner used for the first lab."),
        ],
        "papers": [
            ("ReAct: Synergizing Reasoning and Acting in Language Models",
             "Yao et al., 2022 (arXiv:2210.03629). Foundational paper for the "
             "interleaved thought-action-observation pattern."),
            ("Toolformer: Language Models Can Teach Themselves to Use Tools",
             "Schick et al., 2023 (arXiv:2302.04761). Early demonstration of "
             "self-supervised tool-use signal."),
        ],
        "labs": [
            {
                "title": "Ray cluster onboarding and your first remote task",
                "objective": "Connect to the Proxiant Ray cluster, allocate a GPU, and run a remote task that returns a Hugging Face tokenizer summary.",
                "prereqs": "SSH key registered, Conda environment installed locally.",
                "steps": [
                    "Authenticate to the cluster head node and verify GPU visibility.",
                    "Create a Ray actor that loads a tokenizer and exposes a `summarize` method.",
                    "Submit ten remote tasks in parallel and collect timing data.",
                    "Tear down the actor and verify GPU release.",
                ],
                "deliverables": "Notebook with timing chart, actor source, and a short note on cold-start cost.",
            },
            {
                "title": "Build a tool-using agent in n8n",
                "objective": "Wire up an n8n workflow where an LLM node decides between three tools: web search, calculator, and a CSV lookup.",
                "prereqs": "n8n credentials configured, OpenAI or Anthropic API key bound.",
                "steps": [
                    "Create the three HTTP-backed tool nodes and validate each in isolation.",
                    "Add a Switch node driven by structured JSON output from the LLM.",
                    "Wrap the loop with a max-iteration guard set to five.",
                    "Run five sample questions through the agent and log tool selections.",
                ],
                "deliverables": "Exported workflow JSON, run log table, and a one-paragraph reflection on failure cases.",
            },
        ],
    },
    {
        "num": 2,
        "date": "Sunday, October 11, 2026",
        "title": "Enterprise AI",
        "tagline": "Reasoning workflows, agentic RAG, and multi-agent teams",
        "summary": (
            "Move from a single agent to enterprise patterns. Cover autonomous "
            "reasoning workflows, task decomposition, persistent memory, and the "
            "first taste of agentic RAG. Introduce multi-agent teams and the game "
            "theory that governs cooperation and defection. The lab gets students "
            "running real workflows in Google ADK and LangGraph."
        ),
        "objectives": [
            "Decompose a high-level task into a planner-worker-critic structure",
            "Implement persistent memory using short-term scratchpad plus long-term vector store",
            "Compare static RAG with agentic RAG on retrieval recall and answer faithfulness",
            "Identify cooperation, defection, and coalition formation in multi-agent settings",
            "Build a production evaluation rubric covering quality, cost, latency, and safety",
        ],
        "topics": [
            ("1. Autonomous reasoning workflows",
             "Chain-of-thought is a prompting trick. A reasoning workflow is a "
             "verifiable program: each step has inputs, outputs, a tool, and a check."),
            ("2. Task decomposition",
             "Top-down (planner emits a tree) versus bottom-up (worker discovers "
             "sub-tasks as it runs). Tradeoffs in observability and recovery."),
            ("3. Memory architectures",
             "Scratchpad (this turn), session memory (this conversation), and "
             "semantic memory (this user, this domain). Different stores, different "
             "retention, different eviction."),
            ("4. Agentic RAG, first pass",
             "The agent decides what to retrieve, when to retrieve, and whether to "
             "retrieve again after partial answers. Contrast with one-shot RAG."),
            ("5. Multi-agent teams and game theory",
             "Cooperative, competitive, and mixed-motive settings. When agents share "
             "a reward, when they have private rewards, when reputation is the only "
             "signal that keeps the system honest."),
            ("6. Production evaluation rubric",
             "Four axes: quality (judged by humans or rubric), cost (tokens and tool "
             "calls), latency (P50 and P95), and safety (refusal correctness, leak "
             "rate, jailbreak resistance)."),
        ],
        "papers": [
            ("Reflexion: Language Agents with Verbal Reinforcement Learning",
             "Shinn et al., 2023 (arXiv:2303.11366). Self-reflection loops as an "
             "implicit credit assignment mechanism."),
            ("AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation",
             "Wu et al., 2023 (arXiv:2308.08155). Microsoft's reference framework "
             "for multi-agent dialogue."),
        ],
        "labs": [
            {
                "title": "Google ADK basics: build a research assistant",
                "objective": "Use Google Agent Development Kit to assemble a planner-worker-critic team that answers analyst questions over a small SEC filings corpus.",
                "prereqs": "Google Cloud project, ADK installed, BigQuery sandbox.",
                "steps": [
                    "Define three agents (Planner, Worker, Critic) with explicit system prompts and tool sets.",
                    "Register a BigQuery tool that runs against a public SEC filings sample.",
                    "Wire the message bus so the Critic can reject Worker outputs and request revisions.",
                    "Run five analyst questions and log the rejection rate.",
                ],
                "deliverables": "ADK config files, run transcripts, and a chart of rejection rate by question type.",
            },
            {
                "title": "LangGraph basics: control flow with state",
                "objective": "Recreate the same research assistant in LangGraph with explicit state schema and conditional edges.",
                "prereqs": "LangGraph installed, same SEC sample dataset.",
                "steps": [
                    "Define a typed state schema (question, plan, drafts, critique, final).",
                    "Build nodes for each step and conditional edges driven by the Critic verdict.",
                    "Add a checkpoint store so a failed run can resume.",
                    "Compare runtime and token cost against the ADK version.",
                ],
                "deliverables": "LangGraph source, schema diagram, cost-versus-quality comparison table.",
            },
        ],
    },
    {
        "num": 3,
        "date": "Sunday, October 18, 2026",
        "title": "Model Context Protocol (MCP)",
        "tagline": "Tool servers, schemas, and the tool-use maximalist pattern",
        "summary": (
            "MCP is the cleanest abstraction available for separating tool "
            "definition from agent runtime. Cover the protocol, build a FastMCP "
            "tool server, and connect it to a Google ADK client. Introduce the "
            "tool-use maximalist pattern as a design choice with real tradeoffs."
        ),
        "objectives": [
            "Explain the MCP architecture (client, server, transport, capability negotiation)",
            "Build a FastMCP server with three tools, full JSON schemas, and structured errors",
            "Connect a Google ADK agent to the server and handle authentication via OAuth",
            "Apply the tool-use maximalist pattern and articulate when it breaks down",
            "Write tool documentation that an LLM can read without ambiguity",
        ],
        "topics": [
            ("1. MCP architecture",
             "Server exposes tools, resources, and prompts. Client (the agent host) "
             "negotiates capabilities at startup. Transport can be stdio, HTTP, or "
             "WebSocket. The contract is JSON-RPC underneath."),
            ("2. FastMCP and the developer experience",
             "FastMCP wraps the protocol in decorator-style Python. A tool is a "
             "function with a typed signature. The schema is generated from the "
             "signature plus docstring."),
            ("3. Tool craft",
             "Names matter. Docstrings matter more. Argument names and descriptions "
             "are the prompt the LLM reads at call time. A bad description produces "
             "wrong tool calls long before runtime errors."),
            ("4. The tool-use maximalist pattern",
             "Give one agent every tool. It works surprisingly often, scales further "
             "than people expect, and is much cheaper to operate than a multi-agent "
             "swarm. Fails when tools collide on similar names or when the catalog "
             "exceeds the model's selection bandwidth."),
            ("5. Authentication and authorization",
             "OAuth 2.1 with PKCE for user-delegated access. Service-account tokens "
             "for system tools. Per-tool scopes, not per-server scopes."),
            ("6. Errors, retries, and idempotency",
             "Structured error returns let the agent reason about whether to retry. "
             "Idempotency keys prevent double-execution under retry loops."),
        ],
        "papers": [
            ("MCP Specification",
             "Anthropic, 2024 (modelcontextprotocol.io). The protocol itself, read as "
             "if it were a paper."),
            ("Gorilla: Large Language Model Connected with Massive APIs",
             "Patil et al., 2023 (arXiv:2305.15334). Empirical limits of tool "
             "selection accuracy as the catalog grows."),
        ],
        "labs": [
            {
                "title": "FastMCP tool server: three tools, real schemas",
                "objective": "Build a FastMCP server exposing a calendar reader, a CRM lookup, and an internal wiki search.",
                "prereqs": "Python 3.11, fastmcp installed, sample fixture data shipped with the lab.",
                "steps": [
                    "Define three tools with full type hints and docstrings.",
                    "Add structured error returns (tool_unavailable, invalid_input, rate_limited).",
                    "Run the server on stdio and validate with the MCP inspector.",
                    "Deploy the same server over HTTP and re-validate.",
                ],
                "deliverables": "Server source, schema dump, and a short note on stdio versus HTTP latency.",
            },
            {
                "title": "Google ADK client with MCP and OAuth",
                "objective": "Connect a Google ADK agent to the lab 1 server, with OAuth 2.1 for the calendar tool.",
                "prereqs": "Google OAuth client configured, ADK runtime installed.",
                "steps": [
                    "Configure the agent host to discover the MCP server on startup.",
                    "Wire the OAuth flow so the calendar tool requires user consent the first time.",
                    "Run five user requests that touch all three tools.",
                    "Capture the full trace including token refreshes.",
                ],
                "deliverables": "Trace log, OAuth configuration, and a one-paragraph note on consent UX.",
            },
        ],
    },
    {
        "num": 4,
        "date": "Sunday, October 25, 2026",
        "title": "Prompt Engineering and Optimization",
        "tagline": "From CO-STAR to DSPy, GEPA, TextGrad, and OPRO",
        "summary": (
            "Prompts are programs. Move from hand-crafted prompting (CO-STAR, "
            "few-shot, hallucination mitigation) to optimization frameworks that "
            "search prompt space programmatically. Cover DSPy with COPRO and MIPRO, "
            "then prompt optimizers that search a larger space (GEPA, TextGrad, OPRO)."
        ),
        "objectives": [
            "Apply the CO-STAR framework to structure complex prompts",
            "Build a few-shot prompt with negative examples and a refusal example",
            "Use DSPy to express a task as a signature and optimize with COPRO and MIPRO",
            "Run GEPA or TextGrad to optimize a prompt with gradient-style feedback",
            "Compare hand-crafted prompts against optimized prompts on a fixed eval set",
        ],
        "topics": [
            ("1. CO-STAR framework",
             "Context, Objective, Style, Tone, Audience, Response format. Each field "
             "has a single purpose. Skipping fields produces predictable failure modes."),
            ("2. Few-shot prompting done right",
             "Diversity matters more than count. Include the boundary case and the "
             "explicit refusal. Order matters: recency bias is real."),
            ("3. Hallucination mitigation",
             "Three families: grounding (retrieve before answer), structured output "
             "(refuse to emit invalid JSON), and self-consistency (sample N, vote)."),
            ("4. DSPy basics",
             "A Signature defines inputs and outputs. A Module composes signatures. "
             "An Optimizer searches over instructions and demonstrations. The Compiler "
             "freezes the result."),
            ("5. COPRO and MIPRO",
             "COPRO optimizes instructions through coordinate ascent. MIPRO jointly "
             "optimizes instructions and demonstrations with Bayesian search."),
            ("6. Prompt optimizers: GEPA, TextGrad, OPRO",
             "GEPA is genetic with reflection. TextGrad treats text as a tensor and "
             "uses a critic LLM as the gradient. OPRO uses an LLM as the optimizer: "
             "it reads the trajectory of prior prompts and their scores, then "
             "proposes better prompts. Each fits a different stage. Do not confuse "
             "OPRO with ORPO, which unifies preference optimization with "
             "reference-free training; ORPO is a preference fine-tuning method "
             "(weights, not prompts) and pairs with DPO in Week 6."),
        ],
        "papers": [
            ("DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines",
             "Khattab et al., 2023 (arXiv:2310.03714)."),
            ("GEPA: Reflective Prompt Evolution",
             "Reading guide ships with the lab. Foundational for treating prompts as "
             "an evolutionary search problem."),
            ("TextGrad: Automatic Differentiation via Text",
             "Yuksekgonul et al., 2024 (arXiv:2406.07496)."),
        ],
        "labs": [
            {
                "title": "Advanced prompting: structured outputs and refusal",
                "objective": "Build a classification prompt that handles seven categories plus a 'none of the above' refusal, with structured JSON output.",
                "prereqs": "OpenAI or Anthropic API access, eval set shipped with the lab (200 examples).",
                "steps": [
                    "Write a baseline prompt and measure accuracy on the eval set.",
                    "Add a refusal example and remeasure.",
                    "Switch to structured output via tool-call schema and remeasure.",
                    "Compare the three runs on accuracy, refusal precision, and cost.",
                ],
                "deliverables": "Eval report table, three prompt versions, and a one-paragraph error analysis.",
            },
            {
                "title": "DSPy basics: signature, module, optimize",
                "objective": "Express the lab 1 task in DSPy and optimize with both COPRO and MIPRO.",
                "prereqs": "DSPy installed, same eval set.",
                "steps": [
                    "Define a Signature with seven labels and a refusal slot.",
                    "Wrap in a Module that calls an LM with chain-of-thought.",
                    "Optimize with COPRO and record best instruction.",
                    "Optimize with MIPRO and compare.",
                ],
                "deliverables": "Optimization trace, final compiled program, and a comparison plot.",
            },
            {
                "title": "Evolutionary prompt optimization with GEPA",
                "objective": "Run GEPA on the same task and beat the DSPy baseline.",
                "prereqs": "GEPA reference implementation cloned, GPU available for critic model.",
                "steps": [
                    "Configure the evaluator and the mutation operator.",
                    "Run 50 generations and record the fitness curve.",
                    "Inspect the top three prompts and write a short critique.",
                    "Compare final accuracy against DSPy MIPRO.",
                ],
                "deliverables": "Fitness curve, top prompts, and a written comparison.",
            },
        ],
    },
    {
        "num": 5,
        "date": "Sunday, November 1, 2026",
        "title": "Fine-Tuning Foundations and Economy",
        "tagline": "Embeddings, contrastive loss, LoRA, qLoRA, and Chinchilla scaling",
        "summary": (
            "The first fine-tuning week. Cover embeddings and contrastive objectives "
            "(Triplet, InfoNCE, SimCLR). Walk through Chinchilla scaling to set "
            "intuition about parameter-to-token ratios. Then dive into parameter-"
            "efficient fine-tuning: LoRA, rank allocation, quantization, soft "
            "prompting, and steering vectors. The lab compares full fine-tuning, "
            "LoRA, and qLoRA head to head."
        ),
        "objectives": [
            "Choose between Triplet, InfoNCE, and SimCLR for a given embedding task",
            "Apply Chinchilla scaling to estimate the right model size for a token budget",
            "Configure LoRA with rank, alpha, and target module choices appropriate to the task",
            "Quantize a base model to 4-bit and fine-tune with qLoRA",
            "Compare full fine-tuning, LoRA, and qLoRA on a fixed downstream eval",
        ],
        "topics": [
            ("1. Embeddings as the universal currency",
             "Every modern retrieval, classification, clustering, and RAG system "
             "rests on embeddings. The objective you train with shapes the geometry "
             "you get."),
            ("2. Contrastive objectives",
             "Triplet (anchor, positive, negative with margin). InfoNCE (anchor "
             "against batch of negatives). SimCLR (augmentation-based positives). "
             "Tradeoffs in sample efficiency and hard-negative handling."),
            ("3. Chinchilla scaling",
             "For a fixed compute budget, optimal model size and training tokens "
             "scale together at roughly 20 tokens per parameter. Implications for "
             "your fine-tuning budget."),
            ("4. LoRA: the mechanics",
             "Adapt frozen weights W with a low-rank update BA, where rank r is "
             "small. Update only BA. Recover full-precision performance on most "
             "downstream tasks at one to two percent of the trainable parameters."),
            ("5. Rank allocation",
             "Higher rank helps when the downstream task changes the model's "
             "semantics. Lower rank suffices when only style or format changes. "
             "Per-layer rank schedules sometimes beat uniform allocation."),
            ("6. qLoRA and quantization",
             "Quantize the base model to 4-bit (NF4 with double quantization), "
             "train LoRA adapters in 16-bit. Cuts memory by roughly four times "
             "with little accuracy loss on most tasks."),
            ("7. Soft prompting and steering vectors",
             "Soft prompts train a small embedding prefix instead of adapter "
             "weights. Steering vectors edit activations at inference. Cheap, "
             "narrow, and surprisingly effective for tone control."),
        ],
        "papers": [
            ("LoRA: Low-Rank Adaptation of Large Language Models",
             "Hu et al., 2021 (arXiv:2106.09685)."),
            ("QLoRA: Efficient Finetuning of Quantized LLMs",
             "Dettmers et al., 2023 (arXiv:2305.14314)."),
            ("Training Compute-Optimal Large Language Models",
             "Hoffmann et al., 2022 (arXiv:2203.15556). The Chinchilla paper."),
        ],
        "labs": [
            {
                "title": "Contrastive embedder fine-tuning",
                "objective": "Fine-tune a sentence embedder on a domain corpus using InfoNCE and evaluate on a downstream retrieval task.",
                "prereqs": "Sentence-transformers installed, sample domain corpus shipped with the lab.",
                "steps": [
                    "Build training pairs with hard negatives mined from the corpus.",
                    "Train for three epochs with InfoNCE loss.",
                    "Evaluate Recall@10 and MRR on the held-out queries.",
                    "Compare against the pretrained baseline.",
                ],
                "deliverables": "Training curve, eval table, and a short note on hard-negative mining.",
            },
            {
                "title": "Full fine-tuning vs LoRA vs qLoRA, head to head",
                "objective": "Fine-tune the same base model three ways on a domain instruction set and compare cost, time, and downstream accuracy.",
                "prereqs": "8x H100 access for full fine-tuning, 1x H100 for LoRA and qLoRA.",
                "steps": [
                    "Run full fine-tuning for 1000 steps and record metrics.",
                    "Run LoRA (rank 16, alpha 32) for 1000 steps and record metrics.",
                    "Run qLoRA (4-bit base, rank 16) for 1000 steps and record metrics.",
                    "Compare GPU hours, peak memory, eval accuracy, and inference latency.",
                ],
                "deliverables": "Three-way comparison table, recommended default for the domain, and a short note on when full fine-tuning is still worth it.",
            },
        ],
    },
    {
        "num": 6,
        "date": "Sunday, November 8, 2026",
        "title": "Reinforcement Learning Fundamentals",
        "tagline": "MDPs, value functions, PPO, DPO, GRPO, and alignment",
        "summary": (
            "RL week one. Cover MDPs, value and advantage functions, and the policy "
            "gradient family (TRPO, PPO). Introduce direct preference methods (DPO) "
            "and group relative methods (GRPO). Tie everything back to the Helpful, "
            "Honest, Harmless framing for alignment."
        ),
        "objectives": [
            "Formalize an LLM task as an MDP and identify state, action, reward, transitions",
            "Distinguish value, Q, and advantage functions and when each is used",
            "Derive the PPO surrogate objective and explain the role of the clip term",
            "Compare PPO, DPO, and GRPO on data requirements and training stability",
            "Apply the Helpful, Honest, Harmless rubric when designing a reward signal",
        ],
        "topics": [
            ("1. MDPs and the LLM analogy",
             "State is the context window. Action is the next token (or the next "
             "tool call). Reward is delayed and sparse. Discount is implicit."),
            ("2. Value, Q, and advantage",
             "V is the expected return from a state. Q is the expected return from a "
             "state-action pair. Advantage A = Q - V tells you how much better an "
             "action is than the policy average. PPO uses A; DPO does not need it."),
            ("3. Policy gradients and TRPO",
             "Policy gradient is unbiased but high variance. TRPO constrains step "
             "size by KL divergence to keep training stable."),
            ("4. PPO",
             "Replace the hard KL constraint with a clipped ratio. Easier to "
             "implement, more popular in practice. Defaults: clip 0.2, value loss "
             "coefficient 0.5, entropy bonus 0.01."),
            ("5. DPO",
             "Skip the explicit reward model. Train directly on preference pairs "
             "using a closed-form objective derived from the optimal RLHF policy."),
            ("6. GRPO",
             "Group relative policy optimization. Compare a group of samples per "
             "prompt and use relative advantage. Cuts the value network and matches "
             "PPO on many tasks."),
            ("7. Helpful, Honest, Harmless",
             "Three reward axes that often pull in different directions. Document "
             "the tradeoff before you train, not after."),
        ],
        "papers": [
            ("Proximal Policy Optimization Algorithms",
             "Schulman et al., 2017 (arXiv:1707.06347)."),
            ("Direct Preference Optimization: Your Language Model is Secretly a Reward Model",
             "Rafailov et al., 2023 (arXiv:2305.18290)."),
            ("DeepSeekMath: Pushing the Limits of Mathematical Reasoning",
             "Shao et al., 2024 (arXiv:2402.03300). Introduces GRPO."),
        ],
        "labs": [
            {
                "title": "RL grid problem from scratch",
                "objective": "Implement value iteration and Q-learning on a 5x5 gridworld and visualize convergence.",
                "prereqs": "NumPy only. No deep learning framework needed.",
                "steps": [
                    "Define the grid, reward shape, and transition function.",
                    "Implement value iteration and plot the value function after each sweep.",
                    "Implement tabular Q-learning and plot the learning curve.",
                    "Compare convergence speed and final policies.",
                ],
                "deliverables": "Source, two convergence plots, and a short note on epsilon schedules.",
            },
            {
                "title": "PPO on the same grid",
                "objective": "Replace Q-learning with PPO on the gridworld and observe the effect of the clip parameter.",
                "prereqs": "PyTorch installed.",
                "steps": [
                    "Implement a small policy network and value head.",
                    "Run PPO with clip values of 0.1, 0.2, and 0.4.",
                    "Plot return curves and entropy curves for each.",
                    "Write a short recommendation for the default clip.",
                ],
                "deliverables": "Source, three runs of plots, and the written recommendation.",
            },
        ],
    },
    {
        "num": 7,
        "date": "Sunday, November 15, 2026",
        "title": "Multiple Agents and Deep RL",
        "tagline": "Design patterns, uncertainty, and RL on real LLMs",
        "summary": (
            "Move from single-agent RL to multi-agent systems and deep RL on actual "
            "LLMs. Cover engineering patterns (SRP, facades), the distinction "
            "between epistemic and aleatoric uncertainty, and the tradeoffs between "
            "tool-maximalist single agents and multi-agent architectures. The lab "
            "trio runs PPO, GRPO, and DPO on real LLMs."
        ),
        "objectives": [
            "Apply Single Responsibility Principle and facade patterns to agent design",
            "Distinguish epistemic from aleatoric uncertainty and choose the right response",
            "Make idempotent tool calls that survive retries",
            "Run PPO on an LLM with TRL and recover from training instability",
            "Run GRPO and DPO on the same base model and compare convergence",
        ],
        "topics": [
            ("1. SRP and facades in agent design",
             "One agent, one responsibility. A facade agent wraps a noisy sub-system "
             "and presents a clean tool to the rest of the team."),
            ("2. Epistemic vs aleatoric uncertainty",
             "Epistemic is what the model does not know but could learn. Aleatoric "
             "is what is genuinely random. Treat them differently: more data fixes "
             "the first; better calibration is the only response to the second."),
            ("3. Idempotency in tool calls",
             "Every write tool should accept an idempotency key. Every retry should "
             "be a no-op if the prior call succeeded. This is non-negotiable in "
             "agent systems."),
            ("4. Tool-maximalist vs multi-agent",
             "One agent with twenty tools beats five agents with four tools each, "
             "until the catalog crosses a model-specific bandwidth limit. Test both "
             "before committing."),
            ("5. PPO on LLMs: practical notes",
             "KL penalty is the difference between stable and divergent training. "
             "Reference model is non-negotiable. Reward scaling matters more than "
             "people expect."),
            ("6. GRPO on LLMs",
             "Sample N completions per prompt. Compute group-relative advantage. "
             "Drops the value head and the memory footprint by roughly half."),
            ("7. DPO on LLMs",
             "Pure preference data, no reward model, no sampling at training time. "
             "Cheaper and simpler but less expressive than PPO for multi-turn tasks."),
        ],
        "papers": [
            ("Constitutional AI: Harmlessness from AI Feedback",
             "Bai et al., 2022 (arXiv:2212.08073). Multi-stage RL with AI-generated "
             "preferences."),
            ("Group Relative Policy Optimization (DeepSeekMath section)",
             "Shao et al., 2024 (arXiv:2402.03300). Same paper as week 6, deeper read."),
        ],
        "labs": [
            {
                "title": "PPO on an LLM with TRL",
                "objective": "Fine-tune a 1B-parameter base model with PPO on a reward model trained from human preferences.",
                "prereqs": "TRL installed, reward model checkpoint provided.",
                "steps": [
                    "Configure the PPO trainer with a reference model and KL coefficient 0.1.",
                    "Train for 500 steps and watch the KL curve.",
                    "Diagnose one instability (KL spike, reward hacking, or entropy collapse).",
                    "Adjust hyperparameters and rerun.",
                ],
                "deliverables": "Training curves, the instability diagnosis, and the fix.",
            },
            {
                "title": "GRPO with TRL",
                "objective": "Fine-tune the same base model with GRPO and compare to the PPO run.",
                "prereqs": "TRL with GRPO support, GPU with at least 40 GB.",
                "steps": [
                    "Configure GRPO with group size 8.",
                    "Train for 500 steps and record memory usage.",
                    "Compare final reward, KL, and wallclock time against PPO.",
                ],
                "deliverables": "Comparison table and a short recommendation.",
            },
            {
                "title": "DPO on an LLM",
                "objective": "Fine-tune the base model with DPO on the preference pairs that produced the reward model.",
                "prereqs": "TRL installed, preference dataset provided.",
                "steps": [
                    "Run DPO for one epoch with beta 0.1.",
                    "Evaluate on the same held-out prompts used for PPO and GRPO.",
                    "Write a one-paragraph comparison of the three methods.",
                ],
                "deliverables": "Eval table and the written comparison.",
            },
        ],
    },
    {
        "num": 8,
        "date": "Sunday, November 22, 2026",
        "title": "Distributed Computing with Ray",
        "tagline": "Tasks, actors, parallelism, and production MLOps",
        "summary": (
            "Ray is the connective tissue for serious agent and fine-tuning work. "
            "Cover data, tensor, and pipeline parallelism. Walk the four Ray "
            "subsystems: Train, Tune, Serve, and the core scheduler. Tie into vLLM "
            "for high-throughput inference and Airflow for orchestrating the full "
            "MLOps pipeline."
        ),
        "objectives": [
            "Choose between data, tensor, and pipeline parallelism for a given training run",
            "Write Ray tasks and actors and reason about object-store cost",
            "Configure Ray Train for distributed fine-tuning across multiple GPUs",
            "Serve a fine-tuned model with vLLM behind Ray Serve",
            "Wire the training-evaluation-deployment loop into an Airflow DAG",
        ],
        "topics": [
            ("1. Three parallelism strategies",
             "Data parallel: same model, sharded data. Tensor parallel: split each "
             "matrix multiply across devices. Pipeline parallel: split layers "
             "across devices. Mix as the model grows."),
            ("2. Ray tasks, actors, object store",
             "Tasks are stateless. Actors hold state and a worker. Object store "
             "shares immutable data zero-copy across workers on the same node."),
            ("3. Ray Train",
             "Wraps PyTorch DDP and Hugging Face Trainer with cluster-aware "
             "placement, checkpointing, and fault tolerance."),
            ("4. Ray Tune",
             "Hyperparameter search with ASHA, Population Based Training, or "
             "Bayesian search. Stops bad runs early."),
            ("5. Ray Serve and vLLM",
             "Ray Serve provides routing, autoscaling, and traffic shaping. vLLM "
             "delivers continuous batching and PagedAttention. Compose them."),
            ("6. Production MLOps",
             "Airflow DAG: pull data, build features, train, evaluate, gate on "
             "metric thresholds, register the model, deploy behind a canary."),
        ],
        "papers": [
            ("Ray: A Distributed Framework for Emerging AI Applications",
             "Moritz et al., 2017 (arXiv:1712.05889)."),
            ("Efficient Memory Management for Large Language Model Serving with PagedAttention",
             "Kwon et al., 2023 (arXiv:2309.06180). The vLLM paper."),
        ],
        "labs": [
            {
                "title": "Batched inference with observability",
                "objective": "Serve a fine-tuned model behind vLLM and Ray Serve, then load-test with full tracing.",
                "prereqs": "Ray and vLLM installed on the cluster, fine-tuned checkpoint from week 5.",
                "steps": [
                    "Deploy the model with Ray Serve and configure two replicas with autoscaling.",
                    "Generate a synthetic load curve and capture P50 and P95 latency.",
                    "Add OpenTelemetry tracing and capture per-stage timing.",
                    "Tune continuous batching parameters and re-run.",
                ],
                "deliverables": "Latency curves, tracing flame graph, and a tuning recommendation.",
            },
            {
                "title": "Airflow MLOps pipeline end to end",
                "objective": "Build an Airflow DAG that pulls a dataset, fine-tunes with Ray Train, evaluates, and deploys to Ray Serve.",
                "prereqs": "Airflow installed on the cluster, sample dataset.",
                "steps": [
                    "Write the DAG with five tasks (extract, train, eval, gate, deploy).",
                    "Add a metric gate that blocks deployment if eval drops below threshold.",
                    "Trigger a run and watch the full pipeline complete.",
                    "Simulate a failed eval and confirm the gate blocks deployment.",
                ],
                "deliverables": "DAG source, run history screenshot, and a note on rollback strategy.",
            },
        ],
    },
    {
        "num": 9,
        "date": "Sunday, November 29, 2026",
        "title": "Agent Communications",
        "tagline": "A2A, discovery, AuthN/AuthZ, and cooperation protocols",
        "summary": (
            "Agent-to-agent communication is becoming a protocol problem, not a "
            "framework problem. Cover A2A, Agent Cards, discovery via Nanda and "
            "Cisco's AGNTCY initiative, and the security boundary. Then cover cooperation "
            "protocols: role-based, voting-based, and debate-based."
        ),
        "objectives": [
            "Read and write an Agent Card and publish it to a discovery registry",
            "Authenticate one agent to another and authorize specific capabilities",
            "Choose between role-based, voting-based, and debate-based cooperation",
            "Build an A2A flow that uses Google ADK on one end and a custom client on the other",
            "Diagnose a failed cross-agent call from logs alone",
        ],
        "topics": [
            ("1. A2A protocols",
             "A common message envelope, a capability negotiation handshake, and a "
             "structured task object. Different from MCP, which is agent-to-tool."),
            ("2. Agent Cards",
             "A self-describing manifest that lists capabilities, costs, "
             "limitations, and contact metadata. Read by both humans and other "
             "agents."),
            ("3. Discovery",
             "Nanda is a federated registry. Cisco's AGNTCY initiative proposes a directory "
             "model with identity guarantees. Both compete for the role DNS plays "
             "for hostnames."),
            ("4. AuthN and AuthZ between agents",
             "mTLS or signed JWTs at the transport layer. Scoped capabilities at "
             "the message layer. Audit log at every hop."),
            ("5. Role-based cooperation",
             "Each agent has a fixed role (planner, worker, critic). Cheap, "
             "predictable, brittle when the task shifts."),
            ("6. Voting-based cooperation",
             "N agents propose, a quorum votes on the best. Higher quality, higher "
             "cost. Useful when the verifier is weaker than the proposer."),
            ("7. Debate-based cooperation",
             "Two agents argue opposite positions; a judge agent decides. Useful "
             "for catching subtle errors a single agent misses."),
        ],
        "papers": [
            ("AI Safety via Debate",
             "Irving et al., 2018 (arXiv:1805.00899). Foundational for "
             "debate-based protocols."),
            ("A2A Protocol Specification",
             "Reading guide ships with the lab. Active spec, not a peer-reviewed "
             "paper."),
        ],
        "labs": [
            {
                "title": "Ray Core and Ray Data deep dive",
                "objective": "Build a Ray Data pipeline that processes 100 GB of JSONL, runs an embedding step, and writes to a vector store.",
                "prereqs": "Ray cluster with at least four nodes, sample 100 GB JSONL.",
                "steps": [
                    "Read the JSONL with Ray Data and inspect the resulting Dataset.",
                    "Map a tokenization step across the cluster.",
                    "Map an embedding step using a model actor per node.",
                    "Write results to the cluster vector store and verify counts.",
                ],
                "deliverables": "Pipeline source, throughput chart, and a note on partition sizing.",
            },
            {
                "title": "A2A with Google ADK as one end and a custom Python client as the other",
                "objective": "Stand up a Google ADK agent that exposes an A2A endpoint and call it from a custom Python client.",
                "prereqs": "Google ADK installed, custom client scaffold provided.",
                "steps": [
                    "Publish the ADK agent's Agent Card to a local discovery service.",
                    "Discover the agent from the custom client and negotiate capabilities.",
                    "Send a task and stream the response back.",
                    "Add mTLS and re-verify end to end.",
                ],
                "deliverables": "Both ends of the code, captured pcap or wireshark trace, and a note on mTLS rotation.",
            },
        ],
    },
    {
        "num": 10,
        "date": "Sunday, December 6, 2026",
        "title": "Architecting Agentic Systems",
        "tagline": "Nine production patterns and the doctrine of ruthless simplification",
        "summary": (
            "The week we step back and look at agentic systems as software "
            "architecture. Cover the agentic OSI model and nine production design "
            "patterns: router, fan-out/fan-in, orchestrator-workers, evaluator-"
            "optimizer, autonomy ladder, sandbox-then-act, supervisor-with-veto, "
            "cache-and-skip, and the long-running task pattern. Close with the "
            "doctrine of ruthless simplification."
        ),
        "objectives": [
            "Place each component of an agentic system in the agentic OSI model",
            "Select the correct production pattern for a given problem shape",
            "Recognize anti-patterns: god agent, hidden state, silent retries, and others",
            "Apply ruthless simplification when an architecture starts to sprawl",
            "Build a runnable example of three patterns in LangGraph",
        ],
        "topics": [
            ("1. The agentic OSI model",
             "Transport (HTTP/MCP/A2A), session, capability, planning, execution, "
             "and presentation. A useful mental model when debugging cross-layer "
             "failures."),
            ("2. Router pattern",
             "One small classifier routes input to one of N specialized agents. "
             "Cheap and predictable. The first pattern to try."),
            ("3. Fan-out / fan-in",
             "Split work to N parallel agents, merge results. Useful for "
             "comparison, voting, and parallel search."),
            ("4. Orchestrator-workers",
             "One agent plans and delegates; many workers execute. The standard "
             "pattern for non-trivial tasks."),
            ("5. Evaluator-optimizer",
             "One agent generates, another evaluates, the first revises. Pair "
             "well with structured rubrics."),
            ("6. Autonomy ladder",
             "Start at suggest-only, escalate to approve-each-step, then to "
             "approve-batches, then to autonomous with audit. Production deployments "
             "should ratchet up, never start at the top."),
            ("7. Sandbox-then-act, supervisor-with-veto, cache-and-skip, long-running task",
             "Four more patterns for safety, oversight, cost control, and "
             "asynchronous work. Each maps to a specific failure mode it prevents."),
            ("8. Ruthless simplification",
             "Default to deleting components. A pipeline you can describe in one "
             "page is a pipeline you can debug at 3 AM."),
        ],
        "papers": [
            ("Building Effective Agents",
             "Anthropic engineering blog, 2024. A reference catalog of the patterns "
             "above."),
            ("The Bitter Lesson",
             "Sutton, 2019. Read as a counterweight to over-architecting."),
        ],
        "labs": [
            {
                "title": "A2A with LangGraph plus an agent registry",
                "objective": "Build two LangGraph agents that discover each other through a registry and exchange a task end to end.",
                "prereqs": "LangGraph installed, registry service from week 9.",
                "steps": [
                    "Implement Agent A as a planner with an A2A outbound channel.",
                    "Implement Agent B as a worker that publishes its card to the registry.",
                    "Have A discover B at runtime and dispatch a task.",
                    "Capture the full message trace.",
                ],
                "deliverables": "Both agent sources and the trace.",
            },
            {
                "title": "Three agentic design patterns in code",
                "objective": "Implement Router, Orchestrator-Workers, and Evaluator-Optimizer on the same task and compare quality and cost.",
                "prereqs": "LangGraph or ADK, same eval set used in week 4.",
                "steps": [
                    "Build the three pattern implementations.",
                    "Run each on the eval set and record quality, latency, and cost.",
                    "Choose a winner and justify with the data.",
                ],
                "deliverables": "Three implementations, comparison table, and a one-page architectural justification.",
            },
        ],
    },
    {
        "num": 11,
        "date": "Sunday, December 13, 2026",
        "title": "Agentic RAG and Agentic Training",
        "tagline": "Multi-hop retrieval, HyDE, and trajectory-based training",
        "summary": (
            "Cover serious agentic RAG: multi-hop, HyDE, query decomposition, and "
            "multi-source routing. Then introduce trajectory-based agentic training "
            "with Microsoft Agent Lightning. The lab pair builds a real agentic RAG "
            "system and trains an agent on its own trajectories."
        ),
        "objectives": [
            "Decompose a multi-hop question into a sequence of retrievable sub-queries",
            "Use HyDE to bridge the query-document distribution gap",
            "Route across multiple retrieval sources (vector, BM25, SQL, API)",
            "Capture agent trajectories with the data shape required for training",
            "Train an agent on its own trajectories using Microsoft Agent Lightning",
        ],
        "topics": [
            ("1. Multi-hop RAG",
             "Hard questions need multiple retrievals chained together. The "
             "challenge is intermediate evaluation: knowing when the partial "
             "answer is good enough to query again."),
            ("2. HyDE (Hypothetical Document Embeddings)",
             "Generate a plausible answer first, embed that, retrieve against the "
             "result. Closes the query-document distribution gap. Cheap and "
             "surprisingly effective."),
            ("3. Query decomposition",
             "Two flavors: predetermined (planner emits all sub-queries up front) "
             "and adaptive (each sub-query depends on prior results). Pick based "
             "on how often the planner can predict the full path."),
            ("4. Multi-source routing",
             "Different sources answer different questions. A small classifier "
             "routes; a fallback agent reconciles disagreement."),
            ("5. Trajectory-based agentic training",
             "Every successful agent run is a training example. Capture state, "
             "action, observation, reward at each step. Reuse to train smaller, "
             "faster, cheaper agents."),
            ("6. Microsoft Agent Lightning",
             "A framework for capturing trajectories and training on them. "
             "Handles the data shape, the bookkeeping, and the loss design."),
        ],
        "papers": [
            ("Precise Zero-Shot Dense Retrieval without Relevance Labels",
             "Gao et al., 2022 (arXiv:2212.10496). The HyDE paper."),
            ("Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection",
             "Asai et al., 2023 (arXiv:2310.11511)."),
            ("Agent Lightning",
             "Microsoft Research, 2024. Reading guide ships with the lab."),
        ],
        "labs": [
            {
                "title": "Agentic RAG implementation",
                "objective": "Build a multi-hop agentic RAG over a 100K-document corpus with vector, BM25, and SQL backends.",
                "prereqs": "Vector store provisioned, BM25 index built, SQL warehouse with structured tables.",
                "steps": [
                    "Build a router that selects backend per sub-query.",
                    "Implement query decomposition with adaptive next-step planning.",
                    "Add HyDE for the vector backend.",
                    "Evaluate on a 200-question multi-hop test set.",
                ],
                "deliverables": "End-to-end source, eval report, and per-backend hit-rate breakdown.",
            },
            {
                "title": "Agentic training with Microsoft Agent Lightning",
                "objective": "Capture trajectories from the lab 1 system and train a smaller agent to imitate the successful runs.",
                "prereqs": "Agent Lightning installed, trajectories from lab 1.",
                "steps": [
                    "Filter trajectories to keep only successful runs.",
                    "Convert to the training data format.",
                    "Train a smaller base model (e.g. 3B) on the trajectories.",
                    "Evaluate the student on the same 200-question test set.",
                ],
                "deliverables": "Trained student checkpoint, eval delta versus teacher, and a cost-per-query comparison.",
            },
        ],
    },
    {
        "num": 12,
        "date": "Sunday, December 20, 2026",
        "title": "The Path Ahead (Capstone Week)",
        "tagline": "RAG vs fine-tuning, RLVR, MARL, and capstone presentations",
        "summary": (
            "Wrap-up week. Cover the RAG-versus-fine-tuning escalation ladder, "
            "Reinforcement Learning with Verifiable Rewards (RLVR), evaluation of "
            "fine-tuned models, and an introduction to multi-agent RL (MARL). The "
            "bulk of the week is capstone presentations and peer review."
        ),
        "objectives": [
            "Decide between RAG, fine-tuning, and a hybrid for a given problem",
            "Apply RLVR when the reward is checkable rather than human-judged",
            "Build an evaluation suite that catches regression in fine-tuned models",
            "Identify when MARL is appropriate and when it is overkill",
            "Present a capstone project that is reproducible and honest about limitations",
        ],
        "topics": [
            ("1. The RAG vs fine-tuning escalation ladder",
             "Try RAG first. Fine-tune for behavior change, format change, or "
             "consistent persona. Combine when neither alone hits the bar."),
            ("2. RLVR",
             "When the reward can be programmatically verified (unit tests pass, "
             "code compiles, theorem checker accepts), skip the reward model and "
             "use the verifier directly."),
            ("3. Evaluating fine-tuned models",
             "Held-out eval set, regression suite for base capabilities, "
             "drift checks over time, and an explicit harm test."),
            ("4. Multi-agent RL",
             "Centralized training, decentralized execution. Reward shaping for "
             "credit assignment across agents. Where MARL still beats single-agent "
             "approaches."),
            ("5. Capstone presentations",
             "Twenty minutes per team. Architecture, results, failure modes, and "
             "the one decision they would make differently."),
            ("6. Peer review and the path ahead",
             "Structured peer review using a written rubric. A reading list of "
             "twenty papers for the six months after the bootcamp."),
        ],
        "papers": [
            ("Reinforcement Learning with Verifiable Rewards",
             "Lambert et al., 2024 (reading guide ships with the lab)."),
            ("Cooperative Multi-Agent Reinforcement Learning",
             "Foerster et al., 2017. A starting point for MARL."),
        ],
        "labs": [
            {
                "title": "Capstone work block 1",
                "objective": "Polish the capstone implementation: code quality, evals, and reproducibility.",
                "prereqs": "Capstone in working state.",
                "steps": [
                    "Run the full eval suite and capture results.",
                    "Write the README so a peer can reproduce in under an hour.",
                    "Build the presentation deck (10 slides max).",
                    "Dry-run the presentation with a peer reviewer.",
                ],
                "deliverables": "Eval results, README, and presentation deck.",
            },
            {
                "title": "Capstone presentations and peer review",
                "objective": "Present the capstone and conduct peer review on two other capstones using the structured rubric.",
                "prereqs": "Capstone ready, peer review rubric printed.",
                "steps": [
                    "Present for 15 minutes plus 5 minutes Q&A.",
                    "Review two other capstones using the rubric.",
                    "Write actionable feedback for each reviewed team.",
                ],
                "deliverables": "Presentation, two completed review forms, and one reflection paragraph.",
            },
        ],
    },
]


def slug(week):
    """Filename-safe slug from week title."""
    t = week["title"].lower()
    out = []
    for c in t:
        if c.isalnum():
            out.append(c)
        elif c in " -_":
            out.append("_")
    return "".join(out).strip("_")
