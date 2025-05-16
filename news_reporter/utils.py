import json
import os

def load_json(path: str) -> list:
    """
    주어진 경로에 JSON 파일이 있으면 내용을 로드해 리스트로 반환하고,
    없으면 빈 리스트를 반환합니다.
    """
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_json(path: str, data: list):
    """
    주어진 데이터(리스트 또는 딕셔너리)를 JSON 형태로 파일에 저장합니다.
    """
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
