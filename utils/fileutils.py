import os, shutil


def remove_files_and_folders(folder_path):
    for the_file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def get_list_of_files_in_folder(base_folder_path):
    content_list = os.listdir(base_folder_path)
    detected_object_list = list([])
    for content in content_list:
        full_path = os.path.join(base_folder_path, content)
        if os.path.isdir(full_path):
            for file in os.listdir(full_path):
                detected_object_list.append(content + '/' + file)
    return detected_object_list
