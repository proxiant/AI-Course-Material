"""
Master content map for LLM and Enterprise RAG Bootcamp.
12 weeks. Saturdays = main session (11 AM - 5 PM PST). Mon/Wed = labs. Tue = quiz.
Style rules (project CLAUDE.md): no em dashes, no AI cliches, plain declarative prose.
"""

START_DATE = "Saturday, June 6, 2026"
DURATION_WEEKS = 12
TUITION = "$3,700 (or $3,600 if paid by check or Zelle upfront)"

PREREQ = ("Working Python (3.10+), comfort with NumPy and PyTorch basics, "
          "prior exposure to classical ML (logistic regression, decision trees, "
          "gradient boosting), and familiarity with at least one LLM API.")

WEEKS = [
    {
        "num": 1,
        "date": "Saturday, June 6, 2026",
        "title": "Introduction to Language Models",
        "tagline": "From keyword search to semantic understanding",
        "summary": (
            "Open day for the bootcamp. Trace the path from keyword search "
            "(TF-IDF, BM25) to semantic understanding via Transformers. Cover "
            "self-attention with Q, K, V. Introduce high-dimensional embeddings, "
            "approximate nearest neighbor (ANN) search, and the operational "
            "realities of running a vector database. The lab gets every "
            "student onto the Ray cluster and through a simple end-to-end RAG."
        ),
        "objectives": [
            "Trace the limits of keyword-based search and why semantic retrieval is needed",
            "Explain self-attention using Q, K, V projections and the scaled-dot-product",
            "Distinguish encoder, decoder, and encoder-decoder transformer families",
            "Describe ANN search tradeoffs (HNSW, IVF, PQ) at a working-engineer level",
            "Stand up a simple RAG pipeline (loader, chunker, embedder, store, retriever, generator)",
        ],
        "topics": [
            ("1. The limits of keyword search",
             "TF-IDF and BM25 are still strong baselines on keyword-heavy "
             "queries. They fail when the query and the document share meaning "
             "but no words. Semantic search exists to close that gap."),
            ("2. The transformer attention mechanism",
             "Self-attention computes a weighted combination of value vectors "
             "where the weights come from softmax(Q K^T / sqrt(d)). The "
             "scaling by sqrt(d) keeps softmax in a usable range as dimension "
             "grows."),
            ("3. Encoder vs decoder",
             "Encoder models (BERT family) produce strong embeddings. Decoder "
             "models (GPT family) generate text. Encoder-decoder models (T5) "
             "do both. Pick based on the downstream task, not the popularity."),
            ("4. Embeddings as the universal currency",
             "Every retrieval, classification, and clustering system runs on "
             "embeddings. The objective the embedder was trained with shapes "
             "the geometry you get downstream."),
            ("5. ANN search in practice",
             "Exact search is O(n) per query. ANN trades recall for speed. "
             "HNSW is the default; IVF is memory-friendly at scale; product "
             "quantization compresses the vectors themselves."),
            ("6. Vector database realities",
             "Index build time, RAM footprint, recall at k, query throughput, "
             "and update cost are the five numbers that matter. Benchmark "
             "against your data before committing."),
        ],
        "papers": [
            ("Attention Is All You Need",
             "Vaswani et al., 2017 (arXiv:1706.03762). The transformer paper."),
            ("Efficient and Robust Approximate Nearest Neighbor Search Using HNSW",
             "Malkov and Yashunin, 2016 (arXiv:1603.09320). The HNSW paper."),
        ],
        "labs": [
            {
                "title": "Environment setup and Ray cluster onboarding",
                "objective": "Provision the Conda environment, register your SSH key, and verify GPU visibility on the Proxiant Ray cluster.",
                "prereqs": "Laptop with Python 3.11, SSH key generated.",
                "steps": [
                    "Install the bootcamp Conda env from the lab repo.",
                    "Authenticate to the cluster head node.",
                    "Run the GPU smoke test and confirm one RTX 4090 is visible.",
                    "Submit a remote task that loads a small embedder.",
                ],
                "deliverables": "Notebook with cluster smoke test output and one embedding example.",
            },
            {
                "title": "End-to-end simple RAG walkthrough",
                "objective": "Build a 50-line RAG over a 200-document corpus with FAISS and a small embedder. Generate answers and measure baseline recall.",
                "prereqs": "Working cluster session, corpus shipped with the lab.",
                "steps": [
                    "Load the corpus and split into 500-token chunks.",
                    "Embed with bge-small and index in FAISS.",
                    "Implement retrieve(query, k=8) and generate(query, context).",
                    "Run 20 sample queries and record recall@8 and answer quality.",
                ],
                "deliverables": "Working notebook plus a short note on where the baseline fails.",
            },
        ],
    },
    {
        "num": 2,
        "date": "Saturday, June 13, 2026",
        "title": "High-Dimensional Geometry",
        "tagline": "BERT, contrastive loss, anisotropy, and the math of embeddings",
        "summary": (
            "Embeddings live in spaces with hundreds or thousands of "
            "dimensions. Today covers what is weird about those spaces: the "
            "concentration of measure, anisotropy in pretrained models, and "
            "the temperature-cosine interaction. Cover BERT and masked "
            "language modeling, then contrastive objectives (InfoNCE, "
            "SimCLR, Triplet) and how they shape geometry."
        ),
        "objectives": [
            "Explain three counter-intuitive properties of high-dimensional space",
            "Diagnose anisotropy in a pretrained model's embeddings and correct it",
            "Implement InfoNCE from scratch with in-batch negatives",
            "Pick between InfoNCE, SimCLR, and Triplet for a given task",
            "Use temperature to control sharpness in contrastive losses",
        ],
        "topics": [
            ("1. The geometry of high-dimensional spaces",
             "Almost all volume of a unit ball lies near its surface. Random "
             "vectors are nearly orthogonal. Distances concentrate. These "
             "facts shape everything that follows in retrieval."),
            ("2. BERT and masked language modeling",
             "Predict masked tokens from bidirectional context. The training "
             "signal teaches representations of context, which transfer well "
             "to downstream sentence-level tasks."),
            ("3. Anisotropy",
             "Pretrained model embeddings cluster in a narrow cone. Cosine "
             "similarity is inflated across the board. Whitening or contrastive "
             "fine-tuning corrects it."),
            ("4. Temperature in softmax",
             "A small temperature sharpens the distribution; a large one "
             "flattens it. In contrastive learning the temperature controls "
             "how hard the negatives feel."),
            ("5. InfoNCE",
             "Anchor against batch of negatives via softmax over similarities. "
             "Stable, sample-efficient, and the modern default."),
            ("6. Semantic search mechanics",
             "Query embedding, candidate embeddings, similarity scoring, top-k "
             "selection. The end-to-end latency budget shapes every other "
             "choice."),
        ],
        "papers": [
            ("BERT: Pre-training of Deep Bidirectional Transformers",
             "Devlin et al., 2018 (arXiv:1810.04805)."),
            ("SimCSE: Simple Contrastive Learning of Sentence Embeddings",
             "Gao et al., 2021 (arXiv:2104.08821). Contrastive on top of BERT."),
        ],
        "labs": [
            {
                "title": "Embedding basics: anisotropy and whitening",
                "objective": "Measure anisotropy in three pretrained models. Apply whitening. Compare retrieval quality before and after.",
                "prereqs": "GPU access, sentence-transformers installed.",
                "steps": [
                    "Embed 5000 sentences with three models (mpnet, bge, gte).",
                    "Compute the average pairwise cosine similarity (anisotropy proxy).",
                    "Apply whitening to each set of embeddings.",
                    "Re-measure and benchmark retrieval recall@10 on STS-B.",
                ],
                "deliverables": "Anisotropy chart, retrieval comparison table, and a short note on when whitening helps.",
            },
            {
                "title": "InfoNCE from scratch",
                "objective": "Implement InfoNCE in PyTorch with in-batch negatives. Train an embedder on a small text corpus. Compare against the pretrained baseline.",
                "prereqs": "PyTorch, a tagged text corpus (shipped with the lab).",
                "steps": [
                    "Build the data loader with positive pairs.",
                    "Write the InfoNCE loss with temperature.",
                    "Train for two epochs on a 10K-pair set.",
                    "Evaluate on the held-out retrieval set.",
                ],
                "deliverables": "Training curve, eval table, and a recommendation on temperature.",
            },
        ],
    },
    {
        "num": 3,
        "date": "Saturday, June 20, 2026",
        "title": "Retrieval",
        "tagline": "Enterprise RAG foundations, chunking, and hierarchical retrieval",
        "summary": (
            "The chunking week. Chunking is where most RAG systems quietly "
            "fail. Cover the philosophy first (precision vs context), then "
            "semantic, late, and contextual chunking. End with hierarchical "
            "retrieval using mother and child chunks. The lab implements four "
            "chunking strategies on the same corpus and ranks them."
        ),
        "objectives": [
            "Articulate the precision-vs-context tradeoff in chunking",
            "Implement fixed-size, semantic, late, and contextual chunking",
            "Build a mother-and-child hierarchical retrieval flow",
            "Measure chunking quality with retrieval recall and answer faithfulness",
            "Pick a chunking strategy for a given corpus and task",
        ],
        "topics": [
            ("1. The chunking philosophy",
             "Small chunks give precise hits but lose surrounding context. "
             "Large chunks preserve context but dilute relevance signals. "
             "Pick the chunk size with the downstream answer in mind."),
            ("2. Fixed-size vs semantic chunking",
             "Fixed-size splits on tokens; cheap and predictable. Semantic "
             "chunking splits on similarity drops between adjacent sentences; "
             "respects natural boundaries."),
            ("3. Late chunking",
             "Embed the whole document first, then split the resulting "
             "token-level embeddings into chunks. Preserves cross-chunk "
             "context in each chunk's embedding."),
            ("4. Contextual chunking",
             "Prepend a short LLM-generated summary of the surrounding "
             "context to each chunk before embedding. Anthropic's contextual "
             "retrieval paper showed 35% retrieval improvement on average."),
            ("5. Hierarchical retrieval",
             "Embed and retrieve at multiple granularities. Mother chunks "
             "for context, child chunks for precision. Return the parent of "
             "the matched child to the LLM."),
            ("6. Precision vs context as a system question",
             "The right chunk size also depends on the LLM's context window "
             "and the cost per token. Optimize the system, not the chunker "
             "in isolation."),
        ],
        "papers": [
            ("Late Chunking: Contextual Chunk Embeddings",
             "Günther et al., 2024 (arXiv:2409.04701)."),
            ("Contextual Retrieval",
             "Anthropic, 2024. Reading guide ships with the lab."),
        ],
        "labs": [
            {
                "title": "Four chunking strategies head to head",
                "objective": "Implement fixed-size, semantic, late, and contextual chunking on the same 1000-document corpus. Rank by retrieval recall@10.",
                "prereqs": "Sentence-transformers and an LLM API.",
                "steps": [
                    "Build each chunker as a separate function with shared interface.",
                    "Embed and index all four chunk sets.",
                    "Run a 100-query test set against each.",
                    "Compare recall@10, average chunk length, and end-to-end answer quality.",
                ],
                "deliverables": "Comparison table, a chart of recall vs chunk size, and a written recommendation per corpus type.",
            },
            {
                "title": "Mother-and-child hierarchical retrieval",
                "objective": "Build a two-level retrieval that matches against child chunks but returns mother chunks to the LLM.",
                "prereqs": "Lab 1 implementation as a starting point.",
                "steps": [
                    "Define mother (1000 tokens) and child (250 tokens) chunks with parent references.",
                    "Embed and index both levels.",
                    "Implement retrieve_with_parents(query, k).",
                    "Evaluate on the same 100-query set and compare to single-level.",
                ],
                "deliverables": "Source plus a comparison of hierarchical vs single-level on the eval.",
            },
        ],
    },
    {
        "num": 4,
        "date": "Saturday, June 27, 2026",
        "title": "Retrieval Funnel",
        "tagline": "Sparse + dense, Matryoshka, ColBERT, and cross-encoder fusion",
        "summary": (
            "Production retrieval is a funnel: many candidates in, few "
            "well-scored results out. Cover sparse (BM25, SPLADE) vs dense, "
            "Matryoshka Representation Learning for fast pruning, ColBERT "
            "for token-level interaction, and cross-encoder fusion at the "
            "top. The lab builds the full four-stage funnel."
        ),
        "objectives": [
            "Combine BM25 and dense retrieval in a single retrieve step",
            "Use Matryoshka embeddings to prune cheap candidates quickly",
            "Apply ColBERT (late-interaction) for token-level scoring",
            "Use a cross-encoder for final re-ranking",
            "Measure and tune the funnel end to end",
        ],
        "topics": [
            ("1. Sparse retrieval (BM25, SPLADE)",
             "BM25 is the classical baseline. SPLADE learns sparse "
             "representations that match BM25's efficiency with neural "
             "semantics."),
            ("2. Dense retrieval",
             "Bi-encoders project queries and documents into a shared space. "
             "Cosine similarity gives the score. Cheap at query time once "
             "the index is built."),
            ("3. Hybrid retrieval",
             "Combine sparse and dense via reciprocal rank fusion or "
             "weighted score sum. Almost always beats either alone."),
            ("4. Matryoshka Representation Learning",
             "Train embeddings that work at multiple truncation lengths "
             "(64, 128, 512). Use the short truncation for cheap pruning, "
             "the full length for final scoring."),
            ("5. ColBERT (late interaction)",
             "Score by summing the maximum similarity of each query token "
             "to any document token. More expressive than bi-encoders, "
             "cheaper than cross-encoders."),
            ("6. Cross-encoder fusion",
             "Encode the (query, document) pair jointly. Most accurate, "
             "most expensive. Use only on the final 20 to 100 candidates."),
            ("7. The four-stage funnel",
             "Stage 1: BM25 + dense in parallel (200 candidates each). "
             "Stage 2: Matryoshka prune to top 100. "
             "Stage 3: ColBERT score to top 30. "
             "Stage 4: cross-encoder rerank to top 5."),
        ],
        "papers": [
            ("ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction",
             "Khattab and Zaharia, 2020 (arXiv:2004.12832)."),
            ("Matryoshka Representation Learning",
             "Kusupati et al., 2022 (arXiv:2205.13147)."),
            ("SPLADE: Sparse Lexical and Expansion Model for First Stage Ranking",
             "Formal et al., 2021 (arXiv:2107.05720)."),
        ],
        "labs": [
            {
                "title": "Matryoshka embeddings and progressive pruning",
                "objective": "Train or load a Matryoshka embedder. Build a two-stage retrieval: 64-dim prune, full-dim score.",
                "prereqs": "Sentence-transformers with Matryoshka support.",
                "steps": [
                    "Load nomic-embed or bge-m3 (both support Matryoshka).",
                    "Index documents at full dimension.",
                    "Implement prune-then-score with 64 and 768 dim.",
                    "Measure latency and recall vs single-stage.",
                ],
                "deliverables": "Latency and recall numbers and a tuning recommendation.",
            },
            {
                "title": "Four-stage retrieval funnel end to end",
                "objective": "Build the full four-stage funnel and benchmark against the dense-only baseline.",
                "prereqs": "BM25 (Pyserini), ColBERT (RAGatouille), cross-encoder (sentence-transformers).",
                "steps": [
                    "Wire the four stages with explicit candidate counts.",
                    "Run on a 100-query eval set.",
                    "Compare end-to-end recall@5, latency, and cost.",
                    "Tune candidate counts at each stage.",
                ],
                "deliverables": "Funnel diagram with measured numbers and a tuning writeup.",
            },
        ],
    },
    {
        "num": 5,
        "date": "Saturday, July 4, 2026",
        "title": "Vision",
        "tagline": "CNNs, Vision Transformers, CLIP, and BLIP",
        "summary": (
            "Multimodal week. Walk from CNNs through Vision Transformers, "
            "then into vision-language models with CLIP and BLIP. The lab "
            "trio covers ViT classification, CLIP-based image-text search, "
            "and BLIP-2 for zero-shot visual reasoning."
        ),
        "objectives": [
            "Compare CNN and ViT architectures on a fixed image task",
            "Use CLIP for zero-shot classification and cross-modal retrieval",
            "Apply BLIP-2 with the Q-Former bridge for visual question answering",
            "Add image modalities to an existing RAG system",
            "Reason about latency and quality tradeoffs in multimodal systems",
        ],
        "topics": [
            ("1. CNN foundations",
             "Convolutional filters detect local patterns. Pooling reduces "
             "spatial dimensions. Stacking layers builds up hierarchy. ResNet "
             "added residual connections to train very deep networks."),
            ("2. Vision Transformers",
             "Split an image into patches; embed each patch; run a "
             "transformer. The same architecture as language, applied to "
             "vision. Excellent at scale, weaker on small datasets."),
            ("3. CLIP",
             "Train an image encoder and a text encoder jointly with "
             "contrastive loss on image-caption pairs. The result: a shared "
             "embedding space that supports zero-shot classification and "
             "image-text retrieval."),
            ("4. BLIP and BLIP-2",
             "BLIP unifies vision-language understanding and generation. "
             "BLIP-2 introduces the Q-Former, a small bridge module that "
             "lets a frozen image encoder talk to a frozen LLM. Cheap, "
             "modular, surprisingly strong."),
            ("5. Q-Former bridge",
             "A small set of learnable query tokens cross-attend to image "
             "features and output text-aligned tokens. The trainable surface "
             "is tiny relative to the frozen models."),
            ("6. Multimodal RAG",
             "Index images and text in the same vector space (CLIP-style). "
             "Retrieve across modalities. Pass both to a multimodal LLM "
             "for the final answer."),
        ],
        "papers": [
            ("An Image is Worth 16x16 Words: Vision Transformers",
             "Dosovitskiy et al., 2020 (arXiv:2010.11929)."),
            ("Learning Transferable Visual Models From Natural Language Supervision (CLIP)",
             "Radford et al., 2021 (arXiv:2103.00020)."),
            ("BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and LLMs",
             "Li et al., 2023 (arXiv:2301.12597)."),
        ],
        "labs": [
            {
                "title": "ViT vs CNN classification head to head",
                "objective": "Train a small ViT and a ResNet-18 on CIFAR-10. Compare accuracy, parameters, training time, and inference latency.",
                "prereqs": "PyTorch, CIFAR-10.",
                "steps": [
                    "Build both models from scratch (no pretrained weights).",
                    "Train for 50 epochs each with same optimizer.",
                    "Measure accuracy, params, FLOPs, latency.",
                    "Write a recommendation by dataset size.",
                ],
                "deliverables": "Comparison table and a written recommendation.",
            },
            {
                "title": "CLIP-based image-text search",
                "objective": "Build a tiny image search engine over 5000 images using CLIP. Support text-to-image and image-to-image queries.",
                "prereqs": "open_clip, an image corpus shipped with the lab.",
                "steps": [
                    "Encode all images with CLIP ViT-B/32.",
                    "Build a FAISS index on the image embeddings.",
                    "Implement text query and image query.",
                    "Evaluate on 20 hand-curated query-result pairs.",
                ],
                "deliverables": "Working CLI demo and an eval table.",
            },
            {
                "title": "BLIP-2 zero-shot visual question answering",
                "objective": "Use BLIP-2 to answer 30 questions about images zero-shot. Compare against a GPT-4V baseline.",
                "prereqs": "Lavis library, BLIP-2 checkpoint.",
                "steps": [
                    "Load BLIP-2 with Flan-T5 backbone.",
                    "Run on 30 questions and score correctness.",
                    "Compare against GPT-4V on the same 30 questions.",
                    "Analyze the failures of each.",
                ],
                "deliverables": "Eval results plus a one-page failure analysis.",
            },
        ],
    },
    {
        "num": 6,
        "date": "Saturday, July 11, 2026",
        "title": "Prompts",
        "tagline": "CO-STAR, DSPy, GEPA, TextGrad, ORPO",
        "summary": (
            "Prompts are programs. Start with hand-crafted prompting "
            "(CO-STAR, metaprompting, zero-shot vs few-shot, epistemic "
            "uncertainty). Then move to programmatic optimization with DSPy "
            "(Signatures, Modules, Optimizers) and evolutionary methods "
            "(GEPA, TextGrad, ORPO)."
        ),
        "objectives": [
            "Apply CO-STAR to structure complex production prompts",
            "Use metaprompting to have the model improve its own prompt",
            "Distinguish epistemic from aleatoric uncertainty in LLM outputs",
            "Express a task as DSPy signatures and optimize with MIPRO",
            "Run a GEPA evolutionary loop against a fixed evaluator",
        ],
        "topics": [
            ("1. CO-STAR as a checklist",
             "Context, Objective, Style, Tone, Audience, Response format. "
             "Six fields, each with one purpose. Skipping any one produces "
             "predictable failures."),
            ("2. Metaprompting",
             "Ask the model to critique and improve your prompt. Iterate. "
             "Works because the model has seen many bad prompts in training "
             "and can recognize the patterns."),
            ("3. Zero-shot vs few-shot",
             "Zero-shot is cheaper and faster. Few-shot is more controllable. "
             "Three to seven diverse examples is the practical sweet spot, "
             "with the canonical example last."),
            ("4. Epistemic uncertainty in LLM outputs",
             "When the model does not know, it sometimes hallucinates and "
             "sometimes refuses. Calibration is the practice of getting the "
             "model to refuse exactly when it does not know."),
            ("5. DSPy basics",
             "A Signature defines inputs and outputs. A Module composes "
             "signatures. An Optimizer searches over instructions and "
             "demonstrations. The Compiler freezes the result."),
            ("6. COPRO vs MIPRO",
             "COPRO does coordinate ascent on instructions. MIPRO jointly "
             "optimizes instructions and demonstrations using Bayesian "
             "search. COPRO first; MIPRO when the gain plateaus."),
            ("7. GEPA, TextGrad, ORPO",
             "GEPA: evolutionary with reflective critique. TextGrad: text "
             "as a tensor with critic-LLM gradients. ORPO: preference "
             "optimization unified with reference-free training. Each fits "
             "a different stage."),
        ],
        "papers": [
            ("DSPy: Compiling Declarative Language Model Calls into Self-Improving Pipelines",
             "Khattab et al., 2023 (arXiv:2310.03714)."),
            ("Large Language Models are Human-Level Prompt Engineers",
             "Zhou et al., 2022 (arXiv:2211.01910). The original metaprompt result."),
        ],
        "labs": [
            {
                "title": "Advanced prompting with CO-STAR and metaprompting",
                "objective": "Build a 7-class classification prompt by hand. Then use metaprompting to improve it. Compare accuracy.",
                "prereqs": "OpenAI or Anthropic API, eval set with 200 examples.",
                "steps": [
                    "Write a baseline CO-STAR prompt.",
                    "Run metaprompting for 3 rounds with explicit critique.",
                    "Compare accuracy at each round.",
                    "Identify what metaprompting changed and why.",
                ],
                "deliverables": "Three prompt versions and a comparison table.",
            },
            {
                "title": "DSPy basics and MIPRO optimization",
                "objective": "Express the same task in DSPy. Optimize with COPRO and MIPRO. Compare to the metaprompted baseline.",
                "prereqs": "DSPy installed, same eval set.",
                "steps": [
                    "Define a Signature for the task.",
                    "Build a ChainOfThought module.",
                    "Optimize with COPRO and record the result.",
                    "Optimize with MIPRO and record the result.",
                ],
                "deliverables": "Comparison table covering all four prompts.",
            },
        ],
    },
    {
        "num": 7,
        "date": "Saturday, July 18, 2026",
        "title": "Graph-Based Retrieval",
        "tagline": "RAPTOR, GraphRAG, LightRAG, and graph databases",
        "summary": (
            "Vector retrieval has a ceiling on multi-hop and structural "
            "questions. Graph-based retrieval breaks through it. Cover "
            "RAPTOR (hierarchical summary trees), GraphRAG (extract "
            "triplets, build a knowledge graph, detect communities), and "
            "LightRAG (the lean alternative). The lab implements both "
            "RAPTOR and GraphRAG on the same corpus."
        ),
        "objectives": [
            "Build a RAPTOR hierarchical summary tree over a 5K-document corpus",
            "Extract triplets, build an ontology, and run community detection for GraphRAG",
            "Compare RAPTOR, GraphRAG, and vector RAG on multi-hop questions",
            "Pick a graph database (Neo4j, Memgraph) for the target workload",
            "Understand the LightRAG simplification and where it wins",
        ],
        "topics": [
            ("1. Why graphs beat vectors on multi-hop",
             "A multi-hop question requires connecting facts that may not "
             "appear together. Vector similarity does not capture this. "
             "Graphs do, by design."),
            ("2. RAPTOR",
             "Recursively cluster and summarize the corpus into a tree. "
             "Each level summarizes its children. Retrieval traverses the "
             "tree top-down to find the right granularity."),
            ("3. GraphRAG extraction",
             "Use an LLM to extract (subject, predicate, object) triplets "
             "from each document. Deduplicate entities. Build a graph in "
             "Neo4j or similar."),
            ("4. Ontologies and entity resolution",
             "Define entity types and relationship types up front for "
             "consistency. Resolve aliases (Apple Inc., AAPL, the iPhone "
             "company) to canonical entities."),
            ("5. Community detection",
             "Run Leiden or Louvain on the graph. Summarize each community. "
             "At query time, retrieve relevant communities and pass their "
             "summaries to the LLM."),
            ("6. Graph databases",
             "Neo4j is the mature default. Memgraph is in-memory and "
             "faster for read-heavy workloads. ArangoDB combines "
             "document and graph models."),
            ("7. LightRAG",
             "Skip the community detection. Use dual-level retrieval: "
             "local (entity neighborhood) and global (graph-wide). Simpler, "
             "competitive on many tasks."),
        ],
        "papers": [
            ("RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval",
             "Sarthi et al., 2024 (arXiv:2401.18059)."),
            ("From Local to Global: A Graph RAG Approach to Query-Focused Summarization",
             "Edge et al., 2024 (arXiv:2404.16130). The Microsoft GraphRAG paper."),
            ("LightRAG: Simple and Fast Retrieval-Augmented Generation",
             "Guo et al., 2024 (arXiv:2410.05779)."),
        ],
        "labs": [
            {
                "title": "RAPTOR over the bootcamp corpus",
                "objective": "Build a RAPTOR tree over a 5K-document corpus. Compare to flat vector RAG on a 50-question multi-hop set.",
                "prereqs": "The reference RAPTOR library.",
                "steps": [
                    "Embed all chunks.",
                    "Cluster and summarize recursively (3 levels).",
                    "Index the full tree.",
                    "Run the eval set and compare to flat RAG.",
                ],
                "deliverables": "Tree visualization, eval comparison, and a one-page reflection.",
            },
            {
                "title": "GraphRAG and LightRAG comparison",
                "objective": "Build a GraphRAG and a LightRAG pipeline on the same corpus. Compare on multi-hop questions, cost, and build time.",
                "prereqs": "Neo4j or Memgraph, GraphRAG reference impl, LightRAG.",
                "steps": [
                    "Run triplet extraction on the corpus.",
                    "Build the GraphRAG graph and run community detection.",
                    "Build the LightRAG pipeline.",
                    "Evaluate both on 50 multi-hop questions.",
                ],
                "deliverables": "Build-time comparison, eval results, and a writeup on when each wins.",
            },
        ],
    },
    {
        "num": 8,
        "date": "Saturday, July 25, 2026",
        "title": "Overcoming RAG Challenges",
        "tagline": "Guardrails, grounding, NLI verification, P95 latency",
        "summary": (
            "RAG in production hits real walls: hallucinations, prompt "
            "injection, PII leakage, latency. Today covers guardrail "
            "pipelines (syntax, PII, toxicity, intent), adversarial threats, "
            "grounding via NLI verification, and the P95 latency budget. The "
            "lab builds a guardrail pipeline and an NLI-based grounding "
            "checker."
        ),
        "objectives": [
            "Build a guardrail pipeline with syntax, PII, toxicity, and intent stages",
            "Defend against prompt injection at each layer of the system",
            "Verify answers against retrieved evidence using an NLI model",
            "Hit a P95 latency target while keeping all guardrails enabled",
            "Detect and quantify hallucination rate in production",
        ],
        "topics": [
            ("1. The guardrail pipeline",
             "Four stages, ordered cheap to expensive: syntax (well-formed "
             "JSON), PII detection, toxicity scoring, intent classification. "
             "Each stage can refuse independently."),
            ("2. PII handling",
             "Detect PII in inputs and outputs. Redact in logs and traces. "
             "Use scoped retention policies. Different jurisdictions have "
             "different rules; build for the strictest."),
            ("3. Prompt injection",
             "Treat retrieved content as untrusted data. Use system-prompt "
             "delimiters that fetched text cannot reproduce. Strip "
             "instruction-like patterns from retrievals."),
            ("4. NLI verification",
             "After generation, run the (answer, evidence) pair through a "
             "natural language inference model. Entailment = grounded. "
             "Contradiction = block. Neutral = flag for review."),
            ("5. Grounding frameworks",
             "Train the model to cite which retrieved passage supports "
             "each claim. Verify at inference. Reject answers that fail "
             "verification."),
            ("6. P95 latency",
             "Means lie about user experience. P95 is what users feel. "
             "Budget every stage of the pipeline; nothing exceeds its "
             "allotment without explicit justification."),
            ("7. Hallucination detection in production",
             "Sample 1% of traffic for offline grounding verification. "
             "Alert when the hallucination rate drifts above baseline."),
        ],
        "papers": [
            ("RAGAS: Automated Evaluation of Retrieval Augmented Generation",
             "Es et al., 2023 (arXiv:2309.15217)."),
            ("Constitutional AI: Harmlessness from AI Feedback",
             "Bai et al., 2022 (arXiv:2212.08073). Relevant for guardrail design."),
        ],
        "labs": [
            {
                "title": "Four-stage guardrail pipeline",
                "objective": "Build a pipeline with syntax, PII, toxicity, and intent stages. Measure throughput and false-positive rates.",
                "prereqs": "Presidio (PII), Perspective API or a toxicity model, intent classifier.",
                "steps": [
                    "Implement each stage with a clean refuse-or-pass interface.",
                    "Chain them with early-exit semantics.",
                    "Run on 1000 sample inputs.",
                    "Tune thresholds against a labeled test set.",
                ],
                "deliverables": "Pipeline source, throughput chart, FP/FN breakdown.",
            },
            {
                "title": "NLI-based response grounding",
                "objective": "Implement an NLI verifier that scores answer grounding against the retrieved context.",
                "prereqs": "An NLI model (DeBERTa-large-mnli or similar).",
                "steps": [
                    "Split answers into claims using an LLM.",
                    "Score each claim against the retrieved context.",
                    "Reject answers below a threshold.",
                    "Evaluate on 100 (question, answer, evidence) triples.",
                ],
                "deliverables": "Grounding scores, false-negative analysis, and a tuning recommendation.",
            },
        ],
    },
    {
        "num": 9,
        "date": "Saturday, August 1, 2026",
        "title": "Towards Enterprise RAG",
        "tagline": "Derivative artifacts, query transformation, semantic cache",
        "summary": (
            "Enterprise RAG goes beyond chunk-and-retrieve. Cover derivative "
            "artifacts (factoids, QA pairs) that enrich the index; query "
            "transformation with HyDE and multi-hop decomposition; semantic "
            "caching for cost control; hard negative mining for embedding "
            "fine-tuning. The lab builds three of these and measures the "
            "cumulative effect."
        ),
        "objectives": [
            "Generate factoids and QA pairs from a corpus to enrich retrieval",
            "Apply HyDE and query decomposition for harder questions",
            "Build a semantic cache that cuts inference cost by at least 30%",
            "Mine hard negatives and fine-tune an embedder",
            "Quantify the cumulative effect of these techniques",
        ],
        "topics": [
            ("1. Derivative artifacts: factoids and QA pairs",
             "Use an LLM to extract short factoids from each document. Also "
             "generate plausible QA pairs. Index both alongside the raw "
             "chunks. Retrieval improves on questions that match the "
             "generated artifacts better than the raw text."),
            ("2. Query transformation: HyDE",
             "Hypothetical Document Embeddings. Generate a plausible answer "
             "first; embed that; retrieve against the result. Closes the "
             "query-document distribution gap. One extra LLM call per query."),
            ("3. Multi-hop decomposition",
             "Hard questions need multiple retrievals. A planner emits "
             "sub-queries. Each sub-query retrieves; partial answers inform "
             "the next sub-query."),
            ("4. Semantic caching",
             "Cache answers by query embedding similarity, not exact match. "
             "Typical hit rate: 20% to 40% on production traffic. Cost "
             "savings compound with traffic."),
            ("5. Hard negative mining",
             "Find documents that look similar to positives but are wrong. "
             "Train the embedder to push them apart. Single biggest "
             "embedding improvement after the base model."),
            ("6. Embedding fine-tuning at enterprise scale",
             "Pull in-domain queries from logs (with consent). Mine hard "
             "negatives. Fine-tune with InfoNCE. Re-index. Repeat quarterly."),
        ],
        "papers": [
            ("Precise Zero-Shot Dense Retrieval without Relevance Labels",
             "Gao et al., 2022 (arXiv:2212.10496). The HyDE paper."),
            ("MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries",
             "Tang and Yang, 2024 (arXiv:2401.15391)."),
        ],
        "labs": [
            {
                "title": "Derivative artifacts and query transformation",
                "objective": "Generate factoids and QA pairs for a 1000-document corpus. Add HyDE to retrieval. Measure cumulative effect on recall.",
                "prereqs": "An LLM API plus the embeddings stack from prior weeks.",
                "steps": [
                    "Generate 5 factoids per document with an LLM.",
                    "Generate 3 QA pairs per document.",
                    "Re-index with the enriched corpus.",
                    "Add HyDE on the query side.",
                    "Measure recall@5 before and after.",
                ],
                "deliverables": "Recall comparison plus a cost-per-query analysis.",
            },
            {
                "title": "Semantic cache layer",
                "objective": "Build a semantic cache that caches answers by embedding similarity. Measure hit rate and cost savings on a synthetic 1000-query stream.",
                "prereqs": "A small vector store for the cache, the RAG pipeline.",
                "steps": [
                    "Implement cache lookup with a similarity threshold.",
                    "Implement cache write on each miss.",
                    "Run a synthetic query stream with 30% duplicate intent.",
                    "Measure hit rate, latency, and cost.",
                ],
                "deliverables": "Cache implementation, threshold tuning analysis, and savings report.",
            },
        ],
    },
    {
        "num": 10,
        "date": "Saturday, August 8, 2026",
        "title": "Agentic RAG and Text2SQL",
        "tagline": "Agent lifecycles, MCP, and SQL generation in production",
        "summary": (
            "Two related topics. First: agentic RAG. The agent decides what "
            "to retrieve, when to retrieve, and when to stop. Cover the "
            "agent lifecycle, MCP for tool integration, and specialization "
            "patterns. Second: Text-to-SQL. Cover schema uncertainty, CTE "
            "libraries, and reinforcement learning in SQL generation."
        ),
        "objectives": [
            "Implement an agentic RAG that beats static RAG on multi-hop questions",
            "Use MCP to expose tools cleanly to the agent",
            "Build a Text-to-SQL system with schema uncertainty handling",
            "Apply a CTE library to reduce SQL complexity",
            "Reason about when RL helps SQL generation and when it does not",
        ],
        "topics": [
            ("1. The agentic lifecycle",
             "Perceive the user's question. Plan the retrieval. Act (call "
             "tools). Observe. Decide whether to continue or answer. The "
             "loop has a defined termination condition."),
            ("2. Model Context Protocol (MCP)",
             "A clean abstraction for exposing tools to agents. Tool "
             "servers, JSON schemas, capability negotiation. The right "
             "default for new tool integrations."),
            ("3. Agent specialization patterns",
             "Generalist with many tools. Specialist per domain. Router "
             "that picks among specialists. Each pattern has a sweet "
             "spot in cost and quality."),
            ("4. Text-to-SQL architecture",
             "Schema understanding, query planning, SQL generation, "
             "verification, execution. Each stage can fail differently; "
             "design checkpoints to isolate failures."),
            ("5. Schema uncertainty",
             "Production schemas have hundreds of tables. The model cannot "
             "see all of them. Retrieve relevant tables first; pass only "
             "those to the SQL generator."),
            ("6. CTE libraries",
             "Pre-built Common Table Expressions for recurring patterns "
             "(date ranges, customer segments, revenue calculations). "
             "Reduces SQL complexity; the model composes from a known set."),
            ("7. RL for SQL generation",
             "Reward = SQL executes + matches expected rows. RLVR fits "
             "naturally. Most gains come from base SFT; RL adds the last "
             "5 to 15 percentage points."),
        ],
        "papers": [
            ("Spider: A Large-Scale Human-Labeled Dataset for Complex SQL",
             "Yu et al., 2018 (arXiv:1809.08887)."),
            ("DIN-SQL: Decomposed In-Context Learning of Text-to-SQL",
             "Pourreza and Rafiei, 2023 (arXiv:2304.11015)."),
        ],
        "labs": [
            {
                "title": "Semantic cache plus agentic RAG",
                "objective": "Layer semantic caching under an agentic RAG. Measure cache hit rate and end-to-end cost on a 200-question test.",
                "prereqs": "Cache from week 9, basic agent loop.",
                "steps": [
                    "Wrap the agent's retrieval calls with the cache.",
                    "Run 200 questions with 25% repeat intent.",
                    "Compare cost and latency to agentic-without-cache.",
                ],
                "deliverables": "Comparison table and a writeup on cache-agent interaction edge cases.",
            },
            {
                "title": "ADK, MCP, and A2A condensed",
                "objective": "Build a Text-to-SQL agent using Google ADK with MCP for tool exposure. Add an A2A endpoint for cross-team consumption.",
                "prereqs": "Google ADK, FastMCP, sample database.",
                "steps": [
                    "Build the SQL agent in ADK with three tools (list_tables, get_schema, run_query).",
                    "Expose the tools via FastMCP.",
                    "Wrap the agent with an A2A endpoint.",
                    "Test end-to-end with three external callers.",
                ],
                "deliverables": "Working source, sample call traces, and a one-page architecture diagram.",
            },
        ],
    },
    {
        "num": 11,
        "date": "Saturday, August 15, 2026",
        "title": "Fine-Tuning",
        "tagline": "Chinchilla, PEFT/LoRA, RLHF, and RL with verifiable rewards",
        "summary": (
            "The fine-tuning week. Cover Chinchilla scaling for sizing "
            "decisions. PEFT with LoRA and qLoRA. The full RLHF pipeline "
            "(SFT, reward model, PPO). RL with verifiable rewards (RLVR) "
            "for tasks where the reward can be checked programmatically. "
            "The lab pair runs Text-to-SQL fine-tuning and a basic TRL "
            "GRPO experiment."
        ),
        "objectives": [
            "Apply Chinchilla scaling to estimate the right model size for a token budget",
            "Configure LoRA with appropriate rank, alpha, and target modules",
            "Walk the full RLHF pipeline: SFT, reward model, PPO",
            "Use RLVR for tasks with programmatically checkable correctness",
            "Run a basic GRPO loop with TRL on a small base model",
        ],
        "topics": [
            ("1. Chinchilla scaling",
             "For a fixed compute budget, optimal model size and tokens "
             "scale together at roughly 20 tokens per parameter. Knowing "
             "your token budget tells you the right model size. "
             "Over-trained smaller models often beat under-trained larger."),
            ("2. PEFT and LoRA",
             "Freeze the base. Adapt with a low-rank update BA. Train only "
             "BA. Recover near-full-precision performance on most "
             "downstream tasks at 0.5% to 2% of trainable parameters."),
            ("3. qLoRA",
             "Quantize the base to 4-bit. Train LoRA in 16-bit. Memory "
             "drops 4x. Accuracy stays within 1-2 points on most tasks."),
            ("4. The RLHF pipeline",
             "SFT on demonstrations. Train a reward model on preferences. "
             "PPO against the reward model with KL penalty to a reference. "
             "Three stages, each with its own failure modes."),
            ("5. RL with verifiable rewards (RLVR)",
             "When correctness can be checked programmatically (unit tests, "
             "SQL execution, theorem checker), skip the reward model. The "
             "verifier becomes the reward."),
            ("6. GRPO",
             "Group Relative Policy Optimization. Sample N completions per "
             "prompt; use relative advantage. Drops the value head, halves "
             "memory, matches PPO on many tasks."),
            ("7. Evaluating fine-tuned models",
             "Held-out eval for the target task. Regression suite for base "
             "capabilities. Drift checks over time. Explicit harm tests."),
        ],
        "papers": [
            ("Training Compute-Optimal Large Language Models",
             "Hoffmann et al., 2022 (arXiv:2203.15556). The Chinchilla paper."),
            ("LoRA: Low-Rank Adaptation of Large Language Models",
             "Hu et al., 2021 (arXiv:2106.09685)."),
            ("DeepSeekMath: Pushing the Limits of Mathematical Reasoning in Open Language Models",
             "Shao et al., 2024 (arXiv:2402.03300). Introduces GRPO."),
        ],
        "labs": [
            {
                "title": "Text2SQL fine-tuning on Spider",
                "objective": "Fine-tune a small base model on the Spider dataset with LoRA. Compare to a few-shot baseline.",
                "prereqs": "TRL, PEFT, Spider dataset.",
                "steps": [
                    "Build the few-shot baseline.",
                    "Fine-tune with LoRA (rank 16) for 3 epochs.",
                    "Evaluate exact match and execution accuracy.",
                    "Compare to the baseline.",
                ],
                "deliverables": "Eval comparison, training curve, and a recommendation.",
            },
            {
                "title": "Basic TRL GRPO loop",
                "objective": "Set up a minimal GRPO training run on a small base model with an executable reward.",
                "prereqs": "TRL with GRPO support, simple verifier (string match).",
                "steps": [
                    "Define the prompt set and the verifier.",
                    "Configure GRPO with group size 8.",
                    "Train for 200 steps.",
                    "Compare against the SFT baseline.",
                ],
                "deliverables": "Training curve, eval delta, and a one-page reflection on stability.",
            },
        ],
    },
    {
        "num": 12,
        "date": "Saturday, August 22, 2026",
        "title": "Evals",
        "tagline": "Retrieval metrics, Ragas, LLM-as-judge, and verification asymmetry",
        "summary": (
            "Evaluation week. Cover retrieval metrics (Precision@k, "
            "Recall@k, MRR, MAP, NDCG). Ragas for end-to-end RAG metrics "
            "(faithfulness, answer relevance, context precision/recall). "
            "LLM-as-a-judge: when it works, when it does not. The RGB "
            "benchmark for robustness. Verification asymmetry as the core "
            "principle behind good eval design."
        ),
        "objectives": [
            "Compute and interpret Precision@k, Recall@k, MRR, MAP, and NDCG correctly",
            "Run Ragas on a RAG pipeline and interpret each metric",
            "Use LLM-as-a-judge while controlling for known biases",
            "Apply the RGB benchmark to test robustness against noise",
            "Design an eval where verification is cheaper than generation",
        ],
        "topics": [
            ("1. Retrieval metrics",
             "Precision@k: how many of the top k are relevant. Recall@k: "
             "what fraction of all relevant were retrieved. MRR: rank of "
             "the first relevant. MAP: averaged precision across queries. "
             "NDCG: graded relevance with rank discount. Pick the metric "
             "that matches the downstream use."),
            ("2. Ragas for end-to-end RAG",
             "Four metrics: faithfulness (answer grounded in context), "
             "answer relevance (answer addresses the question), context "
             "precision (retrieved context is relevant), context recall "
             "(retrieved context covers what is needed)."),
            ("3. LLM-as-a-judge",
             "Use a separate strong model to judge answer quality. Cheap "
             "and scalable. Beware: position bias (first answer wins), "
             "verbosity bias (longer is judged better), and self-preference "
             "bias (model prefers its own outputs)."),
            ("4. The RGB benchmark",
             "Tests retrieval robustness against noise, negative passages, "
             "information integration, and counterfactual robustness. A "
             "real RAG should hold up against all four."),
            ("5. Verification asymmetry",
             "When verification is cheaper than generation, you can score "
             "many candidates with a verifier and pick the best. This is "
             "the foundation of self-consistency, best-of-N, and RLVR."),
            ("6. Building an eval that does not lie",
             "Held-out test set. Stable scoring rubric. Multiple judges "
             "or a single judge with calibration. Reproducible seed. "
             "Publish the variance, not just the mean."),
        ],
        "papers": [
            ("RAGAS: Automated Evaluation of Retrieval Augmented Generation",
             "Es et al., 2023 (arXiv:2309.15217)."),
            ("Benchmarking Large Language Models in Retrieval-Augmented Generation",
             "Chen et al., 2023 (arXiv:2309.01431). The RGB benchmark paper."),
            ("Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena",
             "Zheng et al., 2023 (arXiv:2306.05685)."),
        ],
        "labs": [
            {
                "title": "Unsloth walkthrough for fast fine-tuning",
                "objective": "Use Unsloth to fine-tune a 7B model with LoRA in under 30 minutes on a single GPU. Compare to vanilla TRL.",
                "prereqs": "Unsloth installed, small instruction dataset.",
                "steps": [
                    "Configure Unsloth with the recommended defaults.",
                    "Fine-tune for 1 epoch.",
                    "Measure wallclock time and peak GPU memory.",
                    "Evaluate on a held-out set.",
                ],
                "deliverables": "Speedup numbers, eval delta, and a recommendation.",
            },
            {
                "title": "Full RAG eval suite",
                "objective": "Run Ragas on the RAG pipeline you built this week. Add LLM-as-a-judge for answer quality. Add an RGB-style robustness test.",
                "prereqs": "Ragas, your RAG pipeline, a judge model.",
                "steps": [
                    "Configure Ragas with the four core metrics.",
                    "Add LLM-as-a-judge with explicit prompt to control verbosity bias.",
                    "Inject noise and counterfactual passages for RGB-style tests.",
                    "Report all results with confidence intervals.",
                ],
                "deliverables": "Eval report with the full metric table and a writeup on the biggest weakness found.",
            },
        ],
    },
]


def slug(week):
    t = week["title"].lower()
    out = []
    for c in t:
        if c.isalnum():
            out.append(c)
        elif c in " -_":
            out.append("_")
    return "".join(out).strip("_")
