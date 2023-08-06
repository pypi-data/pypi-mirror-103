from datetime import datetime

import click
from gql.transport.exceptions import TransportQueryError
import pytest
from tests.utilities import create_test_credentials
from tests.utilities import monkey_patch_client

import grid.client as grid
import grid.observables.interactive_node as interactive_node_observable


def mp_execute(*args, **kwargs):
    raise Exception("{'message':'not found'}")


class TestIneteractiveObservable:
    @classmethod
    def setup_class(cls):
        create_test_credentials()

        grid.Grid._init_client = monkey_patch_client
        interactive_node_observable.gql = lambda x: x

        cls.grid = grid.Grid(load_local_credentials=False)
        cls.grid._init_client()

    def test_get(self, capsys):
        """InteractiveNode.get() prints correct tables to terminal"""
        interactive_node_observable.env.SHOW_PROCESS_STATUS_DETAILS = False
        interactive_node_observable.env.DEBUG = True
        obsevable = interactive_node_observable.InteractiveNode(client=self.grid.client)

        obsevable.get()
        captured = capsys.readouterr()

        expected_columns = ['Name', 'Status']
        for column in expected_columns:
            assert column in captured.out

    def test_get_accounts_for_different_transition_states(self, capsys, monkeypatch):
        """InteractiveNode.get() accounts for different transition states"""
        interactive_node_observable.env.SHOW_PROCESS_STATUS_DETAILS = False
        interactive_node_observable.env.DEBUG = True
        obsevable = interactive_node_observable.InteractiveNode(client=self.grid.client)

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        def mp_different_states(*args, **kwargs):
            return {
                "getInteractiveNodes": [{
                    'interactiveNodeId': 'node-id-1',
                    'interactiveNodeName': 'node-name0-1',
                    'clusterId': 'cluster-id',
                    'createdAt': now,
                    'projectId': 'project-id',
                    'jupyterUrl': 'https://localhost/test',
                    'status': 'ready',
                    'desiredState': 'RUNNING',
                    'config': {
                        'diskSize': 100,
                        'instanceType': ''
                    }
                }, {
                    'interactiveNodeId': 'node-id-2',
                    'interactiveNodeName': 'node-name0-2',
                    'clusterId': 'cluster-id',
                    'createdAt': now,
                    'projectId': 'project-id',
                    'jupyterUrl': 'https://localhost/test',
                    'status': 'paused',
                    'desiredState': 'RUNNING',
                    'config': {
                        'diskSize': 100,
                        'instanceType': ''
                    }
                }, {
                    'interactiveNodeId': 'node-id-2',
                    'interactiveNodeName': 'node-name0-2',
                    'clusterId': 'cluster-id',
                    'createdAt': now,
                    'projectId': 'project-id',
                    'jupyterUrl': 'https://localhost/test',
                    'status': 'running',
                    'desiredState': 'PAUSED',
                    'config': {
                        'diskSize': 100,
                        'instanceType': ''
                    }
                }, {
                    'interactiveNodeId': 'node-id-2',
                    'interactiveNodeName': 'node-name0-2',
                    'clusterId': 'cluster-id',
                    'createdAt': now,
                    'projectId': 'project-id',
                    'jupyterUrl': 'https://localhost/test',
                    'status': 'running',
                    'desiredState': 'DELETED',
                    'config': {
                        'diskSize': 100,
                        'instanceType': ''
                    }
                }]
            }

        monkeypatch.setattr(self.grid.client, 'execute', mp_different_states)

        obsevable.get()
        captured = capsys.readouterr()

        expected_status = ["resuming", "pausing", "deleting"]
        for status in expected_status:
            assert status in captured.out

    def test_get_handles_error(self, capsys, monkeypatch):
        """InteractiveNode.get() handles API errors"""
        def mp_transport_error(*args, **kwargs):
            raise TransportQueryError('test')

        monkeypatch.setattr(self.grid.client, 'execute', mp_transport_error)
        obsevable = interactive_node_observable.InteractiveNode(client=self.grid.client)
        obsevable.get()

        captured = capsys.readouterr()
        assert "None Active" in captured.out
