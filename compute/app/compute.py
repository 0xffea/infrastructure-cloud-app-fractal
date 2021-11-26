# coding: utf-8

# --------------------------------------------------------------------------
# 2021
# --------------------------------------------------------------------------
"""
Classes and functions used in Fractal app.
"""

import io
import logging

import tensorflow as tf
import numpy as np
import PIL


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()


class Fractal:
    def __init__(self, frame, iterations=100, resolution=(7168, 7168)):
        self.resolution = resolution
        self.range_x = (-2.0, 0.5)
        self.range_y = (-1.3, 1.3)
        self.iterations = iterations
        self.frame = frame

    def _meshgrid(self):
        x_res, y_res = self.resolution
        x_min, x_max = self.range_x
        y_min, y_max = self.range_y
        x_min, x_max, y_min, y_max = self.frame
        h_x = (x_max - x_min) / x_res
        h_y = (y_max - y_min) / y_res
        return np.mgrid[y_min:y_max:h_y, x_min:x_max:h_x]

    @staticmethod
    def _export(a, fmt='png'):
        a = np.uint8(a)
        img_byte_arr = io.BytesIO()
        PIL.Image.fromarray(a).save(img_byte_arr, fmt)
        return img_byte_arr.getvalue()

    @staticmethod
    def step(xs_, zs_, ns_):
        zs_ = zs_*zs_ + xs_

        not_diverged = tf.abs(zs_) < 4
        ns_ = tf.add(ns_, tf.cast(not_diverged, tf.float32))

        return xs_, zs_, ns_

    def generate(self):
        Y, X = self._meshgrid()
        Z = X + 1j*Y
        xs = tf.constant(Z.astype(np.complex64))
        zs = tf.zeros_like(xs)
        ns = tf.Variable(tf.zeros_like(xs, tf.float32))
        for _ in range(self.iterations):
            xs, zs, ns = self.step(xs, zs, ns)
        fractal = np.log(np.array(ns))
        fractal = 255 * fractal / fractal.max()

        return self._export(fractal)
