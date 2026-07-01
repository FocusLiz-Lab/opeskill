#!/usr/bin/env python
"""Build a commercial atom library from the local 生财有术 Markdown archive."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


STAGE_KEYWORDS: dict[str, list[str]] = {
    "offer": ["offer", "报价", "套餐", "方案", "包装", "卖点", "痛点", "刚需", "高客单", "产品阶梯", "价值"],
    "pricing": ["定价", "价格", "客单价", "涨价", "低价", "高价", "利润率", "毛利", "佣金"],
    "acquisition": ["获客", "引流", "流量", "投流", "私信", "加粉", "涨粉", "曝光", "搜索", "关键词", "SEO"],
    "conversion": ["成交", "转化", "下单", "付款", "逼单", "话术", "咨询", "转化率", "留资"],
    "delivery": ["交付", "履约", "服务", "SOP", "流程", "客服", "售后", "发货", "自动化"],
    "retention": ["复购", "留存", "私域", "社群", "微信", "朋友圈", "回购", "沉淀"],
    "scale": ["放大", "矩阵", "批量", "团队", "招人", "复制", "杠杆", "自动化", "规模"],
    "risk": ["风险", "违规", "封号", "踩坑", "失败", "亏", "避坑", "投诉", "成本"],
    "validation": ["MVP", "闭环", "测试", "试错", "验证", "跑通", "复盘", "对标", "模仿"],
    "case_result": ["月入", "日入", "年入", "GMV", "利润", "收入", "营收", "变现", "收益", "订单"],
}

PLATFORM_KEYWORDS: dict[str, list[str]] = {
    "小红书": ["小红书"],
    "视频号": ["视频号"],
    "抖音": ["抖音", "TikTok"],
    "闲鱼": ["闲鱼"],
    "公众号": ["公众号"],
    "淘宝/天猫": ["淘宝", "天猫"],
    "拼多多": ["拼多多"],
    "知乎": ["知乎"],
    "B站": ["B站", "哔哩哔哩"],
    "快手": ["快手"],
    "微信私域": ["微信", "私域", "朋友圈", "社群"],
    "独立站": ["独立站", "Shopify", "shopify"],
    "亚马逊": ["亚马逊", "Amazon", "amazon"],
    "YouTube": ["YouTube", "youtube"],
    "AI工具": ["AI", "ChatGPT", "Claude", "GPT", "AIGC", "数字人"],
}

PROJECT_KEYWORDS: dict[str, list[str]] = {
    "知识付费/资料": ["知识付费", "资料", "课程", "训练营", "社群", "咨询", "陪跑", "教程"],
    "直播带货": ["直播", "带货", "直播间", "主播", "场观", "GMV"],
    "电商": ["电商", "选品", "无货源", "店铺", "上架", "橱窗", "供应链"],
    "本地生活": ["本地生活", "同城", "探店", "门店", "到店", "团购"],
    "内容/IP": ["IP", "个人品牌", "内容", "短视频", "口播", "笔记", "爆款"],
    "服务/代运营": ["代运营", "服务商", "外包", "顾问", "咨询", "交付"],
    "出海": ["出海", "跨境", "海外", "独立站", "亚马逊", "TikTok"],
    "AI商业化": ["AI", "自动化", "数字人", "智能体", "提示词", "工作流"],
}

METRIC_PATTERNS = [
    re.compile(
        r"(?:月入|日入|年入|GMV|利润|收入|营收|收益|佣金|成交|销售额|流水|变现|客单价|订单|涨粉|粉丝|播放|阅读|曝光|场观|ROI|回本)"
        r"[^，。；\n]{0,18}\d+(?:\.\d+)?\s*(?:万|千|百|亿|w|W|k|K)?\+?\s*(?:元|块|美金|美元|GMV|利润|收入|营收|收益|佣金|单|订单|粉|粉丝|播放|阅读|曝光|场观|%|倍)?"
    ),
    re.compile(
        r"\d+(?:\.\d+)?\s*(?:万|千|百|亿|w|W|k|K)\+?\s*(?:元|块|美金|美元|GMV|利润|收入|营收|收益|佣金|单|订单|粉|粉丝|播放|阅读|曝光|场观|%|倍)?"
    ),
    re.compile(
        r"\d+(?:\.\d+)?\s*(?:元|块|美金|美元|GMV|利润|收入|营收|收益|佣金|单|订单|粉|粉丝|播放|阅读|曝光|场观|%|倍)"
    ),
]

FRONTMATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.S)
FIELD_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_]*):\s*"?(.+?)"?\s*$')
URL_RE = re.compile(r"https?://\S+")
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")

NOISE_LINE_PREFIXES = (
    "目录",
    "大家好",
    "各位圈友",
    "生财的小伙伴",
    "hello",
    "hi，大家好",
    "本文目录",
    "文章目录",
    "免责声明",
    "风险提示",
    "仅供参考",
    "欢迎",
    "感谢",
)

NOISE_FRAGMENTS = [
    "更多精彩内容",
    "加入生财",
    "点击链接",
    "原文链接",
    "阅读全文",
    "欢迎交流",
    "不构成投资建议",
    "还望指正",
    "鞠躬",
    "废话不多说",
    "接下来欢迎",
    "欢迎登场",
    "今天周五",
    "本期",
    "专栏嘉宾",
    "更多是偏「道」",
]

ACTION_TERMS = [
    "发现需求",
    "验证",
    "测试",
    "跑通",
    "引流",
    "获客",
    "私域",
    "成交",
    "转化",
    "定价",
    "客单价",
    "交付",
    "复购",
    "裂变",
    "投放",
    "选品",
    "上架",
    "关键词",
    "搜索",
    "付费",
    "利润",
    "收入",
    "营收",
    "GMV",
    "订单",
    "避坑",
    "SOP",
    "流程",
    "矩阵",
]

EMOJI_NUMBER_RE = re.compile(r"[0-9#]\ufe0f?\u20e3")


def default_root() -> Path:
    env_root = os.environ.get("SCYS_CORPUS_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / "_index.jsonl").exists():
            return parent
    return Path.cwd().resolve()


def read_index(root: Path) -> list[dict[str, Any]]:
    index_path = root / "_index.jsonl"
    rows: list[dict[str, Any]] = []
    with index_path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return rows


def parse_years(value: str | None) -> set[int] | None:
    if not value:
        return None
    out: set[int] = set()
    for part in value.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            out.update(range(int(start), int(end) + 1))
        else:
            out.add(int(part))
    return out


def rel_year(rel_file: str) -> int | None:
    head = rel_file.replace("/", "\\").split("\\", 1)[0]
    return int(head) if head.isdigit() else None


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    meta: dict[str, Any] = {}
    match = FRONTMATTER_RE.match(text)
    if not match:
        return meta, text
    for raw in match.group(1).splitlines():
        m = FIELD_RE.match(raw.strip())
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if value.endswith('"'):
            value = value[:-1]
        meta[key] = value
    return meta, text[match.end() :]


def clean_body(body: str) -> str:
    lines: list[str] = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("> 作者：") or stripped.startswith("> 发布时间：") or stripped.startswith("> 原文："):
            continue
        if stripped.startswith("![]("):
            continue
        if stripped.startswith(("---", "***")):
            continue
        if is_noise_line(stripped):
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = MD_LINK_RE.sub(r"\1", text)
    text = URL_RE.sub("", text)
    return text


def is_noise_line(text: str) -> bool:
    if not text:
        return False
    lowered = text.lower()
    if len(text) <= 20 and any(token in text for token in ["目录", "正文", "结语", "总结"]):
        return True
    if any(lowered.startswith(prefix) for prefix in NOISE_LINE_PREFIXES):
        return True
    if any(fragment.lower() in lowered for fragment in NOISE_FRAGMENTS):
        return True
    if re.fullmatch(r"[一二三四五六七八九十\d]+[、.．].{0,18}", text):
        return True
    if len(EMOJI_NUMBER_RE.findall(text)) >= 3:
        return True
    return False


def split_blocks(body: str) -> list[tuple[str, str]]:
    blocks: list[tuple[str, str]] = []
    heading = ""
    buffer: list[str] = []

    def flush() -> None:
        nonlocal buffer
        text = "\n".join(buffer).strip()
        buffer = []
        if len(text) >= 40:
            for unit in split_commercial_units(text):
                blocks.append((heading, unit))

    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            flush()
            heading = stripped.lstrip("#").strip()
            continue
        if not stripped:
            flush()
            continue
        buffer.append(stripped)
    flush()
    return blocks


def split_commercial_units(text: str) -> list[str]:
    text = normalize_space(text)
    sentences = [s.strip() for s in re.split(r"(?<=[。！？!?])\s*", text) if s.strip()]
    if len(sentences) <= 2:
        return [text] if is_candidate_unit(text) else []

    units: list[str] = []
    window: list[str] = []
    for sentence in sentences:
        if is_noise_line(sentence):
            continue
        window.append(sentence)
        joined = normalize_space("".join(window))
        if len(joined) >= 90 or len(window) >= 3:
            if is_candidate_unit(joined):
                units.append(joined)
            window = []
    if window:
        joined = normalize_space("".join(window))
        if is_candidate_unit(joined):
            units.append(joined)
    return units


def is_candidate_unit(text: str) -> bool:
    if len(text) < 45 or len(text) > 520:
        return False
    if is_noise_line(text):
        return False
    lowered = text.lower()
    if any(fragment.lower() in lowered for fragment in NOISE_FRAGMENTS):
        return False
    if text.count("http") >= 2:
        return False
    if len(re.findall(r"\d+[、.．]", text)) >= 8:
        return False
    if len(EMOJI_NUMBER_RE.findall(text)) >= 3:
        return False
    labels = find_labels(text, STAGE_KEYWORDS)
    has_metric = bool(metrics(text))
    has_action = any(term.lower() in lowered for term in ACTION_TERMS)
    return bool(labels) and (has_metric or has_action or len(labels) >= 2)


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def find_labels(text: str, mapping: dict[str, list[str]]) -> list[str]:
    labels = []
    lowered = text.lower()
    for label, words in mapping.items():
        for word in words:
            if word.lower() in lowered:
                labels.append(label)
                break
    return labels


def metrics(text: str) -> list[str]:
    found: list[str] = []
    for pattern in METRIC_PATTERNS:
        for m in pattern.finditer(text):
            value = normalize_space(m.group(0))
            if is_bad_metric(value):
                continue
            if len(value) >= 2 and value not in found:
                found.append(value)
            if len(found) >= 8:
                return found
    return found


def is_bad_metric(value: str) -> bool:
    if len(value) > 42:
        return True
    if re.fullmatch(r"\d+[、.．]\s*[\u4e00-\u9fffA-Za-z]{1,12}", value):
        return True
    if re.fullmatch(r"(?:成交|收益|变现|收入|利润|订单|粉丝)?\s*\d+[、.．]?", value):
        return True
    if any(token in value for token in ["规则", "设置", "简介", "目录", "阶段"]):
        return True
    if re.search(r"[：:]\s*[\u4e00-\u9fff「《]", value) and re.search(r"\s\d+$", value):
        return True
    return False


def atom_score(text: str, title: str, likes: int, favorites: int, reads: int) -> int:
    stages = find_labels(text, STAGE_KEYWORDS)
    plats = find_labels(text, PLATFORM_KEYWORDS)
    projects = find_labels(text, PROJECT_KEYWORDS)
    metric_count = len(metrics(text))
    action_bonus = min(sum(1 for term in ACTION_TERMS if term.lower() in text.lower()), 5)
    title_bonus = 0
    title_text = f"{title} {text[:80]}"
    if any(word in title_text for word in ["月入", "日入", "年入", "GMV", "利润", "变现", "获客", "成交", "高客单", "复盘"]):
        title_bonus += 2
    social = 0
    if likes >= 100:
        social += 1
    if favorites >= 20:
        social += 1
    if reads >= 10000:
        social += 1
    noise_penalty = 4 if any(fragment.lower() in text.lower() for fragment in NOISE_FRAGMENTS) else 0
    return len(stages) * 2 + len(plats) + len(projects) + metric_count * 3 + action_bonus + title_bonus + social - noise_penalty


def parse_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def summarize_atom(text: str, max_len: int = 180) -> str:
    text = normalize_space(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text))
    return text if len(text) <= max_len else text[: max_len - 1] + "…"


def distilled_summary(text: str, max_len: int = 150) -> str:
    text = summarize_atom(text, 420)
    sentences = [s.strip() for s in re.split(r"(?<=[。！？!?])\s*", text) if s.strip()]
    if not sentences:
        return summarize_atom(text, max_len)
    scored: list[tuple[int, str]] = []
    for sentence in sentences:
        score = len(metrics(sentence)) * 4
        score += len(find_labels(sentence, STAGE_KEYWORDS)) * 2
        score += min(sum(1 for term in ACTION_TERMS if term.lower() in sentence.lower()), 4)
        score -= 5 if is_noise_line(sentence) else 0
        if len(sentence) < 25:
            score -= 2
        scored.append((score, sentence))
    best = max(scored, key=lambda item: (item[0], min(len(item[1]), max_len)))[1]
    return summarize_atom(best, max_len)


def build_atom(
    *,
    root: Path,
    rel: str,
    path: Path,
    meta: dict[str, Any],
    title: str,
    idx: int,
    heading: str,
    text: str,
    score: int,
) -> dict[str, Any]:
    atom_id = hashlib.sha1(f"{rel}#{idx}#{text[:80]}".encode("utf-8", errors="ignore")).hexdigest()[:16]
    stages = find_labels(text, STAGE_KEYWORDS)
    platforms = find_labels(text, PLATFORM_KEYWORDS)
    projects = find_labels(text, PROJECT_KEYWORDS)
    nums = metrics(text)
    return {
        "id": atom_id,
        "knowledge": distilled_summary(text),
        "original": summarize_atom(text, 360),
        "url": meta.get("source_url"),
        "date": normalize_date(meta.get("date")),
        "topics": commercial_topics(stages, platforms, projects),
        "skills": ["opes", "commercial-cases"],
        "type": "case" if nums else "method",
        "confidence": "high" if nums and score >= 10 else "medium",
        "commercial_stages": stages,
        "platforms": platforms,
        "project_types": projects,
        "score": score,
        "title": title,
        "heading": heading,
        "metrics": nums,
        "commercial_use": commercial_use(stages, platforms, projects),
        "source": {
            "file": rel,
            "author": meta.get("author"),
            "entity_id": meta.get("entity_id"),
            "likes": parse_int(meta.get("likes")),
            "coins": parse_int(meta.get("coins")),
            "favorites": parse_int(meta.get("favorites")),
            "reads": parse_int(meta.get("reads")),
        },
    }


def normalize_date(value: Any) -> str:
    if not value:
        return ""
    text = str(value)
    for fmt in ("%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    match = re.search(r"(20\d{2})[-/](\d{1,2})[-/](\d{1,2})", text)
    if match:
        year, month, day = match.groups()
        return f"{year}-{int(month):02d}-{int(day):02d}"
    return ""


def quarter_for(date: str) -> str:
    if not date:
        return "undated"
    year, month, _ = date.split("-")
    quarter = (int(month) - 1) // 3 + 1
    return f"{year}Q{quarter}"


def commercial_topics(stages: list[str], platforms: list[str], projects: list[str]) -> list[str]:
    topics = []
    topics.extend(stages[:4])
    topics.extend(platforms[:2])
    topics.extend(projects[:2])
    return topics or ["commercial-case"]


def commercial_use(stages: list[str], platforms: list[str], projects: list[str]) -> str:
    stage_text = "、".join(stages[:4]) if stages else "商业化判断"
    platform_text = "、".join(platforms[:3]) if platforms else "泛平台"
    project_text = "、".join(projects[:3]) if projects else "项目案例"
    return f"用于支撑 {platform_text} / {project_text} 的 {stage_text} 案例或方法。"


def iter_articles(root: Path, years: set[int] | None, limit: int | None):
    count = 0
    for item in read_index(root):
        rel = item.get("file")
        if not rel or not str(rel).lower().endswith(".md"):
            continue
        year = rel_year(rel)
        if years and year not in years:
            continue
        path = root / rel
        if not path.exists():
            continue
        yield item, rel, path
        count += 1
        if limit and count >= limit:
            break


def write_schema(out_dir: Path) -> None:
    schema = """# 商业案例原子库

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
"""
    (out_dir / "README.md").write_text(schema, encoding="utf-8")


def write_quarter_files(out_dir: Path, atoms: list[dict[str, Any]]) -> None:
    buckets: dict[str, list[dict[str, Any]]] = {}
    for atom in atoms:
        buckets.setdefault(quarter_for(atom.get("date", "")), []).append(atom)
    for quarter, rows in sorted(buckets.items()):
        with (out_dir / f"atoms_{quarter}.jsonl").open("w", encoding="utf-8", newline="\n") as f:
            for atom in rows:
                f.write(json.dumps(atom, ensure_ascii=False, separators=(",", ":")) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(default_root()), help="生财文章根目录")
    parser.add_argument("--out", default=None, help="输出目录，默认 <root>/_atoms")
    parser.add_argument("--years", default=None, help="年份，如 2023-2026 或 2024,2025")
    parser.add_argument("--limit", type=int, default=None, help="最多处理文章数，用于试跑")
    parser.add_argument("--min-score", type=int, default=6, help="原子最低分")
    parser.add_argument("--max-atoms-per-article", type=int, default=0, help="每篇最多原子数，0 表示不限制")
    parser.add_argument("--progress-every", type=int, default=5000)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    out_dir = Path(args.out).resolve() if args.out else root / "_atoms"
    out_dir.mkdir(parents=True, exist_ok=True)
    years = parse_years(args.years)

    jsonl_path = out_dir / "atoms.jsonl"
    csv_path = out_dir / "commercial_atoms_index.csv"
    stats_path = out_dir / "commercial_atoms_stats.json"
    sample_path = out_dir / "commercial_atoms_samples.md"

    total_articles = 0
    total_atoms = 0
    counters: dict[str, Counter[str]] = {
        "stages": Counter(),
        "platforms": Counter(),
        "project_types": Counter(),
        "years": Counter(),
    }
    top_atoms: list[dict[str, Any]] = []
    all_atoms: list[dict[str, Any]] = []

    with jsonl_path.open("w", encoding="utf-8", newline="\n") as jf, csv_path.open("w", encoding="utf-8-sig", newline="") as cf:
        writer = csv.DictWriter(
            cf,
            fieldnames=[
                "atom_id",
                "score",
                "atom_type",
                "title",
                "commercial_stages",
                "platforms",
                "project_types",
                "metrics",
                "file",
                "source_url",
            ],
        )
        writer.writeheader()

        for item, rel, path in iter_articles(root, years, args.limit):
            total_articles += 1
            try:
                raw = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            meta, body = parse_frontmatter(raw)
            meta = {**item, **meta}
            title = str(meta.get("title") or item.get("title") or path.stem)
            body = clean_body(body)
            blocks = split_blocks(body)
            article_atoms: list[dict[str, Any]] = []
            likes = parse_int(meta.get("likes"))
            favorites = parse_int(meta.get("favorites"))
            reads = parse_int(meta.get("reads"))

            for idx, (heading, block) in enumerate(blocks):
                text = f"{title}。{heading}。{block}" if heading else f"{title}。{block}"
                score = atom_score(text, title, likes, favorites, reads)
                if score < args.min_score:
                    continue
                article_atoms.append(
                    build_atom(
                        root=root,
                        rel=rel,
                        path=path,
                        meta=meta,
                        title=title,
                        idx=idx,
                        heading=heading,
                        text=block,
                        score=score,
                    )
                )

            article_atoms.sort(key=lambda x: x["score"], reverse=True)
            if args.max_atoms_per_article > 0:
                article_atoms = article_atoms[: args.max_atoms_per_article]

            for atom in article_atoms:
                jf.write(json.dumps(atom, ensure_ascii=False) + "\n")
                writer.writerow(
                    {
                        "atom_id": atom["id"],
                        "score": atom["score"],
                        "atom_type": "commercial_case_atom" if atom["type"] == "case" else "commercial_method_atom",
                        "title": atom["title"],
                        "commercial_stages": "|".join(atom["commercial_stages"]),
                        "platforms": "|".join(atom["platforms"]),
                        "project_types": "|".join(atom["project_types"]),
                        "metrics": "|".join(atom["metrics"]),
                        "file": atom["source"]["file"],
                        "source_url": atom["source"]["source_url"],
                    }
                )
                all_atoms.append(atom)
                total_atoms += 1
                for key in ("commercial_stages", "platforms", "project_types"):
                    counter_name = "stages" if key == "commercial_stages" else key
                    counters[counter_name].update(atom[key])
                year = rel_year(atom["source"]["file"])
                if year:
                    counters["years"][str(year)] += 1
                top_atoms.append(atom)
                top_atoms.sort(key=lambda x: x["score"], reverse=True)
                top_atoms = top_atoms[:40]

            if args.progress_every and total_articles % args.progress_every == 0:
                print(f"processed={total_articles} atoms={total_atoms}", file=sys.stderr)

    stats = {
        "root": str(root),
        "articles_processed": total_articles,
        "atoms_generated": total_atoms,
        "min_score": args.min_score,
        "max_atoms_per_article": args.max_atoms_per_article,
        "years_filter": sorted(years) if years else None,
        "stage_counts": counters["stages"].most_common(),
        "platform_counts": counters["platforms"].most_common(),
        "project_type_counts": counters["project_types"].most_common(),
        "year_counts": counters["years"].most_common(),
        "outputs": {
            "jsonl": str(jsonl_path),
            "csv": str(csv_path),
            "stats": str(stats_path),
            "samples": str(sample_path),
        },
    }
    stats_path.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    write_schema(out_dir)
    write_quarter_files(out_dir, all_atoms)

    lines = ["# Commercial Atom Samples", ""]
    for atom in top_atoms[:30]:
        lines.append(f"## {atom['score']} | {atom['title']}")
        lines.append("")
        lines.append(f"- id: `{atom['id']}`")
        lines.append(f"- stages: {', '.join(atom['commercial_stages'])}")
        lines.append(f"- platforms: {', '.join(atom['platforms'])}")
        lines.append(f"- projects: {', '.join(atom['project_types'])}")
        if atom["metrics"]:
            lines.append(f"- metrics: {', '.join(atom['metrics'])}")
        lines.append(f"- source: `{atom['source']['file']}`")
        lines.append("")
        lines.append(atom["original"])
        lines.append("")
    sample_path.write_text("\n".join(lines), encoding="utf-8")

    print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
