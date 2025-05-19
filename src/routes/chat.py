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
            # 클라이언트 메시지 수신
            user_msg = await ws.receive_text()
            print(f"⬅ Received from client: '{user_msg}'")

            # 모델 추론
            logger.info(f"[generate_text] prompt={user_msg!r}")
            bot_resp = await run_in_threadpool(rag_chain.invoke(user_msg))
            logger.info(f"[generate_text] output={bot_resp!r}")

            # 클라이언트로 전송
            print(f"🧠 모델 응답: '{bot_resp}'")
            print(f"▶ Sending to client: '{bot_resp}'")
            await ws.send_text(bot_resp)
            print("✔ 메시지 전송 완료")

    except WebSocketDisconnect:
        print("INFO: Client disconnected")
    except Exception as e:
        logger.exception("WebSocket error")
        await ws.close(code=1011)
