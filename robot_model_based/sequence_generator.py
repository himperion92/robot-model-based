import logging
import random

import networkx as nx
import networkx.readwrite


class SequenceGenerator(object):
    _AVAILABLE_WALK_STRATEGIES = ['random', 'full']

    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def generate_sequences(self, file_path, path_strategy, **kwargs):
        """
        Generates all the possible sequences for a graph file given a path
        generation strategy.

        Args:
            file_path (str): path where .graphml file is located.
            path_strategy (str): strategy for path generation. Following values
            are allowed:
                - 'full' for generating every single path combination.
                - 'random' for generating random path combinations.
            coverage (int). This argument is used as the test cases coverage
                in case that 'random' path_strategy is selected.

        Returns:
            (dict): dictionary with nodes information.
            (dict): dictionary with edges information.
            (list): list of lists with information of all sequences.
        """
        path_strategy = path_strategy.lower()
        if path_strategy not in self._AVAILABLE_WALK_STRATEGIES:
            raise ValueError('Selected strategy is not available!')

        graph = self._decode_graph(file_path)
        exec_seqs = []

        if path_strategy == 'random':
            coverage = kwargs['coverage'] if 'coverage' in kwargs else 100
            exec_seqs = self._generate_random_sequence(graph, coverage)

        elif path_strategy == 'full':
            exec_seqs = self._generate_full_sequence(graph)

        return graph.nodes(data=True), graph.edges(data=True), exec_seqs

    def _generate_random_sequence(self, graph, coverage=100):
        """
        Generates a random sequence for a given graph.

        Args:
            graph (NetworkX graph): graph.
            coverage (int): percentage of coverage to cover with generated
                            paths.

        Returns:
            (list): list of generated sequences.
        """
        self._logger.info(
            r"Generating random sequence with {cov}% coverage...".format(
                cov=coverage))
        edges = [edge for edge in graph.edges_iter()]
        nodes = [node for node in graph.node]
        now_coverage = 0
        exec_seqs = []

        while now_coverage < coverage:
            curr_path = []
            node = 'n0'

            while graph.successors(node):

                if len(graph.successors(node)) > 0 and node == 'n0':
                    curr_path.append('n0')
                    node = graph.successors(node)[
                        int(random.uniform(0, len(graph.successors(node))))]
                    curr_path.append(node)

                elif len(graph.successors(node)) > 0 and node != 'n0':
                    prev_node = curr_path[-2]
                    node = graph.successors(node)[
                        int(random.uniform(0, len(graph.successors(node))))]

                    if node == prev_node:
                        break
                    curr_path.append(node)

                elif len(graph.successors(node)) == 0:
                    break

            exec_seqs.append(curr_path)

            if len(exec_seqs) > 1:
                exec_seqs = sorted(exec_seqs)
                exec_seqs = [exec_seqs[i] for i in range(len(exec_seqs)) if
                             i == 0 or exec_seqs[i] != exec_seqs[i - 1]]
                curr_nodes = list(set([
                    item for sub_list in exec_seqs for item in sub_list]))
                now_coverage = float(len(curr_nodes)) / float(len(nodes)) * 100

        self._logger.info("Sequence successfully generated!")
        return exec_seqs

    def _generate_full_sequence(self, graph):
        """
        Generates the full sequence for a given graph.

        Args:
            graph (NetworkX graph): graph object.

        Returns:
            (list): list of generated sequences.
        """
        self._logger.info("Generating full sequence...")
        reverse_paths = []
        exec_seqs = []

        # Get all cyclic sequences
        for edge1 in graph.edges:
            for edge2 in graph.edges:
                if edge1[0] == edge2[1] and edge1[1] == edge2[0]:
                    reverse_paths.append(edge1)

        # Go through cyclic sequences
        for reverse_path in reverse_paths:
            for path in nx.all_simple_paths(graph, 'n0', reverse_path[0]):
                if path[-2] == reverse_path[1]:
                    exec_seqs.append(path + [reverse_path[1]])

        # Search all end paths
        for node in graph.nodes:
            if graph.successors(node):
                for path in nx.all_simple_paths(graph, 'n0', node):
                    exec_seqs.append(path)
        
        # Remove redundant paths
        final_seqs = []
        for seq1 in exec_seqs:
            is_subset = False
            for seq2 in exec_seqs:
                if (len(seq1) < len(seq2)) and seq1 == seq2[:len(seq1)]:
                    is_subset = True
            if not is_subset:
                final_seqs.append(seq1)

        self._logger.info("Sequence successfully generated!")
        return final_seqs

    def _generate_specific_sequence(self, graph):
        # TODO possibility to specify paths
        raise NotImplementedError

    def _decode_graph(self, file_path):
        """
        Decodes given .graphml diagram file

        Args:
            file_path (str): path where .graphml file is located.

        Returns:
            NetworkX graph object.
        """

        self._logger.info("Decoding '{graph}' graph file...".format(
            graph=file_path))
        graph = networkx.readwrite.graphml.read_graphml(file_path)
        self._logger.info("Graph decoded!")
        return graph
