from abc import ABC, abstractmethod
import numpy as np

class Normalizer(ABC):
    @abstractmethod
    def normalize(self, x: np.ndarray) -> np.ndarray:
        pass