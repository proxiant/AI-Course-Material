"""Chapter 1: Introduction to AI and Modern Machine Learning."""

CHAPTER = {
    "label": "Chapter 1",
    "title": "Introduction to AI and Modern Machine Learning",
    "intro_image": "21_ai_taxonomy.png",
    "intro_caption": "Figure 1.1: Hierarchy of AI subfields.",
    "sections": [
        {
            "number": "1.1",
            "title": "What This Book Is About",
            "paragraphs": [
                "The field of artificial intelligence has moved through several distinct eras. The "
                "first wave was symbolic: rules, knowledge bases, expert systems. The second was "
                "statistical: classical machine learning with feature engineering, support vector "
                "machines, decision trees, and ensembles. We now live in the third wave, defined "
                "by deep learning on massive datasets, transformer-based foundation models, and "
                "generative systems that produce coherent text, images, audio, and video. This book "
                "is about that third wave and the engineering practice it has created.",

                "The audience is engineers, researchers, and technical leaders who want a working "
                "command of modern AI: how the models are built, how they are trained, how they are "
                "deployed, and how they are evaluated. The level of detail is set to support both "
                "first-time understanding and reference use. Each chapter introduces a topic from "
                "first principles, develops the mathematics where it matters, illustrates with "
                "diagrams, and grounds the discussion in production practice.",

                "The book is opinionated about engineering. Many AI texts emphasize theoretical "
                "results that turn out to have little bearing on production work. Others focus on "
                "framework tutorials that quickly date. This text steers between both. The "
                "principles change slowly: gradient descent, attention, retrieval-augmented "
                "generation, and the bias-variance tradeoff will outlive any specific framework. "
                "We emphasize those principles and use specific tools (PyTorch, Hugging Face, FAISS, "
                "vLLM) as illustrations.",
            ],
        },
        {
            "number": "1.2",
            "title": "Artificial Intelligence, Machine Learning, and Deep Learning",
            "paragraphs": [
                "These terms are often used interchangeably in casual conversation, but they have "
                "distinct meanings.",

                "Artificial intelligence is the broad effort to build systems that exhibit "
                "behaviors we would call intelligent in humans: reasoning, learning, planning, "
                "language understanding, perception. The field includes search algorithms, "
                "logical inference, constraint satisfaction, and game-playing systems as well as "
                "the statistical methods we discuss in this book.",

                "Machine learning is a subfield of AI focused on systems that improve their "
                "behavior from data, rather than being explicitly programmed. A spam filter that "
                "learns from labeled examples, a recommendation system that learns from user "
                "interactions, and a stock-prediction model that learns from historical prices "
                "are all machine learning systems.",

                "Deep learning is a subfield of machine learning that uses neural networks with "
                "many layers. The 'deep' refers to the depth of the network. Deep learning has "
                "driven nearly every breakthrough in AI over the last decade: image recognition, "
                "speech recognition, machine translation, and the large language models that have "
                "captured public attention.",

                "Generative AI is a class of applications, not a separate field. It uses deep "
                "learning models (transformers, diffusion models) trained on massive datasets to "
                "produce novel outputs: text, images, audio, code. The same underlying models also "
                "support understanding tasks such as classification and retrieval.",
            ],
            "callouts": [
                ("Definition",
                 "A model is a function f(x; θ) parameterized by θ that maps inputs x to outputs "
                 "y. Training is the process of adjusting θ to make the model's predictions match "
                 "observed data."),
            ],
        },
        {
            "number": "1.3",
            "title": "Three Learning Paradigms",
            "image": "22_learning_paradigms.png",
            "caption": "Figure 1.2: Supervised, unsupervised, and reinforcement learning.",
            "paragraphs": [
                "Machine learning problems fall into three broad paradigms based on what kind of "
                "feedback the learner receives.",
            ],
            "subsections": [
                {
                    "title": "1.3.1 Supervised Learning",
                    "paragraphs": [
                        "In supervised learning, training data consists of paired examples "
                        "(x, y), where x is an input and y is a target. The model learns a "
                        "function that maps inputs to targets. Common subtypes:",
                        "Classification: y is a discrete label (spam vs not spam, image class). "
                        "Regression: y is a continuous number (house price, temperature). "
                        "Structured prediction: y is itself structured (a sequence, a tree, a "
                        "graph), as in machine translation or named entity recognition.",
                        "Supervised learning is the most mature and widely deployed paradigm. "
                        "It powers most production ML systems. Its main practical constraint is "
                        "labeled data: humans must annotate examples for the model to learn "
                        "from, which is expensive at scale.",
                    ],
                },
                {
                    "title": "1.3.2 Unsupervised Learning",
                    "paragraphs": [
                        "In unsupervised learning, the data consists only of inputs x with no "
                        "targets. The goal is to discover structure: clusters, low-dimensional "
                        "embeddings, generative models of the data distribution.",
                        "Examples include k-means clustering for customer segmentation, principal "
                        "component analysis for dimensionality reduction, topic models for "
                        "document collections, autoencoders for learned representations, and "
                        "generative models such as GANs and diffusion models.",
                        "A particularly important variant is self-supervised learning, in which "
                        "labels are derived from the data itself. Predicting masked tokens in a "
                        "sentence (BERT), predicting the next token (GPT), or predicting an "
                        "image patch from surrounding patches (masked autoencoders) all create "
                        "supervised signals without human annotation. Self-supervised learning is "
                        "the foundation of modern foundation models.",
                    ],
                },
                {
                    "title": "1.3.3 Reinforcement Learning",
                    "paragraphs": [
                        "In reinforcement learning (RL), an agent interacts with an environment "
                        "over time. The agent observes a state, takes an action, and receives a "
                        "reward plus a new state. The agent's goal is to learn a policy (a "
                        "function from states to actions) that maximizes cumulative reward.",
                        "RL has produced spectacular results in games (AlphaGo, AlphaStar), "
                        "robotics, and resource allocation. In language modeling, RL appears in "
                        "the form of Reinforcement Learning from Human Feedback (RLHF) and its "
                        "successors (DPO, GRPO), used to align large language models with human "
                        "preferences.",
                        "RL is harder to scale than supervised learning because rewards are "
                        "often sparse, environments are expensive to simulate, and exploration is "
                        "tricky. But it is uniquely powerful for problems where the right answer "
                        "is not known in advance and must be discovered through interaction.",
                    ],
                },
            ],
        },
        {
            "number": "1.4",
            "title": "The Bias-Variance Tradeoff",
            "image": "23_bias_variance.png",
            "caption": "Figure 1.3: As model complexity grows, bias falls but variance rises.",
            "paragraphs": [
                "Almost every practical decision in machine learning involves a tradeoff between "
                "underfitting (model too simple to capture the truth) and overfitting (model so "
                "complex it memorizes noise). The bias-variance decomposition makes this "
                "tradeoff precise.",

                "For a regression model trained on a finite dataset, the expected squared error "
                "on a test point decomposes into three terms: bias squared (how far the model's "
                "average prediction is from the true value), variance (how much the prediction "
                "varies across training sets), and irreducible noise (inherent randomness in "
                "the data).",
            ],
            "equation": "E[(y - ĥ(x))²] = Bias²[ĥ(x)] + Variance[ĥ(x)] + σ²",
            "equation_label": "1.1",
            "subsections": [
                {
                    "title": "1.4.1 Implications for Model Selection",
                    "paragraphs": [
                        "Simple models (linear regression, shallow trees) tend to have high bias "
                        "and low variance. They make the same kinds of errors on every training "
                        "set but cannot capture complex patterns. Complex models (deep neural "
                        "networks, deep trees) have low bias but high variance. They can fit "
                        "almost any training set but their predictions on new data are sensitive "
                        "to which training set they happened to see.",
                        "The right model complexity depends on data size. With little data, "
                        "simple models often win because their lower variance outweighs their "
                        "higher bias. With abundant data, complex models win because their "
                        "variance shrinks as data grows. This is why deep learning surged once "
                        "datasets reached the millions-of-examples scale.",
                        "Regularization techniques such as L2 penalty, dropout, early stopping, "
                        "and data augmentation reduce variance without giving up too much "
                        "expressiveness. We will use these throughout the book.",
                    ],
                },
            ],
        },
        {
            "number": "1.5",
            "title": "A Brief History of Modern AI",
            "paragraphs": [
                "The modern era of deep learning began around 2012, when Krizhevsky, Sutskever, "
                "and Hinton's AlexNet won the ImageNet image-classification challenge by a wide "
                "margin using a convolutional neural network trained on GPUs. The result "
                "convinced the field that deep neural networks, given enough data and compute, "
                "could outperform decades of hand-crafted feature engineering.",

                "The next several years saw rapid progress in computer vision (ResNet, "
                "Inception), in sequence modeling (LSTM-based encoder-decoder models for "
                "translation), and in generative models (GANs by Goodfellow et al., 2014; "
                "VAEs by Kingma and Welling, 2013).",

                "In 2017, the paper 'Attention Is All You Need' by Vaswani et al. introduced the "
                "transformer architecture, replacing recurrence with self-attention. This proved "
                "to be the foundational architecture for the LLM era. BERT (2018) showed that "
                "pretraining a bidirectional transformer on large text corpora produced "
                "representations that transferred to many downstream tasks. GPT (2018, 2019, "
                "2020) showed that scaling up a decoder-only transformer trained on next-token "
                "prediction produced general-purpose language generators.",

                "GPT-3 (2020) showed in-context learning at scale, the ability to learn new "
                "tasks from a few examples in the prompt. ChatGPT (2022) brought instruction-"
                "tuned LLMs to public attention and triggered the current wave of generative AI "
                "adoption. GPT-4 (2023), Claude, Gemini, LLaMA, and Mistral followed, each "
                "pushing the frontier of capability while open-source alternatives became "
                "competitive with closed models for many tasks.",

                "In parallel, image generation went through its own revolution. DALL-E and "
                "Stable Diffusion brought text-to-image generation to consumers. Diffusion "
                "models displaced GANs as the dominant generative architecture for images. "
                "Multimodal models such as CLIP, Flamingo, GPT-4V, and Gemini integrated vision "
                "and language. The convergence of all modalities into single foundation models "
                "is the current frontier.",
            ],
        },
        {
            "number": "1.6",
            "title": "How to Read This Book",
            "paragraphs": [
                "The book is organized into six parts. Part I covers foundations: the "
                "mathematics, neural networks, and training procedures that underpin everything "
                "that follows. Part II covers natural language processing from classical "
                "techniques through the transformer revolution. Part III covers computer vision "
                "and multimodal models. Part IV covers large language models in depth: prompt "
                "engineering, fine-tuning, alignment. Part V covers retrieval and knowledge "
                "systems including vector databases and RAG. Part VI covers production "
                "engineering, evaluation, and ethics.",

                "Chapters are self-contained enough to read out of order if a topic interests "
                "you, but they cross-reference freely. The prerequisites are honest: you should "
                "know calculus, linear algebra, and probability at an undergraduate level, plus "
                "have working Python skills. Chapter 2 provides a brisk refresher of the math; "
                "skim if you are comfortable, study carefully if you are not.",

                "Each chapter ends with a summary, suggested exercises, and pointers to deeper "
                "reading. The bibliography is selective rather than exhaustive: we point to the "
                "papers and books that we believe most repay study, not all the literature on a "
                "topic.",
            ],
        },
        {
            "number": "1.7",
            "title": "Summary",
            "bullets": [
                "Artificial intelligence is the broad effort to build intelligent systems; "
                "machine learning is the subfield that learns from data; deep learning is the "
                "machine learning subfield based on deep neural networks; generative AI is the "
                "application class focused on producing novel outputs.",
                "Three learning paradigms: supervised (labeled data), unsupervised (no labels), "
                "and reinforcement (interaction with reward).",
                "The bias-variance tradeoff governs model selection. Simple models underfit; "
                "complex models overfit. The right complexity depends on data size.",
                "Modern AI runs on transformer-based foundation models pretrained on massive "
                "corpora, adapted to downstream tasks via prompting, fine-tuning, or retrieval-"
                "augmented generation.",
                "The book takes a principles-first approach grounded in engineering practice.",
            ],
        },
    ],
    "further_reading": [
        "Russell and Norvig, Artificial Intelligence: A Modern Approach (4th ed., 2020). "
        "Comprehensive AI textbook covering symbolic and statistical methods.",
        "Goodfellow, Bengio, Courville, Deep Learning (2016). Authoritative deep learning text.",
        "Bishop, Pattern Recognition and Machine Learning (2006). Classical ML grounded in "
        "Bayesian probability.",
        "Murphy, Probabilistic Machine Learning (2022, 2023). Modern two-volume treatment of "
        "ML from a probabilistic perspective.",
    ],
}
