@echo off
echo ========================================
echo    KeySculptAI - Interfaz Web
echo ========================================
echo.
echo Iniciando servidor backend...
echo.

cd web-interface
python server.py

echo.
echo Servidor iniciado en: http://localhost:5000
echo Presiona Ctrl+C para detener el servidor
pause 