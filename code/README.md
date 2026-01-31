# Cloned Repositories

## Repo 1: self-refine
- URL: https://github.com/madaan/self-refine
- Purpose: Implements Self-Refine (iterative self-feedback + refinement) across multiple tasks.
- Location: `code/self-refine/`
- Key files:
  - `src/acronym/run.py` (acronym generation demo)
  - `src/responsegen/run.py` (dialogue response generation)
  - `src/gsm/run.py` (GSM8K task)
- Notes: Uses `prompt-lib` for LLM calls; requires API access for GPT models.

## Repo 2: reflexion
- URL: https://github.com/noahshinn/reflexion
- Purpose: Implements Reflexion (self-reflection for agents) across reasoning, decision-making, and programming.
- Location: `code/reflexion/`
- Key files:
  - `hotpotqa_runs/` (reasoning experiments)
  - `alfworld_runs/` (decision-making experiments)
  - `programming_runs/` (program synthesis/LeetCode experiments)
- Notes: Requires OpenAI API key and additional dependencies; some experiments are costly.
