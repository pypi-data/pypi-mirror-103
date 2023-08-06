import os
import dimod
from typing import Union
from jijcloud.post_api import post_instance_and_query
from jijcloud.config import Config
from jijcloud.client import JijCloudClient
from jijcloud.entity.schema import SolverType

from cimod import BinaryPolynomialModel

from jijcloud.response import DimodResponse, APIStatus

class JijCloudSampler(dimod.Sampler):
    """JijCloudSampler
    another Sampler is based on this class
    """
    solver_type: SolverType
    hubo_solver_type: SolverType

    def __init__(self, token: str=None, url: Union[str, dict]=None, timeout=None, config=None, config_env='default'):
        """setting token and url

        Args:
            token (str, optional): token string. Defaults to None.
            url (Union[str, dict], optional): API URL. Defaults to None.
            timeout (float, optional): timeout for post request. Defaults to None.
            config (str, optional): Config file path. Defaults to None.

        Raises:
            TypeError: token, url, config is not str
        """

        self.client = JijCloudClient(url, token, config, config_env)
        self.timeout = timeout if timeout is not None else 1

    def sample(self, bqm, num_reads=1, num_sweeps=100, timeout=None, sync=True, **kwargs):
        parameters = {'num_reads': num_reads, 'num_sweeps': num_sweeps}
        parameters.update(kwargs)
        # if timeout is defined in script, use this value
        if timeout:
            self.timeout = timeout

        instance_type = 'BQM'
        instance = bqm.to_serializable()

        response = post_instance_and_query(
                        DimodResponse,
                        self.client,
                        instance_type=instance_type,
                        instance=instance,
                        queue_name=self.solver_type.queue_name,
                        solver=self.solver_type.solver,
                        parameters=parameters,
                        sync=sync)
        return response

    def sample_hubo(self, polynomial, num_reads=1, num_sweeps=100, var_type='SPIN', timeout=None, sync=True, **kwargs):
        parameters = {'num_reads': num_reads, 'num_sweeps': num_sweeps}
        parameters.update(kwargs)

        if timeout:
            self.timeout = timeout

        instance_type = 'BPM'
        instance = BinaryPolynomialModel(polynomial, var_type=var_type).to_serializable()

        response = post_instance_and_query(
                        DimodResponse,
                        self.client,
                        instance_type=instance_type,
                        instance=instance,
                        queue_name=self.hubo_solver_type.queue_name,
                        solver=self.hubo_solver_type.solver,
                        parameters=parameters,
                        sync=sync)
        return response

    def get_result(self, solution_id: str):
        response = DimodResponse.empty_response(
                APIStatus.PENDING,
                self.client.url, self.client.token,
                solution_id
                )

        return response.get_result()


    @property
    def properties(self):
        return dict()

    @property
    def parameters(self):
        return dict()
