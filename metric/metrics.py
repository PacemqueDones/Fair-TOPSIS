import numpy as np
from .metric import Metric

class Euclidiana(Metric):
    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        return np.linalg.norm(x - y)