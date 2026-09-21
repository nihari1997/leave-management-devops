# Leave Management Application

A deliberately small Flask application used to learn an end-to-end DevOps workflow.

## Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
python app.py
```

Open `http://127.0.0.1:5050` in a browser. Port 5050 avoids a common macOS conflict
with AirPlay Receiver on port 5000.

To choose another port for a run, set `PORT` first. For example in PowerShell:

```powershell
$env:PORT = 8080
python app.py
```

## Run tests

```powershell
pytest
```

The application keeps leave requests in memory, so restarting it clears them. This is intentional for the initial learning stage.
