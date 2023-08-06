from pathlib import Path

import openai
from tqdm import tqdm

from api_key import openai_api_key
from odyssey import Section

openai.api_key = openai_api_key


sections = Section.cut_markdown(Path("notes/original.md").read_text())
prompt = "The following are some of my notes. Please re-organize them into coherent text I can use as a section of an essay. Only re-use my words, do not add any content. Keep citations in brackets, like so (Frame, 98-100). Do not structure your response as an entire essay - I will use it as part of a whole."

restructured_sections = []
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
    restructured_sections.append(
        Section(
            level=section.level,
            title=section.title.title(),
            text=response["choices"][0]["message"]["content"],
        )
    )

Path("notes/restructured.md").write_text(
    "\n\n".join(section.to_markdown() for section in restructured_sections)
)
