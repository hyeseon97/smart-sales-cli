"""고객사 데이터 검증 모듈"""

import re


def validate_customer(data: dict, existing_customers: list) -> list:
    """고객사 입력 데이터를 검증하고 오류 메시지 리스트를 반환한다.
    
    Args:
        data: 검증할 데이터 (customer_name, manager_name, email)
        existing_customers: 기존 고객사 리스트 (customer_id 중복 체크용)
    
    Returns:
        오류 메시지 리스트 (비어있으면 검증 통과)
    """
    errors = []

    # customer_name 검증
    customer_name = data.get("customer_name", "").strip()
    if not customer_name:
        errors.append("고객사명은 필수 입력 항목입니다.")

    # manager_name 검증
    manager_name = data.get("manager_name", "").strip()
    if not manager_name:
        errors.append("담당자명은 필수 입력 항목입니다.")

    # email 검증
    email = data.get("email", "").strip()
    if not email:
        errors.append("이메일은 필수 입력 항목입니다.")
    elif not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        errors.append("이메일 형식이 올바르지 않습니다. (예: hong@example.com)")

    return errors


def format_customer(customer: dict) -> str:
    """고객사 정보를 출력용 문자열로 변환한다."""
    return (
        f"  고객사코드: {customer.get('customer_id', '')}\n"
        f"  고객사명:   {customer.get('customer_name', '')}\n"
        f"  담당자명:   {customer.get('manager_name', '')}\n"
        f"  이메일:     {customer.get('email', '')}"
    )