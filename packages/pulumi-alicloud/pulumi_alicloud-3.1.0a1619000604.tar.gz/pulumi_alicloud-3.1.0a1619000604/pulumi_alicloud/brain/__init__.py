# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .get_industrial_pid_loops import *
from .get_industrial_pid_organizations import *
from .get_industrial_pid_projects import *
from .get_industrial_serice import *
from .industrial_pid_loop import *
from .industrial_pid_organization import *
from .industrial_pid_project import *
from . import outputs

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "alicloud:brain/industrialPidLoop:IndustrialPidLoop":
                return IndustrialPidLoop(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:brain/industrialPidOrganization:IndustrialPidOrganization":
                return IndustrialPidOrganization(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:brain/industrialPidProject:IndustrialPidProject":
                return IndustrialPidProject(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("alicloud", "brain/industrialPidLoop", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "brain/industrialPidOrganization", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "brain/industrialPidProject", _module_instance)

_register_module()
