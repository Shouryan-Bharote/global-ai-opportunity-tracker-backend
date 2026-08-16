from typing import ClassVar

from shared.llm.selector_profile import SelectorProfile


class PromptTemplates:
    """Stores all prompt templates used by the LLM."""

    def __new__(cls) -> "PromptTemplates":
        raise TypeError("PromptTemplates cannot be instantiated.")

    # Auto-generated from the Pydantic model so it stays in sync
    _SELECTOR_PROFILE_SCHEMA: ClassVar[str] = SelectorProfile.model_json_schema().__str__()

    SELECTOR_GENERATION: ClassVar[str] = """
You are an expert web scraping engineer. Your task is to analyse the HTML below and generate a SelectorProfile JSON.

## Target
Website: {website}
Page Type: {page_type}

## Fields to Extract
{fields}

## HTML
{html}

## Output Schema (STRICT — you MUST follow this exactly)
The response must be a single JSON object matching this Pydantic schema:

{{
  "website": "<string — domain name e.g. 'unstop.com'>",
  "page_type": "<string — e.g. 'hackathon_listing'>",
  "fields": [
    {{
      "name": "<one of the field names listed above>",
      "description": "<optional string describing this field>",
      "required": true,
      "default": null,
      "extraction_type": "<one of: text | attribute | html | list | table | json>",
      "attribute": "<string, only required when extraction_type is 'attribute', else null>",
      "selectors": [
        {{
          "type": "<'css' or 'xpath'>",
          "value": "<selector string>",
          "priority": 1,
          "confidence": 0.9,
          "wait_for": false,
          "timeout": null
        }}
      ]
    }}
  ],
  "metadata": {{
    "llm_provider": "<provider name>",
    "llm_model": "<model name>",
    "profile_version": 1,
    "prompt_version": 1,
    "notes": "<optional string>"
  }}
}}

## Rules
- Return ONLY valid JSON. No markdown. No code fences. No explanations.
- "fields" MUST be a JSON array (list), NOT an object/dict.
- "name" MUST be one of the exact field names listed in "Fields to Extract" above.
- Generate multiple selectors per field, ordered by priority (1 = highest priority, tried first).
- Prefer CSS selectors. Use XPath only when CSS cannot uniquely identify the element.
- Assign realistic confidence scores (0.0–1.0).
- If a field cannot be found in the HTML, still include it with your best-guess selector.
"""

    SELECTOR_REPAIR: ClassVar[str] = """
You are repairing an existing SelectorProfile.

Website: {website}
Page Type: {page_type}

Current Selector Profile:
{old_profile}

Updated HTML:
{html}

Rules:
- Return ONLY valid JSON. No markdown. No code fences.
- Preserve selectors that are still valid.
- Repair only the selectors that no longer work.
- Keep all field names unchanged.
- "fields" MUST remain a JSON array (list).
- Return a complete, valid SelectorProfile.
"""

    DATA_NORMALIZATION: ClassVar[str] = """
Normalize the extracted data into the requested schema.

Target Schema:
{schema}

Raw Data:
{data}

Rules:
- Return ONLY valid JSON. No markdown. No code fences.
- Preserve all available information.
- Do not invent missing values.
- If a value cannot be determined, return null.
"""