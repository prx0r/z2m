# 🗓️ This Week In AI Research (1-7 August 26)

**From:** "Dr. Ashish Bamania from Into AI" <intoai@substack.com>
**Date:** Thu, 13 Aug 2026 19:29:25 +0000
**Message ID:** 19ffc99e9102dfd2

---

View this post on the web at https://www.intoai.pub/p/this-week-in-ai-research-1-7-august

✨ This week’s newsletter is brought to you by Pathway [ https://substack.com/redirect/ca2d20aa-9682-4f4e-ac18-2413c2a73606?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ]. ✨ 
Researchers at Pathway, Bielik AI, and NYU just published a remarkable model called BDH-CQ, which breaks the previously reported cost-accuracy Pareto frontier in ARC-AGI-1 and sets a new state-of-the-art in benchmark cost efficiency.
BDH-CQ is a 150M-parameter reasoning model. 
It learns each new task from the examples it’s shown at inference time (in-context learning), which progressively updates a recurrent memory rather than filling a growing context window. It then solves a given query by iteratively reasoning in a structured, continuous latent state rather than using a verbalized chain of thought.
It achieves 29.5% pass@2 on ARC-AGI-1 at an inference cost of $0.0007 per task. This is less than 1/10th of a cent per task!
Although this is not the highest-accuracy result, its significance is clear when viewed alongside other LLMs’ results.
BDH-CQ is ~57x cheaper than GPT 5.6 Luna (Low), which scores 34.2% (only 4.7% higher) at $0.040. 
Even after OpenAI announced a recent 80% API price reduction, BDH-CQ is still ~11x cheaper than GPT 5.6 Luna (Low).
GLM 5 scores 44.7% (15.2% higher), but costs 243x more per task than BDH-CQ.
BDH-CQ is based on a post-Transformer sequence-model architecture called ‘Dragon Hatchling’ (BDH) [ https://substack.com/redirect/da5a0cc1-a958-4628-9a22-4adfbf7e776d?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
Early pretraining experiments show that it has Transformer-like scaling behavior across scales from 1B to 600B parameters while preserving its latent reasoning capabilities.
Read more about this research using these links: Hugging Face [ https://substack.com/redirect/59196a3e-422b-474a-b779-6ac0d34f51e0?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ] | ArXiv [ https://substack.com/redirect/21784fa9-844c-4509-97e8-9c04838803f2?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ] | Blog [ https://substack.com/redirect/e66a6386-be81-4cb5-abb6-0de78dbfdef8?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ]
1. Qwen3.8-Max 
Alibaba released its most capable model, Qwen3.8-Max, which is heavily focused on coding, autonomous agents, and long-horizon tasks. 
It outperforms previous Qwen models in agentic coding, computer use, research tasks, and co-working workflows.
The model has 2.4 trillion total parameters (95B active per token) and uses a Mixture-of-Experts architecture [ https://substack.com/redirect/45751c9d-4e83-4f6e-8705-e7459a65ca94?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
With this model, the team is, for the first time, open-sourcing the weights of a Qwen-Max-class model.
Read more about this release using this link [ https://substack.com/redirect/60891f2a-2047-446e-bdde-e0282e4d520d?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
2. On-Policy Self-Distillation without Any Supervision
U-OPSD (Unsupervised On-Policy Self-Distillation) is an algorithm that helps an LLM improve its reasoning without ground-truth answers, rewards, or a stronger teacher model. With U-OPSD, an LLM learns and improves using only its own generations, guided by internal consistency.
The process starts with the model generating multiple solutions for each problem and using a majority vote to form its own pseudo-answer, provided it meets a self-consistency threshold.
It then conditions the model’s distribution on the pseudo-solution and distills itself on the disagreeing completions, letting the model correct itself precisely where it is confidently wrong.
U-OPSD consistently outperforms the base models and matches or surpasses supervised methods with ground truth (GT), such as OPSD and GRPO.
Read more about this research using this link [ https://substack.com/redirect/29d699b2-10cd-4ca5-be36-ba9334170098?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
3. Leanstral
Leanstral is Mistral AI’s series of open-source generalist code-agent models for Lean 4.
The model has a Mixture-of-Experts architecture [ https://substack.com/redirect/45751c9d-4e83-4f6e-8705-e7459a65ca94?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ] with 119B total and 6B active parameters.
It runs within the open-source Mistral Vibe coding-agent harness rather than a specialized theorem-proving scaffold, and uses no test-time scaling method beyond context compaction.
Leanstral 1.5's performance is comparable to far larger, proprietary systems, as it saturates miniF2F [ https://substack.com/redirect/3c39ae72-3328-4d68-99d3-a130d3a82567?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ], solves 587/672 problems on PutnamBench [ https://substack.com/redirect/c3920899-2f60-421e-ad24-3be007fa5761?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ], and reaches a new state-of-the-art of 34% on FATE-X [ https://substack.com/redirect/74c54a90-6e7c-406a-b3dc-1b899c45cf31?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ] and 43.2% pass@8 on FLTEval [ https://substack.com/redirect/495ae808-dd97-419d-8beb-e44f46731826?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
Beyond competition mathematics, Leanstral can formally verify code and resolve bugs and issues in real-world repositories across graduate-level mathematics, mathematical finance, and code verification.
Read more about this research using this link [ https://substack.com/redirect/0ad7e04a-d35a-4b70-b7af-415d292417cf?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
4. The Beginning of ChatGPT Ads
This is the first empirical study of advertising content shown within ChatGPT during the early 2026 rollout.
Researchers created 91 simulated U.S. accounts and ran hundreds of prompts to collect ads from 191 unique advertisers across 127,801 conversations.
The results show that lower-income simulated accounts were significantly more likely to receive ads irrespective of their race.
Product/recommendation-style prompts were more likely to trigger advertising.
The ads were heavily skewed towards consumer goods and directed users to a specific advertiser rather than a particular product.
Ads were clearly marked “Sponsored” and separated from the LLM’s response text rather than embedded within it.
There were near-zero ad rates for medical conditions, mental health, and political prompts.
Read more about this research using this link [ https://substack.com/redirect/26f93c84-36b1-4f29-8a8d-785d1b7a3c9e?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
5. Ten Advances in Mathematics and Theoretical Computer Science
An internal OpenAI model, Astra [ https://substack.com/redirect/7c8517f9-eb66-4885-802a-885fe767eac5?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ], produced 10 research advances in mathematics and theoretical computer science. 
These results go beyond reproducing known proofs to include new resolutions, counterexamples, and improved bounds for many open problems in these subjects.
Read more about this research using this link [ https://substack.com/redirect/5c56ea6a-d1c7-4735-b14f-a20807c455f7?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
6. Maple-Preview
Maple-Preview is DeepGrove’s open-source ternary-weight reasoning model, designed to run efficiently on consumer hardware.
The model uses a Mixture-of-Experts architecture [ https://substack.com/redirect/45751c9d-4e83-4f6e-8705-e7459a65ca94?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ] with 256 experts (8 active) and has 20.2B total parameters (1.49B active).
The model has a 131k-token context window and is competitive with larger models at strong mathematical/general reasoning, including IMO-level problems.
It runs at 218 tokens/sec on an M4 Mac mini, which is 5-16× faster than efficient models like Gemma 4, Qwen3.5, and gpt-oss.
Read more about this release using this link [ https://substack.com/redirect/d4bf10b0-ed0b-4f53-8663-ac904825f771?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
7. Scaling Automated Post-Training with Locus
Locus is Intology’s automated research agent, extended to autonomously run the experiments needed to post-train other AI models.
PostTrainBench [ https://substack.com/redirect/7343f7cb-e291-4e7d-a7e3-8a5ca36b04c9?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ] is a benchmark where an agent is given a base model, a target benchmark, a single-H100 compute node, and internet access, and its task is to produce a post-trained version of the model optimized for the target benchmark.
Locus with Opus 5 has state-of-the-art post-training capabilities on PostTrainBench, where it outperforms every frontier-agent baseline.
On a larger compute variant of PostTrainBench, called PostTrainBench+, when given thousands of H100-hours, Locus continues improving while general-purpose coding agents plateau, and Locus-trained Qwen3-1.7B models collectively surpass Qwen’s official human-tuned checkpoint.
Beyond post-training, across live prize-money Kaggle competitions, Locus achieved an average rank beating 89.5% of human competitors.
Working with Bubble, a no-code app development platform, Locus discovered and executed a post-training recipe end-to-end, and the resulting model now serves millions of users at ~2.8× lower error, ~5.4× lower latency, and ~100× lower cost than the frontier API it replaced.
Read more about this release using this link [ https://substack.com/redirect/890e46d1-61ca-403f-85e5-743e779422a7?j=eyJ1IjoiNHpzZGw5In0.c6J1QH2h1tPto7ASDBIvgsssxOLIkxkwN3xCrpGPyhE ].
8. LLMRouter: Unified Infrastructure
