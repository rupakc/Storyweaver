from utils import exportutils
from config import constants
import numpy as np


def get_average_word_vector(sentence, magnitude_vectors):
    sentence_list = sentence.split(' ')
    composite_vector = [0.0 for _ in range(300)]
    for word in sentence_list:
        word_vector = magnitude_vectors.query(word)
        composite_vector = (np.array(word_vector) + np.array(composite_vector))/2.0
    return composite_vector


def get_image_hash_names(sentence,magnitude_vector_model,index_hash_map=constants.INDEX_HASH_MAP, nearest_neighbor_model=constants.NEAREST_NEIGHBOR_MODEL, top_n=6):
    nearest_neighbor_model = exportutils.load_model(nearest_neighbor_model)
    index_hash_map = exportutils.load_model(index_hash_map)
    word_vec = get_average_word_vector(sentence, magnitude_vector_model)
    _, nearest_index = nearest_neighbor_model.kneighbors(word_vec.reshape(1, -1), n_neighbors=top_n)
    match_index_list = nearest_index[0]
    image_hash_list = list([])
    for match_index in match_index_list:
        image_hash_list.append(index_hash_map[match_index])
    return augment_image_path(image_hash_list)


def augment_image_path(image_hash_list):
    augmented_path_list = list([])
    for image_hash_name in image_hash_list:
        augmented_path_list.append(constants.IMAGE_PATH_PREFIX + image_hash_name + constants.IMAGE_EXTENSION)
    return augmented_path_list
