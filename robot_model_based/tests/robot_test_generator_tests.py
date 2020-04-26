import unittest
import logging
import mock

from robot_model_based.robot_test_generator import RobotTestGenerator


class RobotTestGeneratorTests(unittest.TestCase):
    """
    Unitary tests for RobotTestGenerator class
    """
    _SUITE_NAME = 'ts1'
    _NODES = {'n0': {'y': '122.0', 'x': '603.1', 'label': 'Start'},
              'n1': {'y': '288.0', 'x': '603.1', 'label': 'idle'},
              'n2': {'y': '436.0', 'x': '603.1', 'label': 'selecting'},
              'n3': {'y': '436.0', 'x': '347.20000000000005',
                     'label': 'canceling'},
              'n4': {'y': '436.0', 'x': '839.0', 'label': 'serving'},
              'n5': {'y': '631.06', 'x': '603.1',
                     'label': 'returning_change'},
              'n6': {'y': '773.0', 'x': '603.1', 'label': 'idle'},
              'n7': {'y': '288.0', 'x': '347.20000000000005',
                     'label': 'off'}}
    _EDGES = {'n0': {'n1': {'id': 'e1', 'label': 'turn_on'}},
              'n1': {'n2': {'id': 'e0', 'label': 'input_money'},
                     'n7': {'id': 'e7', 'label': 'turn_off'}},
              'n2': {'n3': {'id': 'e2', 'label': 'cancel'},
                     'n4': {'id': 'e3', 'label': 'select_coffee'}},
              'n3': {'n5': {'id': 'e5', 'label': 'return_change'}},
              'n4': {'n5': {'id': 'e4', 'label': 'return_change'}},
              'n5': {'n6': {'id': 'e6', 'label': 'return_to_idle_state'}},
              'n6': {}, 'n7': {'n1': {'id': 'e8', 'label': 'turn_on'}}}
    _EXEC_SEQS = [['n0', 'n1', 'n7', 'n1'],
                  ['n0', 'n1', 'n2', 'n3', 'n5', 'n6'],
                  ['n0', 'n1', 'n2', 'n4', 'n5', 'n6']]
    _IMPORTS = ['Module1.Lib1', 'Module1.Lib2']

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self._tc_gen = RobotTestGenerator()

    @mock.patch('robot_model_based.robot_test_generator.RobotTestGenerator.'
                '_create_test_cases')
    @mock.patch('robot.api.TestSuite')
    def test_create_test_suite(self, mock_robot_ts, mock_create_tc):
        test_suite_mock = mock.Mock()
        mock_robot_ts.side_effect = [test_suite_mock]
        ts = self._tc_gen.create_test_suite(self._SUITE_NAME, self._NODES,
                                            self._EDGES, self._EXEC_SEQS,
                                            self._IMPORTS)
        self.assertEqual(test_suite_mock, ts)
        test_suite_mock.resource.imports.library.assert_has_calls([
            mock.call(self._IMPORTS[0]), mock.call(self._IMPORTS[1])])
        mock_create_tc.assert_called_once_with(self._NODES, self._EDGES,
                                               self._EXEC_SEQS)

    @mock.patch('robot_model_based.robot_test_generator.RobotTestGenerator.'
                '_generate_test_data')
    @mock.patch('robot_model_based.robot_test_generator.RobotTestGenerator.'
                '_generate_test_name')
    def test_create_test_cases(self, mock_gen_test_name, mock_gen_test_data):
        test_suite_mock = mock.Mock()
        test_case_1 = mock.Mock()
        test_case_2 = mock.Mock()
        test_case_3 = mock.Mock()
        test_suite_mock.tests.create.side_effect = [test_case_1,
                                                    test_case_2,
                                                    test_case_3]
        mock_gen_test_name.side_effect = ['tc1', 'tc2', 'tc3']
        self._tc_gen.test_suite = test_suite_mock
        self._tc_gen._create_test_cases(self._NODES, self._EDGES,
                                        self._EXEC_SEQS)
        test_suite_mock.tests.create.assert_has_calls(
            [
                mock.call('tc1'),
                mock.call('tc2'),
                mock.call('tc3')
            ]
        )
        mock_gen_test_name.assert_has_calls(
            [
                mock.call(self._NODES, self._EDGES, self._EXEC_SEQS[0]),
                mock.call(self._NODES, self._EDGES, self._EXEC_SEQS[1]),
                mock.call(self._NODES, self._EDGES, self._EXEC_SEQS[2])
            ]
        )
        mock_gen_test_data.assert_has_calls(
            [
                mock.call(test_case_1, self._NODES, self._EDGES,
                          self._EXEC_SEQS[0]),
                mock.call(test_case_2, self._NODES, self._EDGES,
                          self._EXEC_SEQS[1]),
                mock.call(test_case_3, self._NODES, self._EDGES,
                          self._EXEC_SEQS[2])
            ]
        )

    def test_generate_test_name(self):
        expected_name = r'Start->idle->off->idle'
        test_name = self._tc_gen._generate_test_name(self._NODES, self._EDGES,
                                                     self._EXEC_SEQS[0])
        self.assertEqual(expected_name, test_name)

    def test_generate_test_data(self):
        test_case = mock.Mock()
        self._tc_gen._generate_test_data(test_case, self._NODES, self._EDGES,
                                         self._EXEC_SEQS[0])
        test_case.keywords.create.assert_has_calls(
            [
                mock.call('turn_on'),
                mock.call('idle'),
                mock.call('turn_off'),
                mock.call('off'),
                mock.call('turn_on'),
                mock.call('idle')
            ]
        )
