import face_recognition

from sortedcontainers import SortedDict


def get_face_encodings(image):
    """
    Function for get facial landmarks.
    """
    encoding_list = face_recognition.api.face_encodings(image)
    return encoding_list


def compare_faces(list_of_face_encodings, unknown_face_encodings):
    """
    Function which find 4 person which closest.
    """

    result_list_of_faces = SortedDict()

    for element in list_of_face_encodings:
        # calculate distance from current encodings to unknown encodings
        current_distance = face_recognition.api.face_distance(
            element["face_encoding"], unknown_face_encodings)
        min_dist = current_distance.min()
        # add to our list of top matches faces
        if len(result_list_of_faces) < 3:
            result_list_of_faces.update({min_dist: element})
        else:
            result_list_of_faces.update({min_dist: element})
            result_list_of_faces.popitem()
    if result_list_of_faces.keys()[0] > 0.555:
        result_list_of_faces = None
    return result_list_of_faces


# def compare_faces(list_of_face_encodings, unknown_face_encodings):
#     """
#     Function which find person which closest.
#     """
#
#     min_dist = face_recognition.api.face_distance(list_of_face_encodings[0]["face_encoding"], unknown_face_encodings)
#     closest_person = list_of_face_encodings[0]
#
#     for element in list_of_face_encodings:
#         # calculate distance from current encodings to unknown encodings
#         current_distance = face_recognition.api.face_distance(
#             element["face_encoding"], unknown_face_encodings)
#
#         if current_distance < min_dist:
#             min_dist = current_distance
#             closest_person = element
#
#     return closest_person
