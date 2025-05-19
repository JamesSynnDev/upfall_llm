# src/routes/chat.py
import logging
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.concurrency import run_in_threadpool
from src.components.rag_chain import get_rag_chain
from src.components.retriever import load_retriever_from_pdf

router = APIRouter()
# 기본 로거 설정 (stdout에도 출력되도록)
logger = logging.getLogger("chat_ws")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s:%(message)s"))
    logger.addHandler(handler)

# PDF 경로
PDF_PATH = "./data/document.pdf"
VECTOR_DB_PATH = "./store/chroma_index"

# 벡터DB + 체인 초기화
retriever = load_retriever_from_pdf(PDF_PATH, VECTOR_DB_PATH)
rag_chain = get_rag_chain(retriever)


@router.websocket("/ws/chat")
async def websocket_chat(ws: WebSocket):
    await ws.accept()
    print("INFO: WebSocket connection accepted")
    try:
        while True:
            user_msg = await ws.receive_text()
            logger.info(f"⬅ 수신된 질문: {user_msg}")

            try:
                # 🔍 문서 디버깅용
                docs = retriever.invoke(user_msg)
                logger.info(f"🔍 검색된 문서 수: {len(docs)}")
                for i, doc in enumerate(docs):
                    logger.info(f"[{i + 1}] {doc.page_content[:100]}...")

                # 🤖 LLM 추론
                resp = await run_in_threadpool(lambda: rag_chain.invoke(user_msg))

                # 결과 처리
                if not resp.strip():
                    logger.warning("⚠️ 모델이 빈 응답을 반환했습니다.")
                    await ws.send_text("⚠️ 답변을 생성하지 못했습니다.")
                else:
                    await ws.send_text(resp)
                    logger.info(f"🧠 전송된 응답: {resp}")

            except Exception as e:
                logger.exception("❌ LLM 추론 중 오류")
                await ws.send_text("⚠️ 모델 응답 생성 중 오류가 발생했습니다.")

    except WebSocketDisconnect:
        print("INFO: Client disconnected")
    except Exception as e:
        logger.exception("WebSocket error")
        await ws.close(code=1011)
