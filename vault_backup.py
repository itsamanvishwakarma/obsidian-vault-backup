import os
import shutil
import time
from tqdm import tqdm

def get_total_size(start_path):
    """Calculate the total size of all files in a directory."""
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    return total_size

def copy_file_with_progress(src, dst, pbar):
    """Copy a file from source to destination with progress bar."""
    file_size = os.path.getsize(src)
    with open(src, 'rb') as fsrc, open(dst, 'wb') as fdst:
        while True:
            buf = fsrc.read(16 * 1024)
            if not buf:
                break
            fdst.write(buf)
            pbar.update(len(buf))
    pbar.update(file_size - pbar.n)  # Update progress bar with remaining file size


def sync_directories(src, dst):
    """Synchronize source and destination directories."""
    total_size = get_total_size(src)

    start_time = time.time()
    with tqdm(total=total_size, unit='B', unit_scale=True, desc="Copying") as pbar:
        for src_dir, _, filenames in os.walk(src):
            dst_dir = src_dir.replace(src, dst)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for filename in filenames:
                src_file = os.path.join(src_dir, filename)
                dst_file = os.path.join(dst_dir, filename)
                if not os.path.exists(dst_file) or os.path.getmtime(src_file) > os.path.getmtime(dst_file):
                    copy_file_with_progress(src_file, dst_file, pbar)
                    pbar.set_postfix({'File': filename})

        # Delete files or directories that are present in the destination but not in the source
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
                        pbar.set_postfix({'Deleting': filename})

    end_time = time.time()
    duration = end_time - start_time
    speed = total_size / duration / (1024 * 1024)  # Speed in MB/s

    print(f"\nCopy completed successfully!")
    print(f"Total time: {duration:.2f} seconds")
    print(f"Average speed: {speed:.2f} MB/s")

def main():
    source = os.path.expanduser("C:\\Users\\<username>\\Documents\\Obsidian Vault")
    destination = "//<raspberrypi_address>/<username>/Obsidian Vault"

    print("Starting copy process...")
    sync_directories(source, destination)

if __name__ == "__main__":
    main()
