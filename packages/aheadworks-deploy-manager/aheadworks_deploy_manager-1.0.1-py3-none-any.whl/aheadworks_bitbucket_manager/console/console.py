import os
from aheadworks_bitbucket_manager.api.bitbucket_api_manager import BitbucketApiManager
from aheadworks_bitbucket_manager.api.dockerhub_api_manager import DockerhubApiManager
from aheadworks_bitbucket_manager.api.version_control_manager import VersionControlManager
from aheadworks_bitbucket_manager.model.parser.php import Php as PhpParser
from aheadworks_bitbucket_manager.model.data.dockerhub import DockerHubConfig
from aheadworks_bitbucket_manager.model.data.bitbucket import BitbucketConfig


class Console:
    """
    this application needed next env variables
    BITBUCKET_KEY
    BITBUCKET_SECRET
    BITBUCKET_REPO_SLUG
    BITBUCKET_WORKSPACE
    DOCKERHUB_LOGIN
    DOCKERHUB_PASSWORD
    DOCKERHUB_REPO
    """

    def __init__(self):
        docker_hub_config = DockerHubConfig(
            dockerhub_user=os.getenv('DOCKERHUB_LOGIN'),
            dockerhub_password=os.getenv('DOCKERHUB_PASSWORD')
        )
        bitbucket_config = BitbucketConfig(
            bitbucket_key=os.getenv('BITBUCKET_KEY'),
            bitbucket_secret=os.getenv('BITBUCKET_SECRET'),
            bitbucket_workspace=os.getenv('BITBUCKET_WORKSPACE'),
            bitbucket_repo_slug=os.getenv('BITBUCKET_REPO_SLUG')
        )
        self.bitbucket_api_manager = BitbucketApiManager(bitbucket_config)
        self.docker_hub_api_manager = DockerhubApiManager(docker_hub_config, bitbucket_config)
        self.version_control_manager = VersionControlManager()
        self.php_parser = PhpParser()

    def remove_depricated_versions_images(self, repo=None):
        """
        :param repo:
        :return:
        """

        repo = repo or os.getenv('DOCKERHUB_REPO')
        self.docker_hub_api_manager.remove_depricated_versions_images(repo)

    def renew_images_by_tag(self, commit_hash, repo=None):
        """
        :param commit_hash:
        :param repo:
        :return:
        """

        repo = repo or os.getenv('DOCKERHUB_REPO')
        self.docker_hub_api_manager.renew_images_by_tag(self, commit_hash, repo)

    def run_app(
            self,
            path_to_versions,
            path_to_project,
            up_cmd,
            down_exclude_current,
            down_cmd,
            host=None,
            user=None
    ):
        host, user = self._get_default_ssh_cred(host, user)
        self.version_control_manager.run_app(
            path_to_versions,
            path_to_project,
            up_cmd,
            down_exclude_current,
            down_cmd,
            host,
            user
        )

    def modify_env(self, path, template):
        self.version_control_manager.modify_env(path, template)

    def get_version_uid(self, version):
        print(self.version_control_manager.get_version_uid(version))

    def get_traefik_version_query(self, path_to_versions):
        print(self.version_control_manager.get_traefik_version_query(path_to_versions))

    # --priority_type low or --priority_type height
    def get_free_priority(self, label_name, priority_type, host=None, user=None):
        host, user = self._get_default_ssh_cred(host, user)
        print(self.version_control_manager.get_free_priority(label_name, priority_type, host, user))

    def get_free_port(self, host=None, user=None):
        host, user = self._get_default_ssh_cred(host, user)
        print(self.version_control_manager.get_free_port(host, user))

    def get_variable_from_php_file(self, var_name, file):
        print(self.php_parser.get_variable_from_file(var_name, file))

    def _get_default_ssh_cred(self, host, user):
        user = user or os.getenv('HOST_USER') or 'root'
        host = host or os.getenv('HOST')

        return [host, user]
