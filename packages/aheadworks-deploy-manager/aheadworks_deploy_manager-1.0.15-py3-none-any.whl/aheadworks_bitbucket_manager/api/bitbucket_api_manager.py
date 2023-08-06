import json

from aheadworks_bitbucket_manager.model.http.api_request import ApiRequest as Api
from typing import Optional


class BitbucketApiManager:
    """api manager for bitbucket"""

    def __init__(self, bitbucket_config):
        self.config = bitbucket_config
        self.request = Api(config=self.config)

    def get_build_by_commit(self, commit_hash: str):
        """
        :param commit_hash: str
        :return: build number: int
        :raises Exception: Сommit hash should not be less than 6 symbols.
        """
        if len(commit_hash) < 6:
            raise Exception('Сommit hash should not be less than 6 symbols.')

        build = self.get_build_number(commit_hash=commit_hash)
        if build is None:
            commit = self.get_commit(commit_hash=commit_hash)
            list_of_parents_build_number = list()
            for _ in commit['parents']:
                commit_hash = _['hash']
                list_of_parents_build_number.append(self.get_build_by_commit(commit_hash))
            build = max(list_of_parents_build_number)

        return build

    def get_build_number(self, commit_hash: str):
        """get bitbucket bld number by commit

        :param commit_hash: bitbucket commit hash, full or short
        :return: build number
        """
        build_number = None
        deploys = self.get_deployments()

        for deploy in deploys['values']:
            pipeline_uuid = deploy['deployable']['pipeline']['uuid']
            if deploy['release']['commit']['hash'].find(commit_hash) == 0:
                pipeline = self.get_pipeline(pipeline_uuid)
                pipeline_commit_hash: Optional[str] = pipeline['target']['commit']['hash']
                if pipeline_commit_hash.find(commit_hash) == 0:
                    build_number = pipeline['build_number']

        return build_number

    def get_commit(self, commit_hash: str, config=None):
        if config is None:
            config = self.config
        commit = self.request.get(location='/2.0/repositories/{}/{}/commit/{}'.format(
            config.bitbucket_workspace,
            config.bitbucket_repo_slug,
            commit_hash))
        return json.loads(commit)

    def get_pipeline(self, pipeline_uuid):
        pipeline = self.request.get(location='/2.0/repositories/{}/{}/pipelines/{}'.format(
            self.config.bitbucket_workspace,
            self.config.bitbucket_repo_slug,
            pipeline_uuid))
        return json.loads(pipeline)

    def get_deployments(self, params=None):
        if params is None:
            params = {'pagelen': '100'}
        deploys = self.request.get(location='/2.0/repositories/{}/{}/deployments/'.format(
            self.config.bitbucket_workspace,
            self.config.bitbucket_repo_slug
            ), params=params
        )
        result = json.loads(deploys)
        if 'next' in result.keys():
            query = result['next'].split('?')[1]
            params = {}
            for _ in query.split('&'):
                params[_.split('=')[0]] = _.split('=')[1]
            result['values'].extend(self.get_deployments(params=params)['values'])
        return result
