# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .bot import *
from .bot_connection import *
from .channel import *
from .enterprise_channel import *
from .get_bot import *
from .get_bot_connection import *
from .get_channel import *
from .get_enterprise_channel import *
from .list_bot_connection_service_providers import *
from .list_bot_connection_with_secrets import *
from .list_channel_with_keys import *
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
            if typ == "azure-native:botservice/v20180712:Bot":
                return Bot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:botservice/v20180712:BotConnection":
                return BotConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:botservice/v20180712:Channel":
                return Channel(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:botservice/v20180712:EnterpriseChannel":
                return EnterpriseChannel(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "botservice/v20180712", _module_instance)

_register_module()
