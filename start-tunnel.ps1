# CryptoMinerPro - Create Public Tunnel with ngrok
# This exposes your local backend to the internet so Vercel can access it

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "CryptoMinerPro - Create Public Tunnel" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if ngrok exists
$ngrokPath = "C:\Windows\System32\ngrok.exe"
if (-not (Test-Path $ngrokPath)) {
    Write-Host "Installing ngrok..." -ForegroundColor Yellow
    
    $ngrokUrl = "https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip"
    $zipPath = "$env:TEMP\ngrok.zip"
    
    # Download
    [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
    Invoke-WebRequest -Uri $ngrokUrl -OutFile $zipPath -ProgressAction SilentlyContinue
    
    # Extract
    Expand-Archive -Path $zipPath -DestinationPath $env:TEMP -Force
    
    # Move to system path
    Move-Item "$env:TEMP\ngrok.exe" $ngrokPath -Force
    
    Write-Host "✓ ngrok installed successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting ngrok tunnel on port 5000..." -ForegroundColor Yellow
Write-Host "This will create a public URL to access your backend from anywhere" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT:" -ForegroundColor Red
Write-Host "1. Copy the URL shown below (e.g., https://xxxx-xx-xxx-xx.ngrok.io)" -ForegroundColor Red
Write-Host "2. Go to Vercel > Project Settings > Environment Variables" -ForegroundColor Red
Write-Host "3. Set: BACKEND_URL = (the ngrok URL)" -ForegroundColor Red
Write-Host "4. Redeploy Vercel" -ForegroundColor Red
Write-Host ""

# Start tunnel
& $ngrokPath http 5000 --region us
