"""고객사 모듈 unittest"""

import unittest
import os
import sys
import json
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__))))

from models.customer import validate_customer, format_customer
from storage.json_storage import read_data, write_data, get_next_id


class TestValidateCustomer(unittest.TestCase):
    """validate_customer 함수 테스트"""

    def test_valid_input(self):
        """정상 입력 → 오류 없음"""
        data = {
            "customer_name": "테스트고객사",
            "manager_name": "홍길동",
            "email": "hong@example.com",
        }
        errors = validate_customer(data, [])
        self.assertEqual(errors, [])

    def test_empty_fields(self):
        """빈 필드 → 3개 오류"""
        data = {
            "customer_name": "",
            "manager_name": "  ",
            "email": "",
        }
        errors = validate_customer(data, [])
        self.assertEqual(len(errors), 3)

    def test_invalid_email_no_at(self):
        """@ 없는 이메일 → 오류"""
        data = {
            "customer_name": "테스트",
            "manager_name": "홍길동",
            "email": "invalid-email",
        }
        errors = validate_customer(data, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("이메일 형식", errors[0])

    def test_invalid_email_no_domain(self):
        """@만 있고 도메인 없음 → 오류"""
        data = {
            "customer_name": "테스트",
            "manager_name": "홍길동",
            "email": "test@",
        }
        errors = validate_customer(data, [])
        self.assertEqual(len(errors), 1)
        self.assertIn("이메일 형식", errors[0])


class TestFormatCustomer(unittest.TestCase):
    """format_customer 함수 테스트"""

    def test_format_output(self):
        """출력 형식에 필수 필드 포함"""
        customer = {
            "customer_id": "C001",
            "customer_name": "테스트고객사",
            "manager_name": "홍길동",
            "email": "hong@example.com",
        }
        result = format_customer(customer)
        self.assertIn("C001", result)
        self.assertIn("테스트고객사", result)
        self.assertIn("홍길동", result)
        self.assertIn("hong@example.com", result)


class TestJsonStorage(unittest.TestCase):
    """json_storage 모듈 함수 테스트"""

    def setUp(self):
        self.tmpfile = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data", "_test_unittest.json"
        )

    def tearDown(self):
        if os.path.exists(self.tmpfile):
            os.remove(self.tmpfile)

    def test_get_next_id_empty(self):
        """빈 리스트 → C001"""
        result = get_next_id([], "C", "customer_id")
        self.assertEqual(result, "C001")

    def test_get_next_id_existing(self):
        """기존 데이터 → 다음 ID"""
        data = [
            {"customer_id": "C001"},
            {"customer_id": "C002"},
            {"customer_id": "C005"},
        ]
        result = get_next_id(data, "C", "customer_id")
        self.assertEqual(result, "C006")

    def test_get_next_id_report(self):
        """R prefix ID 생성"""
        data = [{"report_id": "R001"}, {"report_id": "R003"}]
        result = get_next_id(data, "R", "report_id")
        self.assertEqual(result, "R004")

    def test_read_data_empty_file(self):
        """존재하지 않는 파일 → 빈 리스트"""
        result = read_data("data/_nonexistent_file.json")
        self.assertEqual(result, [])

    def test_read_data_corrupt_file(self):
        """손상된 JSON 파일 → 빈 리스트"""
        with open(self.tmpfile, "w", encoding="utf-8") as f:
            f.write("{invalid json}")
        result = read_data(self.tmpfile)
        self.assertEqual(result, [])

    def test_write_and_read_data(self):
        """쓰기 후 읽기 → 동일한 데이터"""
        test_data = [{"id": "T001", "name": "test"}]
        write_data(self.tmpfile, test_data)
        result = read_data(self.tmpfile)
        self.assertEqual(result, test_data)


if __name__ == "__main__":
    unittest.main()