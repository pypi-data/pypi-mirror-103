from pulumi import ResourceOptions
from data_engineering_pulumi_components.aws import Bucket
from data_engineering_pulumi_components.utils import Tagger
from typing import Optional


class PulumiBackendBucket(Bucket):
    def __init__(
        self, name: str, tagger: Tagger, opts: Optional[ResourceOptions] = None
    ) -> None:
        super().__init__(
            name=name + "-pulumi-backend",
            t="data-engineering-pulumi-components:aws:PulumiBackendBucket",
            tagger=tagger,
            versioning={"enabled": True},
            opts=ResourceOptions(protect=True),
        )
