from click.testing import CliRunner
from tests.mock_backend import resolvers
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

from grid import cli
import grid.client as grid

RUNNER = CliRunner()


class TestCancel:
    @classmethod
    def setup_class(cls):
        grid.Grid._init_client = monkey_patch_client
        grid.gql = lambda x: x

        create_test_credentials()

    def test_logs_without_arguments(self):
        """grid logs without arguments fails"""
        result = RUNNER.invoke(cli.logs, [])
        assert result.exit_code == 2
        assert result.exception
