# Update Payment QR Code Script
# Used to quickly upload and update WeChat and Alipay payment QR codes

Write-Host "🔄 Payment QR Code Update Script" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green

# Check images directory
if (-not (Test-Path "images")) {
    Write-Host "📁 Creating images directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "images" -Force
}

# Check current payment QR code files
$wechatQR = "images/wechat_qr_3.png"
$alipayQR = "images/alipay_qr_3.png"

Write-Host "`n📋 Current Status Check:" -ForegroundColor Cyan

if (Test-Path $wechatQR) {
    $wechatSize = (Get-Item $wechatQR).Length
    $wechatKB = [math]::Round($wechatSize/1KB, 2)
    Write-Host "✅ WeChat Payment QR: Exists ($wechatKB KB)" -ForegroundColor Green
} else {
    Write-Host "❌ WeChat Payment QR: Not Found" -ForegroundColor Red
}

if (Test-Path $alipayQR) {
    $alipaySize = (Get-Item $alipayQR).Length  
    $alipayKB = [math]::Round($alipaySize/1KB, 2)
    Write-Host "✅ Alipay QR: Exists ($alipayKB KB)" -ForegroundColor Green
} else {
    Write-Host "❌ Alipay QR: Not Found" -ForegroundColor Red
}

Write-Host "`n🎯 Operation Options:" -ForegroundColor Cyan
Write-Host "1. Open images directory (Place your payment QR codes)"
Write-Host "2. Verify QR code files"
Write-Host "3. Upload to GitHub"
Write-Host "4. View instructions"
Write-Host "5. Exit"

do {
    $choice = Read-Host "`nPlease select operation (1-5)"
    
    switch ($choice) {
        "1" {
            Write-Host "📂 Opening images directory..." -ForegroundColor Yellow
            if (Test-Path "images") {
                Invoke-Item "images"
                Write-Host "✅ Please place your payment QR code files in this directory:" -ForegroundColor Green
                Write-Host "   - WeChat Pay: wechat_qr_3.png" -ForegroundColor White
                Write-Host "   - Alipay: alipay_qr_3.png" -ForegroundColor White
            } else {
                Write-Host "❌ Images directory does not exist" -ForegroundColor Red
            }
        }
        
        "2" {
            Write-Host "🔍 Verifying payment QR code files..." -ForegroundColor Yellow
            
            if (Test-Path $wechatQR) {
                $wechatInfo = Get-Item $wechatQR
                $wechatKB = [math]::Round($wechatInfo.Length/1KB, 2)
                Write-Host "✅ WeChat Payment QR:" -ForegroundColor Green
                Write-Host "   File Size: $wechatKB KB" -ForegroundColor White
                Write-Host "   Modified: $($wechatInfo.LastWriteTime)" -ForegroundColor White
            } else {
                Write-Host "❌ WeChat payment QR code file not found" -ForegroundColor Red
            }
            
            if (Test-Path $alipayQR) {
                $alipayInfo = Get-Item $alipayQR
                $alipayKB = [math]::Round($alipayInfo.Length/1KB, 2)
                Write-Host "✅ Alipay QR:" -ForegroundColor Green
                Write-Host "   File Size: $alipayKB KB" -ForegroundColor White
                Write-Host "   Modified: $($alipayInfo.LastWriteTime)" -ForegroundColor White
            } else {
                Write-Host "❌ Alipay QR code file not found" -ForegroundColor Red
            }
        }
        
        "3" {
            Write-Host "🚀 Preparing to upload to GitHub..." -ForegroundColor Yellow
            
            # Check if there are files to upload
            $hasFiles = (Test-Path $wechatQR) -or (Test-Path $alipayQR)
            
            if (-not $hasFiles) {
                Write-Host "❌ No payment QR code files found, cannot upload" -ForegroundColor Red
                continue
            }
            
            try {
                Write-Host "📁 Adding files to Git..." -ForegroundColor Yellow
                git add images/
                
                Write-Host "💾 Committing changes..." -ForegroundColor Yellow
                git commit -m "📱 Update Payment QR Codes

✨ Updates:
- Update WeChat payment QR code
- Update Alipay payment QR code
- Enhance sponsorship support

🎯 User Experience:
- Users can directly scan to support development
- Complete sponsorship reward system"
                
                Write-Host "🌐 Pushing to GitHub..." -ForegroundColor Yellow
                git push origin main
                
                Write-Host "✅ Payment QR codes uploaded successfully!" -ForegroundColor Green
                Write-Host "🌟 Users can now scan to support your development!" -ForegroundColor Green
                
            } catch {
                Write-Host "❌ Upload failed: $($_.Exception.Message)" -ForegroundColor Red
            }
        }
        
        "4" {
            Write-Host "`n📖 Payment QR Code Setup Instructions:" -ForegroundColor Cyan
            Write-Host "================================" -ForegroundColor Cyan
            Write-Host "1. Prepare your payment QR code images" -ForegroundColor White
            Write-Host "   - WeChat: WeChat APP → Pay & Receive → QR Code → Save" -ForegroundColor Gray
            Write-Host "   - Alipay: Alipay APP → Money → Save Image" -ForegroundColor Gray
            Write-Host ""
            Write-Host "2. Rename files:" -ForegroundColor White  
            Write-Host "   - WeChat payment QR → wechat_qr_3.png" -ForegroundColor Gray
            Write-Host "   - Alipay QR → alipay_qr_3.png" -ForegroundColor Gray
            Write-Host ""
            Write-Host "3. Place files in images directory" -ForegroundColor White
            Write-Host "4. Run this script and select option 3 to upload" -ForegroundColor White
            Write-Host ""
            Write-Host "💡 Recommended image size: 300x300 pixels, PNG format" -ForegroundColor Yellow
        }
        
        "5" {
            Write-Host "👋 Thank you for using the payment QR code update script!" -ForegroundColor Green
            break
        }
        
        default {
            Write-Host "❌ Invalid selection, please enter 1-5" -ForegroundColor Red
        }
    }
} while ($choice -ne "5")

Write-Host "`n🎉 Script execution completed!" -ForegroundColor Green
Write-Host "💰 Once setup is complete, users can scan codes on your GitHub repo page to support you!" -ForegroundColor Yellow