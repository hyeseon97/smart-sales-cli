"""영업일지 모듈 unittest"""

import unittest
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__))))

from models.report import validate_report, format_report
from storage.json_storage import read_data, write_data, get_next_id
from commands.report_commands import _change_status

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers.json")
REPORT_FILE = os.path.join(DATA_DIR, "sales_reports.json")


class TestValidateReport(unittest.TestCase):
    """validate_report 함수 테스트"""

    def setUp(self):
        self.customers = [
            {"customer_id": "C001", "customer_name": "테스트고객사"},
        ]

    def test_valid_input(self):
        """정상 입력 → 오류 없음"""
        data = {
            "customer_id": "C001",
            "activity_date": "2026-06-09",
            "content": "제품 소개 미팅",
        }
        errors = validate_report(data, self.customers)
        self.assertEqual(errors, [])

    def test_invalid_customer_id(self):
        """존재하지 않는 customer_id → 오류"""
        data = {
            "customer_id": "C999",
            "activity_date": "2026-06-09",
            "content": "미팅",
        }
        errors = validate_report(data, self.customers)
        self.assertEqual(len(errors), 1)
        self.assertIn("C999", errors[0])

    def test_invalid_date_format(self):
        """잘못된 날짜 형식 → 오류"""
        data = {
            "customer_id": "C001",
            "activity_date": "2026/06/09",
            "content": "미팅",
        }
        errors = validate_report(data, self.customers)
        self.assertEqual(len(errors), 1)
        self.assertIn("날짜 형식", errors[0])

    def test_nonexistent_date(self):
        """존재하지 않는 날짜 (2월 30일) → 오류"""
        data = {
            "customer_id": "C001",
            "activity_date": "2026-02-30",
            "content": "미팅",
        }
        errors = validate_report(data, self.customers)
        self.assertEqual(len(errors), 1)
        self.assertIn("존재하지 않는 날짜", errors[0])

    def test_empty_content(self):
        """빈 content → 오류"""
        data = {
            "customer_id": "C001",
            "activity_date": "2026-06-09",
            "content": "",
        }
        errors = validate_report(data, self.customers)
        self.assertEqual(len(errors), 1)
        self.assertIn("활동 내용", errors[0])

    def test_all_empty(self):
        """모든 필드 누락 → 3개 오류"""
        data = {
            "customer_id": "",
            "activity_date": "",
            "content": "",
        }
        errors = validate_report(data, self.customers)
        self.assertEqual(len(errors), 3)


class TestFormatReport(unittest.TestCase):
    """format_report 함수 테스트"""

    def test_format_draft(self):
        """DRAFT 상태 → '작성중' 출력"""
        report = {
            "report_id": "R001",
            "customer_id": "C001",
            "activity_date": "2026-06-09",
            "content": "미팅",
            "status": "DRAFT",
        }
        result = format_report(report)
        self.assertIn("R001", result)
        self.assertIn("작성중", result)

    def test_format_approved(self):
        """APPROVED 상태 → '승인' 출력"""
        report = {
            "report_id": "R001",
            "customer_id": "C001",
            "activity_date": "2026-06-09",
            "content": "미팅",
            "status": "APPROVED",
        }
        result = format_report(report)
        self.assertIn("승인", result)


class TestChangeStatus(unittest.TestCase):
    """_change_status 상태 전이 함수 테스트"""

    def setUp(self):
        # 고객사 데이터 준비
        customers = [
            {"customer_id": "C001", "customer_name": "테스트", "is_deleted": False},
        ]
        with open(CUSTOMER_FILE, "w", encoding="utf-8") as f:
            json.dump(customers, f, indent=2, ensure_ascii=False)

        # 영업일지 데이터 준비
        reports = [
            {"report_id": "R001", "customer_id": "C001", "activity_date": "2026-06-09", "content": "미팅", "status": "DRAFT"},
            {"report_id": "R002", "customer_id": "C001", "activity_date": "2026-06-10", "content": "미팅2", "status": "SUBMITTED"},
            {"report_id": "R003", "customer_id": "C001", "activity_date": "2026-06-11", "content": "미팅3", "status": "DRAFT"},
        ]
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(reports, f, indent=2, ensure_ascii=False)

    def tearDown(self):
        with open(CUSTOMER_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

    def test_draft_to_submitted(self):
        """DRAFT → submit → SUBMITTED"""
        result = _change_status("R001", "DRAFT", "SUBMITTED", "상신")
        self.assertTrue(result)
        reports = read_data(REPORT_FILE)
        for r in reports:
            if r["report_id"] == "R001":
                self.assertEqual(r["status"], "SUBMITTED")

    def test_submitted_to_approved(self):
        """SUBMITTED → approve → APPROVED"""
        result = _change_status("R002", "SUBMITTED", "APPROVED", "승인")
        self.assertTrue(result)
        reports = read_data(REPORT_FILE)
        for r in reports:
            if r["report_id"] == "R002":
                self.assertEqual(r["status"], "APPROVED")

    def test_submitted_to_rejected(self):
        """SUBMITTED → reject → REJECTED"""
        result = _change_status("R002", "SUBMITTED", "REJECTED", "반려")
        self.assertTrue(result)
        reports = read_data(REPORT_FILE)
        for r in reports:
            if r["report_id"] == "R002":
                self.assertEqual(r["status"], "REJECTED")

    def test_submitted_to_draft_withdraw(self):
        """SUBMITTED → withdraw → DRAFT"""
        result = _change_status("R002", "SUBMITTED", "DRAFT", "회수")
        self.assertTrue(result)
        reports = read_data(REPORT_FILE)
        for r in reports:
            if r["report_id"] == "R002":
                self.assertEqual(r["status"], "DRAFT")

    def test_draft_to_approved_blocked(self):
        """DRAFT → approve → 차단"""
        result = _change_status("R001", "SUBMITTED", "APPROVED", "승인")
        self.assertFalse(result)
        # 상태가 DRAFT로 유지되어야 함
        reports = read_data(REPORT_FILE)
        for r in reports:
            if r["report_id"] == "R001":
                self.assertEqual(r["status"], "DRAFT")

    def test_nonexistent_report(self):
        """존재하지 않는 report_id → False"""
        result = _change_status("R999", "DRAFT", "SUBMITTED", "상신")
        self.assertFalse(result)

    def test_full_cycle(self):
        """DRAFT → submit → SUBMITTED → withdraw → DRAFT"""
        _change_status("R003", "DRAFT", "SUBMITTED", "상신")
        _change_status("R003", "SUBMITTED", "DRAFT", "회수")
        reports = read_data(REPORT_FILE)
        for r in reports:
            if r["report_id"] == "R003":
                self.assertEqual(r["status"], "DRAFT")


if __name__ == "__main__":
    unittest.main()