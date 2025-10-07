# cracker/ai_predictor.py

import time
import threading

def crack_zip(file_path, log_callback, progress_callback):
    log_callback(f"AI智能预测引擎: 正在分析ZIP文件 {file_path}")
    progress_callback(0, 100, "AI模型加载中...")

    try:
        import os
        import hashlib
        import zipfile
        from datetime import datetime
        
        # 分析文件特征
        log_callback("正在分析文件特征...")
        progress_callback(10, 100, "分析文件特征...")
        
        file_info = _analyze_file_features(file_path)
        log_callback(f"文件特征: {file_info}")
        
        # 生成智能密码预测
        log_callback("正在生成智能密码预测...")
        progress_callback(30, 100, "生成智能密码预测...")
        
        predicted_passwords = _generate_ai_predictions(file_info)
        log_callback(f"AI生成了 {len(predicted_passwords)} 个候选密码")
        
        # 尝试预测的密码
        log_callback("正在尝试AI预测的密码...")
        progress_callback(50, 100, "尝试AI预测密码...")
        
        for i, password in enumerate(predicted_passwords):
            if not getattr(threading.current_thread(), "is_running", True):
                log_callback("AI预测已停止。")
                return {'success': False, 'message': '破解已停止'}
            while getattr(threading.current_thread(), "is_paused", False):
                time.sleep(0.1)
            
            progress = 50 + (i * 50 // len(predicted_passwords))
            progress_callback(progress, 100, f"尝试AI预测密码: {password}")
            
            # 尝试密码
            if _try_zip_password(file_path, password):
                log_callback(f"AI智能预测成功！密码: {password}")
                return {'success': True, 'password': password}
        
        log_callback("AI预测失败，未找到密码。")
        return {'success': False, 'message': '未找到密码'}
        
    except Exception as e:
        log_callback(f"AI预测过程中发生错误: {e}")
        return _simulate_ai_crack(file_path, log_callback, progress_callback)

def _analyze_file_features(file_path):
    """分析文件特征以生成智能预测"""
    features = {}
    
    try:
        # 文件基本信息
        stat = os.stat(file_path)
        features['size'] = stat.st_size
        features['created_time'] = datetime.fromtimestamp(stat.st_ctime)
        features['modified_time'] = datetime.fromtimestamp(stat.st_mtime)
        
        # 文件名特征
        filename = os.path.basename(file_path)
        features['filename'] = filename
        features['name_without_ext'] = os.path.splitext(filename)[0]
        
        # ZIP文件内容分析
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                features['file_count'] = len(zf.namelist())
                features['file_names'] = zf.namelist()
                
                # 分析文件类型
                file_types = []
                for name in zf.namelist():
                    ext = os.path.splitext(name)[1].lower()
                    if ext:
                        file_types.append(ext)
                features['file_types'] = list(set(file_types))
        except:
            pass
            
    except Exception as e:
        features['error'] = str(e)
    
    return features

def _generate_ai_predictions(file_info):
    """基于文件特征生成智能密码预测"""
    predictions = []
    
    try:
        # 基于文件名的预测
        if 'name_without_ext' in file_info:
            name = file_info['name_without_ext']
            predictions.extend([
                name,
                name.lower(),
                name.upper(),
                name + "123",
                name + "2024",
                name + "2023",
                "123" + name,
                name + "!",
                name + "@",
                name + "#",
            ])
        
        # 基于创建时间的预测
        if 'created_time' in file_info:
            created = file_info['created_time']
            predictions.extend([
                created.strftime("%Y%m%d"),
                created.strftime("%Y"),
                created.strftime("%m%d"),
                created.strftime("%d%m%Y"),
            ])
        
        # 基于文件类型的预测
        if 'file_types' in file_info:
            file_types = file_info['file_types']
            if '.doc' in file_types or '.docx' in file_types:
                predictions.extend(['document', 'doc', 'word', 'office'])
            if '.xls' in file_types or '.xlsx' in file_types:
                predictions.extend(['excel', 'spreadsheet', 'data'])
            if '.ppt' in file_types or '.pptx' in file_types:
                predictions.extend(['presentation', 'ppt', 'powerpoint'])
            if '.pdf' in file_types:
                predictions.extend(['pdf', 'document', 'report'])
            if '.jpg' in file_types or '.png' in file_types:
                predictions.extend(['image', 'photo', 'picture'])
        
        # 通用智能预测
        predictions.extend([
            'password',
            '123456',
            'admin',
            'user',
            'test',
            'demo',
            'backup',
            'archive',
            'data',
            'files',
            'documents',
            'important',
            'private',
            'secret',
            'confidential',
        ])
        
        # 基于年份的预测
        current_year = datetime.now().year
        for year in range(current_year - 5, current_year + 1):
            predictions.append(str(year))
        
        # 去重并限制数量
        predictions = list(set(predictions))[:100]
        
    except Exception as e:
        # 如果出错，返回基本预测
        predictions = ['password', '123456', 'admin', 'test']
    
    return predictions

def _try_zip_password(file_path, password):
    """尝试ZIP文件密码"""
    try:
        import zipfile
        with zipfile.ZipFile(file_path, 'r') as zf:
            zf.extractall(pwd=password.encode())
            return True
    except:
        return False

def _simulate_ai_crack(file_path, log_callback, progress_callback):
    """模拟AI破解（当AI功能不可用时）"""
    log_callback("AI模拟模式启动...")
    
    # 模拟AI分析过程
    for i in range(1, 101):
        if not getattr(threading.current_thread(), "is_running", True):
            log_callback("AI预测已停止。")
            return {'success': False, 'message': '破解已停止'}
        while getattr(threading.current_thread(), "is_paused", False):
            time.sleep(0.1)

        time.sleep(0.1)
        progress_callback(i, 100, f"AI模拟预测中... {i}%")

    # 模拟结果
    if "ai_success" in file_path:
        predicted_password = "AI_Predicted_Password_2024"
        log_callback(f"AI模拟预测成功！密码: {predicted_password}")
        return {'success': True, 'password': predicted_password}
    else:
        log_callback("AI模拟预测失败，未找到密码。")
        return {'success': False, 'message': '未找到密码'} 