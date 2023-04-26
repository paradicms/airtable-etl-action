#!/usr/bin/env python3
import dataclasses
from dataclasses import dataclass

from paradicms_etl.etl_github_action import EtlGitHubAction
from paradicms_etl.extractors.costume_core_data_airtable_extractor import (
    CostumeCoreDataAirtableExtractor,
)
from paradicms_etl.pipeline import Pipeline
from paradicms_etl.transformers.costume_core_data_airtable_transformer import (
    CostumeCoreDataAirtableTransformer,
)


class Action(EtlGitHubAction):
    """
    Extract, transform, and load data from a Paradicms-formatted Airtable base.
    """

    @dataclass(frozen=True)
    class Inputs(EtlGitHubAction.Inputs):
        airtable_access_token: str = dataclasses.field(
            default=EtlGitHubAction.Inputs.REQUIRED,
            metadata={
                "description": "Airtable access token (not API key), see https://support.airtable.com/docs/creating-and-using-api-keys-and-access-tokens"
            },
        )
        airtable_base_id: str = dataclasses.field(
            default=EtlGitHubAction.Inputs.REQUIRED,
            metadata={
                "description": "Airtable base id such as appgU92SdGTwPIVNg, see the base API documentation"
            },
        )
        profile: str = dataclasses.field(
            default="costume_core",
            metadata={
                "description": "Application profile of the data/metadata in the Airtable metadata, one of: costume_core"
            },
        )

    def __init__(
        self, *, airtable_access_token: str, airtable_base_id: str, profile: str, **kwds
    ):
        EtlGitHubAction.__init__(self, **kwds)
        self.__airtable_access_token = airtable_access_token
        self.__airtable_base_id = airtable_base_id
        self.__profile = profile.lower()

    def _run(self):
        if self.__profile == "costume_core":
            extractor = CostumeCoreDataAirtableExtractor(
                access_token=self.__airtable_access_token,
                base_id=self.__airtable_base_id,
                cache_dir_path=self._cache_dir_path,
            )
            transformer = CostumeCoreDataAirtableTransformer()
        else:
            raise NotImplementedError(f"profile: {self.__profile}")

        Pipeline(
            extractor=extractor,
            id=self._pipeline_id,
            loader=self._loader,
            transformer=transformer,
        ).extract_transform_load(force_extract=self._force_extract)


if __name__ == "__main__":
    Action.main()
