from config import constants
from utils import commonutils, urlutils, parseutils


def save_title_source_map_to_file(filename='title_source_map.txt'):
    url = constants.BASE_URL
    page_num = constants.DEFAULT_PAGE_NUM
    per_page = constants.DEFAULT_PER_PAGE
    while page_num < constants.MAX_PAGE_NUM:
        response = urlutils.get_response(url,{'page': page_num, 'per_page': per_page})
        if response != 'error':
            title_url_dict = parseutils.parse_response_json(response)
            page_num = page_num + 1
            write_dict_to_file(title_url_dict,filename)
        else:
            per_page = per_page-1
        if per_page < 1:
            break


def write_dict_to_file(dict_to_write,filename):
    with open(filename,'a') as map_file:
        for title in dict_to_write.keys():
            try:
                map_file.write(title.strip().replace('\n', '') + '=' + dict_to_write[title])
                map_file.write('\n')
            except Exception:
                pass
        map_file.flush()


def generate_hash_files(title_url_map_filename):
    title_url_dict = dict({})
    title_hash_dict = dict({})
    hash_url_dict = dict({})
    with open(title_url_map_filename,'r') as map_file:
        title_url_map_list = map_file.read().split('\n')
        for title_url in title_url_map_list:
            index_sep = title_url.find('=')
            if index_sep != -1:
                title = title_url[:index_sep].strip()
                url = title_url[index_sep+1:].strip()
                title_url_dict[title] = url
        for title in title_url_dict.keys():
            title_hash = commonutils.get_sha_hash(title.encode('ascii',errors='replace'))
            title_hash_dict[title] = title_hash
            hash_url_dict[title_hash] = title_url_dict[title]
        write_dict_to_file(title_hash_dict,'title_hash_map.txt')
        write_dict_to_file(hash_url_dict, 'hash_url_map.txt')


def download_images_from_url_file(hash_url_filename):
    hash_url_dict = dict({})
    with open(hash_url_filename, 'r') as map_file:
        hash_url_map_list = map_file.read().split('\n')
        for hash_url in hash_url_map_list:
            index_sep = hash_url.find('=')
            if index_sep != -1:
                hash = hash_url[:index_sep].strip()
                url = hash_url[index_sep + 1:].strip()
                hash_url_dict[hash] = url
    for image_url_hash in hash_url_dict.keys():
        image_file_extension = hash_url_dict[image_url_hash].rsplit('?', 1)[0].rsplit('.', 1)[1]
        commonutils.download_image(hash_url_dict[image_url_hash], constants.DATA_FOLDER_PATH + image_url_hash + '.' + image_file_extension)


download_images_from_url_file('hash_url_map.txt')

