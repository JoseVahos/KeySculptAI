# Configuración de Node.js para KeySculptAI

## Instalación de Node.js

### Opción 1: Instalador Oficial
1. Ve a [nodejs.org](https://nodejs.org/)
2. Descarga la versión LTS (Long Term Support)
3. Ejecuta el instalador y sigue las instrucciones
4. Reinicia tu terminal/PowerShell

### Opción 2: Chocolatey (Windows)
```powershell
choco install nodejs
```

### Opción 3: Scoop (Windows)
```powershell
scoop install nodejs
```

## Verificación de la Instalación

Después de instalar Node.js, verifica que esté funcionando:

```bash
node --version
npm --version
```

## Configuración del PATH

Si Node.js no se reconoce después de la instalación:

### Windows
1. Busca "Variables de entorno" en el menú de inicio
2. Haz clic en "Variables de entorno..."
3. En "Variables del sistema", busca "Path"
4. Haz clic en "Editar"
5. Agrega las siguientes rutas (ajusta según tu instalación):
   ```
   C:\Program Files\nodejs\
   %AppData%\npm
   ```
6. Haz clic en "Aceptar" en todas las ventanas
7. Reinicia tu terminal

### Verificación del PATH
```bash
echo $env:PATH
```

## Instalación de Dependencias

Una vez que Node.js esté configurado:

```bash
cd web-interface
npm install
```

## Desarrollo con React

### Iniciar servidor de desarrollo
```bash
npm start
```

### Construir para producción
```bash
npm run build
```

## Solución de Problemas

### Error: "npm no se reconoce"
- Verifica que Node.js esté instalado correctamente
- Reinicia tu terminal después de la instalación
- Verifica que el PATH incluya la ruta de Node.js

### Error: "EACCES: permission denied"
- Ejecuta PowerShell como administrador
- O usa `npm install --no-optional`

### Error: "Python no se reconoce"
- Asegúrate de que Python esté instalado y en el PATH
- Verifica con `python --version`

## Alternativa: Usar la Versión Simplificada

Si tienes problemas con Node.js, puedes usar la versión simplificada que ya está funcionando:

1. Inicia el servidor backend:
   ```bash
   cd web-interface
   python server.py
   ```

2. Abre http://localhost:5000 en tu navegador

Esta versión funciona perfectamente sin Node.js y tiene todas las funcionalidades principales. 