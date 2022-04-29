import platform
import os
import json
import subprocess

LINUX = 'Linux'

CURRENT_PLATFORM = platform.system()
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cifs-auto-mount-config.json')
CONFIG = json.load(open(CONFIG_FILE_PATH))


def mount_network_folder():
    folder_to_mount = CONFIG['FolderToMount']
    mounted_folder = CONFIG['MountedFolder']

    is_unc = folder_to_mount.startswith(r'//') or folder_to_mount.startswith(r'\\')
    if not is_unc:
        return

    mount_result = subprocess.getoutput(
        f'sudo mount.cifs "{folder_to_mount}" "{mounted_folder}" -o user=root,password=guest,dir_mode=0777,file_mode=0777')
    if not mount_result:
        return

    raise Exception(f"Mount error. {mount_result}")


def main():
    if CURRENT_PLATFORM != LINUX:
        raise Exception('Platform is not supported.')
    user = os.getenv("SUDO_USER")
    if user is None:
        user = os.getenv("USER")
    if user is None:
        raise Exception('Current user is None.')
    mount_network_folder()


main()
