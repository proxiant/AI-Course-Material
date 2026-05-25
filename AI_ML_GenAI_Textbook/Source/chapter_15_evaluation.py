"""Chapter 15: Evaluation Methodologies."""

CHAPTER = {
    "label": "Chapter 15",
    "title": "Evaluation Methodologies",
    "sections": [
        {
            "number": "15.1",
            "title": "Why Evaluation Is the Hard Part",
            "paragraphs": [
                "It is easy to build something that looks impressive. It is hard to know "
                "whether what you built is actually good. The gap between 'works on a "
                "demo' and 'works in production' is mostly evaluation. Teams that invest "
                "in evaluation ship reliably. Teams that don't ship surprises.",

                "LLM evaluation is harder than classical ML evaluation. Classical ML has "
                "clear right answers (accuracy, F1, RMSE). LLM outputs are open-ended; "
                "there is no single correct response to 'summarize this document'. "
                "Reference-based metrics (BLEU, ROUGE) capture only surface overlap. "
                "Human evaluation is the gold standard but expensive. LLM-as-judge is "
                "cheap and scalable but has well-documented biases.",

                "This chapter walks the evaluation toolkit: classical metrics, modern "
                "LLM-specific approaches, RAG-specific evaluation, methodology for "
                "building evaluation suites that actually inform decisions.",
            ],
        },
        {
            "number": "15.2",
            "title": "Classification Metrics",
            "image": "27_confusion_matrix.png",
            "caption": "Figure 15.1: Confusion matrix for binary classification.",
            "paragraphs": [
                "For classification tasks, evaluation is well-understood.",

                "Accuracy. Fraction of predictions that are correct. Simple but misleading "
                "on imbalanced datasets. A 99% accurate model on a 99%-negative dataset "
                "may be predicting 'negative' always.",

                "Precision. True positives divided by predicted positives. Of the items "
                "the model said were positive, how many were? Important when false "
                "positives are costly (spam filter blocking real email).",

                "Recall. True positives divided by actual positives. Of the items that are "
                "positive, how many did the model catch? Important when false negatives "
                "are costly (cancer screening).",

                "F1 score. Harmonic mean of precision and recall. Balanced single metric. "
                "F-beta generalizes: F2 weights recall more, F0.5 weights precision more.",

                "ROC curve and AUC. Plot true positive rate against false positive rate at "
                "all thresholds. Area under the curve measures ranking quality across all "
                "thresholds. Use when you have a probability output and care about "
                "ranking, not a single threshold.",

                "Precision-Recall curve. For imbalanced datasets, the PR curve and its "
                "area are more informative than ROC. A model can have high ROC-AUC but "
                "poor precision at any useful threshold.",
            ],
        },
        {
            "number": "15.3",
            "title": "Generation Metrics",
            "paragraphs": [
                "For text generation, reference-based metrics measure overlap with one or "
                "more reference outputs.",

                "BLEU (Bilingual Evaluation Understudy). N-gram overlap, with a brevity "
                "penalty for short outputs. Designed for machine translation. Strengths: "
                "simple, fast, well-understood. Weaknesses: rewards surface overlap; "
                "misses paraphrase; correlates only weakly with human judgment on creative "
                "tasks.",

                "ROUGE (Recall-Oriented Understudy for Gisting Evaluation). N-gram "
                "overlap, recall-oriented. ROUGE-1 (unigrams), ROUGE-2 (bigrams), ROUGE-L "
                "(longest common subsequence). The summarization standard.",

                "METEOR. Aligns words by exact match, stem, synonym, and paraphrase. "
                "Higher human-judgment correlation than BLEU. Slower; language-specific "
                "resources required.",

                "chrF. Character-level F-score. Better than BLEU for morphologically rich "
                "languages.",

                "BERTScore. Use a pretrained encoder to embed candidate and reference. "
                "Compute token-level cosine similarity, then average. Captures semantic "
                "similarity that surface metrics miss. Higher correlation with human "
                "judgment than BLEU/ROUGE.",

                "COMET, BLEURT. Learned metrics trained on human judgment data. State of "
                "the art for translation evaluation. Slow but accurate.",

                "When to use reference-based metrics. Translation, summarization with "
                "known reference outputs. Quick iteration during development. Use as one "
                "of several signals, not the only one.",
            ],
        },
        {
            "number": "15.4",
            "title": "Perplexity",
            "paragraphs": [
                "Perplexity = exp(per-token cross-entropy) on a held-out corpus. Lower is "
                "better. The fundamental intrinsic evaluation for language models.",

                "What perplexity measures. How well the model predicts the next token. "
                "A perplexity of 10 means the model is, on average, as uncertain as if "
                "choosing uniformly from 10 options at each step.",

                "What perplexity misses. Factuality (a fluent lie has low perplexity). "
                "Reasoning (predicting the next token of a chain-of-thought is different "
                "from being able to reason). Instruction following. Calibration. Safety. "
                "All the things that matter for actual LLM quality.",

                "When to use. Sanity check during pretraining. Compare models trained with "
                "the same tokenizer on the same evaluation data. Detect regression in "
                "language modeling capability after fine-tuning.",

                "When not to rely on it. Comparing differently-tokenized models (a smaller "
                "vocab artificially increases perplexity). Judging downstream quality "
                "below a threshold (a model with PPL=5 and PPL=4 are both fluent; the "
                "difference does not predict chat quality).",
            ],
        },
        {
            "number": "15.5",
            "title": "LLM Benchmarks",
            "paragraphs": [
                "A standardized way to compare LLMs. Many benchmarks; pick those that "
                "match your use case.",

                "MMLU (Massive Multitask Language Understanding). 57 subjects, "
                "multiple-choice. Tests broad knowledge. Most LLM papers report MMLU. "
                "Strong models hit 80-90% accuracy in 2025.",

                "HellaSwag. Commonsense reasoning via sentence completion. Tests whether "
                "the model picks the natural continuation.",

                "GSM8K. Grade school math word problems. Tests arithmetic reasoning. "
                "Strong models hit 90%+ with chain-of-thought.",

                "MATH. Competition mathematics. Much harder than GSM8K. The proving "
                "ground for reasoning models (o1, R1).",

                "HumanEval, MBPP. Code generation. Pass@k: fraction of problems solved "
                "within k samples. Standard for code LLMs.",

                "BIG-Bench, BBH (BIG-Bench Hard). Diverse hard tasks. Cover capabilities "
                "MMLU misses.",

                "TruthfulQA. Tests for known false beliefs (urban legends, misconceptions). "
                "Distinguishes models that parrot common falsehoods from those that know "
                "the truth.",

                "MT-Bench. Multi-turn dialogue evaluated by GPT-4. Closer to actual chat "
                "use cases than knowledge benchmarks.",

                "Chatbot Arena. Crowd-sourced pairwise comparison. The most ecologically "
                "valid benchmark for chat quality.",

                "Domain-specific. MedQA (medical), FinanceBench (financial), LegalBench "
                "(legal). Use these when relevant to your use case; general benchmarks may "
                "not predict domain performance.",

                "Caveats. Benchmarks get gamed. Top labs train on the test set inadvertently "
                "(data contamination). Look at multiple benchmarks and recent results "
                "rather than trusting any single number.",
            ],
        },
        {
            "number": "15.6",
            "title": "LLM-as-a-Judge",
            "paragraphs": [
                "Have a separate strong LLM (typically GPT-4 or Claude) score outputs "
                "against a rubric or pairwise compare candidates. Cheap and scalable; "
                "replaces (or supplements) human evaluation.",

                "Setup. Define a rubric: helpfulness, factuality, relevance, format "
                "compliance, etc. Prompt the judge with the question, the candidate "
                "answer(s), and the rubric. Get scores or pairwise verdicts. Aggregate "
                "across many examples.",

                "Biases to control. Position bias: when two candidates are presented, the "
                "judge often prefers the first. Randomize positions; or always score "
                "both orderings and average. Verbosity bias: longer responses are often "
                "preferred even when shorter ones are better. Normalize by length or "
                "instruct the judge to ignore length. Self-preference bias: a judge tends "
                "to prefer outputs from its own model family. Use a different judge model "
                "than the model under evaluation.",

                "Reliability. LLM-as-judge correlates well with human judgment on simple "
                "rubrics. Correlation drops on subjective tasks (creativity, humor) and "
                "specialized domains (medical, legal). Sanity-check with human evaluation "
                "on a sample.",

                "Cost. A judge call per evaluation. Cheaper than human evaluation, more "
                "expensive than automated metrics. Use on samples (1% of production "
                "traffic, 100 examples in a CI pipeline) rather than every example.",
            ],
        },
        {
            "number": "15.7",
            "title": "RAG Evaluation: Ragas",
            "paragraphs": [
                "RAG-specific metrics from the Ragas framework (Es et al., 2023). Four "
                "core metrics, each addressing a different failure mode.",

                "Faithfulness. Are all claims in the answer supported by the retrieved "
                "context? Catches hallucination. Decompose the answer into claims; for "
                "each, check whether the context supports it (using an LLM judge or NLI).",

                "Answer relevance. Does the answer actually address the question? Catches "
                "off-topic responses. Generate candidate questions from the answer; "
                "compare them to the original question.",

                "Context precision. Are the retrieved passages relevant? Catches "
                "retrieval that returns junk. For each retrieved passage, score relevance "
                "to the question.",

                "Context recall. Does the retrieved context cover what is needed to "
                "answer? Catches retrieval that misses important information. Compare "
                "the retrieved context against a ground-truth answer.",

                "All four together. Faithfulness + answer relevance measure generation "
                "quality. Context precision + context recall measure retrieval quality. "
                "The four-axis picture is more informative than any single metric.",

                "Limitations. The metrics are themselves computed by LLMs. Same biases "
                "apply. Use as automated screening; sample human review for high-stakes "
                "decisions.",
            ],
        },
        {
            "number": "15.8",
            "title": "Hallucination Evaluation",
            "paragraphs": [
                "Hallucination has its own evaluation toolkit beyond Ragas.",

                "TruthfulQA. Tests known false beliefs. Distinguishes models that parrot "
                "falsehoods from those that know better.",

                "FactScore. Decompose generated text into atomic facts. Verify each fact "
                "against a knowledge source. Report the fraction supported. Strong "
                "correlation with human judgment.",

                "FEVER. Benchmark for claim verification. Three-way classification: "
                "supported, refuted, not enough info. Adapted for LLM output verification.",

                "QAGS. Generate questions from the candidate text; answer them using the "
                "source. Mismatch indicates hallucination.",

                "SelfCheckGPT. Sample multiple responses; compare for consistency. "
                "Inconsistent answers signal hallucination. No external knowledge base "
                "required.",

                "Citation accuracy. For RAG with citations, verify that cited sources "
                "actually contain the claim. Common metric in production systems.",

                "Confidence calibration. The model's predicted probability or verbalized "
                "confidence should correlate with correctness. Calibrate via temperature "
                "scaling or training-time techniques.",
            ],
        },
        {
            "number": "15.9",
            "title": "Bias and Safety Evaluation",
            "paragraphs": [
                "Models trained on web text reflect web biases. Production systems must "
                "evaluate for harm.",

                "BBQ (Bias Benchmark for QA). Probes stereotypes across nine demographic "
                "categories. Measures whether models reinforce stereotypes when context is "
                "ambiguous.",

                "StereoSet, CrowS-Pairs. Measure stereotype bias in language models via "
                "contrasting sentences.",

                "ToxiGen. Tests model responses to potentially harmful inputs.",

                "AdvBench. Jailbreak prompts. Measures refusal rate on adversarial inputs.",

                "WMDP (Weapons of Mass Destruction Proxy). Tests dangerous capability "
                "(chem/bio/cyber) knowledge that frontier models should not provide.",

                "HarmBench. Comprehensive safety evaluation across harm categories.",

                "Process. Run safety evaluation before deployment. Track over time. Add "
                "discovered failures to evaluation sets. Red team continuously; new "
                "attack patterns emerge regularly.",
            ],
        },
        {
            "number": "15.10",
            "title": "Building an Evaluation Suite",
            "paragraphs": [
                "Public benchmarks are useful for comparing models. They are insufficient "
                "for evaluating your specific application. Build a custom evaluation suite.",

                "Step 1: Define what 'good' means. What user outcomes does the system "
                "produce? What failure modes matter most? Concrete examples beat abstract "
                "rubrics.",

                "Step 2: Curate test cases. Sample real user queries (or write "
                "representative ones). Cover: happy path, edge cases, adversarial cases, "
                "out-of-distribution cases. Aim for 100-1000 cases; quality over quantity.",

                "Step 3: Establish ground truth. For each case, write the ideal response, "
                "rubric scores, or pass/fail criteria. Domain experts where relevant. "
                "Document assumptions and disagreements.",

                "Step 4: Build automated evaluation. Run the system; score against ground "
                "truth using appropriate metrics (exact match, F1, LLM-as-judge, Ragas). "
                "Aggregate. Report.",

                "Step 5: Continuous expansion. Every production failure becomes a new "
                "test case. Every new feature gets test cases before launch. The "
                "evaluation suite grows with the system.",

                "Step 6: Run on every change. Prompt changes, model updates, RAG corpus "
                "changes, infrastructure changes all run through the evaluation. CI/CD "
                "for evaluation.",

                "Pitfalls. Evaluation drift: ground truth ages out. Periodic refresh. "
                "Cherry-picking: report aggregate metrics with confidence intervals, not "
                "hand-picked examples. Overfitting to evaluation: hold out a small set "
                "you only run quarterly.",
            ],
        },
        {
            "number": "15.11",
            "title": "A/B Testing in Production",
            "paragraphs": [
                "Offline evaluation is necessary but insufficient. Real users behave "
                "differently than test sets. A/B testing in production catches what "
                "offline evaluation misses.",

                "Setup. Hypothesis: state precisely what you expect ('Model B reduces "
                "support resolution time by 5%'). Pre-register. Sample size: power "
                "analysis to determine N. Stable user assignment so the same user sees "
                "the same arm.",

                "Metrics. Primary: the hypothesis metric. Secondary: leading indicators "
                "(satisfaction, retention). Guardrail: safety violations, latency, cost.",

                "Duration. Long enough to capture weekly cycles. Typically 2-4 weeks.",

                "Analysis. Standard statistical tests. Bonferroni or similar correction "
                "for multiple metrics. Sanity-check distribution match between arms.",

                "Decision. Pre-defined launch criteria. If treatment wins primary by X% "
                "with p<0.05 and no guardrail violations, launch.",

                "Caveats. Novelty effects: users may prefer new features simply because "
                "they are new. Run long enough for the novelty to wear off. Interference: "
                "if treatment and control share resources (model serving capacity), "
                "results can be confounded.",
            ],
        },
        {
            "number": "15.12",
            "title": "Summary",
            "bullets": [
                "LLM evaluation is the hard part of building LLM systems. Teams that "
                "invest in evaluation ship reliably.",
                "Classical metrics (accuracy, F1, ROC-AUC) work for classification. BLEU "
                "and ROUGE work for translation and summarization. Perplexity is an "
                "intrinsic language modeling metric.",
                "LLM-as-a-judge enables scalable evaluation of open-ended outputs. "
                "Control for position, verbosity, and self-preference biases.",
                "Public benchmarks (MMLU, HumanEval, MT-Bench) compare models but don't "
                "predict performance on your application.",
                "Ragas evaluates RAG along four axes: faithfulness, answer relevance, "
                "context precision, context recall.",
                "Hallucination evaluation (TruthfulQA, FactScore, SelfCheckGPT) and "
                "safety evaluation (BBQ, ToxiGen, AdvBench) catch failure modes specific "
                "to LLMs.",
                "Build a custom evaluation suite. Grow it with discovered failures. Run "
                "it on every change. A/B test in production for the final word.",
            ],
        },
    ],
    "further_reading": [
        "Zheng et al., 'Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena' (2023).",
        "Es et al., 'RAGAS: Automated Evaluation of Retrieval Augmented Generation' (2023).",
        "Liang et al., 'HELM: Holistic Evaluation of Language Models' (2023).",
        "Chen et al., 'Benchmarking Large Language Models in Retrieval-Augmented Generation' (2023). RGB benchmark.",
    ],
}
