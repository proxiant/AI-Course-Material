"""Chapter 4: Classical Natural Language Processing."""

CHAPTER = {
    "label": "Chapter 4",
    "title": "Classical Natural Language Processing",
    "sections": [
        {
            "number": "4.1",
            "title": "Why Language Is Hard",
            "paragraphs": [
                "Language carries meaning. Computers traffic in numbers. Bridging that gap is "
                "the central problem of natural language processing. Words are discrete symbols "
                "with rich meaning that depends on context, culture, and intent. The same "
                "string can mean different things; different strings can mean the same thing. "
                "Order matters, but not always equally. Some structures are recursive: a "
                "noun phrase can contain a noun phrase.",

                "Classical NLP attacked these challenges with hand-crafted features (parts of "
                "speech, syntactic parses) and statistical models (n-grams, hidden Markov "
                "models, conditional random fields). These techniques produced working "
                "systems and remain useful as baselines and components, even though deep "
                "learning has displaced them at the cutting edge.",

                "This chapter covers the classical methods you should know. They illuminate "
                "what came before transformers, they remain in production for many tasks where "
                "they are good enough, and they often serve as components of larger neural "
                "systems (BM25 in hybrid retrieval, NER pipelines, sentence boundary "
                "detection).",
            ],
        },
        {
            "number": "4.2",
            "title": "Tokenization",
            "image": "35_tokenization_compare.png",
            "caption": "Figure 4.1: Word, character, and subword tokenization compared.",
            "paragraphs": [
                "Tokenization splits raw text into the units a model will process. The choice "
                "of tokenizer has surprisingly large consequences for downstream model "
                "behavior.",
            ],
            "subsections": [
                {
                    "title": "4.2.1 Word-Level Tokenization",
                    "paragraphs": [
                        "Split on whitespace and punctuation. Simple. Suffers from a vocabulary "
                        "explosion (every inflection, compound, proper noun is a separate "
                        "token) and out-of-vocabulary handling (any unseen word is mapped to "
                        "<UNK>, losing information).",
                        "Variants: lowercasing, stemming (chop suffixes by rule), "
                        "lemmatization (reduce to dictionary form using morphological "
                        "analysis). Modern systems rarely use these explicitly; subword "
                        "tokenizers handle surface variation implicitly through shared "
                        "subword units.",
                    ],
                },
                {
                    "title": "4.2.2 Character-Level Tokenization",
                    "paragraphs": [
                        "Treat each character as a token. Eliminates out-of-vocabulary issues. "
                        "Very long sequences (5-10x longer than word-level) make modeling "
                        "slower. Loses higher-level structure that word boundaries provide.",
                    ],
                },
                {
                    "title": "4.2.3 Subword Tokenization (BPE, WordPiece, SentencePiece)",
                    "paragraphs": [
                        "The dominant choice for modern LLMs. Start from individual characters; "
                        "iteratively merge the most frequent adjacent pair into a new token; "
                        "stop when vocabulary reaches a target size (typically 30K-100K).",
                        "Byte-Pair Encoding (BPE) is the original algorithm; WordPiece is the "
                        "Google variant used in BERT; SentencePiece is a language-agnostic "
                        "framework that handles whitespace as a regular character (used in "
                        "T5 and LLaMA). Unigram language modeling tokenization is another "
                        "approach used in SentencePiece.",
                        "Net effect: common words become single tokens; rare words decompose "
                        "into known subword pieces; truly unseen strings still encode without "
                        "<UNK>. 'unbelievable' might be ['un', 'believ', 'able']. The model's "
                        "embedding for the rare word is composed from its constituent "
                        "embeddings.",
                    ],
                },
            ],
        },
        {
            "number": "4.3",
            "title": "Text Representation: Bag of Words and TF-IDF",
            "paragraphs": [
                "Before learning anything fancy, you need a way to turn documents into vectors. "
                "The Bag of Words (BoW) representation does this naively: enumerate the "
                "vocabulary, represent each document as a vector of term counts.",

                "BoW loses word order entirely. 'Dog bites man' and 'Man bites dog' produce "
                "the same vector. It cannot capture meaning: synonyms become separate "
                "dimensions, polysemous words collapse. The vocabulary grows with the "
                "corpus, producing very high-dimensional sparse vectors.",

                "TF-IDF (Term Frequency × Inverse Document Frequency) refines this. TF(t, d) "
                "is the frequency of term t in document d. IDF(t) = log(N / df(t)) is the "
                "logarithm of the inverse document frequency. The product TF-IDF(t, d) = "
                "TF · IDF gives high scores to words that are frequent in a document but rare "
                "across the corpus.",

                "BM25 is the modern successor of TF-IDF. It adds term-frequency saturation "
                "(diminishing returns from repeated occurrences) and document length "
                "normalization. BM25 remains an extremely strong baseline for retrieval and "
                "is still embedded in Elasticsearch, OpenSearch, and Lucene as the default "
                "scoring function. In hybrid retrieval systems, BM25 plus dense retrieval "
                "almost always beats either alone.",
            ],
        },
        {
            "number": "4.4",
            "title": "Word Embeddings: Word2Vec and GloVe",
            "image": "29_word2vec.png",
            "caption": "Figure 4.2: Word2Vec Skip-Gram predicts context words from a center word.",
            "paragraphs": [
                "The fundamental limitation of BoW and TF-IDF is that each word is a separate "
                "dimension. The model cannot generalize from 'cat' to 'kitten' or from 'dog' "
                "to 'puppy'. Word embeddings solve this by placing each word at a point in a "
                "low-dimensional vector space such that similar words are nearby.",

                "Word2Vec (Mikolov et al., 2013) trains a shallow neural network on a "
                "self-supervised objective: predict context words from a center word (skip-"
                "gram) or predict a center word from its context (CBOW). The hidden layer "
                "produces the embedding. Typical dimension: 100-300.",

                "The famous result: vector arithmetic captures analogies. king - man + woman ≈ "
                "queen. Paris - France + Italy ≈ Rome. The embeddings encode semantic "
                "relationships in linear algebra.",

                "GloVe (Global Vectors for Word Representation, Pennington et al., 2014) "
                "produces similar embeddings by matrix factorization of a global word-context "
                "co-occurrence matrix. Different math, similar properties.",

                "FastText (Facebook, 2016) extends Word2Vec by treating each word as a sum of "
                "character n-gram embeddings. Handles morphologically rich languages and "
                "out-of-vocabulary words better.",

                "Static word embeddings are limited: each word has one vector regardless of "
                "context. 'Bank' (financial institution) and 'bank' (river bank) get the same "
                "embedding. Contextual embeddings from BERT and other transformers fix this; "
                "we cover them in Chapter 8.",
            ],
        },
        {
            "number": "4.5",
            "title": "Named Entity Recognition and Sequence Labeling",
            "paragraphs": [
                "Named Entity Recognition (NER) detects spans in text that refer to entities "
                "of interest (Person, Organization, Location, Date, Money) and tags them with "
                "category labels. It is a foundational information extraction task.",

                "Classical NER used Conditional Random Fields (CRFs) over hand-crafted "
                "features (capitalization, prefix, suffix, gazetteers). Modern NER uses "
                "transformer-based encoders (BERT, RoBERTa) fine-tuned on labeled corpora "
                "(CoNLL-2003, OntoNotes). Zero-shot NER via instruction-tuned LLMs is "
                "increasingly competitive for novel domains.",

                "NER is typically framed as token-level sequence labeling using IOB or BIOES "
                "tagging schemes (B-PER, I-PER, O for outside, etc.). The model predicts a "
                "label for each token; consecutive same-type labels form a span.",

                "Applications: information extraction from news, financial filings, and "
                "clinical notes; populating knowledge graphs; redacting personally "
                "identifiable information; resume parsing; GraphRAG triplet extraction.",
            ],
        },
        {
            "number": "4.6",
            "title": "Topic Modeling with LDA",
            "paragraphs": [
                "Latent Dirichlet Allocation (LDA, Blei et al., 2003) is a generative "
                "probabilistic model of document collections. It assumes each document is a "
                "mixture of topics, and each topic is a distribution over words.",

                "Generative story: for each document, sample a distribution over K topics from "
                "a Dirichlet prior. For each word position, sample a topic from that "
                "distribution, then sample a word from that topic's word distribution. "
                "Inference reverses this: given the observed words, estimate the topic "
                "distributions via variational inference or collapsed Gibbs sampling.",

                "Strengths: unsupervised, interpretable (you can read the top words per "
                "topic), fast on moderate corpora. Weaknesses: requires choosing K; assumes "
                "bag-of-words (no order); topics can be incoherent on noisy data. Modern "
                "alternatives such as BERTopic cluster sentence embeddings and label "
                "clusters with class-based TF-IDF.",
            ],
        },
        {
            "number": "4.7",
            "title": "Evaluation Metrics for NLP",
            "image": "27_confusion_matrix.png",
            "caption": "Figure 4.3: Confusion matrix for binary classification.",
            "paragraphs": [
                "Classification: accuracy (fraction correct), precision (true positives / "
                "predicted positives), recall (true positives / actual positives), F1 "
                "(harmonic mean of precision and recall). ROC curves and AUC for ranking "
                "quality.",

                "Translation: BLEU (n-gram overlap with reference), chrF (character F-score), "
                "COMET (learned metric correlated with human judgment).",

                "Summarization: ROUGE-1/2/L (recall-oriented n-gram overlap). BERTScore for "
                "semantic similarity. Human evaluation for faithfulness and coherence.",

                "Sequence labeling (NER, POS): token-level F1 plus span-level F1 (exact match "
                "of predicted spans against gold).",

                "Language modeling: perplexity = exp(per-token cross-entropy). Lower is "
                "better. Cheap to compute. Only weakly correlated with downstream task "
                "performance once perplexity is below a usable threshold.",
            ],
        },
        {
            "number": "4.8",
            "title": "Summary",
            "bullets": [
                "Tokenization turns text into integer IDs. Subword tokenizers (BPE, "
                "WordPiece, SentencePiece) are the modern default and handle out-of-"
                "vocabulary gracefully.",
                "BoW and TF-IDF are simple but powerful baselines for text representation. "
                "BM25 is the modern variant and remains a strong production retriever.",
                "Word embeddings (Word2Vec, GloVe, FastText) encode words as dense vectors "
                "with meaningful geometry. Static embeddings give one vector per word; "
                "contextual embeddings vary by context (Chapter 8).",
                "Named entity recognition and topic modeling solve information extraction at "
                "different granularities.",
                "Classification metrics, BLEU/ROUGE for generation, and perplexity for "
                "language modeling form the core evaluation toolkit.",
            ],
        },
    ],
    "further_reading": [
        "Jurafsky and Martin, Speech and Language Processing (3rd ed. draft, free online). "
        "The definitive NLP textbook.",
        "Mikolov et al., 'Efficient Estimation of Word Representations in Vector Space' "
        "(2013). the Word2Vec paper.",
        "Pennington, Socher, Manning, 'GloVe: Global Vectors for Word Representation' (2014).",
    ],
}
