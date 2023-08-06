import ast
import asyncio
from shlex import split
import time
from typing import Optional

import click
from gql import Client
from gql import gql
from rich.table import Table
import websockets

from grid.observables.base import BaseObservable
from grid.observables.base import style_status
from grid.observables.base import TASK_CLASS_MAPPING
from grid.utilities import get_experiment_duration_string
from grid.utilities import get_param_values


class Experiment(BaseObservable):
    def __init__(self, client: Client, identifier: str):
        self.client = client
        self.run_name = identifier

        super().__init__(client=client)

    def get_history(self, experiment_id: Optional[str] = None):
        """
        Parameters
        ----------
        experiment_id: Optional[str]
            Experiment ID
        """
        self.spinner.start()
        self.spinner.text = 'Getting Experiments ...'

        query = gql("""
        query (
            $runName: ID!
        ) {
            getExperiments(runName: $runName) {
                name
                status
                invocationCommands
                createdAt
                finishedAt
                commitSha
                run {
                    runId
                }
                startedRunningAt
            }
        }
        """)
        params = {'runName': self.run_name}

        result = self.client.execute(query, variable_values=params)
        if not result['getExperiments']:
            click.echo(f'No experiments available for run "{self.run_name}"')
            return

        self.spinner.text = 'Done!'
        self.spinner.ok("✔")
        self.spinner.stop()
        table = self.render_experiments(result['getExperiments'])
        self.console.print(table)

    def get(self, experiment_id: Optional[str] = None):
        """
        Parameters
        ----------
        experiment_id: Optional[str]
            Experiment ID
        """
        with self.spinner:
            self.spinner.text = 'Fetching experiment status ...'

            query = gql("""
            query (
                $runName: ID!
            ) {
                getExperiments(runName: $runName) {
                    name
                    status
                    invocationCommands
                    createdAt
                    finishedAt
                    commitSha
                    run {
                        runId
                    }
                    startedRunningAt
                }
            }
            """)
            params = {'runName': self.run_name}
            result = self.client.execute(query, variable_values=params)

            experiments = result['getExperiments']
            if not experiments:
                click.echo(f'No experiments available for run "{self.run_name}"')
                return

        table = self.render_experiments(experiments)
        self.console.print(table)
        return result

    @staticmethod
    def render_experiments(experiments) -> Table:
        base_columns = [
            'Experiment',
            'Command',
            'Status',
            'Duration',
        ]
        if not experiments:
            return BaseObservable.create_table(columns=base_columns)

        command = experiments[0]['invocationCommands']
        toks = split(command)
        hparams = [tok.replace('--', '') for tok in toks if '--' in tok]

        table_columns = base_columns + hparams
        table = BaseObservable.create_table(columns=table_columns)

        for experiment in experiments:
            # Split hparam vals
            command = experiment['invocationCommands']
            base_command, *hparam_vals = get_param_values(command)
            # Get job duration - Since experiment started if running, since experiment created if queued
            duration_str = get_experiment_duration_string(created_at=experiment['createdAt'],
                                                          started_running_at=experiment['startedRunningAt'],
                                                          finished_at=experiment['finishedAt'])
            table.add_row(experiment['name'], base_command, experiment['status'], duration_str, *hparam_vals)
        return table

    def follow(self):
        pass
