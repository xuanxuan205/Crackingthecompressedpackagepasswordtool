# GitHub仓库重构部署脚本
# 将源码仓库转换为发布型仓库

param(
    [Parameter(Mandatory=$true)]
    [string]$Version,
    
    [switch]$CreateRelease,
    [switch]$CleanBuild,
    [string]$GitHubToken = $env:GITHUB_TOKEN
)

Write-Host "🚀 开始GitHub仓库重构部署..." -ForegroundColor Green
Write-Host "版本: v$Version" -ForegroundColor Cyan

# 1. 清理旧的构建文件
if ($CleanBuild) {
    Write-Host "🧹 清理旧的构建文件..." -ForegroundColor Yellow
    if (Test-Path "releases") {
        Remove-Item "releases" -Recurse -Force -ErrorAction SilentlyContinue
    }
    if (Test-Path "temp_*") {
        Remove-Item "temp_*" -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# 2. 创建目录结构
Write-Host "📁 创建目录结构..." -ForegroundColor Yellow
$dirs = @(
    "releases\latest",
    "releases\archive\v$Version", 
    "docs",
    "screenshots",
    "build-scripts",
    ".github\workflows",
    ".github\ISSUE_TEMPLATE"
)

foreach ($dir in $dirs) {
    if (!(Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ 创建: $dir" -ForegroundColor Green
    }
}

# 3. 运行打包脚本
Write-Host "📦 执行打包..." -ForegroundColor Yellow
if (Test-Path "build-scripts\package.ps1") {
    & ".\build-scripts\package.ps1" -Version $Version -OutputDir "releases\latest"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✅ 打包成功" -ForegroundColor Green
    } else {
        Write-Host "  ❌ 打包失败" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  ⚠️ 打包脚本不存在，跳过打包" -ForegroundColor Yellow
}

# 4. 创建GitHub Issue模板
Write-Host "📝 创建Issue模板..." -ForegroundColor Yellow

# Bug报告模板
@"
---
name: 🐛 Bug报告
about: 报告软件问题
title: '[BUG] '
labels: bug
assignees: ''
---

## 🐛 问题描述
简要描述遇到的问题

## 🔄 复现步骤
1. 打开程序
2. 执行操作 '...'
3. 查看错误

## 💭 预期行为
描述您期望发生的情况

## 📱 环境信息
- 操作系统: [例如 Windows 11]
- 软件版本: [例如 v1.0]
- 压缩包格式: [例如 ZIP]

## 📎 附加信息
- 错误截图
- 日志文件
- 其他相关信息
"@ | Out-File -FilePath ".github\ISSUE_TEMPLATE\bug_report.md" -Encoding UTF8

# 功能请求模板
@"
---
name: ✨ 功能请求
about: 建议新功能
title: '[FEATURE] '
labels: enhancement
assignees: ''
---

## ✨ 功能描述
描述您希望添加的功能

## 🎯 使用场景
说明这个功能的使用场景和必要性

## 💡 实现建议
如果有实现想法，请详细说明

## 📋 替代方案
是否有其他可行的解决方案

## 📎 附加信息
其他相关信息、截图或参考链接
"@ | Out-File -FilePath ".github\ISSUE_TEMPLATE\feature_request.md" -Encoding UTF8

Write-Host "  ✅ Issue模板创建完成" -ForegroundColor Green

# 5. 创建使用指南
Write-Host "📖 创建使用指南..." -ForegroundColor Yellow
@"
# 🎯 快速使用指南

## 📥 下载安装

### 1. 选择版本
访问 [Releases页面](../../releases) 选择合适的版本：
- **完整版**: 功能全面，包含所有工具和字典
- **精简版**: 体积小巧，基础功能够用

### 2. 下载解压
- 点击下载链接获取压缩包
- 解压到英文路径目录（避免中文路径问题）
- 确保有足够的磁盘空间

### 3. 运行程序
- 双击 ``启动工具.bat`` 启动程序
- 首次运行可能需要管理员权限
- 如被杀毒软件拦截，请添加到白名单

## 🔧 基本操作

### 选择文件
1. 点击"浏览"按钮
2. 选择要破解的压缩文件
3. 确认文件路径显示正确

### 配置破解
1. **破解模式**:
   - 字典攻击：适合常见密码
   - 暴力破解：尝试所有组合
   - 混合模式：推荐选择

2. **高级设置**:
   - 线程数：建议设为CPU核心数×2
   - 超时时间：根据密码复杂度设定
   - 字符集：选择可能的字符范围

### 开始破解
1. 检查所有设置
2. 点击"开始破解"按钮
3. 观察进度和状态信息
4. 等待破解完成

## ⚡ 使用技巧

### 提高成功率
- 了解密码可能的规律
- 使用相关的字典文件
- 尝试常见的密码组合
- 考虑密码的时间背景

### 优化性能
- 关闭不必要的程序
- 使用SSD硬盘
- 保持系统散热良好
- 合理设置线程数

## ❓ 常见问题

### Q: 程序无法启动？
A: 
- 检查是否安装了.NET Framework
- 尝试以管理员身份运行
- 确认系统满足要求

### Q: 破解速度很慢？
A:
- 检查CPU使用率
- 调整线程数设置
- 确认没有其他程序占用资源

### Q: 一直破解不出来？
A:
- 尝试不同的字典
- 检查密码长度设置
- 考虑使用混合模式

### Q: 杀毒软件报毒？
A:
- 这是常见的误报
- 可以添加到白名单
- 或临时关闭实时保护

## 🔒 安全提醒

⚠️ **重要声明**:
- 仅用于恢复自己忘记的密码
- 不得用于破解他人文件
- 使用前请确认有合法权限
- 遵守当地法律法规

## 📞 获取帮助

- 📖 [详细文档](docs/)
- 🐛 [问题反馈](../../issues)  
- 💬 [讨论交流](../../discussions)
- 📧 技术支持邮箱

---
💡 更多高级功能和技巧请查看完整文档！
"@ | Out-File -FilePath "USAGE_GUIDE.md" -Encoding UTF8

Write-Host "  ✅ 使用指南创建完成" -ForegroundColor Green

# 6. 更新README中的徽章链接
Write-Host "🏷️ 更新README徽章..." -ForegroundColor Yellow
if (Test-Path "README.md") {
    $readmeContent = Get-Content "README.md" -Raw
    # 这里可以根据实际的GitHub仓库地址替换徽章链接
    Write-Host "  ℹ️ 请手动更新README.md中的GitHub仓库链接" -ForegroundColor Cyan
}

# 7. 创建GitHub Release (如果指定)
if ($CreateRelease -and $GitHubToken) {
    Write-Host "🎯 创建GitHub Release..." -ForegroundColor Yellow
    
    # 这里需要GitHub CLI或REST API调用
    Write-Host "  ℹ️ 请使用GitHub网页界面或GitHub CLI创建Release" -ForegroundColor Cyan
    Write-Host "  📋 建议的Release信息:" -ForegroundColor Cyan
    Write-Host "    标题: 压缩包密码破解工具 v$Version" -ForegroundColor Gray
    Write-Host "    标签: v$Version" -ForegroundColor Gray
    Write-Host "    文件: releases/latest/*.zip" -ForegroundColor Gray
}

# 8. 生成部署报告
Write-Host "📊 生成部署报告..." -ForegroundColor Yellow
$reportPath = "deployment-report-v$Version.txt"
@"
GitHub仓库重构部署报告
========================

部署版本: v$Version
部署时间: $(Get-Date)
操作系统: $($env:OS)

已创建的文件结构:
$(Get-ChildItem -Recurse | Select-Object -ExpandProperty FullName | ForEach-Object { "  $_" } | Out-String)

下一步操作:
1. 检查所有文件是否正确创建
2. 更新README.md中的仓库链接
3. 提交所有更改到Git仓库
4. 创建GitHub Release
5. 测试下载链接

注意事项:
- 确保所有链接指向正确的仓库地址
- 验证打包文件的完整性
- 测试用户下载和使用流程
- 监控用户反馈和Issues

技术支持:
如有问题请查看USAGE_GUIDE.md或提交Issue
"@ | Out-File -FilePath $reportPath -Encoding UTF8

Write-Host "✅ 部署完成!" -ForegroundColor Green
Write-Host "📋 部署报告已保存到: $reportPath" -ForegroundColor Cyan
Write-Host "" 
Write-Host "🎯 下一步操作:" -ForegroundColor Yellow
Write-Host "  1. git add ." -ForegroundColor Gray
Write-Host "  2. git commit -m '重构为发布型仓库 v$Version'" -ForegroundColor Gray
Write-Host "  3. git push origin main" -ForegroundColor Gray
Write-Host "  4. 在GitHub创建Release并上传文件" -ForegroundColor Gray
Write-Host ""
Write-Host "🌟 仓库重构完成，现在用户可以直接下载使用了！" -ForegroundColor Green