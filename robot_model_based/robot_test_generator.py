import logging

import robot.api


class RobotTestGenerator(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self.test_suite = None
    
    def create_test_suite(self, name, nodes, edges, exec_seqs, imports=None):
        """
        Creates the given Robot Framework Test Suite on runtime.

        Args:
            name (str): name of the test suite.
            nodes (dict): graphml nodes or states
            edges (dict): graphml edges or actions
            exec_seqs (list): list of lists with each sequence of nodes to
                execute.
            imports (list): list of libraries to import within the test suite.

        Returns:
            (robot.running.model.TestSuite): created test suite object.

        """
        self._logger.info("Creating '{name}' Test Suite...".format(name=name))
        self.test_suite = robot.api.TestSuite(name)
        for import_lib in imports:
            self._logger.debug("Importing '{import_lib}' library".format(
                import_lib=import_lib))
            self.test_suite.resource.imports.library(import_lib)
        self._create_test_cases(nodes, edges, exec_seqs)
        self._logger.info("Test Suite successfully created!")
        return self.test_suite

    def _create_test_cases(self, nodes, edges, exec_seqs):
        """
        Creates Robot Framework test cases on a given test suite in runtime
        taking a graphml file diagram as an input.

        Args:
            nodes (dict): graphml nodes or states
            edges (dict): graphml edges or actions
            exec_seqs (list): list of lists with each sequence of nodes to
                execute.

        Returns:
            None.
        """
        self._logger.info(
            "Creating test cases for '{suite_name}' test suite...".format(
                suite_name=self.test_suite.name))

        for exec_seq in exec_seqs:
            test_name = self._generate_test_name(nodes, edges, exec_seq)
            test_case = self.test_suite.tests.create(test_name)
            self._generate_test_data(test_case, nodes, edges, exec_seq)

    def _generate_test_name(self, nodes, edges, exec_seq):
        """
        Generates all the required data for a given test case.

        Args:
            nodes (dict): graphml nodes or states.
            edges (dict): graphml edges or actions.
            exec_seq (list): single sequence of nodes to execute.

        Returns:
            (str): generated test case name.
        """
        self._logger.debug(
            r"Generating test name for sequence {exec_seq}".format(
                exec_seq=str(exec_seq)))
        test_name = ''

        for i in range(len(exec_seq)):

            if exec_seq[i] in nodes:
                test_name += nodes[exec_seq[i]]['label'] + '->'

            elif exec_seq[i] in edges:
                test_name += edges[exec_seq[i - 1]][exec_seq[i]]['label'] + ' '

        test_name = test_name.strip('->')
        self._logger.debug(
            r"Test name '{test_name}' successfully generated!".format(
                test_name=test_name))
        return test_name

    def _generate_test_data(self, test_case, nodes, edges, exec_seq):
        """
        Generates all the required data for a given test case.

        Args:
            test_case (robot.running.model.TestCase).
            nodes (dict): graphml nodes or states.
            edges (dict): graphml edges or actions.
            exec_seq (list): single sequence of nodes to execute.

        Returns:
            None.
        """
        self._logger.info(
            "Creating test case '{name}' for sequence '{path}'...".format(
                name=test_case.name, path=exec_seq))

        #if str(nodes[exec_seq[0]]['label']).lower() == 'start':
        #    test_case.keywords.create(nodes[exec_seq[0]]['label'])

        for i in range(len(exec_seq) - 1):
            self._logger.debug("Generating test case keywords...")
            prev_node = exec_seq[i]
            curr_node = exec_seq[i + 1]
            edge_i_want = None
            for edge in edges:
                if edge[0] == prev_node and edge[1] == curr_node:
                    edge_i_want = edge
                    break
            edge_label = edge_i_want[2]['label']

            # in case edge contains an Action
            # if len(edge_label.split('/')) > 1:
            #    test_case.keywords.create(edge_label.split('/')[0],
            #                              args=[edge_label.split('/')[1]])

            # in case edge does not contain an Action
            #else:
            test_case.keywords.create(edge_label)

            test_case.keywords.create(nodes[curr_node]['label'])

        self._logger.info("Test case successfully created!")
