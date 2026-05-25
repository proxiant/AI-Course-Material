"""Chapter 6: Word and Sentence Embeddings."""

CHAPTER = {
    "label": "Chapter 6",
    "title": "Word and Sentence Embeddings",
    "intro_image": "15_embeddings.png",
    "intro_caption": "Figure 6.1: Word embeddings cluster by meaning in vector space.",
    "sections": [
        {
            "number": "6.1",
            "title": "The Embedding Concept",
            "paragraphs": [
                "Words are discrete symbols. Neural networks operate on continuous vectors. "
                "An embedding is the bridge: a learned function that maps each word, sentence, "
                "or document to a point in a high-dimensional vector space, such that "
                "geometric relationships in that space approximate semantic relationships in "
                "the original domain.",

                "This idea generalizes. Embeddings exist for users in recommendation systems, "
                "for nodes in graphs, for products in e-commerce, for images and audio in "
                "multimodal systems. The same geometric framework applies: similar items are "
                "nearby, related items have meaningful directional relationships, and the "
                "space itself can be analyzed, clustered, and searched.",

                "The historical arc: one-hot vectors (dimension = vocabulary size, all zeros "
                "except one) gave way to count-based methods (LSA, LDA topic distributions), "
                "then to learned word embeddings (Word2Vec, GloVe, FastText), then to "
                "contextual embeddings from transformers (BERT and successors). Each "
                "generation captured more meaning in fewer dimensions with better "
                "generalization. This chapter walks the arc and ends at the state of the "
                "practice.",
            ],
        },
        {
            "number": "6.2",
            "title": "From One-Hot to Dense",
            "paragraphs": [
                "One-hot encoding represents word i as a vector of length |V| (vocabulary "
                "size) with a 1 in position i and 0 elsewhere. Three fatal problems: high "
                "dimensionality (|V| can be 100K+), no notion of similarity (every word is "
                "equidistant from every other word), and out-of-vocabulary words have no "
                "representation at all.",

                "Dense embeddings replace one-hot vectors with low-dimensional (typically "
                "50-1024) real-valued vectors. The vector for 'cat' is learned, not assigned. "
                "Two key properties emerge from good training: similar words have similar "
                "vectors (high cosine similarity), and relationships between words manifest "
                "as consistent directions (vector('king') - vector('man') + vector('woman') ≈ "
                "vector('queen')).",

                "The benefit is generalization. A classifier trained on 'cat' images can "
                "transfer some understanding to 'kitten' images because their text embeddings "
                "are nearby. A model that has seen many sentences about 'Paris' can apply "
                "that knowledge to a question about 'the capital of France' through embedding "
                "similarity. Dense embeddings let models share information across related "
                "items rather than treating each as independent.",
            ],
        },
        {
            "number": "6.3",
            "title": "Word2Vec in Detail",
            "image": "29_word2vec.png",
            "caption": "Figure 6.2: Word2Vec Skip-Gram architecture.",
            "paragraphs": [
                "Word2Vec (Mikolov et al., 2013) was a watershed: a fast, simple neural "
                "training procedure that produced word embeddings of unprecedented quality. "
                "Two architectures.",
            ],
            "subsections": [
                {
                    "title": "6.3.1 Continuous Bag of Words (CBOW)",
                    "paragraphs": [
                        "Predict the center word from its context window. Input: average of "
                        "context word embeddings (or sum). Output: predicted center word via "
                        "softmax over vocabulary. The hidden layer is the embedding lookup "
                        "table; the output layer is a separate matrix.",
                        "CBOW is faster to train than Skip-Gram and produces slightly smoother "
                        "embeddings for frequent words. The downside: small datasets produce "
                        "weaker embeddings because there is less signal per context.",
                    ],
                },
                {
                    "title": "6.3.2 Skip-Gram",
                    "paragraphs": [
                        "Predict the context words from the center word. Input: single center "
                        "word embedding. Output: probability of each context word. The "
                        "training objective: maximize log P(context | center) summed over "
                        "(center, context) pairs in a corpus.",
                        "Skip-Gram works better on rare words and produces embeddings that "
                        "capture finer distinctions. It became the dominant variant in "
                        "practice.",
                    ],
                },
                {
                    "title": "6.3.3 Negative Sampling",
                    "paragraphs": [
                        "Computing softmax over the entire vocabulary is expensive. Negative "
                        "sampling replaces it with a binary classification: distinguish "
                        "actual (center, context) pairs from randomly sampled (center, "
                        "negative) pairs.",
                        "For each true pair, sample k negatives (typically k = 5 to 20). "
                        "Train with binary cross-entropy. The gradient updates only the "
                        "involved word vectors, not all of them. Training speeds up by orders "
                        "of magnitude with little quality loss.",
                    ],
                },
                {
                    "title": "6.3.4 Hierarchical Softmax",
                    "paragraphs": [
                        "An alternative to negative sampling. Organize the vocabulary as a "
                        "binary tree (often a Huffman tree by word frequency). Predicting a "
                        "word becomes log(|V|) binary decisions along the tree path. "
                        "Asymptotically faster than full softmax. Less popular than negative "
                        "sampling in practice but elegant.",
                    ],
                },
            ],
        },
        {
            "number": "6.4",
            "title": "GloVe and FastText",
            "paragraphs": [
                "GloVe (Pennington et al., 2014) approaches embeddings through matrix "
                "factorization. Build a global co-occurrence matrix X where X_ij is the "
                "number of times word i appears in the context of word j. Factor it into "
                "word vectors that approximate log X_ij. GloVe combines the global "
                "statistical view of LSA with the local prediction-based training of "
                "Word2Vec. Empirically comparable to Word2Vec; the choice often comes down "
                "to convenience.",

                "FastText (Bojanowski et al., 2016) addresses the rare-word problem. "
                "Represent each word as a sum of its character n-gram embeddings (typically "
                "n = 3 to 6). The word 'unbelievable' decomposes to character n-grams like "
                "'<un', 'unb', 'nbe', ..., 'le>'. Each n-gram has an embedding; the word "
                "embedding is the sum.",

                "Two benefits. Morphologically rich languages (Finnish, Turkish) get better "
                "embeddings because related word forms share n-grams. Truly unseen words at "
                "test time get meaningful vectors from their character pieces. FastText is "
                "still widely used in production for these reasons.",
            ],
        },
        {
            "number": "6.5",
            "title": "Contextual Embeddings: ELMo and BERT",
            "paragraphs": [
                "Static word embeddings have a fundamental limitation: each word has one "
                "vector regardless of context. 'Bank' as a financial institution and 'bank' "
                "as a river bank get the same embedding. The first cracks in this approach "
                "appeared with ELMo (Embeddings from Language Models, Peters et al., 2018), "
                "which concatenated forward and backward LSTM hidden states to produce "
                "context-dependent representations.",

                "BERT (Devlin et al., 2018) took this much further. A bidirectional "
                "transformer trained with masked language modeling produces an embedding for "
                "each token that depends on the entire sentence. The same word in different "
                "contexts gets different vectors. The same token in 'I deposited money at "
                "the bank' and 'I sat by the river bank' receives meaningfully different "
                "embeddings.",

                "How to use BERT for embedding generation. Pass a sentence through BERT; "
                "take the final hidden states. The [CLS] token's embedding is often used "
                "as a sentence representation, though this is naive. Better practice: pool "
                "the token embeddings (mean or weighted), or use a model fine-tuned with a "
                "sentence-level objective (Sentence-BERT, BGE, E5).",

                "Why contextual embeddings matter for retrieval. A query and a document may "
                "share no surface tokens but have similar meaning. Contextual embeddings of "
                "the full query and document capture this. Modern semantic search depends on "
                "this property.",
            ],
        },
        {
            "number": "6.6",
            "title": "Sentence Embeddings",
            "paragraphs": [
                "Word embeddings can be averaged or pooled to produce sentence embeddings, "
                "but the results are mediocre. Word order, negation, and compositional "
                "structure are lost. Dedicated sentence embedders fix this.",
            ],
            "subsections": [
                {
                    "title": "6.6.1 Sentence-BERT and Successors",
                    "paragraphs": [
                        "Sentence-BERT (Reimers and Gurevych, 2019) fine-tunes a pretrained "
                        "BERT with a siamese network architecture. Two BERT towers share "
                        "weights. Each tower encodes a sentence. The cosine similarity "
                        "between sentence embeddings is trained to match a target "
                        "(similarity score, classification label, contrastive label).",
                        "The result is a sentence encoder that produces high-quality "
                        "embeddings in a single forward pass. Cosine similarity becomes "
                        "meaningful between sentences. Semantic search, clustering, and "
                        "similarity at the sentence and document level all use this pattern.",
                        "Modern successors: MPNet, BGE (Beijing Academy), E5 (Microsoft), "
                        "GTE (Alibaba). Each pushes the MTEB benchmark (Massive Text "
                        "Embedding Benchmark) forward. Open-weights models from these "
                        "families are competitive with closed-source embedders (OpenAI "
                        "ada-002, Cohere embed) at much lower cost.",
                    ],
                },
                {
                    "title": "6.6.2 Contrastive Training Objectives",
                    "paragraphs": [
                        "Modern sentence embedders are trained with contrastive objectives. "
                        "The intuition: pull semantically similar sentence pairs together, "
                        "push dissimilar pairs apart.",
                        "Triplet loss (anchor, positive, negative with margin) was the "
                        "original approach. InfoNCE (anchor against batch of negatives via "
                        "softmax) is now standard. Both are forms of contrastive learning.",
                        "Hard negative mining matters enormously. Random negatives are usually "
                        "trivially distinguishable from the positive; the model learns "
                        "nothing useful. Hard negatives (semantically close but labeled "
                        "different) provide the strongest training signal. Production "
                        "pipelines mine hard negatives from production logs, BM25 top hits, "
                        "or dense top hits that the model previously got wrong.",
                    ],
                },
            ],
        },
        {
            "number": "6.7",
            "title": "Properties of Embedding Spaces",
            "paragraphs": [
                "Beyond the basic 'similar = nearby' property, embedding spaces have richer "
                "structure that influences how you use them.",
            ],
            "subsections": [
                {
                    "title": "6.7.1 Anisotropy",
                    "paragraphs": [
                        "Plain BERT embeddings cluster in a narrow cone in embedding space. "
                        "Average pairwise cosine similarity is high across unrelated "
                        "sentences. This inflates similarity scores uniformly and reduces "
                        "the discriminative power of cosine similarity.",
                        "Two fixes. Whitening: subtract the mean, scale by the inverse "
                        "covariance matrix's square root. The resulting embeddings are zero-"
                        "mean and unit-covariance. Post-hoc, cheap, often substantially "
                        "improves retrieval. Contrastive fine-tuning: train with InfoNCE or "
                        "triplet loss to spread the embeddings across the space. The modern "
                        "default; eliminates anisotropy structurally rather than patching it.",
                    ],
                },
                {
                    "title": "6.7.2 Curse of Dimensionality",
                    "paragraphs": [
                        "Embeddings live in 100-1024-dimensional spaces. Human geometric "
                        "intuition fails. Three counter-intuitive properties: nearly all "
                        "volume of a unit ball lies near its surface; random unit vectors are "
                        "nearly orthogonal; distances concentrate (the ratio of maximum to "
                        "minimum pairwise distance approaches 1).",
                        "Consequences. Naive 'nearest neighbor' search loses discriminative "
                        "power at very high dimensions; approximate methods are necessary. "
                        "Cosine similarity is preferred over Euclidean distance because it "
                        "ignores magnitude. Embeddings should be L2-normalized before "
                        "cosine-based operations.",
                    ],
                },
                {
                    "title": "6.7.3 Matryoshka Embeddings",
                    "paragraphs": [
                        "Some embedders are trained so that prefixes of the full embedding "
                        "also function as useful embeddings at lower dimensions. A 768-"
                        "dimensional embedding's first 64 dimensions are themselves a usable "
                        "64-dimensional embedding.",
                        "Use case: progressive search. Use the 64-dimensional truncation for "
                        "cheap pruning across millions of candidates, then re-score the top "
                        "100 with the full 768-dimensional embedding. Memory and latency drop "
                        "without giving up final-stage quality.",
                        "Implementations: bge-m3, nomic-embed, openai text-embedding-3.",
                    ],
                },
            ],
        },
        {
            "number": "6.8",
            "title": "Cross-Modal Embeddings",
            "paragraphs": [
                "Cross-modal embeddings live in a shared space across modalities (text and "
                "image, text and audio). The same point in the space can be reached from "
                "multiple modalities, enabling cross-modal retrieval (text query for an "
                "image) and zero-shot transfer (use text labels to classify images without "
                "image training labels).",

                "CLIP (Radford et al., 2021) is the canonical example. Image encoder (ViT) "
                "and text encoder (transformer) are trained jointly on 400M image-caption "
                "pairs with a contrastive loss: image embeddings should be near their "
                "captions and far from other captions. The resulting embedding space "
                "supports zero-shot image classification (encode candidate text labels, "
                "embed the image, take argmax similarity) and cross-modal retrieval.",

                "ImageBind (Meta, 2023) extends this to six modalities (images, text, audio, "
                "depth, thermal, IMU) by using image as the binding modality. Train each "
                "non-image modality against images; the space ends up aligned across "
                "modalities that were never paired directly.",
            ],
        },
        {
            "number": "6.9",
            "title": "Quantization and Efficient Storage",
            "paragraphs": [
                "Embeddings are typically stored as float32 vectors. A million 768-"
                "dimensional vectors is 3GB. At billion scale, this becomes the dominant "
                "memory cost. Quantization compresses embeddings at some cost to recall.",
            ],
            "subsections": [
                {
                    "title": "6.9.1 Scalar Quantization",
                    "paragraphs": [
                        "Convert each dimension from float32 to int8 (or int4, or int2). "
                        "4x to 16x smaller. Apply a per-vector or per-dimension scale and "
                        "zero point. Typically loses less than 1 percentage point on retrieval "
                        "recall. The default first step.",
                    ],
                },
                {
                    "title": "6.9.2 Product Quantization (PQ)",
                    "paragraphs": [
                        "Split each vector into m subvectors. Train k codewords per "
                        "subvector via k-means. Replace each subvector with its nearest "
                        "codeword index. Storage: m · log₂(k) bits per vector, often 32x "
                        "smaller than float32. Used by FAISS at billion scale.",
                        "Variants: OPQ (rotate before quantizing), Residual PQ (multi-stage "
                        "to capture remaining error), Inverted File + PQ (the standard "
                        "FAISS index for very large datasets).",
                    ],
                },
                {
                    "title": "6.9.3 Binary Embeddings",
                    "paragraphs": [
                        "One bit per dimension. Hamming distance replaces cosine. 32x "
                        "compression. Loss is real but acceptable for first-stage retrieval. "
                        "Modern production systems rerank with full-precision embeddings on "
                        "the candidate set, so the binary stage is purely for fast filtering.",
                    ],
                },
            ],
        },
        {
            "number": "6.10",
            "title": "Evaluating Embedding Quality",
            "paragraphs": [
                "How do you know if an embedder is good? Several complementary metrics.",
            ],
            "subsections": [
                {
                    "title": "6.10.1 Intrinsic Evaluation",
                    "paragraphs": [
                        "Similarity correlation. Compute cosine similarity of embedding "
                        "pairs; correlate with human similarity ratings (Spearman or "
                        "Pearson). Standard datasets: STS-B (sentence textual similarity), "
                        "WordSim-353, SimLex-999. Spearman correlation is the de facto "
                        "reporting metric for embedding model leaderboards.",
                        "Analogy benchmarks. king - man + woman = ? Classic but limited; "
                        "less informative on modern embedders than retrieval metrics.",
                        "Clustering metrics. Silhouette score, Davies-Bouldin index, "
                        "Calinski-Harabasz index. Useful when you have ground-truth clusters "
                        "(topic-labeled documents, intent-labeled queries).",
                    ],
                },
                {
                    "title": "6.10.2 Extrinsic Evaluation",
                    "paragraphs": [
                        "Downstream task performance is the ultimate test. Use the embeddings "
                        "for the actual task and measure task-specific metrics: Recall@k for "
                        "retrieval, accuracy for classification, V-measure for clustering.",
                        "MTEB (Massive Text Embedding Benchmark) aggregates 50+ tasks across "
                        "classification, clustering, retrieval, reranking, similarity. The "
                        "comprehensive standard for comparing text embedders.",
                        "Domain-specific evaluation. Build a held-out set of relevant queries "
                        "and known answers in your domain. Measure Recall@k. Public "
                        "benchmarks may not reflect your data distribution; in-domain "
                        "evaluation is decisive.",
                    ],
                },
            ],
        },
        {
            "number": "6.11",
            "title": "Summary",
            "bullets": [
                "Embeddings map discrete items (words, sentences, images) to dense vectors "
                "such that geometric relationships approximate semantic relationships.",
                "Word2Vec, GloVe, and FastText produce static word embeddings. They are "
                "fast, mature, and still useful for many tasks.",
                "Contextual embeddings from BERT and successors solve the polysemy problem "
                "and produce strong sentence-level embeddings when fine-tuned with "
                "contrastive objectives.",
                "Cross-modal embeddings (CLIP, ImageBind) align modalities in a shared space, "
                "enabling cross-modal retrieval and zero-shot transfer.",
                "Quantization (scalar, product, binary) makes billion-scale embedding storage "
                "and search feasible.",
                "MTEB is the standard public benchmark; domain-specific in-house evaluation "
                "is decisive for production decisions.",
            ],
        },
    ],
    "further_reading": [
        "Mikolov et al., 'Distributed Representations of Words and Phrases and their "
        "Compositionality' (2013). Word2Vec with negative sampling.",
        "Reimers and Gurevych, 'Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks' "
        "(2019).",
        "Radford et al., 'Learning Transferable Visual Models From Natural Language "
        "Supervision' (2021). CLIP.",
        "Kusupati et al., 'Matryoshka Representation Learning' (2022).",
    ],
}
