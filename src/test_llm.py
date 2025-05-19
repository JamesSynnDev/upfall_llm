# src/test_llm.py
from src.components.llm import get_llm

llm = get_llm()
prompt = """문맥:
AWS는 최근 Amazon Q 에이전트를 출시하여 작업 부하를 줄이고 있습니다.

질문:
aws 관련 에이전트의 특징은 무엇입니까?
"""

response = llm(prompt)
print("✅ LLM 응답:", response)