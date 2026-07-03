"""영업일지 데이터 검증 모듈"""

import re
from datetime import datetime


def validate_report(data: dict, customers: list) -> list:
    """영업일지 입력 데이터를 검증하고 오류 메시지 리스트를 반환한다.
    
    Args:
        data: 검증할 데이터 (customer_id, activity_date, content)
        customers: 고객사 리스트 (customer_id 존재 확인용)
    
    Returns:
        오류 메시지 리스트 (비어있으면 검증 통과)
    """
    errors = []

    # customer_id 검증
    customer_id = data.get("customer_id", "").strip()
    if not customer_id:
        errors.append("고객사 코드는 필수 입력 항목입니다.")
    else:
        found = any(c.get("customer_id") == customer_id for c in customers)
        if not found:
            errors.append(f"고객사 코드 '{customer_id}'가 존재하지 않습니다.")

    # activity_date 검증
    activity_date = data.get("activity_date", "").strip()
    if not activity_date:
        errors.append("활동일은 필수 입력 항목입니다.")
    elif not re.match(r"^\d{4}-\d{2}-\d{2}$", activity_date):
        errors.append("날짜 형식이 올바르지 않습니다. (예: 2026-06-09)")
    else:
        try:
            datetime.strptime(activity_date, "%Y-%m-%d")
        except ValueError:
            errors.append("존재하지 않는 날짜입니다.")

    # content 검증
    content = data.get("content", "").strip()
    if not content:
        errors.append("활동 내용은 필수 입력 항목입니다.")

    return errors


def format_report(report: dict) -> str:
    """영업일지 정보를 출력용 문자열로 변환한다."""
    status_kor = {
        "DRAFT": "작성중",
        "SUBMITTED": "상신",
        "APPROVED": "승인",
        "REJECTED": "반려",
    }
    status = report.get("status", "")
    status_display = status_kor.get(status, status)
    return (
        f"  보고서코드: {report.get('report_id', '')}\n"
        f"  고객사코드: {report.get('customer_id', '')}\n"
        f"  활동일:     {report.get('activity_date', '')}\n"
        f"  활동내용:   {report.get('content', '')}\n"
        f"  상태:       {status_display}"
    )