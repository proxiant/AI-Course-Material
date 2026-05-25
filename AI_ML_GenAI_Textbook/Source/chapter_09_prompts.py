"""Chapter 9: Prompt Engineering and Optimization."""

CHAPTER = {
    "label": "Chapter 9",
    "title": "Prompt Engineering and Optimization",
    "sections": [
        {
            "number": "9.1",
            "title": "Prompts as Programs",
            "paragraphs": [
                "A prompt is the input to a large language model. In the simplest case, it is "
                "a question and the LLM responds with an answer. In production systems, a "
                "prompt is a carefully engineered program: system instructions, examples, "
                "context retrieved from a knowledge base, the user's query, output format "
                "specifications, and constraints. Small changes can swing quality dramatically. "
                "This is the discipline of prompt engineering.",

                "Prompt engineering started as folk wisdom: a list of tricks (chain of "
                "thought, few-shot, role-playing) shared on Twitter. It has matured into a "
                "structured discipline with frameworks (CO-STAR), optimization algorithms "
                "(DSPy, GEPA, TextGrad), and empirical methodology (held-out evaluation, "
                "ablation studies, bias controls). This chapter walks the discipline.",

                "Two themes throughout. First, prompts are not magic incantations. Their "
                "effects can be measured, ablated, and optimized like any engineering "
                "artifact. Second, hand-crafted prompts plateau quickly for complex tasks. "
                "Programmatic optimization wins above a complexity threshold. Know both, "
                "use the right one for the task.",
            ],
        },
        {
            "number": "9.2",
            "title": "The CO-STAR Framework",
            "paragraphs": [
                "CO-STAR provides a structured template for production prompts. Six fields, "
                "each with one purpose. Skipping any field produces predictable failure "
                "modes.",

                "Context. What the model needs to know about the world or the situation. "
                "Background information, user state, system state, domain assumptions. Often "
                "the longest part of the prompt.",

                "Objective. What success looks like for this call. A clear, single-purpose "
                "statement of the task. Vague objectives produce vague answers.",

                "Style. The form of the output: formal, casual, technical, journalistic. Sets "
                "the register.",

                "Tone. The emotional register: calm, urgent, neutral, friendly. Often "
                "important for customer-facing applications.",

                "Audience. Who reads the output. A response for a senior engineer differs "
                "from one for a non-technical executive. Adjust complexity and vocabulary.",

                "Response format. The shape of the output: plain text, JSON, markdown, "
                "table, bulleted list. Often the most under-specified field, leading to "
                "downstream parsing failures.",

                "Worked example. A customer support FAQ bot: Context (the company's product "
                "line and policies); Objective (answer FAQ accurately or escalate); Style "
                "(professional); Tone (warm but precise); Audience (existing customers with "
                "questions); Response format (short answer plus source policy citation, "
                "refuse if outside policy scope). Six lines, all the structure needed.",
            ],
        },
        {
            "number": "9.3",
            "title": "Few-Shot and In-Context Learning",
            "paragraphs": [
                "In-context learning is the LLM's ability to learn a task from examples in "
                "the prompt, with no weight updates. A prompt with three to seven "
                "(input, output) pairs followed by a new input often produces the right "
                "output for the new input.",

                "Why it works. During pretraining, the model has seen many instances of "
                "demonstration patterns: lists, tables, translation pairs, code with "
                "similar function signatures. Predicting the next token in such sequences "
                "requires generalizing the pattern. This generalization is the meta-task "
                "that enables in-context learning at inference time.",

                "Empirical principles. Diversity beats count. Three diverse examples beat "
                "seven similar ones. Include the boundary case. Include an explicit refusal "
                "if your task has one. Order matters: recency bias is real, so put the most "
                "canonical example last. Format consistency matters: if your inputs are "
                "structured, format every example identically.",

                "Limits. Prompt length is finite. Quality plateaus after 5-10 examples for "
                "most tasks. Sensitive to example ordering and selection. For better quality "
                "with abundant examples, use RAG (retrieve relevant examples per query) or "
                "fine-tune.",
            ],
        },
        {
            "number": "9.4",
            "title": "Chain-of-Thought and Reasoning",
            "paragraphs": [
                "Chain-of-thought (CoT) prompting asks the model to produce reasoning steps "
                "before the final answer. Instead of 'Q: ... A: 42', the model produces "
                "'Q: ... Let me think step by step. First... then... so the answer is 42.'",

                "Why it helps. Complex reasoning requires intermediate steps. Asking for "
                "the final answer directly forces the model to do all reasoning in one "
                "forward pass without externalizing intermediate state. CoT lets the model "
                "spread reasoning across multiple tokens, each of which can attend back to "
                "previous tokens.",

                "Variants. Zero-shot CoT (Kojima et al., 2022): 'Let's think step by step.' "
                "Few-shot CoT (Wei et al., 2022): provide examples with reasoning. Self-"
                "consistency (Wang et al., 2022): sample multiple CoT chains and vote. Tree "
                "of Thoughts (Yao et al., 2023): explore branches and backtrack.",

                "Modern reasoning models (o1, o3, DeepSeek-R1, Claude with extended "
                "thinking) are trained to do extensive CoT automatically, with reinforcement "
                "learning on verifiable reward signals. They dramatically outperform "
                "non-reasoning models on math, code, and complex reasoning tasks.",

                "When to use. Tasks requiring multi-step reasoning: math, code, planning, "
                "logical deduction. Skip on simple lookup tasks where CoT adds latency "
                "without benefit. Use a router to send simple queries to non-reasoning "
                "models and complex queries to reasoning models.",
            ],
        },
        {
            "number": "9.5",
            "title": "Hallucination Mitigation",
            "paragraphs": [
                "LLMs sometimes produce plausible-sounding but factually wrong outputs. "
                "This is hallucination. Three families of mitigation strategies.",

                "Grounding. Retrieve evidence before generating; require the model to use "
                "only the retrieved evidence. RAG is the canonical pattern. Force the "
                "model to cite which retrieved passage supports each claim. Verify the "
                "citations.",

                "Structured output. Constrain the output format so invalid responses are "
                "impossible. JSON mode, tool-call schemas, regular expression constraints. "
                "The model cannot hallucinate a function call to a function that doesn't "
                "exist if the function name is constrained to the registered tool list.",

                "Self-consistency. Sample N answers; vote or pick the consistent one. "
                "Differential outputs across samples signal uncertainty. Used in production "
                "high-stakes systems.",

                "Combine all three for critical tasks. Each has limits in isolation; the "
                "combination is more robust.",

                "Detection in production. Sample 1% of traffic. Run NLI verification "
                "(natural language inference: does each claim entail from the retrieved "
                "evidence?). Alert when the hallucination rate drifts above baseline. "
                "Without monitoring, you discover hallucination problems through customer "
                "complaints.",
            ],
        },
        {
            "number": "9.6",
            "title": "Metaprompting",
            "paragraphs": [
                "Metaprompting asks the model to improve its own prompt. The intuition: "
                "the model has seen many examples of well-written prompts in training. It "
                "can recognize patterns of good and bad prompts. Use that.",

                "Workflow. Start with a baseline prompt. Show the model a few failure cases. "
                "Ask it to critique the prompt and produce an improved version. Iterate. "
                "A single round of metaprompting often beats a week of human iteration on "
                "the same prompt.",

                "Practical pattern: pair a target LLM (the one running production) with a "
                "stronger model (GPT-4, Claude 3.5 Opus) as the metaprompter. The "
                "metaprompter rewrites prompts for the target. The combination produces "
                "high-quality prompts for cheaper target models.",

                "Caveats. Metaprompting is local optimization. It improves a starting "
                "point. It does not search the global prompt space. For that, you need "
                "programmatic optimization (next section).",
            ],
        },
        {
            "number": "9.7",
            "title": "DSPy: Prompts as Programs You Can Compile",
            "paragraphs": [
                "DSPy (Khattab et al., 2023) treats prompts as programs to be compiled "
                "against an evaluation function. The framework separates declarative "
                "specification (what you want) from prompt optimization (how to elicit it).",

                "Three core abstractions. Signature: typed input-output specification of a "
                "task. Module: a callable composed from signatures (e.g., ChainOfThought "
                "wrapping a signature in CoT reasoning). Optimizer: searches over "
                "instructions and demonstrations to maximize a metric on training data.",

                "Worked example. Classify a customer support ticket into one of seven "
                "categories. Define a signature with input (ticket text) and output "
                "(category label plus reasoning). Wrap in ChainOfThought. Provide a few "
                "labeled examples as training data and an accuracy metric. Compile with "
                "MIPRO (a Bayesian optimizer). The compiler searches over instructions and "
                "demonstration combinations, evaluates each against the metric, and "
                "freezes the best.",

                "Two main optimizers. COPRO does coordinate ascent on instructions: try "
                "many candidate instructions, keep the best. Fast and shallow. MIPRO "
                "jointly optimizes instructions and demonstrations with Bayesian search. "
                "Slower but deeper. Start with COPRO; promote to MIPRO when the gain "
                "plateaus.",

                "When DSPy wins. Complex multi-step pipelines where prompt quality compounds "
                "across steps. Tasks with a clear automated evaluator. Settings where you "
                "can afford the optimization runtime cost. For simple one-shot prompts, "
                "hand-engineering is usually sufficient.",
            ],
        },
        {
            "number": "9.8",
            "title": "Evolutionary Methods: GEPA, TextGrad, ORPO",
            "paragraphs": [
                "DSPy's optimization is structured. Evolutionary methods search a larger "
                "space and can produce better results when DSPy plateaus.",

                "GEPA (Genetic Evolutionary Prompt Optimization). Apply genetic search "
                "(mutation, crossover) to prompts. Use an LLM critic to mutate prompts "
                "intelligently rather than randomly. The reflective critique provides "
                "directional guidance that pure random mutation lacks. Often outperforms "
                "DSPy MIPRO on complex tasks at higher compute cost.",

                "TextGrad (Yuksekgonul et al., 2024). Treat text as a tensor and use a "
                "critic LLM as the gradient. For each output, the critic produces a textual "
                "diff suggesting improvements. Apply the diff. Iterate. The framework "
                "extends naturally to multi-step pipelines where gradients propagate "
                "through textual chains. Strong on tasks where the critic can provide "
                "specific feedback.",

                "ORPO (Odds Ratio Preference Optimization). Unifies preference optimization "
                "with reference-free training. Different from prompt optimization per se, "
                "but relevant as part of the broader 'text as program' toolkit.",

                "When to use what. GEPA: complex tasks where you can afford compute and need "
                "broad exploration. TextGrad: refining an existing prompt with concrete "
                "failure cases. ORPO: when you have preference data and want to fine-tune "
                "rather than just prompt-optimize.",
            ],
        },
        {
            "number": "9.9",
            "title": "Production Prompt Engineering",
            "paragraphs": [
                "Prompt engineering in production is more than crafting a clever prompt. "
                "It is an engineering discipline with versioning, evaluation, monitoring, "
                "and continuous improvement.",

                "Version control. Treat prompts as code. Store in git. Review changes. "
                "Tie each deployed prompt version to specific evaluation results. Roll "
                "back if production metrics degrade.",

                "Evaluation. Hold out a representative test set. Score every prompt change "
                "against it. Track metrics over time. A prompt that wins on the test set "
                "may lose on the long tail of production queries; sample production "
                "traffic for offline scoring.",

                "Monitoring. Track latency, cost (token usage), refusal rate, user "
                "feedback signals (thumbs, regenerate rate). Alert on regressions. A prompt "
                "change that doubles latency or refuses 10% more often than baseline "
                "deserves immediate attention even if accuracy is unchanged.",

                "Continuous improvement. Capture failure cases. Add them to the evaluation "
                "set. Iterate on prompts (or fine-tune) to fix them. Production data is "
                "the most valuable input to prompt improvement.",

                "Prompt injection defense. Treat retrieved content and user input as "
                "untrusted data. Use system-prompt delimiters that untrusted text cannot "
                "reproduce. Strip instruction-like patterns from retrievals. Log suspicious "
                "patterns. Defense in depth: input filters, output filters, structured "
                "output schemas.",
            ],
        },
        {
            "number": "9.10",
            "title": "Summary",
            "bullets": [
                "Prompts are programs. Engineer them with version control, evaluation, "
                "monitoring, and continuous improvement.",
                "CO-STAR provides a structured template: Context, Objective, Style, Tone, "
                "Audience, Response format.",
                "Few-shot examples with diversity, boundary cases, and consistent format "
                "exploit in-context learning effectively.",
                "Chain-of-thought spreads reasoning across tokens, dramatically improving "
                "performance on multi-step tasks. Reasoning models do this natively.",
                "Hallucination mitigation requires grounding (RAG), structured output, and "
                "self-consistency. Combine them.",
                "Metaprompting uses the model to improve its own prompt; DSPy compiles "
                "prompts against an evaluator; GEPA and TextGrad search larger spaces with "
                "evolutionary or gradient-style updates.",
                "Production prompt engineering is iterative: track failures, expand "
                "evaluation, iterate.",
            ],
        },
    ],
    "further_reading": [
        "Khattab et al., 'DSPy: Compiling Declarative LM Calls into Self-Improving Pipelines' (2023).",
        "Wei et al., 'Chain-of-Thought Prompting Elicits Reasoning in Large Language Models' (2022).",
        "Yuksekgonul et al., 'TextGrad: Automatic Differentiation via Text' (2024).",
        "Kojima et al., 'Large Language Models are Zero-Shot Reasoners' (2022).",
    ],
}
