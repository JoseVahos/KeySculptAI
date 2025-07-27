Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    KeySculptAI - Interfaz Web" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Iniciando servidor backend..." -ForegroundColor Yellow
Write-Host ""

Set-Location "web-interface"
python server.py

Write-Host ""
Write-Host "Servidor iniciado en: http://localhost:5000" -ForegroundColor Green
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Yellow
Read-Host "Presiona Enter para continuar" 