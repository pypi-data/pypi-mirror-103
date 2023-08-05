# coding=utf-8
# *** WARNING: this file was generated by the Pulumi SDK Generator. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from ._enums import *
from .cluster import *
from .file_server import *
from .get_cluster import *
from .get_file_server import *
from .get_job import *
from .job import *
from .list_cluster_remote_login_information import *
from .list_job_output_files import *
from .list_job_remote_login_information import *
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
            if typ == "azure-native:batchai/v20170901preview:Cluster":
                return Cluster(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:batchai/v20170901preview:FileServer":
                return FileServer(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "azure-native:batchai/v20170901preview:Job":
                return Job(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("azure-native", "batchai/v20170901preview", _module_instance)

_register_module()
