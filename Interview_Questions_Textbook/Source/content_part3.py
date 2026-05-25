"""Part 3: LLM fundamentals, Embeddings."""

LLM_FUNDAMENTALS = [
    ("Describe your experience working with text generation using generative models.",
     [
        "A strong interview answer here is concrete and grounded in real artifacts. Cover "
        "three dimensions: (a) which models you have used (GPT-4, Claude, LLaMA, Mistral, "
        "Gemini); (b) how you used them (API calls with few-shot prompting; fine-tuning "
        "with LoRA; RLHF on a custom domain; building a RAG over enterprise documents); "
        "(c) what you learned (prompt patterns that worked, latency and cost tradeoffs, "
        "places where the model failed and how you mitigated).",
        "Avoid generic descriptions. Say 'I built a customer-support assistant on top of "
        "Claude 3.5 Sonnet with a RAG over 80K Confluence pages, hit P95 of 2.1s, and cut "
        "support ticket handle time by 18%'. Specifics signal experience.",
     ]),

    ("What are the fundamental differences between discriminative and generative models?",
     [
        "Discriminative models learn P(y | x): the conditional probability of a label given "
        "the input. They draw decision boundaries between classes. Examples: logistic "
        "regression, SVMs, random forests, classification transformers like BERT.",
        "Generative models learn P(x, y) or P(x): the joint or marginal distribution of "
        "the data. They model how the data was produced and can sample new examples. "
        "Examples: Naive Bayes, HMMs, VAEs, GANs, diffusion models, autoregressive language "
        "models like GPT.",
        "Practical differences: discriminative models often achieve higher accuracy with "
        "less data because they only model what is needed for the task. Generative models "
        "support more tasks (sampling, density estimation, anomaly detection, in-context "
        "learning) and often capture richer structure. Modern LLMs are generative but solve "
        "discriminative tasks via prompting, blurring the historical distinction.",
     ]),

    ("What types of generative models have you worked with, and in what contexts?",
     [
        "Examples of strong context-rich answers (use your own actual work):",
        "Autoregressive LLMs (GPT-4, Claude, LLaMA): customer-facing chatbots, code "
        "completion assistants, document summarization, structured extraction.",
        "Diffusion models (Stable Diffusion, FLUX): marketing image generation, product "
        "photography augmentation, controllable image editing.",
        "VAEs: anomaly detection, latent-space exploration for tabular data.",
        "GANs: synthetic data generation for training, super-resolution.",
        "Specialized: Whisper for transcription, Codex/StarCoder for code, MusicLM for "
        "audio.",
        "Frame each example with the business outcome, not just the model name. Interviewers "
        "want to know you can connect model capabilities to product value.",
     ]),

    ("What is multimodal AI, and why is it important?",
     [
        "Multimodal AI processes more than one modality (text, image, audio, video, "
        "structured data) within a single system. The model may take multiple modalities as "
        "input, produce multiple modalities as output, or both.",
        "Why it matters: real-world problems are rarely single-modality. A medical diagnosis "
        "uses images, lab results, and clinical notes together. A search query may include "
        "a photo and a question. A self-driving car fuses camera, radar, and lidar. "
        "Multimodal models match how humans actually solve these problems.",
        "Modern examples: GPT-4V and Gemini accept images and text. Whisper translates "
        "speech across languages. CLIP enables image search by text. Sora generates video "
        "from text prompts. Multimodal is now the default for foundation models.",
     ]),

    ("Explain cross-modal learning with examples.",
     [
        "Cross-modal learning trains a model to use information from one modality to improve "
        "another. The classic example: training on (image, caption) pairs lets the model "
        "use language to disambiguate visual content and use visual content to ground "
        "language.",
        "CLIP: image and text encoders trained with contrastive loss on 400M pairs. Enables "
        "zero-shot image classification (no labeled image data needed) by encoding class "
        "names as text and choosing the closest match. Powers Stable Diffusion's text "
        "conditioning.",
        "Image captioning: trained on (image, caption) pairs. Generates captions for new "
        "images, using language structure learned from captions and visual "
        "understanding from the encoder.",
        "Visual question answering (VQA): given (image, question), produce an answer. "
        "Requires combining visual perception and language reasoning.",
        "Audio-visual speech recognition: combining lip movement and audio improves "
        "transcription accuracy in noisy environments.",
     ]),

    ("What are common challenges in developing multimodal models, and how do you address them?",
     [
        "Data alignment: paired data across modalities is expensive. Mitigation: leverage "
        "abundant unimodal data with separate pretraining, then align with a smaller paired "
        "set. Use noisy web pairs at scale (LAION).",
        "Modality imbalance: one modality may dominate, drowning out the other. Mitigation: "
        "modality-specific learning rates; gradient balancing; modality dropout (randomly "
        "withhold one modality during training).",
        "Architecture complexity: shared vs. separate encoders, cross-attention vs. shared "
        "embedding space, frozen vs. trainable. Mitigation: standardize on a published "
        "pattern (Q-Former bridge, direct projection) before customizing.",
        "Evaluation: each modality has its own metrics. Mitigation: build per-modality "
        "evaluations plus a unified end-task metric. Add human evaluation for open-ended "
        "outputs.",
        "Compute: multimodal training is expensive. Mitigation: freeze pretrained encoders, "
        "train only the bridge or projection module.",
     ]),

    ("How do CLIP and DALL-E innovate in multimodal learning?",
     [
        "CLIP innovation: showed that a simple contrastive objective on web-scale image-"
        "text pairs produces a model with strong zero-shot transfer. No labels needed for "
        "classification at inference time. The CLIP embedding space became a foundational "
        "asset reused in countless downstream systems (Stable Diffusion conditioning, image "
        "search, content moderation, dataset filtering).",
        "DALL-E innovation: text-to-image generation at quality and prompt-following "
        "fidelity unseen before. DALL-E 1 used a discrete VAE plus autoregressive "
        "transformer; DALL-E 2 and 3 use diffusion with CLIP-based text conditioning. The "
        "result: creative tools that ordinary users can drive with natural language.",
        "Bigger picture: both demonstrated that scale plus a good cross-modal objective "
        "produces emergent capabilities. They opened the door to today's multimodal "
        "foundation models.",
     ]),

    ("Why does data preprocessing and representation matter in multimodal learning?",
     [
        "Different modalities need different preprocessing: text needs tokenization, "
        "normalization, length capping; images need resizing, normalization, augmentation; "
        "audio needs sampling rate conversion and mel-spectrogram computation; video needs "
        "frame sampling and temporal aggregation.",
        "Representation: each modality is mapped to a vector space. Text via a transformer "
        "encoder. Images via a CNN or ViT. Audio via a spectrogram encoder. These vectors "
        "then need to live in a comparable space for the multimodal fusion to make sense.",
        "Alignment: representations are aligned either via a contrastive objective (CLIP "
        "style) or via cross-attention (BLIP, Flamingo style). The choice depends on "
        "downstream use: contrastive for retrieval, cross-attention for generation.",
        "Quality control: garbage in, garbage out applies double in multimodal. Filter for "
        "alignment quality, deduplicate near-duplicates, handle missing modalities "
        "gracefully.",
     ]),

    ("How does multimodal sentiment analysis improve on text-only models?",
     [
        "Text alone misses sarcasm, tone, and visual context. A tweet 'great' with a crying "
        "emoji means the opposite. A product review's accompanying video might show a "
        "broken item while the text is polite.",
        "Multimodal sentiment analysis combines text with audio (tone of voice, prosody), "
        "video (facial expressions), or images (visual content). Aggregating across "
        "modalities reduces ambiguity.",
        "Real cases: customer service analytics on call recordings (text transcript + audio "
        "tone); social media monitoring (text + image/video); video review analysis (text "
        "+ visual + audio).",
        "Accuracy gains are commonly 5-15% over text-only models on benchmarks like "
        "CMU-MOSEI and IEMOCAP. The gains are larger when text alone is ambiguous, which "
        "is precisely the high-value case.",
     ]),

    ("What metrics evaluate multimodal models, and how do they differ from unimodal metrics?",
     [
        "Modality-specific metrics: BLEU/ROUGE for text generation, FID for image "
        "generation, WER for speech, Recall@k for retrieval. Each measures one output type.",
        "Cross-modal metrics: CLIP score (text-image alignment), CIDEr (image captioning), "
        "Image-Text Matching accuracy. These measure how well the modalities work together.",
        "End-task metrics: VQA accuracy, retrieval Recall@k, downstream task performance. "
        "These are what users actually care about.",
        "Human evaluation: especially for generative multimodal outputs. Crowd ratings on "
        "fluency, relevance, factuality, aesthetics.",
        "Bias and fairness: multimodal models can have biases across both modalities. "
        "Evaluate on demographic balanced sets, check for stereotypes in generation.",
        "Difference from unimodal: you need both per-modality and joint metrics. A model "
        "may have perfect image classification and perfect language modeling but fail at "
        "the joint task. Joint metrics catch this.",
     ]),

    ("How do you handle imbalanced data across modalities?",
     [
        "Data-side: collect more data for underrepresented modalities. Oversample the "
        "minority modality. Use modality-specific augmentation (back-translation for text, "
        "augmentation for images).",
        "Training-side: modality-specific learning rates. Loss balancing (e.g. multi-task "
        "uncertainty weighting). Modality dropout: randomly mask one modality so the model "
        "learns to use either.",
        "Architecture-side: separate processing branches per modality with appropriately "
        "scaled representations. Avoid bottlenecks that force one modality through a narrow "
        "channel.",
        "Synthetic data: use a strong generator from the majority modality to produce "
        "training data for the minority. For example, use a TTS system to generate audio "
        "from text transcripts when audio is scarce.",
     ]),

    ("Where is multimodal AI making a significant impact?",
     [
        "Healthcare: combining medical images (X-ray, MRI) with clinical notes for "
        "diagnosis; radiology report generation; pathology image analysis with patient "
        "history.",
        "Autonomous systems: self-driving cars fuse camera, lidar, radar, and HD maps; "
        "drones combine visual and inertial data.",
        "Content moderation: combining text, image, and video to flag policy violations.",
        "E-commerce: visual search, image-based recommendation, AR product try-on.",
        "Education: multimodal tutoring systems that parse handwritten work, voice "
        "questions, and visual diagrams.",
        "Accessibility: image captioning for visually impaired users, real-time speech "
        "transcription, sign language recognition.",
        "Creative tools: text-to-image (DALL-E, Stable Diffusion), text-to-video (Sora, "
        "Runway), text-to-music (Suno).",
     ]),

    ("What future trends do you foresee in multimodal AI?",
     [
        "More modalities natively integrated: text + image + audio + video + 3D + structured "
        "data in one model. Gemini and GPT-4o are early steps.",
        "Longer context across modalities: hours of video, full documents with images, "
        "multi-day conversational history.",
        "Better grounding: models that point to specific image regions or video timestamps "
        "for their claims, reducing hallucination.",
        "Agentic multimodal systems: models that take actions across modalities (read a "
        "screenshot, click a button, summarize a video, generate a chart).",
        "Smaller efficient multimodal models: on-device multimodal assistants, real-time "
        "AR/VR multimodal interfaces.",
        "Ethical concerns: deepfakes (text + image + voice), bias amplification across "
        "modalities, copyright (training data sources), consent (when models can perceive "
        "and act in real environments).",
     ]),
]


EMBEDDINGS = [
    ("What is the fundamental concept of embeddings in ML?",
     [
        "An embedding is a dense vector representation of a discrete or complex object "
        "(word, sentence, image, user, product) such that geometric relationships in the "
        "vector space approximate semantic relationships in the original domain.",
        "Compared to raw input or one-hot encodings, embeddings are much lower-dimensional "
        "(typically 64 to 1024 dimensions vs vocabulary size), dense (not mostly zero), and "
        "carry meaning (similar objects have nearby vectors).",
        "Why this matters: embeddings let downstream models share information across "
        "related items. Similar inputs produce similar embeddings, so a classifier trained "
        "on a few examples generalizes to unseen ones. Retrieval, clustering, "
        "recommendation, and search all reduce to operations in embedding space.",
     ],
     ["15_embeddings.png"]),

    ("Compare word embeddings and sentence embeddings.",
     [
        "Word embeddings represent individual words (or subwords). Static word embeddings "
        "(Word2Vec, GloVe, FastText) give each word one vector regardless of context. "
        "Contextual word embeddings (from BERT, GPT) give different vectors for the same "
        "word in different contexts.",
        "Sentence embeddings represent an entire sentence as a single vector. The naive "
        "approach (average word embeddings) works poorly because it loses word order and "
        "compositionality. Modern sentence embedders (Sentence-BERT, MPNet, BGE, E5) "
        "fine-tune a pretrained transformer with a contrastive objective on pairs of "
        "semantically related sentences.",
        "When to use each: word embeddings for token-level analysis, classical NLP "
        "features. Sentence embeddings for retrieval, similarity, clustering at the "
        "document or query level, RAG.",
     ]),

    ("Explain contextual embeddings.",
     [
        "Contextual embeddings produce a different vector for the same word depending on "
        "its surrounding context. 'Bank' in 'river bank' and 'bank account' gets two "
        "different embeddings.",
        "How BERT generates them: the input text is tokenized, embedded, and run through "
        "the transformer stack. The output at each token position is its contextual "
        "embedding (the final hidden state). Each token's embedding has been influenced by "
        "every other token via self-attention.",
        "Advantages over static embeddings: handles polysemy correctly; captures syntactic "
        "role; produces representations that transfer to many downstream tasks. The cost is "
        "compute (running the encoder per query) and storage (you cannot precompute one "
        "vector per vocabulary word).",
     ]),

    ("Discuss challenges and strategies for cross-modal embeddings.",
     [
        "Challenge 1: alignment. Embeddings from different modalities must live in the same "
        "or comparable space. Strategy: train with a contrastive objective on aligned "
        "pairs (CLIP), or train one modality to project into the other's space (Q-Former).",
        "Challenge 2: scale and quality of paired data. Strategy: web-scale noisy pairs "
        "(LAION) plus high-quality curated pairs for fine-tuning.",
        "Challenge 3: modality-specific dimensionality and structure. Strategy: encode each "
        "modality with a specialized architecture, then project to a shared dimension via "
        "a linear or MLP head.",
        "Challenge 4: evaluation. Cross-modal retrieval (Recall@k) is the standard. "
        "Zero-shot classification (encode candidate labels as text, embed image, match) is "
        "a strong downstream test.",
     ]),

    ("How do you capture embeddings for rare words?",
     [
        "Subword tokenization: BPE, WordPiece, SentencePiece break rare words into known "
        "subword pieces. 'cryptocurrency' becomes ['crypto', 'currency'], each with a "
        "well-trained embedding. The rare word's representation is composed from its parts.",
        "Character-level fallback: encode characters as fallback for any token unseen at "
        "the subword level. FastText averages character n-gram embeddings.",
        "Subsampling and rare-word boosting: oversample rare words during training so each "
        "gets enough gradient signal. Word2Vec and similar use sub-sampling to balance.",
        "Domain-specific tokenizer extension: when working in a specialized domain (medical, "
        "legal), extend the tokenizer vocabulary with domain terms and briefly continue "
        "pretraining so the new tokens learn meaningful embeddings.",
     ]),

    ("Discuss regularization techniques for embedding training.",
     [
        "L2 regularization on embedding norms: penalize large embeddings to prevent a few "
        "from dominating. Common in word2vec.",
        "Dropout on embeddings: zero out random dimensions or random tokens during training "
        "to prevent overfitting to specific dimensions.",
        "Weight tying: share embedding and output projection weights in language models. "
        "Reduces parameters and improves generalization.",
        "Contrastive loss with hard negative mining: harder negatives provide a stronger "
        "regularization signal than random negatives.",
        "Label smoothing: distribute a small probability mass across non-target classes; "
        "useful in classification heads on top of embeddings.",
        "Early stopping based on a held-out evaluation metric (STS-B for sentence "
        "embeddings, MTEB for retrieval).",
     ]),

    ("How are pretrained embeddings leveraged for transfer learning?",
     [
        "Load pretrained embeddings as initialization for a downstream model. The embedding "
        "layer is initialized from Word2Vec, GloVe, or a pretrained transformer's input "
        "embeddings. The rest of the model trains from scratch or is also pretrained.",
        "Freeze vs fine-tune: freezing keeps the pretrained signal intact and reduces "
        "overfitting on small datasets. Fine-tuning adapts to the target domain but can "
        "destroy the pretrained knowledge if the learning rate is too high.",
        "Two-stage training: train the new layers first with the embeddings frozen, then "
        "unfreeze and continue training with a small learning rate.",
        "Embedding-only retrieval: use a frozen pretrained sentence embedder for retrieval "
        "in a RAG system. No task-specific training needed; the pretrained model is "
        "already strong on general similarity.",
        "Benefit: dramatic data efficiency. A target task that would need millions of "
        "labels from scratch may need only thousands with pretrained embeddings.",
     ]),

    ("What is quantization in embeddings, and what does it provide?",
     [
        "Quantization compresses high-precision (float32) embeddings into lower-precision "
        "representations: int8, int4, binary, or product-quantized codes. The result: "
        "4-32x reduction in memory footprint with controlled accuracy loss.",
        "Scalar quantization (int8, int4): each dimension is quantized to a fixed-precision "
        "integer with a per-vector or per-dimension scale and offset.",
        "Product quantization (PQ): split each vector into sub-vectors; quantize each "
        "sub-vector to a codebook of typical sub-vectors. Used by FAISS for billion-scale "
        "vector search.",
        "Binary embeddings: each dimension reduced to one bit. Hamming distance replaces "
        "cosine. 32x compression. Quality loss is real but acceptable for first-stage "
        "retrieval.",
        "Tradeoff: lower precision means faster inference and smaller storage but degraded "
        "recall. Production systems often use int8 for retrieval with re-ranking on int32 "
        "for the final stage.",
     ]),

    ("How do you implement embeddings for high-cardinality categorical features in tabular data?",
     [
        "Use a learned embedding layer per categorical feature. Each unique value maps to a "
        "low-dimensional vector (typically 4 to 64 dimensions). The embedding table has size "
        "(vocab_size, embedding_dim) and is trained jointly with the rest of the model.",
        "Sizing: a common heuristic is min(50, ceil(vocab_size**0.25 * 4)). High-cardinality "
        "features (millions of users) may need larger dimensions but watch memory.",
        "Handling rare categories: bucket all categories with frequency below a threshold "
        "into a single <RARE> token. Helps generalization and reduces noise.",
        "Hash trick: for very high cardinality, hash the category into a fixed-size table. "
        "Trades hash collisions for bounded memory.",
        "Production pattern: train the embedder jointly with downstream model. For online "
        "serving, export the embedding table as a lookup; new categories appearing at "
        "serve time map to the <UNK> embedding.",
     ]),

    ("How do you efficiently search billions of embeddings?",
     [
        "Use approximate nearest neighbor (ANN) indexes. Brute-force search is O(n·d) per "
        "query and infeasible at billion scale.",
        "HNSW (Hierarchical Navigable Small World): graph-based, fast queries, high recall. "
        "Default for many production systems. Memory-heavy.",
        "IVF (Inverted File): cluster the vectors into k centroids; at query time search "
        "only the most relevant clusters. Memory-friendly. Often combined with PQ.",
        "Product Quantization (PQ): compress each vector for memory efficiency. Combine "
        "with IVF for billion-scale indexes.",
        "FAISS, ScaNN, Annoy, NMSLIB are popular libraries. Pinecone, Weaviate, Qdrant, "
        "Milvus are managed vector databases.",
        "Tuning: pick the index type and parameters that hit your recall and latency "
        "targets. Use a held-out test set to measure recall@k and 95th percentile latency.",
     ],
     ["14_ann_search.png"]),

    ("How do you handle OOV words at embedding time in an LLM?",
     [
        "Modern LLMs use subword tokenizers (BPE, WordPiece, SentencePiece) that have no "
        "OOV problem at the input level: any string decomposes into known subword pieces. "
        "Even invented words become a sequence of meaningful subword embeddings.",
        "Where OOV-like issues still arise: domain-specific terminology that decomposes "
        "poorly into general subwords (e.g. drug names, chemical compounds, code "
        "identifiers). Mitigation: extend the tokenizer with domain tokens and continue "
        "pretraining briefly.",
        "Rare token quality: tokens that appear only a handful of times during pretraining "
        "have poor embeddings. Mitigation: subword fallback already helps; for critical "
        "rare tokens, supervised fine-tuning examples that exercise them improve quality.",
        "Cross-lingual OOV: tokens from a language poorly represented in pretraining have "
        "weak embeddings. Mitigation: continue pretraining on target-language corpora.",
     ]),

    ("How do you evaluate embedding quality?",
     [
        "Intrinsic evaluation: similarity benchmarks (STS-B, SICK) measure correlation "
        "between embedding cosine similarity and human similarity ratings. Word analogy "
        "tasks (king - man + woman = ?). Word similarity benchmarks (WordSim-353, "
        "SimLex-999).",
        "Extrinsic evaluation: downstream task performance. Use the embeddings as features "
        "for classification, retrieval, clustering. Report task-specific metrics: accuracy "
        "for classification, Recall@k for retrieval, V-measure for clustering.",
        "MTEB (Massive Text Embedding Benchmark): standardized benchmark across 50+ tasks "
        "in 8 categories. The de facto standard for comparing sentence embedders. Public "
        "leaderboard.",
        "Domain-specific evaluation: build a held-out set of relevant queries and known "
        "answers in your domain. Measure Recall@k and Mean Reciprocal Rank.",
     ]),

    ("Explain triplet loss in embedding learning.",
     [
        "Triplet loss trains embeddings such that an anchor is closer to a positive "
        "example than to a negative example by at least a margin. The loss for one "
        "triplet (a, p, n) is max(0, d(a, p) - d(a, n) + margin), where d is distance.",
        "Triplet sampling matters a lot. Random negatives are usually too easy (already "
        "far from the anchor) and provide little signal. Semi-hard negatives (negatives "
        "that are far enough from the anchor to satisfy the margin but still relatively "
        "close) provide the strongest gradient.",
        "Use cases: face recognition (FaceNet), person re-identification, fine-grained "
        "similarity. InfoNCE has largely replaced triplet loss in modern embedding "
        "training because it handles many negatives per anchor in one batch and is more "
        "stable.",
     ]),

    ("What is the margin in triplet or contrastive loss?",
     [
        "The margin is the minimum gap by which the anchor-positive distance must be less "
        "than the anchor-negative distance for the loss to be zero. A larger margin forces "
        "the model to learn more discriminative embeddings.",
        "Practical effects: too small a margin (0.01) makes the task too easy and produces "
        "weak embeddings. Too large a margin (10) is hard to satisfy and slows learning. "
        "Typical values: 0.2 to 1.0 depending on the distance metric and normalization.",
        "InfoNCE replaces the explicit margin with a temperature τ in softmax(score/τ). "
        "Lower τ behaves like a larger margin: only the closest negatives matter.",
     ]),

    ("Discuss overfitting in LLMs during training and how to prevent it.",
     [
        "LLMs trained on massive web-scale corpora rarely overfit during pretraining. "
        "Overfitting becomes a real concern during fine-tuning on smaller specialized "
        "datasets.",
        "Symptoms: training loss falls while held-out loss rises. Specific behaviors: "
        "memorization of training examples (the model recites them verbatim), narrow "
        "domain capability with degraded general reasoning (catastrophic forgetting).",
        "Mitigation: parameter-efficient fine-tuning (LoRA, qLoRA) limits trainable "
        "parameters and naturally regularizes. Mix domain data with general data to "
        "preserve broad capability. Apply weight decay (typical 0.01 to 0.1). Use early "
        "stopping based on validation. Use lower learning rates (1e-5 to 5e-5 for full FT, "
        "1e-4 for LoRA). Avoid overtraining: 1-3 epochs is usually enough for fine-tuning.",
     ],
     ["17_overfitting.png"]),

    ("How do you adapt learning rates for LLM training stability?",
     [
        "Warm-up: linearly increase from near-zero to the target learning rate over the "
        "first 1-5% of training steps. Prevents huge initial updates that destabilize the "
        "model.",
        "Decay: after warm-up, decay the learning rate. Cosine decay is the default for "
        "pretraining. Linear decay or constant-with-decay for fine-tuning.",
        "Learning rate magnitude: pretraining typically uses 1e-4 to 6e-4 peak. Full fine-"
        "tuning uses 1e-5 to 5e-5. LoRA can use 1e-4 to 3e-4. RLHF/RL uses 1e-6 to 5e-6.",
        "Layer-wise learning rate decay: smaller learning rates for earlier layers (which "
        "encode general patterns) and larger for later layers (which encode task-specific "
        "patterns). Helps prevent catastrophic forgetting during fine-tuning.",
        "Monitor: training loss, gradient norm, parameter norm. Diverging loss or "
        "exploding gradient norm signal the learning rate is too high.",
     ]),

    ("How do you handle long context lengths efficiently?",
     [
        "Architectural: use sparse or sliding-window attention (Longformer, Mistral's "
        "sliding window). Use linear attention or state-space models (Mamba). Use grouped-"
        "query or multi-query attention to reduce KV-cache size.",
        "System: FlashAttention reduces memory and speeds up exact attention. KV-cache "
        "compression. KV-cache offloading to CPU or disk for very long sessions. "
        "PagedAttention (vLLM) manages KV-cache like virtual memory.",
        "Modeling: extend position encodings via RoPE scaling, YaRN, ALiBi for length "
        "extrapolation. Continue pretraining on long-context data.",
        "Application: RAG to inject only relevant chunks instead of stuffing the full "
        "context. Hierarchical summarization for very long documents. Sliding-window "
        "inference for streaming inputs.",
     ]),

    ("What metrics judge LLM generation quality?",
     [
        "Reference-based: BLEU (translation), ROUGE (summarization), METEOR, CIDEr "
        "(captioning), exact match (QA). All measure n-gram overlap with reference, which "
        "correlates only weakly with quality for open-ended generation.",
        "Embedding-based: BERTScore, BLEURT use contextual embeddings to compare candidate "
        "and reference. Better than n-gram overlap.",
        "LLM-as-a-judge: a separate strong model rates the candidate against a rubric or "
        "pairwise against another candidate. Beware position, verbosity, and self-"
        "preference biases.",
        "Human evaluation: still the gold standard for open-ended generation. Cohort "
        "ratings on fluency, relevance, factuality, helpfulness, harmlessness.",
        "Task-specific: pass@1 / pass@k for code (HumanEval, MBPP). Win-rate on MT-Bench "
        "or Chatbot Arena for chat. Factuality on TruthfulQA. Reasoning on MMLU, "
        "BIG-Bench, GSM8K.",
     ]),

    ("How do you evaluate and mitigate hallucinations in LLMs?",
     [
        "Detect: build a held-out fact-verification set. Compare model claims against a "
        "trusted knowledge base. Use an NLI model to check whether generated claims are "
        "entailed by retrieved evidence. TruthfulQA tests for known factual errors. "
        "FactScore decomposes claims and verifies each.",
        "Mitigate at inference: RAG with high-quality retrieval keeps generation grounded "
        "in evidence. Force the model to cite sources and verify citations. Use lower "
        "temperature for factual tasks. Add chain-of-thought to expose reasoning.",
        "Mitigate at training: fine-tune on data with explicit grounding (Self-RAG-style "
        "with critique tokens). Apply RLHF or DPO with preferences for grounded over "
        "ungrounded responses. Train on examples where the correct response is 'I don't "
        "know.' Reward calibrated uncertainty.",
        "Monitoring in production: sample traffic for offline verification; alert when "
        "hallucination rate drifts; collect user feedback signals.",
     ]),

    ("What is a Mixture of Experts (MoE) model?",
     [
        "MoE is an architecture where multiple specialized expert subnetworks (typically "
        "feed-forward blocks) coexist, and a learned router activates only a few experts "
        "per token. Total parameter count is large, but FLOPs per token stay close to a "
        "much smaller dense model.",
        "Mechanics: a gating network produces a score per expert per token. The top-k "
        "experts (often k=1 or k=2) are activated. Each activated expert processes the "
        "token; outputs are combined weighted by gating scores.",
        "Benefits: compute-efficient scaling. A 8x7B MoE can match a 70B dense model's "
        "quality at a fraction of the inference cost.",
        "Challenges: load balancing (experts get specialized to specific kinds of input, "
        "but you want them used roughly equally), training stability (router behavior is "
        "non-smooth), memory (all expert weights must be in memory even if rarely used). "
        "Examples: Mixtral 8x7B, Switch Transformer, DeepSeek-V3.",
     ]),

    ("Why is perplexity a problematic metric for LLM evaluation?",
     [
        "Perplexity measures average per-token uncertainty on a held-out corpus: lower is "
        "'better at predicting the next token.' But many things matter for LLM utility "
        "that perplexity does not capture.",
        "What perplexity misses: factuality (a fluent lie has low perplexity), reasoning "
        "(predicting the next token of a correct chain-of-thought is different from being "
        "able to reason), instruction following, harmlessness, calibration (knowing when "
        "to refuse), code correctness, multi-turn coherence.",
        "Perplexity also depends on the evaluation corpus. A model with low perplexity on "
        "Reddit may have higher perplexity on legal text yet still be the better choice for "
        "legal tasks.",
        "Better: combine perplexity (for sanity-check on representativeness) with "
        "task-specific benchmarks (MMLU, HumanEval, MT-Bench) and human evaluation.",
     ]),

    ("How does Stable Diffusion leverage LLMs to generate high-quality images from text?",
     [
        "Stable Diffusion is a latent diffusion model. It consists of: (a) a VAE that "
        "encodes images to a small latent space (8x compression) and decodes back; (b) a "
        "U-Net that performs the diffusion process in the latent space; (c) a text "
        "encoder (CLIP or T5) that converts the text prompt into a sequence of embeddings.",
        "The U-Net cross-attends to the text embeddings at every layer and timestep. This "
        "is the mechanism by which language conditions image generation. The text encoder "
        "must understand the prompt well enough that the U-Net can condition on it; this "
        "is why SDXL uses two text encoders and Stable Diffusion 3 uses a T5-XXL.",
        "Process: encode the prompt with the text encoder; sample Gaussian noise in latent "
        "space; iteratively denoise the latent for 20-50 steps via the U-Net, conditioned "
        "on text embeddings; decode the final latent through the VAE to produce a pixel "
        "image.",
        "Classifier-free guidance amplifies the text conditioning: at each step, compute "
        "both the conditional and unconditional denoising prediction, then push the "
        "prediction in the direction of the conditional prediction by a guidance scale.",
     ]),
]
