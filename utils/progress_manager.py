import json
import os

def save_progress(file_path, progress_data):
    """
    保存破解进度到文件。
    """
    # 在实际应用中，这里会包含更复杂的逻辑来序列化进度数据
    # 例如，对于暴力破解，可能需要保存当前的字符组合、长度等
    # 对于字典破解，可能需要保存当前尝试到的字典索引
    # 为了演示，这里只做一个骨架
    try:
        output_dir = "crack_progress"
        os.makedirs(output_dir, exist_ok=True)
        progress_file = os.path.join(output_dir, f"{os.path.basename(file_path)}.progress.json")
        with open(progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress_data, f, indent=4)
        # print(f"进度已保存到: {progress_file}")
        return True
    except Exception as e:
        # print(f"保存进度失败: {e}")
        return False

def load_progress(file_path):
    """
    从文件加载破解进度。
    """
    try:
        output_dir = "crack_progress"
        progress_file = os.path.join(output_dir, f"{os.path.basename(file_path)}.progress.json")
        if os.path.exists(progress_file):
            with open(progress_file, 'r', encoding='utf-8') as f:
                progress_data = json.load(f)
            # print(f"进度已从 {progress_file} 加载。")
            return progress_data
    except Exception as e:
        # print(f"加载进度失败: {e}")
        pass
    return None 