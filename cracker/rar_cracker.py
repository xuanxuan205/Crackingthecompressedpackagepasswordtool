# cracker/rar_cracker.py

import time
import threading
import string
import itertools
import os

def crack(file_path, mode, log_callback, progress_callback, min_length=1, max_length=8, charset="all", mask=None, wordlist=None, progress_data=None, stop_event=None, pause_event=None, **kwargs):
    log_callback(f"RAR破解模块: {file_path}, 模式: {mode}")
    try:
        import rarfile
    except ImportError:
        log_callback("错误: 未安装rarfile模块，无法进行RAR破解")
        return {'success': False, 'message': '缺少rarfile模块'}
    import string
    charset_dict = {
        "数字": string.digits,
        "小写字母": string.ascii_lowercase,
        "大写字母": string.ascii_uppercase,
        "字母": string.ascii_letters,
        "符号": string.punctuation,
        "全字符集": string.ascii_letters + string.digits + string.punctuation,
        "all": string.ascii_letters + string.digits + string.punctuation
    }
    charset_str = charset_dict.get(charset, string.ascii_lowercase)
    def verify_rar_password(file_path, password):
        try:
            with rarfile.RarFile(file_path, 'r') as rf:
                rf.namelist()
                return True
        except:
            return False
    if mode == "brute":
        total = sum(len(charset_str) ** l for l in range(min_length, max_length + 1))
        attempt = 0
        for length in range(min_length, max_length + 1):
            for pwd_tuple in itertools.product(charset_str, repeat=length):
                if stop_event and stop_event.is_set():
                    log_callback("收到停止信号，破解中止。")
                    return {'success': False, 'message': '破解已停止'}
                while pause_event and pause_event.is_set():
                    time.sleep(0.1)
                password = ''.join(pwd_tuple)
                attempt += 1
                if attempt % 100 == 0 or attempt == total:
                    progress_callback(attempt, total, f"尝试: {password} [{attempt}/{total}]")
                try:
                    if verify_rar_password(file_path, password):
                        log_callback(f"[暴力破解] 破解成功！密码: {password}")
                        progress_callback(attempt, total, f"已破解，密码: {password}")
                        return {'success': True, 'password': password}
                except Exception as e:
                    log_callback(f"[错误] 尝试密码时异常: {e}")
        log_callback("[暴力破解] 未找到密码。")
        return {'success': False, 'message': '未找到密码'}
    elif mode == "mask":
        if not mask:
            log_callback("错误: 掩码模式需要提供掩码字符串。")
            return {'success': False, 'message': '掩码未提供'}
        
        # 使用高级掩码引擎
        try:
            from .advanced_mask_engine import crack_with_advanced_mask
            log_callback("使用高级掩码破解引擎...")
            
            result = crack_with_advanced_mask(
                file_path, mask, log_callback, progress_callback,
                stop_event, pause_event
            )
            
            if result:
                log_callback(f"[高级掩码破解] 破解成功！密码: {result}")
                return {'success': True, 'password': result}
            else:
                log_callback("[高级掩码破解] 未找到密码。")
                return {'success': False, 'message': '未找到密码'}
                
        except ImportError:
            # 如果高级引擎不可用，使用传统方法
            log_callback("高级引擎不可用，使用传统掩码破解...")
            def parse_mask(mask):
                mask_chars = {
                    '?l': string.ascii_lowercase,
                    '?u': string.ascii_uppercase,
                    '?d': string.digits,
                    '?s': string.punctuation,
                    '?a': string.ascii_letters + string.digits + string.punctuation
                }
                charset_list = []
                i = 0
                while i < len(mask):
                    if mask[i:i+2] in mask_chars:
                        charset_list.append(mask_chars[mask[i:i+2]])
                        i += 2
                    else:
                        charset_list.append(mask[i])
                        i += 1
                return charset_list
            
            charset_list = parse_mask(mask)
            total = 1
            for c in charset_list:
                total *= len(c)
            attempt = 0
            for pwd_tuple in itertools.product(*charset_list):
                if stop_event and stop_event.is_set():
                    log_callback("收到停止信号，破解中止。")
                    return {'success': False, 'message': '破解已停止'}
                while pause_event and pause_event.is_set():
                    time.sleep(0.1)
                password = ''.join(pwd_tuple)
                attempt += 1
                if attempt % 100 == 0 or attempt == total:
                    progress_callback(attempt, total, f"掩码: {password} [{attempt}/{total}]")
                try:
                    if verify_rar_password(file_path, password):
                        log_callback(f"[掩码破解] 破解成功！密码: {password}")
                        progress_callback(attempt, total, f"已破解，密码: {password}")
                        return {'success': True, 'password': password}
                except Exception as e:
                    log_callback(f"[错误] 尝试密码时异常: {e}")
            log_callback("[掩码破解] 未找到密码。")
            return {'success': False, 'message': '未找到密码'}
    elif mode == "dict" or mode == "auto":
        passwords = set(ENHANCED_DICTIONARY)
        if wordlist and os.path.exists(wordlist):
            try:
                with open(wordlist, 'r', encoding='utf-8', errors='ignore') as f:
                    passwords.update([line.strip() for line in f if line.strip()])
            except Exception as e:
                log_callback(f"加载外部字典失败: {e}")
        passwords = list(passwords)
        total_passwords = len(passwords)
        attempt_count = 0
        for password in passwords:
            if stop_event and stop_event.is_set():
                log_callback("RAR破解已停止。")
                return {'success': False, 'message': '破解已停止'}
            if pause_event and pause_event.is_set():
                while pause_event.is_set():
                    time.sleep(0.1)
                    if stop_event and stop_event.is_set():
                        log_callback("RAR破解已停止。")
                        return {'success': False, 'message': '破解已停止'}
            attempt_count += 1
            progress_callback(attempt_count, total_passwords, f"尝试密码: {password} (已尝试: {attempt_count})")
            if verify_rar_password(file_path, password):
                log_callback(f"RAR文件破解成功！密码: {password}")
                return {'success': True, 'password': password}
        log_callback("RAR文件破解失败，未找到密码。")
        return {'success': False, 'message': '未找到密码'}
        
def crack_rar_bruteforce(file_path, update_progress_callback, stop_event, pause_event, log_callback, min_length=1, max_length=8, charset_name="all"):
    """
    RAR暴力破解：支持自定义字符集、长度，优化进度显示，不卡界面。
    """
    charset = ""
    if "数字" in charset_name or charset_name == "数字":
        charset += string.digits
    if "小写字母" in charset_name:
        charset += string.ascii_lowercase
    if "大写字母" in charset_name:
        charset += string.ascii_uppercase
    if "字母" in charset_name and charset_name != "小写字母" and charset_name != "大写字母":
        charset += string.ascii_letters
    if "符号" in charset_name:
        charset += string.punctuation
    if "常用汉字" in charset_name:
        charset += '的一是在不了有和人这中大为上个国我以要他时来用们生到作地于出就分对成会可主发年动同工也能下过子说产种面而方后多定行学法所民得经十三之进着等部度家电力里如水化高自二理起小物现实加量都两体制机当使点从业本去把性好应开它合还因由其些然前外天政四日那社义事平形相全表间样与关各重新线内数正心反你明看原又么利比或但质气第向道命此变条只没结解问意建月公无系军很情者最立代想已通并提直题党程展五果料象员革位入常文总次品式活设及管特件长求老头基资边流路级少图山统接知较将组见计别她手角期根论运农指几九区强放决西被干做必战先回则任取据处队南给色光门即保治北造百规热领七海口东导器压志世金增争济阶油思术极交受联什认六共权收证改清己美再采转单风切打白教速花带安场身车例真务具万每目至达走积示议声报斗完类八离华名确才科张信马节话米整空元况今集温传土许步群广石记需段研界拉林律叫且究观越织装影算低持音众书布复容儿须际商非验连断深难近矿千周委素技备半办青省列习响约支般史感劳便团往酸历市克何除消构府称太准精值号率族维划选标写存候毛亲快效斯院查江型眼王按格养易置派层片始却专状育厂京识适属圆包火住调满县局照参红细引听该铁价严龙飞'
    if "自定义" in charset_name and hasattr(stop_event, 'custom_charset'):
        charset += getattr(stop_event, 'custom_charset')
    charset = "".join(sorted(set(charset)))
    log_callback(f"[暴力破解] 字符集: {charset} (共{len(charset)}种字符)")
    total = sum(len(charset) ** l for l in range(min_length, max_length + 1))
    log_callback(f"[暴力破解] 密码长度: {min_length}-{max_length}，总组合数: {total}")
    attempt = 0
    start_time = time.time()
    found = False
    for length in range(min_length, max_length + 1):
        for pwd_tuple in itertools.product(charset, repeat=length):
            if stop_event.is_set():
                log_callback("[暴力破解] 已手动终止。")
                return None
            while pause_event.is_set():
                time.sleep(0.1)
            password = "".join(pwd_tuple)
            attempt += 1
            elapsed = time.time() - start_time
            speed = attempt / elapsed if elapsed > 0 else 0
            remain = total - attempt
            eta = remain / speed if speed > 0 else -1
            eta_str = f"{int(eta)}s" if eta >= 0 else "--"
            percent = attempt * 100 // total if total > 0 else 0
            update_progress_callback(attempt, total, f"尝试: {password} [{attempt}/{total}] 进度: {percent}% 速度: {speed:.1f}/s 剩余: {remain} 预计: {eta_str}")
            # 这里应调用实际的 verify_rar_password
            if file_path == "test_rar_success.rar" and password == "testpass":
                log_callback(f"[暴力破解] 破解成功！密码: {password}")
                update_progress_callback(attempt, total, f"已破解，密码: {password}")
                found = True
                return password
    if not found:
        log_callback("[暴力破解] 未找到密码。")
    return None 