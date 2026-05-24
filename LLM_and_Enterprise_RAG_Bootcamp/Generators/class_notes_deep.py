"""Deep technical content per week for RAG bootcamp class notes."""

DEEP = {
    1: {
        "intro": (
            "Day one opens the bootcamp. The work for the next twelve weeks "
            "rests on a few foundational ideas: what an embedding actually "
            "is, why transformers won the architecture race, and what makes "
            "vector search practical at scale. We cover those today, then "
            "build a working RAG before the day ends."
        ),
        "sections": [
            {
                "h": "1. From keyword search to semantic understanding",
                "body": (
                    "BM25 has been the IR baseline since the 1980s. It is "
                    "still strong. The case for semantic search is not that "
                    "BM25 is bad; it is that BM25 cannot match meaning when "
                    "the surface form differs. A user asking about "
                    "'cardiac arrest' is not helped by an article that uses "
                    "'heart attack' throughout. Dense retrieval closes that "
                    "gap."
                ),
            },
            {
                "h": "2. Self-attention in one screen",
                "body": (
                    "For each token, compute three vectors: query Q, key K, "
                    "value V. Attention weights are softmax(Q K^T / sqrt(d)). "
                    "The output is the weighted sum of value vectors. The "
                    "sqrt(d) scaling keeps softmax in a usable range as "
                    "dimension grows. Multi-head attention runs this "
                    "computation h times in parallel and concatenates."
                ),
                "code": (
                    "import torch.nn.functional as F\n"
                    "import math\n\n"
                    "def attention(Q, K, V, mask=None):\n"
                    "    d = Q.size(-1)\n"
                    "    scores = Q @ K.transpose(-2, -1) / math.sqrt(d)\n"
                    "    if mask is not None:\n"
                    "        scores = scores.masked_fill(mask == 0, -1e9)\n"
                    "    weights = F.softmax(scores, dim=-1)\n"
                    "    return weights @ V\n"
                ),
            },
            {
                "h": "3. Encoder, decoder, encoder-decoder",
                "body": (
                    "Encoders (BERT) read in both directions and produce "
                    "rich token representations. They are good for "
                    "classification and embeddings. Decoders (GPT) read "
                    "left to right and predict the next token. They are "
                    "good for generation. Encoder-decoder models (T5) do "
                    "both. The right choice depends on the task, not the "
                    "popularity of the model."
                ),
            },
            {
                "h": "4. Embeddings as universal currency",
                "body": (
                    "An embedding is a point in a high-dimensional space "
                    "where geometric relationships approximate semantic "
                    "ones. Cosine similarity becomes meaning similarity. "
                    "Clustering becomes topic grouping. Classifiers become "
                    "shallow heads on top. The training objective shapes "
                    "the geometry; that fact will matter throughout the "
                    "course."
                ),
            },
            {
                "h": "5. ANN search at a working level",
                "body": (
                    "Brute-force similarity search is O(n) per query. For "
                    "a million vectors at 768 dimensions, that is roughly "
                    "750 MB of data to scan per query. ANN trades a small "
                    "amount of recall for orders of magnitude speedup. "
                    "HNSW is the default for moderate scale; IVF for "
                    "memory pressure; product quantization for both at "
                    "billion scale."
                ),
            },
            {
                "h": "6. The five numbers for a vector database",
                "body": (
                    "Index build time. RAM footprint. Recall at k. Query "
                    "throughput. Update cost. Benchmark all five on your "
                    "data before committing. Marketing pages list peak "
                    "throughput; real workloads sit at percentiles."
                ),
            },
        ],
        "review": [
            "Name a query type where BM25 still beats dense retrieval.",
            "Why does the sqrt(d) scaling in attention matter?",
            "Pick a task and choose between encoder, decoder, and encoder-decoder.",
            "When is ANN unacceptable and exact search required?",
        ],
    },
    2: {
        "intro": (
            "High-dimensional space is genuinely strange. Today we cover the "
            "geometry, then anchor it with BERT-style masked language "
            "modeling and contrastive learning. By the end you will have "
            "an intuition for anisotropy, temperature, and InfoNCE."
        ),
        "sections": [
            {
                "h": "1. Three strange properties of high-D space",
                "body": (
                    "First: almost all volume of a unit ball lies near its "
                    "surface (concentration of measure). Second: two random "
                    "vectors in high dimensions are almost orthogonal. "
                    "Third: distances concentrate, so the ratio of "
                    "max-to-min distance approaches 1. These facts mean "
                    "naive intuitions from 3D space mislead in 768D."
                ),
            },
            {
                "h": "2. BERT and masked language modeling",
                "body": (
                    "Mask 15% of tokens at random. Train the model to "
                    "predict the masked tokens from bidirectional context. "
                    "This forces the model to learn rich contextual "
                    "representations. The resulting embeddings transfer "
                    "well to sentence-level tasks like classification and "
                    "similarity."
                ),
            },
            {
                "h": "3. Anisotropy: the BERT problem",
                "body": (
                    "Plain BERT embeddings cluster in a narrow cone in "
                    "embedding space. Average pairwise cosine similarity "
                    "is high across unrelated sentences. This inflates "
                    "similarity scores uniformly and reduces "
                    "discriminative power. Whitening or contrastive "
                    "fine-tuning corrects it."
                ),
                "code": (
                    "import numpy as np\n\n"
                    "def whitening(E):\n"
                    "    mu = E.mean(0, keepdims=True)\n"
                    "    cov = (E - mu).T @ (E - mu) / len(E)\n"
                    "    u, s, _ = np.linalg.svd(cov)\n"
                    "    W = u @ np.diag(1.0 / np.sqrt(s + 1e-8))\n"
                    "    return (E - mu) @ W\n"
                ),
            },
            {
                "h": "4. Temperature and contrastive loss",
                "body": (
                    "Temperature controls the sharpness of the softmax in "
                    "contrastive losses. Low temperature makes negatives "
                    "feel harder (sharp distribution; only the closest "
                    "negative matters). High temperature flattens, smoothing "
                    "the signal. Production defaults sit between 0.05 and "
                    "0.2 for InfoNCE."
                ),
            },
            {
                "h": "5. InfoNCE from scratch",
                "body": (
                    "Given anchor a, positive p, and a batch of negatives, "
                    "compute logits = a @ all.T / temperature. Apply "
                    "cross-entropy with the positive index as label. The "
                    "loss pushes the anchor toward the positive and away "
                    "from negatives in one operation."
                ),
                "code": (
                    "import torch.nn.functional as F\n\n"
                    "def info_nce(anchors, positives, temperature=0.1):\n"
                    "    logits = anchors @ positives.T / temperature\n"
                    "    labels = torch.arange(len(anchors), device=logits.device)\n"
                    "    return F.cross_entropy(logits, labels)\n"
                ),
            },
            {
                "h": "6. Semantic search end to end",
                "body": (
                    "Embed the query. Search the index. Score with cosine "
                    "or inner product. Return top k. The latency budget "
                    "(typically 50-200 ms for the retrieval step) shapes "
                    "every other choice: index type, dimension, candidate "
                    "count."
                ),
            },
        ],
        "review": [
            "Why does cosine similarity 0.8 between random sentences mean less in BERT than in a contrastive model?",
            "Pick a temperature for InfoNCE and justify.",
            "When is whitening a better fix than fine-tuning?",
            "Sketch the latency budget for a 200 ms retrieval step.",
        ],
    },
    3: {
        "intro": (
            "Chunking is the quiet make-or-break of RAG. Too small and the "
            "model loses context; too large and the relevance signal "
            "dilutes. Today we cover four chunking strategies and "
            "hierarchical retrieval. The choice depends on your corpus and "
            "your downstream answer shape."
        ),
        "sections": [
            {
                "h": "1. The precision-context tradeoff",
                "body": (
                    "Small chunks (under 200 tokens) give precise hits and "
                    "high relevance scores but lose surrounding context. "
                    "Large chunks (1000+ tokens) preserve context but "
                    "dilute the relevance score and may push out other "
                    "useful chunks from the top-k. The sweet spot is "
                    "corpus-specific and downstream-specific."
                ),
            },
            {
                "h": "2. Fixed-size chunking",
                "body": (
                    "Split on token count with overlap (typically 10-20%). "
                    "Cheap. Predictable. Ignores natural boundaries. Often "
                    "good enough for homogeneous corpora; bad for "
                    "heterogeneous ones where document structure matters."
                ),
            },
            {
                "h": "3. Semantic chunking",
                "body": (
                    "Embed each sentence. Split where adjacent sentence "
                    "similarity drops below a threshold. Respects natural "
                    "topic boundaries. More expensive than fixed-size but "
                    "produces more coherent chunks."
                ),
            },
            {
                "h": "4. Late chunking",
                "body": (
                    "Embed the entire document first, then split the "
                    "resulting token-level embeddings into chunks. Each "
                    "chunk's embedding still reflects the full document "
                    "context. Works only with embedders that support long "
                    "contexts (Jina v3, bge-m3)."
                ),
                "code": (
                    "def late_chunking(text, model, chunk_size=256):\n"
                    "    token_embeddings = model.encode_tokens(text)\n"
                    "    chunks = []\n"
                    "    for i in range(0, len(token_embeddings), chunk_size):\n"
                    "        chunk_emb = token_embeddings[i:i+chunk_size].mean(0)\n"
                    "        chunks.append(chunk_emb)\n"
                    "    return chunks\n"
                ),
            },
            {
                "h": "5. Contextual chunking",
                "body": (
                    "Before embedding each chunk, prepend a short LLM-"
                    "generated summary of the surrounding context. "
                    "Anthropic reported a 35% retrieval improvement on "
                    "average. The cost is one LLM call per chunk at "
                    "ingestion time."
                ),
            },
            {
                "h": "6. Hierarchical retrieval",
                "body": (
                    "Embed at two granularities: small child chunks (250 "
                    "tokens) for matching, large mother chunks (1000 "
                    "tokens) for context. Match against children; return "
                    "the parent mother chunk to the LLM. Best of both "
                    "worlds, modest extra storage."
                ),
            },
        ],
        "review": [
            "Pick a corpus type where contextual chunking is worth the cost.",
            "When does late chunking fail to help?",
            "Sketch a hierarchical retrieval flow for a medical knowledge base.",
            "What latency does each chunking strategy add at ingestion?",
        ],
    },
    4: {
        "intro": (
            "Production retrieval is a funnel: many cheap candidates in, "
            "few well-scored results out. Today we build it: sparse + "
            "dense first stage, Matryoshka pruning, ColBERT late "
            "interaction, cross-encoder fusion at the top."
        ),
        "sections": [
            {
                "h": "1. Sparse retrieval still matters",
                "body": (
                    "BM25 finds exact and rare term matches that dense "
                    "models miss. SPLADE adds neural query and document "
                    "expansion while preserving BM25's efficient inverted "
                    "index. In production, hybrid (sparse + dense) almost "
                    "always beats either alone."
                ),
            },
            {
                "h": "2. Dense retrieval realities",
                "body": (
                    "Bi-encoders independently encode query and documents. "
                    "Cosine similarity at query time. Cheap, fast, "
                    "scales. Weak on rare terms, named entities, and "
                    "domain-specific abbreviations until fine-tuned."
                ),
            },
            {
                "h": "3. Reciprocal rank fusion",
                "body": (
                    "Combine multiple rankings by summing 1/(k + rank). "
                    "Parameter-light, robust, and the simplest way to "
                    "fuse sparse and dense rankings."
                ),
                "code": (
                    "def rrf(rankings, k=60):\n"
                    "    scores = {}\n"
                    "    for ranking in rankings:\n"
                    "        for rank, doc in enumerate(ranking):\n"
                    "            scores[doc] = scores.get(doc, 0) + 1.0/(k + rank)\n"
                    "    return sorted(scores.items(), key=lambda x: -x[1])\n"
                ),
            },
            {
                "h": "4. Matryoshka Representation Learning",
                "body": (
                    "Train embeddings that work at multiple truncation "
                    "lengths. A 768-dim embedding also functions as a "
                    "useful 64-dim embedding for cheap pruning. Use the "
                    "short truncation to filter, the full length to score."
                ),
            },
            {
                "h": "5. ColBERT late interaction",
                "body": (
                    "Score by sum of maximum query-token-to-doc-token "
                    "similarities. More expressive than single-vector "
                    "bi-encoders, far cheaper than cross-encoders. The "
                    "PLAID engine makes it fast enough for production."
                ),
            },
            {
                "h": "6. Cross-encoder fusion",
                "body": (
                    "Encode the (query, doc) pair jointly with full "
                    "attention. Most accurate, most expensive. Reserve "
                    "for the final 20-100 candidates."
                ),
            },
            {
                "h": "7. The four-stage funnel",
                "body": (
                    "Stage 1: sparse + dense in parallel, 200 candidates "
                    "each. Stage 2: Matryoshka prune to 100. Stage 3: "
                    "ColBERT score to 30. Stage 4: cross-encoder rerank "
                    "to top 5. Tune candidate counts per stage on your "
                    "data."
                ),
            },
        ],
        "review": [
            "Pick a query type where BM25 must be in the funnel.",
            "Why does RRF beat weighted-sum fusion in many cases?",
            "What is the marginal benefit of ColBERT given a strong cross-encoder?",
            "When can you drop the Matryoshka stage?",
        ],
    },
    5: {
        "intro": (
            "Multimodal week. We walk from CNNs through Vision Transformers, "
            "then into CLIP and BLIP. By the end you will be adding image "
            "modalities to a RAG system and reasoning about cross-modal "
            "retrieval honestly."
        ),
        "sections": [
            {
                "h": "1. CNN foundations in one screen",
                "body": (
                    "Convolutional filters detect local patterns. Pooling "
                    "reduces spatial dimensions. Stacking layers builds "
                    "feature hierarchy: edges, textures, parts, objects. "
                    "ResNet's residual connections enabled training of very "
                    "deep networks."
                ),
            },
            {
                "h": "2. Vision Transformers",
                "body": (
                    "Split image into 16x16 patches. Linearly project each "
                    "patch to a token embedding. Add a learnable [CLS] "
                    "token. Run standard transformer layers. Excellent at "
                    "scale; weaker than CNNs on small datasets due to "
                    "weaker inductive bias."
                ),
            },
            {
                "h": "3. CLIP",
                "body": (
                    "Train image encoder and text encoder jointly with "
                    "contrastive loss on 400M image-caption pairs. The "
                    "result: shared embedding space supporting zero-shot "
                    "classification (compare image embedding to text "
                    "embeddings of candidate labels) and cross-modal "
                    "retrieval."
                ),
                "code": (
                    "import open_clip\n\n"
                    "model, _, preprocess = open_clip.create_model_and_transforms(\n"
                    "    'ViT-B-32', pretrained='laion2b_s34b_b79k')\n"
                    "tokenizer = open_clip.get_tokenizer('ViT-B-32')\n\n"
                    "img_emb = model.encode_image(preprocess(img).unsqueeze(0))\n"
                    "txt_emb = model.encode_text(tokenizer(['a cat']))\n"
                    "sim = (img_emb @ txt_emb.T).softmax(dim=-1)\n"
                ),
            },
            {
                "h": "4. BLIP and BLIP-2",
                "body": (
                    "BLIP unifies vision-language understanding and "
                    "generation. BLIP-2 introduces the Q-Former: a small "
                    "bridge module with learnable query tokens that "
                    "cross-attend to image features and output text-"
                    "aligned tokens. Lets a frozen image encoder talk to "
                    "a frozen LLM. Tiny trainable surface."
                ),
            },
            {
                "h": "5. Zero-shot visual reasoning",
                "body": (
                    "BLIP-2 with a Flan-T5 backbone answers visual "
                    "questions reasonably well zero-shot. Limits: counts, "
                    "spatial reasoning beyond simple left/right, and any "
                    "task requiring fine-grained text reading."
                ),
            },
            {
                "h": "6. Multimodal RAG",
                "body": (
                    "Two patterns. One: index images and text in a shared "
                    "CLIP space; retrieve across modalities; pass to a "
                    "multimodal LLM. Two: convert images to descriptive "
                    "text at ingestion; index text only. Pick based on "
                    "query distribution."
                ),
            },
        ],
        "review": [
            "Pick a task where CNNs still beat ViTs in 2026.",
            "When is BLIP-2's Q-Former the right architecture choice?",
            "Compare the two multimodal RAG patterns on cost and quality.",
            "Why does CLIP struggle on fine-grained text reading in images?",
        ],
    },
    6: {
        "intro": (
            "Prompts week. Start with hand-crafted prompting (CO-STAR, "
            "metaprompting, few-shot patterns) and the calibration of "
            "epistemic uncertainty. Then move to programmatic optimization "
            "with DSPy and the newer evolutionary methods."
        ),
        "sections": [
            {
                "h": "1. CO-STAR as a checklist",
                "body": (
                    "Context, Objective, Style, Tone, Audience, Response "
                    "format. Six fields. Each has one purpose. Skipping "
                    "any one produces predictable failures: missing "
                    "context gives wrong answers; missing format gives "
                    "unparseable outputs."
                ),
            },
            {
                "h": "2. Metaprompting",
                "body": (
                    "Ask the model to critique and improve your prompt. "
                    "Iterate. Works because the model has seen many bad "
                    "prompts in training and can recognize patterns. A "
                    "single round of metaprompting often beats a week of "
                    "human iteration."
                ),
            },
            {
                "h": "3. Zero-shot vs few-shot",
                "body": (
                    "Zero-shot: cheap, fast, sometimes underdetermined. "
                    "Few-shot: more controllable, higher token cost. "
                    "Three to seven diverse examples is the sweet spot, "
                    "with the canonical example placed last (recency "
                    "bias is real)."
                ),
            },
            {
                "h": "4. Epistemic uncertainty in LLM outputs",
                "body": (
                    "When the model does not know, it sometimes hallucinates "
                    "and sometimes refuses. Calibration means getting the "
                    "model to refuse exactly when it does not know. "
                    "Techniques: explicit 'I don't know' option in the "
                    "schema; chain-of-thought followed by a confidence "
                    "estimate; ensemble across temperatures."
                ),
            },
            {
                "h": "5. DSPy",
                "body": (
                    "A Signature defines inputs and outputs. A Module "
                    "composes signatures into a callable. An Optimizer "
                    "searches over instructions and demonstrations. The "
                    "Compiler freezes the result into a deployable "
                    "program. DSPy is opinionated; the payoff is that "
                    "you stop hand-tuning prompts."
                ),
                "code": (
                    "import dspy\n\n"
                    "class Classify(dspy.Signature):\n"
                    "    text: str = dspy.InputField()\n"
                    "    label: str = dspy.OutputField()\n\n"
                    "classifier = dspy.ChainOfThought(Classify)\n"
                    "opt = dspy.MIPRO(metric=accuracy)\n"
                    "compiled = opt.compile(classifier, trainset=train)\n"
                ),
            },
            {
                "h": "6. COPRO vs MIPRO",
                "body": (
                    "COPRO does coordinate ascent on instructions. Fast, "
                    "shallow. MIPRO jointly optimizes instructions and "
                    "demonstrations with Bayesian search. Slower, deeper. "
                    "Start with COPRO; promote to MIPRO when the gain "
                    "plateaus."
                ),
            },
            {
                "h": "7. GEPA, TextGrad, ORPO",
                "body": (
                    "GEPA: evolutionary with reflective critique. "
                    "TextGrad: text as a tensor with critic-LLM "
                    "gradients. ORPO: preference optimization unified "
                    "with reference-free training. Each fits a different "
                    "stage of the lifecycle."
                ),
            },
        ],
        "review": [
            "Write a CO-STAR specification for an internal compliance Q&A bot.",
            "Why does metaprompting often beat human iteration?",
            "Pick a calibration technique for an LLM in a high-stakes domain.",
            "When does COPRO suffice and when do you reach for MIPRO?",
        ],
    },
    7: {
        "intro": (
            "Vector retrieval has a ceiling on multi-hop and structural "
            "questions. Today we break through it with RAPTOR, GraphRAG, "
            "and LightRAG. Each has a different cost-benefit profile."
        ),
        "sections": [
            {
                "h": "1. Why graphs beat vectors on multi-hop",
                "body": (
                    "A multi-hop question requires connecting facts that "
                    "may not appear together in any single document. "
                    "Vector similarity captures local meaning; it does "
                    "not capture global structure. Graphs capture both "
                    "by design."
                ),
            },
            {
                "h": "2. RAPTOR",
                "body": (
                    "Cluster chunks. Summarize each cluster. Cluster the "
                    "summaries. Recurse until you have a tree. At query "
                    "time, traverse top-down to find the right "
                    "granularity. Works without a graph database; "
                    "everything lives in the vector store."
                ),
            },
            {
                "h": "3. GraphRAG extraction",
                "body": (
                    "For each document chunk, ask an LLM to extract "
                    "(subject, predicate, object) triplets. Resolve "
                    "entity aliases. Insert into a graph database. "
                    "Expensive at ingestion (one LLM call per chunk); "
                    "fast at query."
                ),
                "code": (
                    "EXTRACTION_PROMPT = '''\n"
                    "Extract entities and relationships from the text.\n"
                    "Output JSON: [{subject, predicate, object}].\n"
                    "Text: {text}\n"
                    "'''\n\n"
                    "def extract_triplets(chunk):\n"
                    "    return json.loads(llm.generate(\n"
                    "        EXTRACTION_PROMPT.format(text=chunk)))\n"
                ),
            },
            {
                "h": "4. Ontologies and entity resolution",
                "body": (
                    "Define entity types (Person, Company, Drug, Disease) "
                    "and relationship types (works_at, treats, "
                    "interacts_with) up front. Resolve aliases (Apple "
                    "Inc., AAPL) to canonical entities. Without these, "
                    "your graph becomes a hairball."
                ),
            },
            {
                "h": "5. Community detection",
                "body": (
                    "Run Leiden or Louvain on the graph to find densely "
                    "connected sub-graphs. Summarize each community with "
                    "an LLM. At query time, retrieve relevant community "
                    "summaries. Microsoft's GraphRAG built this end to "
                    "end."
                ),
            },
            {
                "h": "6. Graph databases",
                "body": (
                    "Neo4j: mature, declarative Cypher, on-disk. "
                    "Memgraph: in-memory, faster on read-heavy workloads. "
                    "ArangoDB: hybrid document + graph. Pick based on "
                    "scale and query patterns."
                ),
            },
            {
                "h": "7. LightRAG",
                "body": (
                    "Skip the community detection. Use dual-level "
                    "retrieval: local (entity neighborhood for specific "
                    "questions) and global (graph-wide for thematic "
                    "questions). Cheaper to build, competitive on many "
                    "tasks."
                ),
            },
        ],
        "review": [
            "Sketch a question that breaks vector RAG but works with GraphRAG.",
            "When is RAPTOR enough; when do you need a real graph?",
            "Pick between Neo4j and Memgraph for a 50M-triplet corpus with read-heavy queries.",
            "What does LightRAG sacrifice for its simplicity?",
        ],
    },
    8: {
        "intro": (
            "Production RAG hits real walls: hallucinations, prompt "
            "injection, PII leakage, latency. Today we cover the guardrail "
            "pipeline, grounding via NLI, and the P95 latency discipline."
        ),
        "sections": [
            {
                "h": "1. The guardrail pipeline",
                "body": (
                    "Four stages, ordered cheap to expensive. Stage 1 "
                    "syntax: well-formed JSON, schema-valid. Stage 2 "
                    "PII: detect and redact. Stage 3 toxicity: score and "
                    "block. Stage 4 intent: route to allowed or "
                    "out-of-scope. Each stage can refuse independently "
                    "and short-circuit the rest."
                ),
            },
            {
                "h": "2. PII handling at the boundary",
                "body": (
                    "Detect PII on inputs and outputs. Redact in logs. "
                    "Use scoped retention. Different jurisdictions have "
                    "different rules (GDPR, CCPA, HIPAA). Build for the "
                    "strictest. Use Presidio or a similar mature library; "
                    "do not roll your own."
                ),
            },
            {
                "h": "3. Prompt injection defense",
                "body": (
                    "Retrieved content is untrusted data. Treat it that "
                    "way. Use system-prompt delimiters that fetched text "
                    "cannot reproduce (random tokens, structured "
                    "headers). Strip instruction-like patterns. Log "
                    "suspicious patterns for review."
                ),
            },
            {
                "h": "4. NLI verification",
                "body": (
                    "After generation, run the (answer, evidence) pair "
                    "through an NLI model. Entailment = grounded. "
                    "Contradiction = block. Neutral = flag for review. "
                    "DeBERTa-large-mnli is a strong baseline."
                ),
                "code": (
                    "def verify_grounding(answer, context, nli_model):\n"
                    "    claims = split_into_claims(answer)\n"
                    "    for claim in claims:\n"
                    "        verdict = nli_model.predict(context, claim)\n"
                    "        if verdict == 'contradiction':\n"
                    "            return False\n"
                    "    return True\n"
                ),
            },
            {
                "h": "5. Grounding via citation",
                "body": (
                    "Have the model cite which retrieved passage supports "
                    "each claim. Verify the citations match. Reject "
                    "answers that fail. The model learns to be more "
                    "honest when it knows it will be checked."
                ),
            },
            {
                "h": "6. The P95 latency discipline",
                "body": (
                    "Means hide tails; users feel P95. Budget each stage "
                    "(retrieval, rerank, generation, verification). "
                    "Nothing exceeds its allotment without explicit "
                    "justification. Standard production target: 2-4 "
                    "seconds P95 for a single RAG turn."
                ),
            },
            {
                "h": "7. Hallucination monitoring",
                "body": (
                    "Sample 1% of traffic for offline grounding "
                    "verification. Trend the hallucination rate weekly. "
                    "Alert when it drifts above baseline. Without "
                    "monitoring, you discover problems through customer "
                    "complaints."
                ),
            },
        ],
        "review": [
            "Pick a guardrail order for a customer-service RAG. Justify.",
            "Sketch a prompt-injection defense that does not break legitimate retrieval.",
            "What is the right action on a 'neutral' NLI verdict?",
            "Allocate a 4-second P95 budget across a 4-stage RAG.",
        ],
    },
    9: {
        "intro": (
            "Enterprise RAG goes beyond chunk-and-retrieve. Today we cover "
            "derivative artifacts that enrich the index, query "
            "transformation for hard questions, semantic caching for cost "
            "control, and hard negative mining for embedder fine-tuning."
        ),
        "sections": [
            {
                "h": "1. Derivative artifacts: factoids and QA pairs",
                "body": (
                    "Use an LLM to extract short factoids from each "
                    "document at ingestion. Also generate plausible QA "
                    "pairs. Index both alongside the raw chunks. "
                    "Retrieval improves on questions that match the "
                    "generated artifacts better than the raw text. Cost: "
                    "one-time ingestion expense per document."
                ),
            },
            {
                "h": "2. HyDE",
                "body": (
                    "Hypothetical Document Embeddings. Generate a "
                    "plausible answer from the query; embed that; "
                    "retrieve against the result. Closes the query-"
                    "document distribution gap that plain query "
                    "embeddings suffer from. Cheap and surprisingly "
                    "effective."
                ),
                "code": (
                    "def hyde_retrieve(query, k=8):\n"
                    "    hypo = llm.generate(\n"
                    "        f'Write a passage that answers: {query}')\n"
                    "    return vector_store.search(embed(hypo), k=k)\n"
                ),
            },
            {
                "h": "3. Multi-hop decomposition",
                "body": (
                    "A planner emits sub-queries. Each sub-query "
                    "retrieves. Partial answers inform the next sub-"
                    "query. Two flavors: predetermined (all sub-queries "
                    "up front) and adaptive (each step depends on prior "
                    "results)."
                ),
            },
            {
                "h": "4. Semantic caching",
                "body": (
                    "Cache answers by query embedding similarity, not "
                    "exact match. Typical hit rate: 20-40% on production "
                    "traffic. Threshold sensitivity matters: too low and "
                    "you serve wrong answers; too high and the cache "
                    "rarely hits."
                ),
            },
            {
                "h": "5. Hard negative mining",
                "body": (
                    "Find documents that look similar to positives but "
                    "are wrong (BM25 high-overlap, dense high-similarity "
                    "but labeled negative). Train the embedder to push "
                    "them apart. Single biggest embedding improvement "
                    "after the base model."
                ),
            },
            {
                "h": "6. Embedding fine-tuning at enterprise scale",
                "body": (
                    "Pull in-domain queries from production logs (with "
                    "consent and privacy review). Build (query, "
                    "clicked-doc) positive pairs. Mine hard negatives. "
                    "Fine-tune with InfoNCE. Re-index. Re-evaluate. "
                    "Repeat quarterly."
                ),
            },
        ],
        "review": [
            "Pick a corpus where QA-pair derivatives help, and one where they do not.",
            "When does HyDE add latency without quality benefit?",
            "Set a semantic cache threshold for a customer-service RAG and defend it.",
            "Sketch the hard-negative mining loop for a code-search corpus.",
        ],
    },
    10: {
        "intro": (
            "Two related topics. Agentic RAG: the agent decides what to "
            "retrieve and when. Text-to-SQL: the agent translates natural "
            "language into executable SQL. Both depend on tool integration "
            "(MCP) and good evaluation."
        ),
        "sections": [
            {
                "h": "1. The agentic lifecycle",
                "body": (
                    "Perceive the user's question. Plan the retrieval. "
                    "Act (call tools). Observe results. Decide whether "
                    "to continue or to answer. The loop has a defined "
                    "termination condition: an answer, a refusal, or a "
                    "max-iteration cap."
                ),
            },
            {
                "h": "2. Model Context Protocol (MCP)",
                "body": (
                    "A clean abstraction for exposing tools to agents. "
                    "Tool servers, JSON schemas, capability negotiation. "
                    "FastMCP wraps it with decorator-style Python. The "
                    "right default for new tool integrations."
                ),
            },
            {
                "h": "3. Agent specialization patterns",
                "body": (
                    "Generalist agent with many tools. Specialist per "
                    "domain. Router that picks among specialists. Each "
                    "pattern has a sweet spot. Generalist wins until tool "
                    "selection saturates the model's bandwidth."
                ),
            },
            {
                "h": "4. Text-to-SQL architecture",
                "body": (
                    "Stages: schema understanding, query planning, SQL "
                    "generation, syntax verification, execution. Each "
                    "stage can fail differently. Build checkpoints to "
                    "isolate failures and fail fast."
                ),
                "code": (
                    "def text_to_sql(question, db):\n"
                    "    relevant_tables = schema_retriever(question, db)\n"
                    "    plan = planner(question, relevant_tables)\n"
                    "    sql = sql_generator(plan, relevant_tables)\n"
                    "    if not is_valid_sql(sql, db):\n"
                    "        sql = repair(sql, error, plan)\n"
                    "    return db.execute(sql)\n"
                ),
            },
            {
                "h": "5. Schema uncertainty",
                "body": (
                    "Production schemas have hundreds of tables. The "
                    "model cannot see them all. Embed table descriptions "
                    "and column names. Retrieve relevant tables for the "
                    "question. Pass only those to the SQL generator."
                ),
            },
            {
                "h": "6. CTE libraries",
                "body": (
                    "Pre-built Common Table Expressions for recurring "
                    "patterns: date ranges, customer segments, revenue "
                    "calculations. The model composes from a known "
                    "vocabulary. Reduces complexity and improves "
                    "correctness."
                ),
            },
            {
                "h": "7. RL for SQL generation",
                "body": (
                    "Reward = SQL executes + result rows match expected. "
                    "RLVR fits naturally. Most gains come from base SFT "
                    "(fine-tune on Spider, Bird, or in-house data); RL "
                    "adds the last 5 to 15 percentage points on hard "
                    "queries."
                ),
            },
        ],
        "review": [
            "When does agentic RAG beat static RAG, and by how much typically?",
            "Why is MCP a better tool abstraction than ad-hoc function calling?",
            "Pick a schema scale where schema retrieval becomes mandatory.",
            "Design a verifier for SQL generation in a finance domain.",
        ],
    },
    11: {
        "intro": (
            "Fine-tuning week. Cover Chinchilla scaling for sizing, PEFT "
            "with LoRA, the full RLHF pipeline, and RL with verifiable "
            "rewards. Tie it back to Text-to-SQL with a concrete "
            "fine-tuning lab."
        ),
        "sections": [
            {
                "h": "1. Chinchilla scaling",
                "body": (
                    "For a fixed compute budget, optimal model size and "
                    "training tokens scale together at roughly 20 tokens "
                    "per parameter. A 7B model wants about 140B tokens. "
                    "Knowing your token budget tells you the right model "
                    "size. Over-trained smaller models often beat under-"
                    "trained larger ones."
                ),
            },
            {
                "h": "2. PEFT and LoRA",
                "body": (
                    "Freeze the base model. Adapt with a low-rank update "
                    "BA. Train only BA. Recover near-full-precision "
                    "performance on most downstream tasks at 0.5% to 2% "
                    "of trainable parameters."
                ),
                "code": (
                    "from peft import LoraConfig, get_peft_model\n\n"
                    "config = LoraConfig(\n"
                    "    r=16, lora_alpha=32,\n"
                    "    target_modules=['q_proj', 'v_proj', 'o_proj'],\n"
                    "    lora_dropout=0.05,\n"
                    "    task_type='CAUSAL_LM',\n"
                    ")\n"
                    "model = get_peft_model(base, config)\n"
                ),
            },
            {
                "h": "3. qLoRA",
                "body": (
                    "Quantize the base to 4-bit (NF4 with double "
                    "quantization). Train LoRA in 16-bit. Memory drops "
                    "4x. Accuracy stays within 1-2 points on most tasks. "
                    "The free lunch is real, with caveats on very small "
                    "models and very long contexts."
                ),
            },
            {
                "h": "4. The RLHF pipeline",
                "body": (
                    "Three stages. SFT on demonstrations. Reward model "
                    "trained on preference pairs. PPO against the reward "
                    "model with KL penalty to a reference model. Each "
                    "stage has its own failure modes (overfitting, "
                    "reward hacking, KL collapse)."
                ),
            },
            {
                "h": "5. RL with verifiable rewards (RLVR)",
                "body": (
                    "When correctness can be checked programmatically "
                    "(SQL execution, unit tests, theorem checker), skip "
                    "the reward model. The verifier becomes the reward "
                    "function. Faster, more honest, less reward hacking."
                ),
            },
            {
                "h": "6. GRPO",
                "body": (
                    "Sample N completions per prompt. Compute group-"
                    "relative advantage. Drop the value head. Halves "
                    "memory. Matches PPO on many tasks. Default for "
                    "RLVR-style training."
                ),
            },
            {
                "h": "7. Evaluating fine-tuned models",
                "body": (
                    "Held-out eval set for the target task. Regression "
                    "suite for base capabilities (so fine-tuning has not "
                    "broken math, code, or reasoning). Drift checks. "
                    "Explicit harm tests."
                ),
            },
        ],
        "review": [
            "Given a 50B-token corpus and 8 H100 weeks, what model size do you train?",
            "Pick LoRA rank and alpha for a SQL-generation task on a 7B base.",
            "When does qLoRA degrade more than 2 points and what is the cause?",
            "Sketch an RLVR setup for a code-generation agent.",
        ],
    },
    12: {
        "intro": (
            "Evaluation week. Cover retrieval metrics, end-to-end RAG "
            "metrics via Ragas, LLM-as-a-judge done right, robustness "
            "via the RGB benchmark, and the principle of verification "
            "asymmetry that underlies all good eval."
        ),
        "sections": [
            {
                "h": "1. Retrieval metrics in one screen",
                "body": (
                    "Precision@k: fraction of top-k that are relevant. "
                    "Recall@k: fraction of all relevant retrieved. MRR: "
                    "rank of the first relevant. MAP: averaged precision "
                    "across queries. NDCG: graded relevance with rank "
                    "discount. Pick the metric that matches your "
                    "downstream use."
                ),
            },
            {
                "h": "2. NDCG correctly",
                "body": (
                    "Most teams report NDCG@10 with binary relevance, "
                    "which is the same as recall@10 weighted by position. "
                    "Use graded relevance (0, 1, 2, 3) for the metric to "
                    "earn its keep. Otherwise stick to recall@k."
                ),
            },
            {
                "h": "3. Ragas for end-to-end RAG",
                "body": (
                    "Four metrics. Faithfulness: answer grounded in "
                    "context. Answer relevance: answer addresses the "
                    "question. Context precision: retrieved context is "
                    "relevant. Context recall: retrieved context covers "
                    "what is needed."
                ),
                "code": (
                    "from ragas import evaluate\n"
                    "from ragas.metrics import (\n"
                    "    faithfulness, answer_relevancy,\n"
                    "    context_precision, context_recall)\n\n"
                    "results = evaluate(\n"
                    "    dataset,\n"
                    "    metrics=[faithfulness, answer_relevancy,\n"
                    "             context_precision, context_recall],\n"
                    ")\n"
                ),
            },
            {
                "h": "4. LLM-as-a-judge",
                "body": (
                    "Use a separate strong model to judge. Cheap and "
                    "scalable. Beware: position bias (first answer wins), "
                    "verbosity bias (longer is preferred), self-"
                    "preference bias (model favors its own outputs). "
                    "Control via randomization, length normalization, "
                    "and a different judge model."
                ),
            },
            {
                "h": "5. The RGB benchmark",
                "body": (
                    "Tests RAG against four robustness axes: noise (do "
                    "irrelevant passages confuse the model?), negative "
                    "passages (does the model refuse when no answer is "
                    "supported?), integration (does the model combine "
                    "facts across passages?), and counterfactual (does "
                    "the model trust evidence over its prior?)."
                ),
            },
            {
                "h": "6. Verification asymmetry",
                "body": (
                    "When verification is cheaper than generation, you "
                    "can score many candidates with a verifier and pick "
                    "the best. This is the principle behind self-"
                    "consistency, best-of-N, and RLVR. Build verifiers "
                    "before you build generators when you can."
                ),
            },
            {
                "h": "7. An eval that does not lie",
                "body": (
                    "Held-out test set never touches training. Stable "
                    "scoring rubric. Multiple judges or a calibrated "
                    "single judge. Reproducible seed. Report variance, "
                    "not just the mean. Publish the eval set so others "
                    "can falsify."
                ),
            },
        ],
        "review": [
            "Pick a task where MRR is the right metric and explain.",
            "Sketch a Ragas configuration for a multi-hop legal RAG.",
            "Design an LLM-as-judge protocol that controls all three biases.",
            "Apply verification asymmetry to a problem you have shipped.",
        ],
    },
}
