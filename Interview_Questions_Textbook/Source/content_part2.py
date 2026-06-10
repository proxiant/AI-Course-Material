"""Part 2: Transformers and extended architectures."""

TRANSFORMERS = [
    ("Describe learning rate scheduling and its role in optimizing generative model training.",
     [
        "A learning rate schedule changes the learning rate over the course of training "
        "rather than holding it constant. The two motivations: (1) very early in training, "
        "the model is far from any good basin, so large steps help quickly; but the random "
        "initialization can produce huge gradients, so a brief warm-up smooths this. (2) "
        "Late in training, smaller steps help the optimizer settle into a sharp minimum "
        "instead of bouncing around it.",
        "Common schedules: linear warm-up followed by linear or cosine decay (transformer "
        "default). One-cycle (Smith): linear warm-up, then linear decay below the initial "
        "rate. Step decay: drop by a factor every N epochs. Inverse-square-root: classical "
        "for transformers, η ∝ 1/√t after warm-up. Plateau-based: decay when validation "
        "stops improving.",
        "For generative models specifically, schedules matter more because the loss surface "
        "is non-stationary as the model's outputs improve. RLHF often uses much smaller "
        "learning rates than SFT (1e-6 vs 1e-5) because policy drift is the main risk.",
     ]),

    ("Discuss transfer learning in NLP. How do pretrained language models help downstream tasks?",
     [
        "The dominant paradigm in NLP since 2018: pretrain a transformer on self-"
        "supervised objectives over a massive corpus, then transfer that knowledge to "
        "downstream tasks. The pretrained model has learned general syntactic and semantic "
        "patterns and can be specialized cheaply.",
        "Forms of transfer: (a) feature extraction with frozen encoder, (b) full fine-"
        "tuning, (c) parameter-efficient fine-tuning (LoRA, adapters, prefix tuning), "
        "(d) prompt-based zero-/few-shot via in-context learning, (e) instruction tuning "
        "to make a base model follow instructions, (f) RLHF for alignment.",
        "Benefit: the cost of pretraining is paid once (hundreds of GPU-years for a frontier "
        "model). Downstream users pay a tiny fraction to adapt. This is why a small startup "
        "can fine-tune LLaMA-3-70B in a few hours on a handful of GPUs and produce a model "
        "competitive on a specific task.",
     ],
     ["12_adaptation_ladder.png"]),

    ("What are the key differences between GPT and BERT?",
     [
        "Architecture: BERT is encoder-only with bidirectional self-attention. GPT is "
        "decoder-only with causal (left-to-right) masked self-attention. BERT sees the full "
        "input at once; GPT sees only the prefix.",
        "Pretraining objective: BERT uses masked language modeling (predict masked tokens "
        "from bidirectional context) plus next-sentence prediction. GPT uses causal language "
        "modeling (predict next token from left context only).",
        "Use case: BERT is best for understanding tasks (classification, NER, extractive "
        "QA, similarity) where you need rich bidirectional representations of an input. "
        "GPT is best for generation (chat, completion, text-to-text, code generation) where "
        "you produce tokens one at a time conditioned on the prefix.",
        "Modern state: instruction-tuned decoder-only LLMs (GPT-4, Claude, LLaMA, Gemini) "
        "have become the dominant pattern because they handle both understanding and "
        "generation via prompting. BERT-style encoders remain dominant for embedding "
        "generation and classification at scale where latency and cost matter.",
     ]),

    ("What problems with RNNs do transformer models solve?",
     [
        "Sequential processing: an RNN must process tokens one at a time because each step "
        "depends on the previous hidden state. Transformers process all tokens in parallel "
        "during training via self-attention, dramatically speeding up training on modern "
        "GPUs and TPUs.",
        "Long-range dependencies: an RNN compresses everything before time t into a single "
        "hidden vector. Information from distant tokens gets diluted or lost. Self-attention "
        "lets every token directly attend to every other token, regardless of distance.",
        "Vanishing/exploding gradients: BPTT through many timesteps suffers gradient "
        "instability. Transformers have a shallower effective depth from any one token to "
        "any other (one attention hop), and use residual connections plus layer "
        "normalization to keep gradients well-behaved.",
        "Modeling capacity per parameter: empirically, transformers scale better than RNNs. "
        "Doubling parameters in a transformer reliably improves performance; the same is not "
        "true for vanilla RNNs.",
     ],
     ["08_rnn.png", "09_transformer.png"]),

    ("How is the transformer different from RNN and LSTM?",
     [
        "RNN/LSTM process sequences sequentially with a recurrent hidden state. Transformers "
        "process sequences in parallel using self-attention. RNN/LSTM mix information one "
        "step at a time; transformers mix in one shot via the Q·K matrix.",
        "Compute cost: RNN/LSTM are O(n) sequential steps with O(d²) work per step. "
        "Transformer self-attention is O(n²·d) per layer but fully parallel. For typical n "
        "and d on a GPU, the transformer is much faster per training step.",
        "Memory: transformer attention is O(n²) memory in the naive form, which is the main "
        "scalability bottleneck. FlashAttention and other techniques reduce constants; "
        "linear-attention and state-space models (Mamba) trade off expressiveness for "
        "asymptotic memory.",
        "Position handling: RNN/LSTM encode position implicitly through the sequential "
        "processing. Transformers have no built-in notion of position and must add explicit "
        "positional encodings (absolute, learned, or relative such as RoPE).",
     ]),

    ("How does BERT work, and what makes it different from previous NLP models?",
     [
        "BERT is a stack of transformer encoder layers pretrained on two self-supervised "
        "objectives: Masked Language Modeling (mask 15% of input tokens, predict them from "
        "both left and right context) and Next Sentence Prediction (binary classification: "
        "are these two sentences contiguous?). It uses WordPiece tokenization.",
        "What was new: previous NLP models either used left-to-right context (ELMo could "
        "concatenate forward and backward, but not jointly) or task-specific architectures. "
        "BERT pretrained a single bidirectional model and then added a thin task-specific "
        "head for any downstream task. This unified pattern, plus the strength of "
        "bidirectional context, set new state-of-the-art across many benchmarks.",
        "Downstream pattern: prepend a [CLS] token to the input; for classification, run a "
        "linear head on the final [CLS] embedding; for token-level tasks like NER, run a "
        "head on each token's final embedding; for span tasks like SQuAD, predict start and "
        "end token positions.",
     ]),

    ("Why is incorporating relative positional information crucial in transformer models?",
     [
        "Self-attention is permutation-equivariant: shuffling the input tokens produces a "
        "shuffled output. To restore order, you must inject position information. Absolute "
        "positional encoding (sinusoidal in the original transformer, learned in BERT) "
        "tells the model 'this token is at position 5'.",
        "Relative position encoding instead tells the model 'this query is k positions "
        "after this key'. This is closer to what the attention computation actually needs: "
        "the relevance of one token to another usually depends on their separation, not "
        "their absolute positions.",
        "When relative position helps: tasks where similar patterns appear at different "
        "absolute positions (most language tasks), and when generalizing to sequences "
        "longer than those seen during training. Rotary Position Embeddings (RoPE), used "
        "in LLaMA, GPT-NeoX, and many modern LLMs, encode relative position by rotating the "
        "Q and K vectors. ALiBi adds a position-dependent bias to attention scores. Both "
        "extrapolate better than absolute encodings.",
     ]),

    ("What challenges arise from the fixed and limited attention span in vanilla Transformers?",
     [
        "The vanilla transformer has a fixed maximum context length set at pretraining time "
        "(typically 512 for BERT, 1024 for GPT-2, up to 200K+ for modern LLMs). Inputs "
        "longer than this must be truncated or chunked, losing information.",
        "Effects: tasks requiring long-range dependencies (long documents, codebases, video) "
        "lose context that should inform the prediction. The model cannot reference details "
        "outside its window. Memory and compute scale O(n²) with context length, so simply "
        "training with a longer window is expensive.",
        "Mitigations: sliding-window attention; sparse attention patterns (Longformer, "
        "BigBird); retrieval augmentation (RAG) so the model sees only relevant chunks; "
        "hierarchical models that summarize chunks then attend over summaries; "
        "state-space models (Mamba) and linear attention for sub-quadratic scaling.",
     ]),

    ("Why is naively increasing context length not straightforward?",
     [
        "Three constraints: memory, compute, and quality.",
        "Memory: self-attention stores an n×n score matrix per head per layer. Doubling n "
        "quadruples memory. For 32K context with 32 heads and 32 layers, the attention "
        "memory alone is many GB. FlashAttention reduces this by tiling but cannot beat the "
        "n² fundamental.",
        "Compute: every attention operation costs O(n²·d). Doubling n quadruples FLOPs. "
        "Training and inference cost scale accordingly.",
        "Quality: models pretrained on short contexts do not automatically generalize to "
        "long contexts. Positional encodings may extrapolate poorly. The model needs "
        "training on long-context examples, which requires long-context training data and "
        "is itself expensive. Length generalization techniques (RoPE scaling, ALiBi, YaRN) "
        "help but require care.",
     ]),

    ("How does self-attention work?",
     [
        "Self-attention computes a new representation of each token as a weighted average of "
        "all token representations, where the weights depend on similarity between tokens. "
        "Mechanics in five steps:",
        "1. Project each input token x_i into three vectors: query Q_i = W_Q · x_i, key "
        "K_i = W_K · x_i, value V_i = W_V · x_i.",
        "2. Compute pairwise scores: S_ij = Q_i · K_j / sqrt(d). The √d scaling keeps "
        "softmax in a usable range.",
        "3. Apply softmax row-wise to get attention weights: A_ij = softmax(S)_ij. Each row "
        "sums to 1.",
        "4. Combine value vectors: output_i = Σ_j A_ij · V_j.",
        "5. Multi-head attention runs steps 1-4 in parallel h times with different W_Q, W_K, "
        "W_V matrices, concatenates the outputs, and projects back to the model dimension.",
        "For causal (decoder) attention, mask scores S_ij for j > i to -∞ before softmax so "
        "each position only attends to itself and earlier positions.",
     ],
     ["10_attention.png"]),

    ("What pretraining mechanisms are used for LLMs?",
     [
        "Causal language modeling (next-token prediction). Predict token t given tokens 1 "
        "to t-1. Used in GPT, LLaMA, Mistral, and most decoder-only LLMs. Simple, scales "
        "well, and naturally enables generation at inference.",
        "Masked language modeling (MLM). Mask a fraction of tokens (15% in BERT) and "
        "predict them from bidirectional context. Used in BERT, RoBERTa, DeBERTa.",
        "Span corruption. Mask contiguous spans of tokens and predict them. Used in T5 and "
        "UL2. Generalizes MLM to longer spans.",
        "Prefix language modeling. Bidirectional attention on a prefix, causal attention "
        "on a suffix. Used in some encoder-decoder models.",
        "Contrastive objectives. SimCSE, sentence-transformers: pull positive pairs "
        "together, push negatives apart. Used to learn sentence embeddings.",
        "Replaced token detection. ELECTRA: a small generator proposes replacements; the "
        "main model classifies which tokens were replaced. More sample-efficient than MLM.",
     ]),

    ("Why is multi-head attention needed?",
     [
        "Single-head attention forces the model to mix all kinds of relationships into one "
        "set of weights. Multi-head attention lets the model attend to different aspects in "
        "parallel: one head might track syntactic dependencies, another semantic "
        "co-reference, another local n-gram patterns.",
        "Mechanics: split the model dimension d into h heads of dimension d/h each. Run "
        "attention independently in each head with its own Q, K, V projections. Concatenate "
        "the h outputs and apply a final linear projection.",
        "Cost is the same as single-head with full dimension (the per-head dimension is "
        "smaller), so multi-head gives you specialization for free. Typical h is 8, 16, or "
        "32. Modern LLMs sometimes use grouped-query attention (GQA) or multi-query "
        "attention (MQA) where Q heads outnumber K/V heads, trading a small quality drop for "
        "much faster inference.",
     ]),

    ("What is RLHF, and how is it used?",
     [
        "Reinforcement Learning from Human Feedback (RLHF) is the standard alignment "
        "pipeline for instruction-following LLMs. It has three stages.",
        "Stage 1: Supervised Fine-Tuning (SFT). Fine-tune the base LLM on a curated set of "
        "(prompt, ideal response) pairs written by humans. The model learns to follow "
        "instructions.",
        "Stage 2: Reward Model (RM). For each prompt, generate multiple responses and have "
        "humans rank them. Train a separate model to predict the human preference: "
        "RM(prompt, response) → scalar. The reward model encodes 'what humans prefer'.",
        "Stage 3: Policy optimization. Use the reward model as the reward signal to fine-"
        "tune the SFT model with reinforcement learning, typically PPO. Add a KL penalty "
        "against the SFT model to prevent the policy from drifting into reward-hacking "
        "regions. Modern variants: DPO (skips the explicit reward model and trains directly "
        "on preference pairs), GRPO (group-relative advantage, drops the value head), RLAIF "
        "(AI-generated preferences).",
     ],
     ["16_rlhf.png"]),

    ("What is catastrophic forgetting in LLMs?",
     [
        "Catastrophic forgetting is when a neural network, fine-tuned on a new task or "
        "domain, loses its performance on tasks it previously knew. Weights that encoded "
        "old knowledge get overwritten by gradients from the new task.",
        "In LLMs: aggressive fine-tuning on a narrow domain can degrade general reasoning, "
        "instruction-following, or safety behavior. The model becomes 'good at the new "
        "task, worse at everything else.'",
        "Mitigations: use parameter-efficient fine-tuning (LoRA, adapters) so the base "
        "weights are frozen. Mix the new data with a sample of original-distribution data "
        "(replay or rehearsal). Apply Elastic Weight Consolidation or similar regularizers "
        "that penalize large changes to weights deemed important for old tasks. Use lower "
        "learning rates. Evaluate on a regression suite covering base capabilities after "
        "any fine-tuning run.",
     ]),

    ("In a transformer seq2seq model, what do the encoder and decoder do, and how does information flow?",
     [
        "Encoder: a stack of transformer encoder layers that processes the entire input "
        "sequence with bidirectional self-attention. Its output is a sequence of contextual "
        "representations (one per input token).",
        "Decoder: a stack of decoder layers that generates the output sequence one token at "
        "a time. Each decoder layer has three sub-layers: (1) masked self-attention over the "
        "already-generated output tokens, (2) cross-attention where Q comes from the decoder "
        "and K, V come from the encoder outputs, (3) feed-forward.",
        "Information flow during training: the entire target sequence is shifted by one "
        "position and fed into the decoder. Cross-attention lets the decoder peek at the "
        "encoder representations. The loss is teacher-forced cross-entropy on the predicted "
        "tokens.",
        "Information flow during inference: feed the start token. Run the decoder. Sample "
        "or argmax the next token. Append. Repeat. Each step costs O(n²) for fresh decoding "
        "or O(n) with KV-cache reuse. Inference is autoregressive and sequential.",
     ],
     ["20_encoder_decoder.png"]),

    ("Why is positional encoding crucial?",
     [
        "Self-attention treats its input as a set, not a sequence. Without positional "
        "information, the model cannot distinguish 'dog bites man' from 'man bites dog'.",
        "Sinusoidal positional encoding (original transformer): add fixed sin/cos functions "
        "of position to the input embeddings. Different frequencies per dimension. "
        "Generalizes (in theory) to unseen positions.",
        "Learned positional encoding (BERT, GPT-2): treat each position as a learnable "
        "embedding. Simple, works well within trained range, does not extrapolate.",
        "Rotary Position Embedding (RoPE, LLaMA): rotate Q and K vectors by an angle "
        "proportional to position. Encodes relative position naturally in the dot product. "
        "Extrapolates better than absolute. ALiBi adds a position-dependent bias to "
        "attention scores; very strong extrapolation.",
     ]),

    ("When fine-tuning a pretrained transformer for a domain-specific NLP task, what strategies ensure effective knowledge transfer?",
     [
        "Data: collect a high-quality target dataset. Quality beats quantity. Deduplicate, "
        "filter for relevance, balance classes or topics if applicable. Domain-mixed "
        "training data (some target, some general) reduces catastrophic forgetting.",
        "Method: prefer PEFT (LoRA, qLoRA) for cost and to avoid catastrophic forgetting. "
        "Full fine-tuning when you have abundant target data and need maximum quality. "
        "Continued pretraining (a brief pass of LM objective on domain text) before fine-"
        "tuning helps when the domain vocabulary diverges from general.",
        "Hyperparameters: use a small learning rate (1e-5 to 5e-5 for full FT; 1e-4 to 3e-4 "
        "for LoRA). Use warm-up. Use weight decay. Monitor validation loss every few hundred "
        "steps and apply early stopping.",
        "Evaluation: hold out a representative test set. Include a regression suite for "
        "base capabilities so you can detect catastrophic forgetting early.",
     ]),

    ("What is cross-attention in encoder-decoder transformers?",
     [
        "Cross-attention is the mechanism that lets the decoder consult the encoder output "
        "when generating each output token. In a decoder layer, after masked self-attention "
        "over generated tokens, cross-attention takes Q from the decoder's current "
        "representation and K, V from the encoder outputs.",
        "Each decoder position emits an attention weight over all encoder positions and "
        "produces a context vector. This is how an English-to-French translator decides "
        "which French word to emit based on which English words are relevant at this "
        "decoding step.",
        "Cross-attention is also central to multimodal transformers. In Flamingo, BLIP-2, "
        "and similar, cross-attention lets the language decoder attend to image features. "
        "In DALL-E 2 / Stable Diffusion, the U-Net cross-attends to the text encoder's "
        "outputs to condition image generation on the prompt.",
     ]),

    ("Compare sparse (cross-entropy) vs dense (MSE) loss functions in training language models.",
     [
        "Cross-entropy is the standard loss for next-token prediction. It treats each token "
        "as a classification target over the vocabulary and penalizes the model based on "
        "the probability assigned to the correct token. Cross-entropy is well-matched to "
        "the categorical nature of language: a token is or is not the correct token.",
        "Mean Squared Error treats the prediction as a vector in continuous space. It is "
        "appropriate for regression but is wrong for token prediction because tokens are "
        "categorical. Using MSE on token IDs is mathematically nonsensical (token 5 is not "
        "'closer' to token 6 than token 100).",
        "Where MSE-like losses appear in language modeling: distillation (match the student's "
        "logits to the teacher's via KL or MSE on logits), representation learning (match "
        "embeddings), and consistency objectives. For token prediction itself, cross-entropy "
        "is the right choice.",
     ]),

    ("How can reinforcement learning be integrated into LLM training, and what challenges arise in loss design?",
     [
        "RL is integrated through RLHF (with a reward model) or RLVR (with a programmatic "
        "verifier). The LLM is treated as a policy: the prompt is the initial state, each "
        "generated token is an action, the final sequence receives a reward.",
        "Algorithms: PPO with a value head and KL penalty against a reference model. DPO "
        "skips the explicit reward model and trains directly on preference pairs via a "
        "closed-form objective. GRPO drops the value head and uses group-relative advantage.",
        "Challenges in loss design: (1) reward hacking when the reward model has exploitable "
        "patterns. (2) Sparse, delayed rewards make credit assignment hard. (3) KL penalty "
        "weight must balance task performance against staying close to the SFT policy. "
        "(4) Off-policy correction: rolling out from a slightly stale policy introduces "
        "bias unless corrected with importance sampling. (5) Variance reduction: advantage "
        "estimation has high variance, hurting sample efficiency.",
     ],
     ["16_rlhf.png"]),

    ("How is information from visual and textual modalities integrated in multimodal LLMs?",
     [
        "Three common patterns. (1) Shared embedding space (CLIP): train a vision encoder "
        "and a text encoder jointly with contrastive loss on image-caption pairs. The "
        "resulting embeddings live in the same space and support cross-modal retrieval and "
        "zero-shot classification.",
        "(2) Cross-attention bridges (Flamingo, BLIP-2): a small bridge module (Perceiver "
        "Resampler or Q-Former) projects visual features into the language model's space "
        "and lets the LM cross-attend to them. The base LM stays frozen.",
        "(3) Direct token projection (LLaVA, GPT-4V style): a vision encoder produces "
        "patch tokens; a linear or MLP projection maps each visual token into the LM's "
        "token embedding space; the LM processes a mixed sequence of visual and text "
        "tokens uniformly via self-attention.",
        "For tasks like image captioning, the decoder generates caption tokens conditioned "
        "on the visual representation. For VQA, the question is fed as text tokens and the "
        "answer is generated conditioned on both the question and the image.",
     ]),

    ("What is the role of cross-modal attention in models like VisualBERT and CLIP?",
     [
        "Cross-modal attention lets one modality query another. In VisualBERT, image region "
        "features and text tokens are concatenated into one sequence and processed by a "
        "transformer with full self-attention. Text tokens can attend to image regions and "
        "vice versa, learning joint representations.",
        "CLIP's setup is different: separate text and image encoders, no cross-attention "
        "between them. Alignment comes from the contrastive objective during training: "
        "image and text embeddings of a matching pair are pulled together; mismatched pairs "
        "are pushed apart. The geometry of the joint space encodes the cross-modal "
        "relationship.",
        "Cross-attention is essential where direct token-level interaction matters (caption "
        "generation, VQA, grounded reasoning). Contrastive joint spaces excel at retrieval, "
        "search, and zero-shot classification where you need cheap, dense comparison.",
     ]),

    ("How is training data annotated for image-text matching, and what considerations matter?",
     [
        "Annotation styles: aligned captions (each image has one or more descriptive "
        "captions, like COCO Captions); product image-title pairs from e-commerce; "
        "scraped alt-text from the web (LAION, used in CLIP and Stable Diffusion); "
        "click-through pairs (a user searched X, clicked image Y).",
        "Considerations: alignment quality (a noisy caption hurts contrastive training); "
        "scale (hundreds of millions of pairs typical for foundation models); diversity "
        "(domain coverage matters more than raw count); bias (web-scraped data reflects web "
        "biases including stereotypes); copyright and licensing (LAION-5B has documented "
        "issues); deduplication (near-duplicates inflate eval metrics if they leak).",
        "Hard negative mining helps when easy negatives dominate: pick negatives that look "
        "similar to the positive but are wrong, so the model learns finer distinctions.",
     ]),

    ("When training a generative model for image synthesis, what loss functions are used?",
     [
        "GANs: adversarial loss. The generator tries to fool a discriminator; the "
        "discriminator tries to distinguish real from generated. Pure adversarial loss is "
        "notoriously unstable; modern GANs add feature matching, gradient penalty, and "
        "spectral normalization.",
        "VAEs: a reconstruction loss (pixel-wise MSE or BCE) plus a KL divergence term "
        "regularizing the latent distribution toward a prior.",
        "Diffusion models: predict the noise added to a clean image at random timesteps, "
        "minimizing MSE between predicted and actual noise. Simple and stable. Modern "
        "extensions: latent diffusion (train in a compressed latent space), classifier-free "
        "guidance, v-prediction, EDM parameterization.",
        "Perceptual losses: compare features extracted by a pretrained network (VGG, "
        "LPIPS) rather than raw pixels. Better correlated with human judgment.",
     ]),

    ("What is perceptual loss, and how does it differ from pixel-wise loss?",
     [
        "Perceptual loss measures the distance between generated and target images in a "
        "deep feature space (typically intermediate layers of a pretrained VGG or LPIPS "
        "network) rather than pixel-by-pixel. Two images can be perceptually similar "
        "(same content, slight color shift) but have high pixel-wise distance; perceptual "
        "loss is much closer to human judgment.",
        "Pixel-wise losses (L1, L2): treat each pixel independently. Penalize even tiny "
        "shifts and color changes that humans do not notice. Lead to blurry outputs in "
        "generation because the optimal solution under L2 is the mean of plausible outputs.",
        "Perceptual loss: feeds both images through a frozen feature extractor and "
        "compares activations. Captures texture, structure, and semantic content. Used in "
        "super-resolution (ESRGAN), style transfer, image-to-image translation. Often "
        "combined with adversarial loss for sharper outputs.",
     ]),

    ("What is masked language-image modeling?",
     [
        "Masked language-image modeling is a multimodal self-supervised objective: mask "
        "tokens from both modalities and reconstruct them from joint context. Used by "
        "models like VisualBERT, ViLBERT, MaskGIT, and BEiT-3.",
        "Setup: take an image and its caption. Tokenize the image (into patches or VQ-VAE "
        "tokens) and the text. Concatenate. Mask some image tokens and some text tokens. "
        "Train the model to predict the masked tokens given the remaining ones.",
        "Why it helps: the model learns cross-modal grounding. Predicting a masked image "
        "patch may require reading the caption; predicting a masked word may require "
        "looking at the image. The shared representation encodes the relationship between "
        "modalities.",
     ]),

    ("How do cross-attention weights influence generation in multimodal models?",
     [
        "In a multimodal generator with cross-attention (Flamingo, BLIP-2, Stable "
        "Diffusion's U-Net), cross-attention weights determine how much each modality "
        "contributes to each generation step.",
        "Concretely: at each generation step, the decoder forms a query and attends to keys "
        "from the conditioning modality (image features for text generation, or text "
        "encoder outputs for image generation). High attention weight on a particular "
        "image patch means that patch is strongly influencing the next token.",
        "Practical implications: classifier-free guidance scales these weights to amplify "
        "the conditioning signal. Inspecting cross-attention maps explains where the model "
        "is looking. In diffusion models, attention manipulation enables compositional "
        "control (e.g. attention slicing for prompt editing).",
     ]),

    ("What are unique challenges in training multimodal generative models?",
     [
        "Data alignment: multimodal training requires aligned pairs across modalities, "
        "which are expensive to curate. Noisy alignment hurts training. Misalignment in "
        "one direction (e.g. captions that don't describe images) is hard to detect.",
        "Modality imbalance: text data is far more abundant than aligned image-text pairs. "
        "Models may overfit to language patterns and underuse visual signals.",
        "Optimization: different modalities have different gradient dynamics. Naive joint "
        "training can let one modality dominate. Techniques: modality-specific learning "
        "rates, gradient balancing, separate warm-up schedules.",
        "Evaluation: there is no single perplexity-like metric. Image generation needs FID, "
        "CLIP-score, human evaluation. Captioning needs BLEU, CIDEr, plus human eval. VQA "
        "needs exact match and human judgment. Cross-modal retrieval needs Recall@k.",
        "Compute: training a state-of-the-art multimodal model takes thousands of GPU-"
        "years, vastly more than unimodal models of similar parameter count.",
     ]),

    ("How do multimodal generative models address data sparsity?",
     [
        "Leverage abundant unimodal data: pretrain text and image encoders separately on "
        "unimodal corpora (BERT for text, ViT for images), then align with a smaller "
        "supervised paired dataset.",
        "Web scraping at scale: LAION-5B, COYO-700M and similar collect billions of "
        "image-text pairs from the web. Noisy but large.",
        "Synthetic data: use one model to generate training data for another. Image "
        "captioning models can generate captions for un-captioned images; text-to-image "
        "models can generate images from textual prompts. Risk of compounding errors.",
        "Cross-modal contrastive objectives (CLIP-style): align modalities with minimal "
        "supervision (just paired examples, no per-pair labels). Scales to billions of "
        "pairs.",
        "Self-distillation and pseudo-labeling: train a model, use it to label new data, "
        "retrain.",
     ]),

    ("Explain Vision-Language Pretraining (VLP) and its significance.",
     [
        "VLP is the practice of pretraining a single model jointly on visual and textual "
        "data so that downstream vision-language tasks can be solved by light fine-tuning "
        "or zero-shot prompting. It is the multimodal analog of BERT pretraining.",
        "Pretraining objectives mix image-text matching, masked language modeling "
        "conditioned on images, masked image modeling conditioned on text, and contrastive "
        "image-text alignment.",
        "Significance: a well-pretrained VLP model transfers to image captioning, visual "
        "question answering, image-text retrieval, visual reasoning, and image generation "
        "with minimal task-specific work. CLIP enabled zero-shot image classification at "
        "ImageNet quality. Flamingo and BLIP-2 enabled few-shot VQA. GPT-4V and Gemini have "
        "taken this further into multimodal reasoning over images, charts, and documents.",
     ]),

    ("How do CLIP and DALL-E integrate vision and language?",
     [
        "CLIP (Contrastive Language-Image Pretraining): trains a vision encoder and a text "
        "encoder jointly with contrastive loss on 400M image-caption pairs. Outputs live in "
        "a shared embedding space. Use cases: zero-shot image classification (encode candidate "
        "labels as text, embed image, take argmax similarity), image-text retrieval, content "
        "moderation, dataset filtering.",
        "DALL-E: text-to-image generation. The original DALL-E used a discrete VAE plus an "
        "autoregressive transformer over image tokens conditioned on text. DALL-E 2 and 3 "
        "replaced this with diffusion models: a CLIP text encoder conditions a diffusion "
        "decoder that generates the image. Stable Diffusion is the open-source "
        "exemplar of the same pattern.",
        "Integration pattern: text provides the conditioning signal; the image generator "
        "(autoregressive or diffusion) attends to text embeddings at every generation step "
        "via cross-attention, producing images that follow the prompt.",
     ]),

    ("How do attention mechanisms enhance vision-language models?",
     [
        "Cross-modal grounding: attention lets the model focus on specific image regions "
        "when generating text about them, and on specific words when interpreting an "
        "image. This grounding is what enables answers like 'the red car on the left' to "
        "actually correspond to the red car on the left.",
        "Compositional reasoning: attention over image regions plus attention over text "
        "tokens lets the model reason about combinations ('the man with the umbrella next "
        "to the woman in red'). Without attention, the model collapses everything into a "
        "single vector and loses compositionality.",
        "Interpretability: attention maps over an image show which regions drove a given "
        "output token, which is useful for debugging and explanation.",
        "Generation control: techniques like attention manipulation, classifier-free "
        "guidance scaling, and prompt-based attention editing rely on attention as the "
        "control surface for steering generation.",
     ]),
]
