
def parse_response_json(response_json):
    data_list = response_json['data']
    parsed_title_url_map = dict({})
    for data_json in data_list:
        title = data_json['title']
        image_size_list = data_json['imageUrls'][0]['sizes']
        if len(image_size_list) > 1:
            url = image_size_list[1]['url']
        else:
            url = image_size_list[0]['url']
        parsed_title_url_map[title] = url
    return parsed_title_url_map
