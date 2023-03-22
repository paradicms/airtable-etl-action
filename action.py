#!/usr/bin/env python3
import dataclasses
from dataclasses import dataclass
from pathlib import Path

from paradicms_etl.extractors.markdown_directory_extractor import (
    MarkdownDirectoryExtractor,
)
from paradicms_etl.pipeline import Pipeline
from paradicms_etl.transformers.markdown_directory_transformer import (
    MarkdownDirectoryTransformer,
)
from paradicms_ssg.github_action import GitHubAction
from paradicms_ssg.github_action_inputs import GitHubActionInputs
from paradicms_ssg.models.root_model_classes_by_name import ROOT_MODEL_CLASSES_BY_NAME


@dataclass(frozen=True)
class _Inputs(GitHubActionInputs):
    markdown_directory_path: str = dataclasses.field(
        default=".",
        metadata={"description": "Path to a directory of Markdown files"},
    )


class Action(GitHubAction[_Inputs]):
    """
    Generate a static site from a Paradicms Markdown directory.
    """

    @classmethod
    @property
    def _inputs_class(cls):
        return _Inputs

    def _run(self):
        Pipeline(
            extractor=MarkdownDirectoryExtractor(
                markdown_directory_path=Path(self._inputs.markdown_directory_path)
            ),
            id=self._inputs.pipeline_id,
            loader=self._create_loader(),
            transformer=MarkdownDirectoryTransformer(
                pipeline_id=self._inputs.pipeline_id,
                root_model_classes_by_name=ROOT_MODEL_CLASSES_BY_NAME,
            ),
        ).extract_transform_load()


if __name__ == "__main__":
    Action.main()
