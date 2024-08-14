# Obsidian Vault Backup Script

This script allows you to automatically backup your Obsidian Vault to a remote location on a weekly basis. It uses the Miniconda environment manager for Windows and the `tqdm` library for progress tracking.

## Prerequisites

- Windows 10 or later
- Miniconda 3

## Installation

1. Install Miniconda 3 by downloading the installer from the [official website](https://docs.conda.io/en/latest/miniconda.html) and following the installation instructions.
2. Open a command prompt and create a new Conda environment named `obsidian_backup` by running the following command:

```
conda create --name obsidian_backup
```

3. Activate the `obsidian_backup` environment by running the following command:

```
conda activate obsidian_backup
```

4. Install the `tqdm` library by running the following command:

```
conda install tqdm
```

5. Clone this repository or download the `vault_backup.py` script to your local machine.
6. Open `vault_backup.py` in a text editor and modify the `main()` function to accept the source and destination directories.

```python
def main():
    source = os.path.expanduser("C:\\Users\\<username>\\Documents\\Obsidian Vault")
    destination = "//<raspberrypi_address>/<username>/Obsidian Vault"
```

7. Create a new batch file named `backup_vault.bat` in the same directory as `vault_backup.py` and paste the following code into it:

```
@echo off
call C:\Users\<username>\miniconda3\Scripts\activate.bat obsidian_backup
python C:\Users\<username>\<path_to_script>\vault_backup.py
pause
```

Replace `<username>` with your Windows username, `<path_to_script>` with the path to the directory containing `vault_backup.py`, `<source_directory>` with the path to your local Obsidian Vault directory, and `<destination_directory>` with the path to the remote backup directory.

8. To make it run automatically, we'll use Windows Task Scheduler
	1. Open the Start menu and search for "Task Scheduler".
	2. In Task Scheduler, click on "Create Basic Task" in the right panel.
	3. Give your task a name, like "Obsidian Vault Backup", and click Next.
	4. Choose how often you want the task to run. Select "Weekly" and click Next.
	5. Choose the day and time you want the backup to occur, then click Next.
	6. For the action, choose "Start a program" and click Next. g. In the "Program/script" field, enter the path to your Batch file.

## Usage

The script will automatically backup your Obsidian Vault to the remote location specified in the `vault_backup.py` script on a weekly basis. The progress of the backup will be displayed in the command prompt using the `tqdm` library.

## Troubleshooting

If you encounter any issues while running the script, please check the following:

- Make sure that the remote location specified in the command-line arguments is accessible and writable.
- Make sure that the `obsidian_backup` environment is activated when running the script.
- Make sure that the `tqdm` library is installed in the `obsidian_backup` environment.

If you are still experiencing issues, please open an issue on the [GitHub repository](https://github.com/itsamanvishwakarma/obsidian-vault-backup) and provide as much detail as possible.

## Contributing

Contributions are welcome! If you have any suggestions or improvements for the script, please open a pull request.
