import os
import shutil
import time
from tqdm import tqdm
import sys
from rich.progress import (
    Progress,
    TextColumn,
    BarColumn,
    FileSizeColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)
from rich.console import Console
from rich import print as rprint

def get_total_size(start_path):
    """Calculate the total size of all files in a directory."""
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def copy_file_with_progress(src, dst, progress, task):
    """Copy a file from source to destination with rich progress bar."""
    file_size = os.path.getsize(src)
    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        while True:
            buf = fsrc.read(16 * 1024)
            if not buf:
                break
            fdst.write(buf)
            progress.update(task, advance=len(buf))

def sync_directories(src, dst):
    """Synchronize source and destination directories."""
    total_size = get_total_size(src)
    console = Console()

    with Progress(
        TextColumn("[bold blue]{task.description}", justify="right"),
        BarColumn(bar_width=None),
        "[progress.percentage]{task.percentage:>3.1f}%",
        "•",
        FileSizeColumn(),
        "•",
        TransferSpeedColumn(),
        "•",
        TimeRemainingColumn(),
        console=console,
        expand=True
    ) as progress:
        
        copy_task = progress.add_task("[cyan]Copying files...", total=total_size)
        start_time = time.time()

        # Copying files
        for src_dir, _, filenames in os.walk(src):
            dst_dir = src_dir.replace(src, dst)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for filename in filenames:
                src_file = os.path.join(src_dir, filename)
                dst_file = os.path.join(dst_dir, filename)
                if not os.path.exists(dst_file) or os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                    progress.update(copy_task, description=f"[cyan]Copying {filename}")
                    copy_file_with_progress(src_file, dst_file, progress, copy_task)

        # Cleanup phase
        progress.update(copy_task, description="[yellow]Cleaning up...")
        for dst_dir, _, filenames in os.walk(dst, topdown=False):
            src_dir = dst_dir.replace(dst, src)
            if not os.path.exists(src_dir):
                shutil.rmtree(dst_dir)
            else:
                for filename in filenames:
                    src_file = os.path.join(src_dir, filename)
                    dst_file = os.path.join(dst_dir, filename)
                    if not os.path.exists(src_file):
                        os.remove(dst_file)
                        progress.update(copy_task, description=f"[red]Removing {filename}")

    # Final statistics
    end_time = time.time()
    duration = end_time - start_time
    speed = total_size / duration / (1024 * 1024)  # Speed in MB/s

    console.print("\n[bold green]Copy completed successfully! ✨[/]")
    console.print(f"[blue]Total time:[/] {duration:.2f} seconds")
    console.print(f"[blue]Average speed:[/] {speed:.2f} MB/s")

def main():
    source = os.path.expanduser("C:\\Users\\<username>\\Documents\\Obsidian Vault")
    destination = "//<rpi_address>/<username>/Obsidian Vault"

    print(f"Python version: {sys.version}")
    print(f"Source path: {source}")
    print(f"Destination path: {destination}")
    print("\nStarting copy process...")
    sync_directories(source, destination)

if __name__ == "__main__":
    main()
