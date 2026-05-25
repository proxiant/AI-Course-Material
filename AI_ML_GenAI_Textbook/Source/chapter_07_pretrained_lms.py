"""Chapter 7: Pretrained Language Models."""

CHAPTER = {
    "label": "Chapter 7",
    "title": "Pretrained Language Models",
    "sections": [
        {
            "number": "7.1",
            "title": "The Pretraining Revolution",
            "paragraphs": [
                "Before 2018, NLP systems were largely task-specific. You trained a model "
                "from scratch (or from word embeddings) on labeled data for your task. Each "
                "new task started over. After 2018, the field shifted decisively to "
                "pretraining and fine-tuning. A single model pretrained on massive text "
                "corpora produced representations that transferred to dozens of downstream "
                "tasks with minimal additional training.",

                "The shift was driven by three forces: scaling laws (more data and "
                "parameters reliably improve performance), self-supervised objectives "
                "(language models learn from raw text without human labels), and architectural "
                "advances (transformers parallelize and scale better than RNNs). By 2020, "
                "every state-of-the-art NLP system was a transformer pretrained on billions "
                "of tokens.",

                "This chapter walks through the major model families. The technical lessons "
                "apply broadly even as specific models age out: encoder versus decoder "
                "architectures, pretraining objectives, scaling behavior, the relationship "
                "between pretraining and fine-tuning, and the design choices that make some "
                "models more useful than others.",
            ],
        },
        {
            "number": "7.2",
            "title": "BERT and the Encoder-Only Family",
            "paragraphs": [
                "BERT (Bidirectional Encoder Representations from Transformers, Devlin et "
                "al., 2018) was the model that mainstreamed pretraining. Two design choices "
                "made it work.",

                "Bidirectional attention. Earlier language models read left-to-right (or "
                "concatenated separate left-to-right and right-to-left models, as in ELMo). "
                "BERT used full bidirectional self-attention. Every token attends to every "
                "other token in both directions. The representations are richer.",

                "Masked language modeling. To train a bidirectional model on next-token "
                "prediction would let it cheat (the answer is in the context it can see). "
                "BERT masks 15% of input tokens and predicts them from bidirectional context. "
                "The training signal is dense across tokens, and bidirectionality is "
                "preserved.",

                "BERT-base has 12 layers, 12 attention heads, 768 hidden dimensions, 110M "
                "parameters. BERT-large doubles depth and hidden size to 340M parameters. "
                "Trained on Wikipedia plus BooksCorpus (3.3B words total). The results were "
                "state-of-the-art across 11 NLP benchmarks at release.",
            ],
            "subsections": [
                {
                    "title": "7.2.1 Downstream Use",
                    "paragraphs": [
                        "BERT's standard usage pattern: prepend a [CLS] token, append a [SEP] "
                        "token, run through the encoder, attach a task-specific head. For "
                        "classification, a linear layer on the [CLS] embedding. For token "
                        "labeling (NER), a linear layer on each token embedding. For span "
                        "tasks (extractive QA), predict start and end token positions.",
                        "The same backbone serves many tasks; only the head and a small "
                        "amount of task-specific data are required. Fine-tuning typically "
                        "requires a few epochs at a small learning rate (1e-5 to 5e-5). The "
                        "pretrained encoder retains most of its representation; the head "
                        "learns the task-specific projection.",
                    ],
                },
                {
                    "title": "7.2.2 BERT Successors",
                    "paragraphs": [
                        "RoBERTa (Liu et al., 2019) revisited BERT's training: larger batches, "
                        "more data (160GB vs 16GB), longer training, removed Next Sentence "
                        "Prediction (which turned out to add little). The result was a "
                        "substantially stronger model with the same architecture.",
                        "DeBERTa (He et al., 2020, 2021) added disentangled attention and "
                        "enhanced mask decoding. Pushed state-of-the-art further on SuperGLUE.",
                        "ELECTRA (Clark et al., 2020) changed the pretraining objective. A "
                        "small generator proposes replacements for masked tokens; the main "
                        "model classifies each token as original or replaced. Every token "
                        "contributes to the loss, making training more sample-efficient than "
                        "MLM.",
                        "ALBERT (Lan et al., 2020) factorized embeddings and shared parameters "
                        "across layers to reduce model size at small quality cost.",
                        "Modern encoder models for embeddings (BGE, E5, GTE, mpnet) are "
                        "based on these designs with contrastive fine-tuning for retrieval.",
                    ],
                },
            ],
        },
        {
            "number": "7.3",
            "title": "GPT and the Decoder-Only Family",
            "paragraphs": [
                "GPT (Generative Pretrained Transformer) took a different bet. Use a "
                "decoder-only transformer with causal (left-to-right) attention. Pretrain on "
                "next-token prediction. Scale up. The architecture is simpler than BERT; the "
                "objective matches the inference-time task (generation); the model "
                "naturally produces text.",

                "GPT-1 (Radford et al., 2018) introduced the architecture but had limited "
                "impact at 117M parameters. GPT-2 (2019) scaled to 1.5B parameters and "
                "demonstrated startling zero-shot capabilities on diverse tasks via "
                "prompting alone. GPT-3 (Brown et al., 2020) scaled to 175B parameters and "
                "introduced in-context learning at scale: the ability to learn new tasks "
                "from a few examples in the prompt, with no weight updates.",

                "After GPT-3, the field bifurcated. OpenAI kept its models closed but "
                "released access through APIs. Meta released LLaMA (2023), then LLaMA-2 and "
                "LLaMA-3, as open-weights models. Mistral, Gemma, Qwen, Yi, DeepSeek "
                "followed. Open-weights LLMs are now competitive with closed-source models "
                "on many benchmarks.",
            ],
            "subsections": [
                {
                    "title": "7.3.1 Modern Decoder Architecture",
                    "paragraphs": [
                        "Modern decoder-only LLMs (LLaMA-style) include refinements over the "
                        "original GPT architecture.",
                        "Pre-normalization. Apply RMSNorm before each sub-layer (attention and "
                        "FFN) instead of after. Stabilizes training at scale.",
                        "Rotary Position Embedding (RoPE). Rotate Q and K vectors by an angle "
                        "proportional to position. Better length extrapolation than absolute "
                        "positional encoding.",
                        "SwiGLU activation. A gated variant of Swish in the FFN. Slightly "
                        "better quality than GELU at similar compute.",
                        "Grouped-Query Attention (GQA). Fewer KV heads than Q heads. Reduces "
                        "KV-cache size and speeds up inference. Used in LLaMA-2 70B and "
                        "LLaMA-3.",
                        "Tied embeddings (sometimes). Share input and output token embeddings "
                        "to save parameters.",
                    ],
                },
                {
                    "title": "7.3.2 Scaling Laws",
                    "image": "38_chinchilla.png",
                    "caption": "Figure 7.1: Chinchilla-optimal scaling: 20 tokens per parameter.",
                    "paragraphs": [
                        "Kaplan et al. (2020) showed that LLM loss scales smoothly with "
                        "parameters and training tokens. The original scaling laws suggested "
                        "ever-larger models. Then Hoffmann et al. (2022, 'Chinchilla') "
                        "showed that GPT-3 and similar models were significantly "
                        "under-trained. For a fixed compute budget, optimal model size and "
                        "training tokens should scale together at roughly 20 tokens per "
                        "parameter.",
                        "A 7B model wants 140B tokens. A 70B model wants 1.4T tokens. Modern "
                        "training has pushed well past these ratios; LLaMA-3 uses ~15T "
                        "tokens for an 8B model and 70B model. The diminishing returns regime "
                        "is real but the absolute gains continue to matter.",
                        "Implication for practitioners: smaller, well-trained models often "
                        "beat larger, under-trained ones. A 7B model trained on 2T tokens "
                        "can outperform a 13B model trained on 100B tokens.",
                    ],
                },
                {
                    "title": "7.3.3 In-Context Learning",
                    "paragraphs": [
                        "GPT-3's headline capability was in-context learning. Provide a few "
                        "input-output examples in the prompt, then ask for a new prediction. "
                        "The model continues the pattern with no parameter updates.",
                        "How does this work? The model was trained on internet text, which "
                        "contains many instances of demonstration patterns: lists, tables, "
                        "translation pairs, code with similar functions. Predicting the next "
                        "token in such sequences requires generalizing the pattern. This "
                        "generalization is the meta-task that enables in-context learning at "
                        "inference time.",
                        "Empirical findings. Quality scales with model size; larger models "
                        "exhibit qualitatively more in-context learning capability. Sensitive "
                        "to example ordering, format, and selection. More examples help up to "
                        "a point, often 5-10 examples. The examples need not be perfectly "
                        "labeled; the pattern matters more than the labels.",
                    ],
                },
            ],
        },
        {
            "number": "7.4",
            "title": "Encoder-Decoder Models: T5 and BART",
            "paragraphs": [
                "Encoder-decoder transformers are well-suited to sequence-to-sequence tasks: "
                "translation, summarization, structured extraction. They combine the rich "
                "input understanding of encoder-only models with the generation capability of "
                "decoder-only models.",

                "T5 (Text-to-Text Transfer Transformer, Raffel et al., 2020) unified every "
                "NLP task as text-to-text. Translation: input 'translate English to French: "
                "The cat is on the mat.' Output: 'Le chat est sur le tapis.' Summarization: "
                "input 'summarize: <article>'. Output: '<summary>'. Even classification was "
                "framed as text generation. T5 was trained with span corruption: mask "
                "contiguous spans of the input, predict them as the output.",

                "BART (Bidirectional and Auto-Regressive Transformers, Lewis et al., 2020) "
                "trained with multiple denoising objectives: token masking, token deletion, "
                "span infilling, sentence permutation, document rotation. The model learned "
                "to reconstruct original text from corrupted versions. Strong on "
                "summarization, translation, and question generation.",

                "FLAN-T5 (Chung et al., 2022) fine-tuned T5 on a massive collection of "
                "instruction-following tasks. The result was a smaller, faster instruction-"
                "following model competitive with much larger decoder-only models on many "
                "tasks.",

                "Today, decoder-only models dominate general-purpose LLMs due to their "
                "scaling efficiency and prompt-based versatility. Encoder-decoder models "
                "remain competitive for specific tasks where the input is bounded and the "
                "output is short (summarization, translation, structured extraction).",
            ],
        },
        {
            "number": "7.5",
            "title": "Comparing the Three Families",
            "paragraphs": [
                "When to choose each.",

                "Encoder-only (BERT family): when you need a single representation of input "
                "for classification, similarity, NER, or embedding generation. Cheaper than "
                "a generative model. Sentence embedders (Sentence-BERT, BGE, E5) are "
                "encoder-only.",

                "Decoder-only (GPT family): when you need generation, instruction following, "
                "or general-purpose intelligence accessible via prompting. The dominant "
                "pattern for modern LLMs. Use this unless you have a specific reason not to.",

                "Encoder-decoder (T5, BART): when the input and output are clearly separated, "
                "and the task benefits from explicit cross-attention between input and "
                "output. Translation and summarization are the classic fits. Less popular "
                "than decoder-only at frontier scale due to training and serving complexity.",

                "Hybrid patterns are increasingly common. A decoder-only LLM with an "
                "external retriever (RAG) combines the generative power of decoders with the "
                "explicit input-conditioning of encoder-decoders. Tool-using agents extend "
                "the decoder's reach to external systems. These patterns may matter more "
                "than the underlying architecture choice for your application.",
            ],
        },
        {
            "number": "7.6",
            "title": "The Foundation Model Ecosystem",
            "paragraphs": [
                "By 2025, the landscape of pretrained models has consolidated into a few "
                "major families with frequent releases.",

                "Closed frontier models: GPT-4, GPT-4o, GPT-5 (OpenAI); Claude 3.5 Sonnet, "
                "Claude 3.5 Opus (Anthropic); Gemini 1.5/2.0 Pro and Ultra (Google). "
                "Access via API. Generally the strongest models on most benchmarks. Highest "
                "cost per token. Hosted; no on-prem option for the largest models.",

                "Open-weights frontier: LLaMA-3 (Meta), Mistral Large, Mixtral 8x22B "
                "(Mistral), Gemma 2 (Google open-weights), Qwen2.5 (Alibaba), DeepSeek-V3. "
                "Weights downloadable; can be self-hosted, fine-tuned, served behind your own "
                "infrastructure. Quality competitive with closed models on many tasks; "
                "occasionally surpassing on specific benchmarks.",

                "Smaller open models: LLaMA-3 8B, Mistral 7B, Phi-3, Gemma 2B, Qwen2.5 7B. "
                "Suitable for on-device, edge, or cost-constrained deployment. Quality has "
                "improved dramatically; a well-tuned 7B model in 2025 outperforms GPT-3.5 "
                "from 2022.",

                "Specialized models: Code (DeepSeek Coder, StarCoder2, Code Llama), math "
                "(DeepSeek-Math, Llemma), medical (Med-PaLM, ClinicalBERT), reasoning "
                "(OpenAI o1, DeepSeek-R1, Claude with extended thinking).",

                "Selection criteria. Quality: measure on your task. Cost: total cost of "
                "ownership including training, inference, and engineering. Privacy: closed "
                "APIs may not be acceptable for sensitive data. Latency: smaller open "
                "models served close to users may beat distant API calls. Vendor risk: avoid "
                "irreplaceable dependencies where possible.",
            ],
        },
        {
            "number": "7.7",
            "title": "Reasoning Models",
            "paragraphs": [
                "A distinct class of models has emerged that performs extensive chain-of-"
                "thought reasoning at inference time. OpenAI's o1 (2024), o3, DeepSeek-R1 "
                "(2025), and Claude with extended thinking represent this category. They "
                "trade longer inference time for higher quality on math, code, and complex "
                "reasoning tasks.",

                "How they differ from standard LLMs. Trained with reinforcement learning on "
                "reasoning tasks, typically with RLVR (Reinforcement Learning with "
                "Verifiable Rewards). The model learns to spend inference compute on "
                "thinking rather than just emitting the final answer. The thinking can be "
                "hundreds or thousands of tokens long and is sometimes hidden from the user.",

                "Performance impact. Dramatic improvements on AIME (American Invitational "
                "Mathematics Examination), Codeforces, USACO, GPQA Diamond. Smaller "
                "improvements on general chat and knowledge tasks where reasoning is not "
                "the bottleneck.",

                "Cost-quality tradeoff. Reasoning models are 5-50x more expensive than "
                "non-reasoning models at the same quality on tasks where reasoning matters. "
                "On tasks where it doesn't, they offer no advantage and may be slower. Route "
                "queries dynamically: cheap fast model for simple queries, reasoning model "
                "for hard ones.",

                "Implications. Inference-time compute scaling is a new lever. A standard "
                "model given 10x thinking budget can match a much larger model without "
                "thinking. This shifts cost from training (one-time) to inference (per "
                "query), changing the economics of AI deployment.",
            ],
        },
        {
            "number": "7.8",
            "title": "Mixture of Experts",
            "image": "34_moe.png",
            "caption": "Figure 7.2: Mixture of Experts: a router activates only a few experts per token.",
            "paragraphs": [
                "Most LLMs are dense: every parameter activates for every token. Mixture of "
                "Experts (MoE) sparsifies this. The feed-forward layer is replaced with "
                "multiple expert subnetworks plus a router. Per token, only a few experts "
                "(typically 1 or 2 out of 8 to 128) are activated.",

                "The result: total parameter count is large (Mixtral 8x7B has 47B total "
                "parameters), but active parameters per token are much smaller (about 13B "
                "for Mixtral). FLOPs per token scale with active parameters; memory scales "
                "with total parameters. A MoE achieves similar quality to a much larger "
                "dense model at a fraction of the inference compute.",

                "Challenges. Load balancing: experts can specialize so heavily that some are "
                "rarely used. Auxiliary losses encourage balanced routing. Training "
                "stability: routing is non-smooth, leading to instabilities. Memory: all "
                "expert weights must be loaded even though most are unused. Communication: "
                "for multi-device serving, routing decisions require cross-device "
                "communication.",

                "Examples. Switch Transformer (Google), GShard, GLaM, Mixtral 8x7B and "
                "Mixtral 8x22B (Mistral), DeepSeek-V3 (~671B total, 37B active). DeepSeek-V3 "
                "uses 256 experts with shared experts, demonstrating MoE at frontier scale.",
            ],
        },
        {
            "number": "7.9",
            "title": "Summary",
            "bullets": [
                "Pretraining on massive corpora plus fine-tuning is the dominant paradigm "
                "for modern NLP.",
                "Encoder-only models (BERT) excel at understanding tasks; decoder-only "
                "models (GPT, LLaMA) dominate generation; encoder-decoder models (T5) suit "
                "explicit sequence-to-sequence tasks.",
                "Scaling laws (Chinchilla) connect parameters, tokens, and quality. Smaller "
                "well-trained models beat larger under-trained ones.",
                "In-context learning lets pretrained LLMs adapt to new tasks via examples in "
                "the prompt, with no parameter updates.",
                "Reasoning models trade inference compute for quality on math, code, and "
                "complex reasoning.",
                "Mixture of Experts scales total parameters while keeping inference cost "
                "low, enabling frontier quality at lower cost per token.",
            ],
        },
    ],
    "further_reading": [
        "Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers' (2018).",
        "Brown et al., 'Language Models are Few-Shot Learners' (2020). GPT-3.",
        "Hoffmann et al., 'Training Compute-Optimal Large Language Models' (2022). Chinchilla.",
        "Touvron et al., 'LLaMA: Open and Efficient Foundation Language Models' (2023).",
        "Shao et al., 'DeepSeekMath' (2024). RLVR and GRPO for reasoning.",
    ],
}
