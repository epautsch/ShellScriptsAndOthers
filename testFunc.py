import os
import shutil
import stat
import subprocess

folder_path = 'C:/SSL/ShellScriptsAndOthers/tmep_hold_dir/onnxmodelzoo'

os.chmod(folder_path, stat.S_IWUSR)
shutil.rmtree(folder_path)