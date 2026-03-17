from .normalizer import Normalizer
import numpy as np

class MinMaxNormalizer(Normalizer):
    def normalize(self, x: np.ndarray) -> np.ndarray:
        min_val = x.min(axis=0)
        max_val = x.max(axis=0)
        
        denom = max_val - min_val
        denom[denom == 0] = 1.0 

        return (x - min_val) / denom
    
class VectorNormalizer(Normalizer):
    def normalize(self, x: np.ndarray) -> np.ndarray:
        norm = np.sqrt(np.sum(x**2, axis=0))
        norm[norm == 0] = 1.0
        return x / norm
    
class SumNormalizer(Normalizer):
    def normalize(self, x: np.ndarray) -> np.ndarray:
        col_sum = np.sum(x, axis=0)
        col_sum[col_sum == 0] = 1.0
        return x / col_sum