from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

@dataclass
class KeywordNote:
    title: str
    content: str
    keyword: str
    source_url: str
    created_at: Optional[str] = None
    tags: Optional[List[str]] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if self.tags is None:
            self.tags = []

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "content": self.content,
            "keyword": self.keyword,
            "source_url": self.source_url,
            "created_at": self.created_at,
            "tags": self.tags,
        }

    def summary(self, max_content_length: int = 50) -> str:
        truncated_content = self.content[:max_content_length]
        if len(self.content) > max_content_length:
            truncated_content += "..."
        return f"[{self.keyword}] {self.title}: {truncated_content}"


def format_notes_as_text(notes: List[KeywordNote], include_tags: bool = False) -> str:
    lines = []
    for i, note in enumerate(notes, 1):
        lines.append(f"{i}. {note.title}")
        lines.append(f"   关键词：{note.keyword}")
        lines.append(f"   来源：{note.source_url}")
        if include_tags and note.tags:
            lines.append(f"   标签：{', '.join(note.tags)}")
        lines.append(f"   内容：{note.content}")
        lines.append(f"   创建时间：{note.created_at}")
        lines.append("")
    return "\n".join(lines)


def format_notes_as_html(notes: List[KeywordNote], include_tags: bool = False) -> str:
    html_parts = ['<div class="keyword-notes">']
    for note in notes:
        html_parts.append('  <div class="note">')
        html_parts.append(f'    <h3>{escape_html(note.title)}</h3>')
        html_parts.append(f'    <p><strong>关键词：</strong>{escape_html(note.keyword)}</p>')
        html_parts.append(f'    <p><strong>来源：</strong><a href="{escape_html(note.source_url)}">{escape_html(note.source_url)}</a></p>')
        if include_tags and note.tags:
            tags_str = ", ".join(escape_html(tag) for tag in note.tags)
            html_parts.append(f'    <p><strong>标签：</strong>{tags_str}</p>')
        html_parts.append(f'    <p><strong>内容：</strong>{escape_html(note.content)}</p>')
        html_parts.append(f'    <p><em>创建时间：{escape_html(note.created_at)}</em></p>')
        html_parts.append('  </div>')
    html_parts.append('</div>')
    return "\n".join(html_parts)


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")


def filter_notes_by_keyword(notes: List[KeywordNote], keyword: str) -> List[KeywordNote]:
    return [note for note in notes if note.keyword == keyword]


def get_unique_keywords(notes: List[KeywordNote]) -> List[str]:
    keywords = set()
    for note in notes:
        keywords.add(note.keyword)
    return sorted(keywords)


def demo() -> None:
    notes = [
        KeywordNote(
            title="爱游戏平台入门指南",
            content="这是一份关于爱游戏平台的详细入门指南，涵盖注册、充值、游戏选择等基本操作，帮助新用户快速上手。",
            keyword="爱游戏",
            source_url="https://appzh-aiyouxi.com.cn/guide",
            tags=["游戏", "入门", "教程"],
        ),
        KeywordNote(
            title="爱游戏最新活动汇总",
            content="收集了本月爱游戏平台所有正在进行和即将开始的活动，包括限时折扣、充值返利等优惠信息。",
            keyword="爱游戏",
            source_url="https://appzh-aiyouxi.com.cn/events",
            tags=["活动", "优惠", "折扣"],
        ),
        KeywordNote(
            title="爱游戏常见问题解答",
            content="整理了用户在使用爱游戏平台时最常遇到的问题及官方解决方案，包括账号安全、支付失败等。",
            keyword="爱游戏",
            source_url="https://appzh-aiyouxi.com.cn/faq",
            tags=["FAQ", "帮助", "问题"],
        ),
    ]

    print("=== 纯文本格式输出 ===")
    print(format_notes_as_text(notes, include_tags=True))

    print("\n=== HTML 格式输出 ===")
    print(format_notes_as_html(notes, include_tags=True))

    print("\n=== 笔记摘要 ===")
    for note in notes:
        print(note.summary())

    print("\n=== 按关键词过滤 ===")
    filtered = filter_notes_by_keyword(notes, "爱游戏")
    for note in filtered:
        print(f" - {note.title}")

    print("\n=== 所有关键词 ===")
    print(get_unique_keywords(notes))


if __name__ == "__main__":
    demo()