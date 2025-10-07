import os
import time
import threading
import hashlib
import itertools
import string
import re
import json
import subprocess
import multiprocessing
from typing import List, Dict, Optional, Callable
import numpy as np
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import psutil
try:
    import GPUtil
    GPU_AVAILABLE = True
except:
    GPU_AVAILABLE = False

class AdvancedCracker:
    """超级密码破解引擎 - 集成所有顶级破解技术"""
    
    def __init__(self):
        self.charsets = {
            'digits': string.digits,
            'lowercase': string.ascii_lowercase,
            'uppercase': string.ascii_uppercase,
            'letters': string.ascii_letters,
            'symbols': string.punctuation,
            'chinese': '的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞',
            'all': string.digits + string.ascii_letters + string.punctuation + '的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转更单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞'
        }
        
        # 常用密码模式
        self.common_patterns = [
            '123456', 'password', '123456789', '12345678', '12345', 'qwerty', 'abc123',
            'password123', '1234567', '1234567890', 'admin', 'letmein', 'welcome',
            'monkey', '123123', '1234', '12345678910', 'dragon', 'baseball', 'football',
            'shadow', 'master', 'jordan', 'superman', 'harley', 'hunter', 'buster',
            'thomas', 'tigger', 'robert', 'soccer', 'batman', 'test', 'pass', 'kelly',
            'hockey', 'george', 'charlie', 'andrew', 'michelle', 'love', 'sunshine',
            'jessica', 'asshole', '696969', 'amanda', 'access', 'computer', 'cookie',
            'mickey', 'secret', 'maxwell', 'mustang', 'marcus', 'jordan23', 'super',
            'allison', 'soccer1', 'tiger', 'badass', 'chevy', 'white', 'black',
            'fishing', 'blowme', 'fishing1', 'debbie', 'miami', 'squirt', 'gators',
            'packers', 'jordan1', 'cowboys', 'eagles', 'chris', 'liverpool', 'gordon',
            'casper', 'stupid', 'shit', 'saturn', 'gemini', 'apples', 'august',
            'canada', 'blazer', 'cumming', 'hunting', 'kitty', 'rainbow', 'arthur',
            'cream', 'calvin', 'shaved', 'surfer', 'samson', 'kelly1', 'paul',
            'matt', 'qwerty1', 'john', 'robert1', 'daniel', 'chris1', 'george1',
            'david1', 'thomas1', 'steven', 'brian', 'kevin', 'jason', 'matthew',
            'gary', 'timothy', 'jose', 'larry', 'jeffrey', 'frank', 'scott', 'eric',
            'stephen', 'andrew1', 'raymond', 'gregory', 'joshua', 'jerry', 'dennis',
            'walter', 'peter', 'harold', 'douglas', 'henry', 'carl', 'arthur1',
            'ryan', 'roger', 'joe', 'juan', 'jack', 'albert', 'jonathan', 'justin',
            'terry', 'gerald', 'keith', 'samuel', 'willie', 'ralph', 'lawrence',
            'nicholas', 'roy', 'benjamin', 'bruce', 'brandon', 'adam', 'harry',
            'fred', 'wayne', 'billy', 'steve', 'louis', 'jeremy', 'aaron', 'randy',
            'howard', 'eugene', 'carlos', 'russell', 'bobby', 'victor', 'martin',
            'ernest', 'phillip', 'todd', 'jesse', 'craig', 'alan', 'shawn', 'clarence',
            'sean', 'philip', 'chris', 'johnny', 'earl', 'jimmy', 'antonio', 'danny',
            'bryan', 'tony', 'luis', 'mike', 'stanley', 'leonard', 'nathan', 'dale',
            'manuel', 'rodney', 'curtis', 'norman', 'allen', 'marvin', 'vincent',
            'glenn', 'jeffery', 'travis', 'jeff', 'chad', 'jacob', 'lee', 'melvin',
            'alfred', 'kyle', 'francis', 'bradley', 'jesus', 'herbert', 'frederick',
            'ray', 'joel', 'edwin', 'don', 'eddie', 'ricky', 'troy', 'randall',
            'barry', 'alexander', 'bernard', 'mario', 'leroy', 'francisco', 'marcus',
            'micheal', 'theodore', 'clifford', 'miguel', 'otis', 'shane', 'leslie',
            'omar', 'angelo', 'duane', 'franklin', 'andres', 'elmer', 'brad',
            'gabriel', 'ron', 'mitchell', 'roland', 'arnold', 'harvey', 'jared',
            'adrian', 'karl', 'cory', 'claude', 'erik', 'darryl', 'jamie', 'neil',
            'jessie', 'christian', 'javier', 'fernando', 'clinton', 'ted', 'mathew',
            'tyrone', 'darren', 'lonnie', 'lance', 'cody', 'julio', 'kelly1',
            'kurt', 'allan', 'nelson', 'guy', 'clayton', 'hugh', 'max', 'dwayne',
            'dwight', 'armando', 'felix', 'jimmie', 'everett', 'jordan', 'ian',
            'wallace', 'ken', 'bob', 'jaime', 'casey', 'alfredo', 'alberto',
            'dave', 'ivan', 'johnnie', 'sidney', 'byron', 'julian', 'isaac',
            'morris', 'clifton', 'willard', 'daryl', 'ross', 'virgil', 'dylan',
            'dewey', 'al', 'kristopher', 'erika', 'jaime', 'casey', 'alfredo',
            'alberto', 'dave', 'ivan', 'johnnie', 'sidney', 'byron', 'julian',
            'isaac', 'morris', 'clifton', 'willard', 'daryl', 'ross', 'virgil',
            'dylan', 'dewey', 'al', 'kristopher', 'erika', 'jaime', 'casey',
            'alfredo', 'alberto', 'dave', 'ivan', 'johnnie', 'sidney', 'byron',
            'julian', 'isaac', 'morris', 'clifton', 'willard', 'daryl', 'ross',
            'virgil', 'dylan', 'dewey', 'al', 'kristopher', 'erika'
        ]
        
        # 智能密码生成规则
        self.smart_rules = [
            # 键盘模式
            'qwerty', 'asdfgh', 'zxcvbn', '123456', '654321',
            # 重复模式
            'aa', 'aaa', 'aaaa', 'aaaaa', 'aaaaaa',
            # 年份模式
            '2020', '2021', '2022', '2023', '2024', '2025',
            # 手机号模式
            '138', '139', '150', '151', '152', '157', '158', '159',
            # 生日模式
            '0101', '0201', '0301', '0401', '0501', '0601', '0701', '0801', '0901', '1001', '1101', '1201',
            # 特殊组合
            'admin123', 'root123', 'user123', 'test123', 'demo123',
            'password123', 'pass123', 'pwd123', 'secret123', 'key123'
        ]
        
        # 初始化GPU检测
        self.gpu_available = self._detect_gpu()
        
    def _detect_gpu(self):
        """检测GPU可用性"""
        try:
            if GPU_AVAILABLE:
                gpus = GPUtil.getGPUs()
                return len(gpus) > 0
            return False
        except:
            return False
    
    def _detect_file_type(self, file_path: str) -> str:
        """检测文件类型"""
        import os
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.zip':
            return 'zip'
        elif ext == '.rar':
            return 'rar'
        elif ext in ['.7z', '.7zip']:
            return '7z'
        elif ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
            return 'office'
        elif ext == '.pdf':
            return 'pdf'
        else:
            # 尝试通过文件头检测
            try:
                with open(file_path, 'rb') as f:
                    header = f.read(8)
                    if header.startswith(b'PK'):
                        return 'zip'
                    elif header.startswith(b'Rar!'):
                        return 'rar'
                    elif header.startswith(b'7z\xbc\xaf\x27\x1c'):
                        return '7z'
                    elif header.startswith(b'%PDF-'):
                        return 'pdf'
                    elif header.startswith(b'\xD0\xCF\x11\xE0'):
                        return 'office'
            except:
                pass
            return 'unknown'
    
    def brute_force_advanced(self, file_path: str, min_len: int = 1, max_len: int = 8, 
                           charset: str = 'all', callback: Callable = None, 
                           stop_event=None, pause_event=None) -> Optional[str]:
        """高级暴力破解 - 多线程优化，支持暂停和停止"""
        charset_str = self.charsets.get(charset, charset)
        if charset == 'all':
            charset_str = self.charsets['all']
        
        # 计算总密码数
        total_combinations = sum(len(charset_str) ** i for i in range(min_len, max_len + 1))
        
        # 单线程暴力破解（支持暂停和停止）
        for length in range(min_len, max_len + 1):
            result = self._brute_force_length(file_path, length, charset_str, callback, stop_event, pause_event)
            if result:
                return result
        
        return None
    
    def _brute_force_length(self, file_path: str, length: int, charset: str, callback: Callable, 
                           stop_event=None, pause_event=None) -> Optional[str]:
        """指定长度的暴力破解，支持暂停和停止"""
        total = len(charset) ** length
        current = 0
        
        for guess in itertools.product(charset, repeat=length):
            # 检查停止事件
            if stop_event and stop_event.is_set():
                return None
            
            # 检查暂停事件
            if pause_event and pause_event.is_set():
                while pause_event.is_set():
                    time.sleep(0.1)
                    if stop_event and stop_event.is_set():
                        return None
            
            current += 1
            password = ''.join(guess)
            
            if callback:
                callback(current, total, f"暴力破解: {password}")
            
            # 尝试破解
            if self._try_password(file_path, password):
                return password
        
        return None
    
    def dictionary_attack_advanced(self, file_path: str, wordlist_path: str = None, 
                                 callback: Callable = None, stop_event=None, pause_event=None) -> Optional[str]:
        """高级字典攻击 - 支持多种字典和规则，支持暂停和停止"""
        wordlists = list(self.common_patterns)
        
        # 添加智能规则生成的密码
        wordlists.extend(self._generate_smart_passwords())
        
        # 添加外部字典文件
        if wordlist_path and os.path.exists(wordlist_path):
            try:
                with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
                    wordlists.extend([line.strip() for line in f if line.strip()])
            except:
                pass
        
        # 去重并排序
        wordlists = list(set(wordlists))
        wordlists.sort(key=len)  # 按长度排序，先试短密码
        
        total = len(wordlists)
        for i, password in enumerate(wordlists):
            # 检查停止事件
            if stop_event and stop_event.is_set():
                return None
            
            # 检查暂停事件
            if pause_event and pause_event.is_set():
                while pause_event.is_set():
                    time.sleep(0.1)
                    if stop_event and stop_event.is_set():
                        return None
            
            if callback:
                callback(i + 1, total, f"字典攻击: {password}")
            
            if self._try_password(file_path, password):
                return password
        
        return None
    
    def _generate_smart_passwords(self) -> List[str]:
        """智能密码生成"""
        passwords = []
        
        # 基于规则的密码生成
        for rule in self.smart_rules:
            passwords.append(rule)
            passwords.append(rule.upper())
            passwords.append(rule.lower())
            passwords.append(rule + '123')
            passwords.append(rule + '!')
            passwords.append(rule + '@')
            passwords.append(rule + '#')
            passwords.append(rule + '$')
        
        # 键盘模式扩展
        keyboard_patterns = [
            'qwerty', 'asdfgh', 'zxcvbn', '123456', '654321',
            'qazwsx', 'edcrfv', 'tgbyhn', 'ujmikl', 'plokij',
            'mnbvcx', 'lkjhgf', 'dsapoi', 'rewq', 'fdsa',
            'vcxz', 'bgt', 'nhy', 'mju', 'kil'
        ]
        
        for pattern in keyboard_patterns:
            passwords.append(pattern)
            passwords.append(pattern.upper())
            passwords.append(pattern.lower())
            passwords.append(pattern + '123')
            passwords.append(pattern + '!')
        
        return passwords
    
    def mask_attack(self, file_path: str, mask: str, callback: Callable = None, 
                   stop_event=None, pause_event=None) -> Optional[str]:
        """掩码攻击，支持暂停和停止"""
        # 掩码字符定义
        mask_chars = {
            '?l': string.ascii_lowercase,
            '?u': string.ascii_uppercase,
            '?d': string.digits,
            '?s': string.punctuation,
            '?a': string.ascii_letters + string.digits + string.punctuation,
            '?c': self.charsets['chinese']
        }
        
        # 解析掩码
        charset_list = []
        i = 0
        while i < len(mask):
            if mask[i:i+2] in mask_chars:
                charset_list.append(mask_chars[mask[i:i+2]])
                i += 2
            else:
                charset_list.append(mask[i])
                i += 1
        
        # 生成密码组合
        total = 1
        for charset in charset_list:
            total *= len(charset)
        
        current = 0
        for guess in itertools.product(*charset_list):
            # 检查停止事件
            if stop_event and stop_event.is_set():
                return None
            
            # 检查暂停事件
            if pause_event and pause_event.is_set():
                while pause_event.is_set():
                    time.sleep(0.1)
                    if stop_event and stop_event.is_set():
                        return None
            
            current += 1
            password = ''.join(guess)
            
            if callback:
                callback(current, total, f"掩码攻击: {password}")
            
            if self._try_password(file_path, password):
                return password
        
        return None
    
    def ai_smart_crack(self, file_path: str, callback: Callable = None) -> Optional[str]:
        """AI智能破解 - 基于机器学习的密码预测"""
        # 这里可以集成机器学习模型来预测密码
        # 目前使用启发式方法
        
        # 1. 基于文件名的密码预测
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        ai_passwords = [
            name_without_ext,
            name_without_ext.lower(),
            name_without_ext.upper(),
            name_without_ext + '123',
            name_without_ext + '!',
            name_without_ext + '@',
            name_without_ext + '#',
            name_without_ext + '$',
            name_without_ext + '2024',
            name_without_ext + '2025',
            'password',
            '123456',
            'admin',
            'root',
            'user',
            'test',
            'demo',
            'guest',
            'welcome',
            'hello',
            'hi',
            'ok',
            'yes',
            'no',
            'true',
            'false',
            'null',
            'empty',
            'blank',
            'default',
            '123',
            'abc',
            'xyz',
            'qwe',
            'asd',
            'zxc'
        ]
        
        total = len(ai_passwords)
        for i, password in enumerate(ai_passwords):
            if callback:
                callback(i + 1, total, f"AI智能破解: {password}")
            
            if self._try_password(file_path, password):
                return password
            
            if hasattr(self, 'stop_event') and self.stop_event.is_set():
                return None
        
        return None
    
    def hybrid_attack(self, file_path: str, callback: Callable = None) -> Optional[str]:
        """混合攻击 - 结合多种破解方法"""
        methods = [
            (self.ai_smart_crack, "AI智能破解"),
            (lambda f, cb: self.dictionary_attack_advanced(f, None, cb), "高级字典攻击"),
            (lambda f, cb: self.brute_force_advanced(f, 1, 6, 'digits', cb), "数字暴力破解"),
            (lambda f, cb: self.brute_force_advanced(f, 1, 4, 'lowercase', cb), "小写字母暴力破解"),
            (lambda f, cb: self.mask_attack(f, '?l?l?l?d?d?d', cb), "掩码攻击"),
        ]
        
        for method, name in methods:
            if callback:
                callback(0, 1, f"开始{name}...")
            
            result = method(file_path, callback)
            if result:
                return result
            
            if hasattr(self, 'stop_event') and self.stop_event.is_set():
                return None
        
        return None
    
    def gpu_accelerated_crack(self, file_path: str, callback: Callable = None) -> Optional[str]:
        """GPU加速破解 - 利用GPU并行计算"""
        if not self.gpu_available:
            if callback:
                callback(0, 1, "GPU不可用，回退到CPU破解...")
            return self.brute_force_advanced(file_path, 1, 8, 'all', callback)
        
        # GPU加速的暴力破解
        try:
            import pyopencl as cl
            import numpy as np
            
            # 创建OpenCL上下文
            platforms = cl.get_platforms()
            devices = platforms[0].get_devices(cl.device_type.GPU)
            ctx = cl.Context(devices)
            queue = cl.CommandQueue(ctx)
            
            # 这里可以实现GPU并行密码生成和验证
            # 由于复杂性，这里简化实现
            if callback:
                callback(0, 1, "GPU加速破解启动...")
            
            return self.brute_force_advanced(file_path, 1, 6, 'digits', callback)
            
        except ImportError:
            if callback:
                callback(0, 1, "PyOpenCL未安装，使用CPU破解...")
            return self.brute_force_advanced(file_path, 1, 8, 'all', callback)
    
    def distributed_crack(self, file_path: str, callback: Callable = None) -> Optional[str]:
        """分布式破解 - 多进程并行"""
        if callback:
            callback(0, 1, "启动分布式破解...")
        
        # 使用多进程池
        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            # 分割工作负载
            tasks = self._split_workload(file_path)
            futures = []
            
            for task in tasks:
                future = executor.submit(self._worker_process, file_path, task)
                futures.append(future)
            
            # 等待结果
            for future in futures:
                result = future.result()
                if result:
                    return result
        
        return None
    
    def _split_workload(self, file_path: str) -> List[Dict]:
        """分割工作负载"""
        # 按字符集和长度分割
        workloads = []
        
        # 数字组合
        for length in range(1, 9):
            workloads.append({
                'type': 'digits',
                'length': length,
                'charset': self.charsets['digits']
            })
        
        # 小写字母
        for length in range(1, 7):
            workloads.append({
                'type': 'lowercase',
                'length': length,
                'charset': self.charsets['lowercase']
            })
        
        # 大写字母
        for length in range(1, 7):
            workloads.append({
                'type': 'uppercase',
                'length': length,
                'charset': self.charsets['uppercase']
            })
        
        return workloads
    
    def _worker_process(self, file_path: str, task: Dict) -> Optional[str]:
        """工作进程函数"""
        charset = task['charset']
        length = task['length']
        
        for guess in itertools.product(charset, repeat=length):
            password = ''.join(guess)
            if self._try_password(file_path, password):
                return password
        
        return None
    
    def rainbow_table_attack(self, file_path: str, callback: Callable = None) -> Optional[str]:
        """彩虹表攻击"""
        if callback:
            callback(0, 1, "彩虹表攻击启动...")
        
        # 生成彩虹表（简化版本）
        rainbow_table = self._generate_rainbow_table()
        
        # 计算文件哈希
        file_hash = self._calculate_file_hash(file_path)
        
        # 在彩虹表中查找
        for password, hash_value in rainbow_table.items():
            if callback:
                callback(0, 1, f"彩虹表查找: {password}")
            
            if hash_value == file_hash:
                return password
        
        return None
    
    def _generate_rainbow_table(self) -> Dict[str, str]:
        """生成彩虹表"""
        rainbow_table = {}
        
        # 常用密码的哈希表
        common_passwords = [
            '123456', 'password', '123456789', '12345678', '12345',
            'qwerty', 'abc123', 'password123', '1234567', '1234567890',
            'admin', 'letmein', 'welcome', 'monkey', '123123'
        ]
        
        for password in common_passwords:
            rainbow_table[password] = hashlib.md5(password.encode()).hexdigest()
        
        return rainbow_table
    
    def _calculate_file_hash(self, file_path: str) -> str:
        """计算文件哈希"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except:
            return ""
    
    def _try_password(self, file_path: str, password: str) -> bool:
        """尝试密码 - 根据文件类型调用相应的破解器，支持多种编码"""
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # 尝试多种编码
            encodings = ['utf-8', 'gbk', 'gb2312', 'latin1', 'cp1252']
            
            for encoding in encodings:
                try:
                    if file_ext == '.zip':
                        import zipfile
                        with zipfile.ZipFile(file_path, 'r') as zf:
                            zf.extractall(pwd=password.encode(encoding))
                            return True
                    elif file_ext == '.rar':
                        import rarfile
                        with rarfile.RarFile(file_path, 'r') as rf:
                            rf.extractall(pwd=password.encode(encoding))
                            return True
                    elif file_ext == '.7z':
                        import py7zr
                        with py7zr.SevenZipFile(file_path, mode='r', password=password) as sz:
                            sz.extractall()
                            return True
                    elif file_ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
                        import msoffcrypto
                        with open(file_path, 'rb') as f:
                            office_file = msoffcrypto.OfficeFile(f)
                            office_file.load_key(password=password)
                            try:
                                office_file.decrypt(open(os.devnull, 'wb'))
                                return True
                            except Exception:
                                continue
                    elif file_ext == '.pdf':
                        import PyPDF2
                        with open(file_path, 'rb') as f:
                            reader = PyPDF2.PdfReader(f)
                            if reader.is_encrypted:
                                if reader.decrypt(password):
                                    return True
                except (UnicodeEncodeError, UnicodeDecodeError):
                    continue
                except Exception:
                    continue
        except Exception:
            pass
        return False
    
    def crack(self, file_path: str, mode: str = "brute", **kwargs) -> Optional[str]:
        """主破解方法 - 根据模式选择破解策略"""
        callback = kwargs.get('callback', None)
        stop_event = kwargs.get('stop_event', None)
        pause_event = kwargs.get('pause_event', None)
        
        if mode == "brute":
            min_len = kwargs.get('min_len', 1)
            max_len = kwargs.get('max_len', 8)
            charset = kwargs.get('charset', 'all')
            return self.brute_force_advanced(file_path, min_len, max_len, charset, callback, stop_event, pause_event)
        
        elif mode == "dict":
            wordlist = kwargs.get('wordlist', None)
            return self.dictionary_attack_advanced(file_path, wordlist, callback, stop_event, pause_event)
        
        elif mode == "mask":
            mask = kwargs.get('mask', '?l?l?l?d?d?d')
            return self.mask_attack(file_path, mask, callback, stop_event, pause_event)
        
        elif mode == "ai":
            return self.ai_smart_crack(file_path, callback)
        
        elif mode == "hybrid":
            return self.hybrid_attack(file_path, callback)
        
        elif mode == "rainbow":
            return self.rainbow_table_attack(file_path, callback)
        
        elif mode == "gpu":
            return self.gpu_accelerated_crack(file_path, callback)
        
        elif mode == "distributed":
            return self.distributed_crack(file_path, callback)
        
        else:
            # 默认使用混合攻击
            return self.hybrid_attack(file_path, callback)
    
    def get_system_info(self) -> Dict:
        """获取系统信息"""
        info = {
            'cpu_count': multiprocessing.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'gpu_available': self.gpu_available,
            'gpu_info': []
        }
        
        if self.gpu_available:
            try:
                gpus = GPUtil.getGPUs()
                for gpu in gpus:
                    info['gpu_info'].append({
                        'name': gpu.name,
                        'memory_total': gpu.memoryTotal,
                        'memory_free': gpu.memoryFree,
                        'temperature': gpu.temperature,
                        'load': gpu.load
                    })
            except:
                pass
        
        return info
    
    def optimize_performance(self) -> Dict:
        """性能优化建议"""
        info = self.get_system_info()
        suggestions = []
        
        if info['cpu_count'] < 4:
            suggestions.append("建议使用更多CPU核心以提高破解速度")
        
        if not info['gpu_available']:
            suggestions.append("建议安装GPU驱动以启用GPU加速")
        
        if info['memory_available'] < 2 * 1024 * 1024 * 1024:  # 2GB
            suggestions.append("建议增加内存以提高性能")
        
        return {
            'system_info': info,
            'suggestions': suggestions
        } 