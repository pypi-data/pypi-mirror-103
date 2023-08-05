# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .b2_c_tenant import *
from .get_b2_c_tenant import *
from .get_guest_usage import *
from .guest_usage import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    v20190101preview,
    v20200501preview,
)

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "azure-native:azureactivedirectory:B2CTenant":
                return B2CTenant(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:azureactivedirectory:GuestUsage":
                return GuestUsage(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "azureactivedirectory", _module_instance)

_register_module()
