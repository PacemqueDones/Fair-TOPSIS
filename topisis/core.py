from metric.factory import get_metric
from normalizer.factory import get_normalizer
import numpy as np

class TOPSIS:
    def __init__(self, metric: str == 'euclidian', normalizer: str == 'vector'):
        self.metric = get_metric(metric)
        self.normalizer = get_normalizer(normalizer)