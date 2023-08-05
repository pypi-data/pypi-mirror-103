# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .domain import *
from .domain_topic import *
from .event_subscription import *
from .get_domain import *
from .get_domain_topic import *
from .get_event_subscription import *
from .get_event_subscription_full_url import *
from .get_private_endpoint_connection import *
from .get_topic import *
from .list_domain_shared_access_keys import *
from .list_topic_shared_access_keys import *
from .private_endpoint_connection import *
from .topic import *
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
            if typ == "azure-native:eventgrid/v20200601:Domain":
                return Domain(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:eventgrid/v20200601:DomainTopic":
                return DomainTopic(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:eventgrid/v20200601:EventSubscription":
                return EventSubscription(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:eventgrid/v20200601:PrivateEndpointConnection":
                return PrivateEndpointConnection(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:eventgrid/v20200601:Topic":
                return Topic(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "eventgrid/v20200601", _module_instance)

_register_module()
