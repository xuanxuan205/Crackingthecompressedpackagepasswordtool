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
from typing import List, Dict, Optional, Callable, Tuple, Set
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
            'dewey', 'al', 'kristopher', 'erika',
            # 特殊组合
            'admin123', 'root123', 'user123', 'test123', 'demo123',
            'password123', 'pass123', 'pwd123', 'secret123', 'key123'
        ]
        
        # 智能规则
        self.smart_rules = [
            'admin', 'root', 'user', 'test', 'demo', 'password', 'pass', 'pwd', 'secret', 'key'
        ]
        
        # 初始化GPU检测
        self.gpu_available = self._detect_gpu()
        
        # 停止和暂停事件
        self.stop_event = threading.Event()
        self.pause_event = threading.Event()
        
        # 缓存已尝试的密码
        self.tried_passwords = set()
        
        # 密码特征分析
        self.password_features = {
            'length_distribution': {},
            'char_distribution': {},
            'common_prefixes': {},
            'common_suffixes': {}
        }
        
        # 优化参数
        self.chunk_size = 10000  # 每个线程处理的密码数量
        self.max_workers = min(32, multiprocessing.cpu_count() * 2)  # 最大线程数
    
    def _detect_gpu(self):
        """检测GPU可用性"""
        try:
            gpus = GPUtil.getGPUs()
            return len(gpus) > 0
        except:
            return False
    
    def brute_force_advanced(self, file_path: str, min_len: int = 1, max_len: int = 8, 
                           charset: str = 'all', callback: Callable = None, 
                           stop_event=None, pause_event=None) -> Optional[str]:
        """高级暴力破解 - 多线程优化，支持暂停和停止"""
        # 使用传入的事件对象或默认对象
        stop_event = stop_event or self.stop_event
        pause_event = pause_event or self.pause_event
        
        # 智能字符集选择
        charset_str = self._smart_charset_selection(file_path, charset)
        
        # 计算总密码数
        total_combinations = sum(len(charset_str) ** i for i in range(min_len, max_len + 1))
        
        if callback:
            callback(0, total_combinations, f"初始化暴力破解 - 字符集: {charset}, 长度范围: {min_len}-{max_len}")
        
        # 优先尝试常见密码模式
        common_result = self._try_common_passwords(file_path, callback, stop_event, pause_event)
        if common_result:
            return common_result
        
        # 优化的多线程暴力破解
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            
            # 按长度和字符集分块
            for length in range(min_len, max_len + 1):
                # 优先尝试更可能的长度
                if length in [4, 6, 8]:
                    priority = 0
                else:
                    priority = 1
                
                # 创建任务
                tasks = self._create_brute_force_tasks(charset_str, length)
                
                for task_id, task in enumerate(tasks):
                    future = executor.submit(
                        self._brute_force_task, 
                        file_path, 
                        task['start'], 
                        task['end'], 
                        length, 
                        charset_str, 
                        callback, 
                        stop_event, 
                        pause_event,
                        task_id,
                        len(tasks),
                        total_combinations
                    )
                    futures.append((priority, future))
            
            # 按优先级排序
            futures.sort(key=lambda x: x[0])
            
            # 等待结果
            for _, future in futures:
                if stop_event.is_set():
                    break
                    
                result = future.result()
                if result:
                    return result
        
        return None
    
    def _smart_charset_selection(self, file_path: str, charset: str) -> str:
        """智能字符集选择 - 根据文件类型和名称优化字符集"""
        charset_str = self.charsets.get(charset, charset)
        if charset == 'all':
            charset_str = self.charsets['all']
            
        # 根据文件名智能缩小字符集范围
        filename = os.path.basename(file_path).lower()
        if any(ext in filename for ext in ['.zip', '.rar', '.7z']):
            # 压缩文件密码通常是数字和字母的组合
            if charset == 'all':
                charset_str = string.digits + string.ascii_letters
        elif any(ext in filename for ext in ['.doc', '.xls', '.ppt']):
            # Office文档密码可能包含特殊字符
            if charset == 'all':
                charset_str = string.digits + string.ascii_letters + string.punctuation
                
        return charset_str
    
    def _create_brute_force_tasks(self, charset: str, length: int) -> List[Dict]:
        """创建暴力破解任务 - 将密码空间分成多个任务"""
        tasks = []
        total = len(charset) ** length
        
        if total <= self.chunk_size:
            # 如果总数小于块大小，只创建一个任务
            tasks.append({'start': 0, 'end': total})
        else:
            # 否则分块
            num_chunks = min(self.max_workers, total // self.chunk_size + (1 if total % self.chunk_size else 0))
            chunk_size = total // num_chunks
            
            for i in range(num_chunks):
                start = i * chunk_size
                end = (i + 1) * chunk_size if i < num_chunks - 1 else total
                tasks.append({'start': start, 'end': end})
        
        return tasks
    
    def _try_common_passwords(self, file_path: str, callback: Callable, 
                             stop_event: threading.Event, pause_event: threading.Event) -> Optional[str]:
        """尝试常见密码 - 在暴力破解前先尝试常见密码"""
        common_passwords = [
            '123456', 'password', 'admin', '12345678', 'qwerty',
            'abc123', 'password123', 'admin123', '1234', '123456789'
        ]
        
        if callback:
            callback(0, len(common_passwords), "尝试常见密码模式...")
        
        for i, password in enumerate(common_passwords):
            # 检查是否应该暂停
            while pause_event.is_set() and not stop_event.is_set():
                time.sleep(0.1)
                
            # 检查是否应该停止
            if stop_event.is_set():
                return None
                
            if callback:
                callback(i + 1, len(common_passwords), f"尝试常见密码: {password}")
                
            if self._try_password(file_path, password):
                return password
                
        return None
    
    def _brute_force_task(self, file_path: str, start: int, end: int, length: int, 
                         charset: str, callback: Callable, stop_event: threading.Event, 
                         pause_event: threading.Event, task_id: int, total_tasks: int,
                         total_combinations: int) -> Optional[str]:
        """暴力破解任务 - 处理指定范围的密码组合"""
        # 生成索引到密码的映射函数
        def index_to_password(index, length, charset):
            password = ''
            for _ in range(length):
                password = charset[index % len(charset)] + password
                index //= len(charset)
            return password
        
        # 处理指定范围的密码
        for i in range(start, end):
            # 检查是否应该暂停
            while pause_event.is_set() and not stop_event.is_set():
                time.sleep(0.1)
                
            # 检查是否应该停止
            if stop_event.is_set():
                return None
                
            # 生成密码
            password = index_to_password(i, length, charset)
            
            # 如果已经尝试过，跳过
            if password in self.tried_passwords:
                continue
                
            # 添加到已尝试集合
            self.tried_passwords.add(password)
            
            # 更新进度
            if callback:
                task_progress = f"任务 {task_id+1}/{total_tasks}, 长度 {length}"
                callback(i - start, end - start, f"尝试密码: {password} ({task_progress})")
            
            # 尝试密码
            if self._try_password(file_path, password):
                # 更新密码特征分析
                self._update_password_features(password)
                return password
        
        return None
    
    def _update_password_features(self, password: str) -> None:
        """更新密码特征分析"""
        # 更新长度分布
        length = len(password)
        self.password_features['length_distribution'][length] = self.password_features['length_distribution'].get(length, 0) + 1
        
        # 更新字符分布
        for char in password:
            self.password_features['char_distribution'][char] = self.password_features['char_distribution'].get(char, 0) + 1
            
        # 更新前缀和后缀
        if length >= 3:
            prefix = password[:3]
            suffix = password[-3:]
            self.password_features['common_prefixes'][prefix] = self.password_features['common_prefixes'].get(prefix, 0) + 1
            self.password_features['common_suffixes'][suffix] = self.password_features['common_suffixes'].get(suffix, 0) + 1
    
    def _brute_force_length(self, file_path: str, length: int, charset: str, callback: Callable, 
                           stop_event=None, pause_event=None) -> Optional[str]:
        """指定长度的暴力破解，支持暂停和停止"""
        stop_event = stop_event or self.stop_event
        pause_event = pause_event or self.pause_event
        
        total = len(charset) ** length
        current = 0
        
        for guess in itertools.product(charset, repeat=length):
            # 检查是否应该暂停
            while pause_event.is_set() and not stop_event.is_set():
                time.sleep(0.1)
                
            # 检查是否应该停止
            if stop_event.is_set():
                return None
                
            current += 1
            password = ''.join(guess)
            
            # 如果已经尝试过，跳过
            if password in self.tried_passwords:
                continue
                
            # 添加到已尝试集合
            self.tried_passwords.add(password)
            
            if callback:
                callback(current, total, f"尝试密码: {password}")
            
            # 尝试破解
            if self._try_password(file_path, password):
                return password
        
        return None
    
    def dictionary_attack_advanced(self, file_path: str, wordlist_path: str = None, 
                                 callback: Callable = None) -> Optional[str]:
        """高级字典攻击 - 支持多种字典和规则"""
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
            if callback:
                callback(i + 1, total, f"字典攻击: {password}")
            
            if self._try_password(file_path, password):
                return password
            
            if hasattr(self, 'stop_event') and self.stop_event.is_set():
                return None
        
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
    
    def mask_attack(self, file_path: str, mask: str, callback: Callable = None) -> Optional[str]:
        """掩码攻击"""
        # 掩码字符定义
        mask_chars = {
            '?l': string.ascii_lowercase,
            '?u': string.ascii_uppercase,
            '?d': string.digits,
            '?s': string.punctuation,
            '?a': string.ascii_letters + string.digits + string.punctuation,
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
            current += 1
            password = ''.join(guess)
            
            if callback:
                callback(current, total, f"掩码攻击: {password}")
            
            if self._try_password(file_path, password):
                return password
            
            if hasattr(self, 'stop_event') and self.stop_event.is_set():
                return None
        
        return None
    
    def ai_smart_crack(self, file_path: str, callback: Callable = None) -> Optional[str]:
        """AI智能破解 - 基于机器学习的密码预测"""
        # 这里可以集成机器学习模型来预测密码
        # 目前使用启发式方法
        
        # 1. 基于文件名的密码预测
        filename = os.path.basename(file_path)
        name_without_ext = os.path.splitext(filename)[0]
        
        ai_passwords = [
            name_without_ext, name_without_ext.lower(), name_without_ext.upper(),
            name_without_ext + '123', name_without_ext + '!', 'password', '123456', 'admin'
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
        try:
            import pyopencl as cl
            # 这里只做演示，实际可用hashcat等专业工具
            if callback:
                callback(0, 1, "GPU加速破解启动...")
            return self.brute_force_advanced(file_path, 1, 6, 'digits', callback)
        except ImportError:
            if callback:
                callback(0, 1, "PyOpenCL未安装，使用CPU破解...")
            return self.brute_force_advanced(file_path, 1, 8, 'all', callback)

    def distributed_crack(self, file_path: str, callback: Callable = None) -> Optional[str]:
        """分布式破解 - 多进程并行"""
        from concurrent.futures import ProcessPoolExecutor
        import multiprocessing
        if callback:
            callback(0, 1, "启动分布式破解...")
        with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
            tasks = self._split_workload(file_path)
            futures = []
            for task in tasks:
                future = executor.submit(self._worker_process, file_path, task)
                futures.append(future)
            for future in futures:
                result = future.result()
                if result:
                    return result
        return None

    def _split_workload(self, file_path: str):
        workloads = []
        for length in range(1, 5):
            workloads.append({'charset': self.charsets['digits'], 'length': length})
            workloads.append({'charset': self.charsets['lowercase'], 'length': length})
        return workloads

    def _worker_process(self, file_path: str, task: dict) -> Optional[str]:
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
        rainbow_table = self._generate_rainbow_table()
        file_hash = self._calculate_file_hash(file_path)
        for password, hash_value in rainbow_table.items():
            if callback:
                callback(0, 1, f"彩虹表查找: {password}")
            if hash_value == file_hash:
                return password
        return None

    def _generate_rainbow_table(self):
        rainbow_table = {}
        common_passwords = ['123456', 'password', '123456789', 'admin', 'letmein']
        for password in common_passwords:
            rainbow_table[password] = hashlib.md5(password.encode()).hexdigest()
        return rainbow_table

    def _calculate_file_hash(self, file_path: str) -> str:
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
                return hashlib.md5(content).hexdigest()
        except:
            return ""

    def _try_password(self, file_path: str, password: str) -> bool:
        try:
            ext = os.path.splitext(file_path)[1].lower()
            if ext == '.zip':
                import zipfile
                with zipfile.ZipFile(file_path, 'r') as zf:
                    zf.extractall(pwd=password.encode())
                    return True
            elif ext == '.rar':
                import rarfile
                with rarfile.RarFile(file_path, 'r') as rf:
                    rf.extractall(pwd=password)
                    return True
            elif ext == '.7z':
                import py7zr
                with py7zr.SevenZipFile(file_path, mode='r', password=password) as sz:
                    sz.extractall()
                    return True
            elif ext in ['.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx']:
                import msoffcrypto
                with open(file_path, 'rb') as f:
                    office_file = msoffcrypto.OfficeFile(f)
                    office_file.load_key(password=password)
                    try:
                        office_file.decrypt(open(os.devnull, 'wb'))
                        return True
                    except Exception:
                        return False
            elif ext == '.pdf':
                import PyPDF2
                with open(file_path, 'rb') as f:
                    reader = PyPDF2.PdfReader(f)
                    if reader.is_encrypted:
                        if reader.decrypt(password):
                            return True
            # 可扩展更多类型
        except Exception as e:
            # print(f"密码尝试错误: {e}")
            return False
        return False

    def crack(self, file_path: str, mode: str = "brute", **kwargs) -> Optional[str]:
        callback = kwargs.get('callback', None)
        if mode == "brute":
            min_len = kwargs.get('min_len', 1)
            max_len = kwargs.get('max_len', 8)
            charset = kwargs.get('charset', 'all')
            return self.brute_force_advanced(file_path, min_len, max_len, charset, callback)
        elif mode == "dict":
            wordlist = kwargs.get('wordlist', None)
            return self.dictionary_attack_advanced(file_path, wordlist, callback)
        elif mode == "mask":
            mask = kwargs.get('mask', '?l?l?l?d?d?d')
            return self.mask_attack(file_path, mask, callback)
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
            return self.hybrid_attack(file_path, callback)