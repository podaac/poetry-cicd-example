"""
================
plotter.py
================

Example module that produces a plot using matplotlib.

Courtesy of https://www.edureka.co/blog/python-projects/#graphs
"""
import logging

import matplotlib.figure
import matplotlib.pyplot as plt
import numpy as np

__all__ = ["plot", "main"]


def plot() -> matplotlib.figure.Figure:
    """
    Generate a random 3D plot.

    Returns
    -------

    matplotlib.figure.Figure
        Figure containing the random 3D plot

    """
    plot_figure = plt.figure()

    def generate_sin(x_values, y_values):
        return np.sin(np.sqrt(x_values ** 2 + y_values ** 2))

    theta = 2 * np.pi * np.random.random(1000)
    r_num = 6 * np.random.random(1000)
    x_data = np.ravel(r_num * np.sin(theta))
    y_data = np.ravel(r_num * np.cos(theta))
    z_data = generate_sin(x_data, y_data)
    axis_space = plt.axes(projection='3d')
    axis_space.plot_trisurf(x_data, y_data, z_data, cmap='viridis', edgecolor='none')

    return plot_figure


def configure_logging() -> None:
    """
    Sets up basic python logging

    Returns
    -------

    """
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s")


def main() -> None:
    """
    Main entry point for the application.

    Returns
    -------

    """
    configure_logging()
    plot()
    plt.show()


if __name__ == '__main__':
    main()
