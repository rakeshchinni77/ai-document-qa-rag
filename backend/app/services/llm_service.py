import requests
from backend.app.core.config import settings
from backend.app.core.exceptions import DownstreamLLMError
from backend.app.utils.logging import get_logger

logger = get_logger(__name__)

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER.lower()
        self.groq_api_key = settings.GROQ_API_KEY
        self.openai_api_key = settings.LLM_API_KEY
        self.groq_model = settings.GROQ_MODEL

    def generate_answer(self, prompt: str) -> str:
        api_key = self.groq_api_key or self.openai_api_key
        
        # Check if API key is valid or placeholder
        if not api_key or api_key == "gsk_demo_key_placeholder" or "your_secret" in api_key:
            logger.warning("No valid LLM API key found in configuration. Operating in deterministic offline fallback mode.")
            return self._extract_fallback_answer_from_prompt(prompt)

        try:
            if self.provider == "groq" or self.groq_api_key:
                url = "https://api.groq.com/openai/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": self.groq_model,
                    "messages": [
                        {"role": "system", "content": "You are a precise, context-grounded Document Question Answering assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2,
                    "max_tokens": 1024
                }
            else:
                url = "https://api.openai.com/v1/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.openai_api_key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "gpt-3.5-turbo",
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.2
                }

            response = requests.post(url, json=payload, headers=headers, timeout=15)
            
            if response.status_code != 200:
                logger.error(f"LLM Provider API returned error status {response.status_code}: {response.text}")
                # Fallback gracefully or raise downstream exception
                if response.status_code in (401, 403, 429, 500, 502, 503):
                    raise DownstreamLLMError(f"LLM service communication failure (HTTP {response.status_code}).")
                raise DownstreamLLMError(f"LLM API Error: {response.text}")

            data = response.json()
            answer = data["choices"][0]["message"]["content"].strip()
            return answer

        except DownstreamLLMError:
            raise
        except requests.RequestException as exc:
            logger.error(f"Network exception communicating with LLM API: {str(exc)}")
            raise DownstreamLLMError(f"Network error connecting to LLM API: {str(exc)}")
        except Exception as exc:
            logger.error(f"Unexpected error in LLM Service: {str(exc)}")
            raise DownstreamLLMError(f"Unexpected error generating answer: {str(exc)}")

    def _extract_fallback_answer_from_prompt(self, prompt: str) -> str:
        """Fallback offline answer generator when external API key is not configured."""
        context_start = prompt.find("Context Information:")
        question_start = prompt.find("Question:")
        
        if context_start != -1 and question_start != -1:
            context = prompt[context_start:question_start]
            question = prompt[question_start:].replace("Question:", "").strip()
            
            # Simple keyword match offline summary
            lines = [line.strip() for line in context.split("\n") if line.strip() and not line.startswith("-")]
            if lines:
                summary = " ".join(lines[:3])
                return f"Based on the provided context: {summary}"
        
        return "I cannot find the answer in the provided documents."
