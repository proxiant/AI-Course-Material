"""
Content for Part 1: ANN, Classical NLP, Transformers, LLM fundamentals.
Each entry: (question, [answer_paragraphs], [optional diagram filenames]).
Style follows CLAUDE.md: plain prose, no em dashes, no AI cliches.
"""

# ============================ ANN ============================
ANN = [
    ("What is an Artificial Neural Network, and how does it work?",
     [
        "An Artificial Neural Network (ANN) is a computational model loosely inspired by "
        "biological neurons. It is a directed graph of simple units called neurons arranged "
        "in layers: an input layer that receives features, one or more hidden layers that "
        "transform them, and an output layer that produces a prediction.",
        "Each neuron computes a weighted sum of its inputs plus a bias term, then applies "
        "a non-linear activation function: a = f(w·x + b). Stacked layers let the network "
        "build up progressively more abstract representations of the input. The training "
        "process adjusts the weights and biases so that the output matches the target on "
        "a training set, using gradient descent driven by backpropagation.",
        "The universal approximation theorem says a sufficiently wide single-hidden-layer "
        "network with a non-linear activation can approximate any continuous function on "
        "a compact set. In practice, depth is what gives modern networks their power: each "
        "layer composes simpler features into more abstract ones, and depth is far more "
        "parameter-efficient than width for the same expressive capacity.",
     ],
     ["01_ann_architecture.png"]),

    ("What are activation functions, what types exist, and why are they used in neural networks?",
     [
        "An activation function is a non-linear transformation applied to the weighted sum "
        "computed by a neuron. Without non-linear activations, a stack of layers would "
        "collapse into a single linear transformation, no matter how many layers were used. "
        "Non-linearity is what gives neural networks the capacity to model complex patterns.",
        "Common activation functions: Sigmoid σ(x) = 1/(1+exp(-x)), bounded to (0, 1), "
        "historically used for binary outputs but suffers from saturation and vanishing "
        "gradients. Tanh, bounded to (-1, 1), zero-centered, better than sigmoid for hidden "
        "layers but still saturates. ReLU max(0, x) is the modern default for hidden layers: "
        "cheap, no saturation in the positive region, sparse activations. Leaky ReLU is ReLU "
        "with a small slope for negative inputs to avoid dead neurons. GELU and SiLU (Swish) "
        "are smoother variants used in transformers. Softmax normalizes a vector into a "
        "probability distribution over classes for the final layer of a classifier.",
        "Choice guidance: ReLU or GELU for hidden layers, sigmoid for binary output, softmax "
        "for multiclass output. Tanh sees use in RNNs and certain attention components.",
     ],
     ["02_neuron.png", "03_activations.png"]),

    ("What is backpropagation, and how does it work in training neural networks?",
     [
        "Backpropagation is the algorithm for efficiently computing the gradient of a loss "
        "function with respect to every weight in a neural network. It is the chain rule of "
        "calculus applied systematically from the output back to the inputs.",
        "The process has two passes. The forward pass computes the output of every layer "
        "given the input and stores intermediate activations. The backward pass starts from "
        "the loss at the output and propagates gradient information back layer by layer, "
        "computing ∂L/∂w for every weight by combining the upstream gradient with the local "
        "derivative at that layer.",
        "These per-weight gradients are then used by an optimizer (SGD, Adam, etc.) to update "
        "the weights in the direction that reduces the loss. Modern deep learning frameworks "
        "(PyTorch, TensorFlow) compute backpropagation automatically via a computational graph "
        "and reverse-mode automatic differentiation, so you almost never write the backward "
        "step yourself. The cost of backpropagation is roughly the same as the forward pass, "
        "which is what makes training deep networks tractable.",
     ],
     ["04_backprop.png"]),

    ("What is the vanishing and exploding gradient problem, and how does it affect training?",
     [
        "When backpropagation multiplies gradients through many layers, those products can "
        "shrink to near zero (vanishing) or blow up to very large values (exploding). With "
        "vanishing gradients, the lower layers learn extremely slowly because the update "
        "signal that reaches them is too small. With exploding gradients, weights oscillate "
        "or diverge, and training becomes unstable.",
        "Vanishing is common with saturating activations like sigmoid or tanh in deep "
        "networks: their derivative is less than 1, and the product of many small numbers "
        "approaches zero. Exploding is common in RNNs unrolled over many timesteps with "
        "weight matrices whose largest singular value exceeds one.",
        "Mitigations: use ReLU-family activations (derivative is 1 on the active side), "
        "use careful weight initialization (Xavier/Glorot for tanh-like, He for ReLU), "
        "use batch normalization or layer normalization, use residual connections (let "
        "gradients flow through identity paths), use gradient clipping (for explosion in "
        "RNNs), and use architectures such as LSTM/GRU and transformers that are designed "
        "to keep gradient norms healthy across long sequences.",
     ],
     ["05_vanishing_gradient.png"]),

    ("How do you prevent overfitting in neural networks?",
     [
        "Overfitting happens when a model fits the training set so precisely that it loses "
        "the ability to generalize to new data. The training loss keeps falling while the "
        "validation loss starts rising. The signs are easy to read; the fixes come in several "
        "complementary families.",
        "Data-side fixes: collect more training data; apply data augmentation (random crops, "
        "flips, noise for images; back-translation and synonym replacement for text); "
        "use cross-validation to get a more honest estimate of generalization.",
        "Model-side fixes: reduce model capacity (fewer layers, narrower layers); use weight "
        "regularization (L1 or L2 penalty on weights); apply dropout, which randomly zeros "
        "activations during training; use batch normalization or layer normalization to keep "
        "activations well-behaved; use early stopping based on validation loss.",
        "Training-side fixes: use a held-out validation set and stop training when validation "
        "loss starts rising; ensemble multiple models; transfer learning from a pretrained "
        "model when the target dataset is small.",
     ],
     ["17_overfitting.png", "18_dropout.png"]),

    ("What is dropout, and how does it help train neural networks?",
     [
        "Dropout is a regularization technique where, during training, each neuron is "
        "independently dropped (its output set to zero) with some probability p (typically "
        "0.2 to 0.5). At test time all neurons are active and their outputs are scaled by "
        "(1 - p) to compensate for the larger sum (inverted dropout scales during training "
        "instead, leaving inference cleaner).",
        "Why it helps: dropout prevents neurons from co-adapting too strongly. Each neuron "
        "must produce useful features regardless of which other neurons happen to be present "
        "in any given batch. The effect is roughly equivalent to training a large ensemble "
        "of subnetworks and averaging them at inference.",
        "Practical notes: apply dropout after fully connected and certain convolutional "
        "layers; do not apply between batch norm and the next layer (the two regularizers "
        "interact badly); typical p is 0.5 for fully connected, 0.1 to 0.3 for convolutional "
        "and transformer blocks; modern transformer models use dropout sparingly and rely "
        "more on data scale and weight decay.",
     ]),

    ("How do you choose the number of layers and neurons for a neural network?",
     [
        "There is no closed-form answer; the choice is empirical and constrained by the "
        "task, data size, and compute budget. The practical approach is to start small, "
        "establish a working baseline, then scale up while watching the validation loss.",
        "Heuristics that work: for tabular data, two to four hidden layers with widths in "
        "the range 64 to 512 is a reasonable starting point. For images, use a published "
        "backbone (ResNet, EfficientNet, ViT) rather than designing from scratch. For text, "
        "use a published transformer with a known parameter count for your model size class.",
        "Scaling: if the model underfits (train loss is high), add capacity. If it overfits "
        "(train loss low, val loss high), reduce capacity or add regularization. Use the "
        "validation curve as the signal. Architecture search and hyperparameter sweeps "
        "(Optuna, Ray Tune) can automate the search when the cost is justified.",
        "Chinchilla scaling for large language models: parameter count and training tokens "
        "should scale together at roughly 20 tokens per parameter for compute-optimal "
        "training.",
     ]),

    ("What is transfer learning, and when is it useful?",
     [
        "Transfer learning is the practice of reusing knowledge from a model trained on one "
        "task or dataset to improve performance on a related task. In modern deep learning "
        "this almost always means: take a model pretrained on a large general corpus, freeze "
        "or fine-tune part of it on your specific task.",
        "It is useful when: (a) your target dataset is small, (b) the source task is related "
        "enough that low-level features transfer, (c) you cannot afford to train from "
        "scratch. Image classifiers fine-tune from ImageNet-pretrained backbones. NLP tasks "
        "fine-tune from BERT, RoBERTa, or instruction-tuned LLMs. Domain adaptation for "
        "medical imaging starts from a general-purpose vision backbone.",
        "Typical workflow: load the pretrained model, replace the final task-specific head, "
        "optionally freeze early layers, train the new head and (optionally) the rest of the "
        "model with a small learning rate. PEFT methods like LoRA take this further by "
        "training only a tiny low-rank update on top of frozen weights.",
     ]),

    ("What is a loss function, and how do you choose the right one?",
     [
        "A loss function is a scalar that measures how wrong a model's predictions are on a "
        "training example or batch. It is what the optimizer minimizes. The choice of loss "
        "is driven by the task type and the distribution you assume over your data.",
        "Common choices: Mean Squared Error (MSE) for regression with Gaussian noise. "
        "Mean Absolute Error (MAE) for regression robust to outliers. Huber loss combines "
        "the two. Binary cross-entropy for binary classification. Categorical cross-entropy "
        "for multiclass classification. Negative log-likelihood (NLL) is the same as cross-"
        "entropy in most cases. Hinge loss for SVM-style classifiers. CTC loss for sequence "
        "alignment without explicit alignment labels. Triplet loss and InfoNCE for embedding "
        "learning. KL divergence for distributional matching.",
        "Choose by asking three questions: what does my model output (a number, a class, a "
        "distribution, an embedding)? What is the noise model in my data? What do I actually "
        "want to optimize at deployment? Aligning the loss with the deployment metric is "
        "more important than picking the fanciest loss.",
     ]),

    ("Explain gradient descent and its variations: SGD and mini-batch gradient descent.",
     [
        "Gradient descent is an iterative optimization algorithm that updates parameters in "
        "the direction opposite the gradient of the loss. The update rule is "
        "θ ← θ - η · ∇L(θ), where η is the learning rate.",
        "Batch gradient descent uses the gradient computed on the entire training set per "
        "step. Smooth convergence, but each step is expensive and the entire set must fit "
        "in memory. Stochastic gradient descent (SGD) uses one example per step. Cheap and "
        "noisy; the noise can help escape sharp minima but slows final convergence. "
        "Mini-batch gradient descent is the practical compromise: compute the gradient on "
        "a small batch (32 to 4096 examples) per step. GPU-friendly and noise-controlled.",
        "Modern optimizers add adaptive learning rates and momentum: SGD with momentum, "
        "RMSProp, Adam, AdamW. Adam combines momentum with per-parameter adaptive learning "
        "rates and is the default for most deep learning workloads. AdamW decouples weight "
        "decay from the gradient update and is the better choice when regularization matters.",
     ],
     ["06_gradient_descent.png"]),

    ("What is the role of the learning rate, and how do you tune it?",
     [
        "The learning rate η controls how large a step the optimizer takes in the direction "
        "opposite the gradient. Too small and training is needlessly slow; too large and "
        "the loss diverges or oscillates without converging.",
        "Practical strategies: start with the standard default for your optimizer (e.g. 3e-4 "
        "for Adam on most tasks, 1e-5 to 5e-5 for fine-tuning transformers). Use a learning "
        "rate range test (Smith): linearly increase η from very small to very large over a "
        "few hundred steps and plot loss; pick η around the steepest descent point. Use a "
        "schedule: warm-up (linearly increase η for the first few hundred steps), then decay "
        "(cosine, polynomial, or step). One-cycle learning rate works well for many tasks.",
        "Symptoms of bad learning rates: loss is constant or jumps up immediately (too "
        "high); loss decreases extremely slowly (too low); loss oscillates after initial "
        "progress (could be too high, or batch size too small).",
     ]),

    ("What are common neural network architectures, and when do you use each?",
     [
        "Multilayer Perceptron (MLP) / Feedforward: tabular data, small models, classical "
        "regression and classification.",
        "Convolutional Neural Network (CNN): image classification, detection, segmentation. "
        "Examples: ResNet, EfficientNet, ConvNeXt.",
        "Recurrent Neural Network (RNN), LSTM, GRU: sequence modeling when transformers are "
        "too expensive or context is short. Largely superseded by transformers for NLP.",
        "Transformer: text, audio, vision, multimodal. BERT, GPT, T5, LLaMA, ViT, CLIP. "
        "The default for modern NLP and increasingly for vision.",
        "Graph Neural Network (GNN): graph-structured data (molecules, social networks, "
        "knowledge graphs). GraphSAGE, GAT, GIN.",
        "Autoencoder, Variational Autoencoder (VAE): unsupervised representation learning, "
        "anomaly detection, generation.",
        "Generative Adversarial Network (GAN): image synthesis, super-resolution. Largely "
        "displaced by diffusion models for high-quality image generation.",
        "Diffusion model: image, audio, and video generation. Stable Diffusion, DALL-E 3.",
        "Mixture of Experts (MoE): scaling LLMs by activating only a subset of parameters "
        "per token. Mixtral, Switch Transformer.",
     ]),

    ("What is a CNN, and how does it differ from a feedforward ANN?",
     [
        "A Convolutional Neural Network (CNN) is built around two ideas: local receptive "
        "fields (each neuron sees only a small spatial neighborhood) and weight sharing "
        "(the same filter is applied at every spatial position). These ideas encode the "
        "prior that local pixel patterns matter and translation invariance should hold.",
        "A CNN has three kinds of layers: convolutional layers (apply learned filters), "
        "pooling layers (downsample spatially), and fully connected layers (final "
        "classification head). A typical pipeline alternates conv and pool layers to build "
        "spatial hierarchy, then flattens and runs a few fully connected layers.",
        "Differences from a plain MLP: an MLP would treat each pixel as an independent "
        "feature, ignoring spatial structure, and would need vastly more parameters. A CNN's "
        "weight sharing makes it parameter-efficient and translation-equivariant. Modern "
        "vision is dominated by CNNs and Vision Transformers, with ViTs winning at scale.",
     ],
     ["07_cnn.png"]),

    ("How does an RNN work, and what are its limitations?",
     [
        "A Recurrent Neural Network processes a sequence one element at a time, maintaining "
        "a hidden state that summarizes everything seen so far. At each step t: "
        "h_t = f(W_h · h_{t-1} + W_x · x_t + b), and the output y_t comes from h_t.",
        "Variants: LSTM (Long Short-Term Memory) adds gates (input, forget, output) and a "
        "cell state to better preserve long-range dependencies. GRU (Gated Recurrent Unit) "
        "is a simpler version with two gates.",
        "Limitations: training is inherently sequential (cannot parallelize over the time "
        "axis), which makes RNNs slow on long sequences. Gradients vanish or explode over "
        "long unrolls. The hidden state has fixed capacity, so very long contexts get "
        "compressed lossily. These limitations are exactly why transformers won the NLP "
        "race: transformers parallelize over tokens via attention, avoid sequential "
        "bottleneck, and handle long-range dependencies more directly.",
     ],
     ["08_rnn.png"]),

    # BONUS Q
    ("What are batch normalization and layer normalization, and when do you use each?",
     [
        "Both normalize activations to stabilize training, but along different axes. Batch "
        "normalization (BatchNorm) normalizes each feature across the batch dimension. "
        "Layer normalization (LayerNorm) normalizes each example across the feature "
        "dimension.",
        "BatchNorm works well for CNNs and large batches but is sensitive to batch size and "
        "awkward for RNNs and variable-length sequences. LayerNorm has no batch dependence "
        "and is the default in transformers. RMSNorm is a recent simplification that drops "
        "the mean-centering and is used in LLaMA and similar models.",
        "Benefits: faster convergence, allows higher learning rates, mild regularization "
        "effect, reduced sensitivity to initialization.",
     ]),
]

# ============================ Classical NLP ============================
CLASSICAL_NLP = [
    ("What is tokenization? Give the difference between lemmatization and stemming.",
     [
        "Tokenization is the process of splitting raw text into discrete units called "
        "tokens. The units may be words, subwords, characters, or sentences. Modern LLMs "
        "use subword tokenization (BPE, WordPiece, SentencePiece) to balance vocabulary "
        "size with the ability to represent rare and out-of-vocabulary words.",
        "Stemming chops off suffixes to reduce a word to its root form using rule-based "
        "heuristics. 'Running' → 'run', 'studies' → 'studi'. Fast but produces non-words.",
        "Lemmatization reduces a word to its dictionary form (lemma) using a vocabulary and "
        "morphological analysis. 'Better' → 'good', 'ran' → 'run'. Slower but produces real "
        "words and respects part of speech.",
        "Modern NLP with subword tokenizers and large pretrained models rarely needs "
        "stemming or lemmatization explicitly; the tokenizer handles surface variation "
        "implicitly through shared subword units.",
     ],
     ["19_tokenization.png"]),

    ("Explain Bag of Words (BoW) and its limitations.",
     [
        "Bag of Words represents a document as a vector of word counts, ignoring word "
        "order. The vocabulary is the union of words across the corpus; each document "
        "becomes a sparse vector where the i-th entry is the count of vocabulary word i.",
        "Limitations: BoW loses all word order ('dog bites man' vs 'man bites dog' have "
        "identical representations). It cannot capture meaning: synonyms get separate "
        "dimensions, polysemous words collapse. The vocabulary grows with the corpus, "
        "producing very high-dimensional sparse vectors. It cannot handle out-of-vocabulary "
        "words at test time.",
        "Mitigations: n-grams capture limited local order; TF-IDF reweights rare words; "
        "hashing tricks bound the vocabulary size. The real fix is dense embeddings and "
        "neural models, which BoW preceded.",
     ]),

    ("How does TF-IDF work, and how is it different from simple word frequency?",
     [
        "TF-IDF stands for Term Frequency × Inverse Document Frequency. It is a weighting "
        "scheme that gives higher scores to words that are frequent in a document but rare "
        "across the corpus.",
        "TF(t, d) = count of term t in document d (often normalized by document length). "
        "IDF(t) = log(N / df(t)) where N is total documents and df(t) is the number of "
        "documents containing t. TF-IDF(t, d) = TF × IDF.",
        "Difference from raw frequency: raw frequency lets common words ('the', 'is') "
        "dominate. TF-IDF down-weights them via IDF, so a word that appears 10 times in "
        "one document but in every document scores low. A word that appears 5 times in one "
        "document and almost nowhere else scores high. TF-IDF is still used as a strong "
        "baseline retriever (BM25 is its more refined cousin).",
     ]),

    ("What is word embedding, and why is it useful in NLP?",
     [
        "A word embedding is a dense, low-dimensional vector representation of a word "
        "(typically 50 to 1024 dimensions) where the geometric relationships approximate "
        "semantic ones. Cosine similarity captures meaning similarity; vector arithmetic "
        "can capture analogies (king - man + woman ≈ queen).",
        "Useful because: it replaces sparse one-hot vectors with dense vectors that share "
        "information across related words; it provides a strong initialization for "
        "downstream models; it enables similarity search, clustering, and retrieval; it "
        "makes models robust to out-of-vocabulary variation when using subword embeddings.",
        "Methods: Word2Vec (CBOW and Skip-Gram), GloVe (global co-occurrence factorization), "
        "FastText (subword-aware), and contextual embeddings from BERT or modern LLMs. "
        "Contextual embeddings are the modern default since the same word can have different "
        "embeddings in different contexts.",
     ],
     ["15_embeddings.png"]),

    ("What are some common real-world applications of NLP?",
     [
        "Search and information retrieval. Question answering and assistants. Translation. "
        "Text summarization. Sentiment analysis and opinion mining. Named entity recognition "
        "for extracting people, places, organizations from text. Chatbots and conversational "
        "agents. Document classification (spam, topic, intent). Speech recognition and "
        "text-to-speech. Text generation (writing assistance, code completion, marketing "
        "copy). Compliance and content moderation. Legal contract analysis. Clinical note "
        "summarization in healthcare. Automated grading and feedback in education. Code "
        "search and program synthesis.",
     ]),

    ("What is Named Entity Recognition (NER), and where is it applied?",
     [
        "NER is the task of detecting spans in text that refer to entities of interest and "
        "assigning them a category: Person, Organization, Location, Date, Money, Product, "
        "and so on. It is typically framed as token-level sequence labeling using IOB or "
        "BIOES tagging schemes.",
        "Applications: information extraction from news, financial filings, and clinical "
        "notes; populating knowledge graphs; redacting personally identifiable information; "
        "indexing documents for search; question-answering pipelines; compliance "
        "(detecting regulated entities); GraphRAG triplet extraction; resume parsing.",
        "Modern systems use transformer-based encoders (BERT, RoBERTa) fine-tuned on "
        "labeled NER corpora (CoNLL-2003, OntoNotes, MIT Restaurant), or zero-shot via "
        "instruction-tuned LLMs for novel domains.",
     ]),

    ("How does Latent Dirichlet Allocation (LDA) work for topic modeling?",
     [
        "LDA is a generative probabilistic model that assumes each document is a mixture of "
        "topics, and each topic is a distribution over words. Given a corpus, LDA infers "
        "(a) the topic distribution per document and (b) the word distribution per topic.",
        "Generative story: for each document, sample a distribution over K topics from a "
        "Dirichlet prior. For each word position, sample a topic from that distribution, "
        "then sample a word from that topic's word distribution. Inference reverses this: "
        "given the words, estimate the topic distributions, typically via variational "
        "inference or collapsed Gibbs sampling.",
        "Strengths: unsupervised, interpretable (you can read the top words per topic), "
        "fast on moderate corpora. Limitations: requires choosing K, assumes bag-of-words "
        "(no order), topics can be incoherent on noisy data. Modern alternatives: BERTopic, "
        "which clusters document embeddings and assigns interpretable labels using class-"
        "based TF-IDF.",
     ]),

    ("What are transformers in NLP, and how have they impacted the field?",
     [
        "Transformers are a neural architecture introduced in 'Attention Is All You Need' "
        "(Vaswani et al., 2017). They replace recurrence with self-attention, allowing every "
        "token to directly attend to every other token in the input. This breaks the "
        "sequential bottleneck of RNNs and parallelizes across the sequence axis.",
        "Impact: transformers swept NLP within three years. BERT (encoder-only) set new "
        "state-of-the-art on classification, NER, question answering. GPT (decoder-only) "
        "showed that scaling decoder transformers produces general-purpose text generators. "
        "T5 unified tasks as text-to-text. By 2020 transformers were ubiquitous in NLP and "
        "by 2022 they had expanded to vision (ViT), audio (Whisper), and multimodal models "
        "(CLIP, DALL-E). Every modern LLM is a transformer or a transformer derivative.",
     ],
     ["09_transformer.png", "10_attention.png"]),

    ("What is transfer learning in NLP, and how is it applied?",
     [
        "Transfer learning in NLP means reusing knowledge from a model pretrained on a "
        "large general corpus to improve a downstream task with limited data. The dominant "
        "pattern: pretrain a transformer on a self-supervised objective on billions of "
        "tokens, then fine-tune on a specific task.",
        "Application patterns: (1) feature extraction: use the pretrained model as a frozen "
        "encoder and train a small classifier on top of its embeddings. (2) Full fine-"
        "tuning: continue training the pretrained model on the target task. (3) PEFT: train "
        "small additional parameters (LoRA, adapters, prefix tuning) while keeping the base "
        "frozen. (4) In-context learning: pass examples in the prompt with no parameter "
        "updates. (5) RAG: retrieve relevant context at inference time.",
        "Choice depends on data size, compute budget, and how far the target domain is from "
        "the pretraining distribution. Small data plus small domain shift → in-context "
        "learning. Larger data with domain shift → PEFT or full fine-tuning.",
     ]),

    ("How do you handle out-of-vocabulary (OOV) words in NLP models?",
     [
        "Classical approach: replace OOV words with a special <UNK> token. Loses information "
        "and degrades quality.",
        "Subword tokenization (BPE, WordPiece, SentencePiece, Unigram): split rare words "
        "into known subword units. 'unbelievable' becomes ['un', 'believ', 'able']. Modern "
        "LLMs use this approach and effectively never face OOV at the input level: any "
        "string can be encoded as a sequence of subword tokens.",
        "Character-level models avoid OOV entirely but are slower and lose word-level "
        "structure. FastText averages character n-gram embeddings to give every word "
        "(including unseen ones) a meaningful vector. For domain-specific terms, extend the "
        "vocabulary with domain tokens, then continue pretraining briefly on domain text so "
        "the new tokens learn meaningful embeddings.",
     ]),

    ("Explain attention mechanisms and their role in sequence-to-sequence tasks.",
     [
        "Attention lets the decoder of a sequence-to-sequence model look back at the encoder "
        "outputs and decide which positions are relevant for generating the next output "
        "token. Instead of compressing the entire input into one fixed vector (as the "
        "original RNN encoder-decoder did), the decoder forms a weighted combination of all "
        "encoder hidden states, where the weights depend on the current decoder state.",
        "Mechanics: compute attention scores between the current query and all keys; "
        "normalize with softmax to produce weights; combine the values with those weights. "
        "Modern transformer attention uses scaled dot-product: softmax(Q·Kᵀ / √d) · V.",
        "Role: attention solves the bottleneck of fixed-size context vectors and enables "
        "much better long-sequence modeling. It is also interpretable to a useful degree: "
        "attention weights tell you which input positions the model relied on, which is "
        "valuable for debugging and explanation.",
     ],
     ["10_attention.png"]),

    ("What is a language model, and how is it evaluated?",
     [
        "A language model assigns probabilities to sequences of words. Equivalently, it "
        "predicts the next word given the previous words: P(w_t | w_1, ..., w_{t-1}). It "
        "may be unidirectional (decoder-only, GPT-style) or bidirectional (encoder-only, "
        "BERT-style with masked language modeling).",
        "Intrinsic evaluation: perplexity = exp(average negative log-likelihood per token) "
        "on a held-out corpus. Lower is better. Perplexity measures how well the model "
        "predicts the next token but is only weakly correlated with downstream task "
        "performance once perplexity is below a usable threshold.",
        "Extrinsic evaluation: performance on downstream benchmarks. Classification "
        "accuracy, F1 for NER, BLEU/ROUGE for translation/summarization, exact match for "
        "QA, MMLU and HellaSwag for general reasoning, HumanEval for code, MT-Bench and "
        "Chatbot Arena for open-ended chat. For generation, also human evaluation and "
        "LLM-as-a-judge with bias control.",
     ]),

    # BONUS
    ("What is BM25 and why is it still relevant?",
     [
        "BM25 (Best Matching 25) is a probabilistic ranking function that extends TF-IDF "
        "with term-frequency saturation and document-length normalization. It computes a "
        "relevance score between a query and a document based on term overlap.",
        "Why it still matters: BM25 is fast, requires no training, no GPU, and produces "
        "strong baselines on keyword-heavy queries. Modern hybrid retrieval combines BM25 "
        "with dense retrieval via reciprocal rank fusion, and almost always beats either "
        "alone. Production search systems (Elasticsearch, OpenSearch, Lucene) ship BM25 as "
        "the default scoring.",
     ]),
]
