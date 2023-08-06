from dataclasses import dataclass
from functools import cached_property


@dataclass(frozen=True)
class Section:
    """A piece of a document."""

    level: int
    title: str
    text: str

    @classmethod
    def cut_markdown(cls, markdown: str):
        result = []
        new_section = None

        for line in markdown.split("\n"):
            if line.startswith("#"):
                if new_section is not None:
                    result.append(cls.from_markdown(new_section))
                new_section = ""
            new_section += line + "\n"

        if new_section is not None:
            result.append(cls.from_markdown(new_section))
        return result

    @classmethod
    def from_markdown(cls, markdown: str):
        if not markdown.startswith("#"):
            raise ValueError("Section must start with a heading")
        lines = markdown.split("\n")
        if any(line.startswith("#") for line in lines[1:]):
            raise ValueError("Section may contain only one heading")
        return cls(
            level=lines[0].count("#"),
            title=lines[0].replace("#", "").strip(),
            text="\n".join(line.strip() for line in lines[1:]).strip(),
        )

    @cached_property
    def word_count(self):
        return self.title.count(" ") + self.text.count(" ")

    def to_markdown(self):
        return "#" * self.level + " " + self.title + "\n\n" + self.text
