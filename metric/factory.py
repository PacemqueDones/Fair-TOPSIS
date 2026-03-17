from .metrics import *

def get_metric(metric: str):
    if metric == 'euclidian':
        return Euclidiana()
    else:
        raise ValueError(f'Metric {metric} not supported.')