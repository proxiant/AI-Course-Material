"""Part 4: RAG and Multimodal RAG."""

RAG = [
    ("What is Retrieval-Augmented Generation (RAG)?",
     [
        "RAG is an architecture that combines a retrieval system with a generative language "
        "model. At inference time, the user query triggers a search over an external "
        "knowledge base; the retrieved passages are inserted into the LLM's prompt; the "
        "LLM generates a response grounded in those passages.",
        "Why it matters: LLMs are limited to what they saw during training. Their knowledge "
        "is frozen, can be wrong, and cannot reference private or recent data. RAG patches "
        "this by giving the model up-to-date or proprietary information at inference time.",
        "Pipeline: (1) ingest documents and chunk them; (2) embed chunks and store in a "
        "vector database; (3) at query time, embed the query, retrieve top-k similar "
        "chunks; (4) construct a prompt with the retrieved chunks and the user question; "
        "(5) generate a response with the LLM.",
     ],
     ["11_rag.png"]),

    ("How does text generation differ between RAG and direct language models?",
     [
        "Direct LLM: the model generates from its parametric memory alone. It has whatever "
        "knowledge was baked in during pretraining. Cannot reference private data, recent "
        "events, or sources it has not seen. Prone to hallucination on facts it half-knows.",
        "RAG: the model generates conditioned on retrieved evidence. The retrieved passages "
        "ground the response. The model can cite sources. Knowledge can be updated by "
        "updating the index, not retraining the model. Hallucinations are reduced when the "
        "retrieved evidence is good.",
        "Quality tradeoff: RAG quality depends on both retrieval quality and generation "
        "quality. Bad retrieval leads to wrong context and poor answers. RAG also adds "
        "latency (retrieval step) and complexity (chunking strategy, index maintenance, "
        "reranking).",
     ]),

    ("What are common applications of RAG?",
     [
        "Customer support assistants over internal documentation. Legal research over "
        "case law and contracts. Medical question answering over clinical guidelines and "
        "literature. Enterprise search across wikis, code, and emails. Compliance question "
        "answering. Educational tutoring grounded in course material. Code assistants that "
        "look up repository-specific functions. Personal assistants over notes and calendar. "
        "Open-domain QA with grounding for factuality.",
     ]),

    ("How does RAG improve response accuracy?",
     [
        "Direct LLMs hallucinate when asked about specifics they only vaguely remember "
        "from pretraining. RAG narrows the scope: the model answers from a small, "
        "relevant set of passages, not from its full parametric memory.",
        "Specific improvements: (a) factuality (the model can quote sources); (b) recency "
        "(the index can be updated as the world changes without retraining); (c) "
        "domain coverage (the model never saw your private documents during pretraining "
        "but can use them at inference); (d) auditability (every response can be traced "
        "back to its retrieved sources).",
        "Effectiveness depends on retrieval quality. A precise, comprehensive retrieval "
        "stage is usually more important than the LLM choice for RAG quality.",
     ]),

    ("Why are retrieval models significant in RAG?",
     [
        "The retrieval model is the gate between the user's question and the LLM's "
        "context. If the right passages are retrieved, the LLM has a chance to produce a "
        "good answer. If the wrong passages are retrieved, the LLM either ignores them "
        "(unhelpful) or grounds in them (wrong answer with confidence).",
        "Retrieval quality drives almost every downstream metric: faithfulness, "
        "factuality, answer relevance, user satisfaction. Tuning the retrieval stage "
        "(embedder, chunking, hybrid sparse+dense, reranking) usually has higher ROI than "
        "tuning the generator.",
        "Practical implication: invest in retrieval evaluation. Build a held-out query set "
        "with known relevant passages; measure Recall@k, NDCG, MRR. Iterate on the "
        "pipeline until retrieval is solid before optimizing the generator.",
     ]),

    ("What data sources are typically used in RAG?",
     [
        "Unstructured text: internal wikis (Confluence, Notion), documentation, knowledge "
        "base articles, PDFs, emails, chat logs, customer support tickets.",
        "Semi-structured: HTML pages, markdown, JSON documents, API responses.",
        "Structured: SQL databases (via Text-to-SQL), data warehouses (BigQuery, Snowflake), "
        "spreadsheets, structured product catalogs.",
        "Multimedia: images with captions, video transcripts, audio recordings (via ASR), "
        "diagrams with extracted text.",
        "Code: source repositories indexed by file, function, or chunk; embedded with "
        "code-aware models.",
        "Live: real-time APIs (weather, stock, news), web search results, sensor streams. "
        "Cached with appropriate TTL.",
     ]),

    ("How does RAG contribute to conversational AI?",
     [
        "Conversational AI without grounding is limited to general knowledge. RAG lets a "
        "chatbot reference specific company policies, product details, account state, or "
        "regulatory rules. Each user turn triggers a retrieval over the relevant corpus.",
        "Multi-turn handling: queries are often follow-ups that require rewriting before "
        "retrieval. 'When was it founded?' depends on the previous turn. A query "
        "rewriter (small LLM call) produces a standalone query from the conversation "
        "history before retrieval.",
        "Memory: long-term conversational memory can itself be a RAG index. Past "
        "conversation summaries get embedded and retrieved when relevant to the current "
        "turn.",
        "Production patterns: RAG combined with tool use, persistent memory, and identity-"
        "aware retrieval is the dominant pattern for production conversational AI.",
     ]),

    ("What is the role of the retrieval component in RAG?",
     [
        "Retrieval selects the small subset of the knowledge base that goes into the LLM's "
        "prompt. Three roles in detail.",
        "Filtering: out of millions of documents, return the few dozen most relevant to "
        "the query. Reduces noise that would confuse the generator.",
        "Grounding: provides the evidence the LLM uses to construct its answer. The "
        "quality of grounding determines factuality.",
        "Auditability: each retrieved passage is a source the user can verify. RAG systems "
        "that surface citations let humans check the model's claims.",
     ]),

    ("How does RAG handle bias and misinformation?",
     [
        "RAG can both reduce and amplify bias depending on the corpus and pipeline.",
        "Reduces bias by: grounding answers in vetted sources rather than the model's "
        "(potentially biased) parametric memory; making the source of each claim "
        "auditable; allowing curation of the knowledge base.",
        "Amplifies bias when: the corpus itself is biased (the model now reliably parrots "
        "biased sources); retrieval is biased (e.g. always retrieves majority-perspective "
        "documents and ignores minority views); the generator was trained with bias and "
        "selectively uses retrieved evidence.",
        "Mitigations: curate the corpus, audit for representation, use diversity in "
        "retrieval (avoid only top-k from one source), measure bias on a held-out test "
        "set, allow users to flag biased outputs.",
     ]),

    ("What are the benefits of RAG over other NLP techniques?",
     [
        "Vs. pure prompting: RAG can access information not in the prompt or in the "
        "model's training data. No prompt length limit on knowledge base size.",
        "Vs. fine-tuning: RAG updates by re-indexing, not retraining. Knowledge updates "
        "are fast and cheap. The model can cite sources. Fine-tuning bakes knowledge into "
        "weights opaquely.",
        "Vs. building a custom model: RAG layers on top of an existing strong LLM. No "
        "training cost. Faster time-to-value.",
        "Vs. search alone: search returns documents; the user has to read and synthesize. "
        "RAG returns synthesized answers grounded in those documents. Better for "
        "conversational and direct-answer use cases.",
     ]),

    ("Describe a scenario where RAG is particularly useful.",
     [
        "Enterprise customer support: a SaaS company has 50K internal documentation pages, "
        "10K Confluence articles, and 500K resolved support tickets. New tickets arrive at "
        "thousands per day. A direct LLM cannot answer specific questions about features, "
        "edge cases, or recent bug fixes.",
        "RAG solution: index all docs, articles, and tickets with a domain-tuned embedder. "
        "At ticket creation, retrieve top relevant passages; assemble a prompt; have an "
        "LLM draft a response that cites sources. Human support reviews and edits before "
        "sending. Outcome: support tickets resolved 30-50% faster; agent satisfaction "
        "improves because they get a strong starting draft.",
        "Why RAG wins here: knowledge changes daily (new features, new bugs); auditability "
        "matters (legal and brand-safety review); fine-tuning would lag behind reality.",
     ]),

    ("How does RAG integrate with ML pipelines?",
     [
        "Ingestion pipeline: ETL job pulls documents from source systems (S3, databases, "
        "APIs), chunks them, embeds them, writes to the vector index. Runs continuously "
        "or on schedule. Same patterns as a feature engineering pipeline.",
        "Serving pipeline: API service receives query, embeds it, calls the vector "
        "database for retrieval, optionally reranks, constructs prompt, calls the LLM, "
        "returns response with citations. Latency-sensitive.",
        "Evaluation: held-out test sets for retrieval quality (Recall@k, NDCG) and "
        "generation quality (Ragas, LLM-as-judge). Continuous evaluation in production via "
        "sampled traffic.",
        "Monitoring: track retrieval recall, generation latency, citation usage, user "
        "feedback signals. Alert on drift (corpus changes, query distribution shift).",
        "Standard tools: LangChain, LlamaIndex for orchestration; Pinecone, Weaviate, "
        "Qdrant, Milvus for vector storage; Ragas for evaluation; OpenTelemetry for "
        "observability.",
     ]),

    ("What challenges does RAG solve in NLP?",
     [
        "Knowledge staleness: pretrained LLMs are stuck at their training cutoff. RAG "
        "lets them answer questions about new information.",
        "Hallucination: ungrounded generation is the source of many factual errors. "
        "Grounding in retrieved evidence reduces this.",
        "Domain specialization: training a model on every enterprise's private data is "
        "impractical. RAG separates knowledge from model and lets each enterprise plug in "
        "its data.",
        "Auditability and compliance: regulated industries need to trace outputs back to "
        "sources. RAG citations support audit trails.",
        "Cost: fine-tuning per knowledge update is expensive. Re-indexing is cheap.",
     ]),

    ("How does RAG keep retrieved information up to date?",
     [
        "Re-indexing pipelines: when source documents change, re-embed and update the "
        "vector store. Patterns: full re-index on a schedule (nightly, weekly); "
        "incremental re-index (only changed documents); event-driven (re-index when source "
        "system signals a change).",
        "Time-aware retrieval: store creation/update timestamps on each chunk; weight "
        "recency in scoring or filter to recent documents only.",
        "TTL on cached data: for live API-backed sources (news, prices), use short TTLs "
        "or pass-through to the live API rather than caching in the vector store.",
        "Versioning: track which version of each document is in the index. Roll back if "
        "an ingestion job introduces bad data.",
        "Detection: monitor for stale answers via user feedback signals or periodic "
        "ground-truth checks against the source system.",
     ]),

    ("How are RAG models trained?",
     [
        "RAG models can be trained end-to-end or assembled from pretrained components.",
        "Component-wise (most common in practice): use a pretrained sentence embedder for "
        "retrieval and a pretrained LLM for generation. No additional training needed. "
        "Fine-tune the embedder on in-domain (query, relevant-doc) pairs to improve "
        "retrieval recall. Fine-tune the LLM on grounded-generation examples to improve "
        "faithfulness.",
        "End-to-end (original RAG paper): jointly train the retriever and the generator "
        "with marginal likelihood over retrieved documents. The retriever learns to "
        "retrieve documents that help generation. Expensive but produces strongly coupled "
        "components.",
        "REALM, DPR, RAG, FiD, RETRO, Self-RAG, Atlas are research benchmarks worth "
        "studying. Production systems usually start with component-wise and tune from "
        "there.",
     ]),

    ("What is the impact of RAG on LLM efficiency?",
     [
        "Latency: RAG adds retrieval latency (typically 50-300 ms) and may increase "
        "generation latency because the prompt is longer.",
        "Cost: longer prompts mean more input tokens, which dominate LLM cost for many "
        "workloads. Mitigations: aggressive reranking to send fewer chunks, prompt "
        "caching for repeated context.",
        "Throughput: RAG is throughput-friendly because retrieval is cheap and "
        "parallelizable. The bottleneck is the LLM.",
        "Net efficiency: for tasks RAG enables (questions over private docs, recent "
        "events), RAG is dramatically cheaper than fine-tuning. For tasks the LLM could "
        "handle alone, RAG is overhead. Apply RAG only where it adds clear value.",
     ]),

    ("How does RAG differ from Parameter-Efficient Fine-Tuning (PEFT)?",
     [
        "RAG provides knowledge externally via retrieval. PEFT modifies a small number of "
        "model parameters to teach the model new behavior or knowledge.",
        "When to use RAG: knowledge changes often, answers must cite sources, domain has "
        "lots of factual content. Auditability matters.",
        "When to use PEFT: behavior change (tone, persona, format), narrow task "
        "specialization, latency-sensitive (no retrieval step). Knowledge is stable.",
        "Combine: many production systems use both. PEFT teaches the model the right "
        "format, persona, and reasoning patterns; RAG provides factual grounding at "
        "inference. The combination beats either alone for many enterprise tasks.",
     ],
     ["12_adaptation_ladder.png"]),

    ("How can RAG enhance human-AI collaboration?",
     [
        "Citations: RAG outputs cite sources, letting humans verify claims and learn from "
        "the underlying material. This shifts AI from 'magic answer' to 'researcher who "
        "shows their work.'",
        "Trust calibration: users see what evidence the model used. If the evidence is "
        "weak, the user can override or seek more sources.",
        "Iteration: humans can refine queries based on retrieved evidence. 'These passages "
        "aren't quite what I meant. Let me rephrase.'",
        "Editing workflows: in customer support and content creation, RAG drafts grounded "
        "responses; humans review and edit. The human-AI pair is faster than either alone.",
        "Knowledge discovery: users find related documents they didn't know existed. RAG "
        "becomes a discovery tool, not just an answer tool.",
     ]),

    ("Explain the technical architecture of a RAG system.",
     [
        "Ingestion: connectors pull documents from sources (S3, GitHub, Notion). Document "
        "loaders parse formats (PDF, HTML, DOCX). Chunkers split into 200-1000 token "
        "chunks with overlap or semantic boundaries. Embedder generates dense vectors. "
        "Vector store persists with metadata.",
        "Retrieval: query embedder produces query vector. Vector store performs ANN search "
        "for top-k similar chunks. Optional: hybrid with BM25 via reciprocal rank fusion. "
        "Optional: cross-encoder reranker rescores the top candidates.",
        "Generation: prompt template combines retrieved chunks with the user query. LLM "
        "generates the response, optionally with citations. Post-processing: format "
        "citations, run guardrails, log for evaluation.",
        "Cross-cutting: caching (semantic cache for repeated queries), observability "
        "(trace each retrieval and generation), evaluation (sample traffic for offline "
        "scoring), security (PII handling, prompt injection defense).",
     ],
     ["11_rag.png"]),

    ("How does RAG maintain context in a conversation?",
     [
        "Query rewriting: a small LLM call rewrites the latest user turn into a standalone "
        "query using the conversation history. 'When was it founded?' becomes 'When was "
        "Acme Corp founded?' before retrieval.",
        "Conversation memory as a RAG source: past turns or summaries get embedded and "
        "indexed. Long conversations no longer fit in the prompt, but their key points "
        "can be retrieved when relevant.",
        "Sliding context window: maintain a rolling window of recent turns plus a "
        "summarized history of earlier turns. Combines short-term verbatim memory with "
        "long-term semantic memory.",
        "Session-level retrieval state: cache documents already retrieved this session so "
        "the model doesn't keep re-introducing them.",
     ]),

    ("What are the limitations of RAG?",
     [
        "Quality ceiling: RAG cannot exceed the quality of its retrieval. If relevant "
        "documents exist but retrieval misses them, the answer suffers.",
        "Latency: extra round-trip to the vector store. Hard to keep total latency below "
        "1 second for complex pipelines.",
        "Cost: longer prompts mean more tokens. For high-volume applications, RAG can be "
        "more expensive than a fine-tuned model.",
        "Multi-hop questions: simple top-k retrieval struggles with questions that need "
        "to combine evidence from multiple unrelated documents.",
        "Schema mismatch: structured questions over tabular data are not RAG's strength "
        "(use Text-to-SQL instead).",
        "Index maintenance: ingestion pipelines need monitoring; stale or incorrect "
        "indexes silently degrade quality.",
     ]),

    ("How does RAG handle complex queries requiring multi-hop reasoning?",
     [
        "Vanilla RAG often fails on multi-hop. Mitigations: query decomposition, "
        "iterative retrieval, GraphRAG.",
        "Query decomposition: an LLM splits the complex query into sub-queries. Each "
        "sub-query retrieves; partial answers feed the next sub-query. 'What is the GDP "
        "of the country where Apple is headquartered?' becomes (1) where is Apple "
        "headquartered, (2) what is the GDP of [USA].",
        "Iterative agentic RAG: the model retrieves, generates partial answer, decides "
        "what to retrieve next based on what it now knows. Continues until the question "
        "is answered or a step limit is reached.",
        "GraphRAG: build a knowledge graph from the corpus. Multi-hop queries traverse "
        "the graph rather than relying on a single vector similarity. Microsoft GraphRAG "
        "and LightRAG are reference implementations.",
        "HyDE (Hypothetical Document Embeddings): generate a plausible answer first; "
        "embed and use as the retrieval query. Closes the gap between question style and "
        "document style.",
     ]),

    ("Discuss the role of knowledge graphs in RAG.",
     [
        "Knowledge graphs encode entities and their relationships explicitly. A RAG "
        "system can use a graph to follow chains of relationships, find structural "
        "patterns, and answer questions that pure text retrieval misses.",
        "GraphRAG pattern (Microsoft): extract triplets from documents with an LLM, build "
        "a graph, detect communities, summarize each community. At query time, retrieve "
        "relevant community summaries (for global questions) or entity neighborhoods (for "
        "specific questions).",
        "Hybrid: use vector retrieval for fact-style questions and graph traversal for "
        "relational or multi-hop questions. A router classifies the question and "
        "dispatches accordingly.",
        "Tradeoffs: graph construction is expensive (one LLM call per chunk). Graph "
        "queries can be slow without good indexing. Maintenance is harder than a flat "
        "vector index. Worth it when multi-hop reasoning matters.",
     ]),

    ("What are the ethical considerations when implementing RAG?",
     [
        "Source bias: a corpus dominated by one perspective produces biased outputs even "
        "if the model is unbiased. Audit the corpus for representation.",
        "PII and privacy: indexed documents may contain personal data. Apply PII "
        "detection, redaction, and access controls. Ensure retrieval respects "
        "authorization (one user cannot retrieve another user's documents).",
        "Misinformation: RAG can authoritatively present misinformation if the corpus "
        "contains it. Curate trusted sources; flag low-confidence retrievals.",
        "Copyright: indexing third-party content may have licensing implications. Track "
        "data provenance and licenses.",
        "Transparency: surface sources to users. Disclose that responses are AI-generated.",
        "Hallucination risk: even with citations, models can misrepresent sources. Test "
        "for grounding faithfulness, not just citation presence.",
     ]),

    ("What is multimodal RAG, and how does it differ from text-only RAG?",
     [
        "Multimodal RAG retrieves and reasons over data from multiple modalities: text, "
        "images, tables, audio, video. The retrieval may return mixed-modality results; "
        "the generator may be a multimodal LLM that takes images and text as input.",
        "Architectures: (a) shared embedding space (CLIP-style) for images and text, with "
        "a multimodal LLM (GPT-4V, Gemini) for generation; (b) per-modality indexes with "
        "a router that picks the right one; (c) text-only retrieval over image captions "
        "and OCR with a text-only LLM (cheaper but loses visual nuance).",
        "Differences from text-only RAG: more chunking choices (how to chunk a "
        "document with images); more retrieval choices (which modalities to retrieve for "
        "a given query); generation depends on a multimodal LLM; evaluation needs "
        "multimodal metrics.",
     ]),

    ("How can multimodal data improve RAG?",
     [
        "Richer context: a financial report's text plus its charts; a medical record's "
        "text plus images; a product page's description plus photos. Retrieving across "
        "modalities gives the LLM the full picture.",
        "Cross-modal queries: 'find me products that look like this image' or 'show me "
        "the trend in this chart.' Pure text retrieval cannot answer these.",
        "Better grounding: visual evidence is harder to misinterpret than paraphrased "
        "text. A retrieved chart that shows the trend is more faithful than a text "
        "description of it.",
        "User flexibility: users can ask questions with mixed inputs (text query + image), "
        "matching natural human communication.",
     ]),

    ("What are challenges of implementing multimodal RAG?",
     [
        "Alignment across modalities: text and image embeddings must live in a comparable "
        "space. Use CLIP-style embedders or modality-specific embedders with explicit "
        "alignment.",
        "Heterogeneous chunking: a PDF page contains text, tables, and images. How to "
        "split? Often each non-text element becomes its own chunk with surrounding text "
        "as context.",
        "Generation cost: multimodal LLMs are typically more expensive and slower than "
        "text-only LLMs.",
        "Evaluation: no single metric covers retrieval, generation, and modality "
        "interaction. Combine per-modality metrics with end-task metrics.",
        "Data quality: paired multimodal data is scarce. Web-scraped pairs are noisy. "
        "Curate carefully.",
        "Privacy: images may contain identifiable information (faces, addresses on "
        "documents, location metadata). Apply detection and redaction.",
     ]),

    ("Describe a real-world multimodal RAG application.",
     [
        "Healthcare diagnostic assistance: ingest patient records (text), lab results "
        "(tables), medical imaging (X-rays, MRIs), and clinical literature. At consult "
        "time, retrieve relevant prior cases, imaging, and literature for the current "
        "presentation. A multimodal LLM (GPT-4V or Med-PaLM) drafts a differential "
        "diagnosis grounded in retrieved evidence.",
        "Benefits over unimodal: doctors see the patient's record, similar prior images, "
        "and relevant literature together. Decisions are better calibrated. Drafts save "
        "documentation time. Citations preserve the audit trail required for regulated "
        "use.",
        "Other domains: e-commerce (text + images for product search), education (text + "
        "video + diagrams), legal (text + scanned exhibits), real estate (text + photos + "
        "floorplans).",
     ]),

    ("What evaluation metrics suit multimodal RAG?",
     [
        "Retrieval metrics, per modality: Recall@k, NDCG, MRR computed separately for "
        "text and image (and other modality) retrieval. Also cross-modal: image-to-text "
        "Recall@k, text-to-image Recall@k.",
        "Generation metrics: BLEU/ROUGE for text generation. CIDEr for caption-style "
        "outputs. CLIPScore for text-image alignment.",
        "End-to-end: Ragas faithfulness (extended to handle visual claims), answer "
        "relevance, context precision/recall.",
        "Multimodal-specific: visual question answering accuracy, citation accuracy "
        "(does the cited image actually contain the referenced content?), modality "
        "coverage (did the system use the right modality for the query?).",
        "Human evaluation: multimodal generative outputs almost always need humans in the "
        "loop for final quality judgment.",
     ]),

    ("How would you design a multimodal RAG for a specific industry?",
     [
        "Take healthcare as an example. Components: (1) ingestion pipeline for EHRs "
        "(text), DICOM imaging (medical images), lab CSVs (structured); (2) modality-"
        "specific embedders (clinical-text encoder, medical-image encoder, table encoder); "
        "(3) per-modality vector indexes with PHI-aware access control; (4) query router "
        "that classifies the query and picks the right index(es); (5) retrieval with "
        "reranking; (6) multimodal LLM with HIPAA-compliant deployment; (7) citation and "
        "explanation layer; (8) human-in-the-loop verification before any clinical use.",
        "Cross-cutting: PHI redaction at ingestion and serving, audit logs for every "
        "retrieval, role-based access control, evaluation set built with clinician "
        "annotation, monitoring for drift and hallucination.",
     ]),

    ("Techniques for aligning and integrating modalities in a RAG pipeline?",
     [
        "Shared embedding space (CLIP-style): one embedder per modality, trained jointly "
        "with contrastive loss. Image and text embeddings are directly comparable.",
        "Cross-modal translation: convert one modality to another at ingestion. Generate "
        "captions for images; extract text from documents via OCR; transcribe audio. "
        "Then index everything as text. Cheap, but loses non-textual nuance.",
        "Late fusion: retrieve from each modality separately, then combine results via "
        "reciprocal rank fusion or weighted reranking.",
        "Early fusion: train a single multimodal encoder that takes inputs from multiple "
        "modalities and produces a joint representation.",
        "Hybrid: most production systems combine approaches. Caption images for fast "
        "text-only retrieval, but also keep the original images for visual reranking and "
        "for the multimodal generator.",
     ]),

    ("How do you evaluate generated content in multimodal RAG?",
     [
        "Reference-based metrics: BLEU/ROUGE for text outputs vs reference text. CIDEr "
        "for image captioning style. BLEURT and BERTScore as embedding-based alternatives.",
        "Grounding metrics: faithfulness (every claim in the output supported by retrieved "
        "evidence). Citation accuracy (cited documents actually contain the claim). "
        "Modality grounding (visual claims supported by the cited image).",
        "Task-specific: VQA exact match for question-answer pairs. Slot-fill accuracy "
        "for structured extraction. Click-through or engagement for recommendation tasks.",
        "Human evaluation: panel ratings on relevance, accuracy, helpfulness. Especially "
        "important for open-ended generation.",
        "User-facing feedback signals: thumbs up/down, regenerate rate, time spent "
        "reading. Aggregate over time and segment by query type.",
     ]),

    ("What challenges arise when scaling multimodal RAG to large datasets?",
     [
        "Storage: image and video embeddings are not larger than text embeddings, but "
        "the raw assets are. Plan for multi-TB storage at scale.",
        "Latency: retrieving and processing visual content takes longer than text. Use "
        "lazy loading, caching, and reranking to keep P95 manageable.",
        "Index maintenance: when source images change, embeddings must be recomputed. "
        "Plan incremental updates.",
        "Cost: multimodal LLMs are 5-20x more expensive per query than text LLMs. Use "
        "them only when the query genuinely needs visual reasoning.",
        "Quality at scale: noisy data drowns out signal as the index grows. Curate "
        "ingestion sources. Apply quality filters.",
        "Evaluation at scale: cannot human-review every query. Build automated "
        "evaluations and sample for human review.",
     ]),

    ("Give an example of an ethical concern in multimodal RAG, and how to mitigate it.",
     [
        "Example: a medical multimodal RAG retrieves images and records. A breach of "
        "access control exposes a patient's images and history to an unauthorized user. "
        "Or: the system reliably retrieves images of one demographic when given clinical "
        "queries about it, reinforcing stereotypes in case reviews.",
        "Mitigations for the breach: role-based access control at the retrieval layer, "
        "not just the application layer. Audit logs for every retrieval. PHI redaction "
        "for any image leaving the system. Encryption at rest and in transit.",
        "Mitigations for bias: train the embedder on a demographically balanced corpus. "
        "Audit retrievals for demographic skew. Add diversity-aware reranking. Surface "
        "the limitation to users and clinicians.",
        "Process: ethics review before deployment, with clinical and patient "
        "representatives. Continuous monitoring after deployment.",
     ]),
]
