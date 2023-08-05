# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .agent_pool import *
from .get_agent_pool import *
from .get_managed_cluster import *
from .get_private_endpoint_connection import *
from .list_managed_cluster_admin_credentials import *
from .list_managed_cluster_monitoring_user_credentials import *
from .list_managed_cluster_user_credentials import *
from .managed_cluster import *
from .private_endpoint_connection import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from ... import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-native:containerservice/v20200601:AgentPool":
                return AgentPool(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:containerservice/v20200601:ManagedCluster":
                return ManagedCluster(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:containerservice/v20200601:PrivateEndpointConnection":
                return PrivateEndpointConnection(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "containerservice/v20200601", _module_instance)

_register_module()
