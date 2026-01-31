# Literature Review: Fixing Lazy LLMs

## Review Scope

### Research Question
How can prompting strategies (e.g., harsh critique roles, response budget control, iterative self-feedback) reduce “lazy” low-effort LLM outputs and improve reasoning quality?

### Inclusion Criteria
- Focus on LLM prompting or test-time interventions that increase effort, reasoning depth, or self-critique
- Empirical evaluation on reasoning or instruction-following tasks
- Recent work (2022–2024), plus key foundational baselines

### Exclusion Criteria
- Training-only interventions without test-time prompting relevance
- Non-LLM-specific evaluation without a clear link to response quality or effort

### Time Frame
2022–2024 (with one foundational work as needed)

### Sources
- arXiv
- ACL Anthology
- Papers with Code / GitHub
- HuggingFace papers pages

## Search Log

| Date | Query | Source | Results | Notes |
|------|-------|--------|---------|-------|
| 2026-01-31 | “LLM lazy learners shortcuts in-context learning” | ACL Anthology / arXiv | 1 | Found direct “lazy learners” paper (ACL Findings 2023). |
| 2026-01-31 | “self-refine iterative self-feedback LLM” | arXiv | 1 | Core iterative self-critique method. |
| 2026-01-31 | “self-critique prompting LLM” | arXiv | 1 | Critic-style prompting. |
| 2026-01-31 | “self-evaluation guided beam search reasoning” | arXiv | 1 | Decoding guided by self-evaluation. |
| 2026-01-31 | “chain-of-thought prompting” | arXiv | 1 | Foundational baseline. |
| 2026-01-31 | “least-to-most prompting” | arXiv | 1 | Structured prompting baseline. |
| 2026-01-31 | “self-consistency chain-of-thought” | arXiv | 1 | Multi-sample consistency baseline. |
| 2026-01-31 | “Reflexion verbal reinforcement learning” | arXiv | 1 | Self-reflection baseline. |

## Screening Results

| Paper | Title Screen | Abstract Screen | Full-Text | Notes |
|-------|-------------|-----------------|-----------|-------|
| Lazy Learners (ACL 2023) | Include | Include | Include | Direct evidence of shortcut reliance in ICL. |
| Self-Refine (2023) | Include | Include | Include | Iterative self-critique/refinement. |
| Reflexion (2023) | Include | Include | Partial | Relevant self-reflection loop for agents. |
| Self-Consistency CoT (2022) | Include | Include | Partial | Reasoning baseline. |
| Least-to-Most (2022) | Include | Include | Partial | Structured reasoning prompting baseline. |
| Chain-of-Thought (2022) | Include | Include | Partial | Foundational baseline. |
| Self-Critique Prompting (2023) | Include | Include | Partial | Critic prompting baseline. |
| Self-Evaluation Guided Beam (2023) | Include | Include | Partial | Decoding guided by self-evaluation. |

## Paper Summaries

### Paper 1: Large Language Models Can Be Lazy Learners: Analyze Shortcuts in In-Context Learning
- **Authors**: Ruixiang Tang, Dehan Kong, Longtao Huang, Hui Xue
- **Year**: 2023
- **Source**: Findings of ACL
- **Key Contribution**: Shows LLMs exploit shortcut triggers in prompts, leading to performance collapse on anti-shortcut test sets.
- **Methodology**: Inject shortcut triggers (words, signs, styles) into ICL prompts and evaluate on classification + extraction tasks.
- **Datasets Used**: SST-2, MR, CR, OLID; ATIS; MIT Movies (slot filling).
- **Results**: Large drops on anti-shortcut sets; larger models show bigger drops (reverse scaling). Trigger insertion alone doesn’t explain drops.
- **Code Available**: Not in paper PDF.
- **Relevance to Our Research**: Direct evidence of “lazy” shortcut reliance and a benchmark paradigm for detecting it.

### Paper 2: Self-Refine: Iterative Refinement with Self-Feedback
- **Authors**: Aman Madaan, Niket Tandon, Prakhar Gupta, et al.
- **Year**: 2023
- **Source**: arXiv
- **Key Contribution**: Introduces iterative self-feedback/refinement loop that improves outputs without extra training.
- **Methodology**: Generate → Feedback → Refine with the same LLM; iterate up to 4 rounds; few-shot prompts for feedback and refinement.
- **Datasets Used**: Dialogue response generation, code optimization, code readability, math reasoning (GSM8K), sentiment reversal, acronym generation, constrained generation.
- **Results**: Consistent improvements across tasks; largest gains in preference-based tasks; modest gains for math unless external error signal exists.
- **Code Available**: Yes (selfrefine.info / GitHub).
- **Relevance to Our Research**: Concrete intervention to reduce lazy first-pass outputs by forcing critique + revision.

### Paper 3: Reflexion: Language Agents with Verbal Reinforcement Learning
- **Authors**: Noah Shinn et al.
- **Year**: 2023
- **Source**: arXiv / NeurIPS
- **Key Contribution**: Adds self-reflection memory to improve agents over trials.
- **Methodology**: Agents keep verbal reflections to guide future attempts; evaluated on reasoning (HotPotQA), decision-making (AlfWorld), programming.
- **Datasets Used**: HotPotQA, AlfWorld, programming tasks.
- **Results**: Reflection improves success rates across domains.
- **Code Available**: Yes.
- **Relevance**: Reflection-based feedback loops relate to “harsh critic” prompting.

### Paper 4: Self-Consistency Improves Chain of Thought Reasoning in Language Models
- **Authors**: Xuezhi Wang et al.
- **Year**: 2022
- **Source**: arXiv
- **Key Contribution**: Sample multiple CoT reasoning paths and choose the most consistent answer.
- **Methodology**: Generate multiple reasoning traces; majority vote / consistency selection.
- **Datasets Used**: GSM8K, SVAMP, AQuA, ARC, StrategyQA, and others.
- **Results**: Substantial improvements over single CoT.
- **Relevance**: A baseline for reducing lazy single-pass reasoning.

### Paper 5: Least-to-Most Prompting Enables Complex Reasoning in Large Language Models
- **Authors**: Denny Zhou et al.
- **Year**: 2022
- **Source**: arXiv
- **Key Contribution**: Decomposes complex problems into subproblems in prompts.
- **Methodology**: First prompt elicits subquestions, then solves sequentially.
- **Datasets Used**: GSM8K, SCAN, compositional reasoning tasks.
- **Results**: Improves performance on complex reasoning.
- **Relevance**: Structured prompting to increase effortful reasoning.

### Paper 6: Chain-of-Thought Prompting Elicits Reasoning in Large Language Models
- **Authors**: Jason Wei et al.
- **Year**: 2022
- **Source**: arXiv
- **Key Contribution**: Demonstrates that explicit reasoning chains improve performance.
- **Methodology**: Few-shot prompts with reasoning steps.
- **Datasets Used**: GSM8K, MultiArith, CommonsenseQA, StrategyQA, others.
- **Results**: Strong improvements for sufficiently large models.
- **Relevance**: Foundational baseline for effortful outputs.

### Paper 7: Self-Critique Prompting with Large Language Models for Inductive Instructions
- **Authors**: Rui Wang et al.
- **Year**: 2023
- **Source**: arXiv
- **Key Contribution**: Critic-style prompting improves instruction induction.
- **Methodology**: Model generates candidate, critiques, then revises.
- **Datasets Used**: Instruction induction and related tasks.
- **Results**: Improves performance vs. direct generation.
- **Relevance**: Aligns with “harsh critic” prompting hypothesis.

### Paper 8: Self-Evaluation Guided Beam Search for Reasoning
- **Authors**: Yuxi Xie et al.
- **Year**: 2023
- **Source**: arXiv
- **Key Contribution**: Uses self-evaluation signals to guide decoding in reasoning.
- **Methodology**: Beam search guided by self-evaluation of candidate reasoning paths.
- **Datasets Used**: Math and reasoning benchmarks (e.g., GSM8K, MATH).
- **Results**: Improves reasoning accuracy compared to standard decoding.
- **Relevance**: Decoding-time control can mitigate lazy single-pass outputs.

## Common Methodologies
- **Self-critique / self-refine loops**: Self-Refine, Self-Critique Prompting, Reflexion.
- **Structured reasoning prompts**: Chain-of-Thought, Least-to-Most.
- **Multi-sample selection**: Self-Consistency; self-evaluation guided decoding.

## Standard Baselines
- Direct generation with same model (no critique)
- Chain-of-Thought prompting
- Self-Consistency (multi-sample majority)
- Least-to-Most prompting

## Evaluation Metrics
- **Accuracy / exact match**: GSM8K, ARC-Challenge
- **Solve rate**: math reasoning tasks
- **Human preference**: dialogue, readability, sentiment reversal
- **Model-judged preference**: GPT-4/LLM-as-judge for some tasks

## Datasets in the Literature
- **GSM8K**: math word problems
- **ARC-Challenge**: multiple-choice science reasoning
- **HotPotQA**: multi-hop QA (Reflexion)
- **AlfWorld**: embodied decision-making (Reflexion)

## Gaps and Opportunities
- Limited work directly tests “lazy” shortcut reliance vs. “effort” prompting.
- Few controlled studies on response budget constraints (length/steps) vs. quality.
- Need standardized benchmarks for “effort” or “critique strength.”

## Recommendations for Our Experiment
- **Recommended datasets**: GSM8K, ARC-Challenge (both already downloaded).
- **Recommended baselines**: direct generation, CoT, self-consistency, least-to-most.
- **Recommended metrics**: accuracy / exact match; optional LLM-judge preference.
- **Methodological considerations**:
  - Treat “harsh critic” prompting as a controllable intervention.
  - Vary response budget (max tokens / steps) to test effort-quality tradeoff.
  - Use anti-shortcut evaluation (from Lazy Learners) as robustness check.
