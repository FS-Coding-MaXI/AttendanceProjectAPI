from insightface.app import FaceAnalysis
import re
import os
import cv2
import pandas as pd
import numpy as np
from sklearn.metrics import pairwise


def prepare_dataframe() -> pd.DataFrame:

    def clean_name(string):
        string = re.sub(r"[^a-zA-Z0-9\s]", " ", string)
        return string.title()

    person_info = []
    for folder_name in os.listdir(path="./images"):
        role, name = folder_name.split("-")
        name = clean_name(name)
        role = clean_name(role)

        # path of each image in respective folder
        img_files = os.listdir(path=f"./images/{folder_name}")
        for file in img_files:
            path = f"./images/{folder_name}/{file}"
            # step-1: read the image
            img_arr = cv2.imread(path)

            # step-2: get the info
            result = faceapp.get(img_arr, max_num=1)  # return list

            if len(result) > 0:
                # step-3: extract facial embedding
                res = result[0]
                embedding = res["embedding"]
                # step-4: save all info name, role, embedding in a list
                person_info.append([name, role, embedding])

    return pd.DataFrame(person_info, columns=["Name", "Role", "Facial_Features"])


faceapp = FaceAnalysis(
    name="buffalo_sc", root="insightface_model", providers=["CPUExecutionProvider"]
)
faceapp.prepare(ctx_id=0, det_size=(640, 640), det_thresh=0.5)

DATAFRAME = prepare_dataframe()


def ml_search_algorithm(
    dataframe, feature_column, test_vector, name_role=["Name", "Role"], thresh=0.5
) -> tuple[str, str]:
    """
    cosine similarity base search algorithm
    """
    # step-1: take the dataframe (collection of data)
    dataframe = dataframe.copy()
    # step-2: Index face embeding from the dataframe and convert into array
    X_list = dataframe[feature_column].tolist()
    x = np.asarray(X_list)

    # step-3: Cal. cosine similarity
    similar = pairwise.cosine_similarity(x, test_vector.reshape(1, -1))
    similar_arr = np.array(similar).flatten()
    dataframe["cosine"] = similar_arr

    # step-4: filter the data
    data_filter = dataframe.query(f"cosine >= {thresh}")
    if len(data_filter) > 0:
        # step-5: get the person name
        data_filter.reset_index(drop=True, inplace=True)
        argmax = data_filter["cosine"].argmax()
        person_name, person_role = data_filter.loc[argmax][name_role]

    else:
        person_name = "Unknown"
        person_role = "Unknown"

    return person_name, person_role


def detect_faces(image):

    results = faceapp.get(image)
    test_copy = image.copy()
    # step-2: use for loop and extract each embedding and pass to ml_search_algorithm
    detected_people = []

    for res in results:
        x1, y1, x2, y2 = res["bbox"].astype(int)
        embeddings = res["embedding"]
        person_name, person_role = ml_search_algorithm(
            DATAFRAME,
            "Facial_Features",
            test_vector=embeddings,
            name_role=["Name", "Role"],
            thresh=0.5,
        )
        if person_name == "Unknown":
            color = (0, 0, 255)  # bgr
        else:
            color = (0, 255, 0)

        cv2.rectangle(test_copy, (x1, y1), (x2, y2), color)

        text_gen = f"{person_role}: {person_name}"
        cv2.putText(
            test_copy, text_gen, (x1, y1), cv2.FONT_HERSHEY_DUPLEX, 0.5, color, 1
        )

        detected_people.append(person_name)

    return (detected_people, test_copy)


# if __name__ == '__main__':
#     img = cv2.imread('./test_images/mo_test2.png')
#     img = cv2.resize(img,(640,640))
#     result = detect_faces(img)
#     cv2.imwrite("output.png",result)
