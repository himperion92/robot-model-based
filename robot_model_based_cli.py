import logging
import argparse

from robot_model_based.sequence_generator import SequenceGenerator
from robot_model_based.robot_test_generator import RobotTestGenerator
from robot_model_based.robot_test_executor import RobotTestExecutor


def main():
    parser = argparse.ArgumentParser(
        description='Robot Framework model based test case generator.')
    parser.add_argument('--graph', '-g', help='Path to the graph file',
                        required=True)
    parser.add_argument('--strategy', '-s',
                        help='assign a path generator strategy: random, or'
                        'full', required=True)
    parser.add_argument('--coverage', '-c', type=int,
                        help='test node coverage. Optional parameter used when'
                        'strategy is random. Default value is 100',
                        required=False)
    parser.add_argument('--testsuite', '-t', help='Test Suite name',
                        required=True)
    parser.add_argument('--libraries', '-l', nargs='+',
                        help='libraries to be imported', required=True)
    parser.add_argument('--report', '-r', help='Path where the report files'
                        'will be stored', required=True)

    args = parser.parse_args()
    graph_seq_generator = SequenceGenerator()
    robot_tc_generator = RobotTestGenerator()
    robot_tc_executor = RobotTestExecutor()

    coverage = args.coverage if args.coverage else 100
    nodes, edges, exec_seq = graph_seq_generator.generate_sequences(
        file_path=args.graph, path_strategy=args.strategy, coverage=coverage)
    test_suite = robot_tc_generator.create_test_suite(args.testsuite,
                                                      nodes, edges, exec_seq,
                                                      args.libraries)
    robot_tc_executor.execute_test_suite(test_suite, args.report)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
