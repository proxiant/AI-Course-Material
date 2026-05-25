"""Chapter 2: Mathematical Foundations."""

CHAPTER = {
    "label": "Chapter 2",
    "title": "Mathematical Foundations",
    "sections": [
        {
            "number": "2.1",
            "title": "Why Mathematics Matters",
            "paragraphs": [
                "Modern deep learning is, at its core, applied calculus and linear algebra "
                "over large datasets. A working command of the math is the difference between "
                "treating neural networks as a black box and being able to reason about why a "
                "training run diverges, why one architecture works better than another for a "
                "given task, or how to design a new objective function. This chapter is a brisk "
                "refresher of the material you need. If you are already comfortable, skim. If "
                "you are not, study it carefully. We will lean on these ideas throughout the "
                "book.",
            ],
        },
        {
            "number": "2.2",
            "title": "Linear Algebra",
            "paragraphs": [
                "Linear algebra is the language of high-dimensional data. Vectors represent "
                "data points, weights, embeddings. Matrices represent transformations, "
                "datasets, attention patterns. Tensors generalize to higher dimensions.",
            ],
            "subsections": [
                {
                    "title": "2.2.1 Vectors and Matrices",
                    "paragraphs": [
                        "A vector is an ordered list of numbers. We write x ∈ ℝⁿ to mean x is a "
                        "vector with n real-valued entries. A matrix A ∈ ℝᵐˣⁿ has m rows and n "
                        "columns. Matrix multiplication: (AB)ᵢⱼ = Σₖ Aᵢₖ Bₖⱼ. Defined only when "
                        "the inner dimensions match.",
                        "The transpose Aᵀ swaps rows and columns. The identity matrix I has "
                        "ones on the diagonal and zeros elsewhere. The inverse A⁻¹ satisfies "
                        "A A⁻¹ = I (defined only for square non-singular A). The determinant "
                        "det(A) measures how A scales volume; det(A) = 0 means A is singular.",
                    ],
                },
                {
                    "title": "2.2.2 Norms and Distances",
                    "paragraphs": [
                        "The L² (Euclidean) norm of a vector: ||x||₂ = sqrt(Σᵢ xᵢ²). The L¹ "
                        "norm: ||x||₁ = Σᵢ |xᵢ|. The L∞ norm: ||x||∞ = maxᵢ |xᵢ|. Norms induce "
                        "distances: d(x, y) = ||x - y||.",
                        "Cosine similarity measures the angle between two vectors: "
                        "cos(x, y) = (x · y) / (||x||₂ ||y||₂). This is the foundational "
                        "similarity measure for embeddings: two embeddings are similar in "
                        "meaning if their cosine similarity is close to 1.",
                    ],
                },
                {
                    "title": "2.2.3 Eigenvalues, Eigenvectors, and Decompositions",
                    "paragraphs": [
                        "For a square matrix A, an eigenvector v satisfies Av = λv for some "
                        "scalar λ (the eigenvalue). Eigenvalues reveal stretching and rotation "
                        "behavior of the matrix.",
                        "The singular value decomposition (SVD) writes any matrix A as "
                        "A = UΣVᵀ, where U and V are orthogonal and Σ is diagonal with "
                        "non-negative entries (singular values). SVD underlies principal "
                        "component analysis, low-rank approximation (used in LoRA), and "
                        "embedding methods. The rank of A is the number of non-zero singular "
                        "values.",
                        "Low-rank approximation: by keeping only the top k singular values, you "
                        "approximate A with much fewer parameters. This is the mathematical "
                        "foundation of LoRA (low-rank adaptation): the weight update during "
                        "fine-tuning is approximately low-rank, so we can represent it as the "
                        "product of two small matrices.",
                    ],
                },
            ],
        },
        {
            "number": "2.3",
            "title": "Calculus and Optimization",
            "paragraphs": [
                "Training neural networks is optimization: find parameters that minimize a "
                "loss function. The basic tool is the derivative.",
            ],
            "subsections": [
                {
                    "title": "2.3.1 Derivatives and Gradients",
                    "paragraphs": [
                        "For a function f: ℝ → ℝ, the derivative f'(x) is the rate of change at "
                        "x. For a function f: ℝⁿ → ℝ, the gradient ∇f(x) is the vector of "
                        "partial derivatives: ∇f = (∂f/∂x₁, ..., ∂f/∂xₙ). The gradient points in "
                        "the direction of steepest increase.",
                        "Gradient descent updates parameters by moving in the opposite direction "
                        "of the gradient: θ ← θ - η ∇L(θ). The learning rate η controls the "
                        "step size.",
                    ],
                },
                {
                    "title": "2.3.2 The Chain Rule",
                    "paragraphs": [
                        "If y = f(u) and u = g(x), then dy/dx = (dy/du) · (du/dx). The chain "
                        "rule extends to vector-valued functions and to compositions of many "
                        "functions. Backpropagation is the application of the chain rule to a "
                        "computational graph (the neural network), computing gradients of the "
                        "loss with respect to every parameter by composing local derivatives "
                        "from output back to input.",
                    ],
                },
                {
                    "title": "2.3.3 Convex and Non-Convex Optimization",
                    "paragraphs": [
                        "A function is convex if its graph lies below any chord between two "
                        "points. Convex optimization problems have a single global minimum and "
                        "are well-understood. Most classical machine learning (linear regression "
                        "with L2 loss, logistic regression, SVMs) is convex.",
                        "Neural network optimization is non-convex: the loss surface has many "
                        "local minima, saddle points, and flat regions. In high dimensions, the "
                        "empirical observation is that most local minima have similar loss "
                        "values, and saddle points (not local minima) are the main obstacle. "
                        "Modern optimizers like Adam, AdamW, and momentum-based SGD handle these "
                        "landscapes well in practice, even though we lack the strong theoretical "
                        "guarantees of convex optimization.",
                    ],
                },
            ],
        },
        {
            "number": "2.4",
            "title": "Probability and Statistics",
            "paragraphs": [
                "Machine learning is fundamentally probabilistic: models predict distributions, "
                "training data is sampled from distributions, and loss functions correspond to "
                "likelihoods.",
            ],
            "subsections": [
                {
                    "title": "2.4.1 Random Variables and Distributions",
                    "paragraphs": [
                        "A random variable X takes values from a probability distribution. "
                        "Discrete distributions are described by a probability mass function "
                        "P(X = x); continuous distributions by a probability density function "
                        "p(x). Common distributions include Gaussian (normal), Bernoulli, "
                        "Categorical, Uniform, and Exponential.",
                        "Expectation: E[X] = Σ x P(X = x) for discrete X, or ∫ x p(x) dx for "
                        "continuous X. Variance: Var(X) = E[(X - E[X])²]. These two moments "
                        "characterize many practical distributions.",
                    ],
                },
                {
                    "title": "2.4.2 Joint, Marginal, and Conditional",
                    "paragraphs": [
                        "Two random variables X, Y have a joint distribution P(X, Y). The "
                        "marginal P(X) is obtained by summing or integrating out Y. The "
                        "conditional P(Y | X) tells you how Y is distributed given a particular "
                        "value of X. Bayes' rule connects them: P(Y | X) = P(X | Y) P(Y) / "
                        "P(X).",
                        "These concepts underpin all of generative modeling. A discriminative "
                        "model learns P(Y | X). A generative model learns P(X, Y) or P(X), and "
                        "can sample new examples.",
                    ],
                },
                {
                    "title": "2.4.3 Maximum Likelihood Estimation",
                    "paragraphs": [
                        "Given a parameterized distribution P(x; θ) and observed data "
                        "{x₁, ..., xₙ}, the maximum likelihood estimate (MLE) is the choice of "
                        "θ that maximizes the likelihood: θ̂ = argmax Πᵢ P(xᵢ; θ). Taking "
                        "logarithms (which preserves the argmax): θ̂ = argmax Σᵢ log P(xᵢ; θ).",
                        "Neural network training is almost always MLE in disguise. Cross-"
                        "entropy loss is the negative log-likelihood of a categorical model. "
                        "MSE loss is the negative log-likelihood of a Gaussian model. "
                        "Maximizing likelihood = minimizing negative log-likelihood = training "
                        "the model with the appropriate loss.",
                    ],
                },
                {
                    "title": "2.4.4 KL Divergence and Cross-Entropy",
                    "paragraphs": [
                        "The Kullback-Leibler divergence between two distributions P and Q is "
                        "D_KL(P || Q) = Σ P(x) log(P(x) / Q(x)). It measures how much Q "
                        "differs from P. It is non-negative, zero iff P = Q, and asymmetric "
                        "(D_KL(P||Q) ≠ D_KL(Q||P)).",
                        "Cross-entropy H(P, Q) = -Σ P(x) log Q(x). It decomposes as "
                        "H(P, Q) = H(P) + D_KL(P || Q). In classification with one-hot true "
                        "labels P, H(P) = 0, so cross-entropy reduces to -log Q(y_true). This "
                        "is the standard classification loss.",
                    ],
                },
            ],
        },
        {
            "number": "2.5",
            "title": "Information Theory",
            "paragraphs": [
                "Entropy H(X) = -Σ P(x) log P(x) measures uncertainty in a distribution. A "
                "uniform distribution has maximum entropy (log of the number of outcomes). A "
                "concentrated distribution has low entropy.",

                "In language modeling, perplexity = exp(cross-entropy per token) measures how "
                "uncertain the model is at each step. Perplexity of 10 means the model is, on "
                "average, as uncertain as if choosing uniformly from 10 options. Lower is "
                "better; modern LLMs achieve perplexity in the single digits on standard "
                "English benchmarks.",

                "Mutual information I(X; Y) = H(X) + H(Y) - H(X, Y) measures shared "
                "information. It appears in representation learning objectives such as InfoNCE.",
            ],
        },
        {
            "number": "2.6",
            "title": "High-Dimensional Geometry",
            "paragraphs": [
                "Human intuition for two- and three-dimensional space misleads in higher "
                "dimensions. Three counter-intuitive facts that matter for embeddings:",

                "Concentration of measure. In a high-dimensional unit ball, almost all volume "
                "lies near the surface. Equivalently, almost all of a Gaussian's probability "
                "mass lies in a thin shell at a specific distance from the mean.",

                "Random vectors are nearly orthogonal. In d dimensions, two independently "
                "sampled random unit vectors have expected cosine similarity that tends to 0 "
                "as d grows.",

                "Distance concentration. The ratio of maximum to minimum pairwise distances "
                "among a finite set of points approaches 1 as dimension grows. 'Nearest "
                "neighbor' loses meaning.",

                "These facts have practical consequences. Embedding quality requires explicit "
                "training (contrastive learning) to keep distances meaningful. Anisotropy in "
                "pretrained BERT embeddings, where all embeddings cluster in a narrow cone, is "
                "a symptom of these effects. Approximate nearest neighbor search trades a "
                "small recall loss for orders of magnitude speedup because exact search in "
                "high dimensions is fundamentally hard.",
            ],
        },
        {
            "number": "2.7",
            "title": "Summary",
            "bullets": [
                "Linear algebra provides the data structures (vectors, matrices, tensors) and "
                "transformations (matrix products, SVD) used throughout deep learning.",
                "Calculus and the chain rule are the foundation of backpropagation; "
                "gradient-based optimization is how every modern deep model is trained.",
                "Probability and statistics frame learning as maximum likelihood; cross-entropy "
                "and KL divergence are the standard loss functions.",
                "Information theory connects probability to model quality via entropy and "
                "perplexity.",
                "High-dimensional geometry has counter-intuitive properties that shape "
                "embedding methods and similarity search.",
            ],
        },
    ],
    "further_reading": [
        "Strang, Introduction to Linear Algebra (5th ed.). Accessible LA reference.",
        "Boyd and Vandenberghe, Convex Optimization (2004). Free PDF; the standard reference.",
        "MacKay, Information Theory, Inference, and Learning Algorithms (2003). Free PDF; "
        "elegant integration of information theory and ML.",
    ],
}
