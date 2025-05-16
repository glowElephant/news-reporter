import json
import os

def load_json(path: str) -> list:
    """
    주어진 경로에 JSON 파일이 있으면 내용을 로드해 리스트로 반환하고,
    없거나 로드 실패 시 빈 리스트를 반환합니다.
    """
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # 파일이 비어있거나 JSON 파싱 오류 발생 시 빈 리스트 반환
            return []
    return []


def save_json(path: str, data: list):
    """
    주어진 데이터(리스트 또는 딕셔너리)를 JSON 형태로 파일에 저장합니다.
    """
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except IOError as e:
        # 파일 쓰기 오류 로그 (필요 시 로깅 추가)
        print(f"Error saving JSON to {path}: {e}")
