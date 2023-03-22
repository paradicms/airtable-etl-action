#!/usr/bin/env python3
import dataclasses
from dataclasses import dataclass
from urllib.parse import urlparse

from paradicms_etl.extractors.costume_core_data_airtable_extractor import (
    CostumeCoreDataAirtableExtractor,
)
from paradicms_etl.pipeline import Pipeline
from paradicms_etl.transformers.costume_core_data_airtable_transformer import (
    CostumeCoreDataAirtableTransformer,
)
from paradicms_ssg.github_action import GitHubAction
from paradicms_ssg.github_action_inputs import GitHubActionInputs


@dataclass(frozen=True)
class _Inputs(GitHubActionInputs):
    airtable_access_token: str = dataclasses.field(
        default=GitHubActionInputs.REQUIRED,
        metadata={
            "description": "Airtable access token (not API key), see https://support.airtable.com/docs/creating-and-using-api-keys-and-access-tokens"
        },
    )
    airtable_base: str = dataclasses.field(
        default=GitHubActionInputs.REQUIRED,
        metadata={
            "description": "Airtable base id such as appgU92SdGTwPIVNg or a full Airtable base URL such as https://airtable.com/appgU92SdGTwPIVNg"
        },
    )
    profile: str = dataclasses.field(
        default="costume_core",
        metadata={
            "description": "Application profile of the data/metadata in the Airtable metadata, one of: costume_core"
        },
    )


class Action(GitHubAction[_Inputs]):
    """
    Generate a static site from a Paradicms-formatted Airtable base.
    """

    @classmethod
    @property
    def _inputs_class(cls):
        return _Inputs

    def _run(self):
        airtable_base_id = self._inputs.airtable_base
        try:
            airtable_base_url = urlparse(self._inputs.airtable_base)
            if airtable_base_url.hostname == "airtable.com":
                airtable_base_id = airtable_base_url.path.split("/")[1]
        except (IndexError, ValueError):
            pass

        profile = self._inputs.profile.lower()
        if profile == "costume_core":
            extractor = CostumeCoreDataAirtableExtractor(
                access_token=self._inputs.airtable_access_token,
                base_id=airtable_base_id,
                extracted_data_dir_path=self._extracted_data_dir_path,
            )
            transformer = CostumeCoreDataAirtableTransformer()
        else:
            raise NotImplementedError(f"profile: {profile}")

        Pipeline(
            extractor=extractor,
            id=self._inputs.pipeline_id,
            loader=self._create_loader(),
            transformer=transformer,
        ).extract_transform_load()


if __name__ == "__main__":
    Action.main()
