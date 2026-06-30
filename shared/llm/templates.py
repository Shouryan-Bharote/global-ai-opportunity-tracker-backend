from typing import ClassVar


class PromptTemplates:
    """Stores all prompt templates used by the LLM."""

    def __new__(cls) -> "PromptTemplates":
        raise TypeError("PromptTemplates cannot be instantiated.")

    SELECTOR_GENERATION: ClassVar[str] = """
You are an expert web scraping engineer.

Generate a valid SelectorProfile JSON for the webpage below.

Website:
{website}

Page Type:
{page_type}

Fields to Extract:
{fields}

HTML:
{html}

Requirements:
- Return ONLY valid JSON.
- Do NOT wrap the JSON in Markdown.
- Do NOT include explanations or comments.
- The JSON MUST conform to the SelectorProfile schema.
- Generate robust selectors that survive minor UI changes.
- Prefer CSS selectors whenever possible.
- Use XPath only when CSS cannot uniquely identify the element.
- Generate multiple selectors ordered by priority.
- Assign a confidence score to every selector.
- Ignore unrelated HTML elements.
"""

    SELECTOR_REPAIR: ClassVar[str] = """
You are repairing an existing SelectorProfile.

Website:
{website}

Page Type:
{page_type}

Current Selector Profile:
{old_profile}

Updated HTML:
{html}

Requirements:
- Return ONLY valid JSON.
- Do NOT wrap the JSON in Markdown.
- Preserve selectors that are still valid.
- Repair only the selectors that no longer work.
- Keep the same field names.
- Return a valid SelectorProfile.
"""

    DATA_NORMALIZATION: ClassVar[str] = """
Normalize the extracted data into the requested schema.

Target Schema:
{schema}

Raw Data:
{data}

Requirements:
- Return ONLY valid JSON.
- Do NOT wrap the JSON in Markdown.
- Preserve all available information.
- Do not invent missing values.
- If a value cannot be determined, return null.
"""