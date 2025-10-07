#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import zipfile
import os
import time
import threading
import itertools
import string
import hashlib
import pickle
from typing import Dict, List, Set, Optional, Tuple, Generator
from concurrent.futures import ThreadPoolExecutor, as_completed
import queue
import multiprocessing
from dataclasses import dataclass
import re

@dataclass
class MaskPattern:
    """掩码模式数据类"""
    pattern: str
    charset: str
    length: int
    complexity: float
    probability: float

class AdvancedMaskEngine:
    """高级掩码破解引擎"""
    
    def __init__(self):
        # 扩展的字符集定义
        self.charsets = {
            '?l': string.ascii_lowercase,  # 小写字母
            '?u': string.ascii_uppercase,  # 大写字母
            '?d': string.digits,           # 数字
            '?s': string.punctuation,      # 特殊字符
            '?a': string.ascii_letters + string.digits + string.punctuation,  # 所有字符
            '?n': string.digits,           # 数字别名
            '?c': string.ascii_lowercase,  # 小写字母别名
            '?C': string.ascii_uppercase,  # 大写字母别名
            '?p': string.punctuation,      # 特殊字符别名
            '?b': string.ascii_letters,    # 字母
            '?h': '0123456789abcdef',      # 十六进制小写
            '?H': '0123456789ABCDEF',      # 十六进制大写
            '?x': '0123456789abcdefABCDEF', # 十六进制
            '?w': ' \t\n\r\v\f',           # 空白字符
            '?k': '!@#$%^&*()_+-=[]{}|;:,.<>?',  # 键盘特殊字符
            '?y': 'aeiou',                 # 元音字母
            '?Y': 'bcdfghjklmnpqrstvwxyz', # 辅音字母
            '?z': '0123456789',            # 数字别名2
            '?Z': 'abcdefghijklmnopqrstuvwxyz', # 小写字母别名2
        }
        
        # 智能字符集映射
        self.smart_charsets = {
            '?1': '123456789',             # 常用数字
            '?2': 'abcdefghijklmnopqrstuvwxyz', # 常用小写
            '?3': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', # 常用大写
            '?4': '!@#$%^&*()_+-=',        # 常用特殊字符
            '?5': '0123456789',            # 纯数字
            '?6': 'abcdefghijklmnopqrstuvwxyz0123456789', # 小写+数字
            '?7': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', # 大写+数字
            '?8': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', # 字母
            '?9': 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', # 字母+数字
        }
        
        # 密码模式分析器
        self.pattern_analyzer = PasswordPatternAnalyzer()
        
        # 缓存系统
        self.cache_file = "mask_cache.pkl"
        self.password_cache = self.load_cache()
        
        # 性能优化参数
        self.batch_size = 1000
        self.max_workers = min(multiprocessing.cpu_count(), 8)
        self.chunk_size = 10000
        
        # 统计信息
        self.stats = {
            'attempts': 0,
            'cache_hits': 0,
            'patterns_tried': 0,
            'start_time': None
        }

    def load_cache(self) -> Dict[str, bool]:
        """加载密码缓存"""
        try:
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
        except Exception:
            pass
        return {}

    def save_cache(self):
        """保存密码缓存"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.password_cache, f)
        except Exception:
            pass

    def parse_mask(self, mask: str) -> List[str]:
        """智能解析掩码"""
        charset_list = []
        i = 0
        
        while i < len(mask):
            # 检查扩展字符集
            if mask[i] == '?' and i + 1 < len(mask):
                char_code = mask[i:i+2]
                if char_code in self.charsets:
                    charset_list.append(self.charsets[char_code])
                    i += 2
                elif char_code in self.smart_charsets:
                    charset_list.append(self.smart_charsets[char_code])
                    i += 2
                else:
                    charset_list.append(mask[i])
                    i += 1
            else:
                charset_list.append(mask[i])
                i += 1
                
        return charset_list

    def optimize_mask_order(self, mask: str) -> List[str]:
        """优化掩码顺序，提高破解效率"""
        charset_list = self.parse_mask(mask)
        
        # 计算每个字符集的复杂度
        complexities = []
        for i, charset in enumerate(charset_list):
            if isinstance(charset, str) and len(charset) > 1:
                # 计算字符集复杂度
                complexity = self.calculate_charset_complexity(charset)
                complexities.append((i, complexity, charset))
            else:
                complexities.append((i, 1, charset))
        
        # 按复杂度排序，复杂度低的放在前面
        complexities.sort(key=lambda x: x[1])
        
        return [charset for _, _, charset in complexities]

    def calculate_charset_complexity(self, charset: str) -> float:
        """计算字符集复杂度"""
        if not charset:
            return 0
        
        # 字符类型权重
        weights = {
            'digit': 1.0,
            'lower': 1.2,
            'upper': 1.5,
            'special': 2.0
        }
        
        complexity = 0
        for char in charset:
            if char.isdigit():
                complexity += weights['digit']
            elif char.islower():
                complexity += weights['lower']
            elif char.isupper():
                complexity += weights['upper']
            else:
                complexity += weights['special']
        
        return complexity / len(charset)

    def generate_smart_passwords(self, mask: str) -> Generator[str, None, None]:
        """智能密码生成器"""
        charset_list = self.optimize_mask_order(mask)
        
        # 使用优化的字符集生成密码
        for combination in itertools.product(*charset_list):
            password = ''.join(combination)
            
            # 缓存检查
            if password in self.password_cache:
                self.stats['cache_hits'] += 1
                continue
                
            yield password

    def verify_zip_password(self, file_path: str, password: str) -> bool:
        """严格校验ZIP密码，尝试解压所有文件内容"""
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                for name in zf.namelist():
                    zf.read(name, pwd=password.encode())
            return True
        except Exception:
            return False

    def batch_verify_passwords(self, file_path: str, passwords: List[str]) -> Optional[str]:
        """批量验证密码，严格校验每个密码"""
        for password in passwords:
            if self.verify_zip_password(file_path, password):
                return password
        return None

    def parallel_mask_crack(self, file_path: str, mask: str, 
                          log_callback, progress_callback, 
                          stop_event=None, pause_event=None) -> Optional[str]:
        """并行掩码破解"""
        charset_list = self.parse_mask(mask)
        total_combinations = 1
        for charset in charset_list:
            if isinstance(charset, str):
                total_combinations *= len(charset)
        
        if total_combinations > 100000000:  # 超过1亿组合时警告
            log_callback(f"警告: 掩码 {mask} 将生成 {total_combinations:,} 个组合，可能需要很长时间")
        
        self.stats['start_time'] = time.time()
        self.stats['attempts'] = 0
        
        # 使用线程池进行并行处理
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            password_queue = queue.Queue()
            
            # 分批生成密码
            batch = []
            for password in self.generate_smart_passwords(mask):
                if stop_event and stop_event.is_set():
                    return None
                
                while pause_event and pause_event.is_set():
                    time.sleep(0.1)
                
                batch.append(password)
                self.stats['attempts'] += 1
                
                if len(batch) >= self.batch_size:
                    # 提交批次任务
                    future = executor.submit(self.batch_verify_passwords, file_path, batch)
                    futures.append(future)
                    batch = []
                
                # 更新进度
                if self.stats['attempts'] % 10000 == 0:
                    elapsed = time.time() - self.stats['start_time']
                    rate = self.stats['attempts'] / elapsed if elapsed > 0 else 0
                    progress_callback(
                        self.stats['attempts'], 
                        total_combinations, 
                        f"掩码破解: {password} [{self.stats['attempts']:,}/{total_combinations:,}] "
                        f"速度: {rate:.0f}/s"
                    )
            
            # 处理最后一批
            if batch:
                future = executor.submit(self.batch_verify_passwords, file_path, batch)
                futures.append(future)
            
            # 等待结果
            for future in as_completed(futures):
                if stop_event and stop_event.is_set():
                    return None
                
                result = future.result()
                if result:
                    return result
        
        return None

    def intelligent_mask_suggestions(self, file_path: str) -> List[str]:
        """智能掩码建议"""
        suggestions = []
        
        # 基于文件名的掩码建议
        filename = os.path.basename(file_path)
        name_parts = re.split(r'[._-]', filename)
        
        for part in name_parts:
            if part.isdigit():
                suggestions.append('?d' * len(part))
            elif part.isalpha():
                if part.islower():
                    suggestions.append('?l' * len(part))
                elif part.isupper():
                    suggestions.append('?u' * len(part))
                else:
                    suggestions.append('?a' * len(part))
            else:
                suggestions.append('?a' * len(part))
        
        # 常见密码模式
        common_patterns = [
            '?l?l?l?l?d?d?d?d',  # 4字母+4数字
            '?u?l?l?l?d?d?d',    # 1大写+3小写+3数字
            '?l?l?l?l?l?d?d?d',  # 5字母+3数字
            '?d?d?d?d?d?d?d?d',  # 8位数字
            '?l?l?l?l?l?l?l?l',  # 8位小写字母
            '?u?l?l?l?l?d?d?d',  # 1大写+4小写+3数字
            '?l?l?l?d?d?d?d',    # 3字母+4数字
            '?u?l?l?d?d?d?d',    # 1大写+2小写+4数字
        ]
        
        suggestions.extend(common_patterns)
        return suggestions

    def analyze_file_pattern(self, file_path: str) -> Dict[str, any]:
        """分析文件模式"""
        analysis = {
            'filename': os.path.basename(file_path),
            'extension': os.path.splitext(file_path)[1],
            'size': os.path.getsize(file_path),
            'suggested_masks': [],
            'complexity_score': 0
        }
        
        # 基于文件特征的掩码建议
        filename = analysis['filename']
        
        # 数字模式检测
        numbers = re.findall(r'\d+', filename)
        for num in numbers:
            analysis['suggested_masks'].append('?d' * len(num))
        
        # 字母模式检测
        letters = re.findall(r'[a-zA-Z]+', filename)
        for letter in letters:
            if letter.islower():
                analysis['suggested_masks'].append('?l' * len(letter))
            elif letter.isupper():
                analysis['suggested_masks'].append('?u' * len(letter))
            else:
                analysis['suggested_masks'].append('?a' * len(letter))
        
        return analysis

class PasswordPatternAnalyzer:
    """密码模式分析器"""
    
    def __init__(self):
        self.common_patterns = {
            'numeric': r'^\d+$',
            'alphabetic': r'^[a-zA-Z]+$',
            'alphanumeric': r'^[a-zA-Z0-9]+$',
            'mixed_case': r'^(?=.*[a-z])(?=.*[A-Z])[a-zA-Z0-9]+$',
            'with_special': r'[!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]'
        }
    
    def analyze_pattern(self, password: str) -> Dict[str, any]:
        """分析密码模式"""
        analysis = {
            'length': len(password),
            'has_digits': any(c.isdigit() for c in password),
            'has_lowercase': any(c.islower() for c in password),
            'has_uppercase': any(c.isupper() for c in password),
            'has_special': any(c in string.punctuation for c in password),
            'pattern_type': 'unknown'
        }
        
        # 确定模式类型
        if re.match(self.common_patterns['numeric'], password):
            analysis['pattern_type'] = 'numeric'
        elif re.match(self.common_patterns['alphabetic'], password):
            analysis['pattern_type'] = 'alphabetic'
        elif re.match(self.common_patterns['alphanumeric'], password):
            analysis['pattern_type'] = 'alphanumeric'
        elif re.match(self.common_patterns['mixed_case'], password):
            analysis['pattern_type'] = 'mixed_case'
        elif re.search(self.common_patterns['with_special'], password):
            analysis['pattern_type'] = 'with_special'
        
        return analysis

def crack_with_advanced_mask(file_path: str, mask: str, 
                           log_callback, progress_callback,
                           stop_event=None, pause_event=None) -> Optional[str]:
    """使用高级掩码引擎进行破解"""
    engine = AdvancedMaskEngine()
    
    log_callback(f"启动高级掩码破解引擎")
    log_callback(f"掩码: {mask}")
    log_callback(f"并行线程数: {engine.max_workers}")
    
    # 分析文件模式
    analysis = engine.analyze_file_pattern(file_path)
    log_callback(f"文件分析: {analysis['filename']} (大小: {analysis['size']:,} 字节)")
    
    # 提供智能建议
    suggestions = engine.intelligent_mask_suggestions(file_path)
    if suggestions:
        log_callback(f"智能掩码建议: {', '.join(suggestions[:5])}")
    
    # 开始破解
    result = engine.parallel_mask_crack(
        file_path, mask, log_callback, progress_callback, 
        stop_event, pause_event
    )
    
    # 保存缓存
    engine.save_cache()
    
    # 输出统计信息
    if engine.stats['start_time']:
        elapsed = time.time() - engine.stats['start_time']
        rate = engine.stats['attempts'] / elapsed if elapsed > 0 else 0
        log_callback(f"破解统计: 尝试 {engine.stats['attempts']:,} 次, "
                    f"缓存命中 {engine.stats['cache_hits']:,} 次, "
                    f"耗时 {elapsed:.1f} 秒, 速度 {rate:.0f}/s")
    
    return result 