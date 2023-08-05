# encoding: utf-8
from __future__ import absolute_import
import enum
import time

from rapyuta_io.clients.provision_client import ProvisionClient
from rapyuta_io.utils import ObjDict, to_objdict, DeploymentNotRunningException, RetriesExhausted
from rapyuta_io.utils.constants import DEPLOYMENT_STATUS_ATTRIBUTES, NON_DEPLOYMENT_ATTRIBUTES
from rapyuta_io.utils.settings import BIND_ID, DEFAULT_SLEEP_INTERVAL, \
    DEPLOYMENT_STATUS_RETRY_COUNT
from rapyuta_io.utils.utils import keep_attributes, remove_attributes
from six.moves import range


def _poll_till_ready(instance, retry_count, sleep_interval):
    """

    :param instance:  instance can be a deployment, volume, or a routed network instance with get_status method
    :param retry_count: Parameter to specify the retries.
    :param sleep_interval: Parameter to specify the interval between retries.

    """
    dep_status = None
    for _ in range(retry_count):
        dep_status = instance.get_status()

        if dep_status.phase == DeploymentPhaseConstants.SUCCEEDED.value:
            if dep_status.status == DeploymentStatusConstants.RUNNING.value:
                return dep_status
            time.sleep(sleep_interval)
            continue
        if dep_status.phase == DeploymentPhaseConstants.INPROGRESS.value:
            time.sleep(sleep_interval)
            continue
        if dep_status.phase == DeploymentPhaseConstants.PROVISIONING.value:
            errors = dep_status.errors or []
            if 'DEP_E153' not in errors:  # DEP_E153 (image-pull error) will persist across retries
                time.sleep(sleep_interval)
                continue

        msg = 'Deployment might not progress: phase={} status={} errors={}'.format(
            dep_status.phase, dep_status.status, dep_status.errors)
        raise DeploymentNotRunningException(msg, deployment_status=dep_status)

    msg = 'Retries exhausted: Tried {} times with {}s interval.'.format(retry_count,
                                                                        sleep_interval)
    if dep_status:
        msg += ' Deployment: phase={} status={} errors={}'.format(dep_status.phase, dep_status.status,
                                                                  dep_status.errors)
    raise RetriesExhausted(msg)


class DeploymentPhaseConstants(enum.Enum):
    """
    Enumeration variables for the deployment phase

    Deployment phase can be any of the following types \n
    DeploymentPhaseConstants.INPROGRESS \n
    DeploymentPhaseConstants.PROVISIONING \n
    DeploymentPhaseConstants.SUCCEEDED \n
    DeploymentPhaseConstants.FAILED_TO_START \n
    DeploymentPhaseConstants.PARTIALLY_DEPROVISIONED \n
    DeploymentPhaseConstants.DEPLOYMENT_STOPPED \n
    """

    def __str__(self):
        return str(self.value)

    INPROGRESS = 'In progress'
    PROVISIONING = 'Provisioning'
    SUCCEEDED = 'Succeeded'
    FAILED_TO_START = 'Failed to start'
    PARTIALLY_DEPROVISIONED = 'Partially deprovisioned'
    DEPLOYMENT_STOPPED = 'Deployment stopped'


class DeploymentStatusConstants(enum.Enum):
    """
    Enumeration variables for the deployment status

    Deployment status can be any of the following types \n
    DeploymentStatusConstants.RUNNING \n
    DeploymentStatusConstants.PENDING \n
    DeploymentStatusConstants.ERROR \n
    DeploymentStatusConstants.UNKNOWN \n
    DeploymentStatusConstants.STOPPED \n
    """

    def __str__(self):
        return str(self.value)

    RUNNING = 'Running'
    PENDING = 'Pending'
    ERROR = 'Error'
    UNKNOWN = 'Unknown'
    STOPPED = 'Stopped'


class DeploymentStatus(ObjDict):
    """
    DeploymentStatus class

    :ivar deploymentId: Deployment Id.
    :ivar name: Deployment name.
    :ivar packageId: Package Id.
    :ivar status: Deployment status
    :ivar phase: Deployment phase
    :ivar errors: Deployment errors
    :ivar componentInfo: List containing the deployment components and their status.
    :ivar dependentDeploymentStatus: Dependent deployment status.
    :ivar packageDependencyStatus: Package dependency status.
    """

    def __init__(self, *args, **kwargs):
        super(ObjDict, self).__init__(*args, **kwargs)


class Deployment(ObjDict):
    """
    Deployment class represents a running deployment. Member variables of the class represent the
    properties of the deployment.

    :ivar deploymentId: Deployment Id.
    :ivar name: Deployment name.
    :ivar planId: Plan Id.
    :ivar packageId: Package Id.
    :ivar labels: Labels associated with the deployment.
    :ivar parameters: Deployment parameters.
    :ivar componentInstanceIds: List of component instance ids.
    :ivar dependentDeployments: List of dependent deployments.
    :ivar inUse: Deployment is in use or not
    """

    def __init__(self, *args, **kwargs):
        super(ObjDict, self).__init__(*args, **kwargs)
        remove_attributes(self, NON_DEPLOYMENT_ATTRIBUTES)

    def get_status(self, retry_limit=0):
        """
        Get the deployment status

        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :returns: instance of class :py:class:`DeploymentStatus`:
        :raises: :py:class:`APIError`: If the get deployment status api returns an error, the status
                code is anything other than 200/201

        Following example demonstrates how to get a deployment status

             >>> from rapyuta_io import Client
             >>> client = Client(auth_token='auth_token', project="project_guid")
             >>> deployment = client.get_deployment('test_deployment_id')
             >>> deployment.get_status()

        """
        provision_client = ProvisionClient(self._host, self._auth_token, self._project)
        deployment_status = provision_client.deployment_status(self.deploymentId, retry_limit)
        keep_attributes(deployment_status, DEPLOYMENT_STATUS_ATTRIBUTES)
        return DeploymentStatus(to_objdict(deployment_status))

    def deprovision(self, retry_limit=0):
        """
        Deprovision the deployment instance represented by the corresponding  :py:class:`~Deployment`: class.

        :param retry_limit:
        :return: True if de-provision is successful, False otherwise
        :raises: :py:class:`~rapyuta_io.utils.error.ParameterMissingException`: If the planId or
                 deploymentId is missing in the request.
        :raises: :py:class:`~rapyuta_io.utils.error.APIError`: If the deprovision-api returns an error, the status code
            is anything other than 200/201

        Following example demonstrates how to deprovision a deployment

             >>> from rapyuta_io import Client
             >>> client = Client(auth_token='auth_token', project="project_guid")
             >>> deployment = client.get_deployment('test_deployment_id')
             >>> deployment.deprovision()

        """
        provision_client = ProvisionClient(self._host, self._auth_token, self._project)
        return provision_client.deprovision(self.deploymentId, self.planId, self.packageId,
                                            retry_limit)

    def get_service_binding(self, binding_id=None, retry_limit=0):
        """
        Get the service bindings of the deployment. Service Bindings contain the credentials that
        can be used to communicate with the deployment.

        :param binding_id: Optional parameter Binding Id
        :type binding_id: string
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: Service binding dictionary containing credentials.
        :raises: :py:class:`ServiceBindingError`: If the request failed to get the service binding.
        :raises: :py:class:`APIError`: If service binding api return an error, the status code is
            anything other than 200/201

        Following example demonstrates how to get the service binding

             >>> from rapyuta_io import Client
             >>> client = Client(auth_token='auth_token', project="project_guid")
             >>> deployment = client.get_deployment('test_deployment_id')
             >>> deployment.get_service_binding()

        """

        if binding_id is None:
            binding_id = BIND_ID
        provision_client = ProvisionClient(self._host, self._auth_token, self._project)
        credentials = provision_client.service_binding(self.deploymentId, self.planId,
                                                       self.packageId, binding_id, retry_limit)
        return credentials

    def poll_deployment_till_ready(self, retry_count=DEPLOYMENT_STATUS_RETRY_COUNT,
                                   sleep_interval=DEFAULT_SLEEP_INTERVAL):
        """

        Wait for the deployment to be ready

        :param retry_count: Optional parameter to specify the retries. Default value is 15
        :param sleep_interval: Optional parameter to specify the interval between retries.
                Default value is 6 Sec.
        :return: instance of class :py:class:`DeploymentStatus`:
        :raises: :py:class:`APIError`: If service binding api return an error, the status code is
            anything other than 200/201
        :raises: :py:class:`DeploymentNotRunningException`: If the deployment’s state might not 
            progress due to errors.
        :raises: :py:class:`RetriesExhausted`: If number of polling retries exhausted before the 
            deployment could succeed or fail.

        Following example demonstrates use of poll_deployment_till_ready, and in case of deployment
        failure uses error codes to check whether it was due to device being offline.
        Read more on error codes: https://userdocs.rapyuta.io/developer-guide/manage-software-cycle/deployments/#error-codes

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.utils.error import (DeploymentNotRunningException,
            ...     RetriesExhausted)
            >>> client = Client(auth_token='auth_token', project="project_guid")
            >>> deployment = client.get_deployment('test_deployment_id')
            >>> try:
            ...     dep_status = deployment.poll_deployment_till_ready()
            ...     print dep_status
            ... except RetriesExhausted as e:
            ...     print e, 'Retry again?'
            ... except DeploymentNotRunningException as e:
            ...     print e
            ...     if 'DEP_E151' in e.deployment_status.errors:
            ...         print 'Device is either offline or not reachable'


        """
        return _poll_till_ready(self, retry_count, sleep_interval)

    def get_component_instance_id(self, component_name):
        for component_info in self.componentInfo:
            component_instance_id = component_info.get('componentInstanceID')
            if component_info.get('name') == component_name:
                return component_instance_id
        return None
