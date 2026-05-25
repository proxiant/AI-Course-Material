"""Chapter 13: Retrieval-Augmented Generation."""

CHAPTER = {
    "label": "Chapter 13",
    "title": "Retrieval-Augmented Generation",
    "intro_image": "11_rag.png",
    "intro_caption": "Figure 13.1: The RAG pipeline: query -> retrieve -> generate.",
    "sections": [
        {
            "number": "13.1",
            "title": "Why RAG",
            "paragraphs": [
                "Pretrained LLMs have two structural limits that show up immediately in "
                "production. Their knowledge is frozen at training time; they cannot "
                "reference anything that happened after their training cutoff or anything "
                "specific to your organization. Their parametric memory is lossy; even for "
                "facts they have seen, they sometimes hallucinate plausible-sounding but "
                "wrong answers.",

                "Retrieval-augmented generation (RAG) solves both. At inference time, "
                "retrieve relevant passages from an external knowledge base. Pass them to "
                "the LLM as context. The LLM generates conditioned on the retrieved "
                "evidence. The knowledge is up-to-date (you control the knowledge base), "
                "private (it can include your proprietary documents), and auditable (the "
                "model cites its sources).",

                "RAG has become the default architecture for production LLM applications. "
                "Customer support assistants, legal research, medical question answering, "
                "internal knowledge tools, agentic systems all run on RAG. This chapter "
                "covers the architecture, the engineering choices, and the production "
                "patterns.",
            ],
        },
        {
            "number": "13.2",
            "title": "The RAG Pipeline",
            "image": "39_production_rag.png",
            "caption": "Figure 13.2: Production RAG: ingestion and query pipelines plus cross-cutting concerns.",
            "paragraphs": [
                "A complete RAG system has two pipelines: ingestion (build the knowledge "
                "base) and query (use the knowledge base to answer questions). Cross-"
                "cutting concerns (caching, observability, guardrails, evaluation) span "
                "both.",
            ],
            "subsections": [
                {
                    "title": "13.2.1 Ingestion Pipeline",
                    "paragraphs": [
                        "Source connection. Pull documents from source systems: S3, "
                        "GitHub, Notion, Confluence, Google Drive, databases, APIs. Handle "
                        "authentication, rate limits, incremental updates.",
                        "Parsing. Extract clean text from heterogeneous formats: PDF, HTML, "
                        "DOCX, Markdown, code files, images (with OCR), audio (with ASR), "
                        "video. Each format has gotchas; layout-preserving PDF parsing is "
                        "notoriously tricky.",
                        "Chunking. Split documents into pieces small enough to fit in the "
                        "LLM context window and big enough to preserve meaning. Strategies "
                        "vary; we cover them next section.",
                        "Embedding. Encode each chunk with a sentence embedder. Use a "
                        "domain-tuned embedder if your corpus is specialized.",
                        "Vector storage. Index the embeddings in a vector database. Store "
                        "metadata (source URL, document title, section, timestamp, author) "
                        "alongside the vectors for filtering and attribution.",
                        "Ongoing updates. When source documents change, re-embed and "
                        "update the index. Incremental updates avoid full rebuilds.",
                    ],
                },
                {
                    "title": "13.2.2 Query Pipeline",
                    "paragraphs": [
                        "Query rewriting. For conversational systems, rewrite the latest "
                        "user turn into a standalone query using conversation history. "
                        "'When was it founded?' becomes 'When was Acme Corp founded?' "
                        "before retrieval.",
                        "Query embedding. Encode the (possibly rewritten) query with the "
                        "same embedder used for the corpus.",
                        "Retrieval. ANN search returns top-k candidates from the vector "
                        "database. Hybrid (vector + BM25 + filters) almost always beats "
                        "pure vector.",
                        "Reranking. Re-score the top-k candidates with a stronger model "
                        "(cross-encoder or LLM-based reranker). Refine to top-n where n is "
                        "much smaller than k.",
                        "Prompt construction. Template the retrieved passages, the user "
                        "query, and the system instructions into a prompt. Include "
                        "citation markers so the model can reference sources.",
                        "Generation. The LLM produces a response conditioned on the prompt. "
                        "Post-process: format citations, run guardrails, log for "
                        "evaluation.",
                    ],
                },
            ],
        },
        {
            "number": "13.3",
            "title": "Chunking Strategies",
            "paragraphs": [
                "Chunking is the quiet make-or-break of RAG. Too small and the model loses "
                "context; too large and the relevance signal dilutes. The right choice "
                "depends on your documents and your query distribution.",
            ],
            "subsections": [
                {
                    "title": "13.3.1 Fixed-Size Chunking",
                    "paragraphs": [
                        "Split on token count with overlap (typically 10-20%). Cheap, "
                        "predictable. Ignores natural document boundaries. Often good "
                        "enough for homogeneous corpora; suboptimal for heterogeneous ones "
                        "where document structure matters.",
                        "Typical chunk sizes: 256-1024 tokens. Smaller = more precise hits "
                        "but less context per hit. Larger = more context but lower "
                        "relevance scores. The right size depends on the downstream LLM's "
                        "context window and the cost per token.",
                    ],
                },
                {
                    "title": "13.3.2 Semantic Chunking",
                    "paragraphs": [
                        "Embed each sentence. Split where adjacent sentence similarity "
                        "drops below a threshold. Respects natural topic boundaries. More "
                        "expensive than fixed-size at ingestion but produces more coherent "
                        "chunks.",
                    ],
                },
                {
                    "title": "13.3.3 Late Chunking",
                    "paragraphs": [
                        "Embed the entire document first, then split the resulting "
                        "token-level embeddings into chunks. Each chunk's embedding still "
                        "reflects the full document context. Works only with embedders "
                        "that support long contexts (Jina v3, bge-m3).",
                    ],
                },
                {
                    "title": "13.3.4 Contextual Chunking",
                    "paragraphs": [
                        "Before embedding each chunk, prepend a short LLM-generated summary "
                        "of the surrounding context. Anthropic's contextual retrieval "
                        "showed 35% retrieval improvement on average. The cost is one LLM "
                        "call per chunk at ingestion.",
                    ],
                },
                {
                    "title": "13.3.5 Hierarchical (Mother-Child) Chunking",
                    "paragraphs": [
                        "Embed at two granularities. Small child chunks (250 tokens) for "
                        "matching. Large mother chunks (1000 tokens) for context. Match "
                        "against children but return the parent mother chunk to the LLM. "
                        "Best of both worlds, modest extra storage.",
                    ],
                },
            ],
        },
        {
            "number": "13.4",
            "title": "Query Transformations",
            "paragraphs": [
                "The user's query and the documents may not share surface form even when "
                "they share meaning. Query transformations bridge the gap.",

                "HyDE (Hypothetical Document Embeddings). Generate a plausible answer "
                "from the query using an LLM. Embed the hypothesis. Retrieve against the "
                "result. Closes the query-document distribution gap. Cheap (one extra LLM "
                "call per query) and surprisingly effective.",

                "Multi-query expansion. Generate multiple paraphrases of the query. "
                "Retrieve for each. Merge results via RRF. Catches retrievals that any "
                "single phrasing would miss.",

                "Query decomposition. For multi-hop questions, decompose into sub-queries. "
                "Each sub-query retrieves separately. Partial answers feed the next "
                "sub-query. Two flavors: predetermined (planner emits all sub-queries up "
                "front) or adaptive (each step depends on prior results).",

                "Self-query. The LLM rewrites the user's natural-language query into a "
                "structured form: vector query + metadata filter. 'Show me Anthropic "
                "papers from 2023' becomes (vector: 'Anthropic papers', filter: "
                "year=2023, source='Anthropic'). Combines semantic and structured search.",
            ],
        },
        {
            "number": "13.5",
            "title": "Retrieval Funnel",
            "paragraphs": [
                "Production retrieval is a funnel. Cheap candidates in, well-scored "
                "results out. Multiple stages, each optimized for its role.",

                "Stage 1: parallel sparse and dense retrieval. BM25 returns 100-500 "
                "candidates. Dense (vector) retrieval returns another 100-500. RRF "
                "fuses them.",

                "Stage 2: optional Matryoshka pruning. If embeddings support it, prune the "
                "top 100 with a 64-dimensional truncation before full-dimensional scoring.",

                "Stage 3: ColBERT or other late-interaction scoring. Re-score the top 30 "
                "with token-level interaction. Cheaper than a cross-encoder, more "
                "expressive than bi-encoders.",

                "Stage 4: cross-encoder reranker. Re-score the top 10-20 with full cross-"
                "attention between query and document. The most accurate, most expensive "
                "stage. Reserve for the final cut.",

                "Stage 5: LLM-based reranker (optional). For the most demanding tasks, an "
                "LLM scores each remaining candidate against the query with a detailed "
                "rubric. Slowest, most accurate.",

                "Tune candidate counts per stage on your data. The default funnel works "
                "well; the exact numbers depend on corpus and latency budget.",
            ],
        },
        {
            "number": "13.6",
            "title": "Multi-Hop and Agentic RAG",
            "paragraphs": [
                "Static RAG (retrieve once, generate once) handles single-hop questions "
                "well. Multi-hop questions require connecting evidence from multiple "
                "sources.",

                "Iterative agentic RAG. The agent retrieves, generates a partial answer, "
                "decides what to retrieve next based on what it now knows. Continues "
                "until the question is answered or a step limit is reached. Higher cost "
                "than static RAG but handles questions that static RAG cannot.",

                "GraphRAG (Microsoft, 2024). Build a knowledge graph from the corpus by "
                "extracting entities and relationships with an LLM. Detect communities of "
                "related entities. Summarize each community. At query time, retrieve "
                "relevant community summaries (for global questions) or entity "
                "neighborhoods (for specific questions). Solves multi-hop and structural "
                "questions that pure vector retrieval misses.",

                "LightRAG. A simpler graph-based approach: dual-level retrieval (local "
                "and global) without explicit community detection. Cheaper to build, "
                "competitive on many tasks.",

                "When to use what. Static RAG: simple factual questions, single-source "
                "answers. Iterative agentic: multi-hop questions, complex reasoning chains. "
                "GraphRAG: questions requiring structural reasoning (who knows whom, what "
                "depends on what, what came before). Pick based on the question "
                "distribution.",
            ],
        },
        {
            "number": "13.7",
            "title": "Derivative Artifacts",
            "paragraphs": [
                "Enterprise RAG often benefits from generating derivative content from the "
                "source corpus at ingestion time.",

                "Factoids. Use an LLM to extract short factoids from each document. Index "
                "the factoids alongside the raw chunks. Retrieval improves on questions "
                "that match the factoid phrasing better than the raw text.",

                "QA pairs. Generate plausible (question, answer) pairs from each document. "
                "Index the questions. At query time, match user queries against the "
                "generated questions; return the corresponding answers and supporting "
                "passages.",

                "Summaries. Generate document-level and section-level summaries. Use them "
                "for global questions ('what is this document about?'); use the original "
                "chunks for specific questions.",

                "Cost. One-time ingestion expense, paid per document. The cost amortizes "
                "over many queries. Quality improvements range from negligible (already "
                "well-structured technical documents) to dramatic (unstructured chat "
                "logs).",
            ],
        },
        {
            "number": "13.8",
            "title": "Semantic Caching",
            "paragraphs": [
                "RAG is expensive: an embedding call, a vector search, optional reranking, "
                "and an LLM generation per query. Semantic caching skips this work when a "
                "similar query was answered recently.",

                "Mechanics. Embed each query. Look up similar past queries in a small "
                "vector store. If similarity exceeds a threshold, return the cached "
                "response. Otherwise process the query normally and cache the result.",

                "Threshold tuning. Too low: serve wrong answers from cache. Too high: "
                "cache rarely hits. Tune against a labeled validation set; calibrate by "
                "user feedback signals in production.",

                "Typical hit rates. 20-40% on production traffic with repeated query "
                "patterns (customer support FAQs, internal help). Lower for free-form "
                "queries.",

                "Cost savings. Cache hits cost the embedding call only, often under "
                "$0.0001 each. Cache misses cost the full RAG pipeline. At 30% hit rate, "
                "total cost drops by roughly 25%.",
            ],
        },
        {
            "number": "13.9",
            "title": "Guardrails and Grounding",
            "paragraphs": [
                "RAG reduces but does not eliminate hallucination. Guardrails add layers "
                "of defense.",

                "Citation requirement. Have the model cite which retrieved passage "
                "supports each claim. Verify the citations match. Reject answers that "
                "fail.",

                "NLI verification. Run each claim through a natural language inference "
                "model against the retrieved context. Entailment = grounded. Contradiction "
                "= block. Neutral = flag for review. DeBERTa-large-mnli is a strong "
                "baseline.",

                "Input guardrails. Detect prompt injection in user input and retrieved "
                "content. Strip instruction-like patterns. Log suspicious queries.",

                "Output guardrails. PII redaction. Toxicity filters. Content moderation. "
                "Structured output schemas to prevent invalid responses.",

                "Defense in depth. No single guardrail catches everything. Layer them. "
                "Monitor each layer's trigger rate.",
            ],
        },
        {
            "number": "13.10",
            "title": "Evaluating RAG",
            "paragraphs": [
                "RAG quality depends on retrieval quality and generation quality. Evaluate "
                "both separately and end to end.",

                "Retrieval evaluation. Build a held-out test set of (query, relevant "
                "documents) pairs. Measure Recall@k, MRR, NDCG. The most important metric "
                "for RAG: if relevant documents are not retrieved, the LLM cannot answer.",

                "Generation evaluation. Faithfulness: is the answer grounded in the "
                "retrieved context? Answer relevance: does the answer address the "
                "question? Context precision: is the retrieved context relevant? Context "
                "recall: does the retrieved context cover what is needed? Ragas is the "
                "standard framework that automates these.",

                "End-to-end evaluation. Beyond Ragas metrics, evaluate user satisfaction "
                "signals (thumbs, regenerate rate, conversation length). The metrics "
                "matter only insofar as they correlate with what users care about.",

                "Robustness evaluation. RGB benchmark (Chen et al., 2023) tests four "
                "axes: noise (do irrelevant passages confuse the model?), negative "
                "(does the model refuse when no answer is supported?), integration (does "
                "the model combine facts across passages?), counterfactual (does the model "
                "trust evidence over its prior?). A real RAG should hold up against all "
                "four.",

                "Continuous evaluation. Sample 1-5% of production traffic. Score offline. "
                "Trend over time. Alert on regression. New deployments must pass these "
                "checks before promotion.",
            ],
        },
        {
            "number": "13.11",
            "title": "Summary",
            "bullets": [
                "RAG combines retrieval with generation, grounding LLM responses in "
                "external knowledge. It is the dominant architecture for production LLM "
                "applications.",
                "The ingestion pipeline (parse, chunk, embed, store) builds the knowledge "
                "base. The query pipeline (rewrite, embed, retrieve, rerank, generate) "
                "uses it.",
                "Chunking strategy matters: fixed-size, semantic, late, contextual, and "
                "hierarchical chunking trade cost for quality.",
                "Query transformations (HyDE, multi-query, decomposition) handle hard "
                "queries.",
                "The retrieval funnel (sparse + dense + Matryoshka + ColBERT + cross-"
                "encoder) optimizes the cost-quality tradeoff at each stage.",
                "Multi-hop questions need iterative agentic RAG or graph-based approaches "
                "(GraphRAG, LightRAG).",
                "Semantic caching cuts cost; guardrails reduce hallucination; Ragas "
                "evaluates end to end.",
            ],
        },
    ],
    "further_reading": [
        "Lewis et al., 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks' (2020). the original RAG paper.",
        "Karpukhin et al., 'Dense Passage Retrieval for Open-Domain Question Answering' (2020). DPR.",
        "Edge et al., 'From Local to Global: A Graph RAG Approach to Query-Focused Summarization' (2024). Microsoft GraphRAG.",
        "Gao et al., 'Precise Zero-Shot Dense Retrieval without Relevance Labels' (2022). HyDE.",
        "Es et al., 'RAGAS: Automated Evaluation of Retrieval Augmented Generation' (2023).",
    ],
}
