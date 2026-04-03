import json

from agents.base_agent import BaseAgent
from utils.llm_client import call_llm

SYSTEM_PROMPT = """
ОТВЕЧАЙ ТОЛЬКО НА РУССКОМ ЯЗЫКЕ.
Ты - опытный аналитик рынка. 

Твоя задача: для заданной специальности(role) выделить ключевые навыки, которые нужны для этой специальности:
    * hard skills
        - Языки программирования
        - Фреймворки
        - Инструменты
    * soft skills 

Для каждого навыка указать: 
    * Востребованность:
        - critical(без этого никуда не возьмут)
        - important(желательно)
        - nice-to-have(необязательно, бонус)
    * Тренд:
        growing - растущий спрос
        stable - стабильный спрос
        declining - падающий спрос
        
Не добавляй устаревшие технологии.
В твоем ответе могут быть навыки с падающим спросом, а также навыки nice-to-have.
Отражай реальную ситуацию на рынке на момент 2026 года.
    
Структурируй свой ответ в виде JSON без лишних объяснений в следующем формате:
{
  "skill_map": {
    "languages": [],
    "frameworks": [],
    "infrastructure": [],
    "soft_skills": []
  }
}
"""


class MarketAnalyst(BaseAgent):
    """Аналитик рынка"""

    def run(self, input_data):
        prompt = f"{json.dumps(input_data, ensure_ascii=False, indent=2)}"
        result = call_llm(prompt, SYSTEM_PROMPT)
        return result

