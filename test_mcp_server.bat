@echo off
echo Testing MCP Filesystem Server for DOCKER_CONSCIOUSNESS_TOOLS
echo ==========================================================
echo.

set SERVER_PATH="C:\Users\Pirate\AppData\Roaming\Claude\Claude Extensions\ant.dir.ant.anthropic.filesystem\server\index.js"
set TARGET_PATH="C:\Users\Pirate\Desktop\DOCKER_CONSCIOUSNESS_TOOLS"

echo Server: %SERVER_PATH%
echo Target: %TARGET_PATH%
echo.

echo Checking if server file exists...
if exist %SERVER_PATH% (
    echo [OK] Server file found
) else (
    echo [ERROR] Server file not found!
    echo The filesystem extension may not be installed properly.
    pause
    exit /b 1
)

echo.
echo Checking if target directory exists...
if exist %TARGET_PATH% (
    echo [OK] Target directory found
) else (
    echo [ERROR] Target directory not found!
    pause
    exit /b 1
)

echo.
echo Testing server startup...
echo.
node %SERVER_PATH% %TARGET_PATH%

pause
