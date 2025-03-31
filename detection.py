import copy
import itertools
from collections import Counter, deque
from typing import Optional
import mediapipe as mp
import numpy as np

from classifier import Classifier
from const import Gesture, MOUTH_LANDMARKS, Face


class Detection:
    def __init__(self, classifier_model: str,classifier_scaler: str):
        self.classifier = Classifier(classifier_model, classifier_scaler)

    @staticmethod
    def pre_process_landmark(landmarks: list[list[int]]) -> list[float]:
        if landmarks:
            temp_landmark_list = copy.deepcopy(landmarks)

            base_x, base_y, base_z = 0, 0, 0
            for index, landmark_point in enumerate(temp_landmark_list):
                if index == 0:
                    base_x, base_y, base_z = landmark_point[0], landmark_point[1], landmark_point[2]

                temp_landmark_list[index][0] = temp_landmark_list[index][0] - base_x
                temp_landmark_list[index][1] = temp_landmark_list[index][1] - base_y
                temp_landmark_list[index][2] = temp_landmark_list[index][2] - base_z

            temp_landmark_list = list(
                itertools.chain.from_iterable(temp_landmark_list))

            max_value = max(list(map(abs, temp_landmark_list)))

            def normalize_(n):
                return n / max_value

            temp_landmark_list_normalized = list(map(normalize_, temp_landmark_list))
            return temp_landmark_list_normalized

        return []

    @staticmethod
    def calculate_landmark_list(image: np.array, landmarks, filter_list: list[int] = None) ->  list[list[int]]:
        image_height, image_width = image.shape[:2]
        landmark_list = []

        for i, landmark in enumerate(landmarks.landmark):
            if filter_list is None or i in filter_list:
                landmark_x = min(int(landmark.x * image_width), image_width - 1)
                landmark_y = min(int(landmark.y * image_height), image_height - 1)
                landmark_z = landmark.z

                landmark_list.append([landmark_x, landmark_y, landmark_z])

        return landmark_list

class HandDetection(Detection):
    def __init__(self, gesture_classifier_model: str, gesture_classifier_scaler: str):
        super().__init__(gesture_classifier_model, gesture_classifier_scaler)
        mp_hands = mp.solutions.hands
        self.model = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.5,
                                    min_tracking_confidence=0.5, model_complexity=0)

    def detect(self, image: np.ndarray) -> list[list[int]]:
        results = self.model.process(image)
        if not results.multi_hand_landmarks:
            return []

        return self.calculate_landmark_list(image, results.multi_hand_landmarks[0])

    def define_gesture(self, normalized_landmarks: list[float]) -> Optional[Gesture]:
        if not normalized_landmarks:
            return None
        return Gesture(self.classifier(normalized_landmarks))

class FaceDetection(Detection):
    def __init__(self, face_classifier_model: str, face_classifier_scaler: str):
        super().__init__(face_classifier_model, face_classifier_scaler)
        mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.history = deque(maxlen=25)

    def detect(self, image: np.ndarray) -> list[list[int]]:
        results = self.face_mesh.process(image)
        if not results.multi_face_landmarks:
            return []

        return self.calculate_landmark_list(
            image,
            results.multi_face_landmarks[0],
            MOUTH_LANDMARKS
        )

    def define_face_expression(self, normalized_landmarks: list[float]) -> bool:
        if not normalized_landmarks:
            return False

        expression = self.classifier(normalized_landmarks)
        self.history.append(Face(expression[0]))

        if len(self.history) == self.history.maxlen:
            (most_common, _), *_ = Counter(self.history).most_common(1)
            if most_common == Face.BLOW:
                self.history.clear()
                return True
        return False




