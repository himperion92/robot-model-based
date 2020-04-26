import unittest
import logging
import mock

from robot_model_based.sequence_generator import SequenceGenerator


class SequenceGeneratorTest(unittest.TestCase):
    """
    Unit Tests for SequenceGenerator class.
    """
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self._seq_gen = SequenceGenerator()

    @mock.patch('robot_model_based.sequence_generator.SequenceGenerator.'
                '_decode_graph')
    @mock.patch('robot_model_based.sequence_generator.SequenceGenerator.'
                '_generate_random_sequence')
    def test_generate_sequences_random(self, mock_gen_seq, mock_decode_graph):
        file_path = '/home/bob/workspace/graph.grahpml'
        decoded_graph = mock.Mock()
        decoded_graph.node = {'node_a': 'a', 'node_b': 'b'}
        decoded_graph.edge = {'edge_a': 'a', 'edge_b': 'b'}
        mock_decode_graph.side_effect = [decoded_graph]
        mock_gen_seq.side_effect = [['1', '2', '3']]
        nodes, edges, exec_seqs = self._seq_gen.generate_sequences(file_path,
                                                                   'random',
                                                                   coverage=45)
        self.assertEqual({'node_a': 'a', 'node_b': 'b'}, nodes)
        self.assertEqual({'edge_a': 'a', 'edge_b': 'b'}, edges)
        self.assertEqual(['1', '2', '3'], exec_seqs)
        mock_decode_graph.assert_called_once_with(file_path)
        mock_gen_seq.assert_called_once_with(decoded_graph, 45)

    @mock.patch('robot_model_based.sequence_generator.SequenceGenerator.'
                '_decode_graph')
    @mock.patch('robot_model_based.sequence_generator.SequenceGenerator.'
                '_generate_full_sequence')
    def test_generate_sequences_full(self, mock_gen_seq, mock_decode_graph):
        file_path = '/home/bob/workspace/graph.grahpml'
        decoded_graph = mock.Mock()
        decoded_graph.node = {'node_a': 'a', 'node_b': 'b'}
        decoded_graph.edge = {'edge_a': 'a', 'edge_b': 'b'}
        mock_decode_graph.side_effect = [decoded_graph]
        mock_gen_seq.side_effect = [['1', '2', '3']]
        nodes, edges, exec_seqs = self._seq_gen.generate_sequences(file_path,
                                                                   'full')
        self.assertEqual({'node_a': 'a', 'node_b': 'b'}, nodes)
        self.assertEqual({'edge_a': 'a', 'edge_b': 'b'}, edges)
        self.assertEqual(['1', '2', '3'], exec_seqs)
        mock_decode_graph.assert_called_once_with(file_path)
        mock_gen_seq.assert_called_once_with(decoded_graph)

    @mock.patch('robot_model_based.sequence_generator.SequenceGenerator.'
                '_decode_graph')
    @mock.patch('robot_model_based.sequence_generator.SequenceGenerator.'
                '_generate_random_sequence')
    def test_generate_sequences_wrong_strategy(self, mock_gen_seq,
                                               mock_decode_graph):
        file_path = '/home/bob/workspace/graph.grahpml'
        decoded_graph = mock.Mock()
        decoded_graph.node = {'node_a': 'a', 'node_b': 'b'}
        decoded_graph.edge = {'edge_a': 'a', 'edge_b': 'b'}
        mock_decode_graph.side_effect = [decoded_graph]
        mock_gen_seq.side_effect = [['1', '2', '3']]
        with self.assertRaises(ValueError) as err:
            self._seq_gen.generate_sequences(file_path, 'rando', coverage=45)
        self.assertEqual('Selected strategy is not available!',
                         str(err.exception))

        mock_decode_graph.assert_not_called()
        mock_gen_seq.assert_not_called()

    @mock.patch('networkx.readwrite.graphml.read_graphml')
    def test_decode_graph(self, mock_read_graphml):
        file_path = '/home/bob/workspace/graph.grahpml'
        mock_read_graphml.side_effect = [1]
        graph = self._seq_gen._decode_graph(file_path)
        mock_read_graphml.assert_called_once_with(file_path)
        self.assertEqual(1, graph)
