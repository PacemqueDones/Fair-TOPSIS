from abc import ABC, abstractmethod
import numpy as np

class Metric(ABC):
    @abstractmethod
    def calculate(self, x: np.ndarray, y: np.ndarray) -> float:
        pass