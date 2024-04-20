import subprocess

# Path to the MATLAB script
matlab_script = "C:/Users/Akhbar/Downloads/OpenBrain-main/OpenBrain-main/fin.m"

# Construct the command to run the MATLAB script
command = ['matlab', '-batch', 'run(\'{}\')'.format(matlab_script)]

# Run MATLAB script
subprocess.call(command)
