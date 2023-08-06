from dataclasses import dataclass


@dataclass(frozen=True)
class Section:
    """A piece of a document."""

    title: str
    text: str

    @classmethod
    def cut_markdown(cls, markdown: str):
        result = []
        new_title = None
        new_text = None

        for line in markdown.split("\n"):
            if line.startswith("#"):
                if new_title is not None:
                    result.append(cls(new_title, new_text.strip()))
                new_title = line.replace("#", "").strip()
                new_text = ""
            else:
                new_text += line

        if new_title is not None:
            result.append(cls(new_title, new_text.strip()))
        return result
