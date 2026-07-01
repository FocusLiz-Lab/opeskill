# Synthesis Rules

Do not average the experts into a generic answer. Preserve each module's advantage, then make one concrete recommendation.

## Process

1. State the selected primary module and supporting modules.
2. Pull the most relevant evidence, frameworks, or patterns from selected child skills. Prefer IMA evidence; use local atom fallback when IMA is unavailable, unauthorized, rate-limited, not found, or weak/no-hit.
3. Translate each module's view into the user's concrete context.
4. Resolve conflicts as tradeoffs.
5. Produce a single action plan.

## Conflict Handling

Common conflicts:

- `ahs` may prioritize revenue speed; `nrs` may warn against low-leverage work.
- `dks` may prefer a solo creator system; `lhs` may recommend team structure once complexity rises.
- `mrs` may push immediate action; `hbs` may identify biological constraints that make discipline unreliable.
- `rts` may focus on system rules; `nrs` may focus on detachment from outcomes.

When conflict appears, explain:

1. what each module optimizes for;
2. which optimization fits the user's stated goal;
3. what to do now;
4. what to revisit later.

## Evidence Discipline

- Retrieval is required before presenting an answer as source-grounded.
- Try the selected module's default IMA knowledge base first when `ima-skill` and access are available.
- If IMA fails, is not found, is rate-limited, or has weak/no hits, use the selected module's packaged `知识库/原子库/atoms.jsonl`.
- For commercialization, monetization, offer, pricing, acquisition, conversion, validation, or Chinese-market example requests, also retrieve local commercial case atoms from `知识库/商业案例库/commercial_atoms.jsonl` when bundled.
- A search result title match is not enough evidence. Use actual retrieved snippets, atom contents, or read the relevant local files when available.
- Do not answer from model memory or web search when selected expert sources are unavailable; label any fallback as general inference.
- If a child package is missing and IMA retrieval is also unavailable, clearly say which module is missing or weak and continue only where the remaining modules are useful.
- Do not invent quotes, episode titles, documents, or exact claims.
- Keep expert labels concise: `ahs 商业化`, `dks 一人公司`, etc.

## Final Answer Requirements

Every synthesized answer should include:

- direct answer;
- selected modules and reasons;
- integrated diagnosis;
- commercial case support when relevant;
- practical plan;
- risks or tradeoffs;
- next actions.

Avoid:

- seven disconnected summaries;
- motivational filler;
- equal weighting when one module clearly dominates;
- hiding uncertainty;
- giving medical, financial, or legal advice as professional advice.
