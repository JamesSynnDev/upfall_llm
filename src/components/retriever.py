from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from src.components.embedding import get_embedding_model
import os

def load_retriever_from_pdf(pdf_path, chroma_path):
    embedding = get_embedding_model()

    if os.path.exists(chroma_path):
        print("✅ 기존 Chroma 벡터 DB 로딩 중...")
        db = Chroma(persist_directory=chroma_path, embedding_function=embedding)
    else:
        print("📄 PDF 로딩 및 임베딩 중...")
        loader = PyPDFLoader(pdf_path)
        text_splitter = CharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        docs = loader.load_and_split(text_splitter=text_splitter)

        db = Chroma.from_documents(
            documents=docs,
            embedding=embedding,
            persist_directory=chroma_path
        )
        db.persist()
        print("✅ Chroma DB 생성 완료")

    return db.as_retriever(search_kwargs={"k": 2})
