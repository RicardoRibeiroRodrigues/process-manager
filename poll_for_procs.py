import time
import os
import shutil
import psutil
import datetime
from send_mail import send_email
from dotenv import load_dotenv

PROC_LIST_FILE = 'processes.txt'
N_MINUTES_TO_POLL = 2


def poll_processes():
    while True:
        procs_to_remove = []
        for index, proc in enumerate(get_processes()):
            pid, full_path = proc.split(' ')
            pid = int(pid)
            if not psutil.pid_exists(pid):
                procs_to_remove.append(index)
                print(f"Process {full_path} with PID {pid} has finished")
                get_data_and_send(full_path, pid)
                
        time.sleep(N_MINUTES_TO_POLL * 60)

def get_processes() -> list[str]:
    with open(PROC_LIST_FILE, 'r') as file:
        return file.read().splitlines()
    
def get_data_and_send(full_path, pid):
    process_name = full_path.split('/')[-1]
    # Put the date in title with format day/month/year - hour:minute
    now = datetime.datetime.now()
    title = f"Training with {process_name} has finished ({now.strftime('%d/%m/%Y - %H:%M')})"
    body = f"Process with PID {pid} has finished. The results are attached."
    # if full_path is a directory, zip it
    if os.path.isdir(full_path):
        res_name = f"{process_name}.zip"
        # zip_file(res_name, full_path)
        shutil.make_archive(res_name, 'zip', full_path)
        path_zip = send_email(title, body, res_name, res_name)
    else:
        print("Not a directory, cant zip it")
        return
    with open(path_zip, 'rb') as file:
        content = file.read()
        send_email(title, body, content, res_name)

def zip_file(res_name, path):
    zf = zipfile.ZipFile(res_name, "w")
    for dirname, _, files in os.walk(path):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()
    # Return full path of the zip file
    return os.path.abspath(res_name)


if __name__ == '__main__':
    load_dotenv()
    poll_processes()