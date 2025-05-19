from huggingface_hub import hf_hub_download, HfApi
from tqdm import tqdm
import os


def download_bge_model(save_dir="./models/bge-m3", model_name="BAAI/bge-m3"):
    print(f"📦 모델 다운로드 시작: {model_name}")

    os.makedirs(save_dir, exist_ok=True)
    api = HfApi()

    try:
        # 모델 파일 리스트 받아오기
        files = api.list_repo_files(repo_id=model_name)
    except Exception as e:
        print(f"❌ 모델 불러오기 실패: {e}")
        return

    # tqdm으로 프로그레스 바 표시하며 하나씩 다운로드
    for file in tqdm(files, desc="📥 다운로드 진행 중", unit="파일"):
        try:
            hf_hub_download(
                repo_id=model_name,
                filename=file,
                cache_dir=save_dir,
                local_dir=save_dir,
                local_dir_use_symlinks=False
            )
        except Exception as e:
            print(f"⚠️ {file} 다운로드 실패: {e}")

    print(f"✅ 모델 다운로드 완료: {save_dir}")


if __name__ == "__main__":
    download_bge_model()
