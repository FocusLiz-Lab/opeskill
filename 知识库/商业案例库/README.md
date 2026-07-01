# 商业案例原子库

每个 `atoms*.jsonl` 文件都是一行一条 JSON 记录，采用 dbskill 风格 `{id, knowledge, original, ...}` 结构。

- `id`: stable short hash.
- `knowledge`: distilled commercial takeaway.
- `original`: source evidence fragment.
- `url`: original article URL when available.
- `date`: source publish date.
- `topics`: commercial stage, platform, and project tags.
- `skills`: related skill entry names.
- `type`: `case` when concrete metrics are present; otherwise `method`.
- `confidence`: high / medium.
- `commercial_stages`: offer, pricing, acquisition, conversion, delivery, retention, scale, risk, validation, case_result.
- `platforms`: detected traffic or sales platform.
- `project_types`: detected business model or project category.
- `score`: heuristic relevance score.
- `title` / `heading`: article context.
- `metrics`: detected result numbers, revenue claims, audience numbers, or conversion-related numbers.
- `commercial_use`: how this atom can support commercialization reasoning.
- `source`: file path, author, entity id, and engagement metadata.

`atoms.jsonl` is the full library. `atoms_YYYYQn.jsonl` files are quarterly splits for lighter browsing and import.
