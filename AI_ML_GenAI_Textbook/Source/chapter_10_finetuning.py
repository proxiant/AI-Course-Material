"""Chapter 10: Fine-Tuning Large Language Models."""

CHAPTER = {
    "label": "Chapter 10",
    "title": "Fine-Tuning Large Language Models",
    "intro_image": "12_adaptation_ladder.png",
    "intro_caption": "Figure 10.1: The adaptation ladder for LLMs.",
    "sections": [
        {
            "number": "10.1",
            "title": "The Adaptation Ladder",
            "paragraphs": [
                "Adapting a pretrained LLM to a specific use case can be done at many levels "
                "of cost and control. From cheapest to most powerful: prompt engineering, "
                "few-shot in-context examples, retrieval-augmented generation, parameter-"
                "efficient fine-tuning, and full fine-tuning. Each rung trades more "
                "engineering effort and compute for more control over model behavior.",

                "The right rung depends on three questions. Do you need to change knowledge "
                "(RAG wins) or behavior (fine-tuning wins)? How much labeled data do you "
                "have (less = lower rungs)? How much compute can you afford (full fine-"
                "tuning is most expensive)?",

                "This chapter covers the upper rungs: supervised fine-tuning (SFT), "
                "parameter-efficient fine-tuning (PEFT) including LoRA and qLoRA, and the "
                "full fine-tuning pipeline. Chapter 11 covers alignment fine-tuning with "
                "reinforcement learning (RLHF, DPO, GRPO).",
            ],
        },
        {
            "number": "10.2",
            "title": "When to Fine-Tune",
            "paragraphs": [
                "Fine-tune when prompt engineering plateaus and you need:",
                "- A specific persona, tone, or output format the base model doesn't "
                "reliably produce.",
                "- A narrow domain where vocabulary or reasoning patterns differ from "
                "general pretraining.",
                "- Latency or cost advantages from a smaller specialized model versus a "
                "larger general one.",
                "- Behavior changes (refusal patterns, format consistency) that prompting "
                "cannot consistently elicit.",

                "Do not fine-tune when:",
                "- Your task is primarily about knowledge that changes often. Use RAG; "
                "fine-tuning bakes knowledge in opaquely and goes stale.",
                "- You have very little training data. Under a few hundred examples, "
                "fine-tuning produces noisy models. Prompt engineering wins.",
                "- You cannot evaluate the fine-tuned model rigorously. Without evaluation, "
                "you will not catch regressions, catastrophic forgetting, or subtle quality "
                "drops.",

                "A common pattern: prompt engineering plus RAG for the first six months. "
                "Fine-tune only after the prompting approach hits a clear ceiling and you "
                "have collected enough labeled data from production to train confidently.",
            ],
        },
        {
            "number": "10.3",
            "title": "Supervised Fine-Tuning (SFT)",
            "paragraphs": [
                "Supervised fine-tuning continues training a pretrained model on labeled "
                "(input, output) pairs. The objective is the same causal language modeling "
                "loss used in pretraining, but the data is task-specific or domain-"
                "specific.",
            ],
            "subsections": [
                {
                    "title": "10.3.1 Data Preparation",
                    "paragraphs": [
                        "Quality matters more than quantity. A few thousand high-quality "
                        "(instruction, response) pairs often outperform tens of thousands of "
                        "noisy ones.",
                        "Format the data as the model expects. Use the chat template that "
                        "matches the model (LLaMA uses a specific structure; Mistral uses "
                        "another). Mismatched chat templates often cause silently poor "
                        "results.",
                        "Mask the loss appropriately. Compute the loss only on response "
                        "tokens, not on instruction tokens. Otherwise the model wastes "
                        "capacity learning to predict the instruction back, which is not "
                        "useful.",
                        "Deduplicate. Near-duplicates inflate the importance of common "
                        "patterns and cause memorization. Run deduplication via MinHash or "
                        "exact-match before training.",
                    ],
                },
                {
                    "title": "10.3.2 Hyperparameters",
                    "paragraphs": [
                        "Learning rate. Full fine-tuning of a 7B model typically uses 1e-5 to "
                        "5e-5. LoRA can go higher: 1e-4 to 3e-4. Too high and the model "
                        "diverges or forgets pretraining. Too low and training is slow.",
                        "Batch size. As large as fits on your hardware. Gradient accumulation "
                        "helps if a single forward pass does not fit.",
                        "Epochs. One to three. More risks overfitting. Watch validation loss; "
                        "early stop if it rises.",
                        "Warm-up. Linearly increase learning rate over the first 1-5% of "
                        "steps. Prevents large initial updates that destabilize the model.",
                        "Decay. Cosine decay after warm-up is the modern default. Linear "
                        "decay also works.",
                        "Weight decay. 0.01 to 0.1. Helps regularize.",
                    ],
                },
                {
                    "title": "10.3.3 Monitoring",
                    "paragraphs": [
                        "Train loss should decrease smoothly. Validation loss should track "
                        "train loss closely; divergence signals overfitting. Gradient norm "
                        "should be stable, typically 0.5-5.0; spikes signal instability and "
                        "may require gradient clipping or lower learning rate.",
                        "Evaluate periodically on the target task plus a regression suite. "
                        "The target task tells you whether you are getting the desired "
                        "improvement; the regression suite catches catastrophic forgetting.",
                    ],
                },
            ],
        },
        {
            "number": "10.4",
            "title": "Parameter-Efficient Fine-Tuning (PEFT)",
            "paragraphs": [
                "Full fine-tuning updates every weight of the model. For a 70B model, this "
                "requires hundreds of GB of GPU memory and produces a 70B-parameter "
                "checkpoint per fine-tuned variant. Storing many variants becomes expensive. "
                "Serving them requires loading the full model each time.",

                "Parameter-efficient fine-tuning methods adapt the model by training a "
                "small additional set of parameters while keeping the base frozen. "
                "Trainable parameter count drops to 0.1-2% of the base. Storage per "
                "variant drops accordingly. Many variants can share the same base model in "
                "memory.",
            ],
        },
        {
            "number": "10.5",
            "title": "LoRA: Low-Rank Adaptation",
            "image": "13_lora.png",
            "caption": "Figure 10.2: LoRA adds a low-rank update to a frozen weight.",
            "paragraphs": [
                "LoRA (Hu et al., 2021) is the dominant PEFT method. The insight: when a "
                "pretrained weight matrix W is adapted to a new task, the change ΔW tends "
                "to be low-rank. So instead of training ΔW directly, train it as the "
                "product of two small matrices B and A, where the rank r is small.",

                "Mechanics. Freeze W. Initialize B (d_out × r) to zero and A (r × d_in) "
                "with a small random distribution. The adapted layer computes y = Wx + "
                "(α/r) · B · A · x. Only B and A are trained. The α/r factor scales the "
                "LoRA contribution; α is typically set to 2r so the effective scaling is 2.",

                "Trainable parameters per layer: r · (d_in + d_out). For a 4096-dim layer "
                "with r=16, that is 131K parameters per layer instead of 16.7M. A typical "
                "configuration trains 0.5-2% of the full model.",

                "Where to apply. Q, V, and O projections in attention layers are the "
                "default. Sometimes K, sometimes MLP. The right set is empirical; start "
                "with Q, V, O. LoRA-on-everything is sometimes useful for harder tasks.",

                "Rank selection. r=4 to r=8 for style and format changes. r=16 to r=32 for "
                "domain adaptation. r=64+ for tasks with strong semantic shift. Higher r "
                "costs more but offers more capacity. Per-layer rank schedules sometimes "
                "outperform uniform allocation.",

                "Merging at inference. Compute W' = W + (α/r)BA once. Store W' as a "
                "plain weight matrix. Zero inference overhead vs the base model after "
                "merging. The price is losing the modularity of swapping adapters.",
            ],
        },
        {
            "number": "10.6",
            "title": "qLoRA: Quantized LoRA",
            "paragraphs": [
                "qLoRA (Dettmers et al., 2023) combines LoRA with aggressive base model "
                "quantization. The base model is loaded in 4-bit NF4 (Normalized Float 4) "
                "with double quantization. LoRA adapters train in 16-bit on top.",

                "Memory savings. A 70B model in fp16 needs roughly 140GB. In 4-bit, it "
                "fits in 35-40GB. With LoRA adapters and optimizer state, fine-tuning a "
                "70B model fits on a single 80GB A100 or H100. Without qLoRA, it would "
                "require multiple GPUs.",

                "Quality. Within 1-2 points of LoRA on most tasks. Quality is preserved "
                "remarkably well given the aggressive quantization. The trick: NF4 is "
                "designed to match the distribution of typical neural network weights "
                "(approximately normal), so the quantization error is small.",

                "Limitations. Very small base models (under 1B) may degrade more. Very long "
                "contexts can amplify quantization error. Inference still requires "
                "dequantization unless served in quantized form.",

                "Practical pattern. Fine-tune with qLoRA on a single GPU. Merge the LoRA "
                "into a higher-precision base for production serving, or serve the LoRA "
                "separately on top of a quantized base.",
            ],
        },
        {
            "number": "10.7",
            "title": "Other PEFT Methods",
            "paragraphs": [
                "LoRA dominates production PEFT but is not the only option.",

                "Adapters (Houlsby et al., 2019). Insert small trainable modules between "
                "transformer layers. Similar in spirit to LoRA. Less popular because "
                "LoRA's merge-into-base trick eliminates inference overhead, while "
                "adapter modules persist at inference.",

                "Prefix tuning (Li and Liang, 2021). Train a small set of learnable "
                "virtual token embeddings prepended to every layer's key and value. Very "
                "few trainable parameters. Lower quality ceiling than LoRA on most tasks.",

                "Prompt tuning (Lester et al., 2021). Like prefix tuning but only at the "
                "input layer. Even fewer parameters. Mostly useful for very large models "
                "where even LoRA is too expensive.",

                "IA3 (Liu et al., 2022). Train multiplicative scaling vectors on key, "
                "value, and FFN activations. Tiny trainable surface. Competitive on some "
                "tasks.",

                "BitFit (Ben-Zaken et al., 2021). Train only the bias terms. Even smaller. "
                "Useful for very narrow adaptations.",

                "Use LoRA or qLoRA as your default. The other methods solve specific "
                "problems that rarely arise in production.",
            ],
        },
        {
            "number": "10.8",
            "title": "Instruction Tuning",
            "paragraphs": [
                "Base LLMs predict the next token. They are good at continuing text but bad "
                "at following instructions. Instruction tuning fine-tunes them on a curated "
                "set of (instruction, response) pairs covering diverse tasks: summarize, "
                "translate, classify, write code, answer questions.",

                "Why it works. The base model already has language modeling capability. "
                "Instruction tuning teaches the pattern of (instruction → response) and "
                "exposes the model to many task types. This generalizes: the model becomes "
                "good at instructions it has never seen, because it has learned the meta-"
                "pattern of how instructions map to responses.",

                "Datasets. FLAN (Google), Alpaca (Stanford), Dolly (Databricks), "
                "OpenAssistant, ShareGPT, UltraChat. Modern instruction-tuned models (LLaMA-"
                "3-Instruct, Mistral-Instruct, Gemma-Instruct) are built from these "
                "datasets, often combined.",

                "Common pitfalls. Instruction-tuning on synthetic data from a stronger "
                "model (distillation): produces models that imitate the teacher but inherit "
                "its biases and weaknesses. Instruction-tuning without diversity: produces "
                "a model that does one thing well but generalizes poorly. Instruction-"
                "tuning without preference data: produces a model that follows "
                "instructions but may not be helpful or safe (alignment requires the next "
                "chapter's techniques).",
            ],
        },
        {
            "number": "10.9",
            "title": "Catastrophic Forgetting",
            "paragraphs": [
                "Aggressive fine-tuning can degrade the model's performance on tasks it "
                "previously handled well. This is catastrophic forgetting. Weights that "
                "encoded old knowledge get overwritten by gradients from the new task.",

                "Symptoms. The fine-tuned model is good at the target task. It is worse at "
                "general reasoning, math, or code. It refuses inappropriately or loses "
                "safety behavior. It becomes overly verbose or develops a strange tone.",

                "Mitigations. PEFT (LoRA, qLoRA) limits the surface area of changes, "
                "naturally reducing forgetting. Mix general data with task data; even "
                "10-30% general data dramatically reduces forgetting. Lower learning rates. "
                "Fewer epochs. Layer-wise learning rate decay (smaller LR for earlier "
                "layers).",

                "Detection. Maintain a regression suite of general benchmarks (MMLU, "
                "HumanEval, GSM8K, BBH). Run it before and after fine-tuning. Any "
                "regression above noise is a red flag.",

                "Elastic Weight Consolidation (EWC) and similar regularizers penalize "
                "large changes to weights deemed important for old tasks. Powerful in "
                "principle, expensive in practice; rarely used in production LLM fine-"
                "tuning. PEFT plus data mixing covers most cases.",
            ],
        },
        {
            "number": "10.10",
            "title": "Distillation",
            "paragraphs": [
                "Knowledge distillation transfers knowledge from a large teacher model to a "
                "smaller student model. The student is trained to match the teacher's "
                "outputs (soft labels) rather than just ground-truth labels.",

                "Why it helps. The teacher's soft probability distribution carries more "
                "information than hard labels. The student learns relative similarities "
                "('this is more like a cat than a dog'), which improves generalization.",

                "For LLMs. Distill a 70B teacher into a 7B student that runs much faster "
                "and cheaper. The student typically loses 1-5 points on benchmarks but "
                "offers 10-50x inference speedup. Examples: DistilBERT (from BERT), "
                "TinyLLaMA, Vicuna (from ChatGPT outputs).",

                "Distillation strategies. Response-based: match output logits or generated "
                "text. Feature-based: match intermediate representations. Relation-based: "
                "match relationships between examples. Combinations work best.",

                "Modern pattern. Train a strong teacher with full RLHF. Collect its "
                "outputs on diverse prompts. Fine-tune a smaller student on those outputs "
                "(synthetic SFT). Most open-source instruction-tuned models use some form "
                "of distillation from stronger models.",
            ],
        },
        {
            "number": "10.11",
            "title": "Evaluating Fine-Tuned Models",
            "paragraphs": [
                "Define the task and the metric before starting. Don't move the goalposts "
                "after training.",

                "Baseline. Measure the base model's performance on a held-out test set. "
                "This is the bar to beat.",

                "Fine-tune. Train. Track training and validation loss.",

                "Evaluate fine-tuned model on the same held-out test set with the same "
                "metric. Compare to baseline. Compute confidence intervals via bootstrap "
                "to avoid celebrating noise.",

                "Regression suite. Measure base capabilities (MMLU, HumanEval, GSM8K, "
                "instruction following) to detect catastrophic forgetting.",

                "Qualitative review. Read a sample of outputs from both models on "
                "representative queries. Note systematic differences.",

                "A/B test in production. If both pass offline checks, route a fraction of "
                "traffic to the new model; compare user signals (thumbs, regenerate "
                "rate, retention).",

                "Decision rule. Accept the fine-tuned model only if it wins on the target "
                "task metric without significant regression on base capabilities.",
            ],
        },
        {
            "number": "10.12",
            "title": "Domain-Specific Fine-Tuning",
            "paragraphs": [
                "Adapting an LLM to a specific domain (medical, legal, financial, code) "
                "follows the general pattern but has domain-specific considerations.",

                "Tokenizer extension. Domain-specific terminology (drug names, ticker "
                "symbols, code identifiers) may tokenize poorly with general subword "
                "tokenizers. Extend the tokenizer with domain tokens; briefly continue "
                "pretraining so the new tokens learn meaningful embeddings.",

                "Continued pretraining. Before instruction tuning, do a brief pass of "
                "language modeling on raw domain text. Builds domain vocabulary and "
                "patterns. Skip if your domain is well-represented in the base model's "
                "pretraining data.",

                "Compliance and licensing. Medical (HIPAA), financial (SOX, GLBA), and "
                "European (GDPR) data have legal restrictions. PII redaction, audit logs, "
                "consent management. Document data provenance.",

                "Expert evaluation. Public benchmarks may not reflect your domain. Build "
                "evaluation sets with domain experts. For regulated domains, expert "
                "review of outputs may be required before deployment.",
            ],
        },
        {
            "number": "10.13",
            "title": "Summary",
            "bullets": [
                "Fine-tuning adapts a pretrained model to a specific task by continuing "
                "training on labeled data. SFT is the standard form.",
                "Use fine-tuning for behavior change, format consistency, persona, and "
                "domain specialization. Use RAG for knowledge that changes.",
                "LoRA trains a low-rank update on top of frozen base weights, reducing "
                "trainable parameters to 0.5-2% of full fine-tuning. qLoRA adds 4-bit base "
                "quantization, enabling 70B fine-tuning on a single GPU.",
                "Instruction tuning teaches the base model to follow natural-language "
                "instructions, producing the chat models most users interact with.",
                "Catastrophic forgetting is real. Mitigate with PEFT, data mixing, and "
                "regression evaluation.",
                "Distillation transfers knowledge from large teachers to small students for "
                "faster, cheaper inference at modest quality cost.",
                "Evaluate rigorously: held-out test set, regression suite, qualitative "
                "review, and production A/B test.",
            ],
        },
    ],
    "further_reading": [
        "Hu et al., 'LoRA: Low-Rank Adaptation of Large Language Models' (2021).",
        "Dettmers et al., 'QLoRA: Efficient Finetuning of Quantized LLMs' (2023).",
        "Wei et al., 'Finetuned Language Models Are Zero-Shot Learners' (2021). FLAN.",
        "Chung et al., 'Scaling Instruction-Finetuned Language Models' (2022). FLAN-T5.",
    ],
}
