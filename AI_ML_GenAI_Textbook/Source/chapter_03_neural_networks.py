"""Chapter 3: Neural Networks and Deep Learning."""

CHAPTER = {
    "label": "Chapter 3",
    "title": "Neural Networks and Deep Learning",
    "intro_image": "01_ann_architecture.png",
    "intro_caption": "Figure 3.1: A feedforward neural network with input, hidden, and output layers.",
    "sections": [
        {
            "number": "3.1",
            "title": "The Artificial Neuron",
            "image": "02_neuron.png",
            "caption": "Figure 3.2: A single artificial neuron computes a weighted sum plus bias, then applies an activation function.",
            "paragraphs": [
                "The basic unit of a neural network is an artificial neuron. Despite its "
                "biological inspiration, the artificial neuron is mathematically simple: take a "
                "weighted sum of inputs, add a bias, apply a non-linear function.",

                "Given input vector x ∈ ℝⁿ, weights w ∈ ℝⁿ, and bias b ∈ ℝ, a neuron computes "
                "the pre-activation z = wᵀx + b, then applies an activation function f to "
                "produce the output a = f(z). With a layer of m neurons, the weights become a "
                "matrix W ∈ ℝᵐˣⁿ, and the layer computes a = f(Wx + b) where f is applied "
                "element-wise.",

                "What makes a neuron useful is the non-linear activation function. Without it, "
                "stacking layers would only compose linear transformations into another linear "
                "transformation, with no gain in expressive power. Non-linearity is what lets "
                "deep networks model complex relationships.",
            ],
        },
        {
            "number": "3.2",
            "title": "Activation Functions",
            "image": "03_activations.png",
            "caption": "Figure 3.3: Common activation functions: sigmoid, tanh, ReLU, leaky ReLU.",
            "paragraphs": [
                "The choice of activation function shapes both expressiveness and trainability.",
            ],
            "subsections": [
                {
                    "title": "3.2.1 Saturating Activations: Sigmoid and Tanh",
                    "paragraphs": [
                        "The sigmoid function σ(x) = 1 / (1 + e⁻ˣ) maps any real value to "
                        "(0, 1). Historically popular because the output can be interpreted as "
                        "a probability. It has two problems: it saturates (gradient vanishes "
                        "when |x| is large), and the output is not zero-centered.",
                        "The hyperbolic tangent tanh(x) maps to (-1, 1) and is zero-centered, "
                        "slightly mitigating the saturation issue. Both sigmoid and tanh are "
                        "still used in specific places (sigmoid for binary classification "
                        "output, LSTM gates) but rarely in modern hidden layers.",
                    ],
                },
                {
                    "title": "3.2.2 ReLU and Variants",
                    "paragraphs": [
                        "The Rectified Linear Unit ReLU(x) = max(0, x) is the dominant choice "
                        "for hidden layers in modern deep networks. It is cheap to compute, "
                        "does not saturate on the positive side, and produces sparse "
                        "activations (many neurons output exactly zero).",
                        "ReLU has a 'dead neuron' problem: once a neuron's weighted input is "
                        "consistently negative, it always outputs zero and its gradient is "
                        "zero, so it stops learning. Leaky ReLU (slope α for negative inputs, "
                        "typically 0.01) and Parametric ReLU (learn α) address this.",
                        "More recent variants include GELU (Gaussian Error Linear Unit), used "
                        "in BERT and most modern transformers, and SiLU (Sigmoid Linear Unit, "
                        "also called Swish), used in LLaMA. Both are smoother than ReLU and "
                        "tend to produce slightly better results at similar compute.",
                    ],
                },
                {
                    "title": "3.2.3 Output Activations",
                    "image": "25_logistic_softmax.png",
                    "caption": "Figure 3.4: Logistic for binary outputs (left), softmax for multiclass (right).",
                    "paragraphs": [
                        "For binary classification, the output layer uses a single neuron with "
                        "sigmoid activation, producing a probability in (0, 1). For multiclass "
                        "classification with K classes, the output is a vector of K logits that "
                        "passes through softmax: softmax(z)ᵢ = exp(zᵢ) / Σⱼ exp(zⱼ). The "
                        "result is a probability distribution over classes.",
                        "For regression, the output is typically linear (no activation), unless "
                        "the target is bounded (use sigmoid for [0, 1] outputs, tanh for "
                        "[-1, 1]).",
                    ],
                },
            ],
        },
        {
            "number": "3.3",
            "title": "Feedforward Networks",
            "paragraphs": [
                "A feedforward network is a stack of fully connected layers. Each layer takes "
                "the output of the previous layer, applies a learned linear transformation, and "
                "passes the result through a non-linear activation. The final layer produces "
                "the output.",

                "Architectural choices: number of layers (depth), number of neurons per layer "
                "(width), activation function. Depth provides hierarchical composition: lower "
                "layers learn simple features, higher layers compose them into complex ones. "
                "Width provides capacity within a layer.",

                "The universal approximation theorem states that a sufficiently wide single-"
                "hidden-layer network can approximate any continuous function on a compact set. "
                "But it says nothing about how easy that approximation is to learn. In practice, "
                "depth is far more parameter-efficient than width: a deep network with modest "
                "width can express functions that would require exponentially many wide-shallow "
                "neurons.",
            ],
        },
        {
            "number": "3.4",
            "title": "Training: Backpropagation and Gradient Descent",
            "image": "04_backprop.png",
            "caption": "Figure 3.5: Forward pass computes the prediction; backward pass propagates gradients.",
            "paragraphs": [
                "Training a neural network is solving an optimization problem: find weights and "
                "biases that minimize a loss function on training data. Modern training uses "
                "backpropagation to compute gradients and stochastic gradient descent (or a "
                "variant) to update parameters.",
            ],
            "subsections": [
                {
                    "title": "3.4.1 Forward Pass",
                    "paragraphs": [
                        "The forward pass evaluates the network on an input. Starting from the "
                        "input layer, each layer applies its transformation and passes the "
                        "result to the next. Intermediate activations are cached for use in "
                        "the backward pass.",
                        "The final output is compared to the target using a loss function. "
                        "Common choices: mean squared error for regression, cross-entropy for "
                        "classification.",
                    ],
                },
                {
                    "title": "3.4.2 Backward Pass",
                    "paragraphs": [
                        "The backward pass computes the gradient of the loss with respect to "
                        "every parameter in the network. It does so by applying the chain rule "
                        "from output backwards.",
                        "Concretely, suppose the loss is L and the network has layers L₁, L₂, "
                        "..., Lₙ producing outputs a₁, a₂, ..., aₙ. The chain rule gives "
                        "∂L/∂Wₖ = (∂L/∂aₙ)(∂aₙ/∂aₙ₋₁)...(∂aₖ₊₁/∂aₖ)(∂aₖ/∂Wₖ). Backpropagation "
                        "computes these products efficiently by reusing intermediate results.",
                        "Cost: backpropagation takes roughly the same time as the forward pass. "
                        "This is what makes deep network training tractable. Modern frameworks "
                        "(PyTorch, JAX, TensorFlow) handle backpropagation automatically via "
                        "computational graphs and reverse-mode automatic differentiation.",
                    ],
                },
                {
                    "title": "3.4.3 Gradient Descent and Variants",
                    "image": "06_gradient_descent.png",
                    "caption": "Figure 3.6: Gradient descent on a quadratic surface vs noisy SGD.",
                    "paragraphs": [
                        "The update rule for gradient descent is θ ← θ - η ∇L(θ). Three "
                        "variants based on how many examples contribute to each gradient "
                        "estimate:",
                        "Batch gradient descent uses the entire training set per step. Smooth "
                        "convergence; each step is expensive; the dataset must fit in memory.",
                        "Stochastic gradient descent (SGD) uses one example per step. Cheap and "
                        "noisy; the noise can help escape sharp local minima but slows fine "
                        "convergence.",
                        "Mini-batch gradient descent is the practical compromise: a small batch "
                        "(typically 32 to 4096) per step. GPU-friendly, noise-controlled, and "
                        "the default for nearly all modern training.",
                        "Modern optimizers add momentum and adaptive learning rates. Momentum "
                        "averages recent gradients, smoothing noisy updates and accelerating "
                        "through ravines. Adam (Adaptive Moment Estimation) combines momentum "
                        "with per-parameter adaptive learning rates and is the default for "
                        "most deep learning workloads. AdamW decouples weight decay from the "
                        "gradient update and is preferred when regularization matters.",
                    ],
                },
            ],
        },
        {
            "number": "3.5",
            "title": "Training Pathologies",
            "image": "05_vanishing_gradient.png",
            "caption": "Figure 3.7: Gradient magnitude across layers under vanishing and exploding conditions.",
            "paragraphs": [
                "Deep networks suffer characteristic training problems that simpler models do "
                "not.",

                "Vanishing gradients: when gradients are repeatedly multiplied by small "
                "numbers (as happens with saturating activations or poorly initialized weights), "
                "the gradient that reaches early layers becomes negligible. Those layers stop "
                "learning. Symptom: training loss plateaus far above optimal.",

                "Exploding gradients: when gradients are repeatedly multiplied by large numbers, "
                "they blow up. Weight updates become huge. Training diverges or produces NaN "
                "values. Common in RNNs unrolled over many steps.",

                "Mitigations: use ReLU-family activations (derivative is 1 on the active side); "
                "use careful weight initialization (Xavier/Glorot for tanh, He for ReLU); "
                "apply batch normalization or layer normalization; use residual connections "
                "(let gradients flow through identity paths); clip gradients (for explosion in "
                "RNNs and RL); use modern architectures (LSTM/GRU, transformers) designed to "
                "keep gradients healthy.",
            ],
        },
        {
            "number": "3.6",
            "title": "Regularization",
            "image": "17_overfitting.png",
            "caption": "Figure 3.8: Overfitting shows as widening gap between train and validation loss.",
            "paragraphs": [
                "A model with enough capacity will memorize the training set. The goal is to "
                "generalize. Regularization techniques reduce variance without sacrificing too "
                "much expressive power.",
            ],
            "subsections": [
                {
                    "title": "3.6.1 Weight Penalties",
                    "paragraphs": [
                        "L2 regularization (weight decay) adds λ Σᵢ wᵢ² to the loss. The "
                        "optimizer pulls weights toward zero in proportion to their "
                        "magnitude. Encourages distributed representations rather than relying "
                        "on a few large weights.",
                        "L1 regularization adds λ Σᵢ |wᵢ|. Encourages sparsity: many weights "
                        "go to exactly zero. Useful when sparse models are desired (feature "
                        "selection, compressed deployment).",
                    ],
                },
                {
                    "title": "3.6.2 Dropout",
                    "image": "18_dropout.png",
                    "caption": "Figure 3.9: Dropout randomly removes neurons during training.",
                    "paragraphs": [
                        "Dropout randomly zeros each neuron's output with probability p during "
                        "training. At test time, all neurons are active. This prevents co-"
                        "adaptation: each neuron must produce useful features regardless of "
                        "which other neurons happen to be active in any given batch.",
                        "Dropout can be interpreted as training an ensemble of subnetworks and "
                        "averaging them at inference. Typical p: 0.5 for fully connected, 0.1 "
                        "to 0.3 for transformer blocks. Modern transformer LLMs rely more on "
                        "data scale and weight decay than aggressive dropout.",
                    ],
                },
                {
                    "title": "3.6.3 Batch and Layer Normalization",
                    "paragraphs": [
                        "Batch normalization (BN) normalizes the activations of each feature "
                        "across the batch dimension. It stabilizes training, allows larger "
                        "learning rates, and acts as mild regularization. Works well in CNNs "
                        "with large batches.",
                        "Layer normalization (LN) normalizes across the feature dimension "
                        "within each example. No batch dependence. The default in transformers "
                        "because attention with variable-length sequences breaks BN's "
                        "assumptions.",
                        "RMSNorm is a recent simplification of LN: drop the mean-centering, "
                        "keep only the variance normalization. Used in LLaMA and other modern "
                        "LLMs. Slightly faster, comparable quality.",
                    ],
                },
                {
                    "title": "3.6.4 Data Augmentation and Early Stopping",
                    "paragraphs": [
                        "Data augmentation creates additional training examples by applying "
                        "transformations that preserve the label: random crops and flips for "
                        "images, back-translation and synonym substitution for text. The model "
                        "sees more variation; generalization improves.",
                        "Early stopping monitors validation loss during training and stops "
                        "when it begins to rise. Simple and effective. Many modern training "
                        "frameworks include early stopping as a default callback.",
                    ],
                },
            ],
        },
        {
            "number": "3.7",
            "title": "Convolutional Neural Networks",
            "image": "07_cnn.png",
            "caption": "Figure 3.10: A typical CNN for image classification.",
            "paragraphs": [
                "Fully connected networks ignore the spatial structure of images. A CNN "
                "encodes two priors that match how images work: local receptive fields (each "
                "neuron sees only a small spatial neighborhood) and weight sharing (the same "
                "filter is applied at every spatial position).",

                "A convolutional layer slides a small filter across the input and computes a "
                "dot product at each position. The result is a feature map indicating where "
                "the filter pattern appears. Multiple filters per layer detect different "
                "patterns. Stacking layers builds hierarchy: edges in lower layers, textures "
                "and parts in middle layers, objects in upper layers.",

                "Pooling layers downsample feature maps, reducing spatial dimensions and "
                "providing translation invariance. Max pooling takes the maximum in each "
                "region; average pooling takes the mean. Modern architectures often use "
                "strided convolutions in place of explicit pooling.",

                "Famous architectures: LeNet (1998, digit recognition), AlexNet (2012, "
                "ImageNet breakthrough), VGG (2014, deep stacks of 3x3 convolutions), ResNet "
                "(2015, residual connections enabling very deep networks), EfficientNet, "
                "ConvNeXt. Vision Transformers (ViT) since 2020 have challenged CNNs at scale, "
                "though CNNs remain competitive and dominant at smaller scales.",
            ],
        },
        {
            "number": "3.8",
            "title": "Recurrent Neural Networks",
            "image": "08_rnn.png",
            "caption": "Figure 3.11: RNN unrolled in time; the hidden state carries information forward.",
            "paragraphs": [
                "RNNs process sequences one element at a time, maintaining a hidden state that "
                "summarizes everything seen so far. Each step: hₜ = f(W_h hₜ₋₁ + W_x xₜ + b). "
                "Outputs can be produced at each step (sequence labeling) or only at the end "
                "(classification).",

                "Vanilla RNNs suffer from vanishing gradients over long sequences. LSTMs (Long "
                "Short-Term Memory) add input, forget, and output gates plus a cell state, "
                "allowing the network to learn what to remember and what to forget over long "
                "spans. GRUs (Gated Recurrent Units) are a simpler variant with two gates and "
                "no separate cell state.",

                "RNNs dominated sequence modeling until transformers replaced them around 2018. "
                "They are still used where transformer overhead is excessive (very short "
                "sequences, embedded systems) and as components of larger architectures (mixed "
                "RNN-attention models, RWKV).",
            ],
        },
        {
            "number": "3.9",
            "title": "Summary",
            "bullets": [
                "A neural network is a parameterized function built from layers of artificial "
                "neurons connected by learned weights.",
                "Non-linear activations (ReLU and variants) are what give deep networks their "
                "expressive power.",
                "Training is gradient descent driven by backpropagation, which computes "
                "gradients through the chain rule.",
                "Vanishing and exploding gradients are the main training pathologies; modern "
                "architectures use normalization and residual connections to control them.",
                "Regularization (weight decay, dropout, normalization, augmentation, early "
                "stopping) trades a small amount of training fit for substantially better "
                "generalization.",
                "Convolutional networks encode spatial structure; recurrent networks encode "
                "temporal structure. Both are largely superseded by transformers for state-of-"
                "the-art results, but remain widely used in production.",
            ],
        },
    ],
    "further_reading": [
        "Goodfellow, Bengio, Courville, Deep Learning (2016), Chapters 6-10.",
        "Krizhevsky, Sutskever, Hinton, 'ImageNet Classification with Deep Convolutional Neural Networks' (2012).",
        "He et al., 'Deep Residual Learning for Image Recognition' (2015). ResNet.",
        "Hochreiter and Schmidhuber, 'Long Short-Term Memory' (1997). the original LSTM paper.",
    ],
}
