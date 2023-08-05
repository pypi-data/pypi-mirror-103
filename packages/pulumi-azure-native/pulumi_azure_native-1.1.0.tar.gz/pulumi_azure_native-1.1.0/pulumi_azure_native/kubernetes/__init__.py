# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .connected_cluster import *
from .get_connected_cluster import *
from .list_connected_cluster_user_credentials import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    v20200101preview,
    v20210301,
    v20210401preview,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-native:kubernetes:ConnectedCluster":
                return ConnectedCluster(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "kubernetes", _module_instance)

_register_module()
