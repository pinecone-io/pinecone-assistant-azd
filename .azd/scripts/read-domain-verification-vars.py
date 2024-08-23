import os
import platform
import subprocess

def run_scripts():
    current_os = platform.system()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if current_os == "Windows":
        # Run PowerShell script on Windows
        script_path = os.path.join(script_dir, "read-domain-verification-vars.ps1")
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", script_path], check=True)
    else:
        # Run shell script on POSIX systems
        script_path = os.path.join(script_dir, "read-domain-verification-vars.sh")
        subprocess.run(["bash", script_path], check=True)

if __name__ == "__main__":
    run_scripts()
