import json

from agents.base_agent import BaseAgent
from utils.llm_client import call_llm

SYSTEM_PROMPT = """
Ты каерьерный советник.
Твоя задача: на основе переданных навыков(skill_map) и таблицы вилок по грейдам и регионам(salary_table) составить карьерный план.
В нем должны быть следующие поля:
learning_path: 3 фазы(Foundation - Practice - Portfolio) по 30 дней.
Каждая фаза: список тем(из skill_map), >= 2 ресурсов (название + тип: курс/книга/документация), ожидаемый milestone.
gap_analysis: quick_wins (можно закрыть за 2–4 нед.) и long_term (3+ месяца).
portfolio_project: конкретная идея с названием, описанием и списком используемых технологий из skill_map.
Структурируй свой ответ в виде JSON без лишних объяснений в формате:

{
  "learning_path": {
    {
      "phase": "Foundation",
      "topics": [],
      "resources": [
            {"title": , "type": },
            {"title": , "type": },
            ...
      ],
      "milestone":
    },
    {
      "phase": "Practice",
      "topics": [],
      "resources": [
            {"title": , "type": },
            {"title": , "type": },
            ...
      ],
      "milestone":
    },
    {
      "phase": "Portfolio",
      "topics": [],
      "resources": [
            {"title": , "type": },
            {"title": , "type": },
            ...
      ],
      "milestone":
    }
  },
  "gap_analysis": {
    "quick_wins": [],
    "long_term": []
  },
  "portfolio_project": {
    "name": ,
    "description": ,
    "skills_demonstrated": []
  }
}
"""


class CareerAdvisor(BaseAgent):
    """Карьерный советник"""

    def run(self, input_data):
        prompt = f"{json.dumps(input_data, ensure_ascii=False, indent=2)}"
        result = call_llm(prompt, SYSTEM_PROMPT)
        return result
