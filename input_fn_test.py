# Author: caixuanting@gmail.com

import tensorflow as tf
import unittest as ut

from input_fn import _parse_serialized_example
from input_fn import input_fn
from generate_example import generate_sequence_example
from constant import *

class TestInputFnMethods(ut.TestCase):
    def test_parse_serialized_example(self):
        sequence_example = generate_sequence_example(
            [[0, 0], [1, 1]], [0, 1])

        parsed_context, parsed_feature = _parse_serialized_example(
            sequence_example.SerializeToString(), 2)

        session = tf.Session()

        parsed_context_output = session.run(parsed_context)
        parsed_feature_output = session.run(parsed_feature)

        sequence_length = parsed_context_output[SEQUENCE_LENGTH]
        self.assertEqual(2, sequence_length)

        label = list(session.run(
            tf.sparse_tensor_to_dense(
                parsed_context_output[LABEL])))
        
        self.assertListEqual([0, 1], label)
        self.assertListEqual([0, 0],
                             list(parsed_feature_output[FEATURE][0]))
        self.assertListEqual([1, 1],
                             list(parsed_feature_output[FEATURE][1]))


    def test_input_fn(self):
        features, labels = input_fn(['test_data/sequence_examples.tfrecord'],
                                    2, # num_features
                                    1, # buffer_size
                                    1, # batch_size
                                    1, # num_epochs
        )

        session = tf.Session()
        
        features_output = session.run(features)
        labels_output = session.run(labels)
        
        self.assertListEqual([4], list(features_output[SEQUENCE_LENGTH]))
        self.assertListEqual([0, 0], list(features_output[FEATURE][0][0]))
        self.assertListEqual([0, 0], list(features_output[FEATURE][0][1]))
        self.assertListEqual([1, 1], list(features_output[FEATURE][0][2]))
        self.assertListEqual([1, 1], list(features_output[FEATURE][0][3]))

        labels = session.run(
            tf.sparse_tensor_to_dense(labels_output))

        self.assertListEqual([0, 1], list(labels[0]))

        
if __name__ == '__main__':
    ut.main()
