"""Weekly project briefs for the RAG bootcamp."""

PROJECTS = {
    1: {
        "title": "Production-grade simple RAG with baseline eval",
        "summary": "Build a 200-line RAG over a 2000-document corpus. Use FAISS, a small embedder, and a generator. Include a 30-question eval set with gold answers and an automated eval harness.",
        "tools": ["FAISS", "bge-small or sentence-transformers", "An LLM API"],
        "deliverables": [
            "rag.py with load, chunk, embed, index, retrieve, generate",
            "evals/test_set.json with 30 questions",
            "evals/run.py that computes recall@8 and answer F1",
            "README with reproducible setup",
            "One-page failure analysis on the 5 worst answers",
        ],
        "rubric_extra": "Bonus 5 points for measuring per-query latency and reporting P50 and P95.",
    },
    2: {
        "title": "Contrastive embedder fine-tuning",
        "summary": "Fine-tune a sentence embedder on a domain corpus with InfoNCE. Mine hard negatives. Evaluate retrieval improvement.",
        "tools": ["sentence-transformers", "Domain corpus shipped with the lab"],
        "deliverables": [
            "Training script with InfoNCE and configurable temperature",
            "Hard-negative miner",
            "Eval on STS-B and the domain retrieval set",
            "Anisotropy measurement before and after",
            "Recommendation on temperature for this corpus",
        ],
        "rubric_extra": "Bonus 5 points for ablating temperature across {0.05, 0.1, 0.2}.",
    },
    3: {
        "title": "Four chunking strategies head to head",
        "summary": "Implement fixed-size, semantic, late, and contextual chunking on the same corpus. Compare retrieval recall@10 and end-to-end answer quality.",
        "tools": ["Embedder with long-context support", "An LLM API for contextual summaries"],
        "deliverables": [
            "Four chunker implementations with shared interface",
            "Indexed corpus for each",
            "100-query eval set with gold answers",
            "Comparison table with recall@10 and answer F1",
            "Recommendation paragraph keyed to corpus characteristics",
        ],
        "rubric_extra": "Bonus 5 points for adding a hierarchical (mother-child) strategy as a fifth option.",
    },
    4: {
        "title": "Four-stage retrieval funnel end to end",
        "summary": "Build the four-stage funnel (sparse + dense, Matryoshka prune, ColBERT, cross-encoder) on a 100K-document corpus. Tune candidate counts. Beat dense-only baseline by at least 5 points recall@5.",
        "tools": ["Pyserini (BM25)", "Matryoshka embedder", "RAGatouille (ColBERT)", "sentence-transformers cross-encoder"],
        "deliverables": [
            "Full funnel implementation",
            "Dense-only baseline",
            "Eval on a 200-question set",
            "Latency breakdown per stage",
            "Tuning writeup with the rationale for each candidate count",
        ],
        "rubric_extra": "Bonus 5 points for measuring marginal contribution of each stage via ablation.",
    },
    5: {
        "title": "Multimodal RAG with CLIP and BLIP-2",
        "summary": "Build a multimodal RAG over a corpus of 5000 images and their captions. Support text-to-image, image-to-image, and image-to-text retrieval. Use BLIP-2 for VQA on retrieved images.",
        "tools": ["open_clip", "Lavis (BLIP-2)", "FAISS"],
        "deliverables": [
            "Unified embedding index for images and text",
            "Three retrieval modes",
            "VQA pipeline using BLIP-2",
            "Eval on 30 multimodal questions",
            "Note on what BLIP-2 gets wrong",
        ],
        "rubric_extra": "Bonus 5 points for comparing CLIP and BLIP-2 image embeddings as the retrieval backbone.",
    },
    6: {
        "title": "DSPy beats hand-crafted prompt",
        "summary": "Pick a 7-class classification task. Write a hand-crafted CO-STAR baseline. Optimize with DSPy MIPRO. Beat the baseline by at least 5 percentage points.",
        "tools": ["DSPy", "OpenAI or Anthropic API"],
        "deliverables": [
            "CO-STAR baseline prompt with documented fields",
            "DSPy Signature and Module",
            "MIPRO optimization trace",
            "Eval comparison with confidence intervals",
            "Writeup on what MIPRO discovered",
        ],
        "rubric_extra": "Bonus 5 points for adding a GEPA run and comparing all three.",
    },
    7: {
        "title": "RAPTOR vs GraphRAG on multi-hop questions",
        "summary": "Build a RAPTOR pipeline and a GraphRAG pipeline on the same 5K-document corpus. Compare on 50 multi-hop questions for quality, ingestion cost, and query latency.",
        "tools": ["RAPTOR reference impl", "Neo4j or Memgraph", "GraphRAG reference impl"],
        "deliverables": [
            "Both pipelines built and indexed",
            "50-question multi-hop eval set",
            "Cost breakdown for ingestion and query",
            "Comparison table",
            "Recommendation by corpus type",
        ],
        "rubric_extra": "Bonus 5 points for adding LightRAG as a third comparison.",
    },
    8: {
        "title": "Production guardrail and grounding pipeline",
        "summary": "Build a four-stage guardrail pipeline (syntax, PII, toxicity, intent) and an NLI-based response grounding checker. Measure throughput and false-positive rates. Hit a 3-second P95 budget end to end.",
        "tools": ["Presidio (PII)", "DeBERTa-large-mnli (NLI)", "Toxicity model"],
        "deliverables": [
            "Pipeline implementation with early exits",
            "1000-input throughput test",
            "False-positive and false-negative analysis",
            "P95 latency report",
            "Tuning recommendation with explicit threshold values",
        ],
        "rubric_extra": "Bonus 5 points for adding a prompt-injection adversarial test suite.",
    },
    9: {
        "title": "Enterprise enrichment: factoids, HyDE, semantic cache",
        "summary": "Add factoid and QA-pair derivative artifacts to a RAG corpus. Add HyDE on the query side. Build a semantic cache layer. Measure cumulative cost reduction and quality impact.",
        "tools": ["LLM API for factoid generation", "Existing RAG stack", "Cache vector store"],
        "deliverables": [
            "Enriched corpus with factoids and QA pairs",
            "HyDE pipeline integrated",
            "Semantic cache with tuned threshold",
            "Cost report: before vs after",
            "Quality report on the same eval set",
        ],
        "rubric_extra": "Bonus 5 points for adding hard-negative mining and quantifying embedder improvement.",
    },
    10: {
        "title": "Agentic RAG + Text-to-SQL on a real schema",
        "summary": "Build an agentic RAG that includes a Text-to-SQL path for structured questions. Use MCP for tool exposure. Compare to static RAG on a mixed test set.",
        "tools": ["Google ADK or LangGraph", "FastMCP", "A sample SQL database"],
        "deliverables": [
            "Agentic loop with structured and unstructured tools",
            "Text-to-SQL pipeline with schema retrieval",
            "MCP tool server",
            "Eval on 100 mixed questions",
            "Cost-quality comparison vs static RAG",
        ],
        "rubric_extra": "Bonus 5 points for adding a small CTE library and measuring SQL complexity reduction.",
    },
    11: {
        "title": "Text-to-SQL fine-tuning with LoRA and GRPO",
        "summary": "Fine-tune a small base model on a Text-to-SQL task. First with LoRA SFT. Then add a GRPO pass using execution accuracy as the verifier. Compare to few-shot baseline.",
        "tools": ["TRL with GRPO", "PEFT", "Spider or Bird dataset"],
        "deliverables": [
            "Few-shot baseline",
            "LoRA SFT checkpoint and eval",
            "GRPO checkpoint and eval",
            "Comparison table on exact match and execution accuracy",
            "Cost-time analysis",
        ],
        "rubric_extra": "Bonus 5 points for analyzing where GRPO helps vs hurts at the query-type level.",
    },
    12: {
        "title": "Capstone: full RAG eval and improvement plan",
        "summary": "Take the RAG you have built across the bootcamp. Run a comprehensive eval (Ragas, LLM-as-judge, RGB-style robustness). Identify the biggest weakness. Implement one targeted improvement. Re-evaluate.",
        "tools": ["Ragas", "LLM judge", "Your full RAG stack"],
        "deliverables": [
            "Full eval report on baseline",
            "Identified biggest weakness with evidence",
            "One targeted improvement implemented",
            "Re-evaluation report",
            "Written reflection on what surprised you",
        ],
        "rubric_extra": "Bonus up to 10 points for novelty and depth of the improvement.",
    },
}


# Reference solution sketches, one per week: a concrete approach paragraph
# plus an implementation outline. Rendered only in the solution documents.
REFERENCE_SOLUTIONS = {
    1: {
        "approach": (
            "The reference keeps rag.py under 200 lines by composing five "
            "pure functions (load, chunk, embed, index, retrieve, generate) "
            "driven by one config dict. Chunks are 500 tokens with 50-token "
            "overlap, embedded with bge-small-en-v1.5, and stored in a flat "
            "FAISS inner-product index; 2,000 documents do not need ANN. "
            "The eval harness reads recall@8 as retrieval health and "
            "token-level F1 against gold answers as generation health, and "
            "the failure analysis traces each of the 5 worst answers back "
            "to whether the gold chunk was even retrieved."
        ),
        "outline": [
            "Normalize embeddings and use IndexFlatIP so similarity is exact cosine; persist the index plus a chunk-id-to-text map.",
            "retrieve(query, k=8) embeds the query once and returns (chunk, score) pairs; generate() formats them into a numbered context block.",
            "evals/run.py loads test_set.json, computes recall@8 and answer F1, and writes results.json with per-query rows.",
            "Wrap retrieve and generate in time.perf_counter timers and report P50/P95 in the README for the bonus.",
            "Classify each bad answer as a retrieval miss (gold chunk absent) or a generation miss (gold chunk present, wrong answer).",
        ],
    },
    2: {
        "approach": (
            "Start from all-MiniLM-L6-v2 and fine-tune with "
            "MultipleNegativesRankingLoss (the sentence-transformers form "
            "of InfoNCE) at temperature 0.05 on the domain pairs. Hard "
            "negatives come from the model itself: retrieve top 20 per "
            "training query with the pretrained checkpoint, drop gold "
            "positives, and sample from ranks 5 to 20. Anisotropy is "
            "measured as mean pairwise cosine over 5,000 random corpus "
            "sentences, before and after fine-tuning, alongside STS-B "
            "Spearman and domain recall@10."
        ),
        "outline": [
            "DataLoader yields (query, positive, hard_negative) triples; in-batch negatives still apply on top of the mined ones.",
            "Train 2 epochs, batch 64, lr 2e-5, warmup 10 percent; checkpoint per epoch and keep the best by dev recall@10.",
            "Eval script reports STS-B Spearman, domain recall@10, and the anisotropy proxy in one table.",
            "Temperature ablation {0.05, 0.1, 0.2} reuses the same loader with the loss scale parameter swapped.",
        ],
    },
    3: {
        "approach": (
            "All four chunkers implement chunk(doc) -> list[Chunk] so the "
            "indexing and eval code is shared. Fixed-size uses 400 tokens "
            "with 50 overlap; semantic splits on embedding-similarity dips "
            "between adjacent sentences; late chunking embeds the full "
            "document with a long-context embedder and mean-pools token "
            "vectors per chunk span; contextual chunking prepends a "
            "one-sentence document summary (one LLM call per chunk, cached "
            "to disk). The comparison table reports recall@10, mean chunk "
            "length, ingestion cost in dollars, and answer F1 on the same "
            "100-query set."
        ),
        "outline": [
            "Define Chunk(text, doc_id, span) and one build_index(chunks) used by all four strategies.",
            "Cache contextual summaries as {doc_id}/{chunk_idx}.txt so re-runs cost zero LLM calls.",
            "Run the 100-query set through a single eval loop parameterized by index name.",
            "Recommendation paragraph keys the winner to corpus traits: section-structured docs favor contextual, clean prose favors semantic.",
            "Bonus mother-child strategy reuses the week's hierarchical lab code with 1,000/250-token levels.",
        ],
    },
    4: {
        "approach": (
            "The funnel is four composable stages with explicit candidate "
            "counts: BM25 (Pyserini) and dense (bge-m3) each return 500, "
            "the union deduplicates to about 900; a 64-dim Matryoshka "
            "prune cuts to 200; ColBERT (RAGatouille) rescores to 50; a "
            "cross-encoder produces the final 10. Each stage logs wall "
            "time and candidate counts so the latency breakdown falls out "
            "of the run log. The dense-only baseline is the same bge-m3 "
            "index returning top 10 directly."
        ),
        "outline": [
            "Stage interface: rank(query, candidates) -> scored candidates, so stages can be dropped for ablation.",
            "Tune counts by sweeping stage budgets on a 50-query dev split before touching the 200-question eval.",
            "Report recall@5, P50/P95 latency, and per-query cost for funnel vs baseline.",
            "Ablation table removes one stage at a time to show marginal contribution (the bonus).",
        ],
    },
    5: {
        "approach": (
            "One CLIP ViT-B/32 model embeds both sides: image embeddings "
            "are indexed in FAISS, captions in a parallel text index. "
            "Text-to-image queries embed the text and search the image "
            "index; image-to-image queries embed the query image; "
            "image-to-text searches captions. For VQA, the top retrieved "
            "image goes to BLIP-2 (Flan-T5-XL backbone) with the user "
            "question. The 20-pair hand-curated eval scores hit@5 per "
            "retrieval direction, and the report contrasts failure modes "
            "(CLIP misses text inside images; BLIP-2 struggles with "
            "counting)."
        ),
        "outline": [
            "Normalize CLIP embeddings and use inner product; one index for images, one for captions.",
            "search(query, mode) dispatches on text-to-image, image-to-image, image-to-text.",
            "BLIP-2 wrapper takes (image, question) and returns the answer plus generation time.",
            "Eval JSON lists 20 queries with expected results; report hit@5 per direction and 3 failure screenshots.",
        ],
    },
    6: {
        "approach": (
            "The task is 7-class support-ticket classification. The "
            "baseline is a hand-written CO-STAR prompt with three few-shot "
            "examples, scored on a frozen 200-example test set. The DSPy "
            "version defines a Signature (ticket -> label), wraps it in "
            "ChainOfThought, and optimizes with MIPRO using a 150-example "
            "train split and accuracy as the metric. The writeup diffs the "
            "baseline and optimized prompts and attributes the gain: "
            "usually better demonstrations, not better instructions."
        ),
        "outline": [
            "Freeze train/dev/test splits in JSON before any prompting so the comparison is honest.",
            "Baseline CO-STAR prompt is versioned in prompts/baseline.txt with its test accuracy.",
            "MIPRO run uses 20 trials, max 3 bootstrapped demos, temperature 0 scoring.",
            "Report accuracy per class plus the confusion pairs MIPRO fixed; require the 5-point gain on the same test set.",
        ],
    },
    7: {
        "approach": (
            "Both pipelines ingest the same 5K-document corpus. RAPTOR "
            "embeds all chunks, clusters with UMAP plus GMM, summarizes "
            "each cluster with one LLM call, and recurses for 3 levels; "
            "the collapsed tree is indexed in FAISS. GraphRAG extracts "
            "triplets per chunk, resolves entities, runs Leiden community "
            "detection, and summarizes communities. The 50-question "
            "multi-hop eval is scored by an LLM judge with the order of "
            "system outputs randomized, and the report tables quality, "
            "ingestion dollars, and P50 query latency side by side."
        ),
        "outline": [
            "Pin chunking (400 tokens) and the embedder so the only variable is the retrieval architecture.",
            "Log every LLM call with token counts during ingestion; ingestion cost comes from the log, not estimates.",
            "RAPTOR query mode: collapsed-tree similarity over all nodes; GraphRAG query mode: local search over entities plus community summaries.",
            "Judge prompt scores answers 1 to 5 on correctness and completeness with the gold answer shown.",
        ],
    },
    8: {
        "approach": (
            "The guardrail pipeline is four stages with a shared "
            "GuardResult(pass, reason, latency_ms) interface and "
            "early-exit chaining: syntax and size checks, Presidio PII "
            "detection and redaction, a toxicity classifier, and an "
            "intent classifier that keeps only in-scope questions. The "
            "grounding checker splits the draft answer into atomic claims "
            "with one LLM call, scores each claim against the retrieved "
            "context with DeBERTa-large-mnli, and rejects answers whose "
            "minimum entailment falls below 0.7. Throughput and "
            "false-positive rates come from a 1,000-input labeled stream."
        ),
        "outline": [
            "Each stage is a class with check(text) -> GuardResult; the chain stops at the first fail.",
            "Threshold tuning sweeps the toxicity and NLI cutoffs against the labeled set and plots FP rate vs catch rate.",
            "Batch NLI scoring (claims x contexts) keeps the verifier inside the P95 budget.",
            "Report throughput (inputs/s), per-stage latency, FP and FN rates, and the end-to-end P95.",
        ],
    },
    9: {
        "approach": (
            "Enrichment runs as three measured increments over the same "
            "RAG stack. First, factoids: 5 per document with a "
            "JSON-output prompt, embedded and indexed alongside the "
            "chunks with a type tag. Second, QA pairs: 3 per document, "
            "where the question side is what gets embedded. Third, HyDE: "
            "the query is answered hypothetically by a small LLM and the "
            "hypothetical answer is embedded for retrieval. Recall@5 is "
            "measured after each increment on the same 100-query set, so "
            "the report shows the marginal gain and marginal dollar cost "
            "of each technique, then the semantic cache sits in front "
            "with a 0.92 threshold."
        ),
        "outline": [
            "Derivative artifacts carry source_doc_id so retrieval hits map back to real documents for citation.",
            "Generation prompts are cached to disk keyed by doc hash; re-runs are free.",
            "HyDE toggles per query, so the eval loop runs with and without it on identical retrieval state.",
            "Cache eval replays a 1,000-query stream with 30 percent duplicate intent and reports hit rate, false-hit rate, latency, and cost saved.",
        ],
    },
    10: {
        "approach": (
            "The agent is a LangGraph (or ADK) graph with a router node "
            "that classifies each question as unstructured (RAG path) or "
            "structured (SQL path). The SQL path exposes list_tables, "
            "get_schema, and run_query as MCP tools over the sample "
            "database, with run_query restricted to read-only and "
            "row-capped. The RAG path reuses the week 4 funnel. A "
            "finalizer node merges evidence and answers with citations. "
            "The mixed 100-question test set (half doc questions, half "
            "SQL questions, a few needing both) is scored against static "
            "RAG with the same generator model."
        ),
        "outline": [
            "FastMCP server wraps the SQLite sample DB; the agent consumes tools via the MCP client, not direct imports.",
            "Router few-shot prompt with 10 labeled examples; log routing accuracy separately.",
            "Cap agent steps at 6 and log every tool call with arguments for the trace deliverable.",
            "Score answer accuracy per question type; the writeup explains where the agent wins (joins, aggregates) and where it just adds latency.",
        ],
    },
    11: {
        "approach": (
            "Base model Qwen2.5-Coder-1.5B (or similar small model). The "
            "few-shot baseline uses 3 in-context examples per Spider "
            "question. LoRA SFT uses rank 16, alpha 32, attention plus "
            "MLP targets, 3 epochs on the Spider train split with the "
            "schema serialized into the prompt. The GRPO pass samples 8 "
            "completions per prompt, rewards 1.0 for execution-match "
            "with the gold result set, 0.2 for valid SQL that executes, "
            "0 otherwise, with a KL penalty against the SFT checkpoint. "
            "All three systems are scored on exact match and execution "
            "accuracy on the same dev split."
        ),
        "outline": [
            "Serialize schemas as CREATE TABLE statements in the prompt; truncate to the tables the question needs when over budget.",
            "SFT with PEFT + TRL SFTTrainer; save the adapter, not the merged model.",
            "Verifier executes candidate and gold SQL against the Spider SQLite files and compares result sets order-insensitively.",
            "GRPO for 200 steps, group size 8, then report baseline vs SFT vs SFT+GRPO in one table with example wins and losses.",
        ],
    },
    12: {
        "approach": (
            "The capstone runs the full eval harness against the RAG "
            "system accumulated over the bootcamp: Ragas (faithfulness, "
            "answer relevancy, context precision, context recall) on a "
            "150-question set, an LLM judge from a different model "
            "family with position randomization, and RGB-style "
            "robustness tests that inject noise passages and "
            "counterfactual evidence. The weakness analysis ranks metric "
            "gaps by user impact, picks one (typically context precision "
            "or noise robustness), implements a single targeted fix such "
            "as a reranker or grounding gate, and re-runs the identical "
            "suite so before and after are directly comparable."
        ),
        "outline": [
            "Pin seeds, model versions, and the eval set in a config committed before the first run.",
            "Ragas plus judge plus robustness results land in one results/ directory keyed by run id.",
            "Robustness tests: swap 30 percent of retrieved passages with topically similar noise, then with counterfactuals, and measure answer flip rate.",
            "The improvement PR is one focused change with an ablation flag so the re-eval isolates its effect.",
            "Final report: metric table before/after, the surprise reflection, and the next two improvements you would make.",
        ],
    },
}
