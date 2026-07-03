"""입력값 검증 공개 함수"""

import re


def validate_email(email: str) -> bool:
    """이메일 형식이 올바른지 검증한다.
    
    Args:
        email: 검증할 이메일 문자열
    
    Returns:
        형식이 올바르면 True, 아니면 False
    """
    if not email or not isinstance(email, str):
        return False
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email.strip()))