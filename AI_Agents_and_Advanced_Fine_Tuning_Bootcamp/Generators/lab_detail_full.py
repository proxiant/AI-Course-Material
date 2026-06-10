"""Per-lab detail for weeks 2-12, merged into LAB_DETAIL by gen_lab_walkthroughs.

Keys are (week_num, lab_index). Week 1 labs live in gen_lab_walkthroughs.py.
"""

LAB_DETAIL_FULL = {
    (2, 0): {
        "environment": "Cluster workspace plus google-adk and a Gemini or OpenAI key in the env. Sample analyst corpus in data/filings/.",
        "concepts": [
            "Planner, worker, critic as separate LlmAgent roles",
            "Sub-agent delegation and shared session state in ADK",
            "Stop conditions: the critic approves or three revisions elapse",
        ],
        "starter_code": (
            "from google.adk.agents import LlmAgent\n\n"
            "worker = LlmAgent(\n"
            "    name='researcher', model='gemini-2.0-flash',\n"
            "    instruction='Answer the sub-question using the filings excerpts given.')\n"
            "critic = LlmAgent(\n"
            "    name='critic', model='gemini-2.0-flash',\n"
            "    instruction='Check the draft for unsupported claims. Reply APPROVE or a fix list.')\n"
            "planner = LlmAgent(\n"
            "    name='planner', model='gemini-2.0-flash',\n"
            "    instruction='Split the analyst question into sub-questions, delegate, merge.',\n"
            "    sub_agents=[worker, critic])\n"
        ),
        "checks": [
            "planner emits 2 to 4 sub-questions for the sample analyst question",
            "critic rejects at least one seeded unsupported-claim draft",
            "final answer cites which filing each figure came from",
            "trace shows planner -> worker -> critic ordering",
        ],
    },
    (2, 1): {
        "environment": "Same workspace; pip install langgraph langchain-openai.",
        "concepts": [
            "TypedDict state schema shared across nodes",
            "Conditional edges as explicit control flow",
            "Checkpointing a graph run for replay",
        ],
        "starter_code": (
            "from typing import TypedDict\n"
            "from langgraph.graph import StateGraph, END\n\n"
            "class RState(TypedDict):\n"
            "    question: str\n"
            "    drafts: list\n"
            "    approved: bool\n\n"
            "g = StateGraph(RState)\n"
            "g.add_node('research', research_node)\n"
            "g.add_node('critique', critique_node)\n"
            "g.add_edge('research', 'critique')\n"
            "g.add_conditional_edges('critique',\n"
            "    lambda s: END if s['approved'] or len(s['drafts']) >= 3 else 'research')\n"
            "g.set_entry_point('research')\n"
            "app = g.compile()\n"
        ),
        "checks": [
            "graph terminates on approval and on the 3-draft cap",
            "state after each step is inspectable via app.get_state history",
            "output quality matches the ADK version on the same 5 questions",
            "diagram of the compiled graph matches the intended topology",
        ],
    },
    (3, 0): {
        "environment": "pip install fastmcp. Fake calendar/CRM/wiki fixtures ship in fixtures/.",
        "concepts": [
            "MCP tool schemas: names, descriptions, typed parameters",
            "stdio vs streamable HTTP transports",
            "Tool descriptions are prompts: write them for the model, not the human",
        ],
        "starter_code": (
            "from fastmcp import FastMCP\n\n"
            "mcp = FastMCP('proxiant-internal')\n\n"
            "@mcp.tool()\n"
            "def calendar_read(day: str) -> list[dict]:\n"
            "    'List meetings for an ISO date, e.g. 2026-10-20.'\n"
            "    return load_fixture('calendar.json').get(day, [])\n\n"
            "@mcp.tool()\n"
            "def crm_lookup(company: str) -> dict:\n"
            "    'Return account owner, stage, and ARR for a company name.'\n"
            "    return load_fixture('crm.json').get(company, {})\n\n"
            "@mcp.tool()\n"
            "def wiki_search(query: str, k: int = 3) -> list[str]:\n"
            "    'Search internal wiki pages, returns top-k snippets.'\n"
            "    return search_fixture('wiki.json', query, k)\n\n"
            "if __name__ == '__main__':\n"
            "    mcp.run()\n"
        ),
        "checks": [
            "mcp dev session lists all three tools with correct schemas",
            "calendar_read('2026-10-20') returns the seeded two meetings",
            "an MCP client (Claude Desktop or mcp CLI) completes a 2-tool chain",
            "malformed arguments produce a schema error, not a crash",
        ],
    },
    (3, 1): {
        "environment": "Lab A server running on streamable HTTP; OAuth test IdP credentials from the TA sheet.",
        "concepts": [
            "MCPToolset in ADK: remote tool discovery",
            "OAuth 2.1 with PKCE for a protected tool",
            "Scope-limited tokens: calendar.read only",
        ],
        "starter_code": (
            "from google.adk.agents import LlmAgent\n"
            "from google.adk.tools.mcp_tool import MCPToolset\n\n"
            "tools = MCPToolset(\n"
            "    connection_params={'url': 'http://localhost:8000/mcp'},\n"
            "    auth={'type': 'oauth2', 'client_id': CLIENT_ID,\n"
            "          'scopes': ['calendar.read']},\n"
            ")\n"
            "agent = LlmAgent(name='assistant', model='gemini-2.0-flash',\n"
            "                 instruction='Use the company tools to answer.',\n"
            "                 tools=[tools])\n"
        ),
        "checks": [
            "tool discovery lists the three remote tools at startup",
            "calendar call without a token is rejected with 401",
            "after the PKCE flow the same call succeeds",
            "agent answers the meeting-plus-CRM question end to end",
        ],
    },
    (4, 0): {
        "environment": "Any LLM API key; eval set of 200 labeled tickets in data/tickets.jsonl.",
        "concepts": [
            "Structured output via JSON schema, not regex on prose",
            "Explicit refusal class beats forced choice",
            "Confusion matrix as the prompt-quality metric",
        ],
        "starter_code": (
            "SCHEMA = {\n"
            "  'type': 'object',\n"
            "  'properties': {\n"
            "    'category': {'enum': ['billing', 'auth', 'bug', 'feature',\n"
            "                          'abuse', 'refund', 'outage', 'none_of_the_above']},\n"
            "    'confidence': {'type': 'number', 'minimum': 0, 'maximum': 1},\n"
            "    'rationale': {'type': 'string', 'maxLength': 200}},\n"
            "  'required': ['category', 'confidence', 'rationale']}\n\n"
            "PROMPT = (\n"
            "  'Classify the support ticket into exactly one category. '\n"
            "  'If no category fits with confidence >= 0.6, use none_of_the_above. '\n"
            "  'Ticket: {ticket}')\n"
        ),
        "checks": [
            "100 percent of responses parse against the schema",
            "macro-F1 >= 0.80 on the 7 real categories",
            "at least 80 percent of the seeded out-of-scope tickets land in none_of_the_above",
            "rationales reference ticket text, not category definitions",
        ],
    },
    (4, 1): {
        "environment": "pip install dspy. Same ticket dataset, 100 train / 100 dev split.",
        "concepts": [
            "Signatures separate task definition from prompt wording",
            "COPRO: coordinate-ascent instruction search",
            "MIPROv2: joint instruction plus demo optimization",
        ],
        "starter_code": (
            "import dspy\n\n"
            "class TicketSig(dspy.Signature):\n"
            "    'Classify a support ticket into one of eight categories.'\n"
            "    ticket: str = dspy.InputField()\n"
            "    category: str = dspy.OutputField()\n\n"
            "classify = dspy.ChainOfThought(TicketSig)\n"
            "metric = lambda gold, pred, _ : gold.category == pred.category\n\n"
            "copro = dspy.COPRO(metric=metric)\n"
            "best_copro = copro.compile(classify, trainset=train)\n\n"
            "mipro = dspy.MIPROv2(metric=metric, auto='light')\n"
            "best_mipro = mipro.compile(classify, trainset=train)\n"
        ),
        "checks": [
            "baseline, COPRO, and MIPROv2 dev scores logged in one table",
            "at least one optimizer beats the hand prompt from Lab A",
            "optimized prompt text inspected and saved to prompts/",
            "run is reproducible from the saved program JSON",
        ],
    },
    (4, 2): {
        "environment": "GEPA reference implementation from the lab repo; same dataset and metric.",
        "concepts": [
            "Genetic-Pareto search over prompt populations",
            "Reflection-based mutation: the LLM critiques failures to propose edits",
            "Pareto front: accuracy vs prompt length",
        ],
        "starter_code": (
            "population = [seed_prompt]\n"
            "for gen in range(8):\n"
            "    scored = [(p, evaluate(p, dev)) for p in population]\n"
            "    front = pareto_front(scored, keys=('accuracy', 'neg_len'))\n"
            "    parents = sample(front, k=4)\n"
            "    children = [reflect_mutate(p, failures(p, dev)) for p in parents]\n"
            "    population = [p for p, _ in front] + children\n"
            "log_front(front)\n"
        ),
        "checks": [
            "8 generations complete within the token budget in the brief",
            "final front contains at least 3 non-dominated prompts",
            "best GEPA prompt meets or beats the MIPROv2 score from Lab B",
            "mutation log shows reflection text driving each edit",
        ],
    },
    (5, 0): {
        "environment": "1 GPU; pip install sentence-transformers. Domain corpus: 20K support-doc pairs.",
        "concepts": [
            "InfoNCE / MultipleNegativesRankingLoss with in-batch negatives",
            "Larger batches give more negatives and a stronger signal",
            "Evaluate on retrieval (recall@k), not on loss",
        ],
        "starter_code": (
            "from sentence_transformers import (SentenceTransformer, losses,\n"
            "                                   InputExample, evaluation)\n"
            "from torch.utils.data import DataLoader\n\n"
            "model = SentenceTransformer('all-MiniLM-L6-v2')\n"
            "train = [InputExample(texts=[q, pos]) for q, pos in pairs]\n"
            "loader = DataLoader(train, batch_size=64, shuffle=True)\n"
            "loss = losses.MultipleNegativesRankingLoss(model)\n"
            "ir_eval = evaluation.InformationRetrievalEvaluator(queries, corpus, relevant)\n"
            "model.fit(train_objectives=[(loader, loss)], epochs=2,\n"
            "          evaluator=ir_eval, evaluation_steps=200,\n"
            "          output_path='ckpt/embedder-v1')\n"
        ),
        "checks": [
            "recall@10 improves at least 8 points over the base model",
            "loss curve is monotonic after warmup (no divergence)",
            "embedding norms stay in a stable range (no collapse)",
            "checkpoint reloads and reproduces the eval score",
        ],
    },
    (5, 1): {
        "environment": "1x A100-class GPU per team; pip install transformers peft bitsandbytes trl.",
        "concepts": [
            "LoRA rank r and alpha: adapters on attention projections",
            "qLoRA: NF4 4-bit base plus bf16 adapters",
            "Compare on cost, wall-clock, and downstream accuracy, not loss",
        ],
        "starter_code": (
            "from transformers import AutoModelForCausalLM, BitsAndBytesConfig\n"
            "from peft import LoraConfig, get_peft_model\n\n"
            "lora_cfg = LoraConfig(r=16, lora_alpha=32, lora_dropout=0.05,\n"
            "    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj'])\n\n"
            "# run 1: full fine-tune (fp16/bf16, all params)\n"
            "# run 2: LoRA  -> get_peft_model(base, lora_cfg)\n"
            "# run 3: qLoRA -> base loaded with\n"
            "bnb = BitsAndBytesConfig(load_in_4bit=True,\n"
            "                         bnb_4bit_quant_type='nf4',\n"
            "                         bnb_4bit_compute_dtype='bfloat16')\n"
        ),
        "checks": [
            "all three runs finish on the same data and eval harness",
            "table reports VRAM peak, minutes, $ estimate, and eval accuracy",
            "LoRA trains under 1 percent of parameters (print the count)",
            "qLoRA accuracy lands within 1 to 2 points of LoRA",
        ],
    },
    (6, 0): {
        "environment": "CPU only; numpy and matplotlib.",
        "concepts": [
            "MDP: states, actions, transitions, rewards, gamma",
            "Value iteration as a fixed point of the Bellman backup",
            "Q-learning: off-policy TD with epsilon-greedy exploration",
        ],
        "starter_code": (
            "import numpy as np\n\n"
            "V = np.zeros(25)\n"
            "for sweep in range(200):\n"
            "    delta = 0\n"
            "    for s in range(25):\n"
            "        q = [sum(p * (r + 0.9 * V[s2])\n"
            "             for p, s2, r in transitions(s, a)) for a in range(4)]\n"
            "        delta = max(delta, abs(max(q) - V[s]))\n"
            "        V[s] = max(q)\n"
            "    if delta < 1e-6:\n"
            "        break\n\n"
            "Q = np.zeros((25, 4))\n"
            "for ep in range(2000):\n"
            "    s = 0\n"
            "    while not terminal(s):\n"
            "        a = epsilon_greedy(Q, s, eps=0.1)\n"
            "        s2, r = step(s, a)\n"
            "        Q[s, a] += 0.1 * (r + 0.9 * Q[s2].max() - Q[s, a])\n"
            "        s = s2\n"
        ),
        "checks": [
            "value iteration converges in under 50 sweeps (log delta)",
            "greedy policies from V and from Q agree on every non-terminal state",
            "convergence plot shows episode return vs episodes for Q-learning",
            "changing gamma to 0.5 visibly shortens the preferred path",
        ],
    },
    (6, 1): {
        "environment": "CPU; torch. Reuses the week's gridworld.",
        "concepts": [
            "Policy gradient with a clipped surrogate objective",
            "Advantage estimates against a value baseline",
            "The clip range bounds the per-update policy shift",
        ],
        "starter_code": (
            "ratio = torch.exp(logp_new - logp_old)\n"
            "clipped = torch.clamp(ratio, 1 - eps_clip, 1 + eps_clip)\n"
            "policy_loss = -torch.min(ratio * adv, clipped * adv).mean()\n"
            "value_loss = (returns - values).pow(2).mean()\n"
            "loss = policy_loss + 0.5 * value_loss - 0.01 * entropy\n"
            "# sweep eps_clip in {0.05, 0.2, 0.5} and plot return curves\n"
        ),
        "checks": [
            "PPO reaches the same optimal return as Q-learning did",
            "eps_clip=0.5 run shows visibly noisier updates than 0.2",
            "eps_clip=0.05 run learns slower but smoother",
            "entropy decays over training without collapsing to zero early",
        ],
    },
    (7, 0): {
        "environment": "2x GPU; pip install trl peft. Preference data: 5K pairs from the lab repo.",
        "concepts": [
            "Reward model from pairwise preferences",
            "PPO loop: rollout, score, KL-penalized update",
            "KL to the reference model prevents reward hacking",
        ],
        "starter_code": (
            "from trl import PPOConfig, PPOTrainer\n\n"
            "cfg = PPOConfig(model_name=BASE_1B, learning_rate=1e-6,\n"
            "                batch_size=32, mini_batch_size=8, kl_coef=0.05)\n"
            "trainer = PPOTrainer(cfg, model, ref_model, tokenizer)\n"
            "for batch in prompt_loader:\n"
            "    responses = trainer.generate(batch['input_ids'],\n"
            "                                 max_new_tokens=128)\n"
            "    rewards = reward_model.score(batch['query'], responses)\n"
            "    stats = trainer.step(batch['input_ids'], responses, rewards)\n"
            "    log(stats['objective/kl'], rewards.mean())\n"
        ),
        "checks": [
            "reward-model pairwise accuracy >= 70 percent on held-out pairs",
            "mean reward rises across PPO steps while KL stays under the target",
            "win rate vs the base model >= 60 percent on 100 prompts (LLM judge)",
            "no degeneration: response length and distinct-2 stay in range",
        ],
    },
    (7, 1): {
        "environment": "Same rig and data as Lab A.",
        "concepts": [
            "GRPO: group-relative advantages, no value head",
            "Group size trades signal quality for compute",
            "Verifiable rewards slot directly into the same loop",
        ],
        "starter_code": (
            "from trl import GRPOConfig, GRPOTrainer\n\n"
            "cfg = GRPOConfig(num_generations=8, learning_rate=1e-6,\n"
            "                 beta=0.04)  # KL weight\n"
            "trainer = GRPOTrainer(model=BASE_1B, args=cfg,\n"
            "                      reward_funcs=[reward_model.score],\n"
            "                      train_dataset=prompts)\n"
            "trainer.train()\n"
        ),
        "checks": [
            "GRPO run uses measurably less VRAM than PPO (no value head)",
            "final win rate within a few points of the PPO run",
            "per-group reward spread logged; advantage normalization verified",
            "report compares PPO vs GRPO on VRAM, time, and win rate",
        ],
    },
    (7, 2): {
        "environment": "Same rig; the raw preference pairs (not the reward model).",
        "concepts": [
            "DPO: closed-form preference optimization against a reference",
            "beta controls how far the policy can drift",
            "No reward model and no rollouts: pure supervised-style loop",
        ],
        "starter_code": (
            "from trl import DPOConfig, DPOTrainer\n\n"
            "cfg = DPOConfig(beta=0.1, learning_rate=5e-7,\n"
            "                max_length=512, max_prompt_length=256)\n"
            "trainer = DPOTrainer(model=BASE_1B, ref_model=None,  # PEFT ref\n"
            "                     args=cfg, train_dataset=pairs,\n"
            "                     processing_class=tokenizer)\n"
            "trainer.train()\n"
        ),
        "checks": [
            "implicit-reward margin (chosen minus rejected) grows during training",
            "DPO finishes in well under half the PPO wall-clock",
            "three-way judge comparison PPO vs GRPO vs DPO on the same 100 prompts",
            "writeup states when each method is the right choice",
        ],
    },
    (8, 0): {
        "environment": "Cluster; pip install vllm 'ray[serve]' locust prometheus-client.",
        "concepts": [
            "PagedAttention and continuous batching in vLLM",
            "Ray Serve deployments, replicas, and autoscaling",
            "p50 vs p95 vs p99 under increasing concurrency",
        ],
        "starter_code": (
            "from ray import serve\n"
            "from vllm import LLM, SamplingParams\n\n"
            "@serve.deployment(num_replicas=2, ray_actor_options={'num_gpus': 1})\n"
            "class Generator:\n"
            "    def __init__(self):\n"
            "        self.llm = LLM(model='ckpt/lora-merged')\n"
            "    async def __call__(self, request):\n"
            "        prompt = (await request.json())['prompt']\n"
            "        out = self.llm.generate([prompt],\n"
            "              SamplingParams(max_tokens=128))\n"
            "        return {'text': out[0].outputs[0].text}\n\n"
            "serve.run(Generator.bind())\n"
            "# locust -u 64 -r 8 -H http://localhost:8000\n"
        ),
        "checks": [
            "throughput (req/s) at 1, 8, 64 concurrent users recorded",
            "p95 latency at 64 users stays under the rubric bound",
            "tokens/s and batch occupancy visible in the vLLM metrics",
            "one replica killed mid-test: Serve recovers without 5xx storms",
        ],
    },
    (8, 1): {
        "environment": "Airflow 2.x local executor; cluster access for Ray Train.",
        "concepts": [
            "DAG as the contract: pull, train, evaluate, gate, deploy",
            "Eval gate blocks bad models from shipping",
            "Idempotent tasks and retries with backoff",
        ],
        "starter_code": (
            "from airflow.decorators import dag, task\n\n"
            "@dag(schedule='@weekly', catchup=False)\n"
            "def ft_pipeline():\n"
            "    @task\n"
            "    def pull():   return stage_dataset('s3://corpus/weekly')\n"
            "    @task\n"
            "    def train(path):  return ray_train_lora(path)\n"
            "    @task\n"
            "    def evaluate(ckpt): return run_eval_suite(ckpt)\n"
            "    @task.branch\n"
            "    def gate(scores):\n"
            "        return 'deploy' if scores['win_rate'] >= 0.55 else 'halt'\n"
            "    @task\n"
            "    def deploy(ckpt): serve_update(ckpt)\n"
            "    @task\n"
            "    def halt(): notify('model below gate, kept previous')\n"
            "    s = evaluate(train(pull())); g = gate(s)\n"
            "    g >> [deploy(s), halt()]\n"
            "ft_pipeline()\n"
        ),
        "checks": [
            "full DAG run green end to end on the sample corpus",
            "gate routes to halt when the eval threshold is raised above the score",
            "task retry works: kill the train task once, run recovers",
            "deployed endpoint serves the new checkpoint (version header changes)",
        ],
    },
    (9, 0): {
        "environment": "Cluster; ray>=2.9 with Ray Data; qdrant or pgvector endpoint from the TA sheet.",
        "concepts": [
            "Ray Data: streaming execution over blocks",
            "map_batches with GPU actors for the embedding stage",
            "Backpressure and block size tuning for 100 GB inputs",
        ],
        "starter_code": (
            "import ray\n\n"
            "ds = ray.data.read_json('s3://corpus/jsonl/')        # 100 GB\n"
            "ds = ds.filter(lambda r: len(r['text']) > 80)\n"
            "ds = ds.map(normalize_record)\n\n"
            "class Embedder:\n"
            "    def __init__(self):\n"
            "        from sentence_transformers import SentenceTransformer\n"
            "        self.m = SentenceTransformer('ckpt/embedder-v1', device='cuda')\n"
            "    def __call__(self, batch):\n"
            "        batch['vec'] = self.m.encode(list(batch['text']),\n"
            "                                     batch_size=256).tolist()\n"
            "        return batch\n\n"
            "ds = ds.map_batches(Embedder, concurrency=4,\n"
            "                    num_gpus=1, batch_size=1024)\n"
            "ds.map_batches(upsert_to_vector_store, batch_size=512)\n"
        ),
        "checks": [
            "pipeline sustains all 4 GPU actors busy (Ray dashboard)",
            "row counts match: input minus filtered equals upserted",
            "vector store returns sane neighbors for 10 probe queries",
            "rerun after a worker kill completes without duplicate upserts",
        ],
    },
    (9, 1): {
        "environment": "google-adk with A2A enabled plus httpx for the custom client.",
        "concepts": [
            "Agent Card: served capability descriptor",
            "A2A task lifecycle: submitted, working, completed",
            "JSON-RPC message/send and tasks/get",
        ],
        "starter_code": (
            "# server: expose the ADK agent over A2A\n"
            "from google.adk.a2a.utils.agent_to_a2a import to_a2a\n"
            "a2a_app = to_a2a(root_agent, port=8001)\n\n"
            "# custom client\n"
            "import httpx\n"
            "card = httpx.get('http://localhost:8001/.well-known/agent-card.json').json()\n"
            "task = httpx.post(card['url'], json={\n"
            "    'jsonrpc': '2.0', 'id': 1, 'method': 'message/send',\n"
            "    'params': {'message': {'role': 'user', 'parts': [\n"
            "        {'kind': 'text', 'text': 'Summarize the Q3 pipeline.'}]}},\n"
            "}).json()\n"
        ),
        "checks": [
            "agent card served at the well-known path with correct skills",
            "message/send returns a task id; tasks/get reaches completed",
            "client handles the working state with polling and a timeout",
            "invalid method returns a JSON-RPC error object, not a 500",
        ],
    },
    (10, 0): {
        "environment": "langgraph plus the lab registry service (FastAPI, ships in repo).",
        "concepts": [
            "Registry as discovery: capabilities, endpoint, version",
            "A2A between two independently-built agents",
            "Task envelopes: id, sender, capability, payload",
        ],
        "starter_code": (
            "# register on startup\n"
            "httpx.post(REGISTRY + '/register', json={\n"
            "    'name': 'extractor', 'capability': 'pdf-extract',\n"
            "    'endpoint': 'http://localhost:9001/a2a'})\n\n"
            "# discover and call from the second agent\n"
            "peer = httpx.get(REGISTRY + '/find',\n"
            "                 params={'capability': 'pdf-extract'}).json()\n"
            "result = a2a_send(peer['endpoint'], task={\n"
            "    'capability': 'pdf-extract', 'payload': {'doc_id': 'fin-204'}})\n"
        ),
        "checks": [
            "both agents appear in GET /agents after startup",
            "summarizer discovers the extractor and completes the chained task",
            "killing the extractor yields a clean capability-unavailable error",
            "re-registration after restart works without duplicate entries",
        ],
    },
    (10, 1): {
        "environment": "Any LLM API key; the week's eval harness (50 task cases).",
        "concepts": [
            "Router: classify then dispatch to a specialist",
            "Orchestrator-workers: decompose, fan out, merge",
            "Evaluator-optimizer: generate, critique, revise loop",
        ],
        "starter_code": (
            "def router(task):\n"
            "    kind = classify(task, labels=['math', 'lookup', 'writing'])\n"
            "    return SPECIALISTS[kind](task)\n\n"
            "def orchestrator(task):\n"
            "    subs = decompose(task)\n"
            "    results = parallel_map(worker, subs)\n"
            "    return merge(task, results)\n\n"
            "def evaluator_optimizer(task, max_rounds=3):\n"
            "    draft = generate(task)\n"
            "    for _ in range(max_rounds):\n"
            "        verdict = critique(task, draft)\n"
            "        if verdict['pass']:\n"
            "            break\n"
            "        draft = revise(task, draft, verdict['feedback'])\n"
            "    return draft\n"
        ),
        "checks": [
            "all three patterns run the same 50-case suite",
            "table reports quality score, tokens, latency per pattern",
            "router wins on cost for single-skill tasks; orchestrator on multi-part",
            "writeup picks a pattern per task family with justification",
        ],
    },
    (11, 0): {
        "environment": "Cluster; corpus of 100K docs pre-indexed in qdrant + OpenSearch + DuckDB (TA sheet).",
        "concepts": [
            "Tool selection across vector, BM25, and SQL backends",
            "Multi-hop: evidence from hop 1 shapes the hop 2 query",
            "Stop conditions and evidence budgets",
        ],
        "starter_code": (
            "TOOLS = {'vector': vector_search, 'bm25': keyword_search,\n"
            "         'sql': duckdb_query}\n\n"
            "def agentic_rag(question, max_hops=4):\n"
            "    evidence = []\n"
            "    for hop in range(max_hops):\n"
            "        plan = llm_plan(question, evidence)   # tool + query + why\n"
            "        if plan['action'] == 'answer':\n"
            "            break\n"
            "        hits = TOOLS[plan['tool']](plan['query'], k=6)\n"
            "        evidence += rerank(question, hits)[:3]\n"
            "    return grounded_answer(question, evidence)\n"
        ),
        "checks": [
            "single-hop questions answer in one hop (no wasted calls)",
            "the 10 seeded multi-hop questions need 2+ hops and get them right",
            "numeric questions route to SQL, not vector search",
            "every answer cites evidence ids; uncited claims fail the harness",
        ],
    },
    (11, 1): {
        "environment": "Lab A system instrumented; pip install agentlightning (or the repo trainer).",
        "concepts": [
            "Trajectories: state, action, observation, reward tuples",
            "Filtering to successful runs before imitation",
            "Train the small model on decisions, not final answers",
        ],
        "starter_code": (
            "# 1) capture: wrap the lab A loop\n"
            "traj.log(step={'obs': question_state, 'action': plan,\n"
            "               'result': hits_summary})\n"
            "traj.finalize(reward=harness_score)\n\n"
            "# 2) build the imitation set from successes\n"
            "good = [t for t in load_trajs() if t.reward >= 0.8]\n"
            "sft = [{'prompt': render(t.steps[:i]),\n"
            "        'completion': t.steps[i].action_json}\n"
            "       for t in good for i in range(len(t.steps))]\n\n"
            "# 3) SFT a 1B student on the decision data, then re-run the harness\n"
        ),
        "checks": [
            "at least 300 trajectories captured; success rate reported",
            "student model emits valid tool-plan JSON on 95+ percent of cases",
            "student harness score within 10 points of the teacher system",
            "cost per question drops by the factor stated in your report",
        ],
    },
    (12, 0): {
        "environment": "Your capstone repo; ruff, pytest, and the course eval template.",
        "concepts": [
            "Reproducibility: pinned deps, seeds, one-command run",
            "Eval suite as the capstone's spine (50 cases minimum)",
            "Observability: traces a reviewer can open",
        ],
        "starter_code": (
            "# Makefile targets the graders will run\n"
            "setup:    pip install -r requirements.lock\n"
            "test:     ruff check . && pytest -q\n"
            "eval:     python -m capstone.eval --cases evals/cases.jsonl \\\n"
            "          --report out/eval_report.md\n"
            "demo:     python -m capstone.demo --trace out/trace.html\n"
        ),
        "checks": [
            "fresh-clone setup + eval completes on a clean machine",
            "eval suite has >= 50 cases with pass/fail criteria",
            "README states the four course patterns used and where",
            "traces show tool calls for three representative runs",
        ],
    },
    (12, 1): {
        "environment": "Presentation room A/V; rubric sheets from the TA.",
        "concepts": [
            "10 slides: problem, architecture, patterns, evals, costs, lessons",
            "Peer review against the structured rubric, not vibes",
            "Live demo with a fallback recording",
        ],
        "starter_code": (
            "# peer_review.py: aggregate rubric sheets\n"
            "import csv, statistics\n"
            "rows = list(csv.DictReader(open('reviews.csv')))\n"
            "by_team = {}\n"
            "for r in rows:\n"
            "    by_team.setdefault(r['team'], []).append(\n"
            "        sum(int(r[k]) for k in ('design', 'evals', 'demo', 'clarity')))\n"
            "for team, scores in sorted(by_team.items()):\n"
            "    print(team, round(statistics.mean(scores), 1))\n"
        ),
        "checks": [
            "presentation fits 10 slides and the 12-minute slot",
            "each student submits two completed peer rubrics",
            "demo runs live or the fallback recording plays",
            "faculty critique delivered in writing within the week",
        ],
    },
}
