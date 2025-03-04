@echo off

REM Check if pip is installed
python -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo pip is not installed. Please install Python and pip first.
    exit /b
)

echo Installing packages from requirements.txt...

REM Install packages from requirements.txt quietly (suppress "Requirement already satisfied" messages)
pip install --upgrade -q -r requirements.txt
if %errorlevel% neq 0 (
    echo Failed to install some packages from requirements.txt.
    exit /b
)

echo All packages installed successfully.

REM Run the Python script (main.py) after installation
echo Running the Python script...
python src\main.py
if %errorlevel% neq 0 (
    echo There was an error running the Python script.
    exit /b
)

echo Python script executed successfully.
