import os
import platform
import subprocess

def run_scripts():
    current_os = platform.system()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    if current_os == "Windows":
        # Run PowerShell scripts on Windows
        create_env_script = os.path.join(script_dir, "create-env.ps1")
        create_infra_env_vars_script = os.path.join(script_dir, "create-infra-env-vars.ps1")
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", create_env_script], check=True)
        subprocess.run(["powershell", "-ExecutionPolicy", "Bypass", "-File", create_infra_env_vars_script], check=True)
    else:
        # Run shell scripts on POSIX systems
        create_env_script = os.path.join(script_dir, "create-env.sh")
        create_infra_env_vars_script = os.path.join(script_dir, "create-infra-env-vars.sh")
        subprocess.run(["bash", create_env_script], check=True)
        subprocess.run(["bash", create_infra_env_vars_script], check=True)

if __name__ == "__main__":
    run_scripts()