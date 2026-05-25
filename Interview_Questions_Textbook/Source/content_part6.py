"""Part 6: LLMOps & system design, Evaluation, Miscellaneous."""

LLMOPS = [
    ("Design a system that uses an LLM for near real-time response at massive scale.",
     [
        "Targets: P95 latency under 2 seconds; throughput 10K+ QPS; cost manageable; "
        "graceful degradation under load.",
        "Architecture: a thin API gateway in front; request routing by user tenant; LLM "
        "serving layer using vLLM or TGI behind a load balancer; semantic cache to short-"
        "circuit repeated queries; KV-cache management at the serving layer; "
        "horizontal scaling with autoscaling on queue depth.",
        "Optimization: continuous batching (vLLM's PagedAttention) raises throughput "
        "5-24x over naive batching. Speculative decoding for lower latency on certain "
        "models. KV-cache reuse for shared prefixes (system prompts, multi-turn "
        "conversations). Use the smallest model that meets quality. Quantize aggressively "
        "(int8 or int4).",
        "Load balancing: queue-aware routing prefers replicas with shorter queues. Sticky "
        "sessions when possible for cache locality.",
        "Observability: distributed tracing across gateway, cache, retrieval, generation. "
        "Track P50/P95/P99 latency, tokens per second, cache hit rate, error rate. Alert "
        "on regressions.",
     ]),

    ("How would you incorporate caching to improve LLM performance?",
     [
        "Exact-match cache: hash the input (prompt + parameters); cache the response. "
        "Cheap, simple. Hit rate depends on traffic patterns. Useful when the same "
        "queries repeat (FAQs, common tasks).",
        "Semantic cache: embed the query; look up similar past queries; return their "
        "cached response if similarity exceeds a threshold. Captures more hits at the "
        "risk of returning a not-quite-right answer. Tune the threshold against a "
        "labeled validation set.",
        "Prompt cache: cache the KV-cache for shared prefixes (system prompts, RAG "
        "context). Anthropic, OpenAI, and many serving stacks support this. Saves both "
        "latency and cost.",
        "Embedding cache: cache embeddings for repeated documents or queries. Cheap to "
        "implement; high hit rate on stable corpora.",
        "Tool-call cache: cache tool responses by argument (deterministic tools only). "
        "Cache-and-skip pattern reduces redundant tool calls in agentic loops.",
        "What to cache: stable, repeated, idempotent content. What NOT to cache: "
        "personalized responses, time-sensitive data, sensitive content with retention "
        "concerns.",
     ]),

    ("How do you reduce model size for deployment on resource-constrained devices?",
     [
        "Quantization: int8 (4x smaller, modest accuracy loss); int4 (8x smaller, "
        "larger but still acceptable loss with good methods like AWQ, GPTQ); int2 and "
        "binary for extreme cases.",
        "Pruning: remove weights or neurons that contribute little. Unstructured pruning "
        "is easier; structured pruning (entire heads or channels) gives real speedups.",
        "Knowledge distillation: train a smaller student from a larger teacher. Common "
        "size ratios: 10x smaller students keep 90-95% of teacher quality.",
        "Architecture search: pick smaller models designed for efficiency (MobileBERT, "
        "DistilBERT, Mistral-7B for LLMs, MobileViT for vision).",
        "Model partitioning: split the model between device and edge server. Run "
        "preprocessing and small layers on-device; larger layers on the server.",
        "Mixed precision inference: BF16 or FP8 instead of FP32. Free 2-4x speedup on "
        "modern hardware.",
        "Compilation: ONNX Runtime, TensorRT, CoreML, TFLite optimize for specific "
        "hardware. Use them.",
     ]),

    ("Discuss tradeoffs of GPUs vs TPUs vs specialized hardware for LLM deployment.",
     [
        "GPUs (NVIDIA H100, H200, B200, RTX series): mature ecosystem, broad framework "
        "support, easy to acquire (though expensive). The default for most LLM workloads. "
        "Strong performance per dollar for inference and training.",
        "TPUs (Google v4, v5, v6): excellent performance for transformer workloads, "
        "tight integration with JAX and TensorFlow, but Google Cloud only. Best for "
        "very large training runs where pod size matters.",
        "AMD GPUs (MI300X): catching up; competitive for inference on big models due "
        "to large HBM. Software ecosystem (ROCm) maturing but still less polished than "
        "CUDA.",
        "AWS Trainium and Inferentia: AWS-specific accelerators with cost advantages "
        "for inference on supported models. Smaller ecosystem.",
        "Cerebras, Groq, SambaNova, Etched: specialized inference accelerators. Very "
        "high throughput on specific architectures. Lock-in risk and smaller ecosystem.",
        "Apple Silicon: increasingly capable for local inference (M2 Ultra, M3 Max). "
        "MLX framework gaining traction.",
        "Selection drivers: workload (training vs inference), scale, framework support, "
        "cost, vendor lock-in, ecosystem maturity. For most enterprises, NVIDIA GPUs on "
        "a major cloud are the default.",
     ]),

    ("How would you build a ChatGPT-like system?",
     [
        "Frontend: web app with streaming responses, conversation history, file upload. "
        "Mobile apps. APIs for developers.",
        "Backend: stateless API layer. Session management with persistent conversation "
        "store. Rate limiting per user.",
        "Model serving: vLLM or TGI behind a load balancer. Continuous batching. "
        "KV-cache management. Speculative decoding for latency.",
        "Models: a frontier base LLM trained with SFT + RLHF. Optionally specialized "
        "variants (code, reasoning, multimodal).",
        "Tool use: function calling for web search, code execution, image generation, "
        "calendar, email. Tool registry; safe execution sandboxes.",
        "RAG: optional, for memory and document upload features.",
        "Safety: input filters (prompt injection, harmful intent), output filters "
        "(toxicity, PII), refusal calibration, jailbreak detection. Continuous red teaming.",
        "Operations: observability (traces, metrics, logs), feature flags, A/B testing, "
        "incident response. Compliance: SOC 2, GDPR.",
        "Scale: tens of millions of users requires global multi-region deployment, "
        "specialized hardware, careful capacity planning.",
     ]),

    ("Design an LLM-based code generation system. What challenges arise?",
     [
        "Base model: a code-specialized LLM (StarCoder, Code Llama, DeepSeek Coder, "
        "Claude). Trained on code corpora plus natural language.",
        "Context: code generation needs the right context, not just the current line. "
        "Include: file imports, related files (cross-file context), open editor tabs, "
        "documentation. Embed and retrieve relevant snippets from the user's repository.",
        "Inference: low latency is critical for inline completion. Use small models for "
        "auto-suggest; larger models for chat-style code generation. Speculative decoding "
        "is well-suited to code.",
        "Quality: verify generated code parses and (ideally) compiles before showing. "
        "Run unit tests when available. Lint for style issues.",
        "Safety: detect attempts to generate malicious code (malware, exploits). Detect "
        "license violations (verbatim copy of GPL code).",
        "Personalization: learn the user's style; respect project conventions. Per-user "
        "and per-project context.",
        "Challenges: hallucinated APIs (functions that don't exist), wrong types, "
        "outdated patterns, security vulnerabilities. Mitigations: type checking, API "
        "verification, security linters, secret detection.",
     ]),

    ("Describe an approach to generative AI for original music composition.",
     [
        "Pipeline: text prompt → music model → audio output. Models like MusicGen, MusicLM, "
        "and Stable Audio take text descriptions and produce audio.",
        "Architecture: transformer or diffusion model trained on (audio, description) "
        "pairs. Audio is typically tokenized via a neural audio codec (Encodec, SoundStream) "
        "into discrete tokens that an autoregressive transformer can predict.",
        "Conditioning: text describes genre, instruments, mood, tempo. Some models accept "
        "melody conditioning (hum a tune; the model orchestrates around it).",
        "Quality considerations: musical coherence over long durations (most models "
        "struggle past 30-60 seconds), structural elements (verse, chorus), and "
        "instrument fidelity.",
        "Practical patterns: hybrid systems combine an LLM (for high-level structure and "
        "lyrics) with a music model (for audio). Human-in-the-loop for refinement.",
        "Ethical: training data licensing, artist attribution, copyright of generated "
        "music. Detection of generated content. Pay-for-training models compensate "
        "rights holders.",
     ]),

    ("How would you build an LLM-based QA system for a specific domain or dataset?",
     [
        "Architecture: RAG is the default. Domain corpus → embeddings → vector DB. User "
        "query → retrieval → grounded LLM response with citations.",
        "Embedder: domain-tuned if vocabulary diverges from general. Start with BGE or "
        "E5 baselines; fine-tune on in-domain (query, relevant-doc) pairs.",
        "Chunking: pick based on document structure. Sections for structured documents, "
        "semantic chunks for prose, semantic + hierarchical (mother-child) for high-stakes.",
        "Retrieval: hybrid (BM25 + dense) almost always beats either alone. Reranker on "
        "top of dense retrieval for the final stage.",
        "LLM: a strong general LLM is usually enough with good retrieval. Domain fine-"
        "tuning helps with format and tone but is rarely necessary for accuracy.",
        "Evaluation: build a held-out QA set with expert-annotated answers. Measure "
        "retrieval (Recall@k) and generation (faithfulness, answer relevance via Ragas, "
        "exact-match on closed-form answers).",
        "Continuous improvement: log all queries; review failures; expand the corpus or "
        "the prompt; retune embedders. The eval set should grow with discovered failure "
        "modes.",
     ]),

    ("What design considerations matter for multi-turn conversational AI with an LLM?",
     [
        "State management: persistent conversation history; conversation summaries for "
        "long sessions; identity (which user is this, what do they have access to).",
        "Query understanding: rewrite follow-up queries to standalone form using the "
        "history. 'When was it founded?' → 'When was Acme Corp founded?'",
        "Memory: short-term (recent verbatim turns) plus long-term (summarized history "
        "or facts about the user). Long-term memory is itself a RAG index.",
        "Tool use: when the user asks for something requiring a tool (search, "
        "calculation, file upload), the model decides to call the tool; the result feeds "
        "the next response.",
        "Safety: per-turn input and output guardrails. Multi-turn jailbreak detection "
        "(some attacks unfold over multiple turns).",
        "Personalization: respect user preferences, prior context, communication style. "
        "Privacy considerations for what is stored.",
        "Recovery: handle errors gracefully (tool failure, LLM timeout). Streaming "
        "responses with intermediate state.",
        "Evaluation: multi-turn benchmarks (MT-Bench), user satisfaction metrics "
        "(thumbs, regenerate rate, session length, return rate).",
     ]),

    ("How can you control creative output of generative models for specific styles?",
     [
        "Prompting: detailed prompts specifying style, medium, mood, references. Few-"
        "shot examples of the desired style in the prompt.",
        "Conditioning: for image models, ControlNet (pose, depth, canny edge) conditions "
        "on structural inputs. For LLMs, system prompts define persona and style. IP-"
        "adapter passes a style image as condition.",
        "Fine-tuning: LoRA on a small dataset of the target style. Dreambooth for "
        "subject-specific image generation. SFT on (instruction, style-matched response) "
        "pairs for text.",
        "Sampling controls: temperature, top-k, top-p, repetition penalty. Lower values "
        "for tighter style adherence; higher values for more creative variation.",
        "Classifier-free guidance: amplifies the prompt's influence. Higher CFG scale = "
        "more on-prompt but potentially less natural.",
        "Negative prompts: specify what to avoid. 'Photo, photographic' as a negative "
        "for stylized illustration.",
        "Evaluation: human raters on style match. Reference-based metrics where "
        "applicable (CLIP-score against style reference, FID against style corpus).",
     ]),

    ("How do you monitor LLM systems once productionized?",
     [
        "Per-request: latency (P50, P95, P99), tokens generated, time-to-first-token, "
        "cost. Tool calls, retrieval hits.",
        "Aggregate: throughput, error rate, queue depth, cache hit rate, GPU utilization.",
        "Quality: sample 1-5% of traffic for offline scoring (faithfulness, relevance, "
        "safety). Build dashboards trending quality over time. Alert on regression.",
        "User signals: thumbs up/down ratio, regenerate rate, conversation length, "
        "abandonment, return user rate.",
        "Drift: input distribution drift (embed queries, monitor distribution); output "
        "distribution drift (length, refusal rate, sentiment).",
        "Safety: jailbreak attempts (input filter triggers), policy violations, PII "
        "exposure events. Audit logs for all retrievals and tool calls.",
        "Cost: dollar cost per user, per query, per session. Trend over time. Alert on "
        "spikes that may indicate abuse or runaway agents.",
        "Tools: OpenTelemetry for tracing. Grafana, Datadog, Honeycomb for dashboards. "
        "Helicone, LangFuse, Arize for LLM-specific observability.",
     ]),
]


EVALUATION = [
    ("What are common NLP evaluation metrics, and how do you choose?",
     [
        "Classification: accuracy, precision, recall, F1, ROC-AUC, PR-AUC. Choose based "
        "on class balance and cost of errors. F1 for imbalanced; ROC-AUC for ranking.",
        "Sequence labeling (NER, POS): token-level F1 plus span-level F1 (exact match of "
        "predicted spans against gold).",
        "Translation: BLEU (n-gram overlap), chrF (character F-score), COMET (learned "
        "metric, often better correlated with human judgment).",
        "Summarization: ROUGE-1/2/L (recall-oriented n-gram overlap). BERTScore for "
        "semantic similarity. Human evaluation for coherence and faithfulness.",
        "Generation: BLEU, ROUGE, METEOR, CIDEr (captioning), BERTScore. LLM-as-judge for "
        "open-ended generation.",
        "Retrieval: Recall@k, Precision@k, MRR, MAP, NDCG. Choose based on whether you "
        "need top-1 (MRR) or coverage (Recall@k).",
        "Selection guidance: pick the metric most aligned with your actual deployment "
        "objective. For chat, win-rate against a baseline (MT-Bench, Arena) is more "
        "meaningful than BLEU.",
     ]),

    ("How does evaluation differ between generative tasks and classification tasks?",
     [
        "Classification has a clear correct answer; metrics like accuracy and F1 are "
        "well-defined and reliable.",
        "Generative tasks (text, image) have many valid outputs. Reference-based metrics "
        "(BLEU, ROUGE) capture only one notion of correctness and correlate weakly with "
        "human judgment.",
        "Generative evaluation needs:",
        "- LLM-as-judge with explicit rubric and bias control (position, verbosity, self-"
        "preference).",
        "- Human evaluation for high-stakes or ambiguous outputs.",
        "- Task-specific metrics (CodeBLEU, pass@k for code; CLIPScore for image; FID "
        "for image distribution match).",
        "- Diversity metrics (self-BLEU, distinct-n) to catch mode collapse.",
        "- Multi-dimensional rubrics: factuality, fluency, relevance, helpfulness, "
        "safety. Compute each separately; combine with care.",
        "Classification can be automated cheaply; generative usually cannot. Plan for "
        "human-in-the-loop evaluation for generative systems.",
     ]),

    ("Why is human evaluation important in NLP, especially for generative AI?",
     [
        "Automated metrics miss what humans care about: factuality, helpfulness, tone, "
        "creativity, harm. A high BLEU score with low quality is common in summarization. "
        "A model that reliably hallucinates may have low perplexity.",
        "When human eval is essential: open-ended generation (chat, summarization, "
        "creative writing); high-stakes outputs (medical, legal, financial); subjective "
        "quality dimensions (style, tone, helpfulness); model comparison at the frontier "
        "where automated metrics saturate.",
        "Methodology: clear rubric; calibration round with examples; multiple annotators "
        "per item; inter-annotator agreement check (Cohen's kappa, Krippendorff's alpha); "
        "blind comparison (don't tell raters which model produced which output); "
        "stratified sampling to cover edge cases.",
        "Tradeoffs: expensive, slow, hard to scale, subjective. Mitigations: LLM-as-"
        "judge for screening with human review on borderline cases; preference data "
        "collection through paid annotation services or crowdsourcing platforms.",
     ]),

    ("How do you evaluate models for bias and fairness?",
     [
        "Benchmarks: BBQ (bias benchmark for QA), StereoSet, CrowS-Pairs, WEAT, BBNLI. "
        "These probe for stereotype and bias along axes like gender, race, religion, "
        "nationality.",
        "Demographic parity in outcomes: when the model classifies or generates, are "
        "outcomes equal across demographic groups? Disparate Impact ratio, equal "
        "opportunity, equalized odds are formal metrics.",
        "Counterfactual evaluation: change a demographic attribute in the input (he → "
        "she); does the output change in a biased way? Build counterfactual pairs and "
        "measure consistency.",
        "Generative bias: in open-ended generation, measure how often the model "
        "associates roles, traits, or attributes with specific groups. Compare against "
        "balanced ground truth.",
        "RAG bias: does retrieval pull representative documents across groups, or only "
        "majority sources?",
        "Process: audit before deployment; continuous evaluation in production; "
        "publish model cards documenting known biases; collect user feedback on bias "
        "incidents.",
     ]),

    ("What is perplexity, and why is it used to evaluate language models?",
     [
        "Perplexity = exp(average negative log-likelihood per token) on a held-out "
        "corpus. Equivalently, the geometric mean of 1/P(token|context). Lower is "
        "better.",
        "Intuition: perplexity measures how 'surprised' the model is by the corpus. "
        "Perplexity of 10 means the model is roughly as uncertain as if it were "
        "choosing uniformly from 10 options for each token.",
        "Why used: directly tied to the training objective (causal LM). Easy to compute. "
        "Comparable across models trained on the same tokenizer and similar evaluation "
        "corpus.",
        "Caveats: perplexity depends on the tokenizer (a model with a smaller vocab "
        "naturally has higher perplexity). Perplexity on Reddit text says nothing about "
        "math reasoning. Below a usable threshold, perplexity decouples from task "
        "performance: a model with PPL=5 and PPL=4 are both 'fluent' but differ "
        "negligibly in chat quality.",
        "Use perplexity as a sanity check during training and for comparing models "
        "within the same family. For downstream quality, use task benchmarks.",
     ]),

    ("How do you evaluate coherence and relevance of generated text?",
     [
        "Reference-based: BLEU, ROUGE, METEOR, BERTScore against a reference. Capture "
        "surface overlap and semantic similarity but not coherence directly.",
        "LLM-as-judge: prompt a separate strong LLM to rate coherence and relevance on "
        "a Likert scale or as pairwise preference. Cheap and scalable; control for "
        "biases (position, verbosity, self-preference).",
        "Human evaluation: panel ratings on a defined rubric. Especially for chat and "
        "summarization where coherence over multiple sentences matters.",
        "Structural metrics: entity coverage in summaries (does the summary include the "
        "key entities from the source?); claim alignment (does each claim in the output "
        "appear in the source?); topical consistency (do successive sentences stay on "
        "topic?).",
        "Engagement signals in production: average response length read by users, "
        "regenerate rate, follow-up rate. Indirect but informative.",
     ]),

    ("Discuss BLEU, METEOR, and human eval for coherence in conversational AI.",
     [
        "BLEU: counts n-gram overlap (1- to 4-grams) between candidate and reference, "
        "applies a brevity penalty. Originally designed for machine translation. "
        "Strengths: simple, fast, well-understood. Weaknesses: rewards surface overlap; "
        "misses paraphrase; one reference is rarely enough.",
        "METEOR: aligns words between candidate and reference using exact, stem, synonym, "
        "and paraphrase matches. Higher correlation with human judgment than BLEU. "
        "Slower; language-specific resources required.",
        "Human eval: the only reliable metric for open-ended conversational AI. Rate "
        "on rubrics covering coherence, helpfulness, factuality, safety. Use pairwise "
        "preference (A vs B) when comparing models, since absolute ratings are noisier.",
        "For chat specifically: MT-Bench (a curated set of multi-turn prompts judged by "
        "GPT-4) and Chatbot Arena (head-to-head human preference at scale) are the "
        "modern standards.",
        "Use BLEU/METEOR as cheap sanity checks; trust human eval for real comparisons.",
     ]),

    ("How do you assess diversity in generated text?",
     [
        "Self-BLEU: BLEU between pairs of samples from the same model. Higher self-BLEU = "
        "more repetitive across samples. Low self-BLEU is good.",
        "Distinct-n: number of distinct n-grams divided by total n-grams across samples. "
        "Distinct-1 measures unique unigrams; distinct-2 unique bigrams. Higher = more "
        "diverse.",
        "Embedding diversity: embed samples; compute average pairwise distance in "
        "embedding space.",
        "Topic coverage: cluster samples by topic; count distinct clusters. Useful for "
        "open-ended generation prompts.",
        "Mode collapse detection: a model that always produces similar outputs to "
        "different prompts is mode-collapsed. Detect by sampling many outputs and "
        "checking for redundancy.",
        "Calibration: sample at multiple temperatures and observe the diversity curve. "
        "Healthy models produce more diverse outputs at higher temperature; collapsed "
        "models produce similar outputs regardless.",
     ]),

    ("What role does prompt engineering play in evaluation?",
     [
        "Prompt engineering affects model behavior dramatically. A model that scores "
        "poorly under one prompt may score well under another. Fair evaluation must "
        "control for this.",
        "For research: report results for both a default prompt and an optimized prompt. "
        "Best-of-N prompt sampling sometimes used.",
        "For benchmarks: use the canonical prompt provided by the benchmark. Don't tune "
        "the prompt on the test set.",
        "For LLM-as-judge: the judge's rating depends heavily on the rating prompt. "
        "Standardize rubrics, randomize candidate order, control for verbosity bias.",
        "For production: prompt engineering is part of the system; evaluate the whole "
        "system, not the model in isolation. Track which prompts perform best.",
     ]),

    ("What are ROUGE scores, and why are they used for summarization?",
     [
        "ROUGE = Recall-Oriented Understudy for Gisting Evaluation. A family of metrics "
        "for summarization that count overlap between candidate summary and reference "
        "summary.",
        "ROUGE-N: counts n-gram overlap. ROUGE-1 (unigram), ROUGE-2 (bigram) are most "
        "common. Recall, precision, and F-measure variants exist.",
        "ROUGE-L: longest common subsequence between candidate and reference. Captures "
        "word order without requiring contiguous matches.",
        "ROUGE-W, ROUGE-S, ROUGE-SU: weighted LCS, skip-bigram, and union of skip-bigram "
        "and unigram. Less commonly used.",
        "Why used: established baseline, easy to compute, correlates moderately with "
        "human judgment for summarization. Most summarization papers report ROUGE.",
        "Limits: rewards surface overlap; misses semantic equivalence (paraphrase); one "
        "reference often not enough; can be gamed by extractive systems that copy "
        "sentences from the source.",
     ]),

    ("How do you assess informativeness and conciseness of a summarization model?",
     [
        "Informativeness: does the summary capture the key information? Measure entity "
        "coverage (% of source entities included), key fact coverage (% of pre-identified "
        "key facts present), ROUGE recall (rewards including reference content).",
        "Conciseness: length penalty (shorter is better if quality is matched); "
        "compression ratio (summary length / source length); redundancy (self-BLEU or "
        "redundant n-grams within the summary).",
        "Faithfulness: are all claims in the summary supported by the source? FactScore, "
        "QAGS (QA-based eval), NLI-based grounding checks.",
        "Human evaluation rubric: informativeness, conciseness, faithfulness, fluency. "
        "Rate each on a 5-point scale; compute mean per dimension.",
        "Tradeoff: longer summaries score higher on informativeness but lower on "
        "conciseness. Set a length budget appropriate to the use case.",
     ]),

    ("How do you evaluate retrieval quality in RAG?",
     [
        "Build an evaluation set with (query, relevant-document) pairs. Annotated by "
        "experts or curated from production logs with implicit feedback.",
        "Recall@k: fraction of relevant documents in the top-k retrieved. The most "
        "important RAG retrieval metric; if relevant docs are not retrieved, the LLM "
        "cannot answer.",
        "Precision@k: fraction of top-k that are relevant. Less important than recall "
        "for RAG because the LLM filters irrelevant context, but a low precision still "
        "wastes context tokens.",
        "MRR: mean reciprocal rank of the first relevant document. Sensitive to ranking "
        "quality of the top result.",
        "NDCG: graded relevance with rank discount. Useful when relevance is graded "
        "(highly relevant vs somewhat relevant).",
        "End-to-end signals: even with good retrieval metrics, downstream answer quality "
        "is what matters. Measure faithfulness and answer relevance via Ragas.",
        "Why it matters: retrieval quality usually dominates RAG outcomes. Invest in "
        "evaluation here before tuning the generator.",
     ]),

    ("What strategies reduce hallucination in RAG?",
     [
        "Better retrieval: stronger embedder, hybrid sparse+dense, reranker, more "
        "comprehensive corpus. The biggest lever.",
        "Grounding prompt: instruct the model to answer only from provided context and "
        "to refuse if the context does not support an answer.",
        "Citation requirement: model must cite which retrieved passage supports each "
        "claim. Verify citations.",
        "NLI verification: post-process by running each claim through an NLI model "
        "against the retrieved context. Block contradictions; flag neutral verdicts.",
        "Self-consistency: sample multiple responses; pick the consistent one.",
        "Fine-tuning: train the model on grounded responses with explicit refusals when "
        "context is insufficient.",
        "Confidence calibration: model output includes a confidence estimate; route low-"
        "confidence outputs to a human or to a refusal.",
        "Monitoring: sample production outputs; verify against sources; trend "
        "hallucination rate.",
     ]),

    ("How do you know if fine-tuning improved a model on a specific task?",
     [
        "Define the task and the metric before starting. Don't move the goalposts after "
        "training.",
        "Baseline: measure the base model's performance on a held-out test set. This is "
        "the bar to beat.",
        "Fine-tune: train. Track training and validation loss.",
        "Evaluate fine-tuned model on the same held-out test set with the same metric. "
        "Compare to baseline. Compute confidence intervals via bootstrap to avoid "
        "celebrating noise.",
        "Regression suite: measure base capabilities (general reasoning, math, code, "
        "instruction following) to detect catastrophic forgetting.",
        "Qualitative review: read a sample of outputs from both models on representative "
        "queries. Note systematic differences.",
        "A/B test in production: if both pass offline checks, route a fraction of "
        "traffic to the new model; compare user signals.",
        "Decision rule: accept the fine-tuned model only if it wins on the target task "
        "metric without significant regression on base capabilities.",
     ]),

    ("What challenges arise when fine-tuning large LLMs, and how do you mitigate?",
     [
        "Overfitting: the fine-tuning set is small relative to pretraining. Mitigations: "
        "PEFT (LoRA/qLoRA), weight decay, early stopping, fewer epochs (1-3), data "
        "augmentation.",
        "Catastrophic forgetting: aggressive fine-tuning degrades base capabilities. "
        "Mitigations: PEFT keeps base frozen; mix general data with task data; lower "
        "learning rate; layer-wise LR decay.",
        "Compute and memory: 70B+ models require multi-GPU training. Mitigations: "
        "qLoRA, gradient checkpointing, FSDP/ZeRO, mixed precision.",
        "Data quality: noisy or biased training data produces bad models. Mitigations: "
        "deduplicate, filter, quality-rank examples, manual review of samples.",
        "Hyperparameter sensitivity: small changes in LR or batch size can swing results. "
        "Mitigations: sweep small set; use known-good defaults; reproducible seeds.",
        "Evaluation cost: thorough evaluation across benchmarks is expensive. "
        "Mitigations: a focused eval suite tuned to the task plus a sample of broad "
        "benchmarks for regression detection.",
        "Deployment: fine-tuned models need to be served alongside or instead of base. "
        "Mitigations: LoRA adapters for multi-tenant serving; canary deployments.",
     ]),

    ("How do you assess the quality of generated samples from a generative model?",
     [
        "Image generation: FID (Frechet Inception Distance) compares the distribution of "
        "generated images to real ones. CLIPScore measures text-image alignment. Inception "
        "Score measures diversity and recognizability. Human evaluation for aesthetics.",
        "Text generation: BLEU/ROUGE for reference-based; BERTScore for semantic; LLM-as-"
        "judge for open-ended; human evaluation for high stakes. Perplexity as a sanity "
        "check.",
        "Code: pass@k (fraction of problems solved within k samples). Compile rate, lint "
        "score.",
        "Audio: human MOS (Mean Opinion Score) for speech quality; FAD (Frechet Audio "
        "Distance) for music.",
        "General principles: combine reference-based, distribution-level, and human "
        "metrics. Report variance, not just mean. Stratify by query type. Pre-register "
        "the evaluation protocol to avoid p-hacking.",
        "Diversity: distinct-n, self-BLEU, distinct topic count. Avoid mode collapse.",
        "Faithfulness for grounded generation: NLI-based, FactScore, citation accuracy.",
     ]),

    ("How would you set up an A/B test for two NLP models?",
     [
        "Hypothesis: state precisely what you expect (e.g. 'Model B reduces customer-"
        "support response time by 5%'). Pre-register the hypothesis.",
        "Sample size: power analysis to determine N. Effect size estimate × variance "
        "estimate → required users per arm. Avoid running too small a test.",
        "Randomization: assign users (not sessions) to arms randomly. Stable assignment "
        "so the same user sees the same model.",
        "Control and treatment: control = current model; treatment = new model. Match "
        "everything else (prompt, latency budget, etc.) between arms.",
        "Metrics: primary (the hypothesis metric, e.g. resolution time); secondary "
        "(satisfaction, regenerate rate, escalation rate); guardrail (safety violations, "
        "latency, cost). Don't move the primary mid-test.",
        "Duration: long enough for weekly cycles. Typically 2-4 weeks.",
        "Analysis: t-test or proportions test with Bonferroni correction for multiple "
        "metrics. Check for distribution shift between arms (sanity).",
        "Decision: pre-defined launch criteria. If treatment wins primary by X% with "
        "p<0.05 and no guardrail violations, launch.",
     ]),

    ("How do latency and efficiency factor into evaluating NLP models in production?",
     [
        "Latency budgets: define P50, P95, P99 targets. P95 is what users feel. "
        "Interactive chat typically targets P95 under 2 seconds; semantic search under "
        "200 ms.",
        "Throughput: requests per second sustained. Determine capacity required and cost.",
        "Time-to-first-token: critical for streaming UX. Users tolerate longer total "
        "latency if the first token appears quickly.",
        "Cost per query: dominated by input tokens for RAG. Optimize prompt size, "
        "use prompt caching, downsize models when quality allows.",
        "Quality-efficiency tradeoff: a slightly lower-quality smaller model that "
        "ships at lower latency and cost often beats a higher-quality slow model in "
        "production. Measure end-to-end user outcomes, not just quality benchmarks.",
        "Efficiency improvements: quantization, distillation, speculative decoding, "
        "KV-cache reuse, batched serving. Each affects quality differently.",
     ]),

    ("What is the role of explainability in NLP evaluation for high-stakes applications?",
     [
        "High-stakes domains (medical, legal, financial, hiring) need explanations of "
        "model outputs for trust, debugging, and compliance.",
        "Citation-based explanation: for RAG, surface the retrieved passages that "
        "supported each claim. Lets users verify and learn.",
        "Attention-based explanation: visualize attention weights to show which input "
        "tokens drove the output. Interpretable but not always faithful (attention "
        "patterns can be misleading).",
        "Chain-of-thought: have the model surface its reasoning. Catches mistakes earlier "
        "and is auditable.",
        "Counterfactual explanations: show how the prediction would change with "
        "different inputs. Useful for fairness audits.",
        "Influence functions: identify which training examples most influenced a "
        "specific prediction. Expensive but powerful for debugging.",
        "Documentation: model cards, datasheets for training data, system cards "
        "describing the full pipeline.",
        "Evaluation: explanation faithfulness (does the explanation match what drove "
        "the prediction?) and explanation utility (do users actually understand and "
        "trust the output better?).",
     ]),

    ("How do you measure user satisfaction with a deployed NLP model?",
     [
        "Direct: thumbs up/down on each response. Survey at session end (CSAT, NPS).",
        "Indirect: regenerate rate (users dissatisfied with first response), conversation "
        "length (longer ≠ better, depends on use case), abandonment rate, time to "
        "resolution.",
        "Behavioral: return user rate, frequency of use, breadth of features used.",
        "Aggregate: weekly/monthly active users, retention curves. Segment by user "
        "cohort and query type.",
        "Qualitative: structured user interviews. Open-ended feedback collection. "
        "Support ticket analysis for pain points.",
        "Triangulate: no single metric is sufficient. A high thumbs-up rate with high "
        "regenerate rate suggests users are satisfied with what they finally got but "
        "had to work for it.",
        "Distinguish satisfaction from sycophancy: a model that flatters users may get "
        "high ratings without being helpful. Cross-check with task completion metrics.",
     ]),

    ("What is domain adaptation, and how do you evaluate it?",
     [
        "Domain adaptation is the process of taking a model trained on a general "
        "distribution and adapting it to a specific domain (medical, legal, financial). "
        "Mechanisms: continued pretraining on domain text, instruction tuning on domain "
        "(prompt, response) pairs, PEFT for behavior changes, domain-specific RAG.",
        "Evaluation: build a held-out domain test set with expert-annotated ground truth. "
        "Measure task metrics on this set. Compare to: (a) the base model (does "
        "adaptation help?), (b) a base model with RAG (is the gain worth the fine-tuning "
        "cost?), (c) a model adapted with more or different data (is your data "
        "sufficient?).",
        "Regression suite: measure general capabilities (MMLU, HumanEval, GSM8K) to "
        "catch catastrophic forgetting.",
        "Domain-specific benchmarks: MedQA, FinanceBench, LegalBench. Use them for "
        "comparable numbers.",
        "Expert review: in regulated domains, human expert review of model outputs is "
        "the gold standard. Sample stratified across query types.",
     ]),

    ("How do you evaluate robustness to adversarial attacks?",
     [
        "Adversarial benchmarks: AdvBench (jailbreak prompts), Anthropic's red-teaming "
        "datasets, HarmBench. Measure refusal rate and harm rate on adversarial inputs.",
        "Prompt injection: test with retrieved content containing injection attempts. "
        "Measure how often the model follows injected instructions vs the system prompt.",
        "Jailbreaks: structured probes (role-play, hypothetical scenarios, language "
        "tricks, prompt encoding). Track jailbreak success rate over a fixed test suite.",
        "Input perturbation: typos, paraphrasing, capitalization. Measure consistency "
        "of outputs.",
        "Continuous red teaming: dedicated team probing the model for novel failure "
        "modes. Add new attacks to the test suite as they are discovered.",
        "Production monitoring: log and alert on attempted attacks. Trend successful "
        "vs blocked over time.",
        "Defense layers: input filters, output filters, RLHF safety training, "
        "constitutional principles. Evaluate the full system, not just the model.",
     ]),
]


MISC = [
    ("What ethical considerations are crucial when deploying generative models?",
     [
        "Truthfulness: generative models hallucinate. Deploy with grounding (RAG), "
        "citations, and refusal-when-unsure behavior. Disclose AI-generated content.",
        "Harm prevention: refuse to help with illegal, harmful, or dangerous requests "
        "(weapons, malware, self-harm). Continuous red teaming; safety RLHF.",
        "Bias and fairness: audit for representational harm across demographics. Apply "
        "balanced training data, fairness benchmarks (BBQ, BBNLI), continuous "
        "evaluation.",
        "Privacy: do not memorize and reproduce training data; protect PII; respect data "
        "subjects' rights (GDPR, CCPA).",
        "Copyright and attribution: training data licensing; provenance; respect for "
        "rights holders.",
        "Consent: humans should know when they are interacting with AI. Disclose model "
        "limitations.",
        "Job displacement: think about downstream effects on workers. Engage with "
        "affected communities.",
        "Misuse: deepfakes, disinformation, fraud. Build detection tools; cooperate with "
        "platforms.",
        "Environmental: training and inference have energy costs. Optimize for "
        "efficiency.",
        "Governance: model cards, system cards, ethics review boards, post-deployment "
        "audits.",
     ]),

    ("Describe a challenging project involving generative models.",
     [
        "An interview answer should be a real story, structured as: situation, task, "
        "action, result.",
        "Example template: 'I led the build of [SYSTEM] for [DOMAIN]. The hardest part "
        "was [SPECIFIC CHALLENGE: data quality, hallucination, latency, regulatory "
        "review]. I tried [APPROACH 1] which failed because [REASON]. I then [APPROACH 2] "
        "which worked because [REASON]. We measured [METRIC] and improved from X to Y. "
        "What I would do differently: [HONEST REFLECTION].'",
        "Strong answers show: ownership (you made decisions, not just executed), "
        "technical depth (specific tools, metrics, tradeoffs), pragmatism (you "
        "compromised when needed), self-awareness (you can critique your own choices).",
        "Weak answers: vague ('I worked on AI'), credit-claiming without specifics, no "
        "metrics, no failure mode acknowledged, blames others for problems.",
     ]),

    ("Explain the concept of latent space in generative models.",
     [
        "Latent space is a learned compressed representation of the data. Each point in "
        "latent space corresponds to a possible output; generation samples a point and "
        "decodes it.",
        "VAEs explicitly learn a latent space with a prior (typically standard normal) "
        "and a posterior conditioned on the input. The latent variable z follows q(z|x), "
        "and the decoder maps z to x.",
        "GANs implicitly define a latent space: noise vectors z fed into the generator "
        "produce data samples. No explicit prior structure, but interpolation between z "
        "vectors produces smooth interpolation in output.",
        "Diffusion models in their latent variant (Stable Diffusion) operate in the "
        "latent space of a separately-trained VAE. The diffusion process runs in this "
        "compressed space, then a decoder produces pixels.",
        "Use cases: interpolation between latents produces smooth transitions; arithmetic "
        "in latent space encodes attribute manipulation ('add smile to face'); semantic "
        "editing via inversion (encode image, edit latent, decode); anomaly detection "
        "(distance from typical latents).",
     ]),

    ("Have you implemented conditional generative models? What conditioning techniques?",
     [
        "Conditional generative models accept a condition c and produce samples from "
        "p(x | c). The condition can be a class label, text description, image, layout, "
        "or other structured input.",
        "Conditioning techniques:",
        "- Concatenation: append the condition embedding to the input or hidden states. "
        "Simple, works for class-conditional GANs.",
        "- Cross-attention: the generator cross-attends to encoded conditions. Used in "
        "text-to-image diffusion (Stable Diffusion attends to text encoder output).",
        "- Adaptive normalization (AdaIN, AdaLN): the condition modulates the "
        "normalization parameters of generator layers. Used in StyleGAN.",
        "- ControlNet: an auxiliary network that takes structural conditions (pose, "
        "edge map, depth) and modulates the main diffusion model.",
        "- Classifier-free guidance: train with and without the condition; at inference, "
        "extrapolate in the direction of the conditional prediction. Boosts conditioning "
        "fidelity.",
        "- LoRA-style: train small adapters per condition style. Used in custom-style "
        "image generators.",
     ]),

    ("Discuss the tradeoffs between GANs and VAEs.",
     [
        "GANs: adversarial training of generator vs discriminator. Strengths: high-"
        "quality, sharp samples. Weaknesses: training instability (mode collapse, "
        "non-convergence), no explicit likelihood, hard to evaluate.",
        "VAEs: probabilistic encoder-decoder with variational inference. Strengths: "
        "stable training, principled latent space, explicit likelihood (lower bound). "
        "Weaknesses: blurry samples (compared to GANs and diffusion) because of pixel-"
        "wise MSE in the reconstruction loss.",
        "Diffusion models have largely won for image generation: training stability of "
        "VAEs, sample quality matching or exceeding GANs, controllable via "
        "conditioning. VAEs remain useful as the encoder/decoder in latent diffusion. "
        "GANs persist for narrow high-throughput use cases (StyleGAN for fast face "
        "generation).",
        "Choose: diffusion for state-of-the-art quality and controllability; VAE for "
        "explicit latent structure and density estimation; GAN for legacy and high-"
        "throughput inference where quality is acceptable.",
     ]),

    ("What are the primary differences between Hugging Face Transformers, Datasets, and Tokenizers?",
     [
        "transformers: model code and pretrained checkpoints for thousands of models. "
        "AutoModel, AutoTokenizer, pipelines, training APIs (Trainer, TRL). The flagship "
        "library.",
        "datasets: dataset loading, processing, streaming. Memory-mapped Arrow format. "
        "Built-in handling for many public datasets. Lazy operations for huge datasets.",
        "tokenizers: fast Rust implementations of BPE, WordPiece, Unigram. Used by "
        "transformers internally; also usable standalone for training custom "
        "tokenizers.",
        "Integration: datasets prepares data, tokenizers turns text into IDs, "
        "transformers runs the model. Workflow: load model and tokenizer; load dataset; "
        "tokenize with dataset.map; train with Trainer. This three-library stack covers "
        "most NLP workflows.",
        "Supporting libraries: peft (PEFT), accelerate (multi-GPU and mixed precision), "
        "evaluate (metrics), trl (RLHF and DPO), diffusers (diffusion models).",
     ]),

    ("Describe Hugging Face Pipelines for end-to-end inference.",
     [
        "A pipeline wraps preprocessing, model inference, and postprocessing into one "
        "callable. Pick a task; load a default model; call the pipeline on input data.",
        "Supported tasks: text-classification, token-classification (NER), question-"
        "answering, summarization, translation, text-generation, fill-mask, "
        "feature-extraction, image-classification, object-detection, image-segmentation, "
        "speech-recognition, text-to-speech, image-to-text, visual-question-answering, "
        "zero-shot-classification, zero-shot-object-detection, and more.",
        "Advantages: quick prototyping (one line to a working model); consistent API "
        "across tasks; sensible defaults; handles batching; works with any model on the "
        "Hub that supports the task.",
        "When to use: prototyping, experimentation, demos, simple production deployments. "
        "For production at scale, prefer direct AutoModel + AutoTokenizer for finer "
        "control over batching, device placement, and preprocessing.",
     ]),

    ("How does Hugging Face Accelerate improve training, and what challenges does it solve?",
     [
        "accelerate provides a thin wrapper that runs the same training code across "
        "CPU, single GPU, multi-GPU, multi-node, and TPU without rewriting the code. "
        "The same script scales from a laptop to a cluster.",
        "Challenges it addresses: device placement boilerplate, distributed data "
        "parallel setup, mixed precision configuration, gradient accumulation, "
        "checkpoint handling across processes. accelerate handles these uniformly.",
        "How to use: wrap the model, optimizer, and dataloader in accelerator.prepare(); "
        "replace loss.backward() with accelerator.backward(); set a config via "
        "accelerate launch.",
        "Beyond DDP: integration with DeepSpeed and FSDP for very large models. "
        "Megatron-LM integration. Quantization (bitsandbytes) support.",
        "Net: lower the friction of moving a small experiment to a large training run. "
        "Reduces bugs from manually rewriting code for different hardware setups.",
     ]),

    ("How does Hugging Face's transformers library facilitate transfer learning?",
     [
        "Pretrained models: thousands of checkpoints on the Hub. AutoModel.from_pretrained "
        "downloads and loads any model by name. Includes weights, tokenizer, "
        "configuration.",
        "Task heads: pretrained models can be loaded with task-specific heads "
        "(AutoModelForSequenceClassification, AutoModelForTokenClassification, "
        "AutoModelForQuestionAnswering, AutoModelForCausalLM). The head is "
        "randomly initialized; the backbone is pretrained.",
        "Trainer: a high-level training API that handles fine-tuning loops, evaluation, "
        "logging, checkpointing, mixed precision, distributed training. Integrated with "
        "datasets and evaluate.",
        "PEFT integration: peft library plugs in. Wrap a model with get_peft_model and "
        "a LoraConfig; train normally with Trainer. Save and load adapters separately "
        "from base.",
        "Typical fine-tuning steps: pick base model and task head; load and preprocess "
        "data; configure TrainingArguments; instantiate Trainer with model, data, "
        "tokenizer, metrics; call trainer.train(); save the result; push to the Hub "
        "for sharing.",
     ]),

    ("What role does multi-modality play in the latest LLMs, and how does it enhance functionality?",
     [
        "Modern frontier LLMs (GPT-4o, Claude 3.5, Gemini 1.5/2.0) natively handle text, "
        "image, audio, and increasingly video. The single model accepts mixed inputs "
        "and may produce mixed outputs.",
        "Enhanced functionality: visual question answering, document understanding, "
        "chart and table interpretation, code from screenshots, image generation from "
        "text, speech recognition and synthesis, video understanding, generative "
        "manipulation.",
        "User experience: natural interaction. Show a photo of a broken appliance; the "
        "model identifies it and provides repair instructions. Paste a screenshot of "
        "code; the model debugs. Speak; the model responds in your voice.",
        "Architectural patterns: shared embedding space (CLIP-style) for retrieval; "
        "cross-attention bridges (Q-Former, Perceiver Resampler); direct token "
        "projection (LLaVA, GPT-4V). Modern models combine techniques.",
        "Impact: multimodal is now the default for foundation models. Single-modality "
        "models persist for narrow latency- or cost-sensitive uses.",
     ]),

    ("Implications of rapid LLM advancement for healthcare, education, and content creation?",
     [
        "Healthcare: clinical documentation automation (ambient AI scribes), diagnostic "
        "decision support, literature search, drug discovery (protein design with "
        "AlphaFold-style models), patient communication. Concerns: regulatory clearance, "
        "liability, bias against underrepresented populations, privacy.",
        "Education: personalized tutoring at scale, lesson plan generation, language "
        "learning, grading assistance. Concerns: cheating, equity of access, role of "
        "teachers, accuracy of explanations.",
        "Content creation: writing assistance, image and video generation, music "
        "composition, code generation. Concerns: copyright and attribution, deepfakes "
        "and misinformation, job displacement, homogenization of aesthetics.",
        "Cross-cutting: trust calibration, transparency about AI involvement, governance "
        "frameworks. Each domain has unique stakes; thoughtful deployment matters more "
        "than raw capability.",
        "Timeline: capabilities are advancing faster than regulatory and societal "
        "frameworks. Practitioners should engage actively in shaping deployment patterns.",
     ]),

    # ADDITIONAL BONUS QUESTIONS
    ("What is in-context learning, and why does it work?",
     [
        "In-context learning is the LLM's ability to learn a task from examples provided "
        "in the prompt, with no weight updates. The model sees a pattern (input → output, "
        "input → output, new input) and produces the corresponding output.",
        "Why it works: during pretraining, the model is exposed to billions of sequences "
        "that include similar patterns (lists, structured QA, code with similar functions). "
        "Predicting the next token in such sequences requires generalizing the pattern. "
        "This generalization is the meta-learning that enables in-context learning at "
        "inference.",
        "Empirical findings: in-context learning quality scales with model size; larger "
        "models exhibit emergent in-context abilities. Sensitive to example ordering, "
        "format, and selection. More examples help up to a point.",
        "Implications: a strong base model can solve many tasks without fine-tuning, "
        "just by clever prompting. This is why prompt engineering and RAG are such "
        "effective levers without touching model weights.",
     ]),

    ("What is constitutional AI?",
     [
        "Constitutional AI is an alignment approach where the model is trained to follow "
        "a written set of principles ('constitution') rather than relying solely on human "
        "preference data.",
        "Process: write the constitution (rules like 'be helpful, be harmless, avoid "
        "deception'). Use it in two ways: (1) supervised stage: model critiques and "
        "revises its own outputs based on constitutional principles. (2) RL stage: AI-"
        "generated preferences using the constitution as a rubric. Train with RLHF on "
        "these AI preferences (RLAIF).",
        "Why it matters: scales beyond what human preference data can cover; makes "
        "behavior more transparent (you can read the rules); easier to update behavior "
        "by editing the constitution.",
        "Limitations: the constitution itself encodes biases; AI judging AI can amplify "
        "errors; rigid rule-following can produce unhelpful refusals. Most production "
        "systems combine constitutional principles with human preference data.",
     ]),

    ("What is chain-of-thought prompting and why is it effective?",
     [
        "Chain-of-thought (CoT) prompting asks the model to produce reasoning steps "
        "before the final answer. Instead of 'Q: ... A: 42', it produces 'Q: ... Let me "
        "think step by step. First... then... so the answer is 42.'",
        "Why it helps: complex reasoning requires intermediate steps. Asking for the "
        "final answer directly forces the model to do all reasoning in one forward pass "
        "without externalizing intermediate state. CoT lets the model spread reasoning "
        "across multiple tokens.",
        "Variants: zero-shot CoT ('let's think step by step'); few-shot CoT (provide "
        "examples with reasoning); self-consistency (sample multiple CoT chains and vote); "
        "Tree of Thoughts (explore branches and backtrack).",
        "Modern frontier models like o1 and Claude 3.5 with thinking are trained to do "
        "extensive chain-of-thought reasoning automatically. They significantly outperform "
        "non-reasoning models on math, code, and complex reasoning tasks.",
     ]),

    ("What is a reasoning model like o1 or Claude with thinking?",
     [
        "A reasoning model is an LLM that, during inference, generates an extensive "
        "internal chain-of-thought before producing the final response. The thinking can "
        "be hundreds or thousands of tokens long.",
        "How they differ from standard LLMs: trained with RL on reasoning tasks "
        "(typically with RLVR using verifiable rewards). The model learns to spend "
        "inference compute on thinking rather than just emitting the final answer.",
        "Performance: dramatically better on math (AIME), code (Codeforces), and logic-"
        "heavy benchmarks. Trade higher inference cost for higher quality.",
        "User experience: longer latency to first answer but higher accuracy. Some "
        "products hide the thinking; others show it. Thinking is sometimes truncated "
        "or summarized.",
        "Implications: inference-time compute scaling becomes a lever. A standard model "
        "with 10x thinking compute can match a much larger model without thinking. This "
        "shifts cost from training to inference.",
     ]),

    ("What is the difference between continued pretraining and fine-tuning?",
     [
        "Continued pretraining (also called continued training or domain pretraining): "
        "extend pretraining with more data, usually from a specific domain. Same self-"
        "supervised objective (causal LM or masked LM). Output: a domain-specialized "
        "base model that has not been instruction-tuned.",
        "Fine-tuning: usually refers to instruction tuning or task-specific tuning. "
        "Supervised loss on (input, target) pairs.",
        "When to use continued pretraining: domain vocabulary and patterns differ "
        "significantly from general (medical, legal, code). Want to inject domain "
        "knowledge before instruction tuning.",
        "When to use fine-tuning: change model behavior, format, persona. Teach specific "
        "tasks. Most enterprise adaptations.",
        "Combination: continued pretraining → instruction fine-tuning → RLHF is the "
        "full pipeline. Most teams skip continued pretraining if their domain is "
        "well-represented in the base model.",
     ]),

    ("What is the difference between prompt engineering and prompt optimization?",
     [
        "Prompt engineering: human writes and iterates on prompts. Uses patterns (CO-"
        "STAR, few-shot, chain-of-thought) and intuition. Fast for simple tasks; "
        "labor-intensive for complex ones.",
        "Prompt optimization: programmatic search over prompt space. Frameworks like "
        "DSPy (COPRO, MIPRO), GEPA (evolutionary), TextGrad (text-as-tensor). The "
        "framework treats the prompt as a program to be compiled against an evaluator.",
        "When prompt engineering suffices: simple tasks, one-off scripts, exploration. "
        "When optimization wins: complex pipelines with multiple LLM calls, where small "
        "improvements compound; tasks with a clear automated evaluator; settings where "
        "you can afford the optimization runtime cost.",
        "Modern practice: start with prompt engineering for a working baseline; switch "
        "to programmatic optimization when the human effort plateaus and an evaluator "
        "is available.",
     ]),

    ("Why does a Mixture of Experts (MoE) model offer compute-efficient scaling?",
     [
        "MoE replaces dense feed-forward layers with many expert subnetworks plus a "
        "router. Per token, only a few experts (typically 1-2 out of 8-128) are "
        "activated.",
        "Total parameters can be very large (Mixtral 8x7B has 47B total) but active "
        "parameters per token are much smaller (about 13B for Mixtral). FLOPs per token "
        "scale with active parameters; memory scales with total.",
        "Result: a MoE with N total experts and k active is roughly the inference cost "
        "of a dense model with k experts' worth of parameters but the quality of a "
        "model with N experts' worth. Net: similar quality to a large dense model at a "
        "fraction of the inference compute.",
        "Caveats: total memory remains high (all experts must be in memory). Training "
        "is more complex (load balancing across experts, routing stability). Latency "
        "may not improve as much as throughput due to MoE-specific overheads.",
        "Examples: Mixtral 8x7B (Mistral), Switch Transformer (Google), GLaM (Google), "
        "DeepSeek-V3.",
     ]),

    ("Explain Retrieval-Augmented Fine-Tuning (RAFT).",
     [
        "RAFT is a fine-tuning paradigm specifically for RAG. Train the model to use "
        "retrieved context correctly: cite relevant passages, ignore distractor "
        "passages, refuse when context is insufficient.",
        "Training data: (question, context, answer) triples where the context includes "
        "both relevant and distractor passages. The target answer references the "
        "relevant passages explicitly.",
        "Why it helps: standard SFT data does not teach the model to navigate retrieved "
        "context well. Vanilla fine-tuning can make the model worse at RAG by teaching "
        "it to rely on parametric memory. RAFT-style data teaches the model to rely on "
        "context appropriately.",
        "Impact: improved faithfulness, better refusal calibration when retrieval misses, "
        "stronger citation behavior.",
     ]),

    ("What is the difference between encoder-only, decoder-only, and encoder-decoder models?",
     [
        "Encoder-only (BERT, RoBERTa, DeBERTa): bidirectional self-attention. Sees full "
        "input at once. Produces rich contextual representations. Best for "
        "classification, NER, embeddings, similarity. Not naturally generative.",
        "Decoder-only (GPT, LLaMA, Mistral, Claude): causal self-attention (left to "
        "right). Generates token by token. Best for generation. Modern instruction-"
        "tuned versions handle understanding tasks via prompting.",
        "Encoder-decoder (T5, BART, mT5): encoder reads input bidirectionally; decoder "
        "generates output left-to-right while cross-attending to encoder. Strong on "
        "translation, summarization, text-to-text tasks. Trickier to train than "
        "decoder-only at scale.",
        "Modern trend: decoder-only models dominate due to scaling efficiency and prompt-"
        "based versatility. Encoder-only models persist for embeddings and "
        "classification at scale where their efficiency wins.",
     ],
     ["20_encoder_decoder.png"]),

    ("What is sparse vs dense retrieval, and when is each preferred?",
     [
        "Sparse retrieval: based on lexical matching (BM25, TF-IDF, SPLADE). Each "
        "document is represented as a sparse vector of term weights. Inverted indexes "
        "make queries fast even at scale.",
        "Dense retrieval: based on neural embeddings (Sentence-BERT, BGE, E5, OpenAI "
        "ada). Documents and queries are dense vectors; similarity is cosine.",
        "Sparse strengths: exact keyword matching, rare terms (drug names, identifiers), "
        "no training required, fast, mature infrastructure.",
        "Dense strengths: semantic similarity, paraphrase handling, cross-lingual "
        "support (with multilingual embedders).",
        "Hybrid: combine both via reciprocal rank fusion or weighted scoring. Almost "
        "always beats either alone on diverse query distributions. The production "
        "default in 2025.",
        "When to prefer one: pure technical search (sparse); conversational search over "
        "concepts (dense); production search at any scale (hybrid).",
     ]),
]
