import asyncio
import logging
import os

from agents import Agent, Runner, ModelSettings, trace
from agents.mcp import MCPServerStdioParams, MCPServerStdio
from openai.types import Reasoning

from configuration.configuration import configure_all

logger = logging.getLogger(__name__)


async def summarize(title: str, reports: list[str]) -> str:
    params = MCPServerStdioParams(
        command="npx",
        args=["-y", "@modelcontextprotocol/server-filesystem", f"{os.getcwd()}"],
    )
    async with MCPServerStdio(params=params, client_session_timeout_seconds=30) as server:
        agent = Agent(
            name="Summarize agent",
            instructions=f"""
                    You are a summarizer that given report to summarize to markdown.
                    Write a markdown file to the `report` directory with `{title}.md` as the file name.
                    The file should be in korean language.
                    
                    Only write a file with no response message content.
                    """,
            model="gpt-5-nano",
            model_settings=ModelSettings(reasoning=Reasoning(effort="minimal")),

            mcp_servers=[server],
        )
        result = await Runner.run(agent, "\n\n".join(reports))
        logger.info(f"Result of the summarization: {result.final_output}")
        return result.final_output


if __name__ == '__main__':
    configure_all()
    asyncio.run(
        summarize(
            title="Ai report",
            reports=[
                "Executive Summary\n- The AI frontier is increasingly defined by agentic capabilities: long-horizon planning, multi-step reasoning, and robust tool use. Public discourse in 2025 positions frontier-models as the core of autonomous AI agents, with a focus on integrating reasoning with action in the real world.\n- Among publicly documented options, Google’s Gemini 2.5 Pro (and its companion Gemini 2.5 Computer Use) are highlighted as leading in advanced reasoning and practical tool use. This places Gemini 2.5 Pro at the forefront of “agentic” capability in widely available offerings as of 2025. Other actors (OpenAI ecosystem with agents, McKinsey/Forrester analyses, and frontier-model research) frame the broader landscape but do not point to a single universally superior model for all agentic tasks.\n\nLandscape and evidence (selected sources)\n- Gemini 2.5 Pro and Gemini 2.5 Computer Use: Google/DeepMind disclosures emphasize “thinking models” with improved reasoning and a dedicated browser-use variant, which are core enablers for agentic tasks that require planning and web interaction. Examples include blog posts and product pages describing Gemini 2.5 Pro as the most advanced thinking model and Gemini 2.5 Computer Use as a model optimized for browser/mobile tasks. These signals support Gemini 2.5 Pro as a leading candidate for agentic frontier tasks. See: Gemini 2.5 Pro / Computer Use model pages and announcements. (Sources indicate: Google/DeepMind Gemini 2.5 family statements)\n- Agentic AI and frontier-model discourse (2025): Analyses and industry pieces frame agentic AI as the next frontier and discuss organizational and competitive implications. Notable references include McKinsey’s agentic-organization framing and Forrester’s claims about agentic AI as a competitive frontier. These sources contextualize why agentic capability (not just model size) matters for real-world deployment.\n- Frontiers in frontier-model research (2024–2025): ArXiv work on frontier models and in-context planning provides academic grounding for the claim that frontier models can perform planning-like tasks within prompts, a capability central to agentic AI.\n- Industry and tooling context: Reports and blogs in 2025 discuss agent frameworks (e.g., AutoGen-like ecosystems, LangChain integrations) and the importance of tool-use + memory for robust agentic behavior.\n\nWhat is the “best model” for agentic AI frontier tasks?\n- Core candidate: Gemini 2.5 Pro (with supporting Gemini 2.5 Computer Use) appears to be the strongest publicly documented model for agentic capabilities as of 2025, due to:\n  - Advanced reasoning capabilities described as “thinking models.”\n  - Dedicated tool-use potential via browser-use capabilities and integration points (e.g., Computer Use variant).\n  - Active productization and ecosystem support (API access, integration with Vertex AI, etc.).\n- Important caveats:\n  - There is no single universal best model for all agentic tasks. The “best” choice is highly dependent on task class (e.g., pure reasoning vs. web-enabled task execution), required toolset, latency, compute budgets, and safety/guardrails.\n  - The frontier is ecosystem-driven: success often comes from combining a strong model with planning frameworks, memory, tooling, and governance. Publicly available sources emphasize the importance of the surrounding toolchain and organizational practices, not just model capabilities alone.\n\nPractical recommendations for pursuing an agentic frontier project in 2025\n- Primary model choice: Start with Gemini 2.5 Pro as the core reasoning engine for agentive tasks, and evaluate Gemini 2.5 Computer Use for tasks requiring web browsing and dynamic tool interaction. Follow official documentation for integration points with Vertex AI, APIs, and tool-use patterns.\n- Toolchain and framework: Employ established agent frameworks and orchestration patterns (e.g., tool-use orchestration, planning + execution loops) to enable long-horizon tasks. Leverage memory, state management, and safety guardrails to mitigate unwanted autonomous behavior.\n- Evaluation plan: Benchmark across (a) multi-step reasoning accuracy, (b) reliability of tool-use (web, file I/O, API calls), (c) safety/constraint adherence, and (d) latency and cost. Include outside-in evaluations (real-world task suites) and controlled red-teaming for safety.\n- Safety and governance: Given the agentic nature of frontier models, implement guardrails, monitoring dashboards, and kill-switches. Align with organizational risk appetite and regulatory considerations.\n- Alternative/complementary options: Keep an eye on OpenAI’s agentic tooling ecosystem and other frontier-model releases (e.g., Claude/Anthropic lineage, Meta/Nova offerings) for task-specific advantages. The field evolves quickly, and hybrid configurations (model + tools + policy) often outperform any single model.\n\nHow to proceed (an actionable plan)\n1) Define task classes: long-horizon planning, web-enabled task execution, and structured data manipulation.\n2) Prototype with Gemini 2.5 Pro as the brain; wire up Gemini 2.5 Computer Use for browser-like tasks if needed.\n3) Choose a toolstack: a planning loop, memory module, and tool-interfaces (web, file systems, APIs); implement safeguards.\n4) Run iterative evaluations with realistic scenarios; log failures and adapt tool interfaces.\n5) Compare with alternative frontier offerings on a fixed task suite to validate the best option for your use-case.\n\nConclusion\n- Public signals in 2025 position Google’s Gemini 2.5 Pro (and 2.5 Computer Use) as leading candidates for agentic frontier-model tasks, particularly where strong reasoning and tool-use are required. Yet, the field remains highly task-specific and ecosystem-driven; the best choice is a function of your use-case, toolchain, and safety requirements. A pragmatic path is to use Gemini 2.5 Pro as the core agent and complement it with a robust tool-use framework and governance safeguards, while staying vigilant for new frontier-model releases and evaluating them against your needs.\n\nReferences and sources (indicative, public signals cited in this note)\n- Google/DeepMind: Gemini 2.5 Pro and Gemini 2.5 Computer Use model announcements and documentation (thinking models; browser/web-use capabilities). https://blog.google/technology/google-deepmind/gemini-model-thinking-updates-march-2025/; https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-pro; https://ai.google.dev/gemini-api/docs/models\n- The frontier and agentic AI landscape: McKinsey on the agentic organization as a paradigm for AI-enabled work; Forrester on agentic AI as a competitive frontier. https://www.mckinsey.com/.../the-agentic-organization-contours-of-the-next-paradigm-for-the-ai-era; https://www.forrester.com/blogs/agentic-ai-is-the-next-competitive-frontier/\n- Frontiers in frontier-model research (in-context planning) and related discussions: Meinke, Frontier Models are Capable of In-context Scheming (arXiv:2412.04984, 2024). https://arxiv.org/abs/2412.04984\n- Industry perspectives and tooling: 2025 analyses on agentic frameworks and frontier-model tooling (e.g., AutoGen/LangChain ecosystems) and “Agentic AI Tools” roundups. See representative industry coverage such as Medium and CRN-style roundups for 2025.\n- Note: URLs above reflect representative sources available publicly in 2025 and are referenced to illustrate landscape trends; exact phrasing and positions are as reported by the respective publishers"
            ]
        )
    )
