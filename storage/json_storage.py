import json
import os


def read_data(file_path: str) -> list:
    """JSON 파일을 읽어 리스트로 반환한다. 파일이 없거나 손상되었으면 빈 리스트를 반환한다."""
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return []
        return data
    except (json.JSONDecodeError, IOError):
        return []


def write_data(file_path: str, data: list) -> None:
    """리스트를 JSON 파일로 저장한다. 디렉터리가 없으면 생성한다."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def get_next_id(existing_data: list, prefix: str, id_field: str) -> str:
    """기존 데이터에서 최대 ID 번호를 찾아 1 증가한 새 ID를 반환한다.
    
    Args:
        existing_data: 데이터 리스트
        prefix: ID 접두사 (예: 'C', 'R')
        id_field: ID 필드명 (예: 'customer_id', 'report_id')
    
    Returns:
        새 ID 문자열 (예: 'C001', 'R002')
    """
    max_num = 0
    for item in existing_data:
        id_value = item.get(id_field, "")
        if id_value.startswith(prefix) and id_value[len(prefix):].isdigit():
            num = int(id_value[len(prefix):])
            if num > max_num:
                max_num = num
    return f"{prefix}{max_num + 1:03d}"