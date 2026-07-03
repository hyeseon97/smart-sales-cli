"""customer_service + validators unittest"""

import unittest
import os
import sys
import json

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__))))

from validators import validate_email
from customer_service import (
    register_customer,
    list_customers,
    get_customer,
    update_customer,
    delete_customer,
)

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
CUSTOMER_FILE = os.path.join(DATA_DIR, "customers.json")


class TestValidators(unittest.TestCase):
    """validators.py 테스트"""

    def test_validate_email_valid(self):
        """정상 이메일 → True"""
        self.assertTrue(validate_email("hong@example.com"))
        self.assertTrue(validate_email("test@test.co.kr"))

    def test_validate_email_no_at(self):
        """@ 없는 이메일 → False"""
        self.assertFalse(validate_email("invalid-email"))

    def test_validate_email_no_domain(self):
        """@만 있고 도메인 없음 → False"""
        self.assertFalse(validate_email("test@"))

    def test_validate_email_empty(self):
        """빈 문자열 → False"""
        self.assertFalse(validate_email(""))

    def test_validate_email_none(self):
        """None → False"""
        self.assertFalse(validate_email(None))


class TestCustomerService(unittest.TestCase):
    """customer_service.py 테스트"""

    def setUp(self):
        """각 테스트 전에 데이터 초기화"""
        with open(CUSTOMER_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

    def tearDown(self):
        """각 테스트 후에 데이터 초기화"""
        with open(CUSTOMER_FILE, "w", encoding="utf-8") as f:
            json.dump([], f, indent=2, ensure_ascii=False)

    def test_register_customer_valid(self):
        """정상 등록 → success + customer_id 반환"""
        result = register_customer("테스트고객사", "홍길동", "hong@example.com")
        self.assertTrue(result["success"])
        self.assertEqual(result["customer_id"], "C001")

    def test_register_customer_empty_name(self):
        """고객사명 누락 → errors"""
        result = register_customer("", "홍길동", "hong@example.com")
        self.assertFalse(result["success"])
        self.assertIn("고객사명은 필수 입력 항목입니다.", result["errors"])

    def test_register_customer_empty_manager(self):
        """담당자명 누락 → errors"""
        result = register_customer("테스트고객사", "", "hong@example.com")
        self.assertFalse(result["success"])
        self.assertIn("담당자명은 필수 입력 항목입니다.", result["errors"])

    def test_register_customer_invalid_email(self):
        """잘못된 이메일 → errors"""
        result = register_customer("테스트고객사", "홍길동", "invalid")
        self.assertFalse(result["success"])
        self.assertIn("이메일 형식이 올바르지 않습니다.", result["errors"])

    def test_register_customer_empty_email(self):
        """이메일 누락 → errors"""
        result = register_customer("테스트고객사", "홍길동", "")
        self.assertFalse(result["success"])
        self.assertIn("이메일은 필수 입력 항목입니다.", result["errors"])

    def test_register_customer_duplicate_id_not_possible(self):
        """customer_id는 자동 생성이므로 중복 불가 → 다른 고객사와 다른 ID"""
        r1 = register_customer("첫번째", "홍길동", "hong@test.com")
        r2 = register_customer("두번째", "김철수", "kim@test.com")
        self.assertTrue(r1["success"])
        self.assertTrue(r2["success"])
        self.assertEqual(r1["customer_id"], "C001")
        self.assertEqual(r2["customer_id"], "C002")

    def test_list_customers_empty(self):
        """등록된 고객사 없음 → 빈 리스트"""
        self.assertEqual(list_customers(), [])

    def test_list_customers_with_data(self):
        """등록 후 목록 조회 → 1건"""
        register_customer("테스트고객사", "홍길동", "hong@example.com")
        customers = list_customers()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]["customer_id"], "C001")

    def test_get_customer_found(self):
        """존재하는 ID 조회 → customer 반환"""
        register_customer("테스트고객사", "홍길동", "hong@example.com")
        customer = get_customer("C001")
        self.assertIsNotNone(customer)
        self.assertEqual(customer["customer_name"], "테스트고객사")

    def test_get_customer_not_found(self):
        """존재하지 않는 ID 조회 → None"""
        customer = get_customer("C999")
        self.assertIsNone(customer)

    def test_update_customer_valid(self):
        """정상 수정 → success"""
        register_customer("테스트고객사", "홍길동", "hong@example.com")
        result = update_customer("C001", "수정된고객사", "", "")
        self.assertTrue(result["success"])

        customer = get_customer("C001")
        self.assertEqual(customer["customer_name"], "수정된고객사")

    def test_update_customer_not_found(self):
        """존재하지 않는 ID 수정 → errors"""
        result = update_customer("C999", "새이름", "담당자", "email@test.com")
        self.assertFalse(result["success"])
        self.assertIn("C999", result["errors"][0])

    def test_update_customer_invalid_email(self):
        """수정 시 잘못된 이메일 → errors"""
        register_customer("테스트고객사", "홍길동", "hong@example.com")
        result = update_customer("C001", "", "", "invalid-email")
        self.assertFalse(result["success"])
        self.assertIn("이메일 형식", result["errors"][0])

    def test_delete_customer_valid(self):
        """정상 삭제 → success + is_deleted=True"""
        register_customer("테스트고객사", "홍길동", "hong@example.com")
        result = delete_customer("C001")
        self.assertTrue(result["success"])

        # 삭제 후 목록에서 제외
        customers = list_customers()
        self.assertEqual(len(customers), 0)

        # 단건 조회도 None
        customer = get_customer("C001")
        self.assertIsNone(customer)

    def test_delete_customer_not_found(self):
        """존재하지 않는 ID 삭제 → errors"""
        result = delete_customer("C999")
        self.assertFalse(result["success"])
        self.assertIn("C999", result["errors"][0])

    def test_delete_customer_already_deleted(self):
        """이미 삭제된 고객사 다시 삭제 → errors"""
        register_customer("테스트고객사", "홍길동", "hong@example.com")
        delete_customer("C001")
        result = delete_customer("C001")
        self.assertFalse(result["success"])
        self.assertIn("C001", result["errors"][0])


if __name__ == "__main__":
    unittest.main()