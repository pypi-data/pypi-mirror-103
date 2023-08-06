from os import path
import requests
from typing import Optional, Set, Union

from chrisclient2.models import PluginInstance, Plugin, Pipeline, Piping


class ChrisResourceNotFoundError(Exception):
    pass


class PluginNotFoundError(ChrisResourceNotFoundError):
    pass


class PipelineNotFoundError(ChrisResourceNotFoundError):
    pass


def run_pipeline_generator(pipeline: Pipeline, plugin_instance: PluginInstance):
    """
    Run a pipeline as a plugin instance generator. Every next() creates a plugin instance.
    :param pipeline: pipeline to run
    :param plugin_instance: plugin instance from which to start the pipeline
    """
    assembly = pipeline.assemble()
    q = assembly.to_queue()
    while not q.empty():
        p = q.get_nowait()
        params = {
            'previous_id': plugin_instance.id
        }
        params.update(p.default_parameters)
        next_instance = p.plugin.create_instance(params)
        q.task_done()
        yield next_instance
        plugin_instance = next_instance


class ChrisClient:
    def __init__(self, address: str, username: str, password: str):
        if not address.endswith('/api/v1/'):
            raise ValueError('Address of CUBE must end with "/api/v1/"')
        self.addr = address
        self.search_addr_plugins = address + 'plugins/search/'
        self.search_addr_plugins_instances = address + 'plugins/instances/search/'
        self.search_addr_pipelines = address + 'pipelins/search/'

        self._s = requests.Session()
        self._s.auth = (username, password)
        self._s.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/vnd.collection+json',
        })

        res = self._s.get(address).json()
        self.collection_links = res['collection_links']
        assert self.collection_links['uploadedfiles']

    def upload(self, file_path: str, upload_folder: str):
        """
        Upload a local file into ChRIS backend Swift storage.
        :param file_path: local file path
        :param upload_folder: path in Swift where to upload to
        :return: response
        """
        bname = path.basename(file_path)
        upload_path = path.join(upload_folder, bname)

        with open(file_path, 'rb') as file_object:
            files = {
                'upload_path': (None, upload_path),
                'fname': (bname, file_object)
            }
            res = self._s.post(
                self.collection_links['uploadedfiles'],
                files=files,
                headers={
                    'Accept': 'application/vnd.collection+json',
                    'Content-Type': None
                }
            )
        res.raise_for_status()
        return res.json()

    def _url2plugin(self, url):
        res = self._s.get(url)
        res.raise_for_status()
        return Plugin(**res.json(), session=self._s)

    def get_plugin(self, name_exact='', version='', url='') -> Plugin:
        """
        Get a single plugin, either searching for it by its exact name, or by URL.
        :param name_exact: name of plugin
        :param version: (optional) version of plugin
        :param url: (alternative to name_exact) url of plugin
        :return:
        """
        if name_exact:
            search = self.search_plugin(name_exact, version)
            return search.pop()
        elif url:
            return self._url2plugin(url)
        else:
            raise ValueError('Must give either plugin name or url')

    def search_plugin(self, name_exact: str, version: '') -> Set[Plugin]:
        payload = {
            'name_exact': name_exact
        }
        if version:
            payload['version'] = version
        res = self._s.get(self.search_addr_plugins, params=payload)
        res.raise_for_status()
        data = res.json()
        if data['count'] < 1:
            raise PluginNotFoundError(name_exact)
        return set(Plugin(**pldata, session=self._s) for pldata in data['results'])

    def get_plugin_instance(self, id: Union[int, str]):
        """
        Get a plugin instance.
        :param id: Either a plugin instance ID or URL
        :return: plugin instance
        """
        res = self._s.get(id if '/' in id else f'{self.addr}plugins/instances/{id}/')
        res.raise_for_status()
        return PluginInstance(**res.json())

    def run(self, plugin_name='', plugin_url='', plugin: Optional[PluginInstance] = None,
            params: Optional[dict] = None) -> PluginInstance:
        """
        Create a plugin instance. Either procide a plugin object,
        or search for a plugin by name or URL.
        :param plugin: plugin to run
        :param plugin_name: name of plugin to run
        :param plugin_url: alternatively specify plugin URL
        :param params: plugin parameters as key-value pairs (not collection+json)
        :return:
        """
        if not plugin:
            plugin = self.get_plugin(name_exact=plugin_name, url=plugin_url)
        return plugin.create_instance(params)

    def get_uploadedfile(self, fname='', fname_exact=''):
        query = {}
        if fname:
            query['fname'] = fname
        if fname_exact:
            query['fname_exact'] = fname_exact

        res = self._s.get(self.collection_links['uploadedfiles'] + 'search/', params=query).json()
        return res['results']

    def search_pipelines(self, name='') -> Set[Pipeline]:
        payload = {
            'name': name
        }
        res = self._s.get(self.collection_links['pipelines'] + 'search/', params=payload)
        res.raise_for_status()
        data = res.json()
        return set(Pipeline(**p, session=self._s) for p in data['results'])

    def get_pipeline(self, name: str) -> Pipeline:
        search = self.search_pipelines(name)
        if not search:
            raise PipelineNotFoundError(name)
        return search.pop()
