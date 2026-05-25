"""Chapter 12: Vector Databases and Approximate Nearest Neighbor Search."""

CHAPTER = {
    "label": "Chapter 12",
    "title": "Vector Databases and Approximate Nearest Neighbor Search",
    "intro_image": "14_ann_search.png",
    "intro_caption": "Figure 12.1: Approximate nearest neighbor search in embedding space.",
    "sections": [
        {
            "number": "12.1",
            "title": "Why Vector Databases",
            "paragraphs": [
                "Modern AI runs on embeddings. Documents, images, audio, products, users are "
                "all represented as vectors in some learned space. The fundamental operation "
                "is: given a query vector, find the most similar stored vectors. At small "
                "scale, brute-force search works. At millions or billions of vectors, "
                "specialized infrastructure is required.",

                "Vector databases are the infrastructure for this. They index high-"
                "dimensional vectors with approximate nearest neighbor (ANN) algorithms, "
                "support hybrid queries combining vector similarity with metadata filters, "
                "scale horizontally, and integrate with the rest of the data stack.",

                "Use cases. Semantic search (the canonical use). Recommendation systems "
                "(find similar items to those a user liked). Retrieval-augmented "
                "generation (the dominant new use). Image and product search. Anomaly "
                "detection (distance from typical embeddings). Duplicate detection. "
                "Personalization (user embeddings as features).",

                "This chapter covers the algorithms (HNSW, IVF, PQ), the major products "
                "(FAISS, Pinecone, Weaviate, Qdrant, Milvus, pgvector), and the design "
                "decisions that determine cost, latency, and quality.",
            ],
        },
        {
            "number": "12.2",
            "title": "The Nearest Neighbor Problem",
            "paragraphs": [
                "Given a query vector q and a set of n stored vectors {v_1, ..., v_n} in d "
                "dimensions, find the k closest vectors to q under some distance metric.",

                "Brute-force is O(n·d) per query: compute the distance from q to every "
                "stored vector. For 1M vectors at 768 dimensions, this is 750M operations "
                "per query. Slow but exact.",

                "Approximate nearest neighbor (ANN) algorithms trade a small recall loss "
                "for orders of magnitude speedup. 'Recall' is the fraction of true k "
                "nearest neighbors that the approximate method returns. 95-99% recall is "
                "typical for production systems.",

                "Distance metrics. Cosine similarity (most common for embeddings; "
                "equivalent to dot product for L2-normalized vectors). Euclidean (L2) "
                "distance. Inner product (for unnormalized vectors). The metric must match "
                "what the embedding model was trained with.",
            ],
        },
        {
            "number": "12.3",
            "title": "HNSW: Hierarchical Navigable Small World",
            "image": "33_hnsw.png",
            "caption": "Figure 12.2: HNSW search drops through hierarchical layers from sparse to dense.",
            "paragraphs": [
                "HNSW (Malkov and Yashunin, 2016) is the dominant ANN algorithm. A "
                "hierarchical graph structure with logarithmic search time and high recall.",
            ],
            "subsections": [
                {
                    "title": "12.3.1 The Algorithm",
                    "paragraphs": [
                        "HNSW builds a multi-layer graph. The bottom layer contains all "
                        "vectors, connected to their neighbors. Higher layers are "
                        "increasingly sparse, with each node randomly promoted to higher "
                        "layers with some probability.",
                        "Search starts at the top layer with the highest-level entry point. "
                        "At each layer, greedy search finds the closest known node. The "
                        "query then drops to the next layer and continues. The hierarchical "
                        "structure provides logarithmic time complexity.",
                        "Construction adds vectors one at a time. Each new vector finds its "
                        "approximate nearest neighbors at each layer and connects to them. "
                        "Index build time is O(n log n).",
                    ],
                },
                {
                    "title": "12.3.2 Parameters and Tradeoffs",
                    "paragraphs": [
                        "M: number of bi-directional links per node. Higher M = better "
                        "recall, more memory. Typical: 16-64.",
                        "ef_construction: search width during index building. Higher = "
                        "better quality index, slower to build. Typical: 100-400.",
                        "ef_search: search width at query time. Higher = better recall, "
                        "slower query. Typical: 50-200, tunable per query.",
                        "Memory: roughly 1.5x the vector storage for the graph structure. "
                        "Add the vectors themselves: for 1M vectors at 768 dimensions in "
                        "float32, that is 3GB of vectors plus 4.5GB of graph = 7.5GB.",
                        "Strengths: best-in-class recall-latency tradeoff at moderate "
                        "scale (millions to hundreds of millions of vectors).",
                        "Weaknesses: memory-heavy. Insertion is not free. Difficult to "
                        "shard.",
                    ],
                },
            ],
        },
        {
            "number": "12.4",
            "title": "IVF: Inverted File Index",
            "paragraphs": [
                "IVF clusters vectors into k groups via k-means. Each cluster has a "
                "centroid. At query time, find the k nearest centroids, then search only "
                "the vectors in those clusters. Scales to billions with much less memory "
                "than HNSW.",

                "Parameters. nlist: number of clusters. Typical: sqrt(n) to 4·sqrt(n). "
                "nprobe: number of clusters to search at query time. Higher = better "
                "recall, slower query. Typical: 8-128.",

                "Memory. Stores the original vectors plus the centroids. The centroid "
                "list is small. The total memory is dominated by the vectors themselves.",

                "Tradeoffs vs HNSW. IVF is memory-friendly and scales better at billion "
                "scale. HNSW typically has better recall at the same query latency for "
                "moderate scale. The IVF + PQ combination (next section) is the standard "
                "for very large indexes.",
            ],
        },
        {
            "number": "12.5",
            "title": "PQ: Product Quantization",
            "paragraphs": [
                "Product quantization compresses vectors for memory efficiency. Split each "
                "vector into m subvectors. Train k codewords per subvector via k-means. "
                "Replace each subvector with its nearest codeword index.",

                "Storage: m · log₂(k) bits per vector. For m=8, k=256, that is 64 bits "
                "(8 bytes) per vector, regardless of original dimension. A 768-dimensional "
                "float32 vector (3KB) becomes 8 bytes: 384x compression.",

                "Query time. Compute distances from the query to each subvector's "
                "codewords once. For each candidate vector, look up the subvector "
                "distances and sum. Much faster than computing the full distance.",

                "Quality. PQ introduces error proportional to the quantization granularity. "
                "Recall drops by a few percentage points compared to exact search. For "
                "first-stage retrieval followed by re-ranking on full-precision vectors, "
                "this is acceptable.",

                "Combinations. IVF + PQ is the standard for billion-scale indexes. FAISS "
                "ships highly optimized implementations. OPQ (Optimized Product "
                "Quantization) rotates vectors before quantizing for better quality. "
                "Residual PQ does multi-stage quantization for further accuracy.",
            ],
        },
        {
            "number": "12.6",
            "title": "The Vector Database Ecosystem",
            "paragraphs": [
                "Different products serve different scale and operational needs.",
            ],
            "subsections": [
                {
                    "title": "12.6.1 FAISS",
                    "paragraphs": [
                        "Library (not a service) from Facebook. C++ with Python bindings. "
                        "The most flexible ANN tool. Implements every major algorithm "
                        "(HNSW, IVF, PQ, IVFPQ, IVFPQ+R, and more). Used as the underlying "
                        "engine in many vector databases.",
                        "Use directly when you need maximum flexibility, are willing to "
                        "manage indexes manually, and do not need a network service. Use a "
                        "vector database when you need a managed service, hybrid queries, "
                        "or scaling beyond a single machine.",
                    ],
                },
                {
                    "title": "12.6.2 Pinecone",
                    "paragraphs": [
                        "Managed vector database service. Serverless. Easy to start: create "
                        "an index, upsert vectors, query. Expensive at scale; tied to "
                        "Pinecone's hosting.",
                        "Strong on: ease of use, integration with the LLM ecosystem, "
                        "low operational burden.",
                        "Weak on: cost at scale, vendor lock-in, no self-hosting option.",
                    ],
                },
                {
                    "title": "12.6.3 Weaviate",
                    "paragraphs": [
                        "Open-source and managed. GraphQL API. Strong on hybrid search "
                        "(vector + BM25 + filters). Good metadata filtering.",
                        "Strong on: hybrid search, schema-driven design, open source with "
                        "managed cloud option.",
                        "Weak on: GraphQL API has a learning curve.",
                    ],
                },
                {
                    "title": "12.6.4 Qdrant",
                    "paragraphs": [
                        "Open-source, Rust-based. Fast, strong filtering. Self-hostable. "
                        "Managed cloud option.",
                        "Strong on: performance, filtering, open source.",
                        "Notable feature: filtering happens before vector search "
                        "(filterable HNSW), avoiding the trap of filtering after retrieval.",
                    ],
                },
                {
                    "title": "12.6.5 Milvus",
                    "paragraphs": [
                        "Open-source, mature, scales to billions. Multiple index types. "
                        "Used at very large scale in production.",
                        "Strong on: scale, breadth of index types.",
                        "Weak on: operational complexity. Best for teams with infrastructure "
                        "engineering capacity.",
                    ],
                },
                {
                    "title": "12.6.6 pgvector",
                    "paragraphs": [
                        "PostgreSQL extension for vector search. Good when you already use "
                        "Postgres and don't need extreme scale. Inherits Postgres's "
                        "transactions, joins, and operational maturity.",
                        "Strong on: simplicity (use what you already have), ACID "
                        "transactions, hybrid SQL + vector queries.",
                        "Weak on: pure scale. For 100M+ vectors with low latency, "
                        "specialized vector databases win.",
                    ],
                },
                {
                    "title": "12.6.7 Elasticsearch and OpenSearch",
                    "paragraphs": [
                        "Added vector search to mature full-text engines. Best when you "
                        "want hybrid sparse (BM25) + dense (vector) search out of the box, "
                        "or are already operating Elasticsearch for logging or search.",
                        "Strong on: hybrid search, mature operations, large ecosystem.",
                        "Weak on: pure vector quality at scale; specialized vector "
                        "databases win on raw ANN metrics.",
                    ],
                },
                {
                    "title": "12.6.8 Others",
                    "paragraphs": [
                        "Vespa: Yahoo's search engine; very mature; supports vector "
                        "search natively.",
                        "LanceDB: embedded vector database with a developer-friendly API.",
                        "MyScale: vector search built on ClickHouse.",
                        "Chroma: lightweight, embeddable, great for prototyping.",
                    ],
                },
            ],
        },
        {
            "number": "12.7",
            "title": "Hybrid Search",
            "paragraphs": [
                "Pure vector retrieval misses exact keyword matches, rare terms, and "
                "structured constraints. Pure keyword search (BM25) misses semantic "
                "similarity. The combination is the production default.",

                "Reciprocal Rank Fusion (RRF). Run BM25 and dense retrieval separately. "
                "Each returns a ranked list. Fuse the rankings: score(d) = Σ 1/(k + "
                "rank(d, list_i)). Parameter-free, robust, often the best fusion strategy.",

                "Weighted score fusion. score(d) = α · sparse(d) + (1-α) · dense(d). "
                "Requires normalizing the scores; sensitive to the choice of α. RRF is "
                "usually a safer default.",

                "Filtering. In addition to vector and keyword similarity, filter by "
                "metadata: 'documents tagged with category X', 'created after date Y', "
                "'authored by user Z'. Pre-filtering (apply filter before vector search) "
                "is usually faster than post-filtering (vector search then filter) if the "
                "vector database supports it.",
            ],
        },
        {
            "number": "12.8",
            "title": "Reranking",
            "paragraphs": [
                "Retrieval returns candidate documents. Reranking re-scores them with a "
                "stronger (and slower) model to refine the order.",

                "Why rerank. The retrieval stage prioritizes speed over precision. A "
                "stronger model can examine each candidate in detail and pick the best. "
                "Cross-encoders (rather than bi-encoders) compute attention between query "
                "and document, capturing finer relevance signals.",

                "Cost. Cross-encoders are 10-100x slower per (query, document) pair than "
                "bi-encoders. Only feasible on a small candidate set (typically top 20-100 "
                "from retrieval).",

                "Modern implementations. Sentence-transformers cross-encoders. Cohere "
                "Rerank API. ColBERT (late interaction, faster than full cross-encoders). "
                "LLM-based rerankers (use an LLM to score each candidate).",

                "Pattern. Retrieval returns 100 candidates from millions. Cross-encoder "
                "reranks to top 5. The top 5 go to the LLM for generation. The retrieval "
                "stage filters; the reranker refines; the generator synthesizes. Each "
                "stage is optimized for its role.",
            ],
        },
        {
            "number": "12.9",
            "title": "Production Considerations",
            "paragraphs": [
                "Beyond the ANN algorithm and the database choice, several engineering "
                "concerns matter.",

                "Index updates. Insertion latency, deletion semantics, eventual "
                "consistency. HNSW insertion is incremental; IVF can require "
                "re-clustering periodically. Plan for this.",

                "Sharding and replication. Sharding splits the index across nodes for "
                "horizontal scale. Replication adds read throughput and fault tolerance. "
                "Different vector databases handle this differently; check before "
                "committing.",

                "Embedding versioning. When you upgrade your embedder, all stored vectors "
                "become incompatible with new query vectors. Plan for re-indexing. Some "
                "deployments run two indexes during transition.",

                "Cost. Memory dominates for HNSW (vector + graph). Storage dominates for "
                "IVF + PQ. Compute is shared. Compute total cost of ownership including "
                "infrastructure, not just vector database licenses.",

                "Quality monitoring. Recall@k against a held-out test set. Sample "
                "production queries; verify retrieval quality offline. Track over time; "
                "alert on regression. A degraded retriever silently degrades the entire "
                "downstream system.",
            ],
        },
        {
            "number": "12.10",
            "title": "Summary",
            "bullets": [
                "Vector databases store and search high-dimensional embeddings. They are "
                "the infrastructure for modern semantic search, recommendation, and RAG.",
                "Approximate nearest neighbor (ANN) algorithms trade small recall loss for "
                "orders of magnitude speedup over brute-force search.",
                "HNSW is the dominant algorithm for moderate scale; IVF + PQ scales to "
                "billions with much less memory.",
                "The vector database ecosystem includes FAISS (library), managed services "
                "(Pinecone, Weaviate, Qdrant, Milvus), and database extensions (pgvector, "
                "Elasticsearch). Choose based on scale, operational model, and integration "
                "needs.",
                "Hybrid search (BM25 + dense via RRF) almost always beats either alone.",
                "Reranking with cross-encoders refines retrieval at acceptable cost.",
                "Production concerns: updates, sharding, embedding versioning, monitoring.",
            ],
        },
    ],
    "further_reading": [
        "Malkov and Yashunin, 'Efficient and Robust Approximate Nearest Neighbor Search Using Hierarchical Navigable Small World Graphs' (2016).",
        "Johnson, Douze, Jégou, 'Billion-scale similarity search with GPUs' (2017). FAISS paper.",
        "Khattab and Zaharia, 'ColBERT' (2020). late-interaction retrieval.",
        "Aumüller et al., 'ANN-Benchmarks'. public benchmarking suite for ANN libraries.",
    ],
}
