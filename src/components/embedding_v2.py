import os
import csv
import chromadb
from sentence_transformers import SentenceTransformer

# 1. 모델 및 Chroma DB 초기화
embed_model = SentenceTransformer('../models/bge-m3')  # 로컬 경로 사용
chroma_client = chromadb.PersistentClient(path='chroma_db')
collection = chroma_client.get_or_create_collection(name='pdf_contents')

# 2. 콘텐츠 시퀀스 로드 (csv.reader 사용)
content_sequence_file = '../pdf_extracted_content/pdf_content_sequence.csv'

def read_content_sequence(csv_path):
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        return list(reader)

def chunk_text(text, max_tokens=300):
    words = text.split()
    chunks, chunk = [], []
    for word in words:
        chunk.append(word)
        if len(chunk) >= max_tokens:
            chunks.append(' '.join(chunk))
            chunk = []
    if chunk:
        chunks.append(' '.join(chunk))
    return chunks

def make_id(content_type, idx, chunk_idx):
    return f"{content_type}_{idx}_chunk_{chunk_idx}"

content_list = read_content_sequence(content_sequence_file)

# 3. 콘텐츠 순회하며 처리
for idx, (content_type, content) in enumerate(content_list):
    chunks = []

    if content_type == 'text':
        chunks = chunk_text(content)

    elif content_type == 'table':
        if os.path.exists(content):
            with open(content, newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                table_text = '\n'.join([', '.join(row) for row in reader if any(row)])
                chunks = chunk_text(table_text)

    elif content_type == 'image':
        chunks = [f"[IMAGE: {os.path.basename(content)}]"]

    # 저장
    for chunk_idx, chunk in enumerate(chunks):
        embedding = embed_model.encode(chunk).tolist()
        collection.add(
            ids=[make_id(content_type, idx, chunk_idx)],
            embeddings=[embedding],
            documents=[chunk],
            metadatas=[{'type': content_type, 'source': content}]
        )

print("✅ 경량 CSV 처리 + Chroma 저장 완료!")
