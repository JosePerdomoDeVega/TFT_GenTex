import httpx
from domain.interfaces import TextGenerationAgent
from domain.settings import Settings

SYSTEM_PROMPT = "Eres un experto en análisis farmacéutico."


class AzureOpenAITextAgent(TextGenerationAgent):

    def __init__(self, settings: Settings):
        self._url = settings.chat_completions_url
        self._api_key = settings.azure_openai_api_key
        self._temperature = settings.llm_temperature
        self._max_tokens = settings.llm_max_tokens
        self._timeout = settings.llm_timeout

    async def write_report(self, prompt: str, data: object) -> str:
        headers = {"Content-Type": "application/json", "api-key": self._api_key}
        payload = {
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{prompt}\n{data}"},
            ],
            "temperature": self._temperature,
            "max_tokens": self._max_tokens,
        }
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            response = await client.post(self._url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]
