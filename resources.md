# Resources Catalog

## Summary
This document catalogs all resources gathered for the research project, including papers, datasets, and code repositories.

## Papers
Total papers downloaded: 8

| Title | Authors | Year | File | Key Info |
|-------|---------|------|------|----------|
| Large Language Models Can Be Lazy Learners: Analyze Shortcuts in In-Context Learning | Tang et al. | 2023 | `papers/2023_lazy_llm_learners_acl.pdf` | Shows shortcut reliance in ICL; reverse scaling effect. |
| Self-Refine: Iterative Refinement with Self-Feedback | Madaan et al. | 2023 | `papers/2023_self_refine.pdf` | Iterative self-feedback improves outputs across tasks. |
| Reflexion: Language Agents with Verbal Reinforcement Learning | Shinn et al. | 2023 | `papers/2023_reflexion.pdf` | Reflection memory improves agents. |
| Self-Consistency Improves Chain of Thought Reasoning in Language Models | Wang et al. | 2022 | `papers/2022_self_consistency_cot.pdf` | Multi-sample consistency baseline. |
| Least-to-Most Prompting Enables Complex Reasoning in LLMs | Zhou et al. | 2022 | `papers/2022_least_to_most_prompting.pdf` | Decomposition prompting baseline. |
| Chain-of-Thought Prompting Elicits Reasoning in LLMs | Wei et al. | 2022 | `papers/2022_chain_of_thought_prompting.pdf` | Foundational reasoning prompting. |
| Self-Critique Prompting with LLMs for Inductive Instructions | Wang et al. | 2023 | `papers/2023_self_critique_prompting.pdf` | Critic-style prompting. |
| Self-Evaluation Guided Beam Search for Reasoning | Xie et al. | 2023 | `papers/2023_self_evaluation_guided_beam.pdf` | Self-evaluation guided decoding. |

See `papers/README.md` for detailed descriptions.

## Datasets
Total datasets downloaded: 2

| Name | Source | Size | Task | Location | Notes |
|------|--------|------|------|----------|-------|
| GSM8K | HuggingFace | 7,473 train / 1,319 test | Math reasoning | `datasets/gsm8k/` | Classic reasoning benchmark. |
| AI2 ARC (ARC-Challenge) | HuggingFace | 1,119 train / 299 val / 1,172 test | Science QA | `datasets/ai2_arc/` | Reasoning + multiple choice. |

See `datasets/README.md` for detailed descriptions and download instructions.

## Code Repositories
Total repositories cloned: 2

| Name | URL | Purpose | Location | Notes |
|------|-----|---------|----------|-------|
| self-refine | https://github.com/madaan/self-refine | Self-feedback refinement | `code/self-refine/` | Contains GSM8K and other task scripts. |
| reflexion | https://github.com/noahshinn/reflexion | Reflection for agents | `code/reflexion/` | HotPotQA/AlfWorld runs, requires API key. |

See `code/README.md` for detailed descriptions.

## Resource Gathering Notes

### Search Strategy
- Started with paper-finder (service unavailable), then manually searched arXiv and ACL Anthology.
- Prioritized papers on self-critique, self-refinement, and reasoning prompting.

### Selection Criteria
- Direct relevance to “lazy” LLM behavior or effort-inducing prompting.
- Publicly available PDFs and (ideally) code.
- Benchmarks commonly used for reasoning evaluation.

### Challenges Encountered
- Paper-finder service not running locally.
- HuggingFace dataset `strategyqa` unavailable via default name; used ARC-Challenge instead.

### Gaps and Workarounds
- No direct dataset specifically labeled “lazy LLM” behavior; used reasoning datasets as proxies.

## Recommendations for Experiment Design

1. **Primary dataset(s)**: GSM8K and ARC-Challenge for reasoning + robustness checks.
2. **Baseline methods**: direct generation, CoT, self-consistency, least-to-most prompting.
3. **Evaluation metrics**: accuracy / exact match; optional LLM-judge preference for output quality.
4. **Code to adapt/reuse**: Self-Refine for critique/refinement loop; Reflexion for reflection memory baselines.

## Experiment Log (Executed)

- **Date**: 2026-01-31
- **Model**: gpt-4.1 (OpenAI API)
- **Datasets**: GSM8K test (n=50), ARC-Challenge test (n=50)
- **Conditions**: direct-neutral, CoT, harsh-critic, harsh-critic (low budget), rude-direct, polite-direct
- **Outputs**: `results/model_outputs/raw_outputs.jsonl`, `results/evaluations/accuracy_summary.csv`
