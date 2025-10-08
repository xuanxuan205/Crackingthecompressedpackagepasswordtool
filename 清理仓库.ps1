# 清理GitHub仓库脚本
# 删除不需要的开发文件，保留发布相关文件

Write-Host "🧹 开始清理仓库，转换为发布型仓库..." -ForegroundColor Green

# 需要删除的开发文件和目录
$filesToDelete = @(
    "advanced_engine.py",
    "build.py", 
    "crack_window.py",
    "create_icon.py",
    "main.py",
    "main.spec",
    "requirements.txt",
    "simple_test.py",
    "test_advanced_mask.py", 
    "test_cracking.py",
    "version.txt",
    "__pycache__",
    ".idea",
    "cracker",
    "utils",
    "logs",
    "crack_results"
)

# 需要保留的文件
$filesToKeep = @(
    "破解压缩包密码工具.zip",
    "README.md",
    "LICENSE", 
    "发布指南.md",
    "docs",
    "screenshots",
    "releases",
    ".github",
    ".git",
    "images"
)

Write-Host "📋 将要删除的文件:" -ForegroundColor Yellow
foreach ($file in $filesToDelete) {
    if (Test-Path $file) {
        Write-Host "  ❌ $file" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "📋 将要保留的文件:" -ForegroundColor Yellow  
foreach ($file in $filesToKeep) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file" -ForegroundColor Green
    }
}

Write-Host ""
$confirm = Read-Host "确认删除上述文件吗？(y/N)"

if ($confirm -eq 'y' -or $confirm -eq 'Y') {
    Write-Host "🗑️ 开始删除文件..." -ForegroundColor Yellow
    
    foreach ($file in $filesToDelete) {
        if (Test-Path $file) {
            try {
                Remove-Item $file -Recurse -Force
                Write-Host "  ✅ 已删除: $file" -ForegroundColor Green
            }
            catch {
                Write-Host "  ❌ 删除失败: $file - $($_.Exception.Message)" -ForegroundColor Red
            }
        }
    }
    
    Write-Host ""
    Write-Host "✅ 仓库清理完成!" -ForegroundColor Green
    Write-Host "📁 当前保留的文件:" -ForegroundColor Cyan
    Get-ChildItem | ForEach-Object { Write-Host "  📄 $($_.Name)" -ForegroundColor Gray }
    
    Write-Host ""
    Write-Host "🚀 下一步操作:" -ForegroundColor Yellow
    Write-Host "  1. 检查README.md中的下载链接" -ForegroundColor Gray
    Write-Host "  2. git add ." -ForegroundColor Gray
    Write-Host "  3. git commit -m '转换为发布型仓库'" -ForegroundColor Gray
    Write-Host "  4. git push origin main" -ForegroundColor Gray
    Write-Host "  5. 在GitHub创建Release并上传zip文件" -ForegroundColor Gray
    
} else {
    Write-Host "❌ 操作已取消" -ForegroundColor Red
}

Write-Host ""
Write-Host "💡 提示: 运行前请确保已备份重要文件!" -ForegroundColor Cyan