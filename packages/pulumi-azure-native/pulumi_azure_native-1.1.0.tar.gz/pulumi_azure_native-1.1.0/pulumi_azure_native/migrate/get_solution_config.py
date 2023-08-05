# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetSolutionConfigResult',
    'AwaitableGetSolutionConfigResult',
    'get_solution_config',
]

@pulumi.output_type
class GetSolutionConfigResult:
    """
    Class representing the config for the solution in the migrate project.
    """
    def __init__(__self__, publisher_sas_uri=None):
        if publisher_sas_uri and not isinstance(publisher_sas_uri, str):
            raise TypeError("Expected argument 'publisher_sas_uri' to be a str")
        pulumi.set(__self__, "publisher_sas_uri", publisher_sas_uri)

    @property
    @pulumi.getter(name="publisherSasUri")
    def publisher_sas_uri(self) -> Optional[str]:
        """
        Gets or sets the publisher sas uri for the solution.
        """
        return pulumi.get(self, "publisher_sas_uri")


class AwaitableGetSolutionConfigResult(GetSolutionConfigResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetSolutionConfigResult(
            publisher_sas_uri=self.publisher_sas_uri)


def get_solution_config(migrate_project_name: Optional[str] = None,
                        resource_group_name: Optional[str] = None,
                        solution_name: Optional[str] = None,
                        opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetSolutionConfigResult:
    """
    Class representing the config for the solution in the migrate project.
    API Version: 2018-09-01-preview.


    :param str migrate_project_name: Name of the Azure Migrate project.
    :param str resource_group_name: Name of the Azure Resource Group that migrate project is part of.
    :param str solution_name: Unique name of a migration solution within a migrate project.
    """
    __args__ = dict()
    __args__['migrateProjectName'] = migrate_project_name
    __args__['resourceGroupName'] = resource_group_name
    __args__['solutionName'] = solution_name
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('azure-native:migrate:getSolutionConfig', __args__, opts=opts, typ=GetSolutionConfigResult).value

    return AwaitableGetSolutionConfigResult(
        publisher_sas_uri=__ret__.publisher_sas_uri)
