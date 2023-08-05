import logging

from spaceone.core.manager import BaseManager
from spaceone.monitoring.error import *
from spaceone.monitoring.connector.plugin_connector import PluginConnector
from spaceone.monitoring.connector.monitoring_plugin_connector import MonitoringPluginConnector
from spaceone.monitoring.model.plugin_metadata_model import MetricPluginMetadataModel, LogPluginMetadataModel

_LOGGER = logging.getLogger(__name__)


class PluginManager(BaseManager):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.plugin_connector: PluginConnector = self.locator.get_connector('PluginConnector')
        self.mp_connector: MonitoringPluginConnector = self.locator.get_connector('MonitoringPluginConnector')

    def initialize(self, plugin_id, version, domain_id):
        endpoint = self.plugin_connector.get_plugin_endpoint(plugin_id, version, domain_id)
        _LOGGER.debug(f'[init_plugin] endpoint: {endpoint}')
        self.mp_connector.initialize(endpoint)

    def init_plugin(self, options, monitoring_type):
        plugin_info = self.mp_connector.init(options)

        _LOGGER.debug(f'[plugin_info] {plugin_info}')
        plugin_metadata = plugin_info.get('metadata', {})

        self._validate_plugin_metadata(plugin_metadata, monitoring_type)
        return plugin_metadata

    def verify_plugin(self, options, secret_data, schema):
        self.mp_connector.verify(options, secret_data, schema)

    def list_metrics(self, schema, options, secret_data, resource):
        return self.mp_connector.list_metrics(schema, options, secret_data, resource)

    def get_metric_data(self, schema, options, secret_data, resource, *args):
        return self.mp_connector.get_metric_data(schema, options, secret_data, resource, *args)

    def list_logs(self, schema, options, secret_data, resource, *args):
        response_stream = self.mp_connector.list_logs(schema, options, secret_data, resource, *args)

        logs = []
        for result in self._process_stream(response_stream, return_resource_type='monitoring.Log'):
            logs += result.get('logs', [])

        return {
            'logs': logs
        }

    @staticmethod
    def _validate_plugin_metadata(plugin_metadata, monitoring_type):
        try:
            if monitoring_type == 'METRIC':
                MetricPluginMetadataModel(plugin_metadata).validate()
            else:
                LogPluginMetadataModel(plugin_metadata).validate()

        except Exception as e:
            raise ERROR_INVALID_PLUGIN_OPTIONS(reason=str(e))

    @staticmethod
    def _process_stream(response_stream, return_resource_type=None):
        is_resource_type_match = False
        for response in response_stream:
            if 'actions' in response:
                pass

            if return_resource_type and response.get('resource_type') == return_resource_type:
                if 'result' not in response:
                    raise ERROR_INTERNAL_API(message=f'Plugin response error: no return result')

                is_resource_type_match = True
                yield response['result']

        if return_resource_type is not None and is_resource_type_match is False:
            raise ERROR_INTERNAL_API(
                message=f'Plugin response error: no return resource_type ({return_resource_type})')
