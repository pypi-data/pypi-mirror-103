from typing import Optional

from pyrasgo.api.create import Create
from pyrasgo.api.match import Match
from pyrasgo.api.publish import Publish
from pyrasgo.utils.monitoring import track_usage

class RasgoOrchestration():

    def __init__(self, api_key: str):
        self.match = Match(api_key=api_key)
        self.create = Create(api_key=api_key)
        self.publish = Publish(api_key=api_key)

    @track_usage
    def get_featureset_id(self, snowflakeTable: str, fs_name: Optional[str] = None) -> Optional[int]:
            fs = self.match.feature_set(table_name=snowflakeTable, fs_name=fs_name)
            return fs.id if fs else None

    @track_usage
    def publish_features_from_yml(self, yml_file: str, sandbox: Optional[bool] = True, git_repo: Optional[str] = None):
        return self.publish.features_from_yml(yml_file=yml_file, sandbox=sandbox, git_repo=git_repo)

    @track_usage
    def run_stats_for_feature(self, feature_id: int):
        return self.create.feature_stats(feature_id)

    @track_usage
    def run_stats_for_featureset(self, featureset_id: int):
        return self.create.feature_set_stats(featureset_id)