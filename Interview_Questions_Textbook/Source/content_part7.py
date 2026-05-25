"""Part 7: Supplementary chapter with content integrated from the external
Generative AI Interview Questions PDF (Mohammad Arbaaz Khan). Adds material
not deeply covered elsewhere in the textbook."""

SUPPLEMENT = [
    # ---------- Mathematical formulas reference ----------
    ("Mathematical formulas reference: perplexity, attention, TF-IDF, triplet loss",
     [
        "This question gathers the most-asked formulas in one place so that "
        "you can recall them under interview pressure.",
        "Perplexity. For a sequence w_1, ..., w_N, perplexity is "
        "P = 2^(-1/N · Σᵢ log₂ P(wᵢ | w_1,...,wᵢ₋₁)). Lower is better; "
        "equivalent to the exponential of average per-token cross-entropy.",
        "Scaled dot-product attention. Attention(Q, K, V) = "
        "softmax(QKᵀ / √d_k) · V. The √d_k scaling keeps softmax in a "
        "usable range as the head dimension grows; without it, large dot "
        "products push softmax into saturation and gradients vanish.",
        "Multi-head attention. Run h attention computations in parallel "
        "with different W_Q, W_K, W_V projections each of dimension d_model / h; "
        "concatenate; project back with W_O.",
        "Term Frequency: TF(t, d) = count(t in d) / total terms in d.",
        "Inverse Document Frequency: IDF(t) = log(N / df(t)), where N is "
        "total documents and df(t) is documents containing t.",
        "TF-IDF(t, d) = TF(t, d) · IDF(t).",
        "Triplet loss: L(A, P, N) = max(0, d(A, P) - d(A, N) + margin), "
        "where d is a distance (Euclidean or cosine). The margin enforces "
        "minimum separation between matched and mismatched pairs.",
        "InfoNCE loss: L = -log(exp(sim(a, p)/τ) / Σⱼ exp(sim(a, j)/τ)), "
        "where the sum is over the positive plus all in-batch negatives; "
        "τ is the temperature.",
        "BM25 score: Σ IDF(qᵢ) · (f(qᵢ, d)(k+1)) / (f(qᵢ, d) + k(1-b+b·|d|/avgdl)). "
        "Saturates with term frequency (controlled by k) and normalizes for "
        "document length (controlled by b).",
        "Cross-entropy loss: -Σ yᵢ log(pᵢ), where y is the one-hot label and "
        "p is the predicted probability. Reduces to -log(p_true_class) for "
        "one-hot targets.",
        "KL divergence: D_KL(p || q) = Σ p(x) log(p(x) / q(x)). Asymmetric. "
        "Used as a regularizer in PPO (keep policy close to reference) and in "
        "VAEs (latent prior matching).",
     ]),

    # ---------- Additional pretraining mechanisms ----------
    ("Beyond MLM and CLM, what other pretraining objectives have been used for LLMs?",
     [
        "Permutation Language Modeling (PLM). Introduced in XLNet. Train the "
        "model to predict tokens in a randomly permuted order so that, for "
        "any given target token, the model sees a mixture of left and right "
        "context (without using masking that breaks BERT's pretrain/fine-tune "
        "consistency). Blends the bidirectional benefit of MLM with the "
        "autoregressive property of CLM. More complex to train than either.",
        "Denoising Auto-encoding (span corruption). Used in T5 and BART. Take "
        "a sentence, corrupt it by masking spans of tokens (T5) or by general "
        "noise functions like deletion, infilling, sentence permutation, "
        "and rotation (BART). Train the decoder to reconstruct the original. "
        "Generalizes MLM from single tokens to contiguous spans; aligns "
        "naturally with text-to-text framing.",
        "Replaced Token Detection (ELECTRA). A small generator proposes "
        "replacements for masked tokens; a larger discriminator classifies "
        "each token as 'original' or 'replaced'. More sample-efficient than "
        "MLM because every token contributes to the loss.",
        "Prefix Language Modeling. Bidirectional attention over a prefix, "
        "causal attention over a suffix. Used in some encoder-decoder hybrids "
        "to combine BERT-style understanding with GPT-style generation.",
        "Why this matters in interviews: knowing the menu of objectives "
        "signals that you understand the design space, not just the BERT/GPT "
        "binary.",
     ]),

    # ---------- Efficient & memory-augmented transformers ----------
    ("What efficient or memory-augmented transformer variants exist for long context?",
     [
        "The vanilla transformer's O(n²) self-attention is the binding "
        "constraint for long sequences. Several families relax it.",
        "Sparse / windowed attention. Longformer combines sliding-window "
        "local attention with a few designated global tokens. BigBird adds "
        "random attention on top. Each token attends to O(n) tokens instead "
        "of O(n²). Used in long-document tasks (legal, biomedical, document "
        "QA).",
        "Linearized attention. Linformer projects K and V to a lower-rank "
        "k_proj before attention, giving O(n·k) complexity. Performer "
        "approximates softmax with random feature maps. Reformer replaces "
        "softmax with LSH-based bucketing. Each trades exact attention for "
        "asymptotic improvement; quality varies by task.",
        "Memory-enhanced models. Transformer-XL caches hidden states from "
        "the previous segment and lets the current segment attend to them. "
        "Equivalent to an extended context window without re-computing. "
        "Compressive Transformer compresses old states rather than dropping "
        "them.",
        "State-space models. Mamba and S4 use selective state-space updates "
        "with sub-quadratic time. Competitive with transformers on long-"
        "context benchmarks at significantly lower cost.",
        "Retrieval augmentation as an alternative. Instead of extending the "
        "context window, retrieve relevant chunks per query (RAG). Often the "
        "right answer when you can structure your problem this way.",
        "Position-encoding tricks for length extrapolation. RoPE with NTK-"
        "aware or YaRN scaling, ALiBi position bias. Let a model trained at "
        "short context generalize to longer contexts without retraining.",
     ]),

    # ---------- Embedding quality metrics extended ----------
    ("Beyond Recall@k, what quantitative metrics evaluate embedding quality?",
     [
        "Recall@k, Precision@k, MRR, NDCG cover retrieval quality. Beyond "
        "those, several intrinsic and clustering-based metrics matter for "
        "evaluating embeddings as embeddings.",
        "Cosine similarity correlation with human judgments. Compute the "
        "cosine similarity of an embedding pair and correlate it with human-"
        "labeled similarity (Spearman or Pearson). Standard for sentence "
        "similarity (STS-B). Spearman is the de facto reporting metric for "
        "embedding model leaderboards (MTEB).",
        "Average Pairwise Distance (APD). Mean pairwise distance within a "
        "cluster (anisotropy proxy at corpus scale). Lower APD across "
        "unrelated documents = healthier (less anisotropic) embedding space.",
        "Silhouette Score. For each point, (b - a) / max(a, b), where a is "
        "mean distance to same-cluster points and b is mean distance to "
        "nearest other cluster. Range [-1, 1]. Higher = better separation. "
        "Useful when you have ground-truth clusters.",
        "Davies-Bouldin Index. Ratio of within-cluster scatter to between-"
        "cluster separation, averaged over clusters. Lower = better. Used in "
        "topic-modeling evaluation of embeddings.",
        "Calinski-Harabasz Index. Variance-ratio criterion. Higher = better.",
        "Analogy benchmarks. Classic 'king - man + woman ≈ queen' style. "
        "Useful as a sanity check; less informative than retrieval benchmarks "
        "on modern embedders.",
        "MTEB. Massive Text Embedding Benchmark. 50+ tasks across "
        "classification, clustering, retrieval, reranking, similarity. The "
        "comprehensive standard.",
     ]),

    # ---------- Quantization types ----------
    ("Explain the main types of embedding quantization and their tradeoffs.",
     [
        "Quantization reduces the precision of stored embeddings to save "
        "memory at some cost to recall. Three main families.",
        "Uniform (scalar) quantization. Each dimension is quantized "
        "independently to a fixed range, typically int8 or int4. Cheapest to "
        "implement. Embedding × dimension × bits/8 bytes per vector. Loss "
        "usually under 1 percentage point on retrieval. Default first step.",
        "Non-Uniform quantization. The quantization grid adapts to the value "
        "distribution. K-means quantization (each dimension's values split "
        "into k clusters) and learned quantizers (mu-law, NF4 from QLoRA) "
        "fit this category. Better quality at the same bit rate; more "
        "complex to compute.",
        "Product Quantization (PQ). Split each vector into m subvectors. "
        "Train k codewords per subvector via k-means. Replace each subvector "
        "with its nearest codeword index. Storage: m · log₂(k) bits per "
        "vector, often 32x smaller than fp32. Used by FAISS at billion-scale. "
        "Approximate distance is computed by table lookup. Variants: OPQ "
        "(rotate before quantizing), Residual PQ (multi-stage), and Inverted "
        "File + PQ for the standard FAISS index.",
        "Binary embeddings. One bit per dimension. Hamming distance instead "
        "of cosine. 32x compression. Usable for first-stage retrieval; "
        "production systems rerank with full-precision embeddings on the "
        "candidate set.",
        "Choosing: start with int8 if memory is not the binding constraint; "
        "move to PQ when memory is. Always benchmark the recall hit on your "
        "own data.",
     ]),

    # ---------- Rare word advanced ----------
    ("What advanced strategies exist for handling rare words and OOV terms?",
     [
        "Subword tokenization (BPE, WordPiece, SentencePiece) is the modern "
        "default and eliminates most OOV issues. The remaining failure cases "
        "are rare and domain-specific; the techniques below cover them.",
        "FastText subword embeddings. Represent each word as a sum of its "
        "character n-gram embeddings. Even an unseen word receives a "
        "meaningful vector from its character pieces.",
        "Retrofitting with external lexical resources. Modify pretrained "
        "embeddings to bring semantically related words (from WordNet, "
        "PPDB, or a domain ontology) closer together. Cheap post-hoc fix that "
        "improves embedding quality on domains where lexical relations "
        "matter more than corpus statistics.",
        "Contextual averaging. For a very rare word, average the contextual "
        "embeddings of its surrounding context words from a large corpus. "
        "Gives a rough estimate when the word itself has too few "
        "occurrences for a stable embedding.",
        "Phonetic or morphological fallback (Soundex, Metaphone, "
        "Levenshtein-based matching). When a rare word does not decompose "
        "well into known subwords, match it phonetically to a known word and "
        "use that embedding. Useful for noisy text (OCR, ASR transcripts).",
        "Embedding imputation. For a missing token, use the mean of similar "
        "tokens' embeddings, the embedding of the lemma, or the embedding of "
        "the closest known word.",
        "Domain tokenizer extension. Add domain-specific tokens (drug names, "
        "chemical formulas, ticker symbols, code identifiers) to the "
        "tokenizer; continue pretraining briefly so the new tokens learn "
        "good embeddings. Standard pattern for production domain adaptation.",
        "Few-shot / zero-shot embedding inference. Modern LLMs can produce "
        "a contextual embedding for any string at inference; no separate "
        "OOV handling needed at the model level.",
     ]),

    # ---------- Image synthesis losses deep dive ----------
    ("Deep dive: image synthesis losses including Total Variation and Style/Content losses",
     [
        "Pixel-wise losses (L1, L2). Simple per-pixel difference. Easy to "
        "compute, prone to blurry outputs because the optimal solution under "
        "L2 is the mean of plausible images. Effective as a baseline or as "
        "one term in a composite loss.",
        "Perceptual loss (LPIPS, VGG-feature). Compare generated and target "
        "in a frozen pretrained network's feature space. Much better "
        "correlated with human perception than pixel-wise loss. Standard in "
        "super-resolution, style transfer, and image-to-image translation.",
        "Adversarial loss. GAN discriminator trained to distinguish real "
        "from generated; generator trained to fool it. Pushes outputs onto "
        "the manifold of real images; produces sharper results than "
        "pixel-wise losses. Hard to stabilize.",
        "Style and Content Loss (Gatys et al.). For style transfer, "
        "decompose: content loss is feature-map L2 against the content image "
        "at deep layers; style loss is the L2 between Gram matrices of "
        "feature maps at shallow layers (Gram matrix captures texture "
        "statistics independent of spatial position). Total loss is a "
        "weighted sum; the weight controls content-vs-style emphasis.",
        "Total Variation (TV) loss. Penalizes the sum of absolute "
        "differences between neighboring pixels: TV(x) = Σ |x_{i+1,j} - x_{i,j}| "
        "+ |x_{i,j+1} - x_{i,j}|. Encourages smoothness. Reduces checkerboard "
        "artifacts and noise in generated images. Used as a regularizer in "
        "super-resolution and inpainting.",
        "Diffusion model losses. Predict the noise added to a clean image at "
        "random timesteps, minimizing MSE between predicted and actual noise. "
        "Simple and stable. v-prediction and EDM parameterizations are "
        "variants. Latent diffusion (Stable Diffusion) applies this in the "
        "VAE latent space, not pixel space.",
        "Composite recipes. Production image generation uses combinations: "
        "for super-resolution, pixel + perceptual + adversarial + TV. For "
        "style transfer, content + style + optional TV. Tuning the weights "
        "is empirical.",
     ]),

    # ---------- Diffusion samplers ----------
    ("What are common diffusion samplers and how do they differ?",
     [
        "Diffusion models generate by iteratively denoising a random latent. "
        "The sampler is the integration scheme used to step through the "
        "reverse-diffusion ODE/SDE.",
        "DDPM (denoising diffusion probabilistic models). The original "
        "ancestral sampler. Stochastic. Needs many steps (~1000) for high "
        "quality.",
        "DDIM (denoising diffusion implicit models). Deterministic, allows "
        "much fewer steps (20-50). Same trained model, different sampling. "
        "Standard default for Stable Diffusion.",
        "PNDM (pseudo numerical methods for diffusion models). Uses a "
        "linear multistep method (Adams-Bashforth-Moulton style) for higher "
        "accuracy at fewer steps. Faster than DDIM at similar quality.",
        "DPM-Solver and DPM-Solver++. Use exponential integrators to take "
        "very large steps. 10-20 steps often suffice. Common in production "
        "image generation services.",
        "Euler, Euler ancestral, Heun. ODE solvers used by k-diffusion / "
        "Karras-style schedulers. Different tradeoffs for stochasticity and "
        "step count.",
        "UniPC. Universal Predictor-Corrector method. Very few steps (~10) "
        "for similar quality to many-step samplers.",
        "Practical guidance: DPM-Solver++ at 20-30 steps is a strong "
        "default for SDXL and similar. Lower steps = faster but less "
        "detailed; higher steps = diminishing returns.",
     ]),

    # ---------- Multimodal RAG metrics ----------
    ("What metrics specifically evaluate multimodal RAG quality?",
     [
        "Text generation metrics. BLEU, ROUGE, METEOR for surface overlap; "
        "BERTScore for semantic similarity. Inherited from text-only "
        "evaluation; necessary but not sufficient for multimodal.",
        "Image captioning metrics. CIDEr (Consensus-based Image Description "
        "Evaluation) weights n-grams by their TF-IDF across reference "
        "captions. Higher = better. SPICE evaluates the semantic propositional "
        "content (objects, attributes, relations) extracted from captions; "
        "captures meaning beyond surface form.",
        "Vision-language alignment. CLIP Score: cosine similarity between "
        "the CLIP image embedding and the CLIP text embedding of the "
        "caption. Cheap and language-agnostic. VLP Score: similar with a "
        "vision-language pretraining model.",
        "Multimodal Relevance Score. Combine per-modality retrieval scores "
        "into a single measure. Approaches: rank fusion, weighted sum, or "
        "joint reranking with a cross-modal scorer.",
        "Faithfulness across modalities. Verify that generated text and "
        "generated images do not contradict each other. NLI-style checks "
        "(text claims vs image content) and vision-language entailment.",
        "LMM-as-a-Judge. Use a strong multimodal model (GPT-4o, Gemini) to "
        "rate outputs on a rubric. Extends LLM-as-a-judge to multimodal. "
        "Same biases apply (position, verbosity, self-preference); control "
        "with randomization and different judge models.",
        "Human evaluation. Still gold standard for nuanced qualities: "
        "creativity, aesthetic quality, factual grounding across modalities.",
        "Modality-specific precision and recall. Compute per-modality so a "
        "weakness in one modality is not masked by strength in another.",
     ]),

    # ---------- Hallucination evaluation specifics ----------
    ("What specific metrics and frameworks evaluate hallucination in LLMs and RAG?",
     [
        "FactCC. Trained classifier that scores whether a generated "
        "sentence is consistent with a source document. Originally for "
        "summarization. Use as a faithfulness metric on RAG outputs.",
        "FEVER (Fact Extraction and Verification). Benchmark and pipeline "
        "for verifying claims against a Wikipedia-derived knowledge base. "
        "Three-way classification: supported, refuted, not enough info. "
        "Adapted for LLM output verification.",
        "QAGS (Question-Answer Generation and Summarization). Generate "
        "questions from the candidate text; answer them using the source. "
        "Mismatch indicates hallucination. More robust than n-gram-overlap "
        "metrics.",
        "FactScore. Decompose generated text into atomic facts. Verify each "
        "fact against a knowledge source. Report the fraction supported. "
        "Strong correlation with human judgment.",
        "TruthfulQA. Benchmark of 817 questions designed to elicit common "
        "false beliefs (urban legends, misconceptions). Tests whether the "
        "model parrots common falsehoods or knows the truth.",
        "SelfCheckGPT. Sample multiple responses; compare consistency. "
        "Inconsistent answers signal hallucination. No external knowledge "
        "base needed.",
        "Confidence scoring and thresholding. Use the model's own predicted "
        "probability or a calibrated estimate; refuse or flag low-confidence "
        "outputs. Calibration techniques: temperature scaling, "
        "verbalized confidence, ensemble agreement.",
        "Retrieval-grounded verification. For RAG, check that each claim in "
        "the output is entailed by the retrieved passages (NLI-based). Block "
        "contradictions; flag neutral verdicts.",
        "Citation accuracy. The model cites a source; verify that the cited "
        "source actually contains the claim. Common metric in agentic RAG "
        "and grounded generation.",
     ]),

    # ---------- ImageBind and unified multimodal embeddings ----------
    ("What is ImageBind, and how does it unify multimodal embeddings?",
     [
        "ImageBind (Meta, 2023) is a model that learns a single embedding "
        "space across six modalities: images, text, audio, depth, thermal, "
        "and IMU (inertial measurement unit) data.",
        "Key idea: pair every non-image modality with images during "
        "training. Images become the binding modality. (image, audio) pairs, "
        "(image, text) pairs, (image, depth) pairs and so on. Train with "
        "contrastive loss. The result: even modalities never paired with "
        "each other (e.g., audio and text) end up aligned through their "
        "shared alignment with images.",
        "Why it matters: cross-modal retrieval and generation without "
        "explicit pairings between every modality combination. Search audio "
        "with text, find images matching a thermal signature, drive image "
        "generation from sound.",
        "Use cases: multimodal search engines that accept any modality as "
        "query; multimodal RAG systems; generative models conditioned on "
        "non-traditional inputs.",
        "Successors: AudioCLIP, LanguageBind, OneLLM extend the pattern. "
        "The space is active and competitive.",
     ]),

    # ---------- Soundex / phonetic similarity ----------
    ("When and how do you use phonetic similarity (Soundex) in NLP?",
     [
        "Soundex is an algorithm that maps words to a short code based on "
        "how they sound. Words that sound alike map to the same code. "
        "Robert and Rupert map to R163; Smith and Smythe to S530.",
        "Algorithm: keep the first letter. Encode the rest by category: "
        "BFPV → 1, CGJKQSXZ → 2, DT → 3, L → 4, MN → 5, R → 6. Drop "
        "vowels and HW. Drop consecutive duplicates. Pad with zeros to 4 "
        "characters.",
        "Variants. Metaphone and Double Metaphone are more linguistically "
        "principled (handle silent letters, common digraphs). Caverphone for "
        "names with New Zealand accents. NYSIIS for surname matching.",
        "Use cases. Fuzzy name matching in databases (especially "
        "genealogical, medical, customer records). OCR error correction "
        "when subword tokenizers fail. Voice-to-text fallback when ASR "
        "produces near-homophone errors. Domain-specific entity "
        "resolution where spelling varies (Mohammed, Muhammad, Mohamed).",
        "When to use: as a fallback when exact-match and subword-based "
        "matching fail. Combine with edit distance and embedding similarity "
        "in a layered matching pipeline.",
        "Limits: English-centric. Loses meaningful information for many "
        "languages. Useless for tonal languages and logographic scripts.",
     ]),

    # ---------- Modality dropout ----------
    ("What is modality dropout, and why is it useful in multimodal training?",
     [
        "Modality dropout randomly hides one or more modalities during "
        "training, forcing the model to learn useful representations from "
        "any subset of available modalities.",
        "Why it helps. Without modality dropout, the model can overfit to "
        "the most informative modality, ignoring others. With modality "
        "dropout, the model must produce useful outputs even when its "
        "favorite modality is unavailable. The trained model is robust to "
        "missing modalities at inference (a video without audio, an image "
        "without caption).",
        "Implementation. For each training example, sample a binary mask "
        "over modalities (with some probability of including each). Zero out "
        "or mask the embeddings of the dropped modalities. Adjust the "
        "attention layers so they ignore zeroed positions.",
        "Hyperparameter. Typical dropout probability per modality: 0.2 to "
        "0.4. Tune on a validation set with simulated missing modalities.",
        "Related techniques. Modality-specific learning rates to prevent "
        "one modality from dominating. Gradient balancing (uncertainty "
        "weighting, GradNorm) to balance contributions during training.",
     ]),
]
