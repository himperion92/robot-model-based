import unittest
import logging
import mock

from robot_model_based.robot_test_generator import RobotTestGenerator


class RobotTestGeneratorTests(unittest.TestCase):
    """
    Unitary tests for RobotTestGenerator class
    """
    _SUITE_NAME = 'ts1'
    _NODES = {'n0': {'x': '603.1', 'y': '122.0', 'label': 'Start'},
              'n1': {'x': '603.1', 'y': '288.0', 'label': 'idle'}, 
              'n2': {'x': '603.1', 'y': '436.0', 'label': 'selecting'}, 
              'n3': {'x': '347.20000000000005', 'y': '436.0', 'label': 'canceling'}, 
              'n4': {'x': '839.0', 'y': '436.0', 'label': 'serving'}, 
              'n5': {'x': '603.1', 'y': '631.06', 'label': 'returning_change'}, 
              'n6': {'x': '603.1', 'y': '773.0', 'label': 'idle'}, 
              'n7': {'x': '347.20000000000005', 'y': '288.0', 'label': 'off'}}
    _EDGES = [('n0', 'n1', {'label': 'turn_on', 'id': 'e1'}), 
              ('n1', 'n2', {'label': 'input_money', 'id': 'e0'}), 
              ('n1', 'n7', {'label': 'turn_off', 'id': 'e7'}), 
              ('n2', 'n3', {'label': 'cancel', 'id': 'e2'}), 
              ('n2', 'n4', {'label': 'select_coffee', 'id': 'e3'}), 
              ('n3', 'n5', {'label': 'return_change', 'id': 'e5'}), 
              ('n4', 'n5', {'label': 'return_change', 'id': 'e4'}), 
              ('n5', 'n6', {'label': 'return_to_idle_state', 'id': 'e6'}), 
              ('n7', 'n1', {'label': 'turn_on', 'id': 'e8'})]
    _EXEC_SEQS = [['n0', 'n1', 'n7', 'n1'],
                  ['n0', 'n1', 'n2', 'n3', 'n5', 'n6'], 
                  ['n0', 'n1', 'n2', 'n4', 'n5', 'n6']]
    _IMPORTS = ['Module1.Lib1', 'Module1.Lib2']

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self._tc_gen = RobotTestGenerator()

    @mock.patch('robot.api')
    def test_create_test_suite(self, mock_robot_api):
        test_suite_mock = mock.Mock(name="dummysuite")
        test_case_1_name = 'Start->idle->off->idle'
        test_case_2_name = 'Start->idle->selecting->canceling->returning_change->idle'
        test_case_3_name = 'Start->idle->selecting->serving->returning_change->idle'
        test_case_1_mock = mock.Mock(name=test_case_1_name)
        test_case_2_mock = mock.Mock(name=test_case_2_name)
        test_case_3_mock = mock.Mock(name=test_case_3_name)
        test_suite_mock.tests.create.side_effect = [test_case_1_mock, 
                                                    test_case_2_mock, 
                                                    test_case_3_mock]
        mock_robot_api.TestSuite.side_effect = [test_suite_mock]
        ts = self._tc_gen.create_test_suite(self._SUITE_NAME, self._NODES,
                                            self._EDGES, self._EXEC_SEQS,
                                            self._IMPORTS)
        mock_robot_api.TestSuite.assert_called_once_with(self._SUITE_NAME)
        test_suite_mock.resource.imports.library.assert_has_calls([
            mock.call(self._IMPORTS[0]), mock.call(self._IMPORTS[1])])
        test_suite_mock.tests.create.assert_has_calls([mock.call(test_case_1_name),
                                                      mock.call(test_case_2_name),
                                                      mock.call(test_case_3_name)])
        test_case_1_mock.keywords.create.assert_has_calls([mock.call('turn_on'),
                                                           mock.call('idle'),
                                                           mock.call('turn_off'),
                                                           mock.call('off'),
                                                           mock.call('turn_on'),
                                                           mock.call('idle')])                                                      
        test_case_2_mock.keywords.create.assert_has_calls([mock.call('turn_on'),
                                                           mock.call('idle'),
                                                           mock.call('input_money'),
                                                           mock.call('selecting'),
                                                           mock.call('cancel'),
                                                           mock.call('canceling'),
                                                           mock.call('return_change'),
                                                           mock.call('returning_change'),
                                                           mock.call('return_to_idle_state'),
                                                           mock.call('idle')])
        test_case_3_mock.keywords.create.assert_has_calls([mock.call('turn_on'),
                                                           mock.call('idle'),
                                                           mock.call('input_money'),
                                                           mock.call('selecting'),
                                                           mock.call('select_coffee'),
                                                           mock.call('serving'),
                                                           mock.call('return_change'),
                                                           mock.call('returning_change'),
                                                           mock.call('return_to_idle_state'),
                                                           mock.call('idle')])                                                        
        self.assertEqual(test_suite_mock, ts)