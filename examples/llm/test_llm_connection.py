"""
LLM Connectivity Smoke Test.

Run with:
    poetry run python examples/llm/test_llm_connection.py
"""

import asyncio

from shared.llm.client import LiteLLMClient
from shared.llm.models import LLMProvider, LLMRequest, LLMTask
from shared.llm.providers import Providers


async def test_provider(provider: LLMProvider) -> None:
    """Test connectivity for a single LLM provider."""
    if not Providers.has_api_key(provider):
        print(f"[SKIP] {provider.value}: No API key configured in .env")
        return

    model = Providers.default_model(provider)
    client = LiteLLMClient()

    request = LLMRequest(
        task=LLMTask.DATA_NORMALIZATION,
        prompt="Reply with exactly this text and nothing else: LLM connection successful.",
        provider=provider,
        model=model,
        temperature=0.0,
        max_tokens=20,
    )

    try:
        response = await client.generate(request)
        tokens = response.usage.total_tokens if response.usage else "N/A"
        print(f"[OK]   {provider.value} — {model}")
        print(f"       Response : {response.content.strip()}")
        print(f"       Tokens   : {tokens}")
        print(f"       Time     : {response.response_time:.2f}s")
    except Exception as exc:
        print(f"[FAIL] {provider.value} — {exc}")


async def main() -> None:
    """Run connectivity test for all configured providers."""
    print("=" * 50)
    print("  LLM Connectivity Smoke Test")
    print("=" * 50)
    print()

    for provider in LLMProvider:
        await test_provider(provider)
        print()

    print("Done.")


if __name__ == "__main__":
    asyncio.run(main())
