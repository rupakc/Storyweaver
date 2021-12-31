from imageai.Detection import ObjectDetection
from utils import exportutils, fileutils
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
    return image_hash_list


def augment_image_path(image_hash_list):
    augmented_path_list = list([])
    for image_hash_name in image_hash_list:
        augmented_path_list.append(constants.DATA_FOLDER_PATH + image_hash_name + constants.IMAGE_EXTENSION)
    return augmented_path_list


def get_initialized_detector_model(model_path=constants.MODEL_FOLDER_PATH+constants.DETECTOR_MODEL_NAME):
    detector = ObjectDetection()
    detector.setModelTypeAsRetinaNet()
    detector.setModelPath(model_path)
    detector.loadModel()
    return detector


def extract_objects_from_image(detector_model_object, image_list, output_path):
    generated_image_path_list = list([])
    image_full_path_list = augment_image_path(image_list)
    print(image_full_path_list)
    for image_hash_name, image_path_name in zip(image_list,image_full_path_list):
        print(output_path+image_hash_name)

        detections, path = detector_model_object.detectObjectsFromImage(input_image=image_path_name,
                                                               extract_detected_objects=True, output_type='file',
                                                               output_image_path=output_path+image_hash_name, minimum_percentage_probability=30)
        generated_image_path_list.extend(path)
        # except Exception:
        #     pass
    return generated_image_path_list


def object_extraction_pipeline(sentence, magnitude_vector_model, detector_model_object):
    fileutils.remove_files_and_folders(constants.DETECTED_OBJECT_OUTPUT_PATH)
    image_hash_name_list = get_image_hash_names(sentence, magnitude_vector_model)
    extract_objects_from_image(detector_model_object, image_hash_name_list, constants.DETECTED_OBJECT_OUTPUT_PATH)
    file_path_list = fileutils.get_list_of_files_in_folder(constants.DETECTED_OBJECT_OUTPUT_PATH)
    full_file_path_list = list([])
    for file_path in file_path_list:
        full_file_path_list.append(constants.DETECT_OUTPUT_PREFIX + file_path)
    return full_file_path_list
