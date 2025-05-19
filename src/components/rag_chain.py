from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from src.components.llm import get_llm
from langchain_core.runnables import RunnableLambda
def get_rag_chain(retriever):

    prompt = PromptTemplate.from_template("""
    system: 당신은 문서를 바탕으로 질문에 답하는 AI입니다.
    문맥에 정보가 없으면 "정보를 찾을 수 없습니다."라고 하세요.

    context:
    {context}

    question:
    {input}
    """)
    llm = get_llm()
    rag_chain = (
            {
                "context": retriever,
                "input": RunnablePassthrough()
            }
            | prompt  #
            | RunnableLambda(lambda x: str(x))  # 또는 .format(...) 필요시 명시적 변환
            | llm
            | StrOutputParser()
    )
    return rag_chain