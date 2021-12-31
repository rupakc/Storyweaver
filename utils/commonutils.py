import hashlib
import shutil
import requests
import os
from config import constants


def get_sha_hash(content):
    sha = hashlib.sha1()
    sha.update(content)
    return sha.hexdigest()


def download_image(image_url,filename_to_save):
    response = requests.get(image_url, stream=True)
    with open(filename_to_save, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)


def get_image_hash_list(image_data_directory_path):
    image_list = os.listdir(image_data_directory_path)
    image_name_without_extension_list = list([])
    for image_name in image_list:
        extension_index = image_name.find('.')
        if extension_index != -1:
            image_name_without_extension_list.append(image_name[:extension_index])
    return image_name_without_extension_list


def get_supported_image_hashes(image_hash_name_list):
    hash_title_dict = dict({})
    filtered_image_hash_dict = dict({})

    with open(constants.TITLE_HASH_MAP, 'r') as title_hash_file:
        title_hash_list = title_hash_file.read().split('\n')
    for title_hash in title_hash_list:
        sep_index = title_hash.find('=')
        if sep_index != -1:
            title = title_hash[:sep_index].strip()
            hash_value = title_hash[sep_index+1:].strip()
            hash_title_dict[hash_value] = title
    for image_name in image_hash_name_list:
        if image_name in hash_title_dict.keys():
            filtered_image_hash_dict[image_name] = hash_title_dict[image_name]
    return filtered_image_hash_dict
