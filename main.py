import argparse
from datetime import datetime
from agents.market_analyst import MarketAnalyst
from agents.salary_appraiser import SalaryAppraiser
from agents.career_advisor import CareerAdvisor
from agents.critic import Critic
from utils import save_report
from utils.logger import setup_logger, get_logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, help="Название специальности")
    args = parser.parse_args()
    report_dir = f"reports/{args.role}"  # Получаем директорию, куда сохраним результат
    setup_logger(report_dir)  # Настраиваем логгер
    logger = get_logger()

    try:
        # Агент 1: Аналитик рынка
        analyst = MarketAnalyst()
        logger.info("Main: Обращение к MarketAnalyst")
        result1 = analyst.run({"role": args.role})
        logger.info("Main: MarketAnalyst закончил работу")

        # Агент 2: Оценщик зарплат
        appraiser = SalaryAppraiser()
        logger.info("Main: Обращение к SalaryAppraiser")
        result2 = appraiser.run(result1)
        logger.info("Main: SalaryAppraiser закончил работу")

        # Агент 3: Карьерный советник
        advisor = CareerAdvisor()
        logger.info("Main: Обращение к CareerAdvisor")
        result3 = advisor.run({**result1, **result2})
        logger.info("Main: CareerAdvisor закончил работу")

        # Агент 4: Критик
        critic = Critic()
        logger.info("Main: Обращение к Critic")
        result4 = critic.run({**result1, **result2, **result3})
        logger.info("Main: Critic закончил работу")

        # Финальный отчёт
        logger.info("Main: Собираем результаты работы агентов")
        final_report = {
            "generated_at": datetime.now().isoformat() + "Z",
            **result1,
            **result2,
            **result3,
            **result4}

        # Сохраняем отчеты
        logger.info(f"Main: Сохраняем отчеты в директорию {report_dir}")
        save_report(final_report, args.role, report_dir)

        logger.info(f"Main: Отчеты для '{args.role}' сохранены в директорию {report_dir}")

    except Exception as e:
        logger.error(f"Ошибка: {e}")
        raise


if __name__ == "__main__":
    main()
