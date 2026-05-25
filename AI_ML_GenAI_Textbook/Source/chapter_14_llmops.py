"""Chapter 14: LLMOps and System Design."""

CHAPTER = {
    "label": "Chapter 14",
    "title": "LLMOps and Production System Design",
    "sections": [
        {
            "number": "14.1",
            "title": "From Model to System",
            "paragraphs": [
                "A working model is not a working product. Bridging that gap is the "
                "discipline of LLMOps. It includes architecture (how the components fit "
                "together), serving infrastructure (how requests get from users to GPUs "
                "and back), monitoring (how you know the system is healthy), evaluation "
                "(how you know the system is actually good), and continuous improvement "
                "(how the system gets better over time).",

                "Traditional MLOps assumes a model with fixed inputs and outputs that "
                "produces clear metrics. LLMOps inherits those assumptions but adds: "
                "prompts that change frequently, retrieval components with their own "
                "quality, tool calls to external systems, conversational state, "
                "alignment-related risks, and an evaluation problem that is fundamentally "
                "harder because outputs are open-ended.",

                "This chapter walks the production landscape. It is opinionated about what "
                "matters most: latency, cost, observability, evaluation, and safety. The "
                "specific tools change quickly; the principles are durable.",
            ],
        },
        {
            "number": "14.2",
            "title": "Serving Infrastructure",
            "paragraphs": [
                "Modern LLM serving is dominated by a few patterns and tools.",
            ],
            "subsections": [
                {
                    "title": "14.2.1 vLLM and Continuous Batching",
                    "paragraphs": [
                        "vLLM (Kwon et al., 2023) introduced PagedAttention, a technique "
                        "that manages the KV-cache like virtual memory. Combined with "
                        "continuous batching (dynamically merging requests of different "
                        "lengths into batches), vLLM achieves 5-24x throughput over naive "
                        "batching.",
                        "The default serving stack for self-hosted LLMs. Compatible with "
                        "most Hugging Face models. Supports tensor parallelism, "
                        "quantization (AWQ, GPTQ, FP8), speculative decoding, structured "
                        "outputs.",
                        "Alternatives. Hugging Face TGI (Text Generation Inference). "
                        "TensorRT-LLM from NVIDIA. SGLang. Ollama for local development. "
                        "Each has tradeoffs; vLLM is the broadest fit.",
                    ],
                },
                {
                    "title": "14.2.2 Tensor and Pipeline Parallelism",
                    "paragraphs": [
                        "A 70B model does not fit on a single GPU. Tensor parallelism "
                        "shards each matrix multiplication across devices (split a "
                        "8192-wide layer into 8 pieces of 1024 across 8 GPUs). Pipeline "
                        "parallelism splits the model by layers, with micro-batches "
                        "flowing through.",
                        "Modern frontier serving uses both: tensor parallelism within a "
                        "node (high inter-GPU bandwidth via NVLink), pipeline parallelism "
                        "across nodes. Mixed-precision (BF16 or FP8) reduces memory and "
                        "compute by 2-4x.",
                        "Inference parallelism is different from training parallelism. "
                        "Inference is latency-sensitive; training is throughput-sensitive. "
                        "Choose configurations accordingly.",
                    ],
                },
                {
                    "title": "14.2.3 Quantization for Serving",
                    "paragraphs": [
                        "Quantizing the served model reduces memory and increases "
                        "throughput. INT8 quantization typically loses less than 1 point "
                        "on benchmarks. INT4 (AWQ, GPTQ) loses 1-3 points but offers 4x "
                        "compression and large speedups. FP8 is the modern compromise: "
                        "near-fp16 quality with substantial efficiency gains.",
                        "Tradeoffs. Quantization adds engineering complexity (calibration, "
                        "post-training vs quantization-aware training). Quality may drop "
                        "on long contexts or specific tasks. Test on your eval set, not "
                        "just published benchmarks.",
                    ],
                },
                {
                    "title": "14.2.4 Speculative Decoding",
                    "paragraphs": [
                        "A small draft model proposes the next k tokens. The main model "
                        "verifies in a single forward pass. Accepted tokens become "
                        "output; rejected tokens fall back to the main model.",
                        "Speedup. Up to 2-3x for tasks where the draft model's predictions "
                        "are mostly correct. Code generation and structured outputs benefit "
                        "most.",
                        "Cost. Run two models. The draft model overhead is small but real. "
                        "Quality is unchanged (verification by the main model ensures the "
                        "output distribution matches main-model-only).",
                    ],
                },
            ],
        },
        {
            "number": "14.3",
            "title": "Latency and Cost Engineering",
            "paragraphs": [
                "User-perceived latency in an LLM application has several components.",

                "Time to first token (TTFT). How long from user submission to the first "
                "streamed token. Dominates the user's impression of speed in chat "
                "interfaces. Reduced by: shorter prompts (RAG retrieval, prompt caching), "
                "smaller models for the first response, speculative decoding.",

                "Inter-token latency. How fast tokens stream after the first. Determined "
                "by model size, batching, hardware. Continuous batching helps under load.",

                "Total response latency. TTFT plus total tokens times inter-token latency. "
                "Some applications care more about TTFT (chat) and others about total "
                "latency (batch jobs).",

                "Cost components. Input tokens: dominant for RAG (long context). Output "
                "tokens: dominant for generation-heavy tasks. Tool calls: external service "
                "costs plus latency. Inference compute: GPU hours.",

                "Cost optimization patterns. Prompt caching: API providers cache shared "
                "prefixes; reuses dramatically reduce cost. Smaller models for simple "
                "tasks; route based on query complexity. Aggressive quantization. "
                "Reducing retrieval candidates so generation prompts are shorter.",

                "Caching strategy. Exact-match cache for repeated queries. Semantic cache "
                "for similar queries. Prompt cache for shared prefixes. Each helps "
                "different traffic patterns; combine them.",
            ],
        },
        {
            "number": "14.4",
            "title": "Multi-Tenant Serving",
            "paragraphs": [
                "Many production LLM applications serve multiple customers with different "
                "needs from shared infrastructure. Multi-tenant serving has its own design "
                "considerations.",

                "Adapter swapping. Serve a single base model with LoRA adapters per "
                "tenant. Load adapters dynamically. Each tenant gets a customized model "
                "without provisioning a separate base. Implementations: vLLM with "
                "multi-LoRA, S-LoRA.",

                "Routing. Different queries should go to different models. Cheap small "
                "model for simple queries. Larger model for complex queries. Reasoning "
                "model for math and code. A learned or rule-based router picks. The router "
                "must be fast (sub-100ms) and correct often enough to justify the "
                "complexity.",

                "Isolation. Tenants should not see each other's data. Per-tenant rate "
                "limits prevent one tenant from monopolizing GPUs. Audit logs per tenant "
                "for compliance.",

                "Cost allocation. Track tokens, latency, and model usage per tenant. "
                "Charge appropriately. Surface usage to customers.",
            ],
        },
        {
            "number": "14.5",
            "title": "Observability",
            "paragraphs": [
                "You cannot improve what you cannot measure. LLM observability is more "
                "complex than traditional service observability because the outputs are "
                "open-ended.",

                "Distributed tracing. Each user request is a trace. Spans for retrieval, "
                "reranking, prompt construction, LLM generation, post-processing, tool "
                "calls. OpenTelemetry is the standard. Hosted platforms: Helicone, "
                "LangFuse, Arize, Langsmith. Custom Grafana dashboards work too.",

                "Per-request metrics. Latency (P50, P95, P99). Token counts (input, "
                "output). Cost. Tool calls. Cache hits.",

                "Aggregate metrics. Throughput. Error rate. Queue depth. GPU utilization. "
                "Cost per active user. These are the metrics a platform team watches.",

                "Quality metrics. User feedback (thumbs, regenerate rate). LLM-as-judge "
                "scores on sampled traffic. Refusal rate. Average response length. These "
                "drift over time; trend them.",

                "Safety metrics. Jailbreak attempts. PII exposure events. Policy "
                "violations. Audit logs.",

                "Alerting. Define SLOs (service level objectives) for latency, error rate, "
                "and quality. Alert on regression. Be careful about alert fatigue; the "
                "right alerts page on real problems and stay quiet otherwise.",
            ],
        },
        {
            "number": "14.6",
            "title": "Tool Use and the Model Context Protocol",
            "paragraphs": [
                "Modern LLMs increasingly call external tools: search, code execution, "
                "databases, internal APIs. Tool use extends the model's reach but adds "
                "engineering complexity.",

                "Tool definition. Each tool has a name, description, input schema, output "
                "schema. The LLM reads these and decides which to call. Names and "
                "descriptions matter more than people realize; ambiguity here produces "
                "wrong tool calls.",

                "The Model Context Protocol (MCP, Anthropic, 2024). A clean abstraction "
                "for tools. A FastMCP server exposes tools, resources, and prompts. An "
                "agent client connects, negotiates capabilities at session start, and "
                "invokes tools via JSON-RPC. Separates tool definition from agent runtime, "
                "making tools reusable across agents.",

                "Tool design. Names should be verbs matching user intent. Descriptions "
                "should be unambiguous. Argument names are also the prompt; 'date' is bad, "
                "'start_date_iso8601' is good. Errors should be structured (tool_"
                "unavailable, invalid_input, rate_limited) so the agent can reason about "
                "retry.",

                "Idempotency. Write tools must accept idempotency keys. Retries with the "
                "same key are no-ops. Otherwise transient failures become double-charge "
                "incidents.",

                "Sandboxing. Code execution tools must run in isolated environments. "
                "File system access must be scoped. Network access must be limited. The "
                "agent should be allowed to make mistakes without destroying the user's "
                "data.",
            ],
        },
        {
            "number": "14.7",
            "title": "Agentic Systems",
            "paragraphs": [
                "An agent is a program that perceives, plans, acts via tools, and observes "
                "results in a loop. Modern AI applications increasingly are agents rather "
                "than single LLM calls.",

                "Agent design patterns. Router: classify input, dispatch to a specialized "
                "agent or pipeline. Orchestrator-workers: a planner agent delegates "
                "sub-tasks to worker agents. Evaluator-optimizer: a generator agent "
                "produces, a critic agent evaluates, the generator revises. Autonomy "
                "ladder: progressively grant the agent more freedom as it proves reliable.",

                "Single agent vs multi-agent. Single agent with many tools is the default; "
                "easier to debug, simpler to deploy. Multi-agent makes sense when "
                "responsibilities are genuinely separable and agents need different "
                "context windows or capabilities.",

                "State management. Conversational state for multi-turn agents. Persistent "
                "memory for long-running agents. Idempotent state transitions so the "
                "agent can recover from interruptions.",

                "Evaluation. Agentic systems are harder to evaluate than single LLM calls. "
                "Define success criteria for tasks the agent should complete. Track "
                "completion rate, intervention rate (human had to step in), and cost per "
                "task. End-to-end evaluation on representative tasks is essential.",

                "Failure modes. Hallucinated tools (calling functions that don't exist). "
                "Infinite loops (no termination condition). Prompt injection through tool "
                "outputs. Mistaken tool choices. Each requires engineering attention.",
            ],
        },
        {
            "number": "14.8",
            "title": "MLOps for the LLM Era",
            "paragraphs": [
                "Classical MLOps focuses on training, model registries, A/B testing, "
                "monitoring. The LLM era extends these.",

                "Prompt versioning. Treat prompts as code. Store in git. Review changes. "
                "Tie deployed versions to evaluation results. Roll back on regression.",

                "Evaluation pipelines. Automated evaluation on every prompt change, model "
                "version, or RAG corpus update. Pre-merge checks: does this change "
                "improve quality? Does it regress anything?",

                "Canary deployments. New prompt, model, or pipeline version goes to a "
                "small fraction of traffic. Compare against control. Roll out gradually if "
                "metrics look good; roll back if not.",

                "Continuous improvement. Sample production traffic. Identify failure "
                "cases. Add them to evaluation set. Iterate on prompts and models. "
                "Production data is the most valuable input to improvement.",

                "Cost monitoring. LLM costs scale with usage. Track per-feature, per-"
                "tenant, per-user. Alert on spikes. Optimize the dominant cost drivers.",
            ],
        },
        {
            "number": "14.9",
            "title": "Building a ChatGPT-Like System",
            "paragraphs": [
                "A worked example: how would you build a production chat assistant from "
                "scratch?",

                "Frontend. Web app with streaming responses, conversation history, file "
                "upload. Mobile apps. APIs for developers.",

                "Backend. Stateless API layer behind a load balancer. Session management "
                "with persistent conversation store (Postgres or a NoSQL store). Per-user "
                "rate limiting.",

                "Model serving. vLLM behind a load balancer. Continuous batching. KV-"
                "cache management. Speculative decoding for latency. Routing for query "
                "complexity (small model for simple queries, large for complex).",

                "Models. A frontier base LLM with SFT and RLHF for chat. Optionally "
                "specialized variants (code, reasoning, multimodal).",

                "Tool use. Function calling for web search, code execution, image "
                "generation, calendar, email. Tool registry. Safe execution sandboxes.",

                "RAG. Optional, for memory and document upload features. Per-user "
                "knowledge bases for personalization.",

                "Safety. Input filters (prompt injection, harmful intent), output "
                "filters (toxicity, PII), refusal calibration, jailbreak detection. "
                "Continuous red teaming.",

                "Operations. Observability (traces, metrics, logs). Feature flags. A/B "
                "testing. Incident response. Compliance: SOC 2, GDPR, regional data "
                "residency.",

                "Scale. Tens of millions of users requires global multi-region "
                "deployment, specialized hardware, careful capacity planning.",
            ],
        },
        {
            "number": "14.10",
            "title": "Summary",
            "bullets": [
                "Production LLM systems are more than models: they are serving "
                "infrastructure, prompts, retrievers, tools, guardrails, and monitoring.",
                "vLLM with continuous batching is the modern self-hosted serving default. "
                "Tensor and pipeline parallelism handle large models. Quantization (INT8, "
                "AWQ, FP8) reduces cost.",
                "Latency components: time to first token, inter-token latency, total "
                "response time. Cost components: input tokens, output tokens, tool calls, "
                "inference compute.",
                "Multi-tenant serving uses adapter swapping (LoRA per tenant) and routing "
                "to serve diverse needs from shared infrastructure.",
                "Observability requires distributed tracing, per-request metrics, quality "
                "monitoring, and safety tracking.",
                "MCP standardizes tool exposure. Agents extend LLMs with tools, planning, "
                "and persistent state.",
                "MLOps for the LLM era includes prompt versioning, automated evaluation "
                "pipelines, canary deployments, and continuous improvement from "
                "production data.",
            ],
        },
    ],
    "further_reading": [
        "Kwon et al., 'Efficient Memory Management for Large Language Model Serving with PagedAttention' (2023). vLLM.",
        "Sheng et al., 'S-LoRA: Serving Thousands of Concurrent LoRA Adapters' (2023).",
        "Leviathan, Kalman, Matias, 'Fast Inference from Transformers via Speculative Decoding' (2022).",
        "Anthropic, 'Building Effective Agents' engineering blog (2024).",
    ],
}
