# goodman_plot.py

import matplotlib.pyplot as plt
import numpy as np

def create_goodman_plot(sigma_m=None, sigma_a=None, Se=200, UTS=400, n=1):
    # Default fallback values
    sigma_m = sigma_m if sigma_m is not None else 50
    sigma_a = sigma_a if sigma_a is not None else 75

    # Create plot
    fig, ax = plt.subplots()
    x_vals = np.array([0, UTS])
    y_vals = Se * (1 - x_vals / UTS)
    ax.plot(x_vals, y_vals, color='red', label='Goodman Line')

    # Operating point
    ax.scatter(sigma_m, sigma_a, color='blue', label='Operating Point')

    # Safety factor line
    safe_line_y = Se * (1 - x_vals / (n * UTS))
    ax.plot(x_vals, safe_line_y, color='green', linestyle='--', label=f'SF={n} Line')

    ax.set_xlabel('Mean Stress, σm (MPa)')
    ax.set_ylabel('Alternating Stress, σa (MPa)')
    ax.set_title('Goodman Diagram')
    ax.set_xlim(0, UTS * 1.1)
    ax.set_ylim(0, Se * 1.5)
    ax.grid(True)
    ax.legend()

    return fig
