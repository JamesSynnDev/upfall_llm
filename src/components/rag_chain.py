from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.components.llm import get_llm

def get_rag_chain(retriever):
    prompt = ChatPromptTemplate.from_messages([
        ("human", """
당신은 문서를 바탕으로 질문에 답하는 AI입니다.
문맥에 정보가 없으면 "정보를 찾을 수 없습니다."라고 하세요.

문맥:
{context}

질문:
{input}
""")
    ])
    llm = get_llm()
    parser = StrOutputParser()

    return {
        "context": retriever,
        "input": RunnablePassthrough()
    } | prompt | llm | parser
