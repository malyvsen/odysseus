import re
from pathlib import Path

import openai

from api_key import openai_api_key

from .section import Section

openai.api_key = openai_api_key


original_sections = Section.cut_markdown(Path("notes/original.md").read_text())
restructured_sections = Section.cut_markdown(Path("notes/restructured.md").read_text())


def extract_references(section: Section):
    return set(re.findall("\(.+?\)", section.text))


extract_references(restructured_sections[5])
for original, restructured in zip(original_sections, restructured_sections):
    original_refs = extract_references(original)
    restructured_refs = extract_references(restructured)
    hallucinated_refs = restructured_refs - original_refs

    print(restructured.title + ": " + ", ".join(hallucinated_refs))
