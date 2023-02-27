import os
import shutil
import stat
import subprocess

folder_path = '/home/epautsch/PTM-Torrent/'

os.chmod(folder_path, stat.S_IWUSR)
shutil.rmtree(folder_path)