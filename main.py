import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
import time
import ttkbootstrap as ttkb
from ttkbootstrap import Style
import requests
from PIL import Image, ImageTk

# 从cracker模块导入所有破解器
from cracker import zip_cracker, rar_cracker, sevenz_cracker, office_cracker, pdf_cracker, hashcat_engine, john_engine, ai_predictor
# 从utils模块导入辅助工具
from utils import password_analyzer, progress_manager, file_utils
from cracker.advanced_engine import AdvancedCracker
# 导入破解窗口
from crack_window import CrackWindow, CrackWindowManager

CURRENT_VERSION = "1.0.3"
UPDATE_URL = "https://raw.githubusercontent.com/xuanxuan205/-/main/version.json"  # 版本更新信息文件

def check_update():
    try:
        resp = requests.get(UPDATE_URL, timeout=5, verify=False)
        if resp.status_code == 200:
            data = resp.json()
            latest = data.get("version", "")
            changelog = data.get("changelog", "")
            download_url = data.get("download_url", "")
            if latest > CURRENT_VERSION:
                if tk.messagebox.askyesno("发现新版本", f"检测到新版本 {latest}！\n\n更新内容：\n{changelog}\n\n是否前往下载？"):
                    import webbrowser
                    webbrowser.open(download_url)
            else:
                tk.messagebox.showinfo("检查更新", "当前已是最新版本。")
        else:
            tk.messagebox.showerror("检查更新", "无法获取更新信息。")
    except Exception as e:
        tk.messagebox.showerror("检查更新", f"检查更新失败：{e}")

class SuperCrackerApp:
    def __init__(self, master):
        self.master = master
        self.language = 'zh'  # 默认中文
        self.texts = {
            'title': {'zh': '超级密码破解工具 v1.0.4', 'en': 'Super Password Cracker v1.0.4'},
            'author': {'zh': '作者：DeZai    QQ：2080341475', 'en': 'Author: DeZai    QQ: 2080341475'},
            'copyright': {'zh': '© 2025 超级密码破解工具. 保留所有权利。\n本工具仅供学习和研究使用，请勿用于非法用途。',
                          'en': '© 2025 Super Password Cracker. All rights reserved.\nFor study and research only. Do not use for illegal purposes.'},
            'select_file': {'zh': '选择加密文件', 'en': 'Select File'},
            'analyze_file': {'zh': '分析文件', 'en': 'Analyze'},
            'add_to_queue': {'zh': '添加到队列', 'en': 'Add to Queue'},
            'queue': {'zh': '文件破解队列', 'en': 'File Queue'},
            'mode': {'zh': '破解模式', 'en': 'Crack Mode'},
            'brute': {'zh': '暴力破解', 'en': 'Brute-force'},
            'dict': {'zh': '字典破解', 'en': 'Dictionary'},
            'mask': {'zh': '掩码破解', 'en': 'Mask'},
            'ai': {'zh': 'AI智能破解', 'en': 'AI Smart Crack'},
            'hashcat': {'zh': 'Hashcat引擎', 'en': 'Hashcat Engine'},
            'john': {'zh': 'John引擎', 'en': 'John Engine'},
            'hybrid': {'zh': '混合破解', 'en': 'Hybrid Crack'},
            'rainbow': {'zh': '彩虹表破解', 'en': 'Rainbow Table'},
            'gpu': {'zh': 'GPU加速破解', 'en': 'GPU Accelerated'},
            'distributed': {'zh': '分布式破解', 'en': 'Distributed Crack'},
            'min_len': {'zh': '最小密码长度:', 'en': 'Min Length:'},
            'max_len': {'zh': '最大密码长度:', 'en': 'Max Length:'},
            'charset': {'zh': '字符集:', 'en': 'Charset:'},
            'dict_file': {'zh': '字典文件:', 'en': 'Dictionary File:'},
            'import_dict': {'zh': '导入字典', 'en': 'Import'},
            'mask_label': {'zh': '掩码 (如: ?l?d?d?d):', 'en': 'Mask (e.g. ?l?d?d?d):'},
            'mask_hint': {'zh': '?l=小写 ?u=大写 ?d=数字 ?s=特殊', 'en': '?l=lower ?u=upper ?d=digits ?s=special'},
            'progress': {'zh': '进度与状态', 'en': 'Progress & Status'},
            'start_crack': {'zh': '开始破解', 'en': 'Start'},
            'pause': {'zh': '暂停', 'en': 'Pause'},
            'stop': {'zh': '停止', 'en': 'Stop'},
            'save': {'zh': '保存进度', 'en': 'Save'},
            'load': {'zh': '加载进度', 'en': 'Load'},
            'export': {'zh': '导出结果', 'en': 'Export'},
            'result': {'zh': '破解结果与分析', 'en': 'Result & Analysis'},
            'copy_pwd': {'zh': '复制密码', 'en': 'Copy'},
            'analyze_pwd': {'zh': '分析密码', 'en': 'Analyze'},
            'log': {'zh': '日志', 'en': 'Log'},
            'log_search': {'zh': '日志搜索:', 'en': 'Log Search:'},
            'search': {'zh': '搜索', 'en': 'Search'},
            'reset': {'zh': '重置', 'en': 'Reset'},
            'waiting': {'zh': '等待开始...', 'en': 'Waiting...'},
        }
        self.style = Style(theme="flatly")
        self.master = self.style.master
        self.master.title("超级密码破解工具 v1.0.4") # 版本号升级
        self.master.geometry("1000x1000") # 扩大窗口

        # 应用状态变量
        self.file_path = None
        self.file_type = None
        self.crack_mode = tk.StringVar(value="brute") # 暴力破解/字典/掩码/AI/Hashcat/John/混合/彩虹表/GPU/分布式
        self.progress = 0
        self.found_password = None
        self.cracker_thread = None
        self.is_running = False
        self.is_paused = False
        self.stop_event = threading.Event() # 用于停止破解的事件
        self.pause_event = threading.Event() # 用于暂停/恢复破解的事件
        self.progress_data = None

        # 暴力破解参数
        self.min_length_var = tk.StringVar(value="1")
        self.max_length_var = tk.StringVar(value="8")
        self.charset_var = tk.StringVar(value="all")

        # 初始化高级破解引擎
        self.advanced_cracker = AdvancedCracker()
        
        # 初始化破解窗口管理器
        self.crack_window_manager = CrackWindowManager(self)

        self.create_widgets()

    def create_widgets(self):
        self.mode_var = tk.StringVar(value="brute")
        ttk = ttkb
        # 语言切换按钮
        lang_btn = ttk.Button(self.master, text='English', command=self.toggle_language)
        lang_btn.pack(anchor='ne', padx=10, pady=5)
        self.lang_btn = lang_btn
        # 居中Frame
        center_frame = ttk.Frame(self.master)
        center_frame.pack(expand=True)
        # 顶部标题
        title_label = ttk.Label(center_frame, text=self.texts['title'][self.language], font=('Arial', 20, 'bold'), anchor='center', justify='center')
        title_label.pack(pady=5, fill=None, anchor='center')
        self.title_label = title_label
        author_label = ttk.Label(center_frame, text=self.texts['author'][self.language], font=('Arial', 11), foreground='#444', anchor='center', justify='center')
        author_label.pack(pady=2, fill=None, anchor='center')
        self.author_label = author_label
        copyright_label = ttk.Label(center_frame, text=self.texts['copyright'][self.language], font=('Arial', 9), foreground='#666', anchor='center', justify='center')
        copyright_label.pack(pady=2, fill=None, anchor='center')
        self.copyright_label = copyright_label
        separator = ttk.Separator(center_frame, orient='horizontal')
        separator.pack(fill='x', padx=8, pady=6)
        # 顶部文件选择
        top_frame = ttk.Frame(center_frame)
        top_frame.pack(pady=6, anchor='center')
        ttk.Button(top_frame, text=self.texts['select_file'][self.language], command=self.select_file, width=14).pack(side=tk.LEFT, padx=8)
        self.file_label = ttk.Label(top_frame, text="未选择文件", width=30, anchor='center', justify='center')
        self.file_label.pack(side=tk.LEFT, padx=8)
        ttk.Button(top_frame, text=self.texts['analyze_file'][self.language], command=self.analyze_file, width=10).pack(side=tk.LEFT, padx=8)
        # 检查更新按钮
        tk.Button(top_frame, text="检查更新", font=("微软雅黑", 10), bg="#007bff", fg="white", command=check_update).pack(side="right", padx=20)
        # 支持作者按钮
        tk.Button(top_frame, text="支持作者", font=("微软雅黑", 10), bg="#28a745", fg="white", command=self.show_qr_code).pack(side="right", padx=10)
        
        # 破解模式选择 - 扩展更多模式
        self.mode_frame = ttk.LabelFrame(center_frame, text="破解模式")
        self.mode_frame.pack(padx=8, pady=4, anchor='center')
        mode_row = ttk.Frame(self.mode_frame)
        mode_row.pack(fill=tk.X, padx=5, pady=2)
        ttk.Radiobutton(mode_row, text="暴力破解", value="brute", variable=self.mode_var).pack(side=tk.LEFT, padx=8)
        ttk.Radiobutton(mode_row, text="字典破解", value="dict", variable=self.mode_var).pack(side=tk.LEFT, padx=8)
        ttk.Radiobutton(mode_row, text="掩码破解", value="mask", variable=self.mode_var).pack(side=tk.LEFT, padx=8)
        
        # 模式说明
        mode_info_frame = ttk.Frame(self.mode_frame)
        mode_info_frame.pack(fill=tk.X, padx=5, pady=2)
        ttk.Label(mode_info_frame, text="说明: 导入字典文件后将使用字典模式，不导入则使用所选模式", 
                 font=("Arial", 9), foreground="#444").pack(pady=2)
        
        # 暴力破解参数设置区域
        self.param_frame = ttk.Frame(center_frame)
        self.param_frame.pack(padx=8, pady=4, anchor='center')
        
        # 直接显示暴力破解参数
        brute_sub_frame = ttk.LabelFrame(self.param_frame, text="暴力破解参数")
        brute_sub_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(brute_sub_frame, text=self.texts['min_len'][self.language]).grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(brute_sub_frame, textvariable=self.min_length_var, width=5).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(brute_sub_frame, text=self.texts['max_len'][self.language]).grid(row=0, column=2, padx=5, pady=5)
        ttk.Entry(brute_sub_frame, textvariable=self.max_length_var, width=5).grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(brute_sub_frame, text=self.texts['charset'][self.language]).grid(row=0, column=4, padx=5, pady=5)
        ttk.Combobox(brute_sub_frame, textvariable=self.charset_var,
                     values=["数字", "小写字母", "大写字母", "字母", "符号", "常用汉字", "自定义", "全字符集"], width=14).grid(row=0, column=5, padx=5, pady=5)
        
        # 字典文件设置
        dict_sub_frame = ttk.LabelFrame(self.param_frame, text="字典文件设置")
        dict_sub_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(dict_sub_frame, text="字典文件:").grid(row=0, column=0, padx=5, pady=5)
        self.dict_file_var = tk.StringVar(value="")
        dict_entry = ttk.Entry(dict_sub_frame, textvariable=self.dict_file_var, width=30)
        dict_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(dict_sub_frame, text="选择字典", command=self.select_dict_file, width=10).grid(row=0, column=2, padx=5, pady=5)
        ttk.Label(dict_sub_frame, text="(选择字典文件进行字典破解，不选择则使用内置字典)").grid(row=0, column=3, padx=5, pady=5)
        ttk.Label(dict_sub_frame, text="提示: 选择字典后将自动使用字典模式，不使用其他模式", foreground="#B22222").grid(row=1, column=0, columnspan=4, padx=5, pady=5)
        
        # 掩码参数设置
        mask_sub_frame = ttk.LabelFrame(self.param_frame, text="掩码参数")
        mask_sub_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Label(mask_sub_frame, text="掩码模式:").grid(row=0, column=0, padx=5, pady=5)
        self.mask_var = tk.StringVar(value="?l?l?l?d?d?d")
        ttk.Entry(mask_sub_frame, textvariable=self.mask_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        ttk.Label(mask_sub_frame, text="(?l=小写 ?u=大写 ?d=数字 ?s=符号 ?a=所有 ?c=中文)").grid(row=0, column=2, padx=5, pady=5)
        
        # 进度条与状态
        progress_frame = ttk.LabelFrame(center_frame, text=self.texts['progress'][self.language])
        progress_frame.pack(padx=8, pady=4, anchor='center')
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate', length=350)
        self.progress_bar.pack(side=tk.LEFT, padx=8, pady=8, anchor='center')
        self.progress_label = ttk.Label(progress_frame, text=self.texts['waiting'][self.language], anchor='center', justify='center')
        self.progress_label.pack(side=tk.LEFT, padx=8, anchor='center')
        
        # 控制按钮
        control_frame = ttk.Frame(center_frame)
        control_frame.pack(padx=8, pady=4, anchor='center')
        self.start_btn = ttk.Button(control_frame, text=self.texts['start_crack'][self.language], command=self.start_crack, width=12)
        self.start_btn.pack(side=tk.LEFT, padx=8)
        self.pause_btn = ttk.Button(control_frame, text=self.texts['pause'][self.language], command=self.toggle_pause, state=tk.DISABLED, width=8)
        self.pause_btn.pack(side=tk.LEFT, padx=8)
        self.stop_btn = ttk.Button(control_frame, text=self.texts['stop'][self.language], command=self.stop_crack, state=tk.DISABLED, width=8)
        self.stop_btn.pack(side=tk.LEFT, padx=8)
        self.save_btn = ttk.Button(control_frame, text=self.texts['save'][self.language], command=self.save_progress, state=tk.DISABLED, width=10)
        self.save_btn.pack(side=tk.LEFT, padx=8)
        self.load_btn = ttk.Button(control_frame, text=self.texts['load'][self.language], command=self.load_progress, width=10)
        self.load_btn.pack(side=tk.LEFT, padx=8)
        self.export_btn = ttk.Button(control_frame, text=self.texts['export'][self.language], command=self.export_result, state=tk.DISABLED, width=10)
        self.export_btn.pack(side=tk.LEFT, padx=8)
        
        # 密码显示与分析
        result_frame = ttk.LabelFrame(center_frame, text=self.texts['result'][self.language])
        result_frame.pack(padx=8, pady=4, anchor='center')
        self.result_text = tk.Text(result_frame, height=4, width=50, font=("Consolas", 12), wrap=tk.WORD)
        self.result_text.pack(padx=8, pady=8, anchor='center')
        self.copy_btn = ttk.Button(result_frame, text=self.texts['copy_pwd'][self.language], command=self.copy_password, state=tk.DISABLED, width=12)
        self.copy_btn.pack(side=tk.LEFT, padx=8)
        self.analyze_btn = ttk.Button(result_frame, text=self.texts['analyze_pwd'][self.language], command=self.analyze_password, state=tk.DISABLED, width=12)
        self.analyze_btn.pack(side=tk.LEFT, padx=8)
        
        # 日志区域
        log_frame = ttk.LabelFrame(center_frame, text=self.texts['log'][self.language])
        log_frame.pack(padx=8, pady=4, anchor='center')
        self.log_text = tk.Text(log_frame, height=8, width=60, font=("Consolas", 11), wrap=tk.WORD)
        self.log_text.pack(padx=8, pady=8, anchor='center')
        xscroll = ttk.Scrollbar(log_frame, orient='horizontal', command=self.log_text.xview)
        xscroll.pack(side=tk.BOTTOM, fill=tk.X)
        self.log_text.config(xscrollcommand=xscroll.set)
        
        # 日志搜索区
        search_frame = ttk.Frame(center_frame)
        search_frame.pack(padx=8, pady=2, anchor='center')
        ttk.Label(search_frame, text=self.texts['log_search'][self.language], anchor='center').pack(side=tk.LEFT)
        self.log_search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.log_search_var, width=20, justify='center')
        search_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text=self.texts['search'][self.language], command=self.filter_log, width=8).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text=self.texts['reset'][self.language], command=self.reset_log, width=8).pack(side=tk.LEFT, padx=5)

    def select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[
                ("所有支持的文件", "*.zip;*.rar;*.7z;*.doc;*.docx;*.xls;*.xlsx;*.ppt;*.pptx;*.pdf"),
                ("压缩文件", "*.zip;*.rar;*.7z"),
                ("Office文档", "*.doc;*.docx;*.xls;*.xlsx;*.ppt;*.pptx"),
                ("PDF文件", "*.pdf"),
                ("所有文件", "*.*")
            ]
        )
        if file_path:
            self.file_path = file_path
            self.file_label.config(text=file_path)
            self.file_type = file_utils.detect_file_type(file_path)
            self.log(f"已选择文件: {file_path} 类型: {self.file_type}")

    def select_dict_file(self):
        """选择字典文件"""
        dict_file_path = filedialog.askopenfilename(
            title="选择字典文件",
            filetypes=[
                ("文本文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )
        if dict_file_path:
            self.dict_file_var.set(dict_file_path)
            self.log(f"已选择字典文件: {dict_file_path}")
            # 自动切换到字典模式
            self.mode_var.set("dict")

    def analyze_file(self):
        if not self.file_path:
            messagebox.showinfo("提示", "请先选择文件！")
            return
        self.log("正在分析文件元数据...")
        metadata = file_utils.analyze_file_metadata(self.file_path) # 移除log_callback参数
        file_type = file_utils.detect_file_type(self.file_path)

        if not file_type or file_type == "unknown":
            self.log("无法识别的文件类型！")
            return

        self.log(f"文件分析结果: {metadata}")

    def start_crack(self):
        if not self.file_path:
            messagebox.showinfo("提示", "请先选择文件！")
            return
        
        if self.is_running:
            self.log("破解正在进行中，请等待完成或停止当前任务。")
            return
        
        self.is_running = True
        self.stop_event.clear() # 清除停止事件
        self.pause_event.clear() # 清除暂停事件
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
        self.save_btn.config(state=tk.DISABLED) # 保存进度目前只针对单个文件
        self.export_btn.config(state=tk.DISABLED)
        self.copy_btn.config(state=tk.DISABLED)
        self.analyze_btn.config(state=tk.DISABLED)
        self.result_text.delete("1.0", tk.END)
        self.progress_bar['value'] = 0
        self.progress_label.config(text="正在初始化...")
        self.log("开始破解...")
        
        # 检测文件类型
        self.file_type = file_utils.detect_file_type(self.file_path)
        self.log(f"开始破解文件: {self.file_path} 类型: {self.file_type}")

        self.cracker_thread = threading.Thread(target=self.crack_dispatcher, daemon=True)
        self.cracker_thread.start()

    def crack_dispatcher(self):
        """破解分发器 - 使用破解窗口进行破解"""
        try:
            mode = self.mode_var.get()
            file_ext = os.path.splitext(self.file_path)[1].lower()
            
            # 确定字典文件路径
            dict_file = self.dict_file_var.get().strip()
            
            # 如果用户选择了字典文件，强制使用字典模式
            if dict_file:
                mode = "dict"
                self.log("检测到字典文件，自动切换到字典破解模式")
            elif mode == "dict":  # 如果选择了字典模式但没有指定字典文件，使用默认字典
                dict_file = "./dictionaries/密码字典.txt"  # 默认字典
            
            # 显示破解模式信息
            mode_info = {
                'brute': '暴力破解',
                'dict': '字典破解',
                'mask': '掩码破解'
            }.get(mode, '未知模式')
            
            self.log(f"启动{mode_info}窗口...")
            
            # 准备破解参数
            crack_params = {
                'min_length': int(self.min_length_var.get()),
                'max_length': int(self.max_length_var.get()),
                'charset': self.charset_var.get(),
                'mask': self.mask_var.get(),
                'dict_file': dict_file,
                'file_ext': file_ext
            }
            
            # 创建破解窗口（自动启动）
            self.crack_window = self.crack_window_manager.create_crack_window(
                file_path=self.file_path,
                crack_mode=mode,
                auto_start=True,  # 自动启动破解
                **crack_params
            )
            
            # 设置结果回调
            def on_crack_result(password):
                if password:
                    self.post_crack_update(password)
                    self.log(f"破解窗口返回结果: {password}")
                else:
                    self.post_crack_update(None)
                    self.log("破解窗口返回: 未找到密码")
            
            self.crack_window.result_callback = on_crack_result
            
            self.log("已启动破解窗口，请在新窗口中查看破解进度")
                
        except Exception as e:
            self.log(f"破解调度错误: {e}")
            messagebox.showerror("错误", f"破解过程出错: {e}")
            self.reset_ui_after_crack()

    def post_crack_update(self, password):
        if password:
            self.result_text.delete("1.0", tk.END)
            self.result_text.insert(tk.END, f"已成功破解密码：{password}", "success")
            self.result_text.tag_config("success", foreground="#228B22", font=("Consolas", 14, "bold"))
            self.copy_btn.config(state=tk.NORMAL)
            self.analyze_btn.config(state=tk.NORMAL)
            self.progress_label.config(text=f"已破解，密码: {password}", foreground="#228B22", font=("Arial", 11, "bold"))
            self.progress_bar.configure(style="Success.Horizontal.TProgressbar")
            self.found_password = password  # 保证复制和分析功能可用
            # 自动保存到 crack_results/auto_saved.txt（全竖线+双横线风格）
            try:
                os.makedirs("crack_results", exist_ok=True)
                save_path = "crack_results/auto_saved.txt"
                file_col_width = 13
                pwd_col_width = 10
                # 读取已有数据，去除所有表头和分隔线，只保留数据行
                records = []
                if os.path.exists(save_path):
                    with open(save_path, "r", encoding="utf-8") as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("║") and line.endswith("║") and "╬" not in line:
                                parts = line.strip("║").split("║")
                                if len(parts) == 2:
                                    file, pwd = parts[0].strip(), parts[1].strip()
                                    records.append((file, pwd))
                # 添加新纪录（去重）
                new_record = (self.file_path, password)
                if new_record not in records:
                    records.append(new_record)
                # 写回全竖线+双横线风格表格
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(f"╔{'═'*file_col_width}╦{'═'*pwd_col_width}╗\n")
                    f.write(f"║ {'文件名':<{file_col_width-1}}║ {'密码':<{pwd_col_width-1}}║\n")
                    f.write(f"╠{'═'*file_col_width}╬{'═'*pwd_col_width}╣\n")
                    for file, pwd in records:
                        f.write(f"║ {file:<{file_col_width-1}}║ {pwd:<{pwd_col_width-1}}║\n")
                    f.write(f"╚{'═'*file_col_width}╩{'═'*pwd_col_width}╝\n")
                self.log("结果已自动保存到 crack_results/auto_saved.txt")
            except Exception as e:
                print(f"自动保存破解结果失败: {e}")
        else:
            self.result_text.delete("1.0", tk.END)
            self.copy_btn.config(state=tk.DISABLED)
            self.analyze_btn.config(state=tk.DISABLED)
            self.progress_label.config(text="破解失败或未找到密码。", foreground="#b22222", font=("Arial", 10, "bold"))
            self.progress_bar.configure(style="TProgressbar")
            self.found_password = None
        self.reset_ui_after_crack()

    def reset_ui_after_crack(self):
        self.is_running = False
        self.is_paused = False
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)
        self.save_btn.config(state=tk.NORMAL if self.progress_data else tk.DISABLED) # 根据是否有进度数据启用保存
        # self.export_btn.config(state=tk.NORMAL if self.found_password else tk.DISABLED)
        # self.copy_btn.config(state=tk.NORMAL if self.found_password else tk.DISABLED)
        # self.analyze_btn.config(state=tk.NORMAL if self.found_password else tk.DISABLED)
        self.progress_label.config(text="已完成或已停止。")
        self.progress_bar['value'] = 0
        self.log("UI已重置。")

    def update_progress(self, current_attempts, total_passwords, status=None):
        # 优化进度条：最大值为total_passwords，当前值为current_attempts，确保平滑推进
        if total_passwords > 0 and total_passwords < 1e9:
            self.progress_bar['maximum'] = total_passwords
            self.progress_bar['value'] = current_attempts
            percent = int(current_attempts * 100 / total_passwords)
        else:
            self.progress_bar['maximum'] = 100
            self.progress_bar['value'] = 0
            percent = 0
        if status and "已破解" in status:
            self.progress_bar.configure(style="Success.Horizontal.TProgressbar")
            self.progress_label.config(text=status, foreground="#228B22", font=("Arial", 11, "bold"))
        else:
            self.progress_bar.configure(style="TProgressbar")
            self.progress_label.config(text=status or f"进度: {percent}%", foreground="#222", font=("Arial", 10))
        self.master.update_idletasks()

    def toggle_pause(self):
        if self.is_running:
            if self.is_paused:
                self.pause_event.clear() # 清除暂停事件，恢复破解
                self.pause_btn.config(text="暂停")
                self.log("已恢复破解。")
            else:
                self.pause_event.set() # 设置暂停事件，暂停破解
                self.pause_btn.config(text="继续")
                self.log("已暂停破解。")
            self.is_paused = not self.is_paused

    def stop_crack(self):
        if self.is_running:
            self.stop_event.set() # 设置停止事件
            self.log("正在发送停止信号...")
            # crack_dispatcher 会检测到 stop_event 并终止
            # self.reset_ui_after_crack() # 此时不立即重置UI，等待线程自然结束

    def save_progress(self):
        # progress_manager.save(self.file_path, self.progress_data)
        messagebox.showinfo("提示", "保存进度功能待完善！")

    def load_progress(self):
        # self.progress_data = progress_manager.load(self.file_path)
        messagebox.showinfo("提示", "加载进度功能待完善！")

    def export_result(self):
        if self.found_password and self.file_path:
            output_dir = "crack_results"
            os.makedirs(output_dir, exist_ok=True)
            file_name = os.path.basename(self.file_path)
            result_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_cracked.txt")
            with open(result_file, 'a', encoding='utf-8') as f:
                f.write(f"文件: {self.file_path}\n")
                f.write(f"破解密码: {self.found_password}\n")
                f.write(f"破解时间: {time.strftime("%Y-%m-%d %H:%M:%S")}\n")
                f.write("------------------------------------\n\n")
            messagebox.showinfo("导出成功", f"破解结果已导出到: {result_file}")
        else:
            messagebox.showinfo("提示", "没有可导出的破解结果。")

    def copy_password(self):
        if self.found_password:
            self.master.clipboard_clear()
            self.master.clipboard_append(self.found_password)
            messagebox.showinfo("复制成功", "密码已复制到剪贴板！")
        else:
            messagebox.showinfo("提示", "没有可复制的密码。")

    def analyze_password(self):
        if self.found_password:
            analysis = password_analyzer.analyze_password_strength(self.found_password)
            analysis_report = f"密码: {self.found_password}\n强度: {analysis['strength']}\n"
            for item in analysis['feedback']:
                analysis_report += f"- {item}\n"
            messagebox.showinfo("密码强度分析", analysis_report)
        else:
            messagebox.showinfo("提示", "没有密码可供分析。")

    def log(self, msg):
        timestamp = time.strftime("[%H:%M:%S]")
        log_line = f"{timestamp} {msg}"
        if not hasattr(self, 'all_logs'):
            self.all_logs = []
        self.all_logs.append(log_line)
        # 如果当前处于过滤状态，自动重置为全部显示
        if getattr(self, 'log_filtered', False):
            self.reset_log()
            self.log_filtered = False
        self.log_text.insert(tk.END, f"{log_line}\n")
        self.log_text.see(tk.END)

    def filter_log(self):
        keyword = self.log_search_var.get().strip()
        if not keyword:
            return
        if not hasattr(self, 'all_logs'):
            return
        filtered = [line for line in self.all_logs if keyword in line]
        self.log_text.delete("1.0", tk.END)
        self.log_text.insert(tk.END, "\n".join(filtered))
        self.log_filtered = True

    def reset_log(self):
        if hasattr(self, 'all_logs'):
            self.log_text.delete("1.0", tk.END)
            self.log_text.insert(tk.END, "\n".join(self.all_logs) + "\n")
            self.log_filtered = False

    def toggle_language(self):
        self.language = 'en' if self.language == 'zh' else 'zh'
        self.lang_btn.config(text='中文' if self.language == 'en' else 'English')
        # 刷新所有界面文本
        self.title_label.config(text=self.texts['title'][self.language])
        self.author_label.config(text=self.texts['author'][self.language])
        self.copyright_label.config(text=self.texts['copyright'][self.language])
        self.mode_frame.config(text=self.texts['mode'][self.language])
        for i, child in enumerate(self.mode_frame.winfo_children()):
            if isinstance(child, ttk.Radiobutton):
                child.config(text=[self.texts['brute'][self.language]][i])
        self.start_btn.config(text=self.texts['start_crack'][self.language])
        self.pause_btn.config(text=self.texts['pause'][self.language])
        self.stop_btn.config(text=self.texts['stop'][self.language])
        self.save_btn.config(text=self.texts['save'][self.language])
        self.load_btn.config(text=self.texts['load'][self.language])
        self.export_btn.config(text=self.texts['export'][self.language])
        self.copy_btn.config(text=self.texts['copy_pwd'][self.language])
        self.analyze_btn.config(text=self.texts['analyze_pwd'][self.language])
        self.progress_label.config(text=self.texts['waiting'][self.language])
        # 进度与状态、日志、结果区等LabelFrame
        for frame, key in zip([self.mode_frame, self.result_text.master, self.log_text.master], ['mode', 'result', 'log']):
            frame.config(text=self.texts[key][self.language])
        # 顶部按钮、队列、参数区等
        for widget in self.master.winfo_children():
            if isinstance(widget, ttk.LabelFrame) and widget.cget('text') in [self.texts['queue']['zh'], self.texts['queue']['en']]:
                widget.config(text=self.texts['queue'][self.language])
        # 顶部按钮
        for widget in self.master.winfo_children():
            if isinstance(widget, ttk.Frame):
                for btn in widget.winfo_children():
                    if isinstance(btn, ttk.Button) and btn.cget('text') in [self.texts['select_file']['zh'], self.texts['select_file']['en']]:
                        btn.config(text=self.texts['select_file'][self.language])
                    if isinstance(btn, ttk.Button) and btn.cget('text') in [self.texts['analyze_file']['zh'], self.texts['analyze_file']['en']]:
                        btn.config(text=self.texts['analyze_file'][self.language])
                    if isinstance(btn, ttk.Button) and btn.cget('text') in [self.texts['add_to_queue']['zh'], self.texts['add_to_queue']['en']]:
                        btn.config(text=self.texts['add_to_queue'][self.language])
        # 日志搜索区
        for widget in self.master.winfo_children():
            if isinstance(widget, ttk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, ttk.Label) and child.cget('text') in [self.texts['log_search']['zh'], self.texts['log_search']['en']]:
                        child.config(text=self.texts['log_search'][self.language])
                    if isinstance(child, ttk.Button) and child.cget('text') in [self.texts['search']['zh'], self.texts['search']['en']]:
                        child.config(text=self.texts['search'][self.language])
                    if isinstance(child, ttk.Button) and child.cget('text') in [self.texts['reset']['zh'], self.texts['reset']['en']]:
                        child.config(text=self.texts['reset'][self.language])

    def show_qr_code(self):
        """显示二维码窗口"""
        # 创建新窗口
        qr_window = tk.Toplevel(self.master)
        qr_window.title("支持作者 - 扫码打赏")
        qr_window.geometry("800x600")
        qr_window.resizable(False, False)
        
        # 设置窗口居中
        qr_window.transient(self.master)
        qr_window.grab_set()
        
        # 创建主框架
        main_frame = ttk.Frame(qr_window)
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)
        
        # 标题
        title_label = ttk.Label(main_frame, text="感谢您的支持！", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 创建二维码显示区域
        qr_frame = ttk.Frame(main_frame)
        qr_frame.pack(expand=True)
        
        # 支付宝二维码
        alipay_frame = ttk.LabelFrame(qr_frame, text="支付宝")
        alipay_frame.pack(side=tk.LEFT, padx=20)
        
        try:
            # 加载支付宝二维码图片
            alipay_img = Image.open("images/alipay_qr_3.png")
            # 调整图片大小 - 增大到300x300像素便于扫码
            alipay_img = alipay_img.resize((300, 300), Image.Resampling.LANCZOS)
            alipay_photo = ImageTk.PhotoImage(alipay_img)
            
            alipay_label = ttk.Label(alipay_frame, image=alipay_photo)
            alipay_label.image = alipay_photo  # 保持引用
            alipay_label.pack(padx=10, pady=10)
        except Exception as e:
            ttk.Label(alipay_frame, text="图片加载失败", foreground='red').pack(padx=10, pady=10)
        
        # 微信二维码
        wechat_frame = ttk.LabelFrame(qr_frame, text="微信")
        wechat_frame.pack(side=tk.LEFT, padx=20)
        
        try:
            # 加载微信二维码图片
            wechat_img = Image.open("images/wechat_qr_3.png")
            # 调整图片大小 - 增大到300x300像素便于扫码
            wechat_img = wechat_img.resize((300, 300), Image.Resampling.LANCZOS)
            wechat_photo = ImageTk.PhotoImage(wechat_img)
            
            wechat_label = ttk.Label(wechat_frame, image=wechat_photo)
            wechat_label.image = wechat_photo  # 保持引用
            wechat_label.pack(padx=10, pady=10)
        except Exception as e:
            ttk.Label(wechat_frame, text="图片加载失败", foreground='red').pack(padx=10, pady=10)
        
        # 说明文字
        info_label = ttk.Label(main_frame, text="扫描二维码即可打赏支持作者开发", 
                              font=('Arial', 12), foreground='#666')
        info_label.pack(pady=(20, 0))
        
        # 关闭按钮
        close_btn = ttk.Button(main_frame, text="关闭", command=qr_window.destroy, width=15)
        close_btn.pack(pady=(20, 0))
        
        # 设置窗口关闭事件
        qr_window.protocol("WM_DELETE_WINDOW", qr_window.destroy)

    def run(self):
        self.master.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SuperCrackerApp(root)
    app.run() 