"""
==============
test_plotter.py
==============

Test the plotter functionality.
"""
import numpy
import plotter
from matplotlib.testing.decorators import image_comparison


@image_comparison(baseline_images=['plotter'], extensions=['png'])
def test_plotter_main():
    numpy.random.seed(0)
    fig = plotter.plot()

    assert fig is not None
