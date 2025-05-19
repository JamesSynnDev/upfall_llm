# scripts/download_and_flatten.py
import os
import shutil
from dotenv import load_dotenv
from huggingface_hub import list_repo_files, hf_hub_download
from tqdm import tqdm

load_dotenv()
REPO_ID    = os.getenv("MODEL_NAME")
if not REPO_ID:
    raise ValueError("환경변수 MODEL_NAME 이 설정되어 있지 않습니다.")

# 저장할 최상위 디렉토리
TARGET_BASE = os.path.join("models", *REPO_ID.split("/"))
os.makedirs(TARGET_BASE, exist_ok=True)

# 1) 리포지토리 안의 파일 목록 조회
print(f"🔍 Listing files in {REPO_ID} …")
files = list_repo_files(REPO_ID)

# 2) 하나씩 내려받으면서 progress bar 표시
print(f"📥 Downloading {len(files)} files from {REPO_ID}:")
for filename in tqdm(files, desc="❏ Downloading", unit="file"):
    # huggingface_hub 의 hf_hub_download 은 내부적으로 진행률 표시를 하지 않으니
    # tqdm 으로 감싸줍니다.
    local_path = hf_hub_download(
        repo_id=REPO_ID,
        filename=filename,
        cache_dir=TARGET_BASE,
        local_files_only=False,  # 허브에서 실제 다운로드
        force_filename=filename,
        use_auth_token=True      # gated repo 인 경우
    )
    # hf_hub_download 은 캐시 위치를 반환하므로, TARGET_BASE/filename 으로 이동
    dst_path = os.path.join(TARGET_BASE, filename)
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    if local_path != dst_path:
        shutil.copy2(local_path, dst_path)

print(f"✅ All files downloaded to {TARGET_BASE}")
