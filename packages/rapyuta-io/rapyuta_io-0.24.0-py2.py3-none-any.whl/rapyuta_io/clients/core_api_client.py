from rapyuta_io.clients.project import Project
from rapyuta_io.clients.secret import Secret
from rapyuta_io.utils.utils import prepend_bearer_to_auth_token, create_auth_header, get_api_response_data
from rapyuta_io.utils.rest_client import HttpMethod
from rapyuta_io.utils import RestClient, to_objdict
from rapyuta_io.clients.static_route import StaticRoute
from rapyuta_io.utils.error import ResourceNotFoundError


class CoreAPIClient:
    STATIC_ROUTE_PATH = '/api/staticroute'
    PROJECT_PATH = '/api/project'
    SECRET_PATH = '/api/secret'

    def __init__(self, auth_token, project, core_api_host):
        self._core_api_host = core_api_host
        self._auth_token = prepend_bearer_to_auth_token(auth_token)
        self._project = project

    def set_project(self, project):
        self._project = project

    def _add_header_fields(self, obj):
        setattr(obj, '_core_api_host', self._core_api_host)
        setattr(obj, '_auth_token', self._auth_token)
        if type(obj) is not Project:
            setattr(obj, '_project', self._project)

    def _add_auth_token_to_routes(self, routes):
        for route in routes:
            self._add_header_fields(route)

    def _get_all_static_routes(self):
        url = self._core_api_host + self.STATIC_ROUTE_PATH + '/list'
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).headers(headers).execute()
        return get_api_response_data(response, parse_full=True)

    def _get_static_route_by_url_prefix(self, url_prefix):
        url = self._core_api_host + self.STATIC_ROUTE_PATH + '/filter'
        query_params = {'urlPrefix': url_prefix}
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).headers(headers).query_param(query_param=query_params).execute()
        return get_api_response_data(response, parse_full=True)

    def _get_static_route(self, route_guid):
        url = "{}{}/{}/get".format(self._core_api_host, self.STATIC_ROUTE_PATH, route_guid)
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).headers(headers).execute()
        return get_api_response_data(response, parse_full=True)

    def _create_static_route(self, url_prefix):
        url = self._core_api_host + self.STATIC_ROUTE_PATH + '/create'
        headers = create_auth_header(self._auth_token, self._project)
        payload = {"urlPrefix": url_prefix}
        response = RestClient(url).method(HttpMethod.POST).headers(headers).execute(payload)
        return get_api_response_data(response, parse_full=True)

    def get_all_static_routes(self):
        static_routes = []
        data = self._get_all_static_routes()
        for route in data:
            static_route = StaticRoute(to_objdict(route))
            static_routes.append(static_route)
        self._add_auth_token_to_routes(static_routes)
        return static_routes

    def get_static_route(self, route_guid):
        data = self._get_static_route(route_guid)
        route = StaticRoute(to_objdict(data))
        self._add_header_fields(route)
        return route

    def create_static_route(self, name):
        data = self._create_static_route(name)
        route = StaticRoute(to_objdict(data))
        self._add_header_fields(route)
        return route

    def get_static_route_by_name(self, name):
        try:
            routes = self._get_static_route_by_url_prefix(name)
        except ResourceNotFoundError as e:
            return None
        route = StaticRoute(to_objdict(routes[0]))
        self._add_header_fields(route)
        return route

    def create_project(self, project):
        url = self._core_api_host + self.PROJECT_PATH + '/create'
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).method(HttpMethod.POST).headers(headers).execute(project.serialize())
        data = get_api_response_data(response, parse_full=True)
        project = Project.deserialize(data)
        self._add_header_fields(project)
        return project

    def get_project(self, guid):
        url = '{}{}/{}/get'.format(self._core_api_host, self.PROJECT_PATH, guid)
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).method(HttpMethod.GET).headers(headers).execute()
        data = get_api_response_data(response, parse_full=True)
        project = Project.deserialize(data)
        self._add_header_fields(project)
        return project

    def list_projects(self):
        url = self._core_api_host + self.PROJECT_PATH + '/list'
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).method(HttpMethod.GET).headers(headers).execute()
        data = get_api_response_data(response, parse_full=True)
        projects = []
        for project_data in data:
            project = Project.deserialize(project_data)
            self._add_header_fields(project)
            projects.append(project)
        return projects

    def delete_project(self, guid):
        url = self._core_api_host + self.PROJECT_PATH + '/delete'
        headers = create_auth_header(self._auth_token, self._project)
        payload = {'guid': guid}
        response = RestClient(url).method(HttpMethod.DELETE).headers(headers).execute(payload)
        get_api_response_data(response, parse_full=True)

    def create_secret(self, secret):
        url = self._core_api_host + self.SECRET_PATH + '/create'
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).method(HttpMethod.POST).headers(headers).execute(secret.serialize())
        data = get_api_response_data(response, parse_full=True)
        secret = Secret.deserialize(data)
        self._add_header_fields(secret)
        return secret

    def get_secret(self, guid):
        url = '{}{}/{}/get'.format(self._core_api_host, self.SECRET_PATH, guid)
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).method(HttpMethod.GET).headers(headers).execute()
        data = get_api_response_data(response, parse_full=True)
        secret = Secret.deserialize(data)
        self._add_header_fields(secret)
        return secret

    def list_secrets(self):
        url = self._core_api_host + self.SECRET_PATH + '/list'
        headers = create_auth_header(self._auth_token, self._project)
        response = RestClient(url).method(HttpMethod.GET).headers(headers).execute()
        data = get_api_response_data(response, parse_full=True)
        secrets = []
        for secret_data in data:
            secret = Secret.deserialize(secret_data)
            self._add_header_fields(secret)
            secrets.append(secret)
        return secrets

    def delete_secret(self, guid):
        url = self._core_api_host + self.SECRET_PATH + '/delete'
        headers = create_auth_header(self._auth_token, self._project)
        payload = {'guid': guid}
        response = RestClient(url).method(HttpMethod.DELETE).headers(headers).execute(payload)
        get_api_response_data(response, parse_full=True)
