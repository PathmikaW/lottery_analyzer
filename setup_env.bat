@echo off
REM Setup Python Virtual Environment for Lottery Analyzer
REM Windows batch script

echo Creating Python virtual environment...
python -m venv lottery_env

echo.
echo Activating virtual environment...
call lottery_env\Scripts\activate.bat

echo.
echo Installing dependencies from requirements.txt...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ============================================
echo Virtual environment setup complete!
echo ============================================
echo.
echo To activate the environment in the future:
echo   lottery_env\Scripts\activate
echo.
echo To deactivate:
echo   deactivate
echo.
echo To run Jupyter notebooks:
echo   jupyter notebook
echo ============================================
