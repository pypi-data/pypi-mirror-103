# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .get_entity import *
from .get_hierarchy_setting import *
from .get_management_group import *
from .get_management_group_subscription import *
from .hierarchy_setting import *
from .management_group import *
from .management_group_subscription import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    v20171101preview,
    v20180101preview,
    v20180301preview,
    v20191101,
    v20200201,
    v20200501,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-native:management:HierarchySetting":
                return HierarchySetting(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:management:ManagementGroup":
                return ManagementGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:management:ManagementGroupSubscription":
                return ManagementGroupSubscription(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "management", _module_instance)

_register_module()
