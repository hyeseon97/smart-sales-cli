"""고객사 관리 명령어 모듈"""

import os
from storage.json_storage import read_data, write_data, get_next_id
from models.customer import validate_customer, format_customer

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers.json")


def _active_customers(customers: list) -> list:
    """삭제되지 않은 고객사만 필터링하여 반환한다."""
    return [c for c in customers if not c.get("is_deleted", False)]


def register_customer() -> None:
    """고객사 등록 화면"""
    customers = read_data(CUSTOMER_FILE)

    print("\n=== 고객사 등록 ===")
    customer_name = input("고객사명: ").strip()
    manager_name = input("담당자명: ").strip()
    email = input("이메일: ").strip()

    data = {
        "customer_name": customer_name,
        "manager_name": manager_name,
        "email": email,
    }

    errors = validate_customer(data, customers)
    if errors:
        print("\n입력 오류:")
        for err in errors:
            print(f"  - {err}")
        return

    customer_id = get_next_id(customers, "C", "customer_id")
    new_customer = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "manager_name": manager_name,
        "email": email,
        "is_deleted": False,
    }
    customers.append(new_customer)
    write_data(CUSTOMER_FILE, customers)
    print(f"\n고객사가 등록되었습니다: {customer_id}")


def list_customers() -> None:
    """고객사 목록 출력"""
    customers = _active_customers(read_data(CUSTOMER_FILE))

    print("\n=== 고객사 목록 ===")
    if not customers:
        print("등록된 고객사가 없습니다.")
        return

    print(f"{'코드':<8} {'고객사명':<20} {'담당자명':<12} {'이메일':<30}")
    print("-" * 70)
    for c in customers:
        print(f"{c.get('customer_id', ''):<8} {c.get('customer_name', ''):<20} {c.get('manager_name', ''):<12} {c.get('email', ''):<30}")


def detail_customer() -> None:
    """고객사 상세 조회"""
    customers = _active_customers(read_data(CUSTOMER_FILE))

    print("\n=== 고객사 상세 조회 ===")
    customer_id = input("조회할 고객사 코드: ").strip()

    for c in customers:
        if c.get("customer_id") == customer_id:
            print(f"\n{format_customer(c)}")
            return

    print(f"\n고객사 코드 '{customer_id}'가 존재하지 않습니다.")


def search_customers() -> None:
    """고객사 검색 (고객사명 또는 담당자명 부분 일치)"""
    customers = _active_customers(read_data(CUSTOMER_FILE))

    print("\n=== 고객사 검색 ===")
    keyword = input("검색어: ").strip()

    if not keyword:
        print("검색어를 입력하세요.")
        return

    results = []
    for c in customers:
        if keyword in c.get("customer_name", "") or keyword in c.get("manager_name", ""):
            results.append(c)

    if not results:
        print(f"\n'{keyword}' 검색 결과가 없습니다.")
        return

    print(f"\n'{keyword}' 검색 결과 ({len(results)}건)")
    print(f"{'코드':<8} {'고객사명':<20} {'담당자명':<12} {'이메일':<30}")
    print("-" * 70)
    for c in results:
        print(f"{c.get('customer_id', ''):<8} {c.get('customer_name', ''):<20} {c.get('manager_name', ''):<12} {c.get('email', ''):<30}")


def update_customer() -> None:
    """고객사 정보 수정"""
    customers = read_data(CUSTOMER_FILE)
    active = _active_customers(customers)

    print("\n=== 고객사 수정 ===")
    customer_id = input("수정할 고객사 코드: ").strip()

    target = None
    for c in active:
        if c.get("customer_id") == customer_id:
            target = c
            break

    if not target:
        print(f"\n고객사 코드 '{customer_id}'가 존재하지 않습니다.")
        return

    print("\n[기존값을 유지하려면 엔터를 입력하세요]")
    new_name = input(f"고객사명 ({target['customer_name']}): ").strip()
    new_manager = input(f"담당자명 ({target['manager_name']}): ").strip()
    new_email = input(f"이메일 ({target['email']}): ").strip()

    update_data = {
        "customer_name": new_name if new_name else target["customer_name"],
        "manager_name": new_manager if new_manager else target["manager_name"],
        "email": new_email if new_email else target["email"],
    }

    errors = validate_customer(update_data, customers)
    if errors:
        print("\n입력 오류:")
        for err in errors:
            print(f"  - {err}")
        return

    for c in customers:
        if c.get("customer_id") == customer_id:
            c["customer_name"] = update_data["customer_name"]
            c["manager_name"] = update_data["manager_name"]
            c["email"] = update_data["email"]
            break

    write_data(CUSTOMER_FILE, customers)
    print(f"\n고객사 '{customer_id}' 정보가 수정되었습니다.")


def delete_customer() -> None:
    """고객사 삭제 (is_deleted 플래그 설정)"""
    customers = read_data(CUSTOMER_FILE)
    active = _active_customers(customers)

    print("\n=== 고객사 삭제 ===")
    customer_id = input("삭제할 고객사 코드: ").strip()

    target = None
    for c in active:
        if c.get("customer_id") == customer_id:
            target = c
            break

    if not target:
        print(f"\n고객사 코드 '{customer_id}'가 존재하지 않습니다.")
        return

    print(f"\n{format_customer(target)}")
    confirm = input("\n정말 삭제하시겠습니까? (y/n): ").strip().lower()
    if confirm != "y":
        print("삭제가 취소되었습니다.")
        return

    for c in customers:
        if c.get("customer_id") == customer_id:
            c["is_deleted"] = True
            break

    write_data(CUSTOMER_FILE, customers)
    print(f"\n고객사 '{customer_id}'가 삭제되었습니다.")


def export_customers_csv() -> None:
    """고객사 목록을 CSV 파일로 내보내기"""
    import csv

    customers = _active_customers(read_data(CUSTOMER_FILE))

    print("\n=== 고객사 CSV 내보내기 ===")
    if not customers:
        print("내보낼 고객사 데이터가 없습니다.")
        return

    file_path = input("저장할 파일 경로: ").strip()
    if not file_path:
        print("파일 경로가 입력되지 않았습니다.")
        return

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f)
            writer.writerow(["customer_id", "customer_name", "manager_name", "email"])
            for c in customers:
                writer.writerow([
                    c.get("customer_id", ""),
                    c.get("customer_name", ""),
                    c.get("manager_name", ""),
                    c.get("email", ""),
                ])
        print(f"\n고객사 목록이 '{file_path}'에 저장되었습니다. (총 {len(customers)}건)")
    except (IOError, OSError) as e:
        print(f"\n파일 저장 중 오류가 발생했습니다: {e}")
