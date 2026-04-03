import argparse
from datetime import datetime
from agents.market_analyst import MarketAnalyst
from agents.salary_appraiser import SalaryAppraiser
from agents.career_advisor import CareerAdvisor
from agents.critic import Critic
from utils import save_report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, help="Название специальности")
    args = parser.parse_args()

    try:
        # Агент 1: Аналитик рынка
        analyst = MarketAnalyst()
        result1 = analyst.run({"role": args.role})

        # Агент 2: Оценщик зарплат
        appraiser = SalaryAppraiser()
        result2 = appraiser.run(result1)

        # Агент 3: Карьерный советник
        advisor = CareerAdvisor()
        result3 = advisor.run({**result1, **result2})

        # Агент 4: Критик
        critic = Critic()
        result4 = critic.run({**result1, **result2, **result3})

        # Финальный отчёт
        final_report = {
            "generated_at": datetime.now().isoformat() + "Z",
            **result1,
            **result2,
            **result3,
            **result4}

        # Сохраняем
        save_report(final_report, args.role)

        print(f"\nОтчёты для '{args.role}' сохранены в папку reports/")

    except Exception as e:
        print(f"\nОшибка: {e}")
        raise


if __name__ == "__main__":
    main()
