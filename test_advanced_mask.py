#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import zipfile

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cracker.advanced_mask_engine import AdvancedMaskEngine, crack_with_advanced_mask

def test_log(message):
    print(f"[LOG] {message}")

def test_progress(current, total, message):
    print(f"[PROGRESS] {current}/{total} - {message}")

def create_test_zip():
    """创建测试ZIP文件"""
    test_file = "test_mask.zip"
    test_password = "abc123"
    
    # 创建测试文件
    with open("test_content.txt", "w", encoding="utf-8") as f:
        f.write("这是一个测试文件，用于掩码破解测试。")
    
    # 创建带密码的ZIP文件
    with zipfile.ZipFile(test_file, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write("test_content.txt", pwd=test_password.encode())
    
    # 清理临时文件
    os.remove("test_content.txt")
    
    print(f"✅ 创建测试ZIP文件: {test_file} (密码: {test_password})")
    return test_file

def test_mask_engine():
    """测试高级掩码引擎"""
    print("🧪 测试高级掩码破解引擎")
    print("=" * 50)
    
    # 创建测试文件
    test_file = create_test_zip()
    
    # 测试掩码
    test_masks = [
        "?l?l?l?d?d?d",  # abc123
        "?l?l?l?n?n?n",  # 使用数字别名
        "?c?c?c?z?z?z",  # 使用小写别名
        "?l?l?l?d?d?d",  # 标准格式
    ]
    
    engine = AdvancedMaskEngine()
    
    print(f"🔧 引擎配置:")
    print(f"   - 并行线程数: {engine.max_workers}")
    print(f"   - 批次大小: {engine.batch_size}")
    print(f"   - 字符集数量: {len(engine.charsets)}")
    print(f"   - 智能字符集数量: {len(engine.smart_charsets)}")
    
    # 测试文件分析
    print(f"\n📊 文件分析:")
    analysis = engine.analyze_file_pattern(test_file)
    print(f"   - 文件名: {analysis['filename']}")
    print(f"   - 文件大小: {analysis['size']:,} 字节")
    print(f"   - 建议掩码: {analysis['suggested_masks']}")
    
    # 测试智能建议
    print(f"\n💡 智能掩码建议:")
    suggestions = engine.intelligent_mask_suggestions(test_file)
    for i, suggestion in enumerate(suggestions[:10], 1):
        print(f"   {i}. {suggestion}")
    
    # 测试掩码解析
    print(f"\n🔍 掩码解析测试:")
    for mask in test_masks:
        charset_list = engine.parse_mask(mask)
        total_combinations = 1
        for charset in charset_list:
            if isinstance(charset, str):
                total_combinations *= len(charset)
        print(f"   掩码 '{mask}': {len(charset_list)} 个字符集, {total_combinations:,} 个组合")
    
    # 测试实际破解
    print(f"\n🚀 开始实际破解测试:")
    start_time = time.time()
    
    result = crack_with_advanced_mask(
        test_file, 
        "?l?l?l?d?d?d",  # abc123
        test_log, 
        test_progress
    )
    
    elapsed = time.time() - start_time
    
    if result:
        print(f"✅ 破解成功! 密码: {result}")
        print(f"⏱️  耗时: {elapsed:.2f} 秒")
    else:
        print(f"❌ 破解失败")
    
    # 清理测试文件
    if os.path.exists(test_file):
        os.remove(test_file)
        print(f"🧹 清理测试文件: {test_file}")

def test_performance():
    """性能测试"""
    print(f"\n⚡ 性能测试")
    print("=" * 50)
    
    engine = AdvancedMaskEngine()
    
    # 测试不同掩码的性能
    test_cases = [
        ("?d?d?d?d", "4位数字"),
        ("?l?l?l?l", "4位小写字母"),
        ("?l?l?l?d?d?d", "3字母+3数字"),
        ("?u?l?l?l?d?d?d", "1大写+3小写+3数字"),
    ]
    
    for mask, description in test_cases:
        charset_list = engine.parse_mask(mask)
        total_combinations = 1
        for charset in charset_list:
            if isinstance(charset, str):
                total_combinations *= len(charset)
        
        print(f"掩码 '{mask}' ({description}): {total_combinations:,} 个组合")
        
        # 估算破解时间 (假设每秒1000次尝试)
        estimated_time = total_combinations / 1000
        if estimated_time < 60:
            time_str = f"{estimated_time:.1f} 秒"
        elif estimated_time < 3600:
            time_str = f"{estimated_time/60:.1f} 分钟"
        else:
            time_str = f"{estimated_time/3600:.1f} 小时"
        
        print(f"  预计破解时间: {time_str}")

def test_advanced_features():
    """测试高级功能"""
    print(f"\n🎯 高级功能测试")
    print("=" * 50)
    
    engine = AdvancedMaskEngine()
    
    # 测试扩展字符集
    print("扩展字符集测试:")
    extended_charsets = {
        '?h': '十六进制小写',
        '?H': '十六进制大写', 
        '?x': '十六进制',
        '?k': '键盘特殊字符',
        '?y': '元音字母',
        '?Y': '辅音字母',
    }
    
    for charset_code, description in extended_charsets.items():
        if charset_code in engine.charsets:
            charset = engine.charsets[charset_code]
            print(f"  {charset_code} ({description}): {len(charset)} 个字符")
    
    # 测试智能字符集
    print("\n智能字符集测试:")
    for charset_code, charset in engine.smart_charsets.items():
        print(f"  {charset_code}: {len(charset)} 个字符")
    
    # 测试复杂度计算
    print("\n字符集复杂度测试:")
    test_charsets = [
        ("0123456789", "纯数字"),
        ("abcdefghijklmnopqrstuvwxyz", "小写字母"),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZ", "大写字母"),
        ("!@#$%^&*()_+-=", "特殊字符"),
    ]
    
    for charset, description in test_charsets:
        complexity = engine.calculate_charset_complexity(charset)
        print(f"  {description}: 复杂度 {complexity:.2f}")

if __name__ == "__main__":
    print("🎮 高级掩码破解引擎测试套件")
    print("=" * 60)
    
    try:
        # 基础功能测试
        test_mask_engine()
        
        # 性能测试
        test_performance()
        
        # 高级功能测试
        test_advanced_features()
        
        print(f"\n🎉 所有测试完成!")
        
    except Exception as e:
        print(f"❌ 测试过程中出现错误: {e}")
        import traceback
        traceback.print_exc() 