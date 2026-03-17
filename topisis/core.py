from metric.factory import get_metric
from normalizer.factory import get_normalizer
import numpy as np

class TOPSIS:
    def __init__(self, metric: str = 'euclidian', normalizer: str = 'vector'):
        self.metric = get_metric(metric)
        self.normalizer = get_normalizer(normalizer)

    def entropy_weight(self, x: np.ndarray):
        x = np.array(x, dtype=float)

        m, n = x.shape
        epsilon = 1e-12

        x_pos = x - np.min(x, axis=0, keepdims=True) + epsilon
        P = x_pos / (np.sum(x_pos, axis=0, keepdims=True) + epsilon)
        E = -np.sum(P * np.log(P + epsilon), axis=0) / np.log(m)

        D = 1 - E
        W = D / (np.sum(D) + epsilon)
        return W
    
    def weight_matrix(self, x: np.ndarray, weights: np.ndarray):
        return x * weights

    def get_ideal_solutions(self, x: np.ndarray, criteria: list[str]):
        ideal_positive = []
        ideal_negative = []

        for j, criterion in enumerate(criteria):
            column = x[:, j]

            if criterion == 'max':
                ideal_positive.append(np.max(column))
                ideal_negative.append(np.min(column))
            elif criterion == 'min':
                ideal_positive.append(np.min(column))
                ideal_negative.append(np.max(column))
            else:
                raise ValueError(f"Critério inválido na coluna {j}: {criterion}")

        return np.array(ideal_positive), np.array(ideal_negative)

    def calculate_distances(self, x, ideal_positive, ideal_negative):
        d_positive = np.array([
            self.metric.calculate(row, ideal_positive) for row in x
        ])
        d_negative = np.array([
            self.metric.calculate(row, ideal_negative) for row in x
        ])
        return d_positive, d_negative

    def calculate_scores(self, d_positive, d_negative):
        eps = 1e-12
        return d_negative / (d_positive + d_negative + eps)

    def fit(self, x: np.ndarray, criteria: list[str], weights: np.ndarray | None = None):
        x = np.array(x, dtype=float)

        if np.any(weights < 0):
            raise ValueError("Os pesos devem ser não negativos.")

        if x.ndim != 2:
            raise ValueError("A matriz x deve ser bidimensional.")

        if len(criteria) != x.shape[1]:
            raise ValueError(
                "O número de critérios deve ser igual ao número de colunas da matriz."
            )
        
        if m <= 1:
            raise ValueError("A matriz deve ter pelo menos duas alternativas para calcular entropia.")

        if weights is None:
            weights = self.entropy_weight(x)
        else:
            weights = np.array(weights, dtype=float)

            if len(weights) != x.shape[1]:
                raise ValueError(
                    "O número de pesos deve ser igual ao número de colunas da matriz."
                )

            weight_sum = np.sum(weights)
            if weight_sum == 0:
                raise ValueError("A soma dos pesos não pode ser zero.")

            weights = weights / weight_sum

        # normalização do TOPSIS
        x_norm = self.normalizer.normalize(x)

        # ponderação
        x_weighted = self.weight_matrix(x_norm, weights)

        # ideais
        ideal_positive, ideal_negative = self.get_ideal_solutions(x_weighted, criteria)

        # distâncias
        d_positive, d_negative = self.calculate_distances(
            x_weighted, ideal_positive, ideal_negative
        )

        # scores
        scores = self.calculate_scores(d_positive, d_negative)
        ranking = np.argsort(scores)[::-1]

        return {
            'weights': weights,
            'normalized_matrix': x_norm,
            'weighted_matrix': x_weighted,
            'ideal_positive': ideal_positive,
            'ideal_negative': ideal_negative,
            'd_positive': d_positive,
            'd_negative': d_negative,
            'scores': scores,
            'ranking': ranking,
            'best_index': ranking[0],
            'best_alternative': x[ranking[0]],
            'best_score': scores[ranking[0]]
        }

    def best(self, x: np.ndarray, criteria: list[str], weights: np.ndarray | None = None):
        result = self.fit(x, criteria, weights)
        return {
            'best_index': result['best_index'],
            'best_alternative': result['best_alternative'],
            'best_score': result['best_score'],
            'weights': result['weights']
        }