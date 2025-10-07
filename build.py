import PyInstaller.__main__
import os
import shutil
import glob

def build_exe():
    # 清理旧的构建文件
    if os.path.exists('dist_new'):
        shutil.rmtree('dist_new')
    if os.path.exists('build'): # Keep this for old 'build' dir
        shutil.rmtree('build')
    if os.path.exists('build_new'): # Explicitly clean build_new
        shutil.rmtree('build_new')
    
    # 构建所有必要文件和目录的绝对路径
    icon_path = os.path.join(os.getcwd(), 'assets', 'icon.ico')
    assets_src_path = os.path.join(os.getcwd(), 'assets')
    hashcat_path = os.path.join(os.getcwd(), 'bin', 'hashcat.exe')
    john_path_in_bin = os.path.join(os.getcwd(), 'bin', 'john.exe') # Assuming john.exe is now directly in bin
    
    # 针对john的特殊DLLs路径
    john_run_dir = os.path.join(os.getcwd(), 'bin', 'john-1.9.0-jumbo-1-win64', 'run')
    cygwin_dlls_dir = os.path.join(os.getcwd(), 'bin', 'john-1.9.0-jumbo-1-win64', 'usr', 'bin')

    # 检查john.exe是否存在于其原始的run目录下，如果存在，使用该路径
    if not os.path.exists(john_path_in_bin) and os.path.exists(os.path.join(john_run_dir, 'john.exe')):
        john_path_for_pyinstaller = os.path.join(john_run_dir, 'john.exe')
    else:
        john_path_for_pyinstaller = john_path_in_bin # 否则，假定它在bin目录下

    # PyInstaller 参数列表
    pyinstaller_args = [
        'main.py',
        '--name=密码破解工具',
        '--windowed',
        f'--icon={icon_path}',  # 程序图标，使用绝对路径
        f'--add-data={assets_src_path}:assets',  # 添加资源文件，使用绝对路径和冒号分隔
        '--onedir',  # 生成单文件夹
        f'--add-binary={hashcat_path}:bin',  # 添加hashcat，使用绝对路径和冒号分隔
        f'--add-binary={john_path_for_pyinstaller}:bin',  # 添加john，使用绝对路径和冒号分隔
        '--hidden-import=torch',  # 添加隐藏导入
        '--hidden-import=torch.nn',
        '--hidden-import=torch.optim',
        '--hidden-import=torch.utils.data',
        '--hidden-import=torchvision',
        '--hidden-import=torchvision.transforms',
        '--hidden-import=torchvision.models',
        '--hidden-import=PIL',
        '--hidden-import=PIL.Image',
        '--hidden-import=PIL.ImageTk',
        '--hidden-import=cv2',
        '--hidden-import=numpy',
        '--hidden-import=matplotlib',
        '--hidden-import=matplotlib.pyplot',
        '--hidden-import=matplotlib.backends.backend_tkagg',
        '--hidden-import=scipy',
        '--hidden-import=scipy.signal',
        '--hidden-import=scipy.io.wavfile',
        '--hidden-import=librosa',
        '--hidden-import=librosa.feature',
        '--hidden-import=librosa.util',
        '--hidden-import=librosa.effects',
        '--hidden-import=librosa.display',
        '--hidden-import=librosa.beat',
        '--hidden-import=librosa.decompose',
        '--hidden-import=librosa.onset',
        '--hidden-import=librosa.segment',
        '--hidden-import=librosa.sequence',
        '--hidden-import=librosa.util',
        '--hidden-import=librosa.visualization',
        '--distpath=dist_new',  # 指定新的输出目录
        '--workpath=build_new',  # 指定新的工作目录
        '--specpath=build_new',  # 指定新的spec文件目录
    ]

    PyInstaller.__main__.run(pyinstaller_args)
    
    # --- 手动复制 John the Ripper 的额外 DLLs --- #
    # 确保目标bin目录存在
    target_bin_dir = os.path.join('dist_new', '密码破解工具', 'bin')
    os.makedirs(target_bin_dir, exist_ok=True)

    # 复制 John 的 Cygwin DLLs
    if os.path.exists(cygwin_dlls_dir):
        for dll_file in glob.glob(os.path.join(cygwin_dlls_dir, 'cyg*.dll')):
            try:
                shutil.copy(dll_file, target_bin_dir)
            except shutil.SameFileError: # 如果目标文件已存在且相同，跳过
                pass
            except Exception as e:
                print(f"复制DLL文件 {dll_file} 失败: {e}")

    # 复制 John 原始运行目录下的其他DLLs
    if os.path.exists(john_run_dir):
        for dll_file in glob.glob(os.path.join(john_run_dir, '*.dll')):
            if os.path.isfile(dll_file): # 确保是文件而不是目录
                try:
                    shutil.copy(dll_file, target_bin_dir)
                except shutil.SameFileError: # 如果目标文件已存在且相同，跳过
                    pass
                except Exception as e:
                    print(f"复制DLL文件 {dll_file} 失败: {e}")

if __name__ == '__main__':
    build_exe() 