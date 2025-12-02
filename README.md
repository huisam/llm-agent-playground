## llm-agent-playground

멀티 에이전트 기반 LLM 리서치 파이프라인을 실험하기 위한 플레이그라운드입니다.  
`openai-agents`, `google-adk`, MCP(Model Context Protocol) 서버 등을 활용해 아래와 같은 **연구 워크플로우**를 자동화합니다.

- **0. Guardrail**: 사용자의 요청이 실제 "리서치 작업"이 필요한지 판단
- **1. Plan**: 웹 검색 플랜(검색 쿼리)을 생성
- **2. Research**: MCP 웹 검색을 통해 자료 조사 및 리포트 작성
- **3. Summarize**: 조사 결과를 한국어 Markdown 리포트로 정리

`orchestration_agent.py` 에서 위 단계를 오케스트레이션하는 에이전트를 실행합니다.

---

## 주요 기능

- **오케스트레이션 에이전트**
  - `orchestration_agent.py` 내 `orchestration(topic: str)`  
  - Guardrail / Planner / Research / Summarize 에이전트를 하나의 워크플로우로 실행

- **OpenAI 기반 에이전트 (`openai_agents/`)**
  - **`guardrail_agent.py`**
    - 사용자의 입력이 실제 리서치가 필요한지 판별 (`is_research_work` 플래그)
  - **`planner_agent.py`**
    - Pydantic 모델(`WebSearchPlan`) 기반으로 검색 플랜 생성
  - **`research_agent.py`**
    - MCP 서버(`serper-mcp-server`)를 통해 웹 검색 수행
    - 결과를 `ResearchReport`(요약 + 전체 리포트)로 반환
  - **`summarize_agent.py`**
    - 파일 시스템 MCP 서버를 사용해 `report` 디렉터리에 Markdown 리포트 파일 생성
    - 응답은 **파일 경로만** 반환

- **Google ADK 기반 예제 (`google_adk/`)**
  - 동일한 역할(Planner / Research / Summarize)을 Google ADK 스타일로 구현한 예제 폴더

- **공통 설정 (`configuration/configuration.py`)**
  - `.env` 로부터 환경 변수 로드
  - 기본 로깅 설정
  - `opik`를 이용한 관측/추적 설정

---

## 설치

이 프로젝트는 Python 3.13 이상을 요구합니다.

```bash
git clone <your-repo-url>
cd llm-agent-playground

# uv를 사용하는 경우 (권장)
uv sync

# 또는 일반 pip 사용 시
pip install -r <(uv export --format=requirements.txt)
```

필요한 주요 의존성은 `pyproject.toml` 에 정의되어 있습니다.

- `openai-agents`
- `google-adk`
- `mcp[cli]`
- `opik`
- `python-dotenv`
- `httpx`, `litellm` 등

---

## 환경 변수 설정

프로젝트 루트에 `.env` 파일을 생성하고 다음과 같은 값을 설정해야 합니다.

```env
OPENAI_API_KEY=...
OPIK_API_KEY=...
SERPER_API_KEY=...
GOOGLE_API_KEY=...
```

각 키는 다음에 사용됩니다.

- **`OPENAI_API_KEY`**: OpenAI 모델 호출 (`gpt-5-mini`, `gpt-5-nano`, `gpt-4o-mini` 등)
- **`GOOGLE_API_KEY`**: Google 모델 호출 (`gemini-2.5-flash`, `gemini-3.0-pro-prview`등)
- **`OPIK_API_KEY`**: `opik` 기반 추적/로그 수집
- **`SERPER_API_KEY`**: `serper-mcp-server`를 통한 웹 검색

---

## 사용 방법

### 1. 오케스트레이션 에이전트 실행

`orchestration_agent.py` 는 전체 리서치 워크플로우를 실행하는 예시 스크립트입니다.

```bash
python orchestration_agent.py
```

기본 예제에서는 다음 토픽으로 실행됩니다.

```python
asyncio.run(orchestration("What is my name?"))
```

직접 토픽을 바꾸고 싶다면, 파일 하단의 호출부를 수정하거나, 별도의 진입 스크립트를 만들어 다음과 같이 사용할 수 있습니다.

```python
from orchestration_agent import orchestration
from configuration.configuration import configure_all
import asyncio

if __name__ == "__main__":
    configure_all()
    asyncio.run(orchestration("당신이 조사하고 싶은 주제"))
```

### 2. 개별 에이전트 실행 예시

- **플래너만 실행**

```bash
python openai_agents/planner_agent.py
```

- **리서치만 실행**

```bash
python openai_agents/research_agent.py
```

- **요약만 실행**

```bash
python openai_agents/summarize_agent.py
```

각 스크립트의 `if __name__ == "__main__":` 블록에 테스트용 예제가 포함되어 있습니다.

---

## MCP 서버

이 프로젝트는 MCP(Model Context Protocol) 기반 툴을 사용합니다.

- **웹 리서치용 MCP 서버**
  - 명령: `uvx serper-mcp-server`
  - 사용 위치: `openai_agents/research_agent.py` (`create_research_mcp_server`)
  - 필요 환경 변수: `SERPER_API_KEY`

- **파일 시스템 MCP 서버**
  - 명령: `npx -y @modelcontextprotocol/server-filesystem <프로젝트_루트>`
  - 사용 위치: `openai_agents/summarize_agent.py` (`create_summarize_mcp_server`)
  - 역할: `report` 디렉터리에 Markdown 리포트를 생성/저장

실행 시 `uvx` / `npx` 가 PATH 에 있어야 하므로 Node.js 및 uv 환경이 구성되어 있어야 합니다.

---

## 프로젝트 구조

```text
llm-agent-playground/
  orchestration_agent.py      # 전체 리서치 워크플로우 오케스트레이션
  configuration/
    configuration.py          # 로깅, .env, Opik 설정
  openai_agents/
    guardrail_agent.py        # 리서치 필요 여부 판단
    planner_agent.py          # 웹 검색 플랜 생성
    research_agent.py         # MCP 웹 리서치 & 리포트 생성
    summarize_agent.py        # Markdown 리포트 생성 (파일 시스템 MCP)
    evaluator_agent.py        # (향후) 결과 평가 에이전트용
  google_adk/
    planner_agent.py          # Google ADK 스타일 플래너 예제
    research_agent.py         # Google ADK 스타일 리서치 예제
    summarize_agent.py        # Google ADK 스타일 요약 예제
    report/
      title.md                # 리포트 샘플/타이틀
```

---

## 개발 노트

- 이 저장소는 **에이전트 오케스트레이션 패턴**과 **MCP 기반 툴 호출**을 실험하기 위한 목적의 예제 프로젝트입니다.
- 실제 서비스에 적용할 때는
  - 에러 핸들링
  - 토큰/비용 관리
  - 추가적인 가드레일 및 모니터링
  - 리포트 스키마 확장
  등을 더 정교하게 구성하는 것을 권장합니다.


