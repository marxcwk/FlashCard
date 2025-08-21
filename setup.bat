@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

echo Setup complete! To run the app:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the app: python app.py
echo 3. Open browser to: http://localhost:5000

pause
