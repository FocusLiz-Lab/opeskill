# Commercial Atom Schema

Each line in `commercial_atoms.jsonl` is one reusable commercial evidence atom.

- `atom_id`: stable short hash.
- `atom_type`: `commercial_case_atom` when concrete metrics are present; otherwise `commercial_method_atom`.
- `commercial_stages`: offer, pricing, acquisition, conversion, delivery, retention, scale, risk, validation, case_result.
- `platforms`: detected traffic or sales platform.
- `project_types`: detected business model or project category.
- `score`: heuristic relevance score.
- `title` / `heading` / `summary`: article context and atom summary.
- `metrics`: detected result numbers, revenue claims, audience numbers, or conversion-related numbers.
- `commercial_use`: how this atom can support commercialization reasoning.
- `evidence`: short source fragment.
- `source`: file path, URL, author, date, and engagement metadata.

Use this library to support `ahs` commercialization answers with local Chinese cases.

> 完整 commercial_atoms.jsonl 已内置在 Releases 的 opes-local.zip 中；代码区保留 samples 方便查看结构，避免接近 100MB 的单文件影响仓库浏览。

