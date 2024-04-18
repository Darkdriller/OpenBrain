import datetime
import shutil


def save_yml(data):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    file_path = '/Users/djs/Documents/Final Year/MRA-FLOW/files/yml_output/network.yaml'
    current_date_file_path = file_path.replace('network.yaml', f'network_{date_str}.yaml')
    shutil.copy(file_path, current_date_file_path)
    print("File saved at: "  + current_date_file_path)
