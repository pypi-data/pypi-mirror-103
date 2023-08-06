import numpy as np


def L2(pred: np.ndarray, gt: np.ndarray) -> float:
    return np.linalg.norm(np.subtract(pred, gt), ord=2)