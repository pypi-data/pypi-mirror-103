# encoding: utf-8
from __future__ import absolute_import
import enum

from rapyuta_io.clients import ProvisionClient
from rapyuta_io.clients.deployment import DeploymentPhaseConstants, _poll_till_ready
from rapyuta_io.clients.package import ProvisionConfiguration
from rapyuta_io.clients.plan import Plan
from rapyuta_io.utils import ObjDict, to_objdict, InvalidParameterException, DeploymentNotRunningException
from rapyuta_io.utils.constants import NON_VOLUME_INSTANCE_ATTRIBUTES, \
    VOLUME_INSTANCE_STATUS_ATTRIBUTES, NON_PACKAGE_ATTRIBUTES
from rapyuta_io.utils.settings import DEPLOYMENT_STATUS_RETRY_COUNT, DEFAULT_SLEEP_INTERVAL
from rapyuta_io.utils.utils import remove_attributes, keep_attributes

VOLUME_COMPONENT = 'volumeComponent'


class DiskType(enum.Enum):
    """
    Enumeration variables for the Volume Type. The type may be 'Default' or 'SSD' \n
    DiskType.DEFAULT \n
    DiskType.SSD
    """

    def __str__(self):
        return str(self.value)

    SSD = 'ssd'
    DEFAULT = 'ssd'


class VolumeInstanceStatus(ObjDict):
    """
    VolumeInstanceStatus class

    :ivar deploymentId: Deployment Id.
    :ivar name: Volume instance name.
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


class PersistentVolumes(ObjDict):
    """
    PersistentVolumes class represents a a persistent volume package. It contains methods to create
    persistent volume instance and listing all the instances.

    :ivar packageId: Id of the package.
    :ivar packageName: Package name.
    :ivar packageVersion: Version of the package.
    :ivar description: Description of the package.
    :ivar plans: List of plans associated with the package.
          binding of the package.
    :ivar isPublic: Boolean denoting whether the package is public or not.
    :ivar status: Status of the package.
    :ivar tags: Tags associated with the package.
    :ivar buildGeneration: Build generation.
    """

    def __init__(self, *args, **kwargs):
        super(ObjDict, self).__init__(*args, **kwargs)
        remove_attributes(self, NON_PACKAGE_ATTRIBUTES)
        plan = Plan(to_objdict(self.plans[0]))
        self.plans = [plan]

    def _update_auth_token(self, objects):
        for obj in objects:
            setattr(obj, '_host', self._host)
            setattr(obj, '_auth_token', self._auth_token)
            setattr(obj, '_project', self._project)
        return

    def create_volume_instance(self, name, capacity, disk_type=DiskType.DEFAULT, retry_limit=0):
        """
        Create a volume instance

        :param name: name of the volume instance
        :type name: str
        :param capacity: capacity of volume instance in GB. Permissible values: 32, 64, 128, 256, 512
        :type capacity: int
        :param disk_type: Type of disk to be deployed. Allowed values are - default or ssd
        :type disk_type: enum :py:class:`~DiskType`
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
               carried out if any failures occurs during the API call.
        :type retry_limit: int
        :returns: volume instance
        :raises: :py:class:`InvalidParameterException`: If the disk type and volume capacity
                 parameters are missing or invalid.
        :raises: :py:class:`APIError`: If the api return an error, the status code is
            anything other than 200/201

        Following example demonstrates how to create a volume instance

             >>> from rapyuta_io import Client
             >>> from rapyuta_io.clients.persistent_volumes import DiskType
             >>> client = Client(auth_token='auth_token', project='project_guid')
             >>> pv = client.get_persistent_volume()
             >>> pv.create_volume_instance(name='myVolume', capacity=32, disk_type=DiskType.SSD)

        """
        if not isinstance(disk_type, DiskType) or not isinstance(capacity, int):
            raise InvalidParameterException('Invalid disk type or disk capacity')
        if capacity not in (32, 64, 128, 256, 512):
            raise InvalidParameterException(
                'Disk size limits out of permitted range. Permissible limits are: 32.0GiB, 64.0GiB, 128.0GiB, 256.0GiB, 512.0GiB')

        provision_payload = ProvisionConfiguration(self.packageId, self.plans[0])
        provision_payload.add_parameter(VOLUME_COMPONENT, 'diskType', disk_type.value)
        provision_payload.add_parameter(VOLUME_COMPONENT, 'capacity', capacity)
        provision_payload.context['name'] = name
        delattr(provision_payload, 'plan')
        delattr(provision_payload, '_dependency_seen_aliases')

        provision_client = ProvisionClient(self._host, self._auth_token, self._project)
        response = provision_client.provision(provision_payload, retry_limit)
        volume_instance = provision_client.deployment_status(response['operation'], retry_limit)
        volume_instance = VolumeInstance(to_objdict(volume_instance))
        self._update_auth_token([volume_instance])
        return volume_instance

    def get_volume_instance(self, volume_instance_id, retry_limit=0):
        """
        Get a volume instance

        :param volume_instance_id: Volume instance Id
        :type volume_instance_id: string
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: return instance of class :py:class:`VolumeInstance`:
        :raises: :py:class:`APIError`: If the api return an error, the status code is
            anything other than 200/201


        Following example demonstrates how to a volume instance

            >>> from rapyuta_io import Client
            >>> client = Client(auth_token='auth_token', project="project_guid")
            >>> persistent_volume = client.get_persistent_volume()
            >>> volume_instance = persistent_volume.get_volume_instance('instance_id')

        """
        provision_client = ProvisionClient(self._host, self._auth_token, self._project)
        instance = provision_client.deployment_status(volume_instance_id, retry_limit)
        volume_instance = VolumeInstance(to_objdict(instance))
        self._update_auth_token([volume_instance])
        return volume_instance

    def get_all_volume_instances(self, phases=None, retry_limit=0):
        """
        Get all persistent volume instances

        :param phases: optional parameter to filter out the deployments based on current deployment
        :type phases: list(DeploymentPhaseConstants)
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
               carried out if any failures occurs during the API call.
        :type retry_limit: int
        :returns: List of volume instances
        :raises: :py:class:`APIError`: If the api return an error, the status code is
            anything other than 200/201

        Following example demonstrates how to create a volume instance

             >>> from rapyuta_io import Client, DeploymentPhaseConstants
             >>> client = Client(auth_token='auth_token', project="project_guid")
             >>> pv = client.get_persistent_volume()
             >>> pv.get_all_volume_instances()
             >>> volume_deployments_list_filtered_by_phase = pv.get_all_volume_instances(phases=
             >>>   [DeploymentPhaseConstants.SUCCEEDED, DeploymentPhaseConstants.PROVISIONING])

        """
        volume_list = ProvisionClient(self._host, self._auth_token, self._project) \
            .deployments(self.packageId, phases, retry_limit)
        volumes = list()
        for volume in volume_list:
            volumes.append(VolumeInstance(to_objdict(volume)))
        self._update_auth_token(volumes)
        return volumes


class VolumeInstance(ObjDict):
    def __init__(self, *args, **kwargs):
        super(ObjDict, self).__init__(*args, **kwargs)
        remove_attributes(self, NON_VOLUME_INSTANCE_ATTRIBUTES)

    def get_status(self, retry_limit=0):
        """
        Get the status of volume instance

        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :returns: instance of class :py:class:`DeploymentStatus`:
        :raises: :py:class:`APIError`: If the api return an error, the status code is
            anything other than 200/201

        Following example demonstrates how to get a deployment status

            >>> from rapyuta_io import Client
            >>> client = Client(auth_token='auth_token', project="project_guid")
            >>> persistent_volume = client.get_persistent_volume()
            >>> volume_instance = persistent_volume.get_volume_instance('instance_id')
            >>> volume_instance.get_status()

        """
        provision_client = ProvisionClient(self._host, self._auth_token, self._project)
        instance_status = provision_client.deployment_status(self.deploymentId, retry_limit)
        keep_attributes(instance_status, VOLUME_INSTANCE_STATUS_ATTRIBUTES)
        return VolumeInstanceStatus(to_objdict(instance_status))

    def poll_deployment_till_ready(self, retry_count=DEPLOYMENT_STATUS_RETRY_COUNT,
                                   sleep_interval=DEFAULT_SLEEP_INTERVAL):
        """

        Wait for the deployment to be ready

        :param retry_count: Optional parameter to specify the retries. Default value is 15
        :param sleep_interval: Optional parameter to specify the interval between retries.
              Default value is 6 Sec.
        :return: instance of class :py:class:`VolumeInstanceStatus`:
        :raises: :py:class:`APIError`: If service binding api return an error, the status code is
            anything other than 200/201
        :raises: :py:class:`DeploymentNotRunningException`: If the deployment's state might not
            progress due to errors
        :raises: :py:class:`RetriesExhausted`: If number of polling retries exhausted before the
            deployment could succeed or fail.

        Following example demonstrates use of poll_deployment_till_ready.

            >>> from rapyuta_io import Client
            >>> from rapyuta_io.utils.error import (DeploymentNotRunningException,
            ...     RetriesExhausted)
            >>> client = Client(auth_token='auth_token', project="project_guid")
            >>> persistent_volume = client.get_persistent_volume()
            >>> volume_instance = persistent_volume.get_volume_instance('instance_id')
            >>> try:
            ...     vol_status = volume_instance.poll_deployment_till_ready(sleep_interval=20)
            ...     print vol_status
            ... except RetriesExhausted as e:
            ...     print e, 'Retry again?'
            ... except DeploymentNotRunningException as e:
            ...     print e, e.deployment_status

        """
        return _poll_till_ready(self, retry_count, sleep_interval)

    def destroy_volume_instance(self, retry_limit=0):
        """
        Destroy a volume instance

        :param retry_limit: Optional parameter to specify the number of retry attempts to be
               carried out if any failures occurs during the API call.
        :type retry_limit: int
        :returns: True if volume is destroyed is successfully, False otherwise
        :raises: :py:class:`APIError`: If the api return an error, the status code is
            anything other than 200/201
        """
        provision_client = ProvisionClient(self._host, self._auth_token, self._project)
        return provision_client.deprovision(self.deploymentId, self.planId, self.packageId,
                                            retry_limit)
