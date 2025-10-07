import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import os
from typing import Optional, Callable
import queue

class CrackWindow:
    """密码破解专用窗口 - 绿色字体主题"""
    
    def __init__(self, parent=None, file_path: str = None, crack_mode: str = "brute", auto_start: bool = True, **kwargs):
        self.parent = parent
        self.file_path = file_path
        self.crack_mode = crack_mode
        self.kwargs = kwargs
        self.auto_start = auto_start
        
        # 破解状态
        self.is_running = False
        self.is_paused = False
        self.found_password = None
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        
        # 消息队列用于线程间通信
        self.message_queue = queue.Queue()
        
        # 创建窗口
        self.create_window()
        
        # 启动消息处理线程
        self.message_thread = threading.Thread(target=self.process_messages, daemon=True)
        self.message_thread.start()
        
        # 如果设置了自动启动，则自动开始破解
        if self.auto_start and self.file_path:
            self.log_message("破解窗口已创建，将在1秒后自动开始破解...", "INFO")
            self.window.after(1000, self.start_crack)  # 延迟1秒启动，让窗口完全显示
    
    def create_window(self):
        """创建破解窗口"""
        # 创建顶级窗口
        self.window = tk.Toplevel(self.parent) if self.parent else tk.Tk()
        self.window.title("🔓 密码破解进行中...")
        self.window.geometry("800x600")
        self.window.resizable(True, True)
        
        # 设置窗口图标（如果有的话）
        try:
            if os.path.exists("icon.ico"):
                self.window.iconbitmap("icon.ico")
        except:
            pass
        
        # 配置绿色主题
        self.setup_green_theme()
        
        # 创建界面元素
        self.create_widgets()
        
        # 绑定窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
        
        # 居中显示窗口
        self.center_window()
    
    def setup_green_theme(self):
        """设置绿色主题"""
        # 配置绿色主题颜色
        self.green_colors = {
            'bg_dark': '#0a0a0a',      # 深色背景
            'bg_medium': '#1a1a1a',    # 中等背景
            'bg_light': '#2a2a2a',     # 浅色背景
            'text_green': '#00ff00',   # 绿色文字
            'text_light_green': '#00cc00',  # 浅绿色文字
            'text_bright_green': '#00ff88', # 亮绿色文字
            'accent_green': '#00ff44', # 强调绿色
            'border_green': '#00aa00'  # 边框绿色
        }
        
        # 应用主题到窗口
        self.window.configure(bg=self.green_colors['bg_dark'])
        
        # 配置文本标签样式
        self.window.option_add('*Label.background', self.green_colors['bg_dark'])
        self.window.option_add('*Label.foreground', self.green_colors['text_green'])
        self.window.option_add('*Label.font', ('Consolas', 10))
        
        # 配置按钮样式
        self.window.option_add('*Button.background', self.green_colors['bg_medium'])
        self.window.option_add('*Button.foreground', self.green_colors['text_green'])
        self.window.option_add('*Button.font', ('Consolas', 9, 'bold'))
        self.window.option_add('*Button.relief', 'flat')
        self.window.option_add('*Button.borderwidth', '1')
    
    def create_widgets(self):
        """创建界面元素"""
        # 主框架
        main_frame = tk.Frame(self.window, bg=self.green_colors['bg_dark'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 标题区域
        title_frame = tk.Frame(main_frame, bg=self.green_colors['bg_dark'])
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = tk.Label(title_frame, 
                              text="🔓 密码破解引擎启动中...", 
                              font=('Consolas', 16, 'bold'),
                              fg=self.green_colors['text_bright_green'],
                              bg=self.green_colors['bg_dark'])
        title_label.pack()
        
        # 文件信息区域
        file_frame = tk.LabelFrame(main_frame, text="📁 目标文件", 
                                  fg=self.green_colors['text_green'],
                                  bg=self.green_colors['bg_dark'],
                                  font=('Consolas', 10, 'bold'))
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        if self.file_path:
            file_name = os.path.basename(self.file_path)
            file_info = tk.Label(file_frame, 
                                text=f"文件: {file_name}\n路径: {self.file_path}",
                                fg=self.green_colors['text_light_green'],
                                bg=self.green_colors['bg_dark'],
                                font=('Consolas', 9),
                                justify=tk.LEFT)
            file_info.pack(padx=10, pady=5, anchor=tk.W)
        
        # 破解模式信息
        mode_frame = tk.LabelFrame(main_frame, text="⚙️ 破解模式", 
                                  fg=self.green_colors['text_green'],
                                  bg=self.green_colors['bg_dark'],
                                  font=('Consolas', 10, 'bold'))
        mode_frame.pack(fill=tk.X, pady=(0, 10))
        
        mode_text = self.get_mode_description()
        mode_info = tk.Label(mode_frame, 
                            text=mode_text,
                            fg=self.green_colors['text_light_green'],
                            bg=self.green_colors['bg_dark'],
                            font=('Consolas', 9),
                            justify=tk.LEFT)
        mode_info.pack(padx=10, pady=5, anchor=tk.W)
        
        # 进度区域
        progress_frame = tk.LabelFrame(main_frame, text="📊 破解进度", 
                                      fg=self.green_colors['text_green'],
                                      bg=self.green_colors['bg_dark'],
                                      font=('Consolas', 10, 'bold'))
        progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 进度条
        self.progress_bar = ttk.Progressbar(progress_frame, 
                                           mode='determinate', 
                                           length=600,
                                           style='Green.Horizontal.TProgressbar')
        self.progress_bar.pack(padx=10, pady=5)
        
        # 进度文本
        self.progress_text = tk.Label(progress_frame, 
                                     text="准备开始破解...",
                                     fg=self.green_colors['text_bright_green'],
                                     bg=self.green_colors['bg_dark'],
                                     font=('Consolas', 10, 'bold'))
        self.progress_text.pack(pady=5)
        
        # 统计信息
        stats_frame = tk.Frame(progress_frame, bg=self.green_colors['bg_dark'])
        stats_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.attempts_label = tk.Label(stats_frame, 
                                      text="尝试次数: 0",
                                      fg=self.green_colors['text_light_green'],
                                      bg=self.green_colors['bg_dark'],
                                      font=('Consolas', 9))
        self.attempts_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.speed_label = tk.Label(stats_frame, 
                                   text="破解速度: 0 pwd/s",
                                   fg=self.green_colors['text_light_green'],
                                   bg=self.green_colors['bg_dark'],
                                   font=('Consolas', 9))
        self.speed_label.pack(side=tk.LEFT, padx=(0, 20))
        
        self.time_label = tk.Label(stats_frame, 
                                  text="运行时间: 00:00:00",
                                  fg=self.green_colors['text_light_green'],
                                  bg=self.green_colors['bg_dark'],
                                  font=('Consolas', 9))
        self.time_label.pack(side=tk.LEFT)
        
        # 控制按钮区域
        control_frame = tk.Frame(main_frame, bg=self.green_colors['bg_dark'])
        control_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 按钮样式
        button_style = {
            'bg': self.green_colors['bg_medium'],
            'fg': self.green_colors['text_green'],
            'font': ('Consolas', 10, 'bold'),
            'relief': 'flat',
            'borderwidth': 1,
            'padx': 15,
            'pady': 5
        }
        
        self.start_btn = tk.Button(control_frame, text="🚀 开始破解", 
                                  command=self.start_crack, **button_style)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.pause_btn = tk.Button(control_frame, text="⏸️ 暂停", 
                                  command=self.toggle_pause, state=tk.DISABLED, **button_style)
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(control_frame, text="⏹️ 停止", 
                                 command=self.stop_crack, state=tk.DISABLED, **button_style)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # 实时日志区域
        log_frame = tk.LabelFrame(main_frame, text="📝 破解日志", 
                                 fg=self.green_colors['text_green'],
                                 bg=self.green_colors['bg_dark'],
                                 font=('Consolas', 10, 'bold'))
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # 日志文本框
        self.log_text = tk.Text(log_frame, 
                               height=12,
                               bg=self.green_colors['bg_medium'],
                               fg=self.green_colors['text_green'],
                               font=('Consolas', 9),
                               insertbackground=self.green_colors['text_green'],
                               selectbackground=self.green_colors['accent_green'],
                               relief='flat',
                               borderwidth=1)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 滚动条
        scrollbar = tk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_text.config(yscrollcommand=scrollbar.set)
        
        # 结果区域
        result_frame = tk.LabelFrame(main_frame, text="🎯 破解结果", 
                                    fg=self.green_colors['text_green'],
                                    bg=self.green_colors['bg_dark'],
                                    font=('Consolas', 10, 'bold'))
        result_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.result_text = tk.Text(result_frame, 
                                  height=3,
                                  bg=self.green_colors['bg_medium'],
                                  fg=self.green_colors['text_bright_green'],
                                  font=('Consolas', 12, 'bold'),
                                  insertbackground=self.green_colors['text_green'],
                                  relief='flat',
                                  borderwidth=1)
        self.result_text.pack(fill=tk.X, padx=5, pady=5)
        
        # 底部按钮
        bottom_frame = tk.Frame(main_frame, bg=self.green_colors['bg_dark'])
        bottom_frame.pack(fill=tk.X)
        
        self.copy_btn = tk.Button(bottom_frame, text="📋 复制密码", 
                                 command=self.copy_password, state=tk.DISABLED, **button_style)
        self.copy_btn.pack(side=tk.LEFT, padx=5)
        
        self.analyze_btn = tk.Button(bottom_frame, text="🔍 分析密码", 
                                    command=self.analyze_password, state=tk.DISABLED, **button_style)
        self.analyze_btn.pack(side=tk.LEFT, padx=5)
        
        self.close_btn = tk.Button(bottom_frame, text="❌ 关闭窗口", 
                                  command=self.close_window, **button_style)
        self.close_btn.pack(side=tk.RIGHT, padx=5)
        
        # 初始化统计变量
        self.start_time = None
        self.total_attempts = 0
        self.last_update_time = time.time()
        self.last_attempts = 0
    
    def get_mode_description(self):
        """获取破解模式描述"""
        mode_descriptions = {
            'brute': '暴力破解模式 - 尝试所有可能的密码组合',
            'dict': '字典破解模式 - 使用预定义密码字典',
            'mask': '掩码破解模式 - 使用密码模式进行破解',
            'ai': 'AI智能破解 - 使用人工智能预测密码',
            'hybrid': '混合破解模式 - 结合多种破解方法',
            'gpu': 'GPU加速破解 - 使用显卡加速计算',
            'distributed': '分布式破解 - 多机协同破解'
        }
        return mode_descriptions.get(self.crack_mode, '未知破解模式')
    
    def center_window(self):
        """居中显示窗口"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def log_message(self, message: str, level: str = "INFO"):
        """添加日志消息"""
        timestamp = time.strftime("%H:%M:%S")
        level_colors = {
            "INFO": self.green_colors['text_green'],
            "SUCCESS": self.green_colors['text_bright_green'],
            "WARNING": "#ffff00",
            "ERROR": "#ff0000"
        }
        
        color = level_colors.get(level, self.green_colors['text_green'])
        formatted_message = f"[{timestamp}] {level}: {message}\n"
        
        # 使用队列发送消息到主线程
        self.message_queue.put(("log", formatted_message, color))
    
    def update_progress(self, current: int, total: int, status: str = None):
        """更新进度显示"""
        if total > 0:
            percentage = (current / total) * 100
            self.progress_bar['value'] = percentage
        
        if status:
            self.message_queue.put(("progress", status))
        
        # 更新统计信息
        self.total_attempts = current
        current_time = time.time()
        
        if self.start_time:
            elapsed_time = current_time - self.start_time
            speed = (current - self.last_attempts) / (current_time - self.last_update_time) if current_time > self.last_update_time else 0
            
            self.message_queue.put(("stats", {
                'attempts': current,
                'speed': speed,
                'elapsed': elapsed_time
            }))
        
        self.last_update_time = current_time
        self.last_attempts = current
    
    def process_messages(self):
        """处理消息队列"""
        while True:
            try:
                msg_type, *args = self.message_queue.get(timeout=0.1)
                
                if msg_type == "log":
                    message, color = args
                    self.log_text.insert(tk.END, message)
                    # 设置最后插入文本的颜色
                    last_line_start = self.log_text.index("end-2c linestart")
                    last_line_end = self.log_text.index("end-1c")
                    self.log_text.tag_add(f"color_{color}", last_line_start, last_line_end)
                    self.log_text.tag_config(f"color_{color}", foreground=color)
                    self.log_text.see(tk.END)
                
                elif msg_type == "progress":
                    status = args[0]
                    self.progress_text.config(text=status)
                
                elif msg_type == "stats":
                    stats = args[0]
                    self.attempts_label.config(text=f"尝试次数: {stats['attempts']:,}")
                    self.speed_label.config(text=f"破解速度: {stats['speed']:.1f} pwd/s")
                    
                    elapsed = stats['elapsed']
                    hours = int(elapsed // 3600)
                    minutes = int((elapsed % 3600) // 60)
                    seconds = int(elapsed % 60)
                    self.time_label.config(text=f"运行时间: {hours:02d}:{minutes:02d}:{seconds:02d}")
                
                elif msg_type == "result":
                    password = args[0]
                    self.show_result(password)
                    # 通知主应用程序
                    self.notify_result(password)
                
            except queue.Empty:
                continue
            except Exception as e:
                print(f"消息处理错误: {e}")
    
    def show_result(self, password: str):
        """显示破解结果"""
        self.found_password = password
        self.result_text.delete(1.0, tk.END)
        result_message = f"🎉 密码破解成功！\n\n密码: {password}\n\n破解完成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}"
        self.result_text.insert(tk.END, result_message)
        
        # 启用结果相关按钮
        self.copy_btn.config(state=tk.NORMAL)
        self.analyze_btn.config(state=tk.NORMAL)
        
        # 更新标题
        self.window.title("✅ 密码破解完成")
        
        # 记录成功日志
        self.log_message(f"密码破解成功: {password}", "SUCCESS")
        
        # 通知主应用程序
        self.notify_result(password)
    
    def start_crack(self):
        """开始破解"""
        if not self.file_path or not os.path.exists(self.file_path):
            messagebox.showerror("错误", "请选择有效的文件")
            return
        
        self.is_running = True
        self.start_time = time.time()
        self.stop_event.clear()
        self.pause_event.clear()
        
        # 更新按钮状态
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
        
        # 清空结果
        self.result_text.delete(1.0, tk.END)
        self.copy_btn.config(state=tk.DISABLED)
        self.analyze_btn.config(state=tk.DISABLED)
        
        # 更新标题
        self.window.title("🔓 密码破解进行中...")
        
        # 记录开始日志
        self.log_message("开始密码破解...", "INFO")
        self.log_message(f"文件: {os.path.basename(self.file_path)}", "INFO")
        self.log_message(f"模式: {self.crack_mode}", "INFO")
        if self.auto_start:
            self.log_message("自动启动模式已启用", "SUCCESS")
        
        # 启动破解线程
        self.crack_thread = threading.Thread(target=self.run_crack, daemon=True)
        self.crack_thread.start()
    
    def run_crack(self):
        """运行破解逻辑"""
        try:
            # 根据文件类型和模式调用相应的破解引擎
            file_ext = self.kwargs.get('file_ext', '').lower()
            mode = self.crack_mode
            
            self.log_message(f"开始破解文件: {os.path.basename(self.file_path)}", "INFO")
            self.log_message(f"文件类型: {file_ext}", "INFO")
            self.log_message(f"破解模式: {mode}", "INFO")
            
            # 准备破解参数
            params = {
                'min_length': self.kwargs.get('min_length', 1),
                'max_length': self.kwargs.get('max_length', 8),
                'charset': self.kwargs.get('charset', 'all'),
                'mask': self.kwargs.get('mask', '?l?l?l?d?d?d'),
                'wordlist': self.kwargs.get('dict_file', ''),
                'log_callback': self.log_message,
                'progress_callback': self.update_progress,
                'stop_event': self.stop_event,
                'pause_event': self.pause_event
            }
            
            password = None
            
            # 根据文件类型选择破解器
            if file_ext == '.zip':
                from cracker.zip_cracker import crack as zip_crack
                result = zip_crack(self.file_path, mode, **params)
                password = result.get('password') if result.get('success') else None
            elif file_ext == '.rar':
                from cracker.rar_cracker import crack as rar_crack
                result = rar_crack(self.file_path, mode, **params)
                password = result.get('password') if result.get('success') else None
            elif file_ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
                from cracker.office_cracker import crack as office_crack
                result = office_crack(self.file_path, mode, **params)
                password = result.get('password') if result.get('success') else None
            elif file_ext == '.pdf':
                from cracker.pdf_cracker import crack as pdf_crack
                result = pdf_crack(self.file_path, mode, **params)
                password = result.get('password') if result.get('success') else None
            else:
                self.log_message(f"不支持的文件类型: {file_ext}", "ERROR")
                return
            
            # 处理结果
            if password:
                self.message_queue.put(("result", password))
                self.log_message(f"密码破解成功: {password}", "SUCCESS")
            else:
                self.log_message("未找到密码，破解失败", "WARNING")
                self.result_text.delete(1.0, tk.END)
                self.result_text.insert(tk.END, "❌ 破解失败\n\n未找到匹配的密码")
                
        except Exception as e:
            self.log_message(f"破解过程出错: {e}", "ERROR")
            import traceback
            self.log_message(f"详细错误: {traceback.format_exc()}", "ERROR")
        finally:
            # 重置UI状态
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.pause_btn.config(state=tk.DISABLED)
            self.stop_btn.config(state=tk.DISABLED)
    
    def set_result_callback(self, callback):
        """设置结果回调函数"""
        self.result_callback = callback
    
    def notify_result(self, password):
        """通知主应用程序破解结果"""
        if hasattr(self, 'result_callback') and self.result_callback:
            self.result_callback(password)
    
    def toggle_pause(self):
        """切换暂停状态"""
        if self.is_paused:
            self.pause_event.clear()
            self.is_paused = False
            self.pause_btn.config(text="⏸️ 暂停")
            self.log_message("破解已恢复", "INFO")
        else:
            self.pause_event.set()
            self.is_paused = True
            self.pause_btn.config(text="▶️ 继续")
            self.log_message("破解已暂停", "WARNING")
    
    def stop_crack(self):
        """停止破解"""
        self.stop_event.set()
        self.is_running = False
        self.is_paused = False
        
        # 更新按钮状态
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        
        # 更新标题
        self.window.title("⏹️ 密码破解已停止")
        
        self.log_message("破解已停止", "WARNING")
    
    def copy_password(self):
        """复制密码到剪贴板"""
        if self.found_password:
            self.window.clipboard_clear()
            self.window.clipboard_append(self.found_password)
            self.log_message("密码已复制到剪贴板", "SUCCESS")
            messagebox.showinfo("复制成功", f"密码已复制到剪贴板:\n{self.found_password}")
    
    def analyze_password(self):
        """分析密码强度"""
        if not self.found_password:
            return
        
        analysis = self.analyze_password_strength(self.found_password)
        
        # 创建分析结果窗口
        analysis_window = tk.Toplevel(self.window)
        analysis_window.title("🔍 密码强度分析")
        analysis_window.geometry("500x400")
        analysis_window.configure(bg=self.green_colors['bg_dark'])
        
        # 分析结果文本
        analysis_text = tk.Text(analysis_window,
                               bg=self.green_colors['bg_medium'],
                               fg=self.green_colors['text_green'],
                               font=('Consolas', 10),
                               relief='flat',
                               borderwidth=1)
        analysis_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 插入分析结果
        analysis_text.insert(tk.END, f"密码: {self.found_password}\n\n")
        analysis_text.insert(tk.END, f"长度: {len(self.found_password)} 字符\n")
        analysis_text.insert(tk.END, f"强度等级: {analysis['strength_level']}\n")
        analysis_text.insert(tk.END, f"强度分数: {analysis['strength_score']}/100\n\n")
        
        analysis_text.insert(tk.END, "详细分析:\n")
        for item in analysis['details']:
            analysis_text.insert(tk.END, f"• {item}\n")
        
        analysis_text.insert(tk.END, f"\n建议:\n{analysis['suggestion']}")
        
        analysis_text.config(state=tk.DISABLED)
    
    def analyze_password_strength(self, password: str) -> dict:
        """分析密码强度"""
        score = 0
        details = []
        
        # 长度检查
        if len(password) >= 8:
            score += 20
            details.append("密码长度≥8位 (+20分)")
        elif len(password) >= 6:
            score += 10
            details.append("密码长度≥6位 (+10分)")
        else:
            details.append("密码长度过短 (-10分)")
            score -= 10
        
        # 字符类型检查
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        if has_lower:
            score += 10
            details.append("包含小写字母 (+10分)")
        if has_upper:
            score += 10
            details.append("包含大写字母 (+10分)")
        if has_digit:
            score += 10
            details.append("包含数字 (+10分)")
        if has_special:
            score += 15
            details.append("包含特殊字符 (+15分)")
        
        # 字符多样性
        unique_chars = len(set(password))
        if unique_chars >= len(password) * 0.8:
            score += 15
            details.append("字符多样性高 (+15分)")
        elif unique_chars >= len(password) * 0.6:
            score += 10
            details.append("字符多样性中等 (+10分)")
        else:
            details.append("字符重复较多 (-5分)")
            score -= 5
        
        # 常见密码检查
        common_passwords = ['123456', 'password', '123456789', 'qwerty', 'admin']
        if password.lower() in common_passwords:
            score -= 30
            details.append("使用常见密码 (-30分)")
        
        # 连续字符检查
        consecutive_count = 0
        for i in range(len(password) - 1):
            if ord(password[i+1]) - ord(password[i]) == 1:
                consecutive_count += 1
        
        if consecutive_count >= 3:
            score -= 10
            details.append("包含连续字符 (-10分)")
        
        # 确定强度等级
        if score >= 80:
            strength_level = "非常强"
            suggestion = "密码强度很高，建议继续使用。"
        elif score >= 60:
            strength_level = "强"
            suggestion = "密码强度良好，可以考虑增加特殊字符。"
        elif score >= 40:
            strength_level = "中等"
            suggestion = "密码强度一般，建议增加长度和字符类型。"
        elif score >= 20:
            strength_level = "弱"
            suggestion = "密码强度较弱，建议重新设置更复杂的密码。"
        else:
            strength_level = "非常弱"
            suggestion = "密码强度很低，强烈建议更换密码。"
        
        return {
            'strength_score': max(0, min(100, score)),
            'strength_level': strength_level,
            'details': details,
            'suggestion': suggestion
        }
    
    def close_window(self):
        """关闭窗口"""
        if self.is_running:
            if messagebox.askyesno("确认", "破解正在进行中，确定要关闭窗口吗？"):
                self.stop_crack()
        
        if self.parent:
            self.window.destroy()
        else:
            self.window.quit()
    
    def on_window_close(self):
        """窗口关闭事件处理"""
        self.close_window()
    
    def get_result(self) -> Optional[str]:
        """获取破解结果"""
        return self.found_password
    
    def is_completed(self) -> bool:
        """检查是否完成破解"""
        return self.found_password is not None or (not self.is_running and not self.crack_thread.is_alive())


# 集成到主应用程序的接口类
class CrackWindowManager:
    """破解窗口管理器"""
    
    def __init__(self, parent_app):
        self.parent_app = parent_app
        self.active_windows = []
    
    def create_crack_window(self, file_path: str, crack_mode: str = "brute", auto_start: bool = True, **kwargs):
        """创建新的破解窗口"""
        crack_window = CrackWindow(
            parent=self.parent_app.master,
            file_path=file_path,
            crack_mode=crack_mode,
            auto_start=auto_start,  # 传递自动启动参数
            **kwargs
        )
        
        # 设置结果回调
        def on_result(password):
            if password:
                self.parent_app.post_crack_update(password)
        
        crack_window.set_result_callback(on_result)
        self.active_windows.append(crack_window)
        
        return crack_window
    
    def close_all_windows(self):
        """关闭所有破解窗口"""
        for window in self.active_windows:
            try:
                window.close_window()
            except:
                pass
        self.active_windows.clear()


# 使用示例
if __name__ == "__main__":
    # 创建测试窗口
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口
    
    # 创建破解窗口
    crack_window = CrackWindow(
        parent=root,
        file_path="test.zip",
        crack_mode="brute"
    )
    
    # 运行
    root.mainloop()