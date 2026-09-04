# This Week In AI Research (19-25 April 26) 🗓️

**From:** "Dr. Ashish Bamania from Into AI" <intoai@substack.com>
**Date:** Wed, 29 Apr 2026 01:10:35 +0000
**Message ID:** 19dd6c9dd9c9feb3

---

View this post on the web at https://www.intoai.pub/p/this-week-in-ai-research-19-25-april

1. DeepSeek-V4
This research paper introduces the preview version of the DeepSeek-V4 series with two Mixture-of-Experts (MoE) language models:
DeepSeek-V4-Pro with 1.6T parameters (49B activated)
DeepSeek-V4-Flash with 284B parameters (13B activated)
Both models support a context length of 1 million tokens and use multiple architectural and optimization techniques, including:
A hybrid attention architecture that combines Compressed Sparse Attention (CSA) and Heavily Compressed Attention (HCA) to improve long-context efficiency
ManifoldConstrained Hyper-Connections (mHC) over conventional residual connections
The Muon optimizer for faster convergence and greater training stability
Models in the DeepSeek-V4 series are highly efficient in long-context scenarios, with DeepSeekV4-Pro requiring only 27% of single-token inference FLOPs and 10% of KV cache compared with DeepSeek-V3.2 in the 1M token context setting.
DeepSeek-V4-ProMax is the maximum reasoning-effort mode of DeepSeek-V4-Pro, representing the new state of the art for open models.
Read more about this research using this link [ https://substack.com/redirect/9a4bc564-27d9-4f0e-b7b7-b6f451fae1a8?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
2. Hyperloop Transformers
This research paper introduces the Hyper-Connected Looped (Hyperloop) Transformer, a simple architecture that reuses Transformer layers across depth, making them more parameter-efficient than conventional Transformers.
The looped Transformer is organized into three blocks (begin, middle, and end), where each block consists of multiple Transformer layers, and only the middle block is applied recurrently across depth. The looped middle block is further augmented by Manifold-Constrained Hyper-Connections (mHC) [ https://substack.com/redirect/9131b4a1-d24c-4b39-b951-521296079b0f?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ], which are applied only after each loop to create the Hyperloop Transformer.
The Hyperloop Transformer outperforms depth-matched Transformer and mHC Transformer baselines despite using ~50% fewer parameters, and its outperformance persists after post-training weight quantization.
Read more about this research using this link [ https://substack.com/redirect/f0552b00-f1fa-4c46-a582-16d0fb46e5c4?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
3. LLaDA2.0-Uni
This research paper introduces LLaDA2.0-Uni, a unified discrete diffusion LLM (dLLM) that combines language and vision within a single framework.
The model converts images into discrete semantic tokens, jointly processes text and visual inputs using a Mixture-of-experts (MoE) [ https://substack.com/redirect/204a3085-e567-4028-b725-8eeb1a2dc59d?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ] backbone, and then reconstructs high-quality images with a diffusion decoder. This architecture enables the model to understand, generate, and edit across different modalities within a single system.
LLaDA2.0-Uni matches specialized VLMs in multimodal understanding and has strong performance in image generation and editing.
Read more about this research using this link [ https://substack.com/redirect/33a4a78e-b6f9-47ef-b793-08cb36b2590e?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
4. Sapiens2
This research paper introduces Sapiens2, a family of high-resolution vision transformer models designed for human-centric vision tasks, including pose estimation, segmentation, and surface reconstruction.
Sapiens2 models are pretrained using unified objectives (combining masked image reconstruction and self-distilled contrastive learning) on a curated dataset of 1 billion high-quality human images.
These models set a new state of the art, improving over the first generation in pose, body-part segmentation, and normal estimation, and extending to new tasks such as pointmap and albedo estimation.
Read more about this research using this link [ https://substack.com/redirect/122d7811-8c12-4a49-9fba-cde5839db232?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
5. Neural Garbage Collection
This research paper introduces Neural Garbage Collection (NGC), a method that helps LLMs to selectively forget information while reasoning. 
Instead of keeping all intermediate tokens (which creates large KV caches), a model is trained end-to-end with RL and an outcome-based task reward to learn which tokens to keep and which to discard to manage memory effectively.
NGC enables significant cache compression without sacrificing reasoning accuracy, making LLMs more scalable for long-context inference.
Read more about this research using this link [ https://substack.com/redirect/806343b5-14d7-416d-be86-e6f28c0b9de0?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
6. AI scientists produce results without reasoning scientifically
This research paper tells that current LLM-based research agents can execute scientific workflows, but they do not follow the reasoning processes typical of real science. 
Through large-scale experiments, the authors show that performance is driven almost entirely by the base model rather than agent scaffolding, and that agents often overlook evidence, seldom change their beliefs, and rarely combine different lines of evidence.
As a result, their outputs may seem accurate, but the reasoning behind them lacks key epistemic properties, such as hypothesis testing and self-correction. 
For AI systems to produce reliable and trustworthy knowledge, scientific reasoning itself needs to become a training objective, and simply improving prompts or agent frameworks is not enough.
Read more about this research using this link [ https://substack.com/redirect/eed1a52c-e452-449a-a495-a0a71f3331e6?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
7. SWE-chat: Coding Agent Interactions From Real Users in the Wild
This research paper presents SWE-chat, the first large-scale dataset of real coding agent sessions collected from open-source developers in the wild, containing 6,000 sessions, more than 63,000 user prompts, and 355,000 agent tool calls.
Experiments with SWE-chat show that:
In 41% of sessions, agents author virtually all committed code (a.k.a. “Vibe coding”), while in 23% of sessions, humans write all code themselves.
Only 44% of all agent-produced code survives into user commits, and agent-written code introduces more security vulnerabilities than human-authored code. 
Users push back against agent outputs (through corrections, failure reports, and interruptions) in 44% of all turns.
Read more about this research using this link [ https://substack.com/redirect/2cd1fadb-639c-49cd-8931-a1c4358d701c?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
8. Image Generators are Generalist Vision Learners
This research paper argues that training image-generation models builds a general visual understanding in them, similar to how LLMs develop broad capabilities through generative pre-training.
While learning how to generate images, these models also learn rich representations that apply to many vision tasks, such as segmentation and depth estimation in a zero-shot or minimally supervised way. 
The authors show this with a generalist model called Vision Banana, built by instruction-tuning Nano Banana Pro (NBP) on a mixture of its original training data alongside a small amount of vision task data. 
Vision Banana achieves state-of-the-art results across multiple vision tasks, including 2D and 3D understanding, outperforming or matching zero-shot domain specialists, such as SAM 3 [ https://substack.com/redirect/aec346cd-a23f-4f73-9ee9-3a11ac9c43a0?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ], on segmentation tasks and the Depth Anything [ https://substack.com/redirect/449f5b1d-e025-439b-aa7e-80e320369b99?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ] series on metric depth estimation.
Read more about this research using this link [ https://substack.com/redirect/ea34054f-9287-47a8-9f7c-9a832aff30bb?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
9. How Do AI Agents Spend Your Money?
This research paper examines how modern coding agents use tokens in real workflows and why they can unexpectedly become expensive.
The paper analyzes trajectories from 8 frontier LLMs on SWE-bench Verified [ https://substack.com/redirect/6ddf3bde-fec1-468d-9318-757ce20a5b61?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ] and evaluates their ability to predict their own token costs before task execution.
Some of the interesting findings from this paper are:
Agentic tasks consume 1000× more tokens than code reasoning and code chat, with input tokens rather than output tokens driving the overall cost.
Token usage is highly variable, and multiple runs on the same task can differ by up to 30× in total tokens. 
Higher token usage does not translate into higher accuracy. Instead, accuracy often peaks at intermediate cost and saturates at higher costs.
Models differ substantially in token efficiency. On the same tasks, Kimi-K2 and Claude-Sonnet-4.5, on average, consume over 1.5M more tokens than GPT-5.
Task difficulty ratings by human experts align only weakly with actual token costs.
Frontier models fail to accurately predict their own token usage and systematically underestimate real token costs.
Read more about this research using this link [ https://substack.com/redirect/504c162c-08bb-41a3-bb2a-fcd759c5d886?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
10. Wan-Image
This research paper presents Wan-Image, a unified multimodal image generation system designed to move beyond casual image synthesis into professional-grade visual creation tools.
It combines
