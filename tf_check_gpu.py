#!/usr/bin/env python

"""Is a GPU available for TensorFlow to use?

Taken from the answers to https://stackoverflow.com/q/38009682/.
"""

import tensorflow as tf

assert tf.test.is_gpu_available()

with tf.device("/gpu:0"):
    a = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[2, 3], name="a")
    b = tf.constant([1.0, 2.0, 3.0, 4.0, 5.0, 6.0], shape=[3, 2], name="b")
    c = tf.matmul(a, b)

# This doesn't work on TF 2.0
# with tf.Session() as sess:
#     print(sess.run(c))
