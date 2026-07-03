"""영업일지 관리 명령어 모듈"""

import os
from storage.json_storage import read_data, write_data, get_next_id
from models.report import validate_report, format_report
from commands.customer_commands import CUSTOMER_FILE

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
REPORT_FILE = os.path.join(DATA_DIR, "sales_reports.json")


def register_report() -> None:
    """영업일지 등록"""
    customers = read_data(CUSTOMER_FILE)
    reports = read_data(REPORT_FILE)

    print("\n=== 영업일지 등록 ===")
    customer_id = input("고객사 코드: ").strip()
    activity_date = input("활동일 (YYYY-MM-DD): ").strip()
    content = input("활동 내용: ").strip()

    data = {
        "customer_id": customer_id,
        "activity_date": activity_date,
        "content": content,
    }

    errors = validate_report(data, customers)
    if errors:
        print("\n입력 오류:")
        for err in errors:
            print(f"  - {err}")
        return

    report_id = get_next_id(reports, "R", "report_id")
    new_report = {
        "report_id": report_id,
        "customer_id": customer_id,
        "activity_date": activity_date,
        "content": content,
        "status": "DRAFT",
    }
    reports.append(new_report)
    write_data(REPORT_FILE, reports)
    print(f"\n영업일지가 등록되었습니다: {report_id}")


def list_reports() -> None:
    """영업일지 목록 출력"""
    reports = read_data(REPORT_FILE)

    print("\n=== 영업일지 목록 ===")
    if not reports:
        print("등록된 영업일지가 없습니다.")
        return

    status_kor = {
        "DRAFT": "작성중",
        "SUBMITTED": "상신",
        "APPROVED": "승인",
        "REJECTED": "반려",
    }

    print(f"{'코드':<8} {'고객사코드':<12} {'활동일':<14} {'상태':<8} {'활동내용':<30}")
    print("-" * 72)
    for r in reports:
        status = r.get("status", "")
        status_display = status_kor.get(status, status)
        content_preview = r.get("content", "")[:28] + ".." if len(r.get("content", "")) > 28 else r.get("content", "")
        print(f"{r.get('report_id', ''):<8} {r.get('customer_id', ''):<12} {r.get('activity_date', ''):<14} {status_display:<8} {content_preview:<30}")


def update_report() -> None:
    """영업일지 수정 (DRAFT 상태만 가능)"""
    customers = read_data(CUSTOMER_FILE)
    reports = read_data(REPORT_FILE)

    print("\n=== 영업일지 수정 ===")
    report_id = input("수정할 보고서 코드: ").strip()

    target = None
    for r in reports:
        if r.get("report_id") == report_id:
            target = r
            break

    if not target:
        print(f"\n보고서 코드 '{report_id}'가 존재하지 않습니다.")
        return

    if target.get("status") != "DRAFT":
        print(f"\nDRAFT 상태에서만 수정 가능합니다. (현재 상태: {target.get('status', '')})")
        return

    print(f"\n{format_report(target)}")
    print("\n[기존값을 유지하려면 엔터를 입력하세요]")
    new_customer_id = input(f"고객사 코드 ({target['customer_id']}): ").strip()
    new_date = input(f"활동일 ({target['activity_date']}): ").strip()
    new_content = input(f"활동 내용 ({target['content']}): ").strip()

    update_data = {
        "customer_id": new_customer_id if new_customer_id else target["customer_id"],
        "activity_date": new_date if new_date else target["activity_date"],
        "content": new_content if new_content else target["content"],
    }

    errors = validate_report(update_data, customers)
    if errors:
        print("\n입력 오류:")
        for err in errors:
            print(f"  - {err}")
        return

    for r in reports:
        if r.get("report_id") == report_id:
            r["customer_id"] = update_data["customer_id"]
            r["activity_date"] = update_data["activity_date"]
            r["content"] = update_data["content"]
            break

    write_data(REPORT_FILE, reports)
    print(f"\n영업일지 '{report_id}'가 수정되었습니다.")


def _change_status(report_id: str, current_status: str, new_status: str, action_name: str) -> bool:
    """영업일지 상태 변경 공통 함수. 성공 시 True, 실패 시 False 반환."""
    reports = read_data(REPORT_FILE)

    target = None
    for r in reports:
        if r.get("report_id") == report_id:
            target = r
            break

    if not target:
        print(f"\n보고서 코드 '{report_id}'가 존재하지 않습니다.")
        return False

    if target.get("status") != current_status:
        print(f"\n{action_name}할 수 없는 상태입니다. (현재 상태: {target.get('status', '')})")
        return False

    for r in reports:
        if r.get("report_id") == report_id:
            r["status"] = new_status
            break

    write_data(REPORT_FILE, reports)
    status_kor = {"DRAFT": "작성중", "SUBMITTED": "상신", "APPROVED": "승인", "REJECTED": "반려"}
    print(f"\n영업일지 '{report_id}'가 {status_kor.get(new_status, new_status)}(으)로 변경되었습니다.")
    return True


def submit_report() -> None:
    """영업일지 상신 (DRAFT → SUBMITTED)"""
    print("\n=== 영업일지 상신 ===")
    report_id = input("상신할 보고서 코드: ").strip()
    _change_status(report_id, "DRAFT", "SUBMITTED", "상신")


def approve_report() -> None:
    """영업일지 승인 (SUBMITTED → APPROVED)"""
    print("\n=== 영업일지 승인 ===")
    report_id = input("승인할 보고서 코드: ").strip()
    _change_status(report_id, "SUBMITTED", "APPROVED", "승인")


def reject_report() -> None:
    """영업일지 반려 (SUBMITTED → REJECTED)"""
    print("\n=== 영업일지 반려 ===")
    report_id = input("반려할 보고서 코드: ").strip()
    _change_status(report_id, "SUBMITTED", "REJECTED", "반려")


def withdraw_report() -> None:
    """영업일지 회수 (SUBMITTED → DRAFT)"""
    print("\n=== 영업일지 회수 ===")
    report_id = input("회수할 보고서 코드: ").strip()
    _change_status(report_id, "SUBMITTED", "DRAFT", "회수")


def summary_by_customer() -> None:
    """고객사별 활동 요약"""
    from commands.customer_commands import _active_customers
    customers = _active_customers(read_data(CUSTOMER_FILE))
    reports = read_data(REPORT_FILE)

    print("\n=== 고객사별 활동 요약 ===")
    if not customers:
        print("등록된 고객사가 없습니다.")
        return

    status_kor = {"DRAFT": "작성중", "SUBMITTED": "상신", "APPROVED": "승인", "REJECTED": "반려"}

    for c in customers:
        cid = c.get("customer_id", "")
        cname = c.get("customer_name", "")
        customer_reports = [r for r in reports if r.get("customer_id") == cid]

        total = len(customer_reports)
        draft_count = sum(1 for r in customer_reports if r.get("status") == "DRAFT")
        submitted_count = sum(1 for r in customer_reports if r.get("status") == "SUBMITTED")
        approved_count = sum(1 for r in customer_reports if r.get("status") == "APPROVED")
        rejected_count = sum(1 for r in customer_reports if r.get("status") == "REJECTED")

        print(f"\n고객사코드: {cid}  {cname}")
        print(f"  전체: {total}건 | 작성중: {draft_count} | 상신: {submitted_count} | 승인: {approved_count} | 반려: {rejected_count}")
        print("-" * 50)
