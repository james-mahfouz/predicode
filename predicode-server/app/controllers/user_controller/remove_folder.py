import os
import shutil


def remove_folders(extracted_files):
    removed_folders = []
    for extracted_file in extracted_files:
        if not str(extracted_file).split("/")[0] + "/" in removed_folders:
            if os.path.exists(extracted_file):
                if os.path.isdir(extracted_file):
                    shutil.rmtree(extracted_file)
                else:
                    os.remove(extracted_file)

            removed_folders.append(str(extracted_file))
