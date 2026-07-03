"""고객사 관리 서비스 모듈"""

import os
from storage.json_storage import read_data, write_data, get_next_id
from validators import validate_email

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers.json")


def _active_customers(customers: list) -> list:
    """삭제되지 않은 고객사만 필터링하여 반환한다."""
    return [c for c in customers if not c.get("is_deleted", False)]


def register_customer(customer_name: str, manager_name: str, email: str) -> dict:
    """고객사를 등록한다.
    
    Args:
        customer_name: 고객사명
        manager_name: 담당자명
        email: 이메일
    
    Returns:
        성공 시 {"success": True, "customer_id": "C001"}
        실패 시 {"success": False, "errors": ["오류 메시지"]}
    """
    errors = []

    if not customer_name or not customer_name.strip():
        errors.append("고객사명은 필수 입력 항목입니다.")
    if not manager_name or not manager_name.strip():
        errors.append("담당자명은 필수 입력 항목입니다.")
    if not email or not email.strip():
        errors.append("이메일은 필수 입력 항목입니다.")
    elif not validate_email(email):
        errors.append("이메일 형식이 올바르지 않습니다.")

    if errors:
        return {"success": False, "errors": errors}

    customers = read_data(CUSTOMER_FILE)
    customer_id = get_next_id(customers, "C", "customer_id")

    new_customer = {
        "customer_id": customer_id,
        "customer_name": customer_name.strip(),
        "manager_name": manager_name.strip(),
        "email": email.strip(),
        "is_deleted": False,
    }
    customers.append(new_customer)
    write_data(CUSTOMER_FILE, customers)

    return {"success": True, "customer_id": customer_id}


def list_customers() -> list:
    """삭제되지 않은 고객사 목록을 반환한다."""
    customers = read_data(CUSTOMER_FILE)
    return _active_customers(customers)


def get_customer(customer_id: str) -> dict | None:
    """고객사 ID로 단건 조회한다. 없으면 None을 반환한다."""
    customers = _active_customers(read_data(CUSTOMER_FILE))
    for c in customers:
        if c.get("customer_id") == customer_id:
            return c
    return None


def update_customer(customer_id: str, customer_name: str, manager_name: str, email: str) -> dict:
    """고객사 정보를 수정한다.
    
    Args:
        customer_id: 수정할 고객사 코드
        customer_name: 새 고객사명 (빈 문자열이면 기존값 유지)
        manager_name: 새 담당자명 (빈 문자열이면 기존값 유지)
        email: 새 이메일 (빈 문자열이면 기존값 유지)
    
    Returns:
        성공 시 {"success": True}
        실패 시 {"success": False, "errors": [...]}
    """
    customers = read_data(CUSTOMER_FILE)
    target = None
    for c in customers:
        if c.get("customer_id") == customer_id and not c.get("is_deleted", False):
            target = c
            break

    if not target:
        return {"success": False, "errors": [f"고객사 코드 '{customer_id}'가 존재하지 않습니다."]}

    new_name = customer_name.strip() if customer_name.strip() else target["customer_name"]
    new_manager = manager_name.strip() if manager_name.strip() else target["manager_name"]
    new_email = email.strip() if email.strip() else target["email"]

    errors = []
    if not new_name:
        errors.append("고객사명은 필수 입력 항목입니다.")
    if not new_manager:
        errors.append("담당자명은 필수 입력 항목입니다.")
    if not new_email:
        errors.append("이메일은 필수 입력 항목입니다.")
    elif not validate_email(new_email):
        errors.append("이메일 형식이 올바르지 않습니다.")

    if errors:
        return {"success": False, "errors": errors}

    target["customer_name"] = new_name
    target["manager_name"] = new_manager
    target["email"] = new_email
    write_data(CUSTOMER_FILE, customers)

    return {"success": True}


def delete_customer(customer_id: str) -> dict:
    """고객사를 삭제한다 (is_deleted 플래그 설정).
    
    Args:
        customer_id: 삭제할 고객사 코드
    
    Returns:
        성공 시 {"success": True}
        실패 시 {"success": False, "errors": [...]}
    """
    customers = read_data(CUSTOMER_FILE)
    target = None
    for c in customers:
        if c.get("customer_id") == customer_id and not c.get("is_deleted", False):
            target = c
            break

    if not target:
        return {"success": False, "errors": [f"고객사 코드 '{customer_id}'가 존재하지 않습니다."]}

    target["is_deleted"] = True
    write_data(CUSTOMER_FILE, customers)

    return {"success": True}