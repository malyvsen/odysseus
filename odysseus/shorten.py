import re
from pathlib import Path

import openai
from tqdm import tqdm

from api_key import openai_api_key

from .section import Section

openai.api_key = openai_api_key


sections = Section.cut_markdown(Path("notes/restructured.md").read_text())


def get_necessity(section: Section):
    return int(re.findall("\d+", section.text)[0])


prompt = (
    "The following message contains a section of an essay. "
    "Please help me shorten it by removing sentences which are not necessary for the overall meaning. "
    "Do not add any content, only remove parts. "
    "Keep references in the format they have, e.g. (Clarke, 19)."
)
shortened_sections = []
for section in tqdm(sections):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt},
            {"role": "user", "content": section.to_markdown()},
        ],
    )
    finish_reason = response["choices"][0]["finish_reason"]
    if finish_reason != "stop":
        raise ValueError(f"Unknown finish_reason: {finish_reason}")
    shortened_sections.append(
        Section(
            level=section.level,
            title=section.title.title(),
            text=response["choices"][0]["message"]["content"],
        )
    )

Path("notes/shortened.md").write_text(
    "\n\n".join(section.to_markdown() for section in shortened_sections)
)
