import sys
from customer_service import register_customer, list_customers, get_customer, update_customer, delete_customer
from commands.report_commands import register_report, list_reports, update_report, submit_report, approve_report, reject_report, withdraw_report, summary_by_customer


def show_customer_menu():
    """고객사 관리 하위 메뉴"""
    while True:
        print("\n=== 고객사 관리 ===")
        print("1. 고객사 등록")
        print("2. 고객사 목록")
        print("3. 고객사 상세 조회")
        print("4. 고객사 수정")
        print("5. 고객사 삭제")
        print("6. 뒤로가기")
        choice = input("\n메뉴를 선택하세요: ").strip()

        if choice == "1":
            _register_customer_ui()
        elif choice == "2":
            _list_customers_ui()
        elif choice == "3":
            _detail_customer_ui()
        elif choice == "4":
            _update_customer_ui()
        elif choice == "5":
            _delete_customer_ui()
        elif choice == "6":
            break
        else:
            print("잘못된 입력입니다. 1~6 사이의 숫자를 입력하세요.")


def _register_customer_ui():
    """고객사 등록 UI"""
    print("\n=== 고객사 등록 ===")
    customer_name = input("고객사명: ").strip()
    manager_name = input("담당자명: ").strip()
    email = input("이메일: ").strip()

    result = register_customer(customer_name, manager_name, email)
    if result["success"]:
        print(f"\n고객사가 등록되었습니다: {result['customer_id']}")
    else:
        print("\n입력 오류:")
        for err in result["errors"]:
            print(f"  - {err}")


def _list_customers_ui():
    """고객사 목록 UI"""
    customers = list_customers()

    print("\n=== 고객사 목록 ===")
    if not customers:
        print("등록된 고객사가 없습니다.")
        return

    print(f"{'코드':<8} {'고객사명':<20} {'담당자명':<12} {'이메일':<30}")
    print("-" * 70)
    for c in customers:
        print(f"{c.get('customer_id', ''):<8} {c.get('customer_name', ''):<20} {c.get('manager_name', ''):<12} {c.get('email', ''):<30}")


def _detail_customer_ui():
    """고객사 상세 조회 UI"""
    print("\n=== 고객사 상세 조회 ===")
    customer_id = input("조회할 고객사 코드: ").strip()

    customer = get_customer(customer_id)
    if customer:
        print(f"\n  고객사코드: {customer.get('customer_id', '')}")
        print(f"  고객사명:   {customer.get('customer_name', '')}")
        print(f"  담당자명:   {customer.get('manager_name', '')}")
        print(f"  이메일:     {customer.get('email', '')}")
    else:
        print(f"\n고객사 코드 '{customer_id}'가 존재하지 않습니다.")


def _update_customer_ui():
    """고객사 수정 UI"""
    print("\n=== 고객사 수정 ===")
    customer_id = input("수정할 고객사 코드: ").strip()

    customer = get_customer(customer_id)
    if not customer:
        print(f"\n고객사 코드 '{customer_id}'가 존재하지 않습니다.")
        return

    print("\n[기존값을 유지하려면 엔터를 입력하세요]")
    new_name = input(f"고객사명 ({customer['customer_name']}): ").strip()
    new_manager = input(f"담당자명 ({customer['manager_name']}): ").strip()
    new_email = input(f"이메일 ({customer['email']}): ").strip()

    result = update_customer(customer_id, new_name, new_manager, new_email)
    if result["success"]:
        print(f"\n고객사 '{customer_id}' 정보가 수정되었습니다.")
    else:
        print("\n입력 오류:")
        for err in result["errors"]:
            print(f"  - {err}")


def _delete_customer_ui():
    """고객사 삭제 UI"""
    print("\n=== 고객사 삭제 ===")
    customer_id = input("삭제할 고객사 코드: ").strip()

    customer = get_customer(customer_id)
    if not customer:
        print(f"\n고객사 코드 '{customer_id}'가 존재하지 않습니다.")
        return

    print(f"\n  고객사코드: {customer.get('customer_id', '')}")
    print(f"  고객사명:   {customer.get('customer_name', '')}")
    print(f"  담당자명:   {customer.get('manager_name', '')}")
    print(f"  이메일:     {customer.get('email', '')}")
    confirm = input("\n정말 삭제하시겠습니까? (y/n): ").strip().lower()
    if confirm != "y":
        print("삭제가 취소되었습니다.")
        return

    result = delete_customer(customer_id)
    if result["success"]:
        print(f"\n고객사 '{customer_id}'가 삭제되었습니다.")


def show_report_menu():
    """영업일지 관리 하위 메뉴"""
    while True:
        print("\n=== 영업일지 관리 ===")
        print("1. 영업일지 등록")
        print("2. 영업일지 목록")
        print("3. 영업일지 수정")
        print("4. 영업일지 상신")
        print("5. 영업일지 승인")
        print("6. 영업일지 반려")
        print("7. 영업일지 회수")
        print("8. 고객사별 활동 요약")
        print("9. 뒤로가기")
        choice = input("\n메뉴를 선택하세요: ").strip()

        if choice == "1":
            register_report()
        elif choice == "2":
            list_reports()
        elif choice == "3":
            update_report()
        elif choice == "4":
            submit_report()
        elif choice == "5":
            approve_report()
        elif choice == "6":
            reject_report()
        elif choice == "7":
            withdraw_report()
        elif choice == "8":
            summary_by_customer()
        elif choice == "9":
            break
        else:
            print("잘못된 입력입니다. 1~9 사이의 숫자를 입력하세요.")


def show_main_menu():
    """메인 메뉴를 출력하고 사용자 입력을 받아 해당 기능으로 분기한다."""
    while True:
        print("\n=== Smart Sales CLI ===")
        print("1. 고객사 관리")
        print("2. 영업일지 관리")
        print("3. 종료")
        choice = input("\n메뉴를 선택하세요: ").strip()

        if choice == "1":
            show_customer_menu()
        elif choice == "2":
            show_report_menu()
        elif choice == "3":
            print("프로그램을 종료합니다.")
            sys.exit(0)
        else:
            print("잘못된 입력입니다. 1~3 사이의 숫자를 입력하세요.")


if __name__ == "__main__":
    show_main_menu()