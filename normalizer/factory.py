from .normalizers import *

def get_normalizer(name: str) -> Normalizer:
    if name == 'minmax':
        return MinMaxNormalizer()
    elif name == 'vector':
        return VectorNormalizer()
    elif name == 'sum':
        return SumNormalizer()
    else:
        raise ValueError(f'Normalizer {name} not supported.')