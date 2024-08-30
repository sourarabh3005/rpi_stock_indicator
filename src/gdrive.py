import subprocess
from gdrive_env import REMOTE_NAME
from gdrive_env import GDRIVE_SYNC_PATH
# Config the rclone with gdrive locally
# if gdrive_env is not present, create a gdrive_env.py
# REMOTE_NAME = <gdrive rclone remote name>
# For security reason the gdrive_env.py is not committed in github

class RCloneDrive:
    def __init__(self):
       self.remote_name = REMOTE_NAME

    def list_files(self, remote_path=''):
        """List files in a specific directory in Google Drive."""
        try:
            command = ['rclone', 'lsf', self.remote_name]
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            files = result.stdout.strip().split('\n')
            print("Files in the directory:")
            for file in files:
                print(file)
            return files
        except subprocess.CalledProcessError as e:
            print(f"Error listing files: {e}")
            return []

    def sync_file(self, local_path):
        """Sync files from Google Drive."""
        try:
            # TODO: implement to clean the local_path first
            
            command = ['rclone', 'sync', f'{self.remote_name}', local_path ]
            subprocess.run(command, check=True)
            print(f"File downloaded to {local_path}")
        except subprocess.CalledProcessError as e:
            print(f"Error downloading file: {e}")

    def upload_file(self, local_path):
        """Upload a file to Google Drive."""
        try:
            command = ['rclone', 'copy', local_path, f'{self.remote_name}']
            subprocess.run(command, check=True)
            print(f"File uploaded to remote path")
        except subprocess.CalledProcessError as e:
            print(f"Error uploading file: {e}")


def upload_file_to_gdrive(local_file):
    rclone = RCloneDrive()  # Replace with your remote name
    rclone.upload_file(local_file)

def download_file_from_gdrive(dload_path):
    rclone = RCloneDrive()
    rclone.sync_file(dload_path)

