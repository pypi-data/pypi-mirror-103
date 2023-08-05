# encoding: utf-8
from __future__ import absolute_import
import json

import enum

import requests
from rapyuta_io.clients.deployment import DeploymentPhaseConstants
from rapyuta_io.clients.model import TopicsStatus, DeviceConfig, Label, Metric, LogUploadStatus, \
    LogUploads, SharedURL
from rapyuta_io.utils import ObjDict, RestClient, ParameterMissingException, \
    ConfigNotFoundException, to_objdict, LabelNotFoundException, DeviceNotFoundException, \
    DeploymentRunningException, \
    OperationNotAllowedError, UnknownTopicStatusException, LogsUUIDNotFoundException
from rapyuta_io.utils.rest_client import HttpMethod
from rapyuta_io.utils.settings import *
from rapyuta_io.utils.utils import create_auth_header, get_error, get_api_response_data, \
    validate_key_value, response_validator

DEVICE_API_ERRORS = {
    400: ParameterMissingException,
    404: DeviceNotFoundException
}


class TopicQOS(enum.IntEnum):
    """
    .. deprecated:: 0.7.0
        Use :class:`QoS` instead. \n
        Enumeration variables for the Topic qos. Topic qos may be 0, 1 or 2 \n
        TopicQOS.ZERO \n
        TopicQOS.ONE \n
        TopicQOS.TWO \n
    """

    ZERO = 0
    ONE = 1
    TWO = 2


class QoS(enum.IntEnum):
    """
    Enumeration variables for QoS for topic/metric subscription. \n
    QoS.LOW \n
    QoS.MEDIUM \n
    QoS.HIGH \n
    """

    def __int__(self):
        return self.value

    LOW = 0
    MEDIUM = 1
    HIGH = 2


class TopicKind(enum.Enum):
    """
    Enumeration variables for the Topic kind. Topic kind may be 'Metric' or 'Log' \n
    TopicKind.METRIC \n
    TopicKind.LOG
    """

    def __str__(self):
        return str(self.value)

    METRIC = 'METRIC'
    LOG = 'LOG'


class DeviceStatus(enum.Enum):
    """
    DeviceStatus enumeration represents the supported device status.
    Device status can be any of the below types \n
    DeviceStatus.ONLINE \n
    DeviceStatus.REJECTED \n
    DeviceStatus.ACCEPTED \n
    DeviceStatus.OFFLINE \n
    DeviceStatus.REGISTERED \n
    DeviceStatus.INITIALIZING \n
    DeviceStatus.FAILED \n
    DeviceStatus.NEW \n
    DeviceStatus.DELETED \n
    """

    def __str__(self):
        return str(self.value)

    ONLINE = 'ONLINE'
    REJECTED = 'REJECTED'
    ACCEPTED = 'ACCEPTED'
    OFFLINE = 'OFFLINE'
    REGISTERED = 'REGISTERED'
    INITIALIZING = 'INITIALIZING'
    FAILED = 'FAILED'
    NEW = 'NEW'
    DELETED = 'DELETED'


class SystemMetric(enum.Enum):
    """
    Metrics options that are currently supported by device.
    User can subscribe any of metrics options given below \n
    SystemMetric.CPU \n
    SystemMetric.MEMORY \n
    SystemMetric.DISK \n
    SystemMetric.DISKIO \n
    SystemMetric.NETWORK \n
    SystemMetric.WIRELESS \n
    """

    def __str__(self):
        return str(self.value)

    CPU = 'cpu'
    MEMORY = 'memory'
    DISK = 'disk'
    DISKIO = 'diskio'
    NETWORK = 'network'
    WIRELESS = 'wireless'


class Device(ObjDict):
    """
    Device class represents a device. Member variables of the class represent the
    properties of device.

    :ivar uuid: Id of the device.
    :ivar name: Name of the device.
    :ivar status: Status of the device. Status can be ONLINE/OFFLINE/REGISTERED.
    :ivar username: User log in to device
    :ivar saltversion: Salt version of the device.
    :ivar registration_time: Device registration time.
    :ivar description: Description of the device.
    :ivar labels: List of labels associated with the device.
    :ivar config_variables: Configuration variables of the device.
    :ivar deployments: List of deployments on device
    :ivar error_code: Error code when device goes to FAILED state. Will be of the form: 'DEV_E*'.
    :ivar error_message: Error message when device goes to FAILED state.

    """

    RUNTIME = 'runtime'
    PRE_INSTALLED = 'preinstalled'
    DOCKER_COMPOSE = 'dockercompose'

    def __init__(self, *args, **kwargs):
        self.status = None
        self.labels = list()
        self.deployments = list()
        self.config_variables = list()
        super(ObjDict, self).__init__(*args, **kwargs)
        self._post_init()

    def _post_init(self):
        self.deviceId = self.uuid
        if self.config_variables:
            config_vars = [DeviceConfig(to_objdict(config)) for config in self.config_variables]
            self.config_variables = config_vars
        if self.labels:
            labels = [Label(to_objdict(label)) for label in self.labels]
            self.labels = labels

    def _execute_api(self, url, request_method=HttpMethod.GET, payload=None, retry_limit=0):
        headers = create_auth_header(self._auth_token, self._project)
        headers['Content-Type'] = 'application/json'
        rest_client = RestClient(url).method(request_method).headers(headers)
        response = rest_client.retry(retry_limit).execute(payload=payload)
        return response

    def is_online(self):
        if self.status == DeviceStatus.ONLINE.value:
            return True
        return False

    def get_runtime(self):
        """
        Get the device runtime
        :return: value of device configuration variable: runtime

        Following example demonstrates how to get device runtime.

        >>> from rapyuta_io import Client
        >>> client = Client(auth_token='auth_token', project="project_guid")
        >>> device = client.get_device('test_device_id')
        >>> device.get_runtime()
        """

        for config in self.config_variables:
            if config.key == self.RUNTIME:
                return config.value

    @response_validator(errors=DEVICE_API_ERRORS, return_value=True)
    def save(self, retry_limit=0):
        """
        Update device details such as device name, device status and description.

        :param retry_limit: Optional parameter to specify the number of retry attempts to be
               carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: returns true if the device details updated successfully.
        :raises: :py:class:`~utils.error.DeviceNotFountException`:  If the device is not found.
        :raises: :py:class:`~utils.error.ParameterMissingException`:  If any parameters are
                 missing in the request.
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is
            anything other than 200/201

        Following example demonstrates how to update a device.

        >>> from rapyuta_io import Client
        >>> client = Client(auth_token='auth_token', project="project_guid")
        >>> device = client.get_device('test_device_id')
        >>> device.name = 'new_device_name'
        >>> device.save()

        """
        url = self._device_api_host + DEVICE_API_PATH
        device = self
        # todo: update backend api to get id in url
        device.device_id = self.uuid
        return self._execute_api(url, HttpMethod.PUT, self, retry_limit)

    def refresh(self, retry_limit=0):
        """
        Refresh the device details

        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :raises: :py:class:`~utils.error.DeviceNotFountException`:  If the device is not found.
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is
            anything other than 200/201

        """
        url = self._device_api_host + DEVICE_API_PATH + self.uuid
        response = self._execute_api(url, HttpMethod.GET, retry_limit=retry_limit)
        device_data = get_api_response_data(response)
        device = Device(to_objdict(device_data))
        for attr in device.keys():
            self.__setattr__(attr, device.__getattr__(attr))

    def reject_device(self, retry_limit=0):
        self.status = DeviceStatus.REJECTED
        return self.save(retry_limit)

    def accept_device(self, retry_limit=0):
        self.status = DeviceStatus.ACCEPTED
        return self.save(retry_limit)

    def delete(self, retry_limit=0):
        """
        Delete the device

        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occur during the API call.
        :type retry_limit: int
        :return: True if the device is deleted successfully. Otherwise returns False.
        :raises: :py:class:`~utils.error.DeviceNotFoundException`:  If the device is not found.
        :raises: :py:class:`~utils.error.DeploymentRunningException`:  When any deployment is
                 running on the device.
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code
            is anything other than 200/201

        Following example demonstrates how to delete a device

         >>> from rapyuta_io import Client
         >>> from rapyuta_io.clients.model import Label
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> device.delete()

        """

        for deployment in self.deployments:
            if deployment.phase.lower() == DeploymentPhaseConstants.SUCCEEDED.value.lower():
                raise DeploymentRunningException('Cannot delete device. Deployment %s is running '
                                                 'on the device' % deployment.deployment_id)

        url = self._device_api_host + DEVICE_API_PATH + self.uuid
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).method(HttpMethod.DELETE).headers(headers) \
            .retry(retry_limit).execute()
        if response.status_code == requests.codes.BAD_REQUEST:
            raise DeploymentRunningException()
        delete_status = get_api_response_data(response, True)
        if delete_status[STATUS] == SUCCESS:
            self.clear()
            return True
        return False

    def execute_command(self, command, retry_limit=0):
        """
        Execute command on device

        :param command: Command to execute
        :type command: :py:class:`Command`
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: Execution result

        :raises: :py:class:`~utils.error.ParameterMissingException`: If any parameters are missing
                 in the request.
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is
            anything other than 200/201

        Following example demonstrates how to execute a command.

         >>> from rapyuta_io import Client
         >>> from rapyuta_io.clients.model import Command
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id', )
         >>> command = Command(cmd='uname -a', shell='/bin/bash', bg=False)
         >>> device.execute_command(command)

        """
        command.validate()
        command.device_ids = [self.uuid]
        url = self._device_api_host + DEVICE_COMMAND_API_PATH
        response = self._execute_api(url, HttpMethod.POST, command.to_json(), retry_limit)
        if response.status_code == requests.codes.BAD_REQUEST:
            raise ParameterMissingException(get_error(response.text))
        execution_result = get_api_response_data(response)
        return execution_result[self.uuid]

    def get_config_variables(self):
        """
        Get configuration variables associated with the device

        :return: list of instances of :py:class:`~clients.DeviceConfig` class.
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is
            anything other than 200/201

        """
        url = self._device_api_host + DEVICE_CONFIG_VAR_API_PATH + DEVICE_PATH + self.uuid
        response = self._execute_api(url, HttpMethod.GET)
        config_list = get_api_response_data(response)
        config_vars = [DeviceConfig(to_objdict(config)) for config in config_list]
        self.config_variables = config_vars
        return self.config_variables

    def add_config_variable(self, key, value):
        """
        Add new configuration variable to the device.

        :param key: Configuration variable key
        :type key: string
        :param value: Configuration value
        :type value: string
        :return: instance of :py:class:`~.DeviceConfig` class.
        :raises: :py:class:`~utils.error.ParameterMissingException`: If any parameters are missing
                 in the request.
        :raises: :py:class:`~utils.error. DeviceNotFoundException`: If the device is not found.
        :raises: :py:class:`~utils.error.APIError`: If the API returns an error, the status code is
            anything other than 200/201

        Following example demonstrates how to add a device configuration variable.

         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> device.add_config_variable('config_key', 'config_value')

        """

        if not key or not value:
            raise ParameterMissingException()
        config_var = {'key': key, 'value': value}
        url = self._device_api_host + DEVICE_CONFIG_VAR_API_PATH + DEVICE_PATH + self.uuid
        response = self._execute_api(url, HttpMethod.POST, payload=config_var)
        if response.status_code == requests.codes.BAD_REQUEST:
            raise ParameterMissingException(get_error(response.text))
        config_var = get_api_response_data(response)
        config_obj = DeviceConfig(to_objdict(config_var))
        self.config_variables.append(config_obj)
        return config_obj

    def update_config_variable(self, config):
        """
        Update device configuration variable of a device.

        :param config: Configuration variable
        :type config: instance of :py:class:`~.DeviceConfig` class
        :return: instance of :py:class:`~.DeviceConfig` class.
        :raises: :py:class:`~utils.error.ParameterMissingException`: If any parameters are missing
                 in the request.
        :raises: :py:class:`~utils.error. DeviceNotFoundException`: If the device is not found.
        :raises: :py:class:`~utils.error.APIError`: If the API call returns an error, the status code
            is anything other than 200/201.

        Following example demonstrates how to update a device configuration variable.

         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> config_var = device.get_config_variables()[0]
         >>> config_var.value = 'new_config_value'
         >>> device.update_config_variable(config_var)

        """

        validate_key_value(config)
        if not config.is_updatable():
            raise OperationNotAllowedError('Default config variable {} cannot be '
                                           'updated'.format(config.key))

        url = self._device_api_host + DEVICE_CONFIG_VAR_API_PATH + str(config.id)
        response = self._execute_api(url, HttpMethod.PUT, payload=config)
        if response.status_code == requests.codes.BAD_REQUEST:
            raise ParameterMissingException(get_error(response.text))
        config_var = get_api_response_data(response)
        for config in self.config_variables:
            if config.id == config_var['id']:
                config.value = config_var['value']
                return config
        return DeviceConfig(to_objdict(config_var))

    def delete_config_variable(self, config_id, retry_limit=0):
        """
        Delete configuration variable for the device.

        :param config_id: Configuration variable id
        :type config_id: int
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occur during the API call.
        :type retry_limit: int
        :return: True if the configuration variable is deleted, otherwise returns false
        :raises: :py:class:`~utils.error.ParameterMissingException`: If any parameters are missing
                 in the request.
        :raises: :py:class:`~utils.error. ConfigNotFoundException`: If the configuration
                 is not found.
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is
            anything other than 200/201

        Following example demonstrates how to delete a device configuration variable.

         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> device.delete_config(config_id='config_id')

        """
        for config in self.config_variables:
            if config.id == config_id and not config.is_deletable():
                raise OperationNotAllowedError('Default config variable {} cannot be '
                                               'deleted'.format(config.key))

        url = self._device_api_host + DEVICE_CONFIG_VAR_API_PATH + str(config_id)
        response = self._execute_api(url, HttpMethod.DELETE, retry_limit)
        if response.status_code == requests.codes.NOT_FOUND:
            raise ConfigNotFoundException(get_error(response.text))
        delete_status = get_api_response_data(response, True)
        if delete_status[STATUS] == SUCCESS:
            for config in self.config_variables:
                if config.id == config_id:
                    self.config_variables.remove(config)
                    break
            return True
        return False

    def get_deployments(self):
        """
        Get partial details of deployments associated with the device. Also, update `deployments` field with these. \n

        **Note**: Deployment details are partial. For full :class:`~rapyuta_io.clients.deployment.Deployment` objects,
        use :meth:`~rapyuta_io.rio_client.Client.get_deployment` as shown in the example below.

        :return: List of deployment details.

        Following example demonstrates how to get device deployments

         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> partial_deployments = device.get_deployments()
         >>> # to get full deployments objects:
         >>> for dep in partial_deployments:
         >>>     full_deployment = client.get_deployment(dep['io_deployment_id'])

        """
        url = self._device_api_host + DEVICE_API_PATH + self.deviceId
        response = self._execute_api(url, HttpMethod.GET)
        if response.status_code == requests.codes.NOT_FOUND:
            raise DeviceNotFoundException(get_error(response.text))
        device_resp = get_api_response_data(response)
        deployment_list = device_resp['deployments']
        self.deployments = [to_objdict(dep) for dep in deployment_list]
        return self.deployments

    def get_labels(self):
        """
        Get all labels associated with the device

        :return: list of instances of the class :py:class:`~clients.model.Label`.

        Following example demonstrates how to get device labels

         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> device.get_labels()

        """

        url = self._device_api_host + DEVICE_LABEL_API_PATH + self.uuid
        response = self._execute_api(url, HttpMethod.GET)
        if response.status_code == requests.codes.NOT_FOUND:
            raise DeviceNotFoundException(get_error(response.text))
        self.labels = [Label(to_objdict(label)) for label in get_api_response_data(response)]
        return self.labels

    def add_label(self, key, value, retry_limit=0):
        """
        Add label to the device

        :param key: label key
        :type key: string
        :param key: label value
        :type key: string
        :param retry_limit: Optional parameter to specify the number of retry attempts to be carried out if any failures occur during the API call.
        :type retry_limit: int
        :return: instances of the class :py:class:`~clients.model.Label`.
        :raises: :py:class:`~utils.error. DeviceNotFoundException`: If the device is not found.
        :raises: :py:class:`~utils.error.ParameterMissingException`: If any parameters are missing in the request.
        :raises: :py:class:`~utils.error.APIError`: If the API call returns an error, the status code
            is anything other than 200/201

        Following example demonstrates how to add device labels

         >>> from rapyuta_io import Client
         >>> from rapyuta_io.clients.model import Label
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> device.add_label('key', 'value')

        """

        request_data = dict()
        if not key or not value:
            raise ParameterMissingException()
        request_data[key] = value
        url = self._device_api_host + DEVICE_LABEL_API_PATH + self.uuid
        response = self._execute_api(url, HttpMethod.POST, request_data, retry_limit)
        if response.status_code == requests.codes.BAD_REQUEST:
            raise ParameterMissingException(get_error(response.text))
        label = Label(to_objdict(get_api_response_data(response)[0]))
        self.labels.append(label)
        return label

    def update_label(self, label, retry_limit=0):
        """
        Update device label

        :param label: instance of class :py:class:`~clients.model.Label` to update
        :type label: :py:class:`~clients.model.Label`
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: updated instance of the class :py:class:`Label`.
        :raises: :py:class:`~utils.error.LabelNotFoundException`: If the label is not found.
        :raises: :py:class:`~utils.error.APIError`: If the API call returns an error, the status code
            is anything other than 200/201.

        Following example demonstrates how to update a device label

         >>> from rapyuta_io import Client
         >>> from rapyuta_io.clients.model import Label
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> label = device.get_labels()[0]
         >>> label.value = 'new label value'
         >>> device.update_label(label)

        """
        validate_key_value(label)
        url = self._device_api_host + DEVICE_LABEL_API_PATH + str(label.id)
        response = self._execute_api(url, HttpMethod.PUT, label, retry_limit)
        if response.status_code == requests.codes.NOT_FOUND:
            raise LabelNotFoundException()
        for _label in self.labels:
            if _label.id == label.id:
                _label.key = label.key
                _label.value = label.value
                return _label
        return label

    def delete_label(self, label_id, retry_limit=0):
        """
        Delete a device label.

        :param label_id: Label Id to delete
        :type label_id: int
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: Boolean value to indicate whether the label is deleted or not
        :raises: :py:class:`~utils.error.LabelNotFoundException`: If the label is not found.
        :raises: :py:class:`~utils.error.APIError`: If the API call returns an error, the status code
            is anything other than 200/201.

        Following example demonstrates how to delete a device label

         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> device.delete_label('label_id')

        """

        url = self._device_api_host + DEVICE_LABEL_API_PATH + str(label_id)
        response = self._execute_api(url, HttpMethod.DELETE, retry_limit=retry_limit)
        if response.status_code == requests.codes.NOT_FOUND:
            raise LabelNotFoundException()
        delete_status = get_api_response_data(response, True)
        if delete_status[STATUS] == SUCCESS:
            for label in self.labels:
                if label.id == label_id:
                    self.labels.remove(label)
                    break
            return True
        return False

    def topics(self, retry_limit=0):
        """
        Fetching the available topics on the device

        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: List of topics in the device (list(string)
        :raises: :py:class:`~utils.error. DeviceNotFountException`: If the device is not found.
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is
            anything other than 200/201

        Following example demonstrates how to get the topic list

                >>> from rapyuta_io import Client
                >>> client = Client(auth_token='auth_token', project="project_guid")
                >>> device = client.get_device('test_device_id')
                >>> device.topics()

        """

        url = self._device_api_host + DEVICE_TOPIC_API_PATH + self.uuid
        response = self._execute_api(url, retry_limit=retry_limit)
        topic_info = get_api_response_data(response)
        if isinstance(topic_info, list):
            if topic_info[0] == requests.codes.OK:
                if isinstance(topic_info[1], dict):
                    return topic_info[1][TOPICS]
                return json.loads(str(topic_info[1]))[TOPICS]

        return list()

    def topic_status(self, retry_limit=0):
        """
        Get the subscribed and unsubscribed topics status

        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: Instance of class :py:class:`~clients.model.TopicsStatus`.
        :raises: :py:class:`~utils.error. DeviceNotFoundException`: If the device is not found.
        :raises: :py:class:`~utils.error. UnknownTopicStatusException`: If the topic status is empty.
        :raises: :py:class:`~utils.error.APIError`: If the API call returns an error, the status code is
            anything other than 200/201.

        Following example demonstrates how to get the topic status

         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> device.topic_status()

        """

        url = self._device_api_host + DEVICE_TOPIC_API_PATH + self.uuid + TOPIC_STATUS
        response = self._execute_api(url, retry_limit=retry_limit)
        topic_status = get_api_response_data(response)

        if not topic_status:
            raise UnknownTopicStatusException('No topics were found')
        topics_info = get_api_response_data(response)[1]

        if not isinstance(topics_info, dict):
            topics_info = json.loads(topics_info)

        topic_status = TopicsStatus(to_objdict(topics_info[TOPICS]))
        topic_status.master_up = topics_info['master_up']
        return topic_status

    def subscribe_topic(self, topic, qos=QoS.LOW.value, kind=TopicKind.METRIC, whitelist_tag=[],
                        whitelist_field=[], fail_on_topic_inexistence=True, retry_limit=0):
        """

        To subscribe a topic

        :param topic: topic name to subscribe
        :type topic: string
        :param qos: QoS value for topic subscription
        :type qos: integer
        :param kind: subscribe the topic as a metric or log
        :type kind: enum :py:class:`~TopicKind`
        :param whitelist_tag: Optional parameter to specify the tags that needs to be whitelisted in metrics
        :type whitelist_tag: list
        :param whitelist_field: Optional parameter to specify the fields that needs to be whitelisted in metrics
        :type whitelist_field: list
        :param fail_on_topic_inexistence: Optional parameter to fail with error if topic doesnt exists on device
        :type fail_on_topic_inexistence: bool
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: list containing subscription status.
        :raises: :py:class:`~utils.error. DeviceNotFountException`: If the device is not found.
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is
            anything other than 200/201

        Following example demonstrates how to subscribe a topic

         >>> from rapyuta_io import Client
         >>> from rapyuta_io.clients.device import QoS
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> device.subscribe_topic('test_topic', qos=QoS.MEDIUM.value, kind=TopicKind.METRIC)

        """
        # check made for backward compatability with old topic subscribe  error response behaviour when an error
        # was thrown if the topic didnt exists on rosmaster
        if fail_on_topic_inexistence:
            topics = self.topics()
            if topic not in topics:
                return {'subscribed_error': [{topic: str.format("Unknown topic type: {0}", topic)}]}

        url = self._device_api_host + DEVICE_TOPIC_API_PATH + self.uuid + TOPIC_SUBSCRIBE
        subscription_request = {
            TOPICS: [{
                'name': topic,
                'config': {
                    'qos': qos,
                    'whitelist_tag': whitelist_tag,
                    'whitelist_field': whitelist_field
                }
            }],
            KIND: str(kind).lower()
        }
        response = self._execute_api(url, HttpMethod.POST, subscription_request, retry_limit)
        subscription_status = json.loads(get_api_response_data(response)[1])
        if len(subscription_status['subscribed_error']) > 0:
            return {'subscribed_error': subscription_status['subscribed_error']}
        return {'subscribed_success': subscription_status['subscribed_success']}

    def unsubscribe_topic(self, topic, kind=TopicKind.METRIC, retry_limit=0):

        """
        To unsubscribe a topic

        :param topic: topic name to unsubscribe
        :type topic: string
        :param kind: unsubscribe the topic as a metric or log
        :type kind: enum :py:class:`~TopicKind`
        :param retry_limit: Optional parameter to specify the number of retry attempts to be
              carried out if any failures occurs during the API call.
        :type retry_limit: int
        :return: list containing unsubscription status.
        :raises: :py:class:`~utils.error. DeviceNotFountException`: If the device is not found.
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is
            anything other than 200/201

        Following example demonstrates how to unsubscribe a topic

         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='auth_token', project="project_guid")
         >>> device = client.get_device('test_device_id')
         >>> device.unsubscribe_topic('test_topic', TopicKind.METRIC)

        """

        url = self._device_api_host + DEVICE_TOPIC_API_PATH + self.uuid + TOPIC_UNSUBSCRIBE
        un_subscription_request = {TOPICS: [topic], KIND: str(kind).lower()}
        response = self._execute_api(url, HttpMethod.POST, un_subscription_request, retry_limit)
        un_subscription_status = json.loads(get_api_response_data(response)[1])
        if len(un_subscription_status['unsubscribed_error']) > 0:
            return {'unsubscribed_error': un_subscription_status['unsubscribed_error']}
        return {'unsubscribed_success': un_subscription_status['unsubscribed_success']}

    def subscribe_metric(self, metric, qos=QoS.LOW, retry_limit=0):
        """
        Subscribe to given metric on the device

        :param metric: metric to be subscribed
        :type metric: SystemMetric
        :param qos: QoS value of associated with metric
        :type qos: QoS
        :param retry_limit: Optional parameter to specify the number of retry attempts to be carried
                            out if any failure occurs during API invocation
        :type retry_limit: int
        :return: returns the boolean indicating status of the operation
        :raises: :py:class:`~utils.error.DeviceNotFoundException`: If the device is not found
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is anything
            other than 200/201

        Following example demonstrate how to subscribe to a metric
          >>> from rapyuta_io import Client
          >>> from rapyuta_io.clients.device import SystemMetric, QoS
          >>> client = Client(auth_token='auth_token', project='project_guid')
          >>> device = client.get_device('device_id')
          >>> device.subscribe_metric(SystemMetric.CPU, QoS.LOW)

        """
        url = self._device_api_host + DEVICE_METRIC_API_PATH + self.uuid
        tags = {'qos': qos.value}
        subcribe_request = {
            'name': metric.value,
            'config': tags
        }
        response = self._execute_api(url, HttpMethod.POST, subcribe_request, retry_limit)
        status = get_api_response_data(response, True)
        return status.get('status') == 'success'

    def unsubscribe_metric(self, metric, retry_limit=0):
        """
        Unsubscribe to given metric

        :param metric: metric to be unsubscribed
        :type metric: SystemMetric
        :param retry_limit: Optional parameter to specify the number of retry attempts to be carried
                            out if any failure occurs during API invocation
        :type retry_limit: int
        :return: boolean indicates the status of the operation
        :raises: :py:class:`~utils.error.DeviceNotFoundException`: If the device is not found
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is anything
            other than 200/201

        Following example demonstrate how to unsubscribe to a metric
         >>> from rapyuta_io import Client
         >>> from rapyuta_io.clients.device import SystemMetric
         >>> client = Client(auth_token='token', project='project_id')
         >>> device = client.get_device('device_id')
         >>> device.unsubscribe_metric(SystemMetric.CPU)

        """
        url = self._device_api_host + DEVICE_METRIC_API_PATH + self.uuid + '/' + metric.value
        response = self._execute_api(url, HttpMethod.DELETE, retry_limit=retry_limit)
        status = get_api_response_data(response, True)
        return status.get('status') == 'success'

    def metrics(self, retry_limit=0):
        """
        Gets the metric status from the device

        :param retry_limit: Optional parameter to specify the number of retry attempts to be carried
                            out if any failure occurs during API invocation
        :type retry_limit: int
        :return: list of instances of class :py:class:`Metric`:
        :raises: :py:class:`~utils.error.DeviceNotFoundException`: If the device is not found
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is anything
            other than 200/201

        Following example demonstrate how to get the status of metric from the device
         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='token', project='project_id')
         >>> device = client.get_device('device_id')
         >>> device.metrics()

        """
        url = self._device_api_host + DEVICE_METRIC_API_PATH + self.uuid
        response = self._execute_api(url, HttpMethod.GET, retry_limit=retry_limit)
        metrics = get_api_response_data(response)
        return [Metric(metric) for metric in metrics]

    def upload_log_file(self, upload_request, retry_limit=0):
        """
        Uploads the specified logfile in request to the cloud storage

        :param upload_request: upload specific details
        :type  upload_request: :py:class:`~.LogsUploadRequest`
        :param retry_limit: Optional parameter to specify the number of retry attempts to be carried
                            out if any failure occurs during API invocation
        :type retry_limit: int
        :return: UUID of the upload request using which user can query the status/download the file from cloud
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is anything
            other than 200/201

        Following example demonstrate how to upload the log file from device
         >>> from rapyuta_io import Client
         >>> from rapyuta_io.clients import LogsUploadRequest
         >>> client = Client(auth_token='token', project='project_id')
         >>> device = client.get_device('device_id')
         >>> upload_request = LogsUploadRequest('/path/to/file.log', file_name='new-file-name.log', override=False,
         >>>                    purge_after=False, metadata={'key': 'value'})
         >>> request_uuid = device.upload_log_file(upload_request)
        """
        url = self._device_api_host + DEVICE_LOG_API_PATH + '{}/{}'.format(self.uuid, 'upload')
        response = self._execute_api(url, HttpMethod.POST, upload_request.to_json(),
                                     retry_limit=retry_limit)
        data = get_api_response_data(response)
        return data['request_uuid']

    def get_log_upload_status(self, request_uuid, retry_limit=0):
        """
        Gets the current upload status

        :param request_uuid: UUID of the upload request
        :type request_uuid: str
        :param retry_limit: Optional parameter to specify the number of retry attempts to be carried
                            out if any failure occurs during API invocation
        :type retry_limit: int
        :return: returns instance of the class :py:class:`~.LogUploadStatus`
        :raises: :py:class:`~utils.error.LogsUUIDNotFoundException`: If the request_uuid is not found
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is anything
            other than 200/201

        Following example demonstrate how to get the status of ongoing upload operation
         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='token', project='project_id')
         >>> device = client.get_device('device_id')
         >>> upload_status = device.get_log_upload_status('request_uuid')
        """
        url = self._device_api_host + DEVICE_LOG_API_PATH + '{}/status/{}'.format(self.uuid, request_uuid)
        response = self._execute_api(url, HttpMethod.GET, retry_limit=retry_limit)
        if response.status_code == requests.codes.NOT_FOUND:
            raise LogsUUIDNotFoundException('not able to find requested UUID {}'.format(request_uuid))
        data = get_api_response_data(response)
        result = LogUploadStatus(data)
        if 'shared_urls' in result:
            for shared_url in result['shared_urls']:
                setattr(shared_url, '_device_api_host', self._device_api_host)
        return result

    def cancel_log_file_upload(self, request_uuid, retry_limit=0):
        """
        Cancels the ongoing upload operation.

        :param request_uuid: UUID of the upload request
        :type request_uuid: str
        :param retry_limit: Optional parameter to specify the number of retry attempts to be carried
                                out if any failure occurs during API invocation
        :type retry_limit: int
        :return: status of the cancel operation, True indicates operation succeeded False otherwise
        :raises: :py:class:`~utils.error.LogsUUIDNotFoundException`: If the request_uuid is not found
        :raises: :py:class:`~utils.error.BadRequestError`: if the upload operation is completed
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is anything
            other than 200/201

        Following example demonstrate how to cancel the ongoing upload operation
         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='token', project='project_id')
         >>> device = client.get_device('device_id')
         >>> cancel_status = device.cancel_log_file_upload('request_uuid')
        """
        url = self._device_api_host + DEVICE_LOG_API_PATH + '{}/{}/cancel'.format(self.uuid, request_uuid)
        response = self._execute_api(url, HttpMethod.PUT, retry_limit=retry_limit)
        if response.status_code == requests.codes.NOT_FOUND:
            raise LogsUUIDNotFoundException('not able to find requested UUID {}'.format(request_uuid))
        data = get_api_response_data(response)
        return data['success']

    def delete_uploaded_log_file(self, request_uuid, retry_limit=0):
        """
         Deletes the logs file from cloud storage

        :param request_uuid: UUID of the upload request
        :type request_uuid: str
        :param retry_limit: Optional parameter to specify the number of retry attempts to be carried
                           out if any failure occurs during API invocation
        :type retry_limit: int
        :return: status of the operation, True indicates operation succeeded false otherwise
        :raises: :py:class:`~utils.error.LogsUUIDNotFoundException`: If the request_uuid is not found
        :raises: :py:class:`~utils.error.BadRequestError`: if the upload is in progress
        :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is anything
           other than 200/201

        Following example demonstrate how to delete the uploaded log file from cloud storage
         >>> from rapyuta_io import Client
         >>> client = Client(auth_token='token', project='project_id')
         >>> device = client.get_device('device_id')
         >>> device.delete_uploaded_log_file('request_uuid')
        """
        url = self._device_api_host + DEVICE_LOG_API_PATH + '{}/{}'.format(self.uuid, request_uuid)
        response = self._execute_api(url, HttpMethod.DELETE, retry_limit=retry_limit)
        if response.status_code == requests.codes.NOT_FOUND:
            raise LogsUUIDNotFoundException('not able to find requested UUID {}'.format(request_uuid))
        data = get_api_response_data(response)
        return data['success']

    def download_log_file(self, request_uuid, retry_limit=0):
        """
        Returns downloadable log file URL, using this URL user can download log file using Wget or curl

       :param request_uuid: UUID of the upload request
       :type request_uuid: str
       :param retry_limit: Optional parameter to specify the number of retry attempts to be carried
                           out if any failure occurs during API invocation
       :type retry_limit: int
       :return: url of the uploaded log file in the cloud
       :raises: :py:class:`~utils.error.LogsUUIDNotFoundException`: If the request_uuid is not found
       :raises: :py:class:`~utils.error.BadRequestError`: if the upload operation is in progress
       :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is anything
           other than 200/201

       Following example demonstrate how to get the downloadable url
        >>> from rapyuta_io import Client
        >>> client = Client(auth_token='token', project='project_id')
        >>> device = client.get_device('device_id')
        >>> download_url = device.download_log_file('request_uuid')
        """
        url = self._device_api_host + DEVICE_LOG_API_PATH + '{}/{}'.format(self.uuid, request_uuid)
        response = self._execute_api(url, HttpMethod.GET, retry_limit=retry_limit)
        if response.status_code == requests.codes.NOT_FOUND:
            raise LogsUUIDNotFoundException('not able to find requested UUID {}'.format(request_uuid))
        data = get_api_response_data(response)
        return data['signed_url']

    def list_uploaded_files_for_device(self, retry_limit=0):
        """
        Returns list of the uploaded files with status and other properties

       :param retry_limit: Optional parameter to specify the number of retry attempts to be carried
                           out if any failure occurs during API invocation
       :type retry_limit: int
       :return: returns the list of instance of the class :py:class:`~.LogUploads`
       :raises: :py:class:`~utils.error.BadRequestError`: if the upload operation is in progress
       :raises: :py:class:`~utils.error.APIError`: If the api returns an error, the status code is anything
           other than 200/201

       Following example demonstrate how to get the downloadable url
        >>> from rapyuta_io import Client
        >>> client = Client(auth_token='token', project='project_id')
        >>> device = client.get_device('device_id')
        >>> status_list = device.list_uploaded_files_for_device()
        """
        url = self._device_api_host + DEVICE_LOG_API_PATH + '{}/list'.format(self.uuid)
        response = self._execute_api(url, HttpMethod.GET, retry_limit=retry_limit)
        data = get_api_response_data(response)
        return [LogUploads(status) for status in data]

    def create_shared_url(self, shared_url):
        """
        Create a SharedURL that let's you download the Log file from a Public URL.

       :param shared_url: Instance of the SharedURL Object
       :type shared_url: :py:class:`~rapyuta_io.clients.model.SharedURL`
       :return: Instance of :py:class:`~rapyuta_io.clients.model.SharedURL` class

       Following example demonstrate how to get the downloadable url
        >>> from datetime import timedelta, datetime
        >>> from rapyuta_io import Client
        >>> expiry_time = datetime.now() + timedelta(days=7)
        >>> client = Client(auth_token='token', project='project_id')
        >>> device = client.get_device('device_id')
        >>> log = [log.filename == 'file.log' for log in device.list_uploaded_files_for_device()][0]
        >>> shared_url = device.create_shared_url(SharedURL(log.request_uuid, expiry_time=expiry_time))
        >>> print shared_url.url
        """
        url = self._device_api_host + DEVICE_LOG_API_PATH + '{}/shared_urls'.format(shared_url.request_uuid)
        response = self._execute_api(url, HttpMethod.POST, payload=shared_url.serialize())
        if response.status_code == requests.codes.NOT_FOUND:
            raise LogsUUIDNotFoundException('not able to find requested UUID {}'.format(shared_url.request_uuid))
        data = get_api_response_data(response)
        shared_url = SharedURL.deserialize(data)
        setattr(shared_url, '_device_api_host', self._device_api_host)
        return shared_url
