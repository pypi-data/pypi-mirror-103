# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .consumer_group import *
from .instance import *
from .sasl_acl import *
from .sasl_user import *
from .topic import *

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "alicloud:alikafka/consumerGroup:ConsumerGroup":
                return ConsumerGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:alikafka/instance:Instance":
                return Instance(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:alikafka/saslAcl:SaslAcl":
                return SaslAcl(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:alikafka/saslUser:SaslUser":
                return SaslUser(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:alikafka/topic:Topic":
                return Topic(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("alicloud", "alikafka/consumerGroup", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "alikafka/instance", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "alikafka/saslAcl", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "alikafka/saslUser", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "alikafka/topic", _module_instance)

_register_module()
