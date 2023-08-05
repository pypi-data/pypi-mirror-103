# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .asset import *
from .content_key_policy import *
from .get_asset import *
from .get_asset_encryption_key import *
from .get_content_key_policy import *
from .get_content_key_policy_properties_with_secrets import *
from .get_job import *
from .get_live_event import *
from .get_live_output import *
from .get_media_service import *
from .get_streaming_endpoint import *
from .get_streaming_locator import *
from .get_streaming_policy import *
from .get_transform import *
from .job import *
from .list_asset_container_sas import *
from .list_streaming_locator_content_keys import *
from .list_streaming_locator_paths import *
from .live_event import *
from .live_output import *
from .media_service import *
from .streaming_endpoint import *
from .streaming_locator import *
from .streaming_policy import *
from .transform import *
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
            if typ == "azure-native:media/v20180601preview:Asset":
                return Asset(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:media/v20180601preview:ContentKeyPolicy":
                return ContentKeyPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:media/v20180601preview:Job":
                return Job(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:media/v20180601preview:LiveEvent":
                return LiveEvent(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:media/v20180601preview:LiveOutput":
                return LiveOutput(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:media/v20180601preview:MediaService":
                return MediaService(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:media/v20180601preview:StreamingEndpoint":
                return StreamingEndpoint(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:media/v20180601preview:StreamingLocator":
                return StreamingLocator(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:media/v20180601preview:StreamingPolicy":
                return StreamingPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:media/v20180601preview:Transform":
                return Transform(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "media/v20180601preview", _module_instance)

_register_module()
