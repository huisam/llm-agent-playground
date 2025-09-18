import asyncio

from agents import Agent, Runner, trace
from dotenv import load_dotenv
from pydantic import BaseModel

from log.logger import get_logger

load_dotenv(override=True)
logger = get_logger()


class EvaluateResult(BaseModel):
    passed: bool
    result: str
    reasoning: str


async def evaluate(markdown_report: str) -> str:
    with trace("Evaluate agent"):
        agent = Agent(
            name="Evaluate Agent",
            instructions="""
            You are a expert evaluator to evaluate the markdown report text. 
            Check whether the report has a clear introduction, methodology, findings, and conclusion.
            Assess the logical flow of sections and whether arguments are well connected.
            Identify ambiguous or confusing statements.
            Provide the result is passed or not, and give me the result in 2~3 sentence and write about the reason to reasoning
            """,
            output_type=EvaluateResult,
            model="gpt-4o-mini"
        )
        result = await Runner.run(agent, markdown_report)
        logger.info(result.final_output)
        return result.final_output


if __name__ == '__main__':
    report = """
    ## Weather Forecast for Seoul Tomorrow\n\n- **Date:** Tomorrow\n- **Temperature:** Low 64°F (approx. 18°C)\n- **Feels Like:** 59°F (approx. 15°C)\n- **Conditions:** Cloudy with periods of rain\n- **Wind:** Northeast at 5 mph\n- **Humidity:** High, contributing to a cooler feel\n\nFor more details, please check the full forecast at [AccuWeather](https://www.accuweather.com/en/kr/seoul/226081/weather-forecast/226081) or [Weather.com](https://weather.com/weather/tenday/l/3bee6716da8e17a02afd2a6ab2d45025839d2616b95bb871cbea1cfc6f15018e).
    """
    asyncio.run(evaluate(report))
