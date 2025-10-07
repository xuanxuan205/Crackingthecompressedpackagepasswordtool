import os
import zipfile
import struct
import time

def detect_file_type(file_path):
    """
    根据文件扩展名和简单文件头检测文件类型。
    """
    file_path = str(file_path) # 确保 file_path 是字符串
    if not os.path.exists(file_path):
        return "unknown"

    # 优先根据扩展名判断
    ext = os.path.splitext(file_path)[1].lower()

    if ext == ".zip":
        return "zip"
    elif ext == ".rar":
        return "rar"
    elif ext == ".7z":
        return "7z"
    elif ext in [".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"]:
        # 对于Office文档，区分新旧格式
        if ext.endswith("x"): # .docx, .xlsx, .pptx
            return "office"
        else: # .doc, .xls, .ppt (旧格式，可能需要更复杂的检测)
            return "office"
    elif ext == ".pdf":
        return "pdf"

    # Fallback to magic bytes for more robust detection if extension is ambiguous or missing
    try:
        with open(file_path, 'rb') as f:
            header = f.read(8)

            # ZIP (PK\x03\x04 or PK\x05\x06 or PK\x07\x08)
            if header.startswith(b'\x50\x4b\x03\x04') or \
               header.startswith(b'\x50\x4b\x05\x06') or \
               header.startswith(b'\x50\x4b\x07\x08'):
                return "zip"
            # RAR (Rar!\x1a\x07\x00 or Rar!\x1a\x07\x01\x00)
            elif header.startswith(b'Rar!\x1a\x07\x00') or header.startswith(b'Rar!\x1a\x07\x01\x00'):
                return "rar"
            # 7z (7z\xbc\xaf\x27\x1c)
            elif header.startswith(b'\x37\x7a\xbc\xaf\x27\x1c'):
                return "7z"
            # PDF (%PDF-)
            elif header.startswith(b'%PDF-'):
                return "pdf"
            # Office Old Format (D0 CF 11 E0 A1 B1 1A E1 - Compound File Binary Format)
            elif header.startswith(b'\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1'):
                return "office"

    except Exception:
        pass # 忽略读取文件头时的错误

    return "unknown"

def analyze_file_metadata(file_path):
    """
    分析文件的元数据，例如是否加密。
    目前主要针对ZIP文件，判断其是否加密。
    """
    metadata = {"is_encrypted": False, "file_size": 0, "num_files": 0, "comments": ""}
    file_path = str(file_path)

    if not os.path.exists(file_path):
        return metadata

    metadata["file_size"] = os.path.getsize(file_path)

    file_type = detect_file_type(file_path)

    if file_type == "zip":
        try:
            with zipfile.ZipFile(file_path, 'r') as zf:
                metadata["num_files"] = len(zf.namelist())
                metadata["comments"] = zf.comment.decode('utf-8', errors='ignore') if zf.comment else ""
                # 检查ZIP文件是否加密
                for info in zf.infolist():
                    if info.flag_bits & 0x1: # Check if encrypted (bit 0 is set)
                        metadata["is_encrypted"] = True
                        break
        except zipfile.BadZipFile:
            # 文件损坏或不是有效的zip文件
            metadata["is_encrypted"] = True # 假设损坏文件也可能加密
        except Exception as e:
            # 捕获其他所有未知异常，例如加密文件在尝试infolist时可能抛出异常
            if "password required" in str(e).lower() or "encrypted" in str(e).lower():
                metadata["is_encrypted"] = True
            # print(f"验证ZIP文件是否加密时发生未知错误: {e}")

    # 未来可以添加对RAR, 7Z, Office, PDF等文件的加密检测逻辑

    return metadata

def export_result(file_path, password):
    """
    将破解结果导出到txt文件。
    """
    output_dir = "crack_results"
    os.makedirs(output_dir, exist_ok=True)
    
    file_name = os.path.basename(file_path)
    result_file = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_cracked.txt")

    with open(result_file, 'a', encoding='utf-8') as f:
        f.write(f"文件: {file_path}\n")
        f.write(f"破解密码: {password}\n")
        f.write(f"破解时间: {time.strftime("%Y-%m-%d %H:%M:%S")}\n")
        f.write("------------------------------------\n\n") 