import os
import subprocess
import sys

VENV_DIR = "venv"

def create_venv():
    if not os.path.exists(VENV_DIR):
        print("Creating virtual environment...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
    else:
        print("Virtual environment already exists.")

def install_requirements():
    pip_path = os.path.join(VENV_DIR, "Scripts", "pip.exe") if os.name == "nt" else os.path.join(VENV_DIR, "bin", "pip")
    if not os.path.exists("requirements.txt"):
        print("requirements.txt not found.")
        return
    print("Installing dependencies...")
    subprocess.check_call([pip_path, "install", "-r", "requirements.txt"])

def activate_env():
    if os.name == "nt":
        script_path = os.path.join(os.getcwd(), "activate_env.ps1")
        print("Opening a new PowerShell window with the virtual environment activated...")
        subprocess.Popen(["powershell.exe", "-NoExit", "-File", script_path])
    else:
        print("Automatic activation is only supported on Windows with PowerShell.")

if __name__ == "__main__":
    create_venv()
    install_requirements()
    activate_env()
    print("Setup complete.")
