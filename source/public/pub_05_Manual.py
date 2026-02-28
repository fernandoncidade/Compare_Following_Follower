from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple


@dataclass(frozen=True)
class ManualDetails:
    summary: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()


@dataclass(frozen=True)
class ManualSection:
    id: str
    title: str
    paragraphs: tuple[str, ...] = ()
    bullets: tuple[str, ...] = ()
    details: tuple[ManualDetails, ...] = ()


@dataclass(frozen=True)
class ManualBlock:
    kind: str
    text: str = ""
    section_id: str | None = None

def normalize_language(lang: str | None) -> str:
    if not lang:
        return "pt_BR"

    v = lang.strip().replace("-", "_").lower()
    if v in ("pt_br", "pt"):
        return "pt_BR"

    if v in ("en_us", "en"):
        return "en_US"

    return "pt_BR"

def get_manual_title(lang: str | None = None) -> str:
    lang = normalize_language(lang)
    return "Manual de Utilização — Compare - Following and Follower" if lang == "pt_BR" else "User Manual — Compare - Following and Follower"

def get_manual_document(lang: str | None = None) -> tuple[ManualSection, ...]:
    lang = normalize_language(lang)

    try:
        from source.public.manual import DOC_PT_BR, DOC_EN_US
        if lang == "en_US":
            return getattr(DOC_EN_US, "_DOC_EN_US", tuple())

        return getattr(DOC_PT_BR, "_DOC_PT_BR", tuple())

    except Exception:
        return tuple()

def get_manual_blocks(lang: str | None = None) -> tuple[tuple[ManualBlock, ...], Tuple[str, ...]]:
    lang = normalize_language(lang)
    sections = get_manual_document(lang)

    blocks: list[ManualBlock] = []
    order: list[str] = []

    def blank() -> None:
        blocks.append(ManualBlock(kind="blank"))

    def line(text: str) -> None:
        blocks.append(ManualBlock(kind="line", text=text))

    def toc_title(text: str) -> None:
        blocks.append(ManualBlock(kind="toc_title", text=text))

    def toc_item(text: str, section_id: str) -> None:
        blocks.append(ManualBlock(kind="toc_item", text=text, section_id=section_id))

    def section_title(text: str, section_id: str) -> None:
        blocks.append(ManualBlock(kind="section_title", text=text, section_id=section_id))

    def detail_title(text: str) -> None:
        blocks.append(ManualBlock(kind="detail_title", text=text))

    def paragraph(text: str) -> None:
        blocks.append(ManualBlock(kind="paragraph", text=text))

    def bullet(text: str) -> None:
        blocks.append(ManualBlock(kind="bullet", text=text))

    def divider() -> None:
        blocks.append(ManualBlock(kind="divider", text="-" * 60))

    line(get_manual_title(lang))
    line("=" * len(get_manual_title(lang)))
    blank()

    if lang == "pt_BR":
        paragraph(
            "Este manual descreve como operar o aplicativo Compare - Following and Follower (modo de uso), cobrindo funcionalidades, atalhos, "
            "fluxo de trabalho sugerido, solução de problemas e informações sobre persistência de dados."
        )
        paragraph("Não é um guia de desenvolvimento.")
        blank()
        toc_title("Indice")

    else:
        paragraph(
            "This manual describes how to operate the Compare - Following and Follower application (user guide), covering features, shortcuts, "
            "suggested workflows, troubleshooting, and information about data persistence."
        )
        paragraph("It is not a development guide.")
        blank()
        toc_title("Table of Contents")

    for idx, s in enumerate(sections, start=1):
        toc_item(f"{idx}. {s.title}", section_id=s.id)

    blank()
    divider()
    blank()

    for s in sections:
        order.append(s.id)

        section_title(s.title, section_id=s.id)
        blank()

        for p in s.paragraphs:
            paragraph(p)
            blank()

        for b in s.bullets:
            bullet(b)

        if s.bullets:
            blank()

        for d in s.details:
            detail_title(d.summary)
            blank()

            for p in d.paragraphs:
                paragraph(p)
                blank()

            for b in d.bullets:
                bullet(b)

            if d.bullets:
                blank()

        divider()
        blank()

    return tuple(blocks), tuple(order)

def get_manual_text(lang: str | None = None) -> str:
    text, _positions, _order = get_manual_text_with_positions(lang)
    return text

def get_manual_text_with_positions(lang: str | None = None,) -> tuple[str, Dict[str, int], Tuple[str, ...]]:
    lang = normalize_language(lang)
    sections = get_manual_document(lang)

    lines: list[str] = []
    positions: dict[str, int] = {}
    order: list[str] = []

    def add_line(s: str = "") -> None:
        lines.append(s)

    def current_offset() -> int:
        return sum(len(l) + 1 for l in lines)

    title = get_manual_title(lang)
    add_line(title)
    add_line("=" * len(title))
    add_line()

    if lang == "pt_BR":
        add_line(
            "Este manual descreve como operar o aplicativo Compare - Following and Follower (modo de uso), cobrindo funcionalidades, atalhos, "
            "fluxo de trabalho sugerido, solução de problemas e informações sobre persistência de dados."
        )
        add_line("Não é um guia de desenvolvimento.")
        add_line()
        add_line("Indice")
        add_line("----------")

    else:
        add_line(
            "This manual describes how to operate the Compare - Following and Follower application (user guide), covering features, shortcuts, "
            "suggested workflows, troubleshooting, and information about data persistence."
        )
        add_line("It is not a development guide.")
        add_line()
        add_line("Table of Contents")
        add_line("------------------------------")

    for idx, s in enumerate(sections, start=1):
        add_line(f"{idx}. {s.title}")

    add_line()
    add_line("-" * 60)
    add_line()

    for s in sections:
        positions[s.id] = current_offset()
        order.append(s.id)

        add_line(s.title)
        add_line("-" * len(s.title))
        add_line()

        for p in s.paragraphs:
            add_line(p)
            add_line()

        for b in s.bullets:
            add_line(f"    - {b}")

        if s.bullets:
            add_line()

        for d in s.details:
            add_line(d.summary)
            add_line("." * len(d.summary))
            add_line()

            for p in d.paragraphs:
                add_line(p)
                add_line()

            for b in d.bullets:
                add_line(f"    - {b}")

            if d.bullets:
                add_line()

        add_line("-" * 60)
        add_line()

    return "\n".join(lines), positions, tuple(order)
