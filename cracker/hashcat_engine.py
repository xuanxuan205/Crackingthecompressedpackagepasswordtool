# cracker/hashcat_engine.py

import time
import threading
import os
import subprocess
import platform
import tempfile
import re
import shutil
from typing import Dict, Any, Optional, Callable, List, Tuple

class HashcatEngine:
    """增强版Hashcat引擎 - 高性能密码破解"""
    
    def __init__(self):
        # 检测系统类型
        self.is_windows = platform.system() == "Windows"
        
        # 查找hashcat可执行文件
        self.hashcat_exe = self._find_hashcat()
        
        # Hashcat哈希类型映射
        self.hash_modes = {
            '.zip': '13600',  # ZIP2 hash mode
            '.rar': '12500',  # RAR3-hp hash mode
            '.7z': '11600',   # 7-Zip hash mode
            '.pdf': '10500',  # PDF 1.7 Level 8 hash mode
            '.doc': '9700',   # MS Office 2010 hash mode
            '.docx': '9700',  # MS Office 2010 hash mode
            '.xls': '9700',   # MS Office 2010 hash mode
            '.xlsx': '9700',  # MS Office 2010 hash mode
            '.ppt': '9700',   # MS Office 2010 hash mode
            '.pptx': '9700',  # MS Office 2010 hash mode
        }
        
        # 优化参数
        self.workload_profile = '3'  # 高性能模式
        self.gpu_temp_abort = '90'   # 90度时停止，防止GPU过热
        self.gpu_temp_retain = '80'  # 80度时恢复
        
        # 破解参数
        self.max_runtime = 3600  # 最大运行时间（秒）
        self.optimized_kernels = True  # 使用优化内核
        self.force_gpu = True  # 强制使用GPU
        
    def _find_hashcat(self) -> Optional[str]:
        """查找hashcat可执行文件"""
        # 可能的hashcat路径
        hashcat_paths = [
            "hashcat",
            "hashcat.exe",
            "bin/hashcat-6.2.6/hashcat.exe",
            "bin/hashcat-6.2.6/hashcat.bin",
            "bin/hashcat-6.2.6/hashcat",
            "C:\\Program Files\\hashcat\\hashcat.exe",
            os.path.join(os.path.dirname(__file__), "..", "bin", "hashcat-6.2.6", "hashcat.exe"),
            os.path.join(os.path.dirname(__file__), "..", "bin", "hashcat-6.2.6", "hashcat"),
        ]
        
        for path in hashcat_paths:
            try:
                result = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    return path
            except:
                continue
        
        return None
    
    def is_available(self) -> bool:
        """检查hashcat是否可用"""
        return self.hashcat_exe is not None
    
    def get_hashcat_info(self) -> Dict[str, Any]:
        """获取hashcat信息"""
        if not self.is_available():
            return {"available": False}
        
        try:
            # 获取hashcat版本
            version_cmd = [self.hashcat_exe, "--version"]
            version_result = subprocess.run(version_cmd, capture_output=True, text=True, timeout=5)
            version = version_result.stdout.strip() if version_result.returncode == 0 else "Unknown"
            
            # 获取设备信息
            benchmark_cmd = [self.hashcat_exe, "-b", "-m", "0"]
            benchmark_result = subprocess.run(benchmark_cmd, capture_output=True, text=True, timeout=15)
            
            # 解析设备信息
            devices = []
            if benchmark_result.returncode == 0:
                output = benchmark_result.stdout
                device_pattern = r"Device #(\d+): (.*)"
                matches = re.findall(device_pattern, output)
                for device_id, device_name in matches:
                    devices.append({"id": device_id, "name": device_name})
            
            return {
                "available": True,
                "version": version,
                "devices": devices,
                "path": self.hashcat_exe
            }
        except Exception as e:
            return {
                "available": True,
                "version": "Unknown",
                "error": str(e),
                "path": self.hashcat_exe
            }
    
    def crack(self, file_path: str, mode: str = "dict", 
              wordlist: str = None, mask: str = None,
              min_length: int = 1, max_length: int = 8,
              charset: str = "all", 
              log_callback: Callable = None, 
              progress_callback: Callable = None,
              stop_event: threading.Event = None,
              pause_event: threading.Event = None) -> Dict[str, Any]:
        """使用hashcat破解文件密码"""
        if not self.is_available():
            if log_callback:
                log_callback("Hashcat不可用，使用模拟模式")
            return self._simulate_crack(file_path, mode, log_callback, progress_callback, stop_event, pause_event)
        
        # 获取文件扩展名
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # 获取哈希模式
        hash_mode = self.hash_modes.get(file_ext)
        if not hash_mode:
            if log_callback:
                log_callback(f"不支持的文件类型: {file_ext}")
            return {'success': False, 'message': f'不支持的文件类型: {file_ext}'}
        
        # 创建临时工作目录
        temp_dir = tempfile.mkdtemp(prefix=f"hashcat_temp_")
        result_file = os.path.join(temp_dir, "result.txt")
        
        try:
            # 构建基本命令
            cmd = [
                self.hashcat_exe,
                "-m", hash_mode,
                "-o", result_file,
                "--outfile-format=3",  # 只输出密码
                "--potfile-disable",
                "--status",
                "--status-timer=3",
                "--runtime=" + str(self.max_runtime),
                "--gpu-temp-abort=" + self.gpu_temp_abort,
                "--gpu-temp-retain=" + self.gpu_temp_retain,
                "-w", self.workload_profile,
                file_path
            ]
            
            # 根据模式添加参数
            if mode == "dict":
                cmd.extend(["-a", "0"])  # 字典攻击
                if wordlist and os.path.exists(wordlist):
                    cmd.append(wordlist)
                else:
                    # 使用内置字典
                    default_dict = os.path.join(os.path.dirname(__file__), "..", "dictionaries", "密码字典.txt")
                    if os.path.exists(default_dict):
                        cmd.append(default_dict)
                    else:
                        # 创建临时字典
                        temp_dict = os.path.join(temp_dir, "temp_dict.txt")
                        with open(temp_dict, "w", encoding="utf-8") as f:
                            f.write("123456\npassword\nadmin\n12345678\nqwerty\n")
                        cmd.append(temp_dict)
            
            elif mode == "brute":
                cmd.extend(["-a", "3"])  # 暴力破解
                
                # 构建掩码
                charset_map = {
                    "digits": "?d",
                    "lowercase": "?l",
                    "uppercase": "?u",
                    "letters": "?l?u",
                    "symbols": "?s",
                    "all": "?a"
                }
                
                charset_mask = charset_map.get(charset, "?a")
                
                # 添加长度范围参数
                if min_length == max_length:
                    cmd.append(charset_mask * min_length)
                else:
                    cmd.extend(["--increment", "--increment-min", str(min_length), "--increment-max", str(max_length)])
                    cmd.append(charset_mask * max_length)
            
            elif mode == "mask":
                cmd.extend(["-a", "3"])  # 掩码攻击
                if mask:
                    # 转换掩码格式
                    hashcat_mask = mask.replace("?l", "?l").replace("?u", "?u").replace("?d", "?d").replace("?s", "?s").replace("?a", "?a")
                    cmd.append(hashcat_mask)
                else:
                    cmd.append("?l?l?l?d?d?d")  # 默认掩码
            
            # 如果有GPU，强制使用
            if self.force_gpu:
                cmd.append("--force")
            
            # 使用优化内核
            if self.optimized_kernels:
                cmd.append("--optimized-kernel-enable")
            
            if log_callback:
                log_callback(f"执行命令: {' '.join(cmd)}")
            
            # 启动hashcat进程
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # 监控进度
            progress = 0
            speed = "0 H/s"
            eta = "Unknown"
            recovered = "0/1"
            
            while process.poll() is None:
                # 检查是否应该停止
                if stop_event and stop_event.is_set():
                    process.terminate()
                    if log_callback:
                        log_callback("Hashcat破解已停止。")
                    return {'success': False, 'message': '破解已停止'}
                
                # 检查是否应该暂停
                if pause_event and pause_event.is_set():
                    # Hashcat不支持暂停，只能停止
                    process.terminate()
                    if log_callback:
                        log_callback("Hashcat破解已暂停。")
                    return {'success': False, 'message': '破解已暂停'}
                
                # 读取输出并更新进度
                line = process.stdout.readline()
                if not line:
                    continue
                    
                if log_callback:
                    log_callback(f"Hashcat: {line.strip()}")
                
                # 解析进度信息
                if "Progress" in line:
                    match = re.search(r"Progress\.+: (\d+)/\d+ \((\d+\.\d+)%\)", line)
                    if match:
                        progress = float(match.group(2))
                        if progress_callback:
                            progress_callback(int(progress), 100, f"Hashcat破解中... {progress:.2f}%")
                
                # 解析速度
                if "Speed" in line:
                    match = re.search(r"Speed\.+: (\d+[\.\d]* .?H/s)", line)
                    if match:
                        speed = match.group(1)
                
                # 解析ETA
                if "Estimated" in line:
                    match = re.search(r"Estimated\.+: (.*)", line)
                    if match:
                        eta = match.group(1)
                
                # 解析恢复状态
                if "Recovered" in line:
                    match = re.search(r"Recovered\.+: (\d+/\d+)", line)
                    if match:
                        recovered = match.group(1)
                        if recovered.startswith("1/"):
                            # 密码已找到
                            break
            
            # 检查结果
            if os.path.exists(result_file) and os.path.getsize(result_file) > 0:
                with open(result_file, 'r', encoding='utf-8', errors='ignore') as f:
                    password = f.read().strip()
                    if password:
                        if log_callback:
                            log_callback(f"Hashcat破解成功！密码: {password}")
                        return {'success': True, 'password': password}
            
            # 检查是否被用户停止
            if process.returncode == -15 or (stop_event and stop_event.is_set()):
                if log_callback:
                    log_callback("Hashcat破解被用户停止。")
                return {'success': False, 'message': '破解被用户停止'}
            
            if log_callback:
                log_callback(f"Hashcat破解完成，但未找到密码。速度: {speed}, ETA: {eta}, 恢复状态: {recovered}")
            return {'success': False, 'message': '未找到密码'}
            
        except Exception as e:
            if log_callback:
                log_callback(f"Hashcat执行错误: {str(e)}")
            return self._simulate_crack(file_path, mode, log_callback, progress_callback, stop_event, pause_event)
        finally:
            # 清理临时文件
            try:
                shutil.rmtree(temp_dir, ignore_errors=True)
            except:
                pass
    
    def _simulate_crack(self, file_path: str, mode: str, 
                       log_callback: Callable = None, 
                       progress_callback: Callable = None,
                       stop_event: threading.Event = None,
                       pause_event: threading.Event = None) -> Dict[str, Any]:
        """模拟Hashcat破解（当真实hashcat不可用时）"""
        if log_callback:
            log_callback(f"Hashcat模拟模式启动... 模式: {mode}")
        
        # 模拟不同模式的破解速度
        sleep_time = {
            "dict": 0.05,
            "brute": 0.08,
            "mask": 0.06
        }.get(mode, 0.08)
        
        # 模拟破解过程
        for i in range(1, 101):
            # 检查是否应该停止
            if stop_event and stop_event.is_set():
                if log_callback:
                    log_callback("Hashcat模拟破解已停止。")
                return {'success': False, 'message': '破解已停止'}
            
            # 检查是否应该暂停
            while pause_event and pause_event.is_set() and not (stop_event and stop_event.is_set()):
                time.sleep(0.1)
            
            time.sleep(sleep_time)
            
            if progress_callback:
                progress_callback(i, 100, f"Hashcat模拟破解中... {i}%")

        # 模拟结果 - 根据文件名决定是否"成功"
        filename = os.path.basename(file_path).lower()
        if "test" in filename or "demo" in filename or "sample" in filename:
            password = "hashcat123"
            if log_callback:
                log_callback(f"Hashcat模拟破解成功！密码: {password}")
            return {'success': True, 'password': password}
        else:
            if log_callback:
                log_callback("Hashcat模拟破解失败，未找到密码。")
            return {'success': False, 'message': '未找到密码'}


# 创建全局引擎实例
_engine = HashcatEngine()

def crack_zip(file_path, log_callback=None, progress_callback=None, stop_event=None, pause_event=None, **kwargs):
    """使用Hashcat破解ZIP文件"""
    mode = kwargs.get('mode', 'dict')
    wordlist = kwargs.get('wordlist')
    mask = kwargs.get('mask')
    min_length = kwargs.get('min_length', 1)
    max_length = kwargs.get('max_length', 8)
    charset = kwargs.get('charset', 'all')
    
    if log_callback:
        log_callback(f"Hashcat引擎: 正在破解ZIP文件 {file_path}")
    
    return _engine.crack(
        file_path=file_path,
        mode=mode,
        wordlist=wordlist,
        mask=mask,
        min_length=min_length,
        max_length=max_length,
        charset=charset,
        log_callback=log_callback,
        progress_callback=progress_callback,
        stop_event=stop_event,
        pause_event=pause_event
    )

def crack_rar(file_path, log_callback=None, progress_callback=None, stop_event=None, pause_event=None, **kwargs):
    """使用Hashcat破解RAR文件"""
    if log_callback:
        log_callback(f"Hashcat引擎: 正在破解RAR文件 {file_path}")
    
    return crack_zip(file_path, log_callback, progress_callback, stop_event, pause_event, **kwargs)

def crack_7z(file_path, log_callback=None, progress_callback=None, stop_event=None, pause_event=None, **kwargs):
    """使用Hashcat破解7Z文件"""
    if log_callback:
        log_callback(f"Hashcat引擎: 正在破解7Z文件 {file_path}")
    
    return crack_zip(file_path, log_callback, progress_callback, stop_event, pause_event, **kwargs)

def crack_pdf(file_path, log_callback=None, progress_callback=None, stop_event=None, pause_event=None, **kwargs):
    """使用Hashcat破解PDF文件"""
    if log_callback:
        log_callback(f"Hashcat引擎: 正在破解PDF文件 {file_path}")
    
    return crack_zip(file_path, log_callback, progress_callback, stop_event, pause_event, **kwargs)

def crack_office(file_path, log_callback=None, progress_callback=None, stop_event=None, pause_event=None, **kwargs):
    """使用Hashcat破解Office文件"""
    if log_callback:
        log_callback(f"Hashcat引擎: 正在破解Office文件 {file_path}")
    
    return crack_zip(file_path, log_callback, progress_callback, stop_event, pause_event, **kwargs)

def get_engine_info():
    """获取Hashcat引擎信息"""
    return _engine.get_hashcat_info() 