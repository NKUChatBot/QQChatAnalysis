import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde


def plot_density(res):
    """画传入参数的概率密度曲线"""
    density = gaussian_kde(res)
    xs = np.linspace(min(res), max(res), 1000)
    density.covariance_factor = lambda: .25
    density._compute_covariance()
    plt.subplot(211)
    plt.plot(xs, density(xs))
    plt.subplot(212)
    plt.hist(res, bins=100)
    plt.show()
