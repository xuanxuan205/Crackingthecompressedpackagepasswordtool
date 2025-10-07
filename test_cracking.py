#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证密码破解工具的所有功能
包括暴力破解、经典破解、掩码破解、暂停和停止功能
"""

import os
import sys
import time
import threading
import zipfile
import tempfile
import shutil

# 添加项目路径到sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def create_test_zip():
    """创建测试用的ZIP文件"""
    test_dir = tempfile.mkdtemp()
    test_file = os.path.join(test_dir, "test.txt")
    
    # 创建测试文件
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("这是一个测试文件，用于验证密码破解功能。\n")
        f.write("如果能看到这个内容，说明密码破解成功！\n")
    
    # 创建带密码的ZIP文件
    zip_path = "test_password_123.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(test_file, "test.txt")
    
    # 重新创建带密码的ZIP文件
    import subprocess
    try:
        # 使用7zip命令行工具创建带密码的ZIP
        cmd = f'7z a -p"password123" "{zip_path}" "{test_file}"'
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
    except:
        # 如果7zip不可用，创建一个简单的测试文件
        with open(zip_path, 'wb') as f:
            f.write(b'PK\x03\x04\x14\x00\x00\x00\x08\x00')
        print("注意：创建了模拟ZIP文件用于测试")
    
    # 清理临时文件
    shutil.rmtree(test_dir)
    
    print(f"已创建测试ZIP文件: {zip_path}")
    print("密码: password123")
    return zip_path

def test_brute_force():
    """测试暴力破解功能"""
    print("\n=== 测试暴力破解功能 ===")
    
    from cracker.zip_cracker import crack
    
    # 创建测试文件
    test_file = create_test_zip()
    
    # 创建事件对象
    stop_event = threading.Event()
    pause_event = threading.Event()
    
    def log_callback(msg):
        print(f"[LOG] {msg}")
    
    def progress_callback(current, total, status):
        if total > 0:
            percent = int(current * 100 / total)
            print(f"[进度] {percent}% - {status}")
        else:
            print(f"[进度] {current} - {status}")
    
    try:
        # 测试暴力破解
        print("开始暴力破解测试...")
        result = crack(
            file_path=test_file,
            mode="brute",
            log_callback=log_callback,
            progress_callback=progress_callback,
            min_length=1,
            max_length=6,
            charset="数字",
            stop_event=stop_event,
            pause_event=pause_event
        )
        
        if result.get('success'):
            print(f"✅ 暴力破解成功！密码: {result.get('password')}")
        else:
            print(f"❌ 暴力破解失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 暴力破解测试出错: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def test_dictionary_attack():
    """测试字典攻击功能"""
    print("\n=== 测试字典攻击功能 ===")
    
    from cracker.zip_cracker import crack
    
    # 创建测试文件
    test_file = create_test_zip()
    
    # 创建事件对象
    stop_event = threading.Event()
    pause_event = threading.Event()
    
    def log_callback(msg):
        print(f"[LOG] {msg}")
    
    def progress_callback(current, total, status):
        if total > 0:
            percent = int(current * 100 / total)
            print(f"[进度] {percent}% - {status}")
        else:
            print(f"[进度] {current} - {status}")
    
    try:
        # 测试字典攻击
        print("开始字典攻击测试...")
        result = crack(
            file_path=test_file,
            mode="dict",
            log_callback=log_callback,
            progress_callback=progress_callback,
            stop_event=stop_event,
            pause_event=pause_event
        )
        
        if result.get('success'):
            print(f"✅ 字典攻击成功！密码: {result.get('password')}")
        else:
            print(f"❌ 字典攻击失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 字典攻击测试出错: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def test_mask_attack():
    """测试掩码攻击功能"""
    print("\n=== 测试掩码攻击功能 ===")
    
    from cracker.zip_cracker import crack
    
    # 创建测试文件
    test_file = create_test_zip()
    
    # 创建事件对象
    stop_event = threading.Event()
    pause_event = threading.Event()
    
    def log_callback(msg):
        print(f"[LOG] {msg}")
    
    def progress_callback(current, total, status):
        if total > 0:
            percent = int(current * 100 / total)
            print(f"[进度] {percent}% - {status}")
        else:
            print(f"[进度] {current} - {status}")
    
    try:
        # 测试掩码攻击
        print("开始掩码攻击测试...")
        result = crack(
            file_path=test_file,
            mode="mask",
            mask="?l?l?l?l?l?l?l?l?d?d?d",  # password123
            log_callback=log_callback,
            progress_callback=progress_callback,
            stop_event=stop_event,
            pause_event=pause_event
        )
        
        if result.get('success'):
            print(f"✅ 掩码攻击成功！密码: {result.get('password')}")
        else:
            print(f"❌ 掩码攻击失败: {result.get('message')}")
            
    except Exception as e:
        print(f"❌ 掩码攻击测试出错: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def test_pause_stop():
    """测试暂停和停止功能"""
    print("\n=== 测试暂停和停止功能 ===")
    
    from cracker.zip_cracker import crack
    
    # 创建测试文件
    test_file = create_test_zip()
    
    # 创建事件对象
    stop_event = threading.Event()
    pause_event = threading.Event()
    
    def log_callback(msg):
        print(f"[LOG] {msg}")
    
    def progress_callback(current, total, status):
        if total > 0:
            percent = int(current * 100 / total)
            print(f"[进度] {percent}% - {status}")
        else:
            print(f"[进度] {current} - {status}")
    
    try:
        # 在后台线程中运行破解
        def run_crack():
            result = crack(
                file_path=test_file,
                mode="brute",
                log_callback=log_callback,
                progress_callback=progress_callback,
                min_length=1,
                max_length=8,
                charset="数字",
                stop_event=stop_event,
                pause_event=pause_event
            )
            return result
        
        # 启动破解线程
        crack_thread = threading.Thread(target=run_crack)
        crack_thread.start()
        
        # 等待一段时间后暂停
        time.sleep(2)
        print("🔄 暂停破解...")
        pause_event.set()
        
        # 等待一段时间后恢复
        time.sleep(2)
        print("▶️ 恢复破解...")
        pause_event.clear()
        
        # 等待一段时间后停止
        time.sleep(2)
        print("⏹️ 停止破解...")
        stop_event.set()
        
        # 等待线程结束
        crack_thread.join()
        print("✅ 暂停和停止功能测试完成")
        
    except Exception as e:
        print(f"❌ 暂停和停止功能测试出错: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def test_advanced_engine():
    """测试高级破解引擎"""
    print("\n=== 测试高级破解引擎 ===")
    
    from cracker.advanced_engine import AdvancedCracker
    
    # 创建测试文件
    test_file = create_test_zip()
    
    # 创建事件对象
    stop_event = threading.Event()
    pause_event = threading.Event()
    
    def progress_callback(current, total, status):
        if total > 0:
            percent = int(current * 100 / total)
            print(f"[进度] {percent}% - {status}")
        else:
            print(f"[进度] {current} - {status}")
    
    try:
        # 创建高级破解引擎
        engine = AdvancedCracker()
        
        # 测试暴力破解
        print("开始高级引擎暴力破解测试...")
        result = engine.brute_force_advanced(
            file_path=test_file,
            min_len=1,
            max_len=6,
            charset="数字",
            callback=progress_callback,
            stop_event=stop_event,
            pause_event=pause_event
        )
        
        if result:
            print(f"✅ 高级引擎暴力破解成功！密码: {result}")
        else:
            print("❌ 高级引擎暴力破解失败")
            
    except Exception as e:
        print(f"❌ 高级引擎测试出错: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(test_file):
            os.remove(test_file)

def main():
    """主测试函数"""
    print("🔧 密码破解工具功能测试")
    print("=" * 50)
    
    # 测试各个功能
    test_brute_force()
    test_dictionary_attack()
    test_mask_attack()
    test_pause_stop()
    test_advanced_engine()
    
    print("\n" + "=" * 50)
    print("🎉 所有测试完成！")

if __name__ == "__main__":
    main() 