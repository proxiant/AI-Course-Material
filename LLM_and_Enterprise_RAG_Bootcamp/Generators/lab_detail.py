"""Per-lab starter code and verification checks for the RAG bootcamp.

Keyed by (week_num, lab_index). Rendered into every lab walkthrough by
gen_all.build_labs. Starter code is real, runnable Python with TODO markers
where students fill in the lab work.
"""

LAB_DETAIL = {
    (1, 0): {
        "starter_code": (
            "import ray\n"
            "import torch\n"
            "\n"
            "ray.init(address='ray://head.proxiant.internal:10001')\n"
            "print(ray.cluster_resources())  # expect GPU >= 1\n"
            "\n"
            "@ray.remote(num_gpus=1)\n"
            "def gpu_smoke_test():\n"
            "    name = torch.cuda.get_device_name(0)\n"
            "    x = torch.randn(2048, 2048, device='cuda')\n"
            "    y = (x @ x).sum().item()\n"
            "    return name, y\n"
            "\n"
            "@ray.remote(num_gpus=1)\n"
            "def load_embedder(model_id='BAAI/bge-small-en-v1.5'):\n"
            "    from sentence_transformers import SentenceTransformer\n"
            "    model = SentenceTransformer(model_id, device='cuda')\n"
            "    vec = model.encode(['hello bootcamp'])\n"
            "    return vec.shape\n"
            "\n"
            "print(ray.get(gpu_smoke_test.remote()))\n"
            "print(ray.get(load_embedder.remote()))  # expect (1, 384)\n"
        ),
        "checks": [
            "ray.cluster_resources() reports at least one GPU and the dashboard URL loads.",
            "gpu_smoke_test returns an RTX device name and a finite matmul sum (no NaN).",
            "load_embedder returns shape (1, 384) in under 60 seconds on a warm node.",
            "conda env list shows the bootcamp env and python -c 'import torch; print(torch.__version__)' prints 2.4 or later.",
        ],
    },
    (1, 1): {
        "starter_code": (
            "import faiss\n"
            "import numpy as np\n"
            "from sentence_transformers import SentenceTransformer\n"
            "\n"
            "model = SentenceTransformer('BAAI/bge-small-en-v1.5')\n"
            "\n"
            "def chunk(text, size=500, overlap=50):\n"
            "    words = text.split()\n"
            "    step = size - overlap\n"
            "    return [' '.join(words[i:i + size]) for i in range(0, len(words), step)]\n"
            "\n"
            "docs = load_corpus('data/corpus_200.jsonl')  # provided by the lab repo\n"
            "chunks = [c for d in docs for c in chunk(d['text'])]\n"
            "emb = model.encode(chunks, normalize_embeddings=True)\n"
            "index = faiss.IndexFlatIP(emb.shape[1])\n"
            "index.add(emb.astype(np.float32))\n"
            "\n"
            "def retrieve(query, k=8):\n"
            "    qv = model.encode([query], normalize_embeddings=True)\n"
            "    scores, ids = index.search(qv.astype(np.float32), k)\n"
            "    return [(chunks[i], float(s)) for i, s in zip(ids[0], scores[0])]\n"
            "\n"
            "def generate(query, context_chunks):\n"
            "    # TODO: call your LLM API with a grounded prompt and citations\n"
            "    raise NotImplementedError\n"
        ),
        "checks": [
            "Index size equals the number of chunks (index.ntotal == len(chunks)).",
            "retrieve('What is the refund policy?') returns 8 results with scores in descending order between -1 and 1.",
            "recall@8 on the provided 20-query set is at least 0.70.",
            "End-to-end answer latency P95 is under 5 seconds on the 20 sample queries.",
        ],
    },
    (2, 0): {
        "starter_code": (
            "import numpy as np\n"
            "from sentence_transformers import SentenceTransformer\n"
            "\n"
            "MODELS = ['all-mpnet-base-v2', 'BAAI/bge-base-en-v1.5',\n"
            "          'thenlper/gte-base']\n"
            "sentences = load_sentences('data/wiki_5k.txt')  # 5000 lines\n"
            "\n"
            "def anisotropy(emb):\n"
            "    emb = emb / np.linalg.norm(emb, axis=1, keepdims=True)\n"
            "    sample = emb[np.random.choice(len(emb), 1000, replace=False)]\n"
            "    sims = sample @ sample.T\n"
            "    mask = ~np.eye(len(sample), dtype=bool)\n"
            "    return sims[mask].mean()\n"
            "\n"
            "def whiten(emb):\n"
            "    mu = emb.mean(axis=0)\n"
            "    cov = np.cov((emb - mu).T)\n"
            "    u, s, _ = np.linalg.svd(cov)\n"
            "    w = u @ np.diag(1.0 / np.sqrt(s + 1e-9))\n"
            "    return (emb - mu) @ w\n"
            "\n"
            "for name in MODELS:\n"
            "    emb = SentenceTransformer(name).encode(sentences)\n"
            "    print(name, 'raw:', anisotropy(emb), 'whitened:', anisotropy(whiten(emb)))\n"
            "    # TODO: benchmark retrieval recall@10 on STS-B before and after\n"
        ),
        "checks": [
            "Raw anisotropy for each model is a single scalar; plain BERT-style models land well above 0.3.",
            "After whitening, mean pairwise cosine drops to roughly 0 (absolute value under 0.05).",
            "Whitened embeddings keep their shape (n, d) and contain no NaNs (np.isfinite check passes).",
            "The before/after recall@10 table covers all three models from the same eval split.",
        ],
    },
    (2, 1): {
        "starter_code": (
            "import torch\n"
            "import torch.nn.functional as F\n"
            "from torch.utils.data import DataLoader\n"
            "\n"
            "def info_nce(anchors, positives, temperature=0.1):\n"
            "    a = F.normalize(anchors, dim=1)\n"
            "    p = F.normalize(positives, dim=1)\n"
            "    logits = a @ p.T / temperature\n"
            "    labels = torch.arange(len(a), device=logits.device)\n"
            "    return F.cross_entropy(logits, labels)\n"
            "\n"
            "model = load_base_encoder()              # provided wrapper\n"
            "pairs = load_pairs('data/pairs_10k.tsv') # (query, positive) rows\n"
            "loader = DataLoader(pairs, batch_size=64, shuffle=True)\n"
            "opt = torch.optim.AdamW(model.parameters(), lr=2e-5)\n"
            "\n"
            "for epoch in range(2):\n"
            "    for queries, positives in loader:\n"
            "        loss = info_nce(model.encode(queries), model.encode(positives))\n"
            "        loss.backward()\n"
            "        opt.step()\n"
            "        opt.zero_grad()\n"
            "    print('epoch', epoch, 'loss', loss.item())\n"
            "# TODO: evaluate recall@10 on the held-out set vs the pretrained baseline\n"
        ),
        "checks": [
            "A sanity batch where positives equal anchors drives loss toward 0 within a few steps.",
            "Training loss falls below ln(batch_size) (about 4.16 for batch 64) by the end of epoch 1.",
            "Held-out recall@10 improves over the pretrained baseline by at least 3 points.",
            "Swapping temperature 0.1 to 0.05 changes the loss value, confirming temperature is wired in.",
        ],
    },
    (3, 0): {
        "starter_code": (
            "from dataclasses import dataclass\n"
            "\n"
            "@dataclass\n"
            "class Chunk:\n"
            "    text: str\n"
            "    doc_id: str\n"
            "    strategy: str\n"
            "\n"
            "def chunk_fixed(doc, size=400, overlap=50):\n"
            "    words = doc['text'].split()\n"
            "    step = size - overlap\n"
            "    return [Chunk(' '.join(words[i:i + size]), doc['id'], 'fixed')\n"
            "            for i in range(0, len(words), step)]\n"
            "\n"
            "def chunk_semantic(doc, threshold=0.55):\n"
            "    # TODO: split where cosine similarity between adjacent\n"
            "    # sentence embeddings dips below threshold\n"
            "    raise NotImplementedError\n"
            "\n"
            "def chunk_late(doc, embedder):\n"
            "    # TODO: embed full doc with a long-context embedder, then\n"
            "    # mean-pool token vectors per chunk span\n"
            "    raise NotImplementedError\n"
            "\n"
            "def chunk_contextual(doc, llm):\n"
            "    # TODO: prepend a one-sentence document summary to each\n"
            "    # fixed chunk; cache LLM calls to disk by doc hash\n"
            "    raise NotImplementedError\n"
            "\n"
            "STRATEGIES = [chunk_fixed, chunk_semantic, chunk_late, chunk_contextual]\n"
        ),
        "checks": [
            "All four chunkers return list[Chunk] on the same sample document and round-trip through one shared indexer.",
            "Reconstructing fixed chunks covers the full document with no gaps (overlap regions excepted).",
            "Contextual chunking writes its LLM summaries to the cache directory; a second run makes zero API calls.",
            "The final table reports recall@10, mean chunk length, and answer F1 for all four strategies on the same 100 queries.",
        ],
    },
    (3, 1): {
        "starter_code": (
            "import faiss\n"
            "import numpy as np\n"
            "\n"
            "def build_levels(doc, mother_tokens=1000, child_tokens=250):\n"
            "    mothers, children = [], []\n"
            "    words = doc['text'].split()\n"
            "    for mi in range(0, len(words), mother_tokens):\n"
            "        m_text = ' '.join(words[mi:mi + mother_tokens])\n"
            "        m_id = f\"{doc['id']}_m{mi}\"\n"
            "        mothers.append({'id': m_id, 'text': m_text})\n"
            "        m_words = m_text.split()\n"
            "        for ci in range(0, len(m_words), child_tokens):\n"
            "            children.append({'mother_id': m_id,\n"
            "                             'text': ' '.join(m_words[ci:ci + child_tokens])})\n"
            "    return mothers, children\n"
            "\n"
            "child_emb = embed([c['text'] for c in all_children])\n"
            "index = faiss.IndexFlatIP(child_emb.shape[1])\n"
            "index.add(child_emb.astype(np.float32))\n"
            "\n"
            "def retrieve_with_parents(query, k=8):\n"
            "    _, ids = index.search(embed([query]).astype(np.float32), k * 3)\n"
            "    mother_ids = []\n"
            "    for i in ids[0]:\n"
            "        mid = all_children[i]['mother_id']\n"
            "        if mid not in mother_ids:\n"
            "            mother_ids.append(mid)\n"
            "    return [mother_by_id[m] for m in mother_ids[:k]]\n"
        ),
        "checks": [
            "Every child carries a mother_id that resolves to exactly one mother chunk.",
            "retrieve_with_parents returns deduplicated mothers (no repeated ids) of roughly 1,000 tokens each.",
            "Recall@8 on the 100-query set beats the single-level child-only baseline.",
            "Token count handed to the LLM stays within the configured context budget on all queries.",
        ],
    },
    (4, 0): {
        "starter_code": (
            "import numpy as np\n"
            "import faiss\n"
            "import time\n"
            "from sentence_transformers import SentenceTransformer\n"
            "\n"
            "model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5',\n"
            "                            trust_remote_code=True)\n"
            "full = model.encode(corpus, normalize_embeddings=True)   # (n, 768)\n"
            "\n"
            "def truncate(emb, dim):\n"
            "    t = emb[:, :dim]\n"
            "    return t / np.linalg.norm(t, axis=1, keepdims=True)\n"
            "\n"
            "small = truncate(full, 64)\n"
            "idx_small = faiss.IndexFlatIP(64); idx_small.add(small.astype(np.float32))\n"
            "\n"
            "def prune_then_score(query_vec, shortlist=200, k=10):\n"
            "    q64 = truncate(query_vec[None, :], 64).astype(np.float32)\n"
            "    _, cand = idx_small.search(q64, shortlist)\n"
            "    cand = cand[0]\n"
            "    scores = full[cand] @ query_vec\n"
            "    order = np.argsort(-scores)[:k]\n"
            "    return cand[order], scores[order]\n"
            "\n"
            "# TODO: time prune_then_score vs full-dim flat search over 100 queries\n"
            "# and record recall@10 of the two-stage scheme against the full-dim result\n"
        ),
        "checks": [
            "Truncated 64-dim vectors are re-normalized (norms within 1e-5 of 1.0).",
            "Two-stage recall@10 against full-dim ground truth is at least 0.95 with shortlist=200.",
            "Two-stage query latency beats single-stage full-dim flat search on the 1M-vector index.",
            "Shrinking the shortlist to 50 visibly drops recall, confirming the recall/latency knob works.",
        ],
    },
    (4, 1): {
        "starter_code": (
            "import time\n"
            "\n"
            "COUNTS = {'sparse': 500, 'dense': 500, 'prune': 200,\n"
            "          'colbert': 50, 'cross': 10}\n"
            "\n"
            "def funnel(query):\n"
            "    t = {}\n"
            "    s = time.perf_counter()\n"
            "    cands = dedupe(bm25.search(query, COUNTS['sparse']) +\n"
            "                   dense.search(query, COUNTS['dense']))\n"
            "    t['stage1'] = time.perf_counter() - s\n"
            "\n"
            "    s = time.perf_counter()\n"
            "    cands = matryoshka_prune(query, cands, keep=COUNTS['prune'])\n"
            "    t['prune'] = time.perf_counter() - s\n"
            "\n"
            "    s = time.perf_counter()\n"
            "    cands = colbert_rerank(query, cands, keep=COUNTS['colbert'])\n"
            "    t['colbert'] = time.perf_counter() - s\n"
            "\n"
            "    s = time.perf_counter()\n"
            "    final = cross_encoder_rerank(query, cands, keep=COUNTS['cross'])\n"
            "    t['cross'] = time.perf_counter() - s\n"
            "    return final, t\n"
            "\n"
            "# TODO: run the 100-query eval set, log per-stage latency,\n"
            "# and compare recall@5 against dense.search(query, 10) alone\n"
        ),
        "checks": [
            "Candidate counts shrink monotonically through the funnel (about 900 to 200 to 50 to 10).",
            "Funnel recall@5 beats the dense-only baseline by at least 5 points on the eval set.",
            "Per-stage latency log shows the cross-encoder is not the dominant cost (it sees only 50 candidates).",
            "Dropping the ColBERT stage in an ablation changes recall, proving the stage is live.",
        ],
    },
    (5, 0): {
        "starter_code": (
            "import torch\n"
            "import torch.nn as nn\n"
            "import torchvision\n"
            "\n"
            "class PatchEmbed(nn.Module):\n"
            "    def __init__(self, img=32, patch=4, dim=192):\n"
            "        super().__init__()\n"
            "        self.proj = nn.Conv2d(3, dim, kernel_size=patch, stride=patch)\n"
            "        n = (img // patch) ** 2\n"
            "        self.cls = nn.Parameter(torch.zeros(1, 1, dim))\n"
            "        self.pos = nn.Parameter(torch.zeros(1, n + 1, dim))\n"
            "    def forward(self, x):\n"
            "        x = self.proj(x).flatten(2).transpose(1, 2)\n"
            "        cls = self.cls.expand(x.size(0), -1, -1)\n"
            "        return torch.cat([cls, x], dim=1) + self.pos\n"
            "\n"
            "class TinyViT(nn.Module):\n"
            "    def __init__(self, dim=192, depth=6, heads=3, classes=10):\n"
            "        super().__init__()\n"
            "        self.embed = PatchEmbed(dim=dim)\n"
            "        layer = nn.TransformerEncoderLayer(dim, heads, dim * 4,\n"
            "                                           batch_first=True)\n"
            "        self.encoder = nn.TransformerEncoder(layer, depth)\n"
            "        self.head = nn.Linear(dim, classes)\n"
            "    def forward(self, x):\n"
            "        z = self.encoder(self.embed(x))\n"
            "        return self.head(z[:, 0])\n"
            "\n"
            "resnet = torchvision.models.resnet18(num_classes=10)\n"
            "# TODO: train both 50 epochs on CIFAR-10 with identical optimizer,\n"
            "# then table accuracy, params, FLOPs, and inference latency\n"
        ),
        "checks": [
            "Both models overfit a single batch to near-100 percent accuracy (training loop sanity check).",
            "Parameter counts are reported from sum(p.numel()) and land near 2.7M (TinyViT) and 11.2M (ResNet-18).",
            "After 50 epochs both models clear 75 percent test accuracy on CIFAR-10.",
            "Latency is measured with torch.cuda.synchronize around batched inference, not wall-clock of the first call.",
        ],
    },
    (5, 1): {
        "starter_code": (
            "import open_clip\n"
            "import torch\n"
            "import faiss\n"
            "import numpy as np\n"
            "from PIL import Image\n"
            "\n"
            "model, _, preprocess = open_clip.create_model_and_transforms(\n"
            "    'ViT-B-32', pretrained='laion2b_s34b_b79k')\n"
            "tokenizer = open_clip.get_tokenizer('ViT-B-32')\n"
            "\n"
            "@torch.no_grad()\n"
            "def embed_images(paths, batch=64):\n"
            "    out = []\n"
            "    for i in range(0, len(paths), batch):\n"
            "        ims = torch.stack([preprocess(Image.open(p)) for p in paths[i:i + batch]])\n"
            "        v = model.encode_image(ims)\n"
            "        out.append((v / v.norm(dim=-1, keepdim=True)).cpu().numpy())\n"
            "    return np.vstack(out)\n"
            "\n"
            "@torch.no_grad()\n"
            "def embed_text(queries):\n"
            "    v = model.encode_text(tokenizer(queries))\n"
            "    return (v / v.norm(dim=-1, keepdim=True)).cpu().numpy()\n"
            "\n"
            "img_emb = embed_images(image_paths)          # 5000 images\n"
            "index = faiss.IndexFlatIP(img_emb.shape[1])\n"
            "index.add(img_emb.astype(np.float32))\n"
            "\n"
            "def search_text(query, k=10):\n"
            "    _, ids = index.search(embed_text([query]).astype(np.float32), k)\n"
            "    return [image_paths[i] for i in ids[0]]\n"
            "# TODO: add search_image(path, k) and run the 20-pair eval\n"
        ),
        "checks": [
            "Image and text embeddings share dimension 512 and are unit-normalized.",
            "search_text('a red sports car') returns car images in the top 5 on the sample corpus.",
            "search_image with a query image returns the image itself at rank 1 (self-retrieval sanity check).",
            "hit@5 on the 20 hand-curated pairs is at least 0.7 for text-to-image.",
        ],
    },
    (5, 2): {
        "starter_code": (
            "import torch\n"
            "from PIL import Image\n"
            "from lavis.models import load_model_and_preprocess\n"
            "\n"
            "device = 'cuda' if torch.cuda.is_available() else 'cpu'\n"
            "model, vis_processors, _ = load_model_and_preprocess(\n"
            "    name='blip2_t5', model_type='pretrain_flant5xl',\n"
            "    is_eval=True, device=device)\n"
            "\n"
            "def vqa(image_path, question):\n"
            "    raw = Image.open(image_path).convert('RGB')\n"
            "    image = vis_processors['eval'](raw).unsqueeze(0).to(device)\n"
            "    prompt = f'Question: {question} Short answer:'\n"
            "    return model.generate({'image': image, 'prompt': prompt},\n"
            "                          max_length=20)[0]\n"
            "\n"
            "results = []\n"
            "for row in load_questions('data/vqa_30.jsonl'):\n"
            "    pred = vqa(row['image'], row['question'])\n"
            "    results.append({'q': row['question'], 'pred': pred,\n"
            "                    'gold': row['answer']})\n"
            "    print(row['question'], '->', pred)\n"
            "# TODO: score correctness, run the same 30 through GPT-4V,\n"
            "# and write the failure analysis comparing the two\n"
        ),
        "checks": [
            "BLIP-2 loads in eval mode and answers the smoke-test image ('how many dogs?') sensibly.",
            "All 30 questions produce non-empty answers with no CUDA OOM (use fp16 if VRAM is tight).",
            "The score sheet marks each of the 30 answers correct/incorrect for both BLIP-2 and GPT-4V.",
            "The failure analysis cites at least 3 concrete examples where the two models diverge.",
        ],
    },
    (6, 0): {
        "starter_code": (
            "BASELINE = '''\n"
            "# CONTEXT: You classify internal support tickets for an IT helpdesk.\n"
            "# OBJECTIVE: Assign exactly one of 7 categories: {categories}.\n"
            "# STYLE: Output only the category name.\n"
            "# TONE: Neutral.\n"
            "# AUDIENCE: A routing system that parses your output.\n"
            "# RESPONSE: One line, no punctuation.\n"
            "Ticket: {ticket}\n"
            "Category:'''\n"
            "\n"
            "CRITIQUE = '''You are a prompt engineer. Here is a prompt and 10\n"
            "examples it misclassified. Diagnose the failure pattern and rewrite\n"
            "the prompt. Keep the CO-STAR structure and the output contract.\n"
            "PROMPT:\\n{prompt}\\nFAILURES:\\n{failures}\\nRewritten prompt:'''\n"
            "\n"
            "def accuracy(prompt, dataset):\n"
            "    hits = sum(llm(prompt.format(categories=CATS, ticket=t)) == y\n"
            "               for t, y in dataset)\n"
            "    return hits / len(dataset)\n"
            "\n"
            "prompt = BASELINE\n"
            "for round_num in range(3):\n"
            "    acc = accuracy(prompt, dev_set)\n"
            "    fails = sample_failures(prompt, dev_set, n=10)\n"
            "    print(f'round {round_num}: dev accuracy {acc:.3f}')\n"
            "    prompt = llm(CRITIQUE.format(prompt=prompt, failures=fails))\n"
            "# TODO: report final accuracy on the frozen test set, not dev\n"
        ),
        "checks": [
            "The baseline prompt yields a parseable single-line category for all dev examples.",
            "Dev accuracy is logged for every metaprompting round (3 rounds minimum).",
            "Final comparison uses the frozen test split, never the dev set the critique loop saw.",
            "The writeup names the concrete change metaprompting made (e.g. added boundary rules between two confusable classes).",
        ],
    },
    (6, 1): {
        "starter_code": (
            "import dspy\n"
            "\n"
            "lm = dspy.LM('openai/gpt-4o-mini', temperature=0.0)\n"
            "dspy.configure(lm=lm)\n"
            "\n"
            "class TicketClassify(dspy.Signature):\n"
            "    '''Classify an IT support ticket into one of 7 categories.'''\n"
            "    ticket: str = dspy.InputField()\n"
            "    category: str = dspy.OutputField(desc='one of: ' + ', '.join(CATS))\n"
            "\n"
            "classifier = dspy.ChainOfThought(TicketClassify)\n"
            "\n"
            "def metric(example, pred, trace=None):\n"
            "    return example.category == pred.category.strip()\n"
            "\n"
            "train = [dspy.Example(ticket=t, category=y).with_inputs('ticket')\n"
            "         for t, y in train_rows]\n"
            "\n"
            "copro = dspy.COPRO(metric=metric, breadth=8, depth=3)\n"
            "best_copro = copro.compile(classifier, trainset=train)\n"
            "\n"
            "mipro = dspy.MIPROv2(metric=metric, auto='medium')\n"
            "best_mipro = mipro.compile(classifier, trainset=train)\n"
            "# TODO: evaluate baseline, COPRO, and MIPRO on the frozen test set\n"
            "# and report accuracy plus total optimization cost in API calls\n"
        ),
        "checks": [
            "The unoptimized DSPy module scores within a few points of the week's hand-written baseline.",
            "COPRO and MIPRO runs complete and persist their compiled programs to disk.",
            "MIPRO beats the metaprompted baseline on the frozen test set (target: 5 or more points).",
            "The cost log shows total LLM calls per optimizer, demonstrating the COPRO vs MIPRO cost gap.",
        ],
    },
    (7, 0): {
        "starter_code": (
            "import numpy as np\n"
            "import umap\n"
            "from sklearn.mixture import GaussianMixture\n"
            "\n"
            "def cluster_layer(embeddings, max_clusters=12):\n"
            "    reduced = umap.UMAP(n_components=8, metric='cosine').fit_transform(embeddings)\n"
            "    n = best_k_by_bic(reduced, max_clusters)\n"
            "    labels = GaussianMixture(n_components=n).fit_predict(reduced)\n"
            "    return labels\n"
            "\n"
            "def summarize_cluster(texts, llm):\n"
            "    joined = '\\n'.join(texts)[:12000]\n"
            "    return llm(f'Summarize these passages in 150 words, keeping '\n"
            "               f'named entities exact:\\n{joined}')\n"
            "\n"
            "def build_raptor(chunks, embed, llm, levels=3):\n"
            "    tree = [list(chunks)]\n"
            "    for level in range(levels):\n"
            "        emb = embed([c['text'] for c in tree[-1]])\n"
            "        labels = cluster_layer(emb)\n"
            "        parents = []\n"
            "        for k in sorted(set(labels)):\n"
            "            members = [c for c, l in zip(tree[-1], labels) if l == k]\n"
            "            parents.append({'text': summarize_cluster(\n"
            "                [m['text'] for m in members], llm), 'level': level + 1})\n"
            "        tree.append(parents)\n"
            "        if len(parents) <= 2:\n"
            "            break\n"
            "    return [node for layer in tree for node in layer]  # collapsed tree\n"
        ),
        "checks": [
            "Each level has strictly fewer nodes than the level below it.",
            "Cluster summaries preserve named entities (spot-check 5 clusters against member chunks).",
            "The collapsed-tree index answers at least one multi-hop eval question that flat RAG misses.",
            "Ingestion cost (LLM calls and tokens) is logged and reported per level.",
        ],
    },
    (7, 1): {
        "starter_code": (
            "TRIPLET_PROMPT = '''Extract knowledge triplets from the passage.\n"
            "Rules: subjects and objects are named entities; predicates are\n"
            "short verb phrases; no pronouns. Output JSON list:\n"
            "[{\"s\": ..., \"p\": ..., \"o\": ...}]\n"
            "PASSAGE:\\n{passage}'''\n"
            "\n"
            "import json\n"
            "import networkx as nx\n"
            "\n"
            "def extract_triplets(chunks, llm):\n"
            "    triplets = []\n"
            "    for ch in chunks:\n"
            "        rows = json.loads(llm(TRIPLET_PROMPT.format(passage=ch['text'])))\n"
            "        for r in rows:\n"
            "            r['source'] = ch['doc_id']\n"
            "        triplets.extend(rows)\n"
            "    return triplets\n"
            "\n"
            "def build_graph(triplets):\n"
            "    g = nx.MultiDiGraph()\n"
            "    for t in triplets:\n"
            "        g.add_edge(normalize(t['s']), normalize(t['o']),\n"
            "                   predicate=t['p'], source=t['source'])\n"
            "    return g\n"
            "\n"
            "g = build_graph(extract_triplets(chunks, llm))\n"
            "communities = nx.community.louvain_communities(nx.Graph(g))\n"
            "# TODO: summarize each community with one LLM call, then build the\n"
            "# LightRAG pipeline on the same chunks and run the 50-question eval\n"
        ),
        "checks": [
            "Triplet extraction returns valid JSON on every chunk (log and retry malformed outputs).",
            "Entity normalization merges obvious duplicates ('IBM' and 'I.B.M.' share one node).",
            "Community detection yields more than 5 and fewer than 200 communities on the 5K-doc corpus.",
            "The eval table reports quality, total ingestion cost, and P50 query latency for GraphRAG and LightRAG side by side.",
        ],
    },
    (8, 0): {
        "starter_code": (
            "import time\n"
            "from dataclasses import dataclass\n"
            "\n"
            "@dataclass\n"
            "class GuardResult:\n"
            "    passed: bool\n"
            "    stage: str\n"
            "    reason: str\n"
            "    latency_ms: float\n"
            "\n"
            "class SyntaxGuard:\n"
            "    def check(self, text):\n"
            "        ok = 0 < len(text) <= 4000 and text.isprintable()\n"
            "        return ok, 'oversized or non-printable input'\n"
            "\n"
            "class PIIGuard:\n"
            "    def __init__(self):\n"
            "        from presidio_analyzer import AnalyzerEngine\n"
            "        self.engine = AnalyzerEngine()\n"
            "    def check(self, text):\n"
            "        hits = self.engine.analyze(text=text, language='en')\n"
            "        bad = [h for h in hits if h.score > 0.6]\n"
            "        return not bad, f'PII detected: {[h.entity_type for h in bad]}'\n"
            "\n"
            "PIPELINE = [('syntax', SyntaxGuard()), ('pii', PIIGuard())]\n"
            "# TODO: add ToxicityGuard (HF classifier) and IntentGuard, then chain:\n"
            "\n"
            "def run_pipeline(text):\n"
            "    for name, guard in PIPELINE:\n"
            "        t0 = time.perf_counter()\n"
            "        ok, reason = guard.check(text)\n"
            "        ms = (time.perf_counter() - t0) * 1000\n"
            "        if not ok:\n"
            "            return GuardResult(False, name, reason, ms)\n"
            "    return GuardResult(True, 'all', 'clean', ms)\n"
        ),
        "checks": [
            "Each of the four stages fires on its own crafted bad input and reports the right stage name.",
            "A clean input passes all stages and total pipeline latency is under 150 ms.",
            "On the 1,000-input labeled stream, false-positive rate is under 5 percent after threshold tuning.",
            "Early exit works: a syntax failure never invokes the PII or toxicity models (check call counters).",
        ],
    },
    (8, 1): {
        "starter_code": (
            "import torch\n"
            "from transformers import AutoTokenizer, AutoModelForSequenceClassification\n"
            "\n"
            "MODEL = 'microsoft/deberta-large-mnli'\n"
            "tok = AutoTokenizer.from_pretrained(MODEL)\n"
            "nli = AutoModelForSequenceClassification.from_pretrained(MODEL).eval()\n"
            "\n"
            "CLAIM_PROMPT = ('Split this answer into atomic factual claims, '\n"
            "                'one per line:\\n{answer}')\n"
            "\n"
            "@torch.no_grad()\n"
            "def entailment(premise, hypothesis):\n"
            "    inputs = tok(premise, hypothesis, truncation=True,\n"
            "                 max_length=512, return_tensors='pt')\n"
            "    probs = nli(**inputs).logits.softmax(-1)[0]\n"
            "    return probs[2].item()  # index 2 = entailment for this model\n"
            "\n"
            "def grounding_score(answer, context_chunks, llm, threshold=0.7):\n"
            "    claims = [c for c in llm(CLAIM_PROMPT.format(answer=answer)).splitlines() if c.strip()]\n"
            "    scores = []\n"
            "    for claim in claims:\n"
            "        best = max(entailment(chunk, claim) for chunk in context_chunks)\n"
            "        scores.append((claim, best))\n"
            "    verdict = all(s >= threshold for _, s in scores)\n"
            "    return verdict, scores\n"
            "# TODO: evaluate on the 100 (question, answer, evidence) triples\n"
            "# and report precision/recall of the rejection decision\n"
        ),
        "checks": [
            "entailment('The sky is blue.', 'The sky is blue.') scores above 0.9 (label-index sanity check).",
            "A fabricated claim against unrelated context scores below 0.3.",
            "Grounded answers in the 100-triple set pass and ungrounded ones fail at threshold 0.7 with at least 80 percent accuracy.",
            "Batching claim-context pairs keeps verification under 400 ms per answer on GPU.",
        ],
    },
    (9, 0): {
        "starter_code": (
            "import json\n"
            "import hashlib\n"
            "import os\n"
            "\n"
            "FACTOID_PROMPT = '''Extract exactly 5 atomic facts from this document.\n"
            "One sentence each, no pronouns, keep numbers and dates verbatim.\n"
            "Output a JSON list of strings.\\nDOCUMENT:\\n{doc}'''\n"
            "\n"
            "QA_PROMPT = '''Write 3 question-answer pairs a user might ask about\n"
            "this document. Output JSON: [{\"q\": ..., \"a\": ...}]\\nDOCUMENT:\\n{doc}'''\n"
            "\n"
            "HYDE_PROMPT = 'Write a short plausible answer to: {query}'\n"
            "\n"
            "def cached_llm(prompt, llm, cache_dir='cache'):\n"
            "    key = hashlib.sha1(prompt.encode()).hexdigest()\n"
            "    path = os.path.join(cache_dir, key + '.txt')\n"
            "    if os.path.exists(path):\n"
            "        return open(path).read()\n"
            "    out = llm(prompt)\n"
            "    os.makedirs(cache_dir, exist_ok=True)\n"
            "    open(path, 'w').write(out)\n"
            "    return out\n"
            "\n"
            "def enrich(doc, llm):\n"
            "    facts = json.loads(cached_llm(FACTOID_PROMPT.format(doc=doc['text'][:6000]), llm))\n"
            "    qas = json.loads(cached_llm(QA_PROMPT.format(doc=doc['text'][:6000]), llm))\n"
            "    rows = [{'text': f, 'type': 'factoid', 'source': doc['id']} for f in facts]\n"
            "    rows += [{'text': qa['q'], 'answer': qa['a'], 'type': 'qa', 'source': doc['id']} for qa in qas]\n"
            "    return rows\n"
            "# TODO: re-index chunks + artifacts, add HyDE at query time,\n"
            "# and measure recall@5 after each increment\n"
        ),
        "checks": [
            "Every document yields exactly 5 factoids and 3 QA pairs of valid JSON (retry loop handles malformed output).",
            "All artifacts carry a source id that resolves back to a real document.",
            "A second enrichment run makes zero LLM calls (cache hit confirmed by call counter).",
            "The recall@5 table shows four rows: baseline, +factoids, +QA pairs, +HyDE, measured on the same 100 queries.",
        ],
    },
    (9, 1): {
        "starter_code": (
            "import numpy as np\n"
            "import time\n"
            "\n"
            "class SemanticCache:\n"
            "    def __init__(self, embed_fn, threshold=0.92):\n"
            "        self.embed = embed_fn\n"
            "        self.threshold = threshold\n"
            "        self.keys = []     # embeddings\n"
            "        self.values = []   # answers\n"
            "        self.hits = 0\n"
            "        self.misses = 0\n"
            "\n"
            "    def lookup(self, query):\n"
            "        if not self.keys:\n"
            "            self.misses += 1\n"
            "            return None\n"
            "        qv = self.embed(query)\n"
            "        sims = np.array(self.keys) @ qv\n"
            "        best = int(np.argmax(sims))\n"
            "        if sims[best] >= self.threshold:\n"
            "            self.hits += 1\n"
            "            return self.values[best]\n"
            "        self.misses += 1\n"
            "        return None\n"
            "\n"
            "    def store(self, query, answer):\n"
            "        self.keys.append(self.embed(query))\n"
            "        self.values.append(answer)\n"
            "\n"
            "cache = SemanticCache(embed_fn=normalized_embed)\n"
            "for q in synthetic_stream(n=1000, duplicate_rate=0.3):\n"
            "    t0 = time.perf_counter()\n"
            "    answer = cache.lookup(q) or full_rag(q)\n"
            "    # TODO: store on miss, log latency and cost per query\n"
        ),
        "checks": [
            "An exact repeat of a cached query hits (similarity 1.0 passes any sane threshold).",
            "Hit rate on the 30 percent duplicate-intent stream lands between 20 and 35 percent at threshold 0.92.",
            "Manually inspect 10 hits: none serves a different intent (false-hit audit).",
            "Cache hits are at least 10 times faster than full RAG calls in the latency log.",
        ],
    },
    (10, 0): {
        "starter_code": (
            "class CachedRetriever:\n"
            "    '''Wraps the agent's retrieval tool with the week 9 cache.'''\n"
            "    def __init__(self, retriever, cache):\n"
            "        self.retriever = retriever\n"
            "        self.cache = cache\n"
            "        self.calls = {'cached': 0, 'fresh': 0}\n"
            "\n"
            "    def __call__(self, query: str) -> list[str]:\n"
            "        hit = self.cache.lookup(query)\n"
            "        if hit is not None:\n"
            "            self.calls['cached'] += 1\n"
            "            return hit\n"
            "        result = self.retriever(query)\n"
            "        self.cache.store(query, result)\n"
            "        self.calls['fresh'] += 1\n"
            "        return result\n"
            "\n"
            "retr = CachedRetriever(funnel_retrieve, SemanticCache(embed, 0.92))\n"
            "agent = build_agent(tools=[retr, entity_lookup, scratchpad])\n"
            "\n"
            "costs = []\n"
            "for q in test_questions(n=200, repeat_intent=0.25):\n"
            "    answer, trace = agent.run(q, max_steps=6)\n"
            "    costs.append(trace.total_tokens)\n"
            "# TODO: rerun with the cache disabled and compare cost,\n"
            "# latency, and answer quality on the same 200 questions\n"
        ),
        "checks": [
            "The agent's retrieval tool calls route through CachedRetriever (calls counter is nonzero for both kinds).",
            "Cache hit rate on agent sub-queries is reported; note it is lower than week 9 because agents reformulate queries.",
            "Total token cost with cache is measurably below the no-cache run on the same 200 questions.",
            "Answer quality (LLM-judge score) stays within 2 points of the no-cache run; the cache must not degrade answers.",
        ],
    },
    (10, 1): {
        "starter_code": (
            "from fastmcp import FastMCP\n"
            "import sqlite3\n"
            "\n"
            "mcp = FastMCP('sql-tools')\n"
            "DB = 'data/sample.db'\n"
            "\n"
            "@mcp.tool()\n"
            "def list_tables() -> list[str]:\n"
            "    '''List all tables in the database.'''\n"
            "    con = sqlite3.connect(DB)\n"
            "    rows = con.execute(\n"
            "        \"SELECT name FROM sqlite_master WHERE type='table'\").fetchall()\n"
            "    return [r[0] for r in rows]\n"
            "\n"
            "@mcp.tool()\n"
            "def get_schema(table: str) -> str:\n"
            "    '''Return the CREATE TABLE statement for a table.'''\n"
            "    con = sqlite3.connect(DB)\n"
            "    row = con.execute(\n"
            "        \"SELECT sql FROM sqlite_master WHERE name=?\", (table,)).fetchone()\n"
            "    return row[0] if row else 'no such table'\n"
            "\n"
            "@mcp.tool()\n"
            "def run_query(sql: str) -> list[tuple]:\n"
            "    '''Run a read-only SELECT, capped at 50 rows.'''\n"
            "    if not sql.strip().lower().startswith('select'):\n"
            "        raise ValueError('read-only: SELECT statements only')\n"
            "    con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)\n"
            "    return con.execute(sql).fetchmany(50)\n"
            "\n"
            "if __name__ == '__main__':\n"
            "    mcp.run()\n"
            "# TODO: point the ADK agent at this MCP server, then wrap the\n"
            "# agent with an A2A endpoint and test with three external callers\n"
        ),
        "checks": [
            "An MCP client lists exactly three tools with docstrings intact.",
            "run_query('DROP TABLE users') raises the read-only error; a SELECT returns at most 50 rows.",
            "The ADK agent answers 'how many orders shipped last month?' by chaining list_tables, get_schema, run_query (verify in the trace).",
            "The A2A endpoint serves the agent card and completes a task from an external client script.",
        ],
    },
    (11, 0): {
        "starter_code": (
            "from datasets import load_dataset\n"
            "from peft import LoraConfig, get_peft_model\n"
            "from transformers import AutoModelForCausalLM, AutoTokenizer\n"
            "from trl import SFTTrainer, SFTConfig\n"
            "\n"
            "BASE = 'Qwen/Qwen2.5-Coder-1.5B-Instruct'\n"
            "tok = AutoTokenizer.from_pretrained(BASE)\n"
            "model = AutoModelForCausalLM.from_pretrained(BASE, torch_dtype='bfloat16')\n"
            "\n"
            "peft_config = LoraConfig(\n"
            "    r=16, lora_alpha=32, lora_dropout=0.05,\n"
            "    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj'])\n"
            "\n"
            "def format_row(row):\n"
            "    return (f\"-- Schema:\\n{row['schema']}\\n\"\n"
            "            f\"-- Question: {row['question']}\\n\"\n"
            "            f\"SELECT\" + row['query'].split('SELECT', 1)[1])\n"
            "\n"
            "train = load_dataset('spider', split='train').map(\n"
            "    lambda r: {'text': format_row(r)})\n"
            "\n"
            "trainer = SFTTrainer(\n"
            "    model=get_peft_model(model, peft_config),\n"
            "    train_dataset=train,\n"
            "    args=SFTConfig(output_dir='out/sql-lora', num_train_epochs=3,\n"
            "                   per_device_train_batch_size=8, learning_rate=2e-4),\n"
            ")\n"
            "trainer.train()\n"
            "# TODO: build the 3-shot baseline and the execution-accuracy evaluator\n"
        ),
        "checks": [
            "Trainable parameter count printed by PEFT is under 1 percent of total parameters.",
            "Training loss decreases across the 3 epochs (inspect the trainer log).",
            "The evaluator executes generated SQL against the Spider SQLite files and compares result sets, not strings only.",
            "Fine-tuned execution accuracy beats the 3-shot baseline on the dev split.",
        ],
    },
    (11, 1): {
        "starter_code": (
            "import re\n"
            "import sqlite3\n"
            "from trl import GRPOConfig, GRPOTrainer\n"
            "\n"
            "def execute(db_path, sql):\n"
            "    try:\n"
            "        con = sqlite3.connect(f'file:{db_path}?mode=ro', uri=True)\n"
            "        return sorted(map(tuple, con.execute(sql).fetchmany(200)))\n"
            "    except Exception:\n"
            "        return None\n"
            "\n"
            "def reward_fn(completions, prompts, gold_sql, db_paths, **kw):\n"
            "    rewards = []\n"
            "    for comp, gold, db in zip(completions, gold_sql, db_paths):\n"
            "        m = re.search(r'SELECT.*', comp, re.S | re.I)\n"
            "        pred = execute(db, m.group(0)) if m else None\n"
            "        if pred is None:\n"
            "            rewards.append(0.0)\n"
            "        elif pred == execute(db, gold):\n"
            "            rewards.append(1.0)\n"
            "        else:\n"
            "            rewards.append(0.2)  # valid SQL, wrong result\n"
            "    return rewards\n"
            "\n"
            "config = GRPOConfig(output_dir='out/sql-grpo', num_generations=8,\n"
            "                    max_steps=200, beta=0.04)\n"
            "trainer = GRPOTrainer(model='out/sql-lora', reward_funcs=reward_fn,\n"
            "                      args=config, train_dataset=prompt_dataset)\n"
            "trainer.train()\n"
            "# TODO: evaluate SFT vs SFT+GRPO on the dev split\n"
        ),
        "checks": [
            "reward_fn on a hand-built batch returns 1.0 for a correct query, 0.2 for valid-but-wrong, 0.0 for invalid SQL.",
            "Mean reward per step trends upward over the 200 steps (plot from the trainer log).",
            "KL divergence stays bounded (beta penalty active), so completions remain valid SQL rather than reward hacks.",
            "SFT+GRPO execution accuracy on the dev split is at least equal to SFT alone, with the delta reported.",
        ],
    },
    (12, 0): {
        "starter_code": (
            "import time\n"
            "import torch\n"
            "from unsloth import FastLanguageModel\n"
            "from trl import SFTTrainer, SFTConfig\n"
            "\n"
            "model, tok = FastLanguageModel.from_pretrained(\n"
            "    'unsloth/mistral-7b-instruct-v0.3-bnb-4bit',\n"
            "    max_seq_length=2048, load_in_4bit=True)\n"
            "\n"
            "model = FastLanguageModel.get_peft_model(\n"
            "    model, r=16, lora_alpha=32,\n"
            "    target_modules=['q_proj', 'k_proj', 'v_proj', 'o_proj',\n"
            "                    'gate_proj', 'up_proj', 'down_proj'])\n"
            "\n"
            "t0 = time.time()\n"
            "trainer = SFTTrainer(\n"
            "    model=model, tokenizer=tok, train_dataset=train_ds,\n"
            "    args=SFTConfig(output_dir='out/unsloth', num_train_epochs=1,\n"
            "                   per_device_train_batch_size=4,\n"
            "                   gradient_accumulation_steps=4, learning_rate=2e-4))\n"
            "trainer.train()\n"
            "print('wallclock minutes:', (time.time() - t0) / 60)\n"
            "print('peak GPU GB:', torch.cuda.max_memory_allocated() / 1e9)\n"
            "# TODO: run the identical config through vanilla TRL (no Unsloth)\n"
            "# and compare wallclock, peak memory, and held-out eval loss\n"
        ),
        "checks": [
            "The Unsloth run finishes 1 epoch in under 30 minutes on a single GPU.",
            "Peak GPU memory is logged for both runs; the Unsloth run uses less.",
            "Held-out eval loss of the two runs matches within noise (the speedup must not cost quality).",
            "The saved LoRA adapter reloads and generates coherent completions on 3 spot-check prompts.",
        ],
    },
    (12, 1): {
        "starter_code": (
            "from datasets import Dataset\n"
            "from ragas import evaluate\n"
            "from ragas.metrics import (faithfulness, answer_relevancy,\n"
            "                           context_precision, context_recall)\n"
            "\n"
            "rows = []  # built from your RAG pipeline\n"
            "for q in eval_questions:               # 150 questions\n"
            "    ctx = [c.text for c in rag.retrieve(q['question'])]\n"
            "    ans = rag.answer(q['question'], ctx)\n"
            "    rows.append({'question': q['question'], 'answer': ans,\n"
            "                 'contexts': ctx, 'ground_truth': q['gold']})\n"
            "\n"
            "report = evaluate(Dataset.from_list(rows),\n"
            "                  metrics=[faithfulness, answer_relevancy,\n"
            "                           context_precision, context_recall])\n"
            "print(report)\n"
            "\n"
            "JUDGE_PROMPT = '''Score the answer 1-5 for factual correctness against\n"
            "the gold answer. Length must not affect the score. Output JSON:\n"
            "{\"score\": n, \"reason\": \"...\"}\n"
            "QUESTION: {q}\\nGOLD: {gold}\\nANSWER: {a}'''\n"
            "\n"
            "def rgb_noise_test(rows, noise_pool, rate=0.3):\n"
            "    # TODO: replace `rate` of each row's contexts with topically\n"
            "    # similar noise passages, re-answer, and measure the flip rate\n"
            "    raise NotImplementedError\n"
            "# TODO: report all metrics with bootstrap confidence intervals\n"
        ),
        "checks": [
            "Ragas returns all four metrics with no NaN rows (malformed contexts are the usual cause).",
            "The judge model is from a different family than the RAG's generator, and each pair is scored twice with order swapped.",
            "The noise test shows a nonzero answer flip rate, and the counterfactual test is reported separately.",
            "Every reported metric carries a 95 percent bootstrap confidence interval over the 150 questions.",
        ],
    },
}
