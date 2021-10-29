import os
import subprocess
import sys

success = False

print("Testing interpret \"Hello World\" script...")

cmd = ["python3", "../J.py", "-i", "interpret - \"Hello World!\" script/script.J"]
env = {}
env.update(os.environ)
print(env)
try:
    print(f"Running system command \"{cmd}\"")
    subprocess.run(cmd, check=True, env=env)
    sys.stdout.flush()

    success = True
    print("\033[92mSuccess!\033[0m")

finally:
    if not success:
        print("\033[91mFailed\033[0m")
    print("Finished!")
