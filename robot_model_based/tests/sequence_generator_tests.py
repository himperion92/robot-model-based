import unittest
import logging
import mock
import itertools

from robot_model_based.sequence_generator import SequenceGenerator


class SequenceGeneratorTest(unittest.TestCase):
    """
    Unit Tests for SequenceGenerator class.
    """
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self._seq_gen = SequenceGenerator()
        self.dummy_file_path = '/home/bob/workspace/graph.grahpml'
        self.dummy_nodes = {'n0': {'x': '0', 'y':'1', 'label':'state_a'}, 
                       'n1': {'x': '2', 'y':'3', 'label':'state_b'},
                       'n2': {'x': '4', 'y':'5', 'label':'state_c'},
                       'n3': {'x': '6', 'y':'7', 'label':'state_d'}}
        self.dummy_edges = [('n0', 'n1', {'label':'action_1', 'id':'e1'}),
                       ('n1', 'n0', {'label':'action_2', 'id':'e2'}),
                       ('n1', 'n2', {'label':'action_3', 'id':'e3'}),
                       ('n1', 'n3', {'label':'action_4', 'id':'e4'})] 

    @mock.patch('networkx.readwrite.graphml.read_graphml')
    @mock.patch('networkx.all_simple_paths')
    def test_generate_sequences_full(self, mock_simple_paths, mock_read_graphml):
        expected_exec_seq = [['n0', 'n1', 'n0'],
                             ['n0','n1','n2'],
                             ['n0','n1','n3']]
        decoded_graph = mock.Mock()
        decoded_graph.nodes.return_value = self.dummy_nodes
        decoded_graph.edges.return_value = self.dummy_edges
        mock_read_graphml.side_effect = [decoded_graph]
        mock_simple_paths.side_effect = [[],[['n0', 'n1']], [], [['n0', 'n1']],
                                         [['n0', 'n1', 'n2']],
                                         [['n0', 'n1', 'n3']]]
        nodes, edges, exec_seqs = self._seq_gen.generate_sequences(self.dummy_file_path,
                                                                   'full')
        mock_read_graphml.assert_called_once_with(self.dummy_file_path)
        self.assertEqual(self.dummy_nodes, nodes)
        self.assertEqual(self.dummy_edges, edges)
        self.assertEqual(expected_exec_seq, exec_seqs)

    @mock.patch('networkx.number_of_nodes')
    @mock.patch('networkx.readwrite.graphml.read_graphml')
    @mock.patch('robot_model_based.sequence_generator.SequenceGenerator.'
                '_generate_full_sequence')
    def test_generate_sequences_coverage_low(self, mock_gen_seq,
                                         mock_read_graphml,
                                         mock_num_of_nodes):
        expected_exec_seq = [['n0', 'n1', 'n3']]
        mock_num_of_nodes.side_effect = [len(self.dummy_nodes)]
        decoded_graph = mock.Mock()
        decoded_graph.nodes.return_value = self.dummy_nodes
        decoded_graph.edges.return_value = self.dummy_edges
        mock_read_graphml.side_effect = [decoded_graph]
        mock_gen_seq.side_effect = [[['n0', 'n1', 'n0'],
                                     ['n0','n1','n2'],
                                     ['n0','n1','n3']]]
        nodes, edges, exec_seqs = self._seq_gen.generate_sequences(self.dummy_file_path,
                                                                   'random',
                                                                   coverage=1)
        mock_read_graphml.assert_called_once_with(self.dummy_file_path)
        mock_gen_seq.assert_called_once_with(decoded_graph)
        self.assertEqual(self.dummy_nodes, nodes)
        self.assertEqual(self.dummy_edges, edges)
        self.assertEqual(expected_exec_seq, exec_seqs)

    @mock.patch('networkx.number_of_nodes')
    @mock.patch('networkx.readwrite.graphml.read_graphml')
    @mock.patch('robot_model_based.sequence_generator.SequenceGenerator.'
                '_generate_full_sequence')
    def test_generate_sequences_coverage_high(self, mock_gen_seq,
                                         mock_read_graphml,
                                         mock_num_of_nodes):
        expected_exec_seq = [['n0', 'n1', 'n0'],
                             ['n0', 'n1', 'n2']]
        mock_num_of_nodes.side_effect = [len(self.dummy_nodes)]
        decoded_graph = mock.Mock()
        decoded_graph.nodes.return_value = self.dummy_nodes
        decoded_graph.edges.return_value = self.dummy_edges
        mock_read_graphml.side_effect = [decoded_graph]
        mock_gen_seq.side_effect = [[['n0', 'n1', 'n0'],
                                     ['n0','n1','n2'],
                                     ['n0','n1','n3']]]
        nodes, edges, exec_seqs = self._seq_gen.generate_sequences(self.dummy_file_path,
                                                                   'random',
                                                                   coverage=100)
        mock_read_graphml.assert_called_once_with(self.dummy_file_path)
        mock_gen_seq.assert_called_once_with(decoded_graph)
        self.assertEqual(self.dummy_nodes, nodes)
        self.assertEqual(self.dummy_edges, edges)
        self.assertEqual(expected_exec_seq, exec_seqs)

    @mock.patch('networkx.readwrite.graphml.read_graphml')
    @mock.patch('robot_model_based.sequence_generator.SequenceGenerator.'
                '_generate_full_sequence')
    def test_generate_sequences_wrong_strategy(self, mock_gen_seq,
                                               mock_decode_graph):
        decoded_graph = mock.Mock()
        decoded_graph.node = {'node_a': 'a', 'node_b': 'b'}
        decoded_graph.edge = {'edge_a': 'a', 'edge_b': 'b'}
        mock_decode_graph.side_effect = [decoded_graph]
        mock_gen_seq.side_effect = [['1', '2', '3']]
        with self.assertRaises(ValueError) as err:
            self._seq_gen.generate_sequences(self.dummy_file_path,
                                             'rando', coverage=45)
        self.assertEqual('Selected strategy is not available!',
                         str(err.exception))

        mock_decode_graph.assert_not_called()
        mock_gen_seq.assert_not_called()
