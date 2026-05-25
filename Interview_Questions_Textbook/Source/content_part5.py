"""Part 5: Fine-tuning, Vector DB."""

FINE_TUNING = [
    ("What is fine-tuning?",
     [
        "Fine-tuning is the process of continuing to train a pretrained model on a "
        "smaller, task-specific or domain-specific dataset. The model's weights are "
        "updated so that it specializes for the new task while retaining knowledge from "
        "pretraining.",
        "Why it works: pretraining produces general capabilities; fine-tuning shapes "
        "those capabilities for a specific purpose. A code-completion model fine-tuned on "
        "your company's codebase becomes much better at your internal patterns. A general "
        "LLM fine-tuned on medical notes becomes a credible medical assistant.",
        "Modern variants: full fine-tuning updates every weight. Parameter-efficient "
        "fine-tuning (LoRA, qLoRA, adapters) updates a small additional set of "
        "parameters while keeping the base frozen. Instruction tuning fine-tunes on "
        "(instruction, response) pairs. RLHF aligns the model to human preferences.",
     ],
     ["12_adaptation_ladder.png"]),

    ("Describe the fine-tuning process step by step.",
     [
        "1. Choose a base model. Match capability and size to your task. Smaller models "
        "are cheaper to fine-tune; larger models often produce better results.",
        "2. Prepare data. Collect (input, output) pairs in the format the model expects. "
        "Quality matters more than quantity. Deduplicate, filter, balance.",
        "3. Choose method. Full fine-tuning for maximum quality and ample compute. LoRA "
        "or qLoRA for cost efficiency and to avoid catastrophic forgetting.",
        "4. Configure training. Learning rate (1e-5 to 5e-5 for full FT; 1e-4 to 3e-4 "
        "for LoRA). Batch size as large as fits. Epochs 1-3 typically. Warm-up and decay.",
        "5. Train. Monitor train and validation loss. Watch gradient norm and parameter "
        "norm. Apply early stopping if validation diverges.",
        "6. Evaluate. Held-out test set for the target task. Regression suite for base "
        "capabilities. Compare against base and against alternative methods.",
        "7. Deploy. Merge LoRA into base if applicable. Quantize if needed. Serve behind "
        "vLLM or similar. Monitor in production.",
     ]),

    ("What are different fine-tuning methods?",
     [
        "Full fine-tuning: update every weight. Maximum quality. Highest cost (compute, "
        "memory, storage). Risk of catastrophic forgetting.",
        "LoRA (Low-Rank Adaptation): freeze base; learn a low-rank update BA. Trainable "
        "params drop to 0.5-2% of full. Quality often within 1-2 points of full FT. The "
        "default for most fine-tuning workloads.",
        "qLoRA: LoRA on a 4-bit quantized base. Cuts memory by 4x. Modest accuracy loss "
        "vs LoRA. Enables fine-tuning 70B models on a single 80GB GPU.",
        "Adapters: insert small trainable modules between transformer layers; freeze the "
        "rest. Similar to LoRA in spirit, less popular than LoRA.",
        "Prefix tuning / Prompt tuning: prepend a small set of trainable virtual token "
        "embeddings; freeze the rest. Very few trainable params. Lower quality ceiling "
        "than LoRA.",
        "BitFit: train only bias terms. Tiny parameter footprint. Limited expressiveness.",
        "Instruction tuning: full or LoRA FT on a curated mix of (instruction, response) "
        "pairs to make a base model follow instructions.",
        "RLHF/DPO/GRPO: alignment-stage fine-tuning using human preferences or verifiable "
        "rewards.",
     ],
     ["13_lora.png"]),

    ("When should you fine-tune?",
     [
        "Fine-tune when:",
        "- Prompting alone consistently misses your target quality or format.",
        "- You need a specific persona, tone, or output format the base model doesn't "
        "reliably produce.",
        "- You have a narrow domain where vocabulary or reasoning patterns differ from "
        "general pretraining.",
        "- You have ample examples (typically thousands of high-quality (input, output) "
        "pairs) of the desired behavior.",
        "- Latency and cost favor a smaller fine-tuned model over a larger general one.",
        "Do NOT fine-tune when:",
        "- Your task is primarily about knowledge that changes often (use RAG instead).",
        "- You have very little training data (under a few hundred examples).",
        "- The task is well-handled by prompting and few-shot examples.",
        "- You cannot evaluate the fine-tuned model rigorously (you will not catch "
        "regressions).",
     ]),

    ("What is the difference between fine-tuning and transfer learning?",
     [
        "Transfer learning is the broader concept: take knowledge learned in one setting "
        "and apply it to another. It includes using features from a pretrained model as "
        "input to a new classifier (feature extraction), prompt-based zero/few-shot, RAG, "
        "and fine-tuning.",
        "Fine-tuning is a specific transfer learning technique: continue training the "
        "pretrained model on target data, updating some or all of its weights.",
        "In modern NLP, 'transfer learning' is sometimes used as a synonym for "
        "'fine-tuning' but the broader meaning includes any reuse of pretrained "
        "knowledge.",
     ]),

    ("Write about instruction fine-tuning and explain how it works.",
     [
        "Instruction fine-tuning teaches a base LLM to follow natural-language "
        "instructions. The training data consists of (instruction, response) pairs across "
        "diverse task types: 'Summarize this passage', 'Translate to French', 'Write a "
        "Python function that...'.",
        "Mechanics: standard supervised fine-tuning with a causal LM objective. The "
        "training input is the instruction (and any provided input data); the target is "
        "the desired response. Loss is computed only on response tokens (masking out the "
        "instruction itself).",
        "Why it works: the base model already has strong language modeling capabilities. "
        "Instruction tuning teaches it the pattern of (instruction → response) and "
        "exposes it to many task types. This generalizes: the model becomes good at "
        "instructions it never saw, because it has learned the meta-pattern.",
        "Datasets: FLAN (Google), Alpaca, Dolly, OpenAssistant, ShareGPT-cleaned. Modern "
        "instruction-tuned models (LLaMA-Chat, Mistral-Instruct, Gemma-Instruct) are built "
        "this way.",
     ]),

    ("Explain RLHF in detail.",
     [
        "Reinforcement Learning from Human Feedback is the standard alignment pipeline. "
        "Three stages.",
        "Stage 1: SFT. Supervised fine-tune the base model on (prompt, ideal response) "
        "pairs crafted by humans. The model learns to follow instructions in a desirable "
        "style.",
        "Stage 2: Reward Model. For each prompt, generate multiple responses from the SFT "
        "model. Have humans rank them (typically pairwise). Train a separate reward model "
        "RM(prompt, response) → scalar to predict which response humans prefer. The reward "
        "model encodes 'what humans like.'",
        "Stage 3: Policy optimization. Use the reward model as the reward signal to fine-"
        "tune the SFT model with PPO. Each step: sample a prompt, generate a response, "
        "compute reward = RM(prompt, response) - β · KL(policy || SFT). The KL term "
        "prevents the policy from drifting into reward-hacking regions far from the SFT "
        "distribution.",
        "Result: an LLM that is helpful, harmless, and honest within the limits of the "
        "preference data. Used to train ChatGPT, Claude, LLaMA-Chat. Modern variants "
        "include DPO (skip the reward model), GRPO (drop the value head), and Constitutional "
        "AI (AI feedback instead of human).",
     ],
     ["16_rlhf.png"]),

    ("Write about different RLHF techniques.",
     [
        "Classic RLHF (PPO): three-stage pipeline with SFT, reward model, PPO. Used in "
        "ChatGPT-3.5, Claude-1.",
        "Direct Preference Optimization (DPO): skips the explicit reward model. Trains "
        "directly on preference pairs (prompt, chosen, rejected) using a closed-form "
        "objective derived from the optimal RLHF policy. Simpler pipeline, no sampling at "
        "training time, more stable. Lower compute. Often matches PPO quality.",
        "Group Relative Policy Optimization (GRPO): drops the value network. Sample N "
        "completions per prompt; compute group-relative advantage as reward minus group "
        "mean. Cuts memory by roughly half. Default for math and code RL training "
        "(DeepSeekMath, DeepSeek-R1).",
        "RLAIF (RL from AI Feedback): replace human preferences with AI-generated "
        "preferences. Scales better than human-only. Used in Constitutional AI.",
        "RLVR (RL with Verifiable Rewards): for tasks with checkable correctness (code "
        "compiles, math answer matches), skip the reward model and use the verifier as "
        "reward. Faster, less reward hacking. Used for code, math, theorem proving.",
        "PPO-variants: ReMax, ORPO (preference optimization combined with reference-free "
        "training), KTO (Kahneman-Tversky Optimization).",
     ]),

    ("Explain PEFT in detail.",
     [
        "Parameter-Efficient Fine-Tuning (PEFT) refers to methods that adapt a large "
        "pretrained model by training a small fraction of its parameters (or a small "
        "additional module) while keeping the base frozen.",
        "Motivations: full fine-tuning of a 70B model needs hundreds of GB of GPU memory "
        "and is slow. PEFT methods cut trainable parameters to 0.1-2% of the base while "
        "preserving most quality.",
        "Main families: (a) LoRA-style low-rank updates; (b) adapter modules inserted "
        "between layers; (c) prefix/prompt tuning of trainable virtual tokens; (d) BitFit "
        "training only biases; (e) IA3 scaling activations.",
        "Practical benefits: train multiple task-specific adapters cheaply; swap them at "
        "inference for multi-tenant or multi-task serving; avoid catastrophic forgetting "
        "(base weights stay intact); ship a small adapter file (megabytes) instead of a "
        "full model checkpoint (gigabytes).",
        "Hugging Face's `peft` library is the de facto standard implementation. Supports "
        "LoRA, qLoRA, adapters, prefix tuning, IA3.",
     ]),

    ("What is LoRA and qLoRA?",
     [
        "LoRA (Low-Rank Adaptation): freeze the pretrained weight W. Add a low-rank "
        "update BA where A is r × d and B is d × r, rank r ≪ d (typically r = 4 to 64). "
        "The forward pass becomes W·x + α/r · BA·x. Only B and A are trained. "
        "Trainable parameter count drops to about r·(d_in + d_out) per layer, often 0.5% "
        "to 2% of full fine-tuning. Quality is usually within 1-2 points of full FT.",
        "qLoRA: LoRA on top of a 4-bit quantized base model. The base is loaded in NF4 "
        "(normalized 4-bit floating-point with double quantization). LoRA adapters train "
        "in 16-bit. Memory drops 4x; accuracy typically within 1-2 points of LoRA on 16-bit "
        "base. Enables fine-tuning a 70B model on a single 80GB GPU.",
        "Tradeoffs: very small ranks (r=1, r=2) can hurt quality on tasks with strong "
        "semantic shift. Higher ranks (r=32, r=64) are safer but cost more. The α parameter "
        "scales the contribution; a common rule is α = 2r.",
     ],
     ["13_lora.png"]),

    ("Define pre-training vs fine-tuning in LLMs.",
     [
        "Pre-training: train a model from scratch (or from random init) on a massive "
        "general corpus using a self-supervised objective (causal LM, masked LM). The "
        "result is a base model with broad capabilities but no specific task alignment. "
        "Costs hundreds to thousands of GPU-years for frontier models.",
        "Fine-tuning: continue training a pretrained model on a smaller, task-specific or "
        "alignment dataset. The base model's general capabilities are specialized for the "
        "task. Costs hours to days for most workloads.",
        "Pre-training happens once per model release (very expensive). Fine-tuning happens "
        "many times by many users (much cheaper). The economics of foundation models hinge "
        "on this asymmetry: pay once to pretrain, reuse forever for many fine-tuning "
        "downstream tasks.",
     ]),

    ("How do you train LLMs with billions of parameters?",
     [
        "Distributed training. Three parallelism strategies in combination.",
        "Data parallel: same model on every device, sharded data, all-reduce on gradients. "
        "Default for everything that fits.",
        "Tensor parallel: split each matrix multiplication across devices. Required when "
        "the model is too large for one device.",
        "Pipeline parallel: split layers across devices; stream micro-batches through. "
        "For very large models.",
        "ZeRO/FSDP: shard optimizer states, gradients, and parameters across devices to "
        "fit larger models. Stage 1, 2, 3 shard progressively more.",
        "Mixed precision: store weights in BF16 or FP8; do most computation in low "
        "precision; keep an FP32 master copy of the optimizer state.",
        "Gradient checkpointing: trade compute for memory by recomputing activations "
        "during the backward pass instead of storing them.",
        "Training infrastructure: Megatron-LM, DeepSpeed, Hugging Face Accelerate, Ray "
        "Train, FairScale. Data pipeline: WebDataset or MosaicML Streaming for efficient "
        "streaming. Logging and checkpointing: Weights & Biases, MLflow.",
     ]),

    ("How does LoRA work mechanically?",
     [
        "Pick a pretrained weight matrix W of size d_out × d_in (in a linear or attention "
        "projection). Freeze W.",
        "Initialize a pair of matrices: B (d_out × r) initialized to zero and A (r × d_in) "
        "initialized with a small random distribution. The product BA has the same shape "
        "as W but is constrained to rank r ≪ min(d_in, d_out).",
        "The adapted layer computes: y = W·x + (α/r) · B · A · x. Only B and A receive "
        "gradients during training. The α/r factor scales the LoRA contribution; "
        "α is typically set to 2r so the effective scaling is 2.",
        "At inference: optionally merge by computing W' = W + (α/r) · BA once, store W', "
        "and serve as if it were a plain weight matrix. Zero inference overhead vs the "
        "base model after merging.",
        "Where to apply: query, value (sometimes key), and output projections in attention "
        "layers. Sometimes MLP. The right set is empirical; start with Q, V, O.",
     ],
     ["13_lora.png"]),

    ("How do you train an LLM that prevents prompt hallucinations?",
     [
        "Pretraining: filter the training corpus to favor high-quality, factual sources. "
        "Deduplicate aggressively; duplicates teach the model to be overconfident.",
        "SFT: include high-quality (instruction, response) pairs where the response is "
        "grounded, conservative, and willing to say 'I don't know.' Avoid examples that "
        "reward confident-but-wrong responses.",
        "Reward modeling and RLHF: explicitly reward correct refusals and grounded "
        "answers. Penalize unsupported claims. Add adversarial examples designed to elicit "
        "hallucinations to the preference data.",
        "RAG at inference: ground every response in retrieved evidence. Require citations. "
        "Verify citations match claims with an NLI model.",
        "Calibration training: include examples that teach the model to express "
        "uncertainty appropriately. Self-consistency: sample multiple times and pick the "
        "consistent answer.",
        "Evaluation: build hallucination benchmarks (TruthfulQA, FactScore). Monitor "
        "hallucination rate in production via sampling and offline grounding checks.",
     ]),

    ("How do you prevent bias and harmful prompt generation?",
     [
        "Data curation: filter pretraining and fine-tuning data for harmful content. "
        "Use demographic-balanced datasets. Audit for representation across groups.",
        "Constitutional principles: define explicit principles for desired model behavior. "
        "Use them to filter SFT examples and to generate AI preferences (Constitutional "
        "AI, RLAIF).",
        "RLHF alignment: collect human preferences across diverse demographics. Reward "
        "responses that avoid stereotypes and harmful content.",
        "System prompts: production deployments add a system prompt that establishes "
        "behavior rules, including refusal of harmful requests.",
        "Inference-time guardrails: input filters (intent classification, content "
        "moderation) and output filters (toxicity, PII, hate speech detection). "
        "Multi-layer defense.",
        "Red teaming: actively probe the model for failure modes before deployment. "
        "Continuous adversarial evaluation in production.",
        "Transparency: publish model cards documenting known limitations and bias.",
     ]),

    ("How does proximal policy gradient (PPO) work in prompt generation?",
     [
        "PPO is a reinforcement learning algorithm used to optimize an LLM's generation "
        "policy against a reward signal.",
        "Setup: the LLM is the policy π_θ(a|s). State s = prompt + tokens generated so "
        "far. Action a = next token. Reward = signal from a reward model or programmatic "
        "verifier, typically only at the end of generation.",
        "PPO objective: max over θ of E[ min(r_t · A_t, clip(r_t, 1-ε, 1+ε) · A_t) ], "
        "where r_t = π_θ(a_t|s_t) / π_old(a_t|s_t) is the probability ratio and A_t is "
        "the advantage. The clip term prevents oversized updates that would destabilize "
        "training.",
        "KL penalty: in RLHF, add -β · KL(π_θ || π_SFT) to keep the policy near the "
        "SFT reference. Without this, the policy drifts off-manifold and reward-hacks.",
        "Practical notes: small learning rates (1e-6 to 5e-6). KL coefficient typically "
        "0.01 to 0.1, tuned to balance reward chasing vs staying on-manifold. Reward "
        "normalization important for stability.",
     ]),

    ("How does knowledge distillation benefit LLMs?",
     [
        "Knowledge distillation transfers knowledge from a large teacher model to a "
        "smaller student model. The student is trained to match the teacher's outputs "
        "(soft labels) rather than just ground-truth labels.",
        "Why it helps: the teacher's soft probability distribution carries more "
        "information than hard labels. The student learns relative similarities ('this is "
        "more like a cat than a dog'), which improves generalization.",
        "For LLMs: distill a 70B teacher into a 7B student that runs much faster and "
        "cheaper. The student typically loses 1-5 points on benchmarks but offers 10-50x "
        "inference speedup. Examples: DistilBERT (from BERT), TinyLLaMA, Vicuna (from "
        "ChatGPT outputs).",
        "Distillation strategies: response-based (match output logits), feature-based "
        "(match intermediate representations), relation-based (match relationships between "
        "examples). Combinations work best.",
        "Modern pattern: train a strong teacher with RLHF; collect its outputs on diverse "
        "prompts; fine-tune a smaller student on those outputs (synthetic SFT). Most "
        "open-source instruction-tuned models use some form of distillation from "
        "stronger models.",
     ]),

    ("What is few-shot learning in LLMs?",
     [
        "Few-shot learning is the ability to learn a new task from a small number of "
        "examples provided at inference time, without weight updates. Examples are passed "
        "in the prompt itself, a technique called in-context learning.",
        "Pattern: a prompt with 1-5 examples of (input, output) pairs followed by a new "
        "input. The model continues the pattern by producing the output for the new "
        "input.",
        "Zero-shot: no examples, just an instruction. Few-shot: a handful of examples. "
        "Many-shot: dozens to hundreds, fitting in long contexts.",
        "Mechanism: the LLM has learned the meta-task of pattern continuation during "
        "pretraining. Few-shot examples specify the task implicitly. No backprop, no "
        "weight changes.",
        "Limits: prompt length is finite. Quality plateaus after 5-10 examples for "
        "most tasks. Sensitive to example ordering and selection. For better quality with "
        "abundant examples, use RAG (retrieve relevant examples per query) or fine-tune.",
     ]),

    ("How do you evaluate LLM performance metrics?",
     [
        "Intrinsic: perplexity on held-out text. Useful sanity check but only weakly "
        "correlated with utility.",
        "Generation: BLEU/ROUGE for reference-based tasks; BERTScore for semantic "
        "similarity; CIDEr for captioning; LLM-as-a-judge for open-ended.",
        "Reasoning: MMLU (multi-domain knowledge), HellaSwag (commonsense), GSM8K, MATH "
        "(math), BIG-Bench (diverse hard tasks), ARC (science), TruthfulQA (factuality).",
        "Code: HumanEval, MBPP, LiveCodeBench (pass@k on programming problems).",
        "Chat: MT-Bench, Chatbot Arena (human preference at scale).",
        "Safety: ToxiGen, BBQ (bias benchmark), AdvBench (jailbreak resistance), "
        "WMDP (dangerous capability).",
        "RAG: Ragas (faithfulness, answer relevance, context precision, context recall), "
        "RGB (robustness against noise, negatives, integration, counterfactuals).",
        "Production: latency, throughput, cost per query, user satisfaction signals "
        "(thumbs, regenerate rate), retention.",
     ]),

    ("How would you use RLHF to train an LLM?",
     [
        "Step 1: SFT. Curate or buy a high-quality instruction dataset. Fine-tune the base "
        "model on (prompt, response) pairs. 1-3 epochs, LR 1e-5 to 5e-5.",
        "Step 2: Collect preferences. Generate multiple responses per prompt using the SFT "
        "model. Have humans rank them pairwise. Aim for 30K to 100K preference pairs.",
        "Step 3: Train reward model. Initialize from the SFT model or a same-family base. "
        "Train to predict P(response A > response B | prompt). Standard cross-entropy on "
        "preference pairs.",
        "Step 4: PPO. Initialize policy from SFT. Initialize reference from SFT. For each "
        "step: sample prompts, generate responses from the policy, score with the reward "
        "model, compute advantages, take a PPO step with a KL penalty against the "
        "reference. Run for 1-5K steps.",
        "Step 5: Evaluate. Held-out preference pairs, MT-Bench, safety benchmarks. "
        "Compare against base and SFT. Iterate on the reward model and PPO settings.",
        "Variants: DPO (skip steps 3-4, train directly on preferences) for cost; GRPO "
        "(skip the value head) for memory; RLAIF (AI-generated preferences) for scale.",
     ],
     ["16_rlhf.png"]),

    ("What techniques improve factual accuracy in LLM-generated text?",
     [
        "RAG: ground generation in retrieved evidence. The single biggest factuality "
        "improvement available.",
        "Citations: require the model to cite sources for claims; verify citations.",
        "Self-consistency: sample N answers; vote on the majority answer.",
        "Chain-of-thought: explicit reasoning steps surface errors and improve correctness "
        "on multi-step tasks.",
        "Tool use: call external tools (calculator, search, code execution) instead of "
        "relying on parametric memory for verifiable facts.",
        "NLI verification: verify each claim against retrieved evidence with an NLI model; "
        "block or flag unsupported claims.",
        "Fine-tuning on factual data: SFT on high-quality factual sources; preference "
        "learning that prefers correct over incorrect responses.",
        "Lower temperature: reduces creative drift for factual tasks.",
        "Constrained decoding: force the output to match a schema or to be drawn from a "
        "fixed set of valid options when applicable.",
     ]),

    ("How do you detect drift in LLM performance over time?",
     [
        "Baseline benchmarks: fix a held-out evaluation set. Re-run the benchmarks on a "
        "schedule (daily, weekly). Track metrics over time. Alert on regressions.",
        "Production sampling: sample 1-5% of production traffic. Score offline with "
        "automated metrics and periodic human review.",
        "User feedback signals: thumbs up/down, regenerate rate, conversation length, "
        "abandonment. Trend over time. Segment by query type.",
        "Distribution drift: monitor the input distribution. Embed queries and detect "
        "shifts in embedding space. Alert when the production distribution diverges from "
        "the evaluation distribution.",
        "Output drift: track output statistics (length, sentiment, refusal rate). "
        "Sudden shifts often indicate a problem.",
        "Canary deployments: shadow-deploy new model versions and compare metrics before "
        "promotion.",
        "Causes of drift: data distribution change (users ask different questions over "
        "time), upstream service changes (a tool the model relies on changed), model "
        "version updates by the provider (silent prompt-response changes).",
     ]),

    ("Strategies for curating high-quality training data for generative AI?",
     [
        "Quality filtering: deduplicate (exact and near-duplicate); remove low-quality "
        "sources (boilerplate, machine-translated, spam); filter for fluency.",
        "Domain coverage: ensure the data spans the topics, tasks, and styles your model "
        "should handle. Underrepresented topics produce weak capabilities.",
        "Toxicity and safety filtering: remove harmful content, but preserve enough "
        "negative examples to teach the model to recognize and refuse them.",
        "Source diversity: web alone is biased; supplement with books, scientific "
        "papers, code, structured data, multilingual sources.",
        "Annotation quality: for SFT and preference data, hire skilled annotators, "
        "provide clear guidelines, run pilot rounds, measure inter-annotator agreement.",
        "Data provenance and licensing: track sources and licenses. Sensitive in 2025+ "
        "with growing legal scrutiny.",
        "Validation: hold out a clean test set that was never in the training pipeline. "
        "Decontaminate.",
        "Iteration: data curation is iterative. Train, evaluate, identify failure modes, "
        "augment data to fix them, retrain.",
     ]),

    ("Methods to identify and address biases in training data?",
     [
        "Demographic analysis: measure representation across protected attributes (race, "
        "gender, age, language). Quantify imbalances.",
        "Topic and source analysis: which topics dominate? Which sources contribute most? "
        "Are minority perspectives represented?",
        "Embedding analysis: cluster the data in embedding space; look for over- or "
        "under-represented clusters.",
        "Bias benchmarks for evaluation: BBQ, StereoSet, CrowS-Pairs measure stereotype "
        "and bias in language models.",
        "Mitigation: oversample underrepresented groups; downsample overrepresented ones; "
        "augment with synthetic balanced data; train with bias-mitigation objectives "
        "(adversarial debiasing, contrastive debiasing).",
        "Process: bias review board, diverse annotation team, transparent documentation "
        "of training data choices (Datasheets for Datasets, Model Cards).",
     ]),

    ("How would you fine-tune an LLM for a financial or medical domain?",
     [
        "Data: collect domain-specific text: clinical notes, medical literature, financial "
        "reports, regulatory filings. Get permission and ensure compliance (HIPAA, "
        "GDPR, SOC 2). Apply PII redaction.",
        "Vocabulary: extend the tokenizer with domain-specific terms (drug names, "
        "ticker symbols, ICD codes) and briefly continue pretraining so the new tokens "
        "learn meaningful embeddings.",
        "Continued pretraining: optional brief pass of LM objective on domain text "
        "before instruction tuning. Helps with domain vocabulary and patterns.",
        "Instruction tuning: curate (instruction, response) pairs from domain experts. "
        "Include question answering, summarization, structured extraction, common "
        "domain tasks.",
        "RLHF or DPO: use domain experts to rate responses for accuracy, helpfulness, "
        "safety. Higher cost but produces better-calibrated models.",
        "RAG over domain knowledge bases for current information. Fine-tuning teaches "
        "behavior; RAG provides facts.",
        "Evaluation: domain-specific benchmarks (MedQA, FinanceBench), expert review "
        "panels. Compliance review for regulated outputs. Continuous monitoring after "
        "deployment.",
     ]),

    ("Explain the architecture of LLaMA and similar modern LLMs.",
     [
        "LLaMA is a decoder-only transformer with several modern refinements over the "
        "original architecture.",
        "Pre-normalization: RMSNorm applied before each sub-layer (attention and FFN) "
        "instead of after. Stabilizes training at scale.",
        "Rotary Position Embeddings (RoPE): apply position information by rotating the Q "
        "and K vectors. Better length extrapolation than absolute positional encoding.",
        "SwiGLU activation in the FFN: a gated variant of Swish/SiLU. Slightly better "
        "quality than ReLU or GELU at similar compute.",
        "Grouped-Query Attention (GQA) in LLaMA-2 70B and LLaMA-3: fewer KV heads than Q "
        "heads, reducing KV-cache size and speeding up inference.",
        "Tied embeddings (sometimes): share input and output token embeddings to save "
        "parameters.",
        "Training: trillions of tokens of mixed web, code, books. SFT, then DPO or RLHF "
        "for the chat variants.",
        "Family: Mistral, Mixtral (MoE), Gemma, Qwen, Yi, Falcon all share most of these "
        "design choices. Modern decoder-only LLMs have converged on a similar template.",
     ]),
]


VECTOR_DB = [
    ("What are vector databases, and how do they differ from relational databases?",
     [
        "A vector database stores high-dimensional vector embeddings and supports similarity "
        "search: given a query vector, return the most similar stored vectors. Relational "
        "databases store structured rows and support exact lookups, joins, and range "
        "queries via SQL.",
        "Use cases: vector DB for semantic search, recommendation, RAG, image search, "
        "duplicate detection, anomaly detection. Relational DB for transactions, "
        "reporting, structured queries.",
        "Differences: vector DB indexes are ANN structures (HNSW, IVF, PQ), not B-trees. "
        "Vector DBs typically also store metadata for filtering. Many production stacks "
        "use both: relational for source of truth, vector for similarity search.",
     ]),

    ("Explain how vector embeddings are generated and their role.",
     [
        "Generation: pass the raw input (text, image, audio) through a neural encoder. "
        "Text: a sentence transformer (BGE, GTE, E5, mpnet) or an LLM embedding endpoint "
        "(OpenAI ada, Cohere). Image: a vision encoder (CLIP, ViT). Audio: an audio "
        "encoder (Wav2Vec, Whisper encoder).",
        "Role in vector DB: embeddings turn unstructured data into vectors that can be "
        "indexed and searched by similarity. The geometry of the embedding space encodes "
        "semantic relationships, so 'nearest in vector space' approximates 'most similar "
        "in meaning'.",
        "Quality matters: the embedder choice determines retrieval quality. Domain-tuned "
        "embedders typically beat general-purpose ones on specialized corpora. Track "
        "Recall@k against a held-out test set to compare options.",
     ],
     ["15_embeddings.png"]),

    ("What are the challenges of indexing and searching high-dimensional vector spaces?",
     [
        "Curse of dimensionality: in high dimensions, distances concentrate (max and min "
        "distance to random points become similar). Naive nearest neighbor search loses "
        "discriminating power.",
        "Compute cost: brute-force search is O(n·d) per query. For 100M vectors at 768 "
        "dimensions, that is 75GB scanned per query. Impractical.",
        "Memory: even a billion 768-dim float32 vectors is 3TB. ANN indexes need clever "
        "structures (HNSW graphs, IVF clusters, product quantization) to fit and stay "
        "fast.",
        "Accuracy vs speed: ANN trades a small recall loss for orders of magnitude "
        "speedup. Tuning the recall-speed tradeoff is application-specific.",
        "Updates: insertion and deletion in indexes like HNSW are not free. Some indexes "
        "require periodic rebuilds.",
        "Hybrid queries: combining vector similarity with metadata filters (e.g., search "
        "for documents in this category only) requires careful index design.",
     ],
     ["14_ann_search.png"]),

    ("How do you evaluate a vector database's performance?",
     [
        "Recall@k: fraction of true top-k neighbors returned. The most important quality "
        "metric.",
        "Latency: P50 and P95 query latency. Production targets: under 50 ms P95 for "
        "interactive, under 500 ms for batch.",
        "Throughput: queries per second under sustained load. Test at expected load and "
        "at 2-3x to find limits.",
        "Index build time: how long to add N new vectors? Some indexes (HNSW) are slow "
        "to build; others (IVF) are faster.",
        "Memory footprint: RAM per million vectors. Tighter is cheaper.",
        "Update behavior: insertion latency, deletion semantics, eventual consistency.",
        "Filter performance: hybrid queries with metadata filters; effective filter "
        "push-down vs post-filtering.",
        "Methodology: build a held-out evaluation set with known ground-truth nearest "
        "neighbors. Test at the index sizes you'll deploy, not at toy scale.",
     ]),

    ("Describe a scenario where you'd prefer a vector DB over a traditional DB.",
     [
        "Semantic search over enterprise documents: users ask natural-language questions "
        "that need to match meaning, not keywords. A relational DB cannot do this. A "
        "vector DB indexes document embeddings and returns relevant chunks for the query.",
        "Recommendation: 'find products similar to this one.' Embed products; ANN search "
        "for nearest. Relational DBs handle facets and filters; vector DBs handle the "
        "similarity.",
        "Image search: 'find images that look like this one.' CLIP embeddings indexed in "
        "a vector DB.",
        "Duplicate or near-duplicate detection: embed everything, compute pairwise "
        "similarity at scale.",
        "RAG: the most common modern use case. Embed knowledge base; retrieve at query "
        "time for grounding LLM responses.",
        "Combined patterns: a hybrid system with relational metadata, full-text search "
        "(BM25), and vector similarity is the gold standard for production search.",
     ]),

    ("What are some popular vector databases?",
     [
        "Pinecone: managed, serverless, easy to start, expensive at scale.",
        "Weaviate: open-source and managed, GraphQL API, hybrid search.",
        "Qdrant: open-source, Rust-based, fast, strong metadata filtering.",
        "Milvus: open-source, mature, supports many index types and scales to billions.",
        "Chroma: lightweight, embeddable, good for prototyping.",
        "FAISS (library, not a DB): Facebook's library for ANN search. Powers many "
        "custom solutions and is embedded in tools like LangChain.",
        "pgvector: PostgreSQL extension for vector search. Good when you already use "
        "Postgres and don't need extreme scale.",
        "Elasticsearch and OpenSearch: added vector search to their full-text engines. "
        "Best when you want hybrid sparse+dense out of the box.",
        "Vespa, MyScale, LanceDB, Marqo: also strong contenders depending on use case.",
        "Selection criteria: scale, latency targets, hybrid search needs, hosting "
        "preference, ecosystem maturity, cost.",
     ]),

    ("How do vector databases support ML workflows?",
     [
        "Feature store role: store entity embeddings (user, item, document) for downstream "
        "models to consume. Embeddings become reusable features across tasks.",
        "Real-time inference: a recommendation service embeds the user query/context, "
        "calls the vector DB for nearest items, returns recommendations. Sub-100ms "
        "round-trip.",
        "Model serving augmentation: in a RAG system, the vector DB is the retrieval "
        "layer between user query and LLM.",
        "Training data sampling: nearest-neighbor queries find similar examples for "
        "few-shot prompting, active learning, or contrastive training.",
        "Model evaluation: embed eval set; find similar training examples; check for "
        "leakage and contamination.",
        "Deduplication: at ingestion time, find near-duplicates and dedupe before "
        "training.",
        "Monitoring: embed production traffic; track drift in embedding space; detect "
        "anomalies.",
     ]),

    ("What techniques ensure vector DB scalability?",
     [
        "Sharding: split the index across nodes by vector ID or hash. Each query fans "
        "out to all shards, aggregates results. Linear scaling on read.",
        "Replication: multiple replicas per shard for read throughput and fault tolerance.",
        "Hierarchical indexes (HNSW): naturally scale to billions of vectors with good "
        "query latency.",
        "IVF + PQ: cluster vectors into IVF buckets; quantize within each bucket with "
        "PQ. Trades memory for speed and is the standard for very large indexes.",
        "Tiered storage: hot data in RAM, warm in SSD, cold in object storage. Acceptable "
        "if query patterns are skewed.",
        "Incremental indexing: avoid full rebuilds. Pinecone, Qdrant, and Milvus support "
        "online updates.",
        "Quantization: int8 or binary embeddings shrink memory 4-32x. Use for first-"
        "stage retrieval with re-ranking in higher precision.",
        "Caching: semantic cache for repeated queries; embedding cache for repeated "
        "documents.",
     ]),

    ("How do you handle vectors of different dimensionalities?",
     [
        "Normalize first: most vector DBs assume vectors have a fixed dimension per "
        "collection. Embed everything with the same model or with models that produce "
        "the same dimension.",
        "Matryoshka embeddings: a single embedder trained to produce useful representations "
        "at multiple truncation lengths. Lets you use 64-dim for cheap prune and 768-dim "
        "for fine scoring.",
        "Projection: project vectors of different dimensions into a common space with a "
        "learned linear projection. Useful when you have multi-modal embedders that "
        "produce different dimensions.",
        "Separate indexes per dimension: maintain one index per embedder. Query the "
        "right one based on the input type. Combine results post-hoc.",
        "Dimensionality reduction: PCA or random projection to reduce all vectors to a "
        "common smaller dimension. Loses some recall.",
     ]),

    ("What role does vector similarity play in recommendation and NLP?",
     [
        "Recommendation: embed users and items in the same space (collaborative filtering "
        "or two-tower models). Similarity = predicted affinity. Nearest items to a user's "
        "embedding are the recommendations. Scales to billions of items with ANN.",
        "NLP: embedding similarity is the core operation in semantic search, retrieval-"
        "augmented generation, clustering, classification (via prototypes), and similarity-"
        "based reasoning.",
        "Similarity functions: cosine similarity is the standard. Dot product is "
        "equivalent for L2-normalized vectors. Euclidean distance is sometimes used but "
        "behaves worse in high dimensions.",
        "Production patterns: retrieval at a coarse similarity threshold, followed by "
        "fine reranking with a stronger model. Hybrid combining vector similarity with "
        "lexical (BM25) and structured (metadata filter) constraints.",
        "Limitations: similarity does not imply relevance for all tasks. A semantically "
        "similar passage may not contain the answer. Reranking and grounding steps "
        "close this gap.",
     ]),
]
