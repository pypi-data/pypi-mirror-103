# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = ['NetworkAclAttachmentArgs', 'NetworkAclAttachment']

@pulumi.input_type
class NetworkAclAttachmentArgs:
    def __init__(__self__, *,
                 network_acl_id: pulumi.Input[str],
                 resources: pulumi.Input[Sequence[pulumi.Input['NetworkAclAttachmentResourceArgs']]]):
        """
        The set of arguments for constructing a NetworkAclAttachment resource.
        :param pulumi.Input[str] network_acl_id: The id of the network acl, the field can't be changed.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkAclAttachmentResourceArgs']]] resources: List of the resources associated with the network acl. The details see Block Resources.
        """
        pulumi.set(__self__, "network_acl_id", network_acl_id)
        pulumi.set(__self__, "resources", resources)

    @property
    @pulumi.getter(name="networkAclId")
    def network_acl_id(self) -> pulumi.Input[str]:
        """
        The id of the network acl, the field can't be changed.
        """
        return pulumi.get(self, "network_acl_id")

    @network_acl_id.setter
    def network_acl_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_acl_id", value)

    @property
    @pulumi.getter
    def resources(self) -> pulumi.Input[Sequence[pulumi.Input['NetworkAclAttachmentResourceArgs']]]:
        """
        List of the resources associated with the network acl. The details see Block Resources.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: pulumi.Input[Sequence[pulumi.Input['NetworkAclAttachmentResourceArgs']]]):
        pulumi.set(self, "resources", value)


@pulumi.input_type
class _NetworkAclAttachmentState:
    def __init__(__self__, *,
                 network_acl_id: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkAclAttachmentResourceArgs']]]] = None):
        """
        Input properties used for looking up and filtering NetworkAclAttachment resources.
        :param pulumi.Input[str] network_acl_id: The id of the network acl, the field can't be changed.
        :param pulumi.Input[Sequence[pulumi.Input['NetworkAclAttachmentResourceArgs']]] resources: List of the resources associated with the network acl. The details see Block Resources.
        """
        if network_acl_id is not None:
            pulumi.set(__self__, "network_acl_id", network_acl_id)
        if resources is not None:
            pulumi.set(__self__, "resources", resources)

    @property
    @pulumi.getter(name="networkAclId")
    def network_acl_id(self) -> Optional[pulumi.Input[str]]:
        """
        The id of the network acl, the field can't be changed.
        """
        return pulumi.get(self, "network_acl_id")

    @network_acl_id.setter
    def network_acl_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_acl_id", value)

    @property
    @pulumi.getter
    def resources(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['NetworkAclAttachmentResourceArgs']]]]:
        """
        List of the resources associated with the network acl. The details see Block Resources.
        """
        return pulumi.get(self, "resources")

    @resources.setter
    def resources(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['NetworkAclAttachmentResourceArgs']]]]):
        pulumi.set(self, "resources", value)


class NetworkAclAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 network_acl_id: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkAclAttachmentResourceArgs']]]]] = None,
                 __props__=None):
        """
        Provides a network acl attachment resource to associate network acls to vswitches.

        > **NOTE:** Available in 1.44.0+. Currently, the resource are only available in Hongkong(cn-hongkong), India(ap-south-1), and Indonesia(ap-southeast-1) regions.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "NatGatewayConfigSpec"
        default_zones = alicloud.get_zones(available_resource_creation="VSwitch")
        default_network = alicloud.vpc.Network("defaultNetwork", cidr_block="172.16.0.0/12")
        default_network_acl = alicloud.vpc.NetworkAcl("defaultNetworkAcl", vpc_id=default_network.id)
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=default_network.id,
            cidr_block="172.16.0.0/21",
            availability_zone=default_zones.zones[0].id)
        default_network_acl_attachment = alicloud.vpc.NetworkAclAttachment("defaultNetworkAclAttachment",
            network_acl_id=default_network_acl.id,
            resources=[alicloud.vpc.NetworkAclAttachmentResourceArgs(
                resource_id=default_switch.id,
                resource_type="VSwitch",
            )])
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] network_acl_id: The id of the network acl, the field can't be changed.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkAclAttachmentResourceArgs']]]] resources: List of the resources associated with the network acl. The details see Block Resources.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkAclAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a network acl attachment resource to associate network acls to vswitches.

        > **NOTE:** Available in 1.44.0+. Currently, the resource are only available in Hongkong(cn-hongkong), India(ap-south-1), and Indonesia(ap-southeast-1) regions.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "NatGatewayConfigSpec"
        default_zones = alicloud.get_zones(available_resource_creation="VSwitch")
        default_network = alicloud.vpc.Network("defaultNetwork", cidr_block="172.16.0.0/12")
        default_network_acl = alicloud.vpc.NetworkAcl("defaultNetworkAcl", vpc_id=default_network.id)
        default_switch = alicloud.vpc.Switch("defaultSwitch",
            vpc_id=default_network.id,
            cidr_block="172.16.0.0/21",
            availability_zone=default_zones.zones[0].id)
        default_network_acl_attachment = alicloud.vpc.NetworkAclAttachment("defaultNetworkAclAttachment",
            network_acl_id=default_network_acl.id,
            resources=[alicloud.vpc.NetworkAclAttachmentResourceArgs(
                resource_id=default_switch.id,
                resource_type="VSwitch",
            )])
        ```

        :param str resource_name: The name of the resource.
        :param NetworkAclAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkAclAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 network_acl_id: Optional[pulumi.Input[str]] = None,
                 resources: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkAclAttachmentResourceArgs']]]]] = None,
                 __props__=None):
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NetworkAclAttachmentArgs.__new__(NetworkAclAttachmentArgs)

            if network_acl_id is None and not opts.urn:
                raise TypeError("Missing required property 'network_acl_id'")
            __props__.__dict__["network_acl_id"] = network_acl_id
            if resources is None and not opts.urn:
                raise TypeError("Missing required property 'resources'")
            __props__.__dict__["resources"] = resources
        super(NetworkAclAttachment, __self__).__init__(
            'alicloud:vpc/networkAclAttachment:NetworkAclAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            network_acl_id: Optional[pulumi.Input[str]] = None,
            resources: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkAclAttachmentResourceArgs']]]]] = None) -> 'NetworkAclAttachment':
        """
        Get an existing NetworkAclAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] network_acl_id: The id of the network acl, the field can't be changed.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['NetworkAclAttachmentResourceArgs']]]] resources: List of the resources associated with the network acl. The details see Block Resources.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkAclAttachmentState.__new__(_NetworkAclAttachmentState)

        __props__.__dict__["network_acl_id"] = network_acl_id
        __props__.__dict__["resources"] = resources
        return NetworkAclAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="networkAclId")
    def network_acl_id(self) -> pulumi.Output[str]:
        """
        The id of the network acl, the field can't be changed.
        """
        return pulumi.get(self, "network_acl_id")

    @property
    @pulumi.getter
    def resources(self) -> pulumi.Output[Sequence['outputs.NetworkAclAttachmentResource']]:
        """
        List of the resources associated with the network acl. The details see Block Resources.
        """
        return pulumi.get(self, "resources")

