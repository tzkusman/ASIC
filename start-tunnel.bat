@echo off
REM Create ngrok tunnel to expose backend to internet
REM This will generate a public URL that Vercel can access

echo ========================================
echo CryptoMinerPro - Create Public Tunnel
echo ========================================
echo.
echo This will expose your local backend to the internet via ngrok
echo.

REM Check if ngrok is installed
where ngrok >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Installing ngrok...
    powershell -Command "& { [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile $env:TEMP'\ngrok.zip'; Expand-Archive -Path $env:TEMP'\ngrok.zip' -DestinationPath $env:TEMP -Force; Move-Item $env:TEMP'\ngrok.exe' 'C:\Windows\System32\ngrok.exe' -Force; }"
)

echo.
echo Starting ngrok tunnel on port 5000...
echo.
ngrok http 5000

REM The URL will be displayed - copy it and use in Vercel
