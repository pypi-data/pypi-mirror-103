# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from ._enums import *

__all__ = [
    'ConfigurationIdentityArgs',
    'ExtensionStatusArgs',
    'HelmOperatorPropertiesArgs',
    'ScopeArgs',
    'ScopeClusterArgs',
    'ScopeNamespaceArgs',
]

@pulumi.input_type
class ConfigurationIdentityArgs:
    def __init__(__self__, *,
                 type: Optional[pulumi.Input['ResourceIdentityType']] = None):
        """
        Identity for the managed cluster.
        :param pulumi.Input['ResourceIdentityType'] type: The type of identity used for the configuration. Type 'SystemAssigned' will use an implicitly created identity. Type 'None' will not use Managed Identity for the configuration.
        """
        if type is not None:
            pulumi.set(__self__, "type", type)

    @property
    @pulumi.getter
    def type(self) -> Optional[pulumi.Input['ResourceIdentityType']]:
        """
        The type of identity used for the configuration. Type 'SystemAssigned' will use an implicitly created identity. Type 'None' will not use Managed Identity for the configuration.
        """
        return pulumi.get(self, "type")

    @type.setter
    def type(self, value: Optional[pulumi.Input['ResourceIdentityType']]):
        pulumi.set(self, "type", value)


@pulumi.input_type
class ExtensionStatusArgs:
    def __init__(__self__, *,
                 code: Optional[pulumi.Input[str]] = None,
                 display_status: Optional[pulumi.Input[str]] = None,
                 level: Optional[pulumi.Input[Union[str, 'LevelType']]] = None,
                 message: Optional[pulumi.Input[str]] = None,
                 time: Optional[pulumi.Input[str]] = None):
        """
        Status from this instance of the extension.
        :param pulumi.Input[str] code: Status code provided by the Extension
        :param pulumi.Input[str] display_status: Short description of status of this instance of the extension.
        :param pulumi.Input[Union[str, 'LevelType']] level: Level of the status.
        :param pulumi.Input[str] message: Detailed message of the status from the Extension instance.
        :param pulumi.Input[str] time: DateLiteral (per ISO8601) noting the time of installation status.
        """
        if code is not None:
            pulumi.set(__self__, "code", code)
        if display_status is not None:
            pulumi.set(__self__, "display_status", display_status)
        if level is None:
            level = 'Information'
        if level is not None:
            pulumi.set(__self__, "level", level)
        if message is not None:
            pulumi.set(__self__, "message", message)
        if time is not None:
            pulumi.set(__self__, "time", time)

    @property
    @pulumi.getter
    def code(self) -> Optional[pulumi.Input[str]]:
        """
        Status code provided by the Extension
        """
        return pulumi.get(self, "code")

    @code.setter
    def code(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "code", value)

    @property
    @pulumi.getter(name="displayStatus")
    def display_status(self) -> Optional[pulumi.Input[str]]:
        """
        Short description of status of this instance of the extension.
        """
        return pulumi.get(self, "display_status")

    @display_status.setter
    def display_status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "display_status", value)

    @property
    @pulumi.getter
    def level(self) -> Optional[pulumi.Input[Union[str, 'LevelType']]]:
        """
        Level of the status.
        """
        return pulumi.get(self, "level")

    @level.setter
    def level(self, value: Optional[pulumi.Input[Union[str, 'LevelType']]]):
        pulumi.set(self, "level", value)

    @property
    @pulumi.getter
    def message(self) -> Optional[pulumi.Input[str]]:
        """
        Detailed message of the status from the Extension instance.
        """
        return pulumi.get(self, "message")

    @message.setter
    def message(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "message", value)

    @property
    @pulumi.getter
    def time(self) -> Optional[pulumi.Input[str]]:
        """
        DateLiteral (per ISO8601) noting the time of installation status.
        """
        return pulumi.get(self, "time")

    @time.setter
    def time(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "time", value)


@pulumi.input_type
class HelmOperatorPropertiesArgs:
    def __init__(__self__, *,
                 chart_values: Optional[pulumi.Input[str]] = None,
                 chart_version: Optional[pulumi.Input[str]] = None):
        """
        Properties for Helm operator.
        :param pulumi.Input[str] chart_values: Values override for the operator Helm chart.
        :param pulumi.Input[str] chart_version: Version of the operator Helm chart.
        """
        if chart_values is not None:
            pulumi.set(__self__, "chart_values", chart_values)
        if chart_version is not None:
            pulumi.set(__self__, "chart_version", chart_version)

    @property
    @pulumi.getter(name="chartValues")
    def chart_values(self) -> Optional[pulumi.Input[str]]:
        """
        Values override for the operator Helm chart.
        """
        return pulumi.get(self, "chart_values")

    @chart_values.setter
    def chart_values(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "chart_values", value)

    @property
    @pulumi.getter(name="chartVersion")
    def chart_version(self) -> Optional[pulumi.Input[str]]:
        """
        Version of the operator Helm chart.
        """
        return pulumi.get(self, "chart_version")

    @chart_version.setter
    def chart_version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "chart_version", value)


@pulumi.input_type
class ScopeArgs:
    def __init__(__self__, *,
                 cluster: Optional[pulumi.Input['ScopeClusterArgs']] = None,
                 namespace: Optional[pulumi.Input['ScopeNamespaceArgs']] = None):
        """
        Scope of the extensionInstance. It can be either Cluster or Namespace; but not both.
        :param pulumi.Input['ScopeClusterArgs'] cluster: Specifies that the scope of the extensionInstance is Cluster
        :param pulumi.Input['ScopeNamespaceArgs'] namespace: Specifies that the scope of the extensionInstance is Namespace
        """
        if cluster is not None:
            pulumi.set(__self__, "cluster", cluster)
        if namespace is not None:
            pulumi.set(__self__, "namespace", namespace)

    @property
    @pulumi.getter
    def cluster(self) -> Optional[pulumi.Input['ScopeClusterArgs']]:
        """
        Specifies that the scope of the extensionInstance is Cluster
        """
        return pulumi.get(self, "cluster")

    @cluster.setter
    def cluster(self, value: Optional[pulumi.Input['ScopeClusterArgs']]):
        pulumi.set(self, "cluster", value)

    @property
    @pulumi.getter
    def namespace(self) -> Optional[pulumi.Input['ScopeNamespaceArgs']]:
        """
        Specifies that the scope of the extensionInstance is Namespace
        """
        return pulumi.get(self, "namespace")

    @namespace.setter
    def namespace(self, value: Optional[pulumi.Input['ScopeNamespaceArgs']]):
        pulumi.set(self, "namespace", value)


@pulumi.input_type
class ScopeClusterArgs:
    def __init__(__self__, *,
                 release_namespace: Optional[pulumi.Input[str]] = None):
        """
        Specifies that the scope of the extensionInstance is Cluster
        :param pulumi.Input[str] release_namespace: Namespace where the extension Release must be placed, for a Cluster scoped extensionInstance.  If this namespace does not exist, it will be created
        """
        if release_namespace is not None:
            pulumi.set(__self__, "release_namespace", release_namespace)

    @property
    @pulumi.getter(name="releaseNamespace")
    def release_namespace(self) -> Optional[pulumi.Input[str]]:
        """
        Namespace where the extension Release must be placed, for a Cluster scoped extensionInstance.  If this namespace does not exist, it will be created
        """
        return pulumi.get(self, "release_namespace")

    @release_namespace.setter
    def release_namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "release_namespace", value)


@pulumi.input_type
class ScopeNamespaceArgs:
    def __init__(__self__, *,
                 target_namespace: Optional[pulumi.Input[str]] = None):
        """
        Specifies that the scope of the extensionInstance is Namespace
        :param pulumi.Input[str] target_namespace: Namespace where the extensionInstance will be created for an Namespace scoped extensionInstance.  If this namespace does not exist, it will be created
        """
        if target_namespace is not None:
            pulumi.set(__self__, "target_namespace", target_namespace)

    @property
    @pulumi.getter(name="targetNamespace")
    def target_namespace(self) -> Optional[pulumi.Input[str]]:
        """
        Namespace where the extensionInstance will be created for an Namespace scoped extensionInstance.  If this namespace does not exist, it will be created
        """
        return pulumi.get(self, "target_namespace")

    @target_namespace.setter
    def target_namespace(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "target_namespace", value)


