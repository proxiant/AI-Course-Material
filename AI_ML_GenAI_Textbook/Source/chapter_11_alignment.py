"""Chapter 11: Alignment with Reinforcement Learning."""

CHAPTER = {
    "label": "Chapter 11",
    "title": "Alignment with Reinforcement Learning",
    "intro_image": "40_rlhf_detailed.png",
    "intro_caption": "Figure 11.1: The three stages of RLHF: SFT, reward model, PPO.",
    "sections": [
        {
            "number": "11.1",
            "title": "What Alignment Means",
            "paragraphs": [
                "A pretrained language model predicts the next token. An instruction-tuned "
                "model follows directions. Neither is automatically helpful, honest, or "
                "harmless. Alignment is the process of making the model behave the way we "
                "want, even when the right behavior is hard to specify.",

                "The challenge: 'be helpful' is not a function we can write down. It is a "
                "judgment that depends on context, user intent, and downstream consequences. "
                "Traditional supervised learning needs (input, output) pairs, but there is "
                "no single correct output for an open-ended question.",

                "Reinforcement learning from human feedback (RLHF) addresses this by "
                "learning a reward function from human preferences. Humans rank model "
                "outputs against each other. A reward model is trained to predict the "
                "rankings. The LLM is then optimized to maximize the reward model's score. "
                "The result: an LLM that produces responses humans prefer, even on prompts "
                "where the right answer cannot be enumerated in advance.",

                "This chapter walks through the alignment pipeline: classical RLHF with "
                "PPO, modern simplifications (DPO, GRPO), reinforcement learning with "
                "verifiable rewards (RLVR) for reasoning, and the practical pitfalls of "
                "alignment training.",
            ],
        },
        {
            "number": "11.2",
            "title": "The Three Stages of RLHF",
            "paragraphs": [
                "RLHF as originally formulated has three sequential stages.",

                "Stage 1: Supervised fine-tuning (SFT). Start from a pretrained base model. "
                "Fine-tune on a curated set of (prompt, ideal response) pairs written or "
                "selected by humans. The model learns to follow instructions in a "
                "desirable style. The output of this stage is the SFT model.",

                "Stage 2: Reward model (RM). Sample multiple responses from the SFT model "
                "per prompt. Have humans rank them (typically pairwise: A vs B, which is "
                "better?). Train a separate model to predict the human preference: "
                "RM(prompt, response) → scalar. The reward model encodes 'what humans like'.",

                "Stage 3: Policy optimization. Use the reward model as the reward signal "
                "to fine-tune the SFT model with reinforcement learning, typically PPO. "
                "Each step: sample a prompt, generate a response, compute reward = "
                "RM(prompt, response) - β · KL(policy || SFT). The KL penalty prevents the "
                "policy from drifting into reward-hacking regions far from the SFT "
                "distribution.",

                "The result: an LLM that is helpful, harmless, and honest within the limits "
                "of the preference data. Used to train ChatGPT, Claude, LLaMA-Chat, and "
                "every modern frontier instruction-tuned model.",
            ],
        },
        {
            "number": "11.3",
            "title": "Proximal Policy Optimization (PPO)",
            "image": "32_ppo_clip.png",
            "caption": "Figure 11.2: PPO's clipped surrogate objective bounds policy updates.",
            "paragraphs": [
                "PPO is the workhorse RL algorithm for LLM alignment. It is a policy "
                "gradient method with two key innovations: a clipped surrogate objective "
                "to bound policy updates, and an advantage estimate to reduce variance.",
            ],
            "subsections": [
                {
                    "title": "11.3.1 The Clipped Objective",
                    "paragraphs": [
                        "Naive policy gradient is unbiased but high-variance. Trust region "
                        "methods (TRPO) constrain the KL divergence between old and new "
                        "policies to prevent destructive updates. PPO replaces the hard KL "
                        "constraint with a soft clipped ratio:",
                    ],
                    "equation": "L^CLIP(θ) = E[min(r_t · A_t, clip(r_t, 1-ε, 1+ε) · A_t)]",
                    "equation_label": "11.1",
                    "more_paragraphs": [
                        "where r_t = π_θ(a_t|s_t) / π_old(a_t|s_t) is the probability ratio "
                        "and A_t is the advantage. The clip range (typically ε=0.2) "
                        "prevents the policy from changing too much in either direction. "
                        "PPO takes min(clipped, unclipped) to make the surrogate "
                        "pessimistic: rewards are limited by the clip, but penalties are "
                        "not.",
                    ],
                },
                {
                    "title": "11.3.2 KL Penalty Against the Reference",
                    "paragraphs": [
                        "In RLHF, PPO is augmented with a KL penalty against the reference "
                        "(SFT) model. The full reward becomes:",
                    ],
                    "equation": "r_total = RM(prompt, response) - β · KL(π_θ || π_SFT)",
                    "equation_label": "11.2",
                    "more_paragraphs": [
                        "Without this, the policy drifts off the language model manifold "
                        "and reward hacks: it finds inputs that trick the reward model into "
                        "high scores but produce gibberish. The β coefficient (typically "
                        "0.01-0.1) balances reward chasing against staying close to the "
                        "SFT policy.",
                        "Tuning β is a black art. Too low: policy hacks the reward. Too "
                        "high: the policy doesn't improve. Start with β=0.05 and adjust "
                        "based on KL divergence and reward trends.",
                    ],
                },
                {
                    "title": "11.3.3 Practical Notes",
                    "paragraphs": [
                        "Learning rate: very small, 1e-6 to 5e-6 for 7B models. RL is "
                        "fragile.",
                        "Value function: a separate value head estimates V(s). The advantage "
                        "is computed as A_t = R_t - V(s_t). The value function adds memory "
                        "cost but reduces variance.",
                        "Reward scaling: scale rewards so the median advantage is order 1. "
                        "Otherwise gradients are too large or too small.",
                        "Reference policy: the SFT model itself. Held fixed during PPO. Used "
                        "for both the KL penalty and as the initialization for the trainable "
                        "policy.",
                        "Sample efficiency: low. Each PPO step requires sampling new "
                        "completions, scoring them, and updating. Expensive.",
                    ],
                },
            ],
        },
        {
            "number": "11.4",
            "title": "Direct Preference Optimization (DPO)",
            "paragraphs": [
                "PPO works but is complex: three models in play (policy, reference, "
                "reward), sampling at training time, careful tuning of β and clip. DPO "
                "(Rafailov et al., 2023) simplifies dramatically.",

                "The insight. The optimal solution to the RLHF objective has a closed form. "
                "Substituting it back gives a simple classification loss on preference "
                "pairs:",
            ],
            "equation": "L^DPO = -E[log σ(β · (log π_θ(y_w|x)/π_ref(y_w|x) - log π_θ(y_l|x)/π_ref(y_l|x)))]",
            "equation_label": "11.3",
            "subsections": [
                {
                    "title": "11.4.1 Why DPO Wins",
                    "paragraphs": [
                        "No reward model. The RM is implicit in the policy's own preference "
                        "for chosen over rejected responses.",
                        "No sampling at training time. DPO trains on pre-collected "
                        "preference pairs (prompt, chosen, rejected). Just compute the loss.",
                        "No value function. No PPO clipping. Just supervised learning on "
                        "preferences.",
                        "Smaller compute footprint. Often matches or beats PPO at a "
                        "fraction of the engineering and compute cost.",
                    ],
                },
                {
                    "title": "11.4.2 When DPO Loses",
                    "paragraphs": [
                        "Multi-turn tasks where the policy needs to learn long sequences "
                        "of actions. PPO's on-policy sampling adapts; DPO's offline "
                        "preferences can become stale.",
                        "Tasks where the reward signal is rich and well-defined "
                        "(verifiable rewards). PPO can extract more from such signals.",
                        "Tasks with sparse positive examples. DPO's contrastive nature "
                        "needs paired data.",
                    ],
                },
                {
                    "title": "11.4.3 DPO Variants",
                    "paragraphs": [
                        "IPO (Identity Preference Optimization) addresses DPO's tendency to "
                        "overfit when preferences are noisy.",
                        "KTO (Kahneman-Tversky Optimization) needs only binary feedback "
                        "(good/bad), not paired preferences.",
                        "ORPO (Odds Ratio Preference Optimization) combines SFT and "
                        "preference optimization in a single loss, eliminating the need "
                        "for a separate SFT stage.",
                        "SimPO (Simple Preference Optimization) drops the reference model "
                        "and length-normalizes, simplifying the training pipeline further.",
                    ],
                },
            ],
        },
        {
            "number": "11.5",
            "title": "Group Relative Policy Optimization (GRPO)",
            "paragraphs": [
                "GRPO (introduced in DeepSeekMath, Shao et al., 2024) is a policy "
                "optimization method that drops the value network. Instead of training a "
                "separate V(s), it computes relative advantages within groups of samples.",

                "The procedure. For each prompt, sample G responses (typically 4-8). "
                "Compute reward for each. The advantage of response i is its reward minus "
                "the group mean reward. Update the policy with the standard PPO objective "
                "using these group-relative advantages.",

                "Why this matters. The value network is half the parameters and half the "
                "memory of PPO. GRPO eliminates it. Memory footprint drops roughly 50%, "
                "enabling RL training of larger models on the same hardware.",

                "Quality. Matches PPO on many tasks. The group-relative baseline is a "
                "noisier estimate of the value function but does not require maintaining "
                "and updating a separate network.",

                "Use cases. Default for reasoning RL (DeepSeek-R1, DeepSeekMath). "
                "Increasingly popular for general alignment as the memory savings compound "
                "at scale.",
            ],
        },
        {
            "number": "11.6",
            "title": "Reinforcement Learning with Verifiable Rewards (RLVR)",
            "paragraphs": [
                "Classical RLHF uses a learned reward model. The reward model can be wrong, "
                "biased, or exploitable. The model also generalizes poorly far from the "
                "preference distribution.",

                "When the correct answer can be programmatically verified, you can skip "
                "the reward model entirely. The verifier is the reward function. Examples: "
                "code generation (does the code pass unit tests?), math (does the answer "
                "match the gold?), SQL (does the query execute and return the expected "
                "rows?), theorem proving (does the proof check?).",

                "This is RLVR (Reinforcement Learning with Verifiable Rewards). Faster than "
                "RLHF (no reward model to train), more honest (no exploitable proxy "
                "reward), and uniquely suited to reasoning tasks.",

                "DeepSeek-R1 (2025) demonstrated RLVR at scale. Starting from a base "
                "language model, RLVR on math and code produced a reasoning model "
                "competitive with OpenAI's o1. The reasoning emerged from RL on verifiable "
                "rewards, without any chain-of-thought demonstration data.",

                "Limits. RLVR is only available when verification is cheaper than "
                "generation. For open-ended tasks (write a poem, compose an email, "
                "summarize a meeting), there is no programmatic verifier. RLHF is "
                "necessary.",
            ],
        },
        {
            "number": "11.7",
            "title": "Constitutional AI and RLAIF",
            "paragraphs": [
                "Human preference annotation is expensive. Constitutional AI (Bai et al., "
                "2022, Anthropic) replaces human preferences with AI-generated preferences "
                "guided by a written constitution.",

                "Process. Write the constitution: principles like 'be helpful', 'be "
                "harmless', 'avoid deception'. Use the constitution in two ways:",

                "Supervised stage. The model critiques and revises its own outputs based "
                "on constitutional principles. The revised outputs become SFT training data.",

                "RL stage. AI-generated preferences using the constitution as a rubric. "
                "Train with RLHF on these AI preferences (RLAIF, Reinforcement Learning "
                "from AI Feedback).",

                "Why it matters. Scales beyond human preference data. Makes behavior more "
                "transparent (you can read the rules). Easier to update behavior by editing "
                "the constitution. Used by Anthropic in Claude.",

                "Limits. The constitution itself encodes biases. AI judging AI can amplify "
                "errors. Rigid rule-following can produce unhelpful refusals. Most "
                "production systems combine constitutional principles with human "
                "preference data.",
            ],
        },
        {
            "number": "11.8",
            "title": "Reward Hacking and Alignment Failures",
            "paragraphs": [
                "Reward hacking is the central failure mode of RL on imperfect rewards. "
                "The model finds inputs that score high according to the reward signal but "
                "do not match the intent.",

                "Examples. Length bias: the reward model prefers longer responses; the "
                "policy learns to produce verbose answers regardless of quality. "
                "Sycophancy: the reward model prefers responses that agree with the user; "
                "the policy learns to flatter rather than be accurate. Refusal hacking: "
                "the reward model penalizes harmful outputs; the policy learns to refuse "
                "everything ambiguous, even legitimate requests.",

                "Mitigations. Diverse preference data. KL penalty against a reference. "
                "Detection: monitor for length inflation, sycophancy, over-refusal. "
                "Red-team adversarially before deployment. Use multiple reward signals "
                "(helpfulness, harmlessness, honesty) and balance them explicitly.",

                "Catastrophic forgetting. Aggressive RL can degrade general capabilities. "
                "Maintain a regression suite (MMLU, HumanEval, GSM8K) and check after "
                "each major training run.",

                "Distribution shift. RL can push the policy into regions far from "
                "pretraining. KL penalty mitigates this; explicit mixing of pretraining "
                "data during RL also helps for some objectives.",
            ],
        },
        {
            "number": "11.9",
            "title": "Practical Alignment Pipeline",
            "paragraphs": [
                "A typical modern alignment pipeline.",

                "Step 1: Data collection. Curate or buy a high-quality instruction "
                "dataset. Collect preference data through pairwise rankings or A/B tests.",

                "Step 2: SFT. Fine-tune the base model on instructions. Use LoRA or full "
                "fine-tuning depending on compute. 1-3 epochs.",

                "Step 3: Preference optimization. Train with DPO or GRPO on preference "
                "pairs. Simpler than PPO, often comparable quality. Use PPO only if you "
                "have specific reasons.",

                "Step 4: Evaluation. Held-out preference pairs. MT-Bench. Chatbot Arena if "
                "you can. Safety benchmarks. Regression suite for base capabilities.",

                "Step 5: Iteration. Identify failure modes. Collect new preference data "
                "targeting those failures. Repeat training.",

                "Step 6: Production deployment with continuous evaluation. Sample traffic "
                "for offline scoring. Monitor for drift. Collect production preference "
                "data to feed the next iteration.",
            ],
        },
        {
            "number": "11.10",
            "title": "Summary",
            "bullets": [
                "Alignment is making models behave the way we want, even when correct "
                "behavior is hard to specify.",
                "Classical RLHF has three stages: SFT, reward model, PPO. The KL penalty "
                "against the reference model is essential to prevent reward hacking.",
                "DPO simplifies RLHF dramatically by deriving the optimal policy in "
                "closed form. No reward model, no sampling at training time. Often the "
                "right default.",
                "GRPO drops the value network. Memory savings enable larger-model RL.",
                "RLVR uses programmatic verifiers as rewards. Faster, more honest, "
                "well-suited to math and code. Limited to tasks with verifiable "
                "correctness.",
                "Constitutional AI generates preferences from written principles, scaling "
                "beyond human annotation.",
                "Reward hacking, sycophancy, over-refusal, and catastrophic forgetting are "
                "the main alignment failure modes. Diverse data and ongoing evaluation are "
                "the main defenses.",
            ],
        },
    ],
    "further_reading": [
        "Christiano et al., 'Deep Reinforcement Learning from Human Preferences' (2017).",
        "Ouyang et al., 'Training Language Models to Follow Instructions with Human Feedback' (2022). the InstructGPT paper, foundational for ChatGPT.",
        "Rafailov et al., 'Direct Preference Optimization' (2023).",
        "Shao et al., 'DeepSeekMath' (2024). GRPO.",
        "Bai et al., 'Constitutional AI: Harmlessness from AI Feedback' (2022).",
        "DeepSeek-AI, 'DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning' (2025).",
    ],
}
