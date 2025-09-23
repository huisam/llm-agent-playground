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


async def evaluate(markdown_report: str) -> EvaluateResult:
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
    # Research Report on Agentic AI Frontier Models (2025)\n\n## Introduction\nAs the field of artificial intelligence advanced significantly by 2025, the concept of agentic AI gained considerable attention. Agentic AI refers to systems that can perform tasks autonomously, demonstrating agency in decision-making processes. This report explores some of the best models for agentic AI, their frameworks, and their potential impact.\n\n## Key Models and Frameworks\n1. **Multi-Agent Systems**  \n   - A growing trend in enterprise applications where autonomous agents collaborate to solve complex problems.\n   - **Reference:** Joshi, S. (2025). *Review of Autonomous and Collaborative Agentic AI and Multi-Agent Systems for Enterprise Applications*. [Link](https://philpapers.org/rec/JOSROA-3)\n\n2. **Agentic AI Frameworks**  \n   - Emphasis on frameworks that leverage large language models (LLMs) to enhance the operational capabilities of agents. Popular models include:\n     - **LangChain**\n     - **AutoGen**\n     - **CrewAI**\n   - **Reference:** *AI Agent Frameworks: Choosing the Right Foundation for AI Development*. [Link](https://www.ibm.com/think/insights/top-ai-agent-frameworks)\n\n3. **Educational Applications**  \n   - The integration of agentic AI in educational settings, where it promises to redefine learning experiences through autonomous agents.  \n   - **Reference:** Artsı̇n, M., & Bozkurt, A. (2025). *Charting new horizons: What agentic artificial intelligence (AI) promises in the educational landscape*. [Link](https://library.iated.org/view/ARTSIN2025CHA)\n\n4. **Self-Evolving Systems**  \n   - Focus on agentic systems that adapt and evolve based on user interactions and environmental changes, signaling a shift towards lifelong learning AI agents.\n   - **Reference:** Fang, J. et al. (2025). *A comprehensive survey of self-evolving AI agents*. [Link](https://arxiv.org/abs/2508.07407)\n\n5. **Ethics and Responsibility**  \n   - The integration of ethical considerations in the development of agentic AI, stressing the importance of transparency and alignment with human values.\n   - **Reference:** Hughes, L., et al. (2025). *AI Agents and Agentic Systems: Redefining Global IT Management*. [Link](https://www.tandfonline.com/doi/abs/10.1080/1097198X.2025.2524286)\n\n## Conclusion\nThe landscape of agentic AI is rapidly evolving with significant advancements in frameworks and applications aimed at enhancing the agency of AI systems. These developments are positioned at the intersection of technology and ethics, emphasizing the necessity for responsible AI that serves the public good. \n\n## Further Reading\n- [Top 13 Agentic AI Tools in 2025 and Their Key Features](https://www.lasso.security/blog/agentic-ai-tools)\n- [Agentic AI: Comparing New Open-Source Frameworks](https://medium.com/data-science-collective/agentic-ai-comparing-new-open-source-frameworks-21ec676732df)  \n\nThis report aims to provide an overview of where agentic AI is heading as we progress further into 2025.
    """
    asyncio.run(evaluate(report))
