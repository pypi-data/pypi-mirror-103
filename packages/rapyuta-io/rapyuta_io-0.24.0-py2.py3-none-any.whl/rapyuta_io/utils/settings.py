# encoding: utf-8

default_host_config = {
    "core_api_host": "https://gaapiserver.apps.rapyuta.io",
    "catalog_host": "https://gacatalog.apps.rapyuta.io",
    "rip_host": "https://garip.apps.rapyuta.io"
}

# Paramserver APIs
PARAMSERVER_API_BASE_PATH = '/api/paramserver/'
PARAMSERVER_API_TREE_PATH = PARAMSERVER_API_BASE_PATH + 'tree/'
PARAMSERVER_API_TREEBLOBS_PATH = PARAMSERVER_API_BASE_PATH + 'treeblobs'
PARAMSERVER_API_FILENODE_PATH = PARAMSERVER_API_BASE_PATH + 'filenode/'
# Device selection API host Config
SHARED_URL_PATH = '/logs/sharedurl'
DEVICE_API_BASE_PATH = '/api/device-manager/v0/'
DEVICE_PATH = 'device/'
DEVICE_API_PATH = DEVICE_API_BASE_PATH + 'devices/'
DEVICE_SELECTION_API_PATH = DEVICE_API_BASE_PATH + 'selection/query/'
DEVICE_CONFIG_VAR_API_PATH = DEVICE_API_BASE_PATH + 'config_variables/'
DEVICE_COMMAND_API_PATH = DEVICE_API_BASE_PATH + 'cmd/'
DEVICE_TOPIC_API_PATH = DEVICE_API_BASE_PATH + 'topics/'
PARAMETERS_API_PATH = DEVICE_API_BASE_PATH + 'parameters/'
TOPIC_STATUS = '/status'
TOPIC_SUBSCRIBE = '/subscribe'
TOPIC_UNSUBSCRIBE = '/unsubscribed'
DEVICE_LABEL_API_PATH = DEVICE_API_BASE_PATH + 'labels/'
DEVICE_LOG_API_PATH = DEVICE_API_BASE_PATH + 'logs/'
FILE_DOWNLOAD_PATH = 'download?file_path='
DESERIALIZE_PATH = 'deserialize'
DEVICE_METRIC_API_PATH = DEVICE_API_BASE_PATH + 'metrics/'
# Catalog API Config
CATALOG_API_PATH = '/serviceclass/status'
PROVISION_API_PATH = '/v2/service_instances'
DEPROVISION_API_PATH = '/v2/service_instances'
SERVICE_INSTANCE_GUID = 'ser-guid'

INSTANCE_ID = 'instanceId'
ORGANIZATION_GUID = 'organizationGuid'
SPACE_GUID = 'spaceGuid'
BIND_ID = 'bind-rio'

VOLUME_PACKAGE_ID = 'io-public-persistent-volume'
LOCAL_COMMUNICATION_BROKER_ID = 'io-public-amqp-broker-amd64'
LABEL_FORMAT = {
    "labels": {

        "select_criteria": {
            "fields": [
                {
                    "operator": "=",
                    "field": "",
                    "values": {"max_value": "", "min_value": ""}
                }
            ],
            "clause": "OR"
        }
    }
}

MEASUREMENT_FORMAT = {
    "measurements": {
        "measurement": "topicInt",
        "select_criteria": {
            "fields": [
                {
                    "operator": ">",
                    "field": "data",
                    "values": {"max_value": 700, "min_value": 100}
                }
            ],
            "clause": "OR"}
    }
}

EMPTY = ''
AUTH_TOKEN = ''
PROJECT = ''
DEVICE = 'device'
TOPICS = 'topics'
KIND = 'kind'
STATUS = 'status'
SUCCESS = 'success'
RESUMABLE_UPLOAD_URL = 'resumable_upload_url'
DEFAULT_SLEEP_INTERVAL = 6
DEPLOYMENT_STATUS_RETRY_COUNT = 15

BIND_ID_PREFIX = 'bind-'
DEFAULT_RANDOM_VALUE_LENGTH = 10

ENV_VAR_REGEX_PATTERN = r'[a-zA-Z_][a-zA-Z0-9_]*'
