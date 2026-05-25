"""Chapter 8: Computer Vision and Multimodal Models."""

CHAPTER = {
    "label": "Chapter 8",
    "title": "Computer Vision and Multimodal Models",
    "sections": [
        {
            "number": "8.1",
            "title": "The Vision Frontier",
            "paragraphs": [
                "Computer vision has gone through three major eras in the deep learning age. "
                "The CNN era (2012-2018) saw AlexNet, VGG, GoogLeNet, and ResNet establish "
                "the dominance of convolutional networks for image tasks. The transition "
                "(2018-2020) brought attention into vision through models like the Image "
                "Transformer and DETR for object detection. The transformer era (2020-) "
                "started with Vision Transformers (ViT) and continued through multimodal "
                "models that span vision and language.",

                "This chapter covers each era briefly and lands on the modern state: "
                "multimodal foundation models that process images, text, audio, and video in "
                "a single architecture. The themes from earlier chapters reappear: "
                "self-supervised pretraining, contrastive learning, transformer "
                "architectures, scaling laws. The technologies look different but the "
                "principles converge.",
            ],
        },
        {
            "number": "8.2",
            "title": "Convolutional Neural Networks Revisited",
            "image": "07_cnn.png",
            "caption": "Figure 8.1: A typical CNN architecture for image classification.",
            "paragraphs": [
                "We introduced CNNs in Chapter 3. Here we dig into the architectural "
                "patterns that defined the CNN era and remain relevant today.",
            ],
            "subsections": [
                {
                    "title": "8.2.1 Building Blocks",
                    "paragraphs": [
                        "Convolutional layer: slide a learned filter across the input, "
                        "producing a feature map. Filters detect local patterns "
                        "(edges, textures, parts). Stride controls how the filter moves; "
                        "padding controls boundary handling. Each filter learns one kind of "
                        "pattern; a layer has many filters detecting different patterns.",
                        "Pooling layer: downsample feature maps. Max pooling takes the "
                        "maximum in each region; average pooling takes the mean. Reduces "
                        "spatial dimensions and provides limited translation invariance. "
                        "Modern architectures sometimes replace pooling with strided "
                        "convolutions.",
                        "Activation: typically ReLU. Applied element-wise after convolution.",
                        "Batch normalization: normalizes activations across the batch "
                        "dimension. Stabilizes training, allows larger learning rates.",
                        "Residual connection: add the input of a block to its output. "
                        "Enables training of very deep networks (ResNet-152 and beyond).",
                    ],
                },
                {
                    "title": "8.2.2 Famous Architectures",
                    "paragraphs": [
                        "LeNet-5 (LeCun, 1998): the original CNN for digit recognition. "
                        "Two conv layers, two pooling layers, three fully connected layers. "
                        "MNIST accuracy that beat hand-crafted features.",
                        "AlexNet (Krizhevsky et al., 2012): five conv layers, three FC. "
                        "ReLU, dropout, GPU training. Won ImageNet 2012 by a wide margin. "
                        "The paper that started the deep learning revolution.",
                        "VGG (Simonyan and Zisserman, 2014): a stack of 3x3 convolutions. "
                        "Up to 19 layers. Demonstrated that depth and small filters work "
                        "well. Still used as a feature extractor for perceptual loss.",
                        "GoogLeNet / Inception (Szegedy et al., 2014): parallel branches with "
                        "different filter sizes; concatenate outputs. Captures patterns at "
                        "multiple scales efficiently.",
                        "ResNet (He et al., 2015): residual connections enable training of "
                        "152-layer networks. Won ImageNet 2015. Residual connections "
                        "transferred to nearly every subsequent deep architecture, "
                        "including transformers.",
                        "EfficientNet (Tan and Le, 2019): compound scaling of depth, width, "
                        "and resolution. Achieves SOTA with fewer parameters than competing "
                        "architectures.",
                        "ConvNeXt (Liu et al., 2022): a modernized CNN matching ViT "
                        "performance with traditional convolutions. Demonstrates that CNN "
                        "architecture has more room to grow than transformer enthusiasm "
                        "suggested.",
                    ],
                },
            ],
        },
        {
            "number": "8.3",
            "title": "Vision Transformers",
            "paragraphs": [
                "Vision Transformer (ViT, Dosovitskiy et al., 2020) brought the transformer "
                "architecture to images. The recipe is brutally simple: split an image into "
                "fixed-size patches (typically 16x16 pixels), flatten and linearly project "
                "each patch into a vector, prepend a [CLS] token, add positional "
                "embeddings, run through a standard transformer encoder, classify from the "
                "[CLS] embedding.",

                "The simplicity belies the power. At sufficient scale (300M+ images), ViTs "
                "match or exceed CNN performance on image classification. The inductive "
                "biases of convolutions (locality, translation equivariance) are less "
                "important when you have enough data; the model learns whatever structure "
                "is useful.",

                "Variants. DeiT (Touvron et al., 2021) trained ViTs efficiently on smaller "
                "datasets through better regularization and distillation. Swin Transformer "
                "(Liu et al., 2021) introduced shifted windows to give ViTs the "
                "hierarchical structure of CNNs. MAE (Masked Autoencoder, He et al., 2021) "
                "applied BERT-style masked patch prediction to vision pretraining.",

                "Production state. CNNs (ResNet, EfficientNet, ConvNeXt) and ViTs both have "
                "their place. CNNs are easier to train on small datasets and have well-"
                "optimized inference. ViTs win at very large scale and transfer better to "
                "multimodal architectures. The choice often comes down to deployment "
                "constraints and the size of available data.",
            ],
        },
        {
            "number": "8.4",
            "title": "Object Detection and Segmentation",
            "paragraphs": [
                "Image classification assigns one label to a whole image. Detection and "
                "segmentation are harder.",

                "Object detection finds bounding boxes plus class labels for each object in "
                "the image. Classical approaches (R-CNN family) used a region proposal "
                "step plus a CNN classifier. YOLO (You Only Look Once, Redmon et al.) and "
                "SSD (Single Shot Detector) made detection real-time by predicting boxes "
                "and classes in a single forward pass. DETR (DEtection TRansformer, Carion "
                "et al., 2020) reformulated detection as a set prediction problem using a "
                "transformer; no hand-tuned post-processing required.",

                "Semantic segmentation labels every pixel with a class. U-Net (Ronneberger "
                "et al., 2015) is the classic architecture: an encoder-decoder with skip "
                "connections from encoder to decoder at matching resolutions. Used "
                "everywhere from medical imaging to satellite analysis. The same U-Net "
                "architecture is the backbone of Stable Diffusion's denoiser, decades after "
                "its original publication.",

                "Instance segmentation labels every pixel and distinguishes between "
                "instances of the same class (this cat vs that cat). Mask R-CNN (He et al., "
                "2017) extends Faster R-CNN with a parallel mask prediction branch.",

                "Segment Anything Model (SAM, Meta, 2023) brought a foundation-model "
                "approach: a single model trained on 1 billion masks across 11 million "
                "images, capable of zero-shot segmentation of any object in any image given "
                "a prompt (point, box, text).",
            ],
        },
        {
            "number": "8.5",
            "title": "CLIP and Vision-Language Pretraining",
            "paragraphs": [
                "CLIP (Contrastive Language-Image Pretraining, Radford et al., 2021) was a "
                "watershed for multimodal AI. The approach is conceptually simple: train an "
                "image encoder and a text encoder jointly with contrastive loss on 400M "
                "image-caption pairs from the web. Each (image, caption) pair is a positive; "
                "every other pairing in the batch is a negative. The two encoders end up "
                "producing aligned embeddings in a shared space.",

                "The capabilities that emerge are remarkable. Zero-shot image "
                "classification: encode candidate class names as text, embed the image, "
                "take the argmax similarity. No labeled image data required for the new "
                "classes. CLIP matched supervised ImageNet models without seeing ImageNet "
                "labels.",

                "Cross-modal retrieval: search images with text queries; search text with "
                "image queries. Used in image search engines, content moderation, "
                "duplicate detection at scale.",

                "Foundation for downstream models. CLIP's text encoder is the conditioning "
                "input for Stable Diffusion. CLIP's image encoder is the visual backbone "
                "of many multimodal LLMs (LLaVA, BLIP-2). The CLIP embedding space has "
                "become an infrastructure asset, used in countless downstream systems.",

                "Successors and competitors. ALIGN (Google, 2021) scaled to 1.8B noisy "
                "pairs. SigLIP (Google, 2023) replaced softmax contrastive loss with a "
                "sigmoid-based pairwise loss, more efficient at large batch sizes. LiT "
                "(Zhai et al., 2022) showed that a frozen image encoder plus a learned text "
                "encoder works well. EVA-CLIP and OpenCLIP are strong open-weights "
                "alternatives.",
            ],
        },
        {
            "number": "8.6",
            "title": "BLIP, BLIP-2, and Vision-Language Generation",
            "paragraphs": [
                "CLIP aligns images and text but does not generate. For tasks like image "
                "captioning, visual question answering, and visual reasoning, you need a "
                "model that can generate text conditioned on images.",

                "BLIP (Bootstrapping Language-Image Pretraining, Li et al., 2022) unified "
                "vision-language understanding and generation. A single transformer that can "
                "operate as image-text matching, image grounded text encoder, or image "
                "grounded text decoder.",

                "BLIP-2 (Li et al., 2023) introduced the Q-Former: a small bridge module "
                "between a frozen image encoder and a frozen LLM. The Q-Former has a small "
                "set of learnable query tokens that cross-attend to image features and "
                "output tokens that an LLM can consume. The trainable surface is tiny "
                "compared to the frozen models (32M Q-Former parameters vs billions in the "
                "encoders), but the resulting model is competitive with much larger "
                "end-to-end systems.",

                "Flamingo (DeepMind, 2022) interleaved cross-attention layers between "
                "transformer blocks of a frozen LLM, conditioned on visual features from a "
                "Perceiver Resampler. Few-shot visual reasoning emerged at scale.",

                "LLaVA (Liu et al., 2023) took a simpler approach: project visual features "
                "from CLIP into the LLM's token embedding space via a linear or MLP layer. "
                "The LLM processes a mixed sequence of visual and text tokens uniformly. "
                "Strong instruction-following multimodal model that became the open-source "
                "default.",

                "GPT-4V (OpenAI, 2023), Gemini (Google, 2023+), and Claude 3 (Anthropic, "
                "2024) brought multimodal capabilities to frontier closed models. Native "
                "multimodality: images, text, and (in Gemini and GPT-4o) audio in a single "
                "model, trained jointly rather than bolted together.",
            ],
        },
        {
            "number": "8.7",
            "title": "Diffusion Models for Image Generation",
            "image": "31_diffusion.png",
            "caption": "Figure 8.2: Diffusion forward pass adds noise; reverse pass denoises.",
            "paragraphs": [
                "Generative image models went through three eras. VAEs (Variational "
                "Autoencoders, Kingma and Welling, 2013) produced blurry but principled "
                "samples. GANs (Generative Adversarial Networks, Goodfellow et al., 2014) "
                "produced sharp samples but were hard to train. Diffusion models (Sohl-"
                "Dickstein et al., 2015; Ho et al., 2020) became the dominant approach "
                "around 2021, combining training stability with sharp samples.",
            ],
            "subsections": [
                {
                    "title": "8.7.1 The Diffusion Process",
                    "paragraphs": [
                        "Forward process: starting from a real image, progressively add "
                        "Gaussian noise over T steps until the image is indistinguishable "
                        "from pure noise. The noise schedule controls how quickly noise "
                        "accumulates.",
                        "Reverse process: learn to undo the noising. A neural network "
                        "(typically a U-Net) takes a noisy image at timestep t and predicts "
                        "either the original image, the noise added, or a velocity "
                        "parameterization. Apply iteratively from t=T to t=0 to generate "
                        "a clean image from pure noise.",
                        "Training is stable and simple: pick a random timestep t, noise a "
                        "training image to that timestep, train the network to predict the "
                        "noise. Cross-entropy and adversarial training are not required.",
                    ],
                },
                {
                    "title": "8.7.2 Latent Diffusion and Stable Diffusion",
                    "paragraphs": [
                        "Pixel-space diffusion is expensive: high resolution means large "
                        "tensors. Latent Diffusion Models (Rombach et al., 2022) operate in "
                        "the latent space of a pretrained VAE. Encode the image to a small "
                        "latent (typically 8x compression). Apply diffusion in latent space. "
                        "Decode the final latent through the VAE.",
                        "Stable Diffusion is the open-weights implementation of this idea. "
                        "Made high-quality text-to-image generation accessible to anyone "
                        "with a consumer GPU. The U-Net cross-attends to text encoder "
                        "(CLIP) embeddings at every layer to condition generation on the "
                        "prompt.",
                        "SDXL (2023), SD3 (2024), and the FLUX family (2024) pushed quality "
                        "further with larger models, better text encoders (T5-XXL), and "
                        "improved training data and procedures.",
                    ],
                },
                {
                    "title": "8.7.3 Classifier-Free Guidance",
                    "paragraphs": [
                        "Naive text conditioning is weak. The model trades off between "
                        "following the prompt and producing realistic images. Classifier-"
                        "free guidance (CFG, Ho and Salimans, 2022) strengthens text "
                        "conditioning at inference time.",
                        "Train the model with the text condition dropped some fraction of "
                        "the time. At inference, compute both the conditional and "
                        "unconditional predictions; extrapolate in the direction of the "
                        "conditional: ε_guided = ε_uncond + s · (ε_cond - ε_uncond), where "
                        "s is the guidance scale (typically 5-15).",
                        "Higher s = more prompt adherence, less realism. Lower s = more "
                        "realistic, less prompt-following. Tune for your application.",
                    ],
                },
                {
                    "title": "8.7.4 Diffusion Samplers",
                    "paragraphs": [
                        "The sampler is the numerical integration scheme for the reverse "
                        "process. Many choices, each trading speed for quality.",
                        "DDPM (the original): stochastic; needs ~1000 steps for high quality.",
                        "DDIM: deterministic; 20-50 steps suffice. Standard default.",
                        "PNDM: linear multistep method. Higher accuracy at fewer steps.",
                        "DPM-Solver / DPM-Solver++: exponential integrators. 10-20 steps. "
                        "Common in production services.",
                        "UniPC: universal predictor-corrector. ~10 steps. Strong default for "
                        "modern models.",
                        "Choose based on speed-quality requirements. Most production "
                        "systems use 20-30 steps of DPM-Solver++.",
                    ],
                },
                {
                    "title": "8.7.5 Beyond Images: Audio, Video, 3D",
                    "paragraphs": [
                        "Diffusion has expanded beyond images. AudioLM, MusicLM, and Suno use "
                        "diffusion-like processes for music. Stable Audio, Stable Video "
                        "Diffusion, Sora (OpenAI), and Runway Gen-3 apply diffusion to "
                        "video. Point-E and DreamFusion generate 3D models.",
                        "The general pattern: tokenize the target modality (or work in a "
                        "latent space), train a diffusion model to denoise, condition on "
                        "text. Each modality adds challenges (temporal coherence in video, "
                        "perceptual quality in audio), but the underlying recipe is "
                        "remarkably consistent.",
                    ],
                },
            ],
        },
        {
            "number": "8.8",
            "title": "Multimodal Foundation Models",
            "paragraphs": [
                "The frontier today is multimodal foundation models: single models that "
                "natively handle text, images, audio, and video in both input and output. "
                "Gemini 1.5/2.0 (Google), GPT-4o (OpenAI), and Claude 3.5 (Anthropic) "
                "exemplify this category.",

                "Architectural patterns. Shared embedding space (CLIP-style) for retrieval "
                "and zero-shot classification. Cross-attention bridges (Q-Former, Perceiver "
                "Resampler) connecting modality-specific encoders to a language model. "
                "Direct token projection (LLaVA, GPT-4V style) where the LLM processes "
                "mixed-modality sequences uniformly. Native multimodal training where the "
                "model is trained on interleaved text and images from the start.",

                "Capabilities. Visual question answering (what's in this chart?), document "
                "understanding (extract data from a PDF screenshot), code from screenshots "
                "(implement this UI design), text generation from images (caption, "
                "describe), image generation from text, video understanding, transcription, "
                "speech synthesis. The same model handles all of these.",

                "Engineering implications. A single API replaces what used to require "
                "separate models for vision, speech, and language. Cost and latency "
                "decisions move from 'which model to call' to 'how much context to "
                "provide'. Production systems can ask users to attach images, screenshots, "
                "or recordings naturally, since the model handles them.",
            ],
        },
        {
            "number": "8.9",
            "title": "Summary",
            "bullets": [
                "CNNs dominated computer vision through the 2010s. ResNet's residual "
                "connections are the most influential architectural choice; they transferred "
                "to transformers and beyond.",
                "Vision Transformers (ViT) treat images as sequences of patches. At scale, "
                "they match or exceed CNNs.",
                "Object detection (YOLO, DETR) and segmentation (U-Net, SAM) tackle more "
                "structured vision tasks.",
                "CLIP aligned image and text in a shared embedding space, enabling zero-shot "
                "classification and cross-modal retrieval. Its embeddings became "
                "infrastructure.",
                "Diffusion models generate images by learning to denoise. Latent Diffusion "
                "and Stable Diffusion brought high-quality text-to-image generation to "
                "consumers.",
                "Multimodal foundation models (Gemini, GPT-4o, Claude 3.5) handle text, "
                "images, audio, and video in a single architecture. The frontier of AI is "
                "now multimodal by default.",
            ],
        },
    ],
    "further_reading": [
        "He et al., 'Deep Residual Learning for Image Recognition' (2015). ResNet.",
        "Dosovitskiy et al., 'An Image is Worth 16x16 Words: Transformers for Image Recognition' (2020). ViT.",
        "Radford et al., 'Learning Transferable Visual Models From Natural Language Supervision' (2021). CLIP.",
        "Ho et al., 'Denoising Diffusion Probabilistic Models' (2020).",
        "Rombach et al., 'High-Resolution Image Synthesis with Latent Diffusion Models' (2022). Stable Diffusion.",
        "Li et al., 'BLIP-2: Bootstrapping Language-Image Pre-training' (2023).",
    ],
}
