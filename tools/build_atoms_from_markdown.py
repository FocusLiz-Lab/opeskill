#!/usr/bin/env python3
"""Build dbskill-style JSONL atom libraries from local Markdown archives.

This is a deterministic first-pass extractor. It does not pretend to be a
human-quality distillation model; it creates a large, structured atom base from
sentences and paragraphs that already carry usable claims, methods, examples,
or checklists. The output is suitable for lite skill packages and can be
improved later with manual curation or LLM-assisted rewriting.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


MAX_REASONABLE_YEAR = datetime.now().year + 1
YEAR_RE = re.compile(r"(20\d{2})[-_年/]?(\d{2})?[-_月/]?(\d{2})?")
YYMMDD_RE = re.compile(r"(?<!\d)(\d{2})(\d{2})(\d{2})(?!\d)")
TIME_RANGE_RE = re.compile(r"^\s*\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*")
TIME_RANGE_ANY_RE = re.compile(r"\[?\d{1,2}:\d{2}(?::\d{2})?\s*(?:→|-)\s*\d{1,2}:\d{2}(?::\d{2})?\]?")
TIMESTAMP_MARKER_RE = re.compile(r"\[?\d{1,2}:\d{2}(?::\d{2})?\]?\s*[-–—:]")
FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.S)
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\([^)]+\)")
URL_RE = re.compile(r"https?://\S+")
MULTISPACE_RE = re.compile(r"[ \t]+")
CHINESE_RE = re.compile(r"[\u4e00-\u9fff]")


@dataclass(frozen=True)
class ExpertConfig:
    skill: str
    source_expert: str
    default_skills: list[str]
    topic_keywords: dict[str, list[str]]


CONFIGS: dict[str, ExpertConfig] = {
    "ahs": ExpertConfig(
        "ahs",
        "Alex Hormozi",
        ["ahs"],
        {
            "offer": ["offer", "报价", "产品", "价值", "guarantee", "bonus", "risk reversal"],
            "pricing": ["price", "pricing", "价格", "定价", "profit", "margin", "利润"],
            "sales": ["sales", "close", "成交", "销售", "objection", "异议"],
            "leads": ["lead", "traffic", "获客", "线索", "funnel", "广告"],
            "scale": ["scale", "hiring", "team", "运营", "团队", "系统"],
            "mindset": ["belief", "mindset", "fear", "identity", "心态"],
        },
    ),
    "dks": ExpertConfig(
        "dks",
        "Dan Koe",
        ["dks"],
        {
            "one-person-business": ["one-person", "solo", "一人公司", "个人商业", "creator", "创作者"],
            "personal-brand": ["personal brand", "个人品牌", "定位", "niche", "利基"],
            "content": ["content", "内容", "writing", "写作", "newsletter", "推文"],
            "digital-product": ["digital product", "产品", "课程", "知识产品", "offer"],
            "audience": ["audience", "受众", "粉丝", "growth", "增长"],
            "ai-workflow": ["AI", "workflow", "自动化", "系统"],
        },
    ),
    "hbs": ExpertConfig(
        "hbs",
        "Huberman Lab",
        ["hbs"],
        {
            "sleep": ["sleep", "睡眠", "circadian", "昼夜", "light", "光照"],
            "focus": ["focus", "专注", "attention", "dopamine", "多巴胺"],
            "stress": ["stress", "压力", "breath", "呼吸", "anxiety", "焦虑"],
            "exercise": ["exercise", "training", "运动", "训练", "recovery", "恢复"],
            "nutrition": ["nutrition", "diet", "营养", "supplement", "补剂"],
            "learning": ["learning", "memory", "学习", "记忆"],
        },
    ),
    "lhs": ExpertConfig(
        "lhs",
        "Leila Hormozi",
        ["lhs"],
        {
            "hiring": ["hiring", "招聘", "人才", "interview"],
            "management": ["management", "管理", "delegation", "授权"],
            "leadership": ["leadership", "领导", "culture", "文化"],
            "operations": ["operations", "运营", "SOP", "process", "流程"],
            "accountability": ["accountability", "绩效", "问责", "metrics"],
        },
    ),
    "mrs": ExpertConfig(
        "mrs",
        "Mel Robbins",
        ["mrs"],
        {
            "action": ["action", "行动", "start", "开始", "5 second", "5秒"],
            "confidence": ["confidence", "自信", "self-doubt", "怀疑"],
            "fear": ["fear", "恐惧", "anxiety", "焦虑"],
            "habits": ["habit", "习惯", "routine", "日常"],
            "emotion": ["emotion", "情绪", "motivation", "动力"],
        },
    ),
    "nrs": ExpertConfig(
        "nrs",
        "Naval Ravikant",
        ["nrs"],
        {
            "wealth": ["wealth", "财富", "rich", "致富", "money"],
            "leverage": ["leverage", "杠杆", "code", "media", "capital"],
            "judgment": ["judgment", "判断", "decision", "决策"],
            "long-term": ["long-term", "长期", "compounding", "复利"],
            "freedom": ["freedom", "自由", "happiness", "幸福"],
            "specific-knowledge": ["specific knowledge", "特定知识", "skill"],
        },
    ),
    "rts": ExpertConfig(
        "rts",
        "Rayner Teo",
        ["rts"],
        {
            "trend": ["trend", "趋势", "trend following"],
            "price-action": ["price action", "价格行为", "support", "resistance", "支撑", "阻力"],
            "risk": ["risk", "风险", "stop loss", "止损", "position sizing", "仓位"],
            "backtesting": ["backtest", "回测", "journal", "复盘"],
            "psychology": ["psychology", "心理", "discipline", "纪律"],
        },
    ),
}


TYPE_KEYWORDS = {
    "method": ["how to", "step", "步骤", "方法", "流程", "系统", "framework", "原则"],
    "case": ["case", "example", "案例", "我", "客户", "学生", "公司", "business"],
    "anti-pattern": ["don't", "avoid", "mistake", "错误", "不要", "陷阱", "问题"],
    "checklist": ["checklist", "清单", "必须", "需要", "至少", "包含"],
    "principle": ["is", "means", "本质", "核心", "关键", "原则", "不是", "而是"],
}

SIGNAL_TERMS = [
    "because",
    "therefore",
    "if ",
    "when ",
    "how to",
    "step",
    "framework",
    "system",
    "principle",
    "mistake",
    "leverage",
    "offer",
    "audience",
    "content",
    "risk",
    "habit",
    "should",
    "must",
    "need",
    "can",
    "核心",
    "本质",
    "关键",
    "因为",
    "所以",
    "如果",
    "当你",
    "步骤",
    "方法",
    "系统",
    "原则",
    "不要",
    "必须",
    "需要",
    "可以",
    "不是",
    "而是",
]

NOISE_TERMS = [
    "download your free",
    "free trial",
    "subscribe",
    "link in",
    "check out",
    "welcome to",
    "happy monday",
    "hope this",
    "today's episode",
    "in this episode",
    "thank you for watching",
    "like and subscribe",
    "分类",
    "中英对照",
    "课程",
    "属性",
    "文稿",
    "talk then",
    "drop me an email",
    "good luck and good trading",
    "thanks for watching",
    "tomorrow we will",
    "your action step for today",
    "i hope that your",
    "i promise your",
    "here's my writing",
    "my original writing",
    "我的文字是",
    "你的内容",
]


def clean_markdown(text: str) -> str:
    text = FRONTMATTER_RE.sub("", text)
    text = MD_LINK_RE.sub(r"\1", text)
    text = TIME_RANGE_ANY_RE.sub("", text)
    text = TIMESTAMP_MARKER_RE.sub("", text)
    text = URL_RE.sub("", text)
    text = text.replace("\ufeff", "")
    text = re.sub(r"\[(音乐|掌声|笑声|music|applause|laughter)\]", "", text, flags=re.I)
    lines = []
    for line in text.splitlines():
        line = TIME_RANGE_RE.sub("", line)
        line = line.strip()
        if not line:
            lines.append("")
            continue
        if line.startswith(("![", "<!--")):
            continue
        lines.append(line)
    text = "\n".join(lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", text)
    return text


def split_units(text: str) -> list[str]:
    blocks = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    units: list[str] = []
    for block in blocks:
        if block.startswith("#"):
            continue
        block = re.sub(r"^[-*]\s+", "", block)
        block = re.sub(r"\s*\n\s*", " ", block)
        block = MULTISPACE_RE.sub(" ", block).strip()
        if is_good_unit(block):
            units.append(block)
            continue
        sentences = re.split(r"(?<=[。！？.!?])\s+", block)
        for sentence in sentences:
            sentence = sentence.strip()
            if is_good_unit(sentence):
                units.append(sentence)
    return units


def sentence_count(text: str) -> int:
    return max(1, len(re.findall(r"[。！？.!?]", text)))


def is_question_only(text: str) -> bool:
    stripped = text.strip()
    if not stripped.endswith(("?", "？")):
        return False
    return sentence_count(stripped) <= 1


def is_good_unit(text: str) -> bool:
    if len(text) < 32 or len(text) > 420:
        return False
    if text.count("|") > 4:
        return False
    if sum(ch.isalpha() or "\u4e00" <= ch <= "\u9fff" for ch in text) < 20:
        return False
    bad_fragments = [
        "source pdf:",
        "pdf text extraction",
        "subscribe",
        "copyright",
        "all rights reserved",
        "transcript",
        "字幕",
        "隐藏属性",
        "提示词搜集库",
        "方法论搜集",
        "字数",
        "属性 文稿",
        "here's an ai prompt",
        "role:",
        "[your content]",
        "社交媒体文案犀利评审员",
        "download ",
        "free scaling roadmap",
        "talk then",
        "tomorrow we will",
        "your action step for today",
        "drop me an email",
        "good luck and good trading",
        "thanks for watching",
        "here's my writing",
        "my original writing",
        "my writing is:",
        "我的文字是",
        "你的内容",
        "based on these, evaluate",
        "inside the first set of parentheses",
    ]
    lower = text.lower()
    if any(fragment in lower for fragment in bad_fragments):
        return False
    if TIMESTAMP_MARKER_RE.search(text):
        return False
    if re.fullmatch(r"(page|第)\s*\d+\s*(页)?", lower):
        return False
    if is_question_only(text):
        return False
    if text[0].islower() and not text.lower().startswith(("if ", "when ", "because ", "the ", "people ")):
        return False
    if lower.count(" um ") + lower.count(" uh ") + lower.count(" you know ") >= 2:
        return False
    if sum(1 for term in NOISE_TERMS if term in lower) >= 1:
        return False
    return True


def quality_score(text: str, config: ExpertConfig) -> int:
    lower = text.lower()
    score = 0
    score += min(len(text) // 35, 8)
    score += sum(3 for term in SIGNAL_TERMS if term.lower() in lower)
    score += sum(4 for keywords in config.topic_keywords.values() for keyword in keywords if keyword.lower() in lower)
    score += 8 if re.search(r"\d+[%倍xX]|\d+\s*(steps?|步骤|个|种|条)", text) else 0
    score += 8 if any(marker in text for marker in ["不是", "而是", "核心", "本质", "关键", "原则"]) else 0
    score += 5 if any(marker in lower for marker in ["if ", "when ", "because", "therefore"]) else 0
    score += 5 if "：" in text or ":" in text else 0

    score -= sum(10 for term in NOISE_TERMS if term in lower)
    score -= 8 if lower.count(" um ") or lower.count(" uh ") else 0
    score -= 6 if text.startswith(("欢迎", "Welcome", "Download", "Thanks", "Thank you")) else 0
    score -= 10 if any(term in lower for term in ["welcome back", "feel free to", "hope you enjoyed"]) else 0
    score -= 6 if sentence_count(text) == 1 and len(text) < 70 else 0
    score -= 10 if "general" in infer_topics(text, config) and score < 20 else 0
    score -= 8 if CHINESE_RE.search(text) and lower.count(" i ") >= 3 and "case" not in infer_type(text) else 0
    return score


def infer_date(path: Path, text: str) -> str:
    sample = f"{path.name}\n{text[:500]}"
    yymmdd = YYMMDD_RE.search(path.name)
    if yymmdd:
        yy, month, day = yymmdd.groups()
        year = 2000 + int(yy)
        try:
            if year > MAX_REASONABLE_YEAR:
                raise ValueError
            return datetime(year, int(month), int(day)).strftime("%Y-%m-%d")
        except ValueError:
            pass
    match = YEAR_RE.search(sample)
    if not match:
        return ""
    year = match.group(1)
    month = match.group(2) or "01"
    day = match.group(3) or "01"
    try:
        if int(year) > MAX_REASONABLE_YEAR:
            return ""
        return datetime(int(year), int(month), int(day)).strftime("%Y-%m-%d")
    except ValueError:
        return f"{year}-01-01"


def quarter_for(date: str) -> str:
    if not date:
        return "undated"
    year, month, _ = date.split("-")
    q = (int(month) - 1) // 3 + 1
    return f"{year}Q{q}"


def infer_topics(text: str, config: ExpertConfig) -> list[str]:
    lower = text.lower()
    topics = []
    for topic, keywords in config.topic_keywords.items():
        if any(keyword.lower() in lower for keyword in keywords):
            topics.append(topic)
    return topics[:6] or ["general"]


def infer_type(text: str) -> str:
    lower = text.lower()
    scores = {
        atom_type: sum(1 for keyword in keywords if keyword.lower() in lower)
        for atom_type, keywords in TYPE_KEYWORDS.items()
    }
    best_type, best_score = max(scores.items(), key=lambda item: item[1])
    return best_type if best_score else "insight"


def confidence_for(text: str) -> str:
    if any(marker in text for marker in ["步骤", "原则", "必须", "核心", "framework", "step"]):
        return "high"
    if len(text) > 80:
        return "medium"
    return "low"


def source_url(text: str) -> str:
    match = URL_RE.search(text)
    return match.group(0).strip('"\'）)') if match else ""


def simplify_bilingual_knowledge(text: str) -> str:
    if not CHINESE_RE.search(text):
        return text
    text = re.sub(r"[A-Za-z][A-Za-z0-9 ,.'\"!?;:()&/+\-]{18,}(?=[\u4e00-\u9fff])", "", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s+[A-Za-z][A-Za-z0-9 ,.'\"!?;:()&/+\-]{18,}", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", text)
    return text.strip(" -–—:：")


def make_knowledge(text: str) -> str:
    text = TIME_RANGE_ANY_RE.sub("", text)
    text = re.sub(r"\s+", " ", text).strip()
    sentences = [s.strip() for s in re.split(r"(?<=[。！？.!?])\s+", text) if s.strip()]
    scored: list[tuple[int, str]] = []
    has_chinese = bool(CHINESE_RE.search(text))
    for sentence in sentences:
        if len(sentence) < 24:
            continue
        if not is_good_unit(sentence) and len(sentence) < 120:
            continue
        score = sum(1 for term in SIGNAL_TERMS if term.lower() in sentence.lower())
        score += 2 if any(marker in sentence for marker in ["不是", "而是", "核心", "本质", "关键", "步骤", "方法"]) else 0
        score += 1 if re.search(r"\d+[%倍xX]|\d+\s*(steps?|步骤|个|种|条)", sentence) else 0
        score += min(len(CHINESE_RE.findall(sentence)) // 10, 8) if has_chinese else 0
        score -= min(len(re.findall(r"[A-Za-z]", sentence)) // 25, 6) if has_chinese else 0
        scored.append((score, sentence))
    if scored:
        best = max(scored, key=lambda item: (item[0], min(len(item[1]), 220)))[1]
    else:
        best = text
    best = simplify_bilingual_knowledge(best)
    if len(best) <= 220:
        return best
    clipped = best[:220]
    boundary = max(clipped.rfind("。"), clipped.rfind("."), clipped.rfind("；"), clipped.rfind(";"))
    if boundary > 60:
        return clipped[: boundary + 1]
    return clipped.rstrip(" ,，;；:：") + "..."


def stable_id(skill: str, path: Path, text: str) -> str:
    digest = hashlib.sha1(f"{path.as_posix()}\n{text}".encode("utf-8", "ignore")).hexdigest()[:12]
    return f"{skill}_{digest}"


def should_skip_path(path: Path, root: Path, excluded_path_parts: set[str]) -> bool:
    if not excluded_path_parts:
        return False
    relative = path.relative_to(root)
    parts = [part.lower() for part in relative.parts]
    return any(excluded.lower() in part for excluded in excluded_path_parts for part in parts)


def build_atoms(
    skill: str,
    roots: list[Path],
    output: Path,
    limit_per_file: int,
    excluded_path_parts: set[str] | None = None,
) -> list[dict]:
    config = CONFIGS[skill]
    atoms = []
    seen: set[str] = set()
    excluded_path_parts = excluded_path_parts or set()

    for root in roots:
        for path in sorted(root.rglob("*.md")):
            if not path.is_file():
                continue
            if should_skip_path(path, root, excluded_path_parts):
                continue
            raw = path.read_text(encoding="utf-8", errors="ignore")
            cleaned = clean_markdown(raw)
            units = split_units(cleaned)
            units = sorted(
                ((quality_score(unit, config), unit) for unit in units),
                key=lambda item: item[0],
                reverse=True,
            )
            units = [unit for score, unit in units if score >= 12]
            if limit_per_file > 0:
                units = units[:limit_per_file]
            for unit in units:
                key = hashlib.sha1(unit.lower().encode("utf-8", "ignore")).hexdigest()
                if key in seen:
                    continue
                seen.add(key)
                date = infer_date(path, raw)
                atoms.append(
                    {
                        "id": stable_id(skill, path, unit),
                        "knowledge": make_knowledge(unit),
                        "original": unit,
                        "source_expert": config.source_expert,
                        "source_path": str(path.relative_to(root)).replace("\\", "/"),
                        "url": source_url(raw),
                        "date": date,
                        "topics": infer_topics(unit, config),
                        "skills": config.default_skills,
                        "type": infer_type(unit),
                        "confidence": confidence_for(unit),
                    }
                )

    output.mkdir(parents=True, exist_ok=True)
    write_jsonl(output / "atoms.jsonl", atoms)
    write_readme(output / "README.md", skill, atoms)
    by_quarter: dict[str, list[dict]] = {}
    for atom in atoms:
        by_quarter.setdefault(quarter_for(atom.get("date", "")), []).append(atom)
    for quarter, quarter_atoms in sorted(by_quarter.items()):
        write_jsonl(output / f"atoms_{quarter}.jsonl", quarter_atoms)
    return atoms


def write_jsonl(path: Path, atoms: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for atom in atoms:
            handle.write(json.dumps(atom, ensure_ascii=False, separators=(",", ":")) + "\n")


def write_readme(path: Path, skill: str, atoms: list[dict]) -> None:
    type_counts: dict[str, int] = {}
    topic_counts: dict[str, int] = {}
    for atom in atoms:
        type_counts[atom["type"]] = type_counts.get(atom["type"], 0) + 1
        for topic in atom["topics"]:
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
    lines = [
        f"# {skill} 原子库",
        "",
        f"- atoms: {len(atoms)}",
        f"- generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
        "## type counts",
        "",
    ]
    lines.extend(f"- {k}: {v}" for k, v in sorted(type_counts.items()))
    lines.extend(["", "## top topics", ""])
    lines.extend(f"- {k}: {v}" for k, v in sorted(topic_counts.items(), key=lambda item: item[1], reverse=True)[:20])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", required=True, choices=sorted(CONFIGS))
    parser.add_argument("--root", action="append", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--limit-per-file", type=int, default=80)
    parser.add_argument("--exclude-path-part", action="append", default=[])
    args = parser.parse_args()

    roots = [Path(root).resolve() for root in args.root]
    atoms = build_atoms(
        args.skill,
        roots,
        Path(args.out).resolve(),
        args.limit_per_file,
        {part.lower() for part in args.exclude_path_part},
    )
    print(f"{args.skill}: wrote {len(atoms)} atoms to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
