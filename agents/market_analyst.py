import json

from agents.base_agent import BaseAgent
from utils.llm_client import call_llm

SYSTEM_PROMPT = """
Ты - аналитик рынка. 
Твоя задача: для заданной специальности выделить hard skills (языки, фреймворки, инструменты) и soft skills.
Для каждого навыка указать: востребованность (critical / important / nice-to-have) и тренд (growing / stable /
declining).
Структурируй свой ответ в виде JSON без лишних объяснений в следующем формате:
{
  "skill_map": {
    "languages": [],
    "frameworks": [],
    "infrastructure": [],
    "soft_skills": []
  }
}
Навыки должны быть актуальными на 2026 год.
"""


class MarketAnalyst(BaseAgent):
    """Аналитик рынка"""

    def run(self, input_data):
        prompt = f"{json.dumps(input_data, ensure_ascii=False, indent=2)}"
        result = call_llm(prompt, SYSTEM_PROMPT)
        return result

