import sys
from commands.customer_commands import register_customer, list_customers, detail_customer, search_customers, update_customer, delete_customer, export_customers_csv
from commands.report_commands import register_report, list_reports, update_report, submit_report, approve_report, reject_report, withdraw_report, summary_by_customer


def show_customer_menu():
    """고객사 관리 하위 메뉴"""
    while True:
        print("\n=== 고객사 관리 ===")
        print("1. 고객사 등록")
        print("2. 고객사 목록")
        print("3. 고객사 상세 조회")
        print("4. 고객사 검색")
        print("5. 고객사 수정")
        print("6. 고객사 삭제")
        print("7. CSV 내보내기")
        print("8. 뒤로가기")
        choice = input("\n메뉴를 선택하세요: ").strip()

        if choice == "1":
            register_customer()
        elif choice == "2":
            list_customers()
        elif choice == "3":
            detail_customer()
        elif choice == "4":
            search_customers()
        elif choice == "5":
            update_customer()
        elif choice == "6":
            delete_customer()
        elif choice == "7":
            export_customers_csv()
        elif choice == "8":
            break
        else:
            print("잘못된 입력입니다. 1~8 사이의 숫자를 입력하세요.")


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
