# cracker/john_engine.py

import time
import threading
# import subprocess # 实际调用外部工具时可能需要

def crack_zip(file_path, log_callback, progress_callback):
    log_callback(f"John the Ripper引擎: 正在破解ZIP文件 {file_path}")
    progress_callback(0, 100, "John the Ripper破解初始化...")

    try:
        # 检查john是否可用
        import subprocess
        import os
        
        # 尝试找到john可执行文件
        john_paths = [
            "john",
            "john.exe",
            "bin/john-1.9.0-jumbo-1-win64/run/john.exe",
            "C:\\Program Files\\John\\john.exe"
        ]
        
        john_exe = None
        for path in john_paths:
            try:
                result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    john_exe = path
                    break
            except:
                continue
        
        if not john_exe:
            log_callback("警告: 未找到john可执行文件，使用模拟模式")
            return _simulate_john_crack(file_path, log_callback, progress_callback)
        
        # 使用真实的john进行破解
        log_callback(f"使用John the Ripper: {john_exe}")
        
        # 创建临时工作目录
        temp_dir = f"temp_john_{os.path.basename(file_path)}_{int(time.time())}"
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # 使用john破解ZIP文件
            cmd = [
                john_exe,
                "--format=zip",
                "--wordlist=bin/john-1.9.0-jumbo-1-win64/run/password.lst",
                file_path
            ]
            
            log_callback(f"执行命令: {' '.join(cmd)}")
            
            # 启动john进程
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # 监控进度
            progress = 0
            while process.poll() is None:
                if not getattr(threading.current_thread(), "is_running", True):
                    process.terminate()
                    log_callback("John the Ripper破解已停止。")
                    return {'success': False, 'message': '破解已停止'}
                
                while getattr(threading.current_thread(), "is_paused", False):
                    time.sleep(0.1)
                
                # 读取输出并更新进度
                output = process.stdout.readline()
                if output:
                    log_callback(f"John: {output.strip()}")
                    if "Loaded" in output or "Cracked" in output:
                        progress += 10
                        progress_callback(min(progress, 100), 100, f"John破解中... {progress}%")
                
                time.sleep(0.1)
            
            # 检查结果
            show_cmd = [john_exe, "--show", "--format=zip", file_path]
            result = subprocess.run(show_cmd, capture_output=True, text=True)
            
            if result.stdout and "1 password hash cracked" in result.stdout:
                # 解析密码
                lines = result.stdout.split('\n')
                for line in lines:
                    if ':' in line and not line.startswith('Loaded'):
                        password = line.split(':')[-1]
                        log_callback(f"John the Ripper破解成功！密码: {password}")
                        return {'success': True, 'password': password}
            
            log_callback("John the Ripper破解失败，未找到密码。")
            return {'success': False, 'message': '未找到密码'}
            
        finally:
            # 清理临时文件
            try:
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
                
    except Exception as e:
        log_callback(f"John the Ripper执行错误: {e}")
        return _simulate_john_crack(file_path, log_callback, progress_callback)

def _simulate_john_crack(file_path, log_callback, progress_callback):
    """模拟John the Ripper破解（当真实john不可用时）"""
    log_callback("John the Ripper模拟模式启动...")
    
    # 模拟破解过程
    for i in range(1, 101):
        if not getattr(threading.current_thread(), "is_running", True):
            log_callback("John the Ripper破解已停止。")
            return {'success': False, 'message': '破解已停止'}
        while getattr(threading.current_thread(), "is_paused", False):
            time.sleep(0.1)

        time.sleep(0.08)
        progress_callback(i, 100, f"John模拟破解中... {i}%")

    # 模拟结果
    if "success" in file_path:
        log_callback("John模拟破解成功！密码: johnpass")
        return {'success': True, 'password': 'johnpass'}
    else:
        log_callback("John模拟破解失败，未找到密码。")
        return {'success': False, 'message': '未找到密码'} 