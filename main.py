from drive_manager import upload_to_folder
import time
import os
import shutil
import psutil
import datetime
from send_mail import send_email
from dotenv import load_dotenv

PROC_LIST_FILE = 'processes.txt'
N_MINUTES_TO_POLL = 5


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
        remove_finished_processes(procs_to_remove)
                
        time.sleep(N_MINUTES_TO_POLL * 60)

def get_processes() -> list[str]:
    with open(PROC_LIST_FILE, 'r') as file:
        return file.read().splitlines()
    
def get_data_and_send(full_path, pid):
    process_name = full_path.split('/')[-1]
    now = datetime.datetime.now()
    title = f"Training with name {process_name} has finished ({now.strftime('%d/%m/%Y - %H:%M')})"

    # if full_path is a directory, zip it
    if os.path.isdir(full_path):
        res_name = f"{process_name}.zip"

        shutil.make_archive(process_name, 'zip', full_path)
        file_name = f"{process_name}_{now.strftime('%d%m%Y%H%M')}.zip"
        upload_to_folder(file_name, res_name)
        body = f"Process with PID {pid} has finished. The results are in the file {file_name}"
        send_email(title, body)
    else:
        print("Not a directory, cant zip it")
        return

def remove_finished_processes(procs_to_remove):
    lines = get_processes()
    with open(PROC_LIST_FILE, 'w') as file:
        for index, line in enumerate(lines):
            if index not in procs_to_remove:
                file.write(line + '\n')

if __name__ == '__main__':
    load_dotenv()
    poll_processes()