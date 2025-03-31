import joblib


class Classifier:
    def __init__(self, model_path: str, scaler_path: str):
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def __call__(self, landmark_list: list[float]) -> int | None:
        if landmark_list:
            data_scaled = self.scaler.transform([landmark_list])
            prediction_id = self.model.predict(data_scaled)
            return prediction_id

        return None