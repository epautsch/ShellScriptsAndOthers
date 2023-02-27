import os
import shutil
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from argparse import Namespace

from args import JIT_batch
from batch_json_commits import search_for_git_files, make_commits_json

# Queue to hold the directories to be processed
processing_q = []


def make_dirs(_dir: str):
    if not os.path.exists(_dir):
        os.makedirs(_dir)


def process_tar_gz(q_file_path: str, temp_hold_dir: str, output_dir: str) -> None:
    # extract folder from .tar.gz format
    make_dirs(temp_hold_dir)
    folder_path = temp_hold_dir + '/' + os.path.basename(q_file_path)[:-7]
    make_dirs(folder_path)
    shutil.unpack_archive(q_file_path, folder_path)
    # add line to print file extracted
    print("File extracted: " + folder_path)

    # get directory containing the .git folder
    git_list = search_for_git_files(folder_path)

    print("Creating commits .json files for: " + folder_path)
    # function call to make commits json from the .git folder
    make_dirs(output_dir)
    output_dir += '/' + os.path.basename(folder_path)
    make_dirs(output_dir)
    make_commits_json(git_list, output_dir)

    # delete original .tar.gz file
    os.remove(q_file_path)
    print("Compressed file deleted: " + q_file_path)

    shutil.rmtree(folder_path, ignore_errors=True)

    return


# function to listen for new files in the directory
class PTMLargeTransferHandler(FileSystemEventHandler):
    # on_created is called whenever a '.tar.gz' file is transferred to the directory
    def on_created(self, event: FileSystemEventHandler) -> None:
        # check if the file is a .tar.gz file and add to clime-git-commits-extract queue
        if event.src_path[-7:] == '.tar.gz':
            print("File found: " + event.src_path)
            processing_q.append(event.src_path)


def main(args=JIT_batch()):
    args: Namespace = args

    event_handler = PTMLargeTransferHandler()
    observer = Observer()
    observer.schedule(event_handler, path=args.incoming, recursive=False)
    observer.start()

    process_single = args.process_single

    # process dirs in the queue
    try:
        while True:
            if processing_q:
                q_file_path = processing_q.pop(0)
                process_tar_gz(q_file_path, args.output_unzip, args.output_json)
                if process_single:
                    return
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()


if __name__ == '__main__':
    main()
