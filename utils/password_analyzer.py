import re

def analyze_password_strength(password):
    """
    分析密码强度，返回 {'strength': '弱/中/强', 'feedback': [建议列表]}
    """
    feedback = []
    length = len(password)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9]', password))

    # 评分
    score = 0
    if length >= 8:
        score += 1
    if has_lower and has_upper:
        score += 1
    if has_digit:
        score += 1
    if has_special:
        score += 1

    # 反馈建议
    if length < 8:
        feedback.append("建议密码长度至少8位")
    if not has_lower:
        feedback.append("建议包含小写字母")
    if not has_upper:
        feedback.append("建议包含大写字母")
    if not has_digit:
        feedback.append("建议包含数字")
    if not has_special:
        feedback.append("建议包含特殊字符")

    if score <= 1:
        strength = "弱"
    elif score == 2 or score == 3:
        strength = "中"
    else:
        strength = "强"

    return {'strength': strength, 'feedback': feedback} 