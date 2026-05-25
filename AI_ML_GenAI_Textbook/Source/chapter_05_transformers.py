"""Chapter 5: The Transformer Architecture."""

CHAPTER = {
    "label": "Chapter 5",
    "title": "The Transformer Architecture",
    "intro_image": "09_transformer.png",
    "intro_caption": "Figure 5.1: The original transformer architecture (Vaswani et al., 2017).",
    "sections": [
        {
            "number": "5.1",
            "title": "Why Transformers Won",
            "paragraphs": [
                "Before 2017, sequence modeling was dominated by RNNs and LSTMs. These models "
                "had two structural problems that capped their performance: they processed "
                "sequences strictly left to right (no parallelism over the time axis), and "
                "they compressed everything seen so far into a fixed-size hidden state "
                "(information about distant tokens leaked away).",

                "The transformer, introduced in 'Attention Is All You Need' by Vaswani et al. "
                "in 2017, replaced recurrence with self-attention. Every token can attend "
                "directly to every other token. Computation parallelizes over the sequence "
                "dimension. Long-range dependencies are one hop away. The result was both "
                "faster training on GPUs and better quality at scale.",

                "Within five years, transformers swept NLP, then computer vision (Vision "
                "Transformers, 2020), then audio (Whisper, 2022), then multimodal (CLIP, "
                "GPT-4V). Every modern frontier model is a transformer or a transformer "
                "derivative. Understanding the transformer is the single most important "
                "investment you can make in modern AI.",
            ],
        },
        {
            "number": "5.2",
            "title": "Self-Attention",
            "image": "10_attention.png",
            "caption": "Figure 5.2: Self-attention computes Q, K, V from the input and combines V weighted by softmax(QK^T/√d).",
            "paragraphs": [
                "Self-attention is the core operation. The intuition: every token computes a "
                "weighted combination of all tokens, where the weights depend on relevance.",
            ],
            "subsections": [
                {
                    "title": "5.2.1 Queries, Keys, and Values",
                    "paragraphs": [
                        "Each input token x_i is projected to three vectors: a query q_i = "
                        "W_Q · x_i, a key k_i = W_K · x_i, and a value v_i = W_V · x_i. The "
                        "projection matrices W_Q, W_K, W_V are learned.",

                        "The query represents what the token is looking for. The key represents "
                        "what the token offers. The value is the actual content. The metaphor: "
                        "querying a database, where keys identify entries and values are the "
                        "content returned.",
                    ],
                },
                {
                    "title": "5.2.2 The Attention Formula",
                    "paragraphs": [
                        "For all tokens, the attention output is:",
                    ],
                    "equation": "Attention(Q, K, V) = softmax(QK^T / √d_k) · V",
                    "equation_label": "5.1",
                    "more_paragraphs": [
                        "Three steps. First, compute pairwise dot products between every "
                        "query and every key. The result is an n×n matrix of raw attention "
                        "scores. Second, scale by √d_k (where d_k is the key dimension) and "
                        "apply softmax row-wise. This turns scores into a probability "
                        "distribution: each row sums to 1. Third, multiply by V to combine "
                        "values weighted by attention.",

                        "Why the √d_k scaling? Without it, dot products grow large in high "
                        "dimensions, pushing softmax into saturation. Gradients vanish. The "
                        "scaling keeps softmax inputs in a usable range.",

                        "Masked self-attention (used in decoder layers and autoregressive "
                        "models): set scores S_ij to -∞ for j > i before softmax. The model "
                        "cannot peek at future tokens. This is what makes GPT-style models "
                        "autoregressive.",
                    ],
                },
                {
                    "title": "5.2.3 Multi-Head Attention",
                    "paragraphs": [
                        "Single-head attention forces all relationships through one set of "
                        "weights. Multi-head attention runs h attention computations in "
                        "parallel with different W_Q, W_K, W_V projections, each of dimension "
                        "d_model / h. The outputs are concatenated and projected back through "
                        "W_O.",

                        "Each head can specialize. One might track syntactic dependencies, "
                        "another semantic coreference, another local n-gram patterns. The same "
                        "compute as single-head with full dimension, but much richer behavior.",

                        "Typical h: 8, 16, or 32. Modern LLMs use grouped-query attention "
                        "(GQA) or multi-query attention (MQA) where the number of Q heads "
                        "exceeds the number of K and V heads, reducing KV-cache memory at "
                        "inference time with minor quality loss.",
                    ],
                },
            ],
        },
        {
            "number": "5.3",
            "title": "Positional Encoding",
            "image": "30_rope.png",
            "caption": "Figure 5.3: RoPE rotates query and key vectors in 2D subspaces by an angle proportional to position.",
            "paragraphs": [
                "Self-attention is permutation-equivariant: shuffle the input tokens, get a "
                "shuffled output. The transformer has no built-in notion of order. Positional "
                "encoding injects position information.",

                "Sinusoidal positional encoding (original transformer): add fixed sin/cos "
                "functions of position to the input embeddings. Different frequencies per "
                "dimension. Generalizes in theory to unseen positions.",

                "Learned positional encoding (BERT, GPT-2): treat each position index as a "
                "learnable embedding. Simple, works well within trained range, does not "
                "extrapolate to longer sequences.",

                "Rotary Position Embedding (RoPE, used in LLaMA, GPT-NeoX, Mistral): rotate "
                "Q and K vectors by an angle proportional to position. The dot product Q·K "
                "depends on the relative position because both rotations cancel out the "
                "absolute position. Extrapolates better than absolute encodings. Augmented "
                "with NTK-aware scaling or YaRN for further length extension.",

                "ALiBi (Attention with Linear Biases): add a position-dependent bias to "
                "attention scores. Very strong extrapolation. Used in MPT, BLOOM.",
            ],
        },
        {
            "number": "5.4",
            "title": "The Full Transformer Layer",
            "paragraphs": [
                "A transformer layer composes attention with a feed-forward network. The "
                "structure: multi-head self-attention, then residual connection plus layer "
                "normalization, then position-wise feed-forward network, then residual "
                "connection plus layer normalization.",

                "The feed-forward network is a two-layer MLP applied independently at each "
                "position. Typically 4x the model dimension as the hidden width. Modern "
                "architectures replace ReLU with GELU or SiLU (Swish) and sometimes add a "
                "gating mechanism (SwiGLU in LLaMA).",

                "Residual connections are essential. Without them, deep transformers do not "
                "train. They allow gradients to flow back through the network unimpeded.",

                "Layer normalization is applied either before each sub-layer (Pre-LN, modern "
                "default, more stable training) or after (Post-LN, original transformer, "
                "harder to train at large depths). LLaMA uses RMSNorm, a simpler variant.",
            ],
        },
        {
            "number": "5.5",
            "title": "Encoder, Decoder, Encoder-Decoder",
            "image": "20_encoder_decoder.png",
            "caption": "Figure 5.4: Encoder-decoder transformer for sequence-to-sequence tasks.",
            "paragraphs": [
                "Three transformer variants depending on the task.",
            ],
            "subsections": [
                {
                    "title": "5.5.1 Encoder-Only (BERT family)",
                    "paragraphs": [
                        "Bidirectional self-attention over the input. Produces rich contextual "
                        "representations of every token. No generation. Best for classification, "
                        "NER, embedding generation, similarity. Trained with Masked Language "
                        "Modeling (MLM): mask 15% of tokens, predict them from bidirectional "
                        "context.",
                        "Examples: BERT, RoBERTa, DeBERTa, ELECTRA. Still dominant for "
                        "embedding generation and classification at scale due to efficiency.",
                    ],
                },
                {
                    "title": "5.5.2 Decoder-Only (GPT family)",
                    "paragraphs": [
                        "Causal (left-to-right) masked self-attention. Generates tokens one at "
                        "a time. Trained with causal language modeling: predict next token "
                        "given previous tokens. Modern instruction-tuned variants (GPT-4, "
                        "Claude, LLaMA, Mistral, Gemma) handle both understanding and "
                        "generation tasks via prompting.",
                        "Examples: GPT-1/2/3/4, LLaMA, Mistral, Claude. The dominant pattern "
                        "for general-purpose LLMs.",
                    ],
                },
                {
                    "title": "5.5.3 Encoder-Decoder",
                    "paragraphs": [
                        "Encoder produces contextual representations of the input. Decoder "
                        "generates the output autoregressively, with cross-attention into the "
                        "encoder output at each layer. The natural choice for translation, "
                        "summarization, and any text-to-text task.",
                        "Examples: original transformer (translation), BART, T5. T5 unified "
                        "every NLP task as text-to-text. Decoder-only models have largely "
                        "displaced encoder-decoders in production for general LLMs, but "
                        "encoder-decoder remains competitive for specific structured tasks.",
                    ],
                },
            ],
        },
        {
            "number": "5.6",
            "title": "Pretraining Objectives",
            "paragraphs": [
                "Modern transformers are pretrained with self-supervised objectives on massive "
                "corpora, then fine-tuned or prompted for downstream tasks. The choice of "
                "objective shapes the model's capabilities.",
            ],
            "subsections": [
                {
                    "title": "5.6.1 Causal Language Modeling (CLM)",
                    "paragraphs": [
                        "Predict the next token given the previous tokens. Used in GPT, "
                        "LLaMA, Mistral, and most decoder-only LLMs. Simple, scales well, "
                        "and naturally enables generation at inference time. Each token "
                        "contributes to the loss.",
                    ],
                },
                {
                    "title": "5.6.2 Masked Language Modeling (MLM)",
                    "paragraphs": [
                        "Mask a fraction of tokens (15% in BERT), predict them from "
                        "bidirectional context. Forces the model to use both left and right "
                        "context. Used in BERT, RoBERTa, DeBERTa.",
                    ],
                },
                {
                    "title": "5.6.3 Span Corruption (T5, BART)",
                    "paragraphs": [
                        "Mask contiguous spans rather than individual tokens. Predict the "
                        "spans in order. Generalizes MLM to longer spans. Natural fit for "
                        "text-to-text framing.",
                    ],
                },
                {
                    "title": "5.6.4 Replaced Token Detection (ELECTRA)",
                    "paragraphs": [
                        "A small generator proposes replacements for masked tokens. The main "
                        "model classifies each token as original or replaced. Every token "
                        "contributes to the loss, making it more sample-efficient than MLM.",
                    ],
                },
                {
                    "title": "5.6.5 Permutation Language Modeling (XLNet)",
                    "paragraphs": [
                        "Predict tokens in a randomly permuted order so each target sees a "
                        "mix of left and right context without using MLM's masking artifact. "
                        "Combines the bidirectional benefit of MLM with the autoregressive "
                        "property of CLM.",
                    ],
                },
            ],
        },
        {
            "number": "5.7",
            "title": "Long Context: Beyond Quadratic Attention",
            "paragraphs": [
                "Standard self-attention has O(n²) time and memory in sequence length n. "
                "This is the binding constraint for long-context applications: documents, "
                "codebases, conversations spanning hours.",

                "Sparse and windowed attention: Longformer combines sliding-window local "
                "attention with a few global tokens. BigBird adds random attention. Each "
                "token attends to O(n) tokens instead of O(n²). Used for long-document tasks.",

                "Linearized attention: Linformer projects keys and values to a smaller rank. "
                "Performer approximates softmax with random feature maps. Reformer uses LSH "
                "to bucket similar queries. Each trades exact attention for asymptotic "
                "improvement; quality varies.",

                "Memory-augmented architectures: Transformer-XL caches hidden states across "
                "segments. Compressive Transformer further compresses old states. RWKV and "
                "state-space models (Mamba) replace attention entirely with recurrent or "
                "linear updates.",

                "Production answer: retrieval-augmented generation. Instead of extending the "
                "context window, retrieve only relevant chunks per query. We cover this in "
                "Chapter 12. For many use cases, this is more cost-effective than long-"
                "context training.",
            ],
        },
        {
            "number": "5.8",
            "title": "Summary",
            "bullets": [
                "The transformer replaces recurrence with self-attention, enabling "
                "parallelism over the sequence dimension and direct modeling of long-range "
                "dependencies.",
                "Self-attention computes Q, K, V projections, then weights values by "
                "softmax(QK^T/√d_k). Multi-head attention adds specialization.",
                "Positional encoding (sinusoidal, learned, RoPE, ALiBi) injects order "
                "information that self-attention lacks.",
                "Encoder-only models (BERT) understand; decoder-only models (GPT) generate; "
                "encoder-decoder models (T5) translate. Decoder-only dominates general LLMs.",
                "Pretraining objectives (CLM, MLM, span corruption, ELECTRA, PLM) define how "
                "the model learns from raw text.",
                "Quadratic attention is the long-context bottleneck. Sparse attention, "
                "linearized attention, state-space models, and RAG all address it differently.",
            ],
        },
    ],
    "further_reading": [
        "Vaswani et al., 'Attention Is All You Need' (2017). The foundational paper. Read it.",
        "Devlin et al., 'BERT: Pre-training of Deep Bidirectional Transformers' (2018).",
        "Radford et al., 'Language Models are Few-Shot Learners' (2020). GPT-3.",
        "Su et al., 'RoFormer: Enhanced Transformer with Rotary Position Embedding' (2021).",
    ],
}
