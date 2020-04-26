import logging
from datetime import datetime

from robot.reporting import ResultWriter


class RobotTestExecutor(object):
    def __init__(self):
        self._logger = logging.getLogger(__name__)

    def execute_test_suite(self, test_suite, report_path):
        """
        Executes test suite and generates reports.

        Args:
             test_suite (robot.api.TestSuite): test suite to be executed.
             report_path (str): path where the reports will be saved.

        Returns:
            None.
        """
        self._logger.info("Executing '{name}' test suite...".format(
            name=test_suite.name))
        test_suite.run(output='{path}/{name}.xml'.format(path=report_path,
                       name=test_suite.name))
        self._logger.info("Execution finished!")
        self._generate_log_files(test_suite.name, report_path)

    def _generate_log_files(self, suite_name, report_path):
        """
        Generates _log.html, _report.html and _output.xml files given a test
        suite execution result.

        Args:
            suite_name (str): test suite name.
            report_path (str): path where the test suite result has been saved.

        Returns:
            None.
        """
        self._logger.info(
            "Generating log files for '{name}' test suite...".format(
                name=suite_name))
        curr_time = datetime.now().strftime('%Y%m%d-%H%M%S')
        ResultWriter('{report_path}/{suite_name}.xml'.format(
            report_path=report_path, suite_name=suite_name)).write_results(
                log=r'{path}/{name}-{curr_time}_log.html'.format(
                    path=report_path, curr_time=curr_time, name=suite_name),
                report=r'{path}/{name}-{curr_time}_report.html'.format(
                    path=report_path, curr_time=curr_time, name=suite_name),
                output=r'{path}/{name}-{curr_time}_output.xml'.format(
                    path=report_path, curr_time=curr_time, name=suite_name))
        self._logger.info("Log generation finished!")
