# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NetworkInterfaceAttachmentArgs', 'NetworkInterfaceAttachment']

@pulumi.input_type
class NetworkInterfaceAttachmentArgs:
    def __init__(__self__, *,
                 instance_id: pulumi.Input[str],
                 network_interface_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a NetworkInterfaceAttachment resource.
        :param pulumi.Input[str] instance_id: The instance ID to attach.
        :param pulumi.Input[str] network_interface_id: The ENI ID to attach.
        """
        pulumi.set(__self__, "instance_id", instance_id)
        pulumi.set(__self__, "network_interface_id", network_interface_id)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        The instance ID to attach.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Input[str]:
        """
        The ENI ID to attach.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "network_interface_id", value)


@pulumi.input_type
class _NetworkInterfaceAttachmentState:
    def __init__(__self__, *,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NetworkInterfaceAttachment resources.
        :param pulumi.Input[str] instance_id: The instance ID to attach.
        :param pulumi.Input[str] network_interface_id: The ENI ID to attach.
        """
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if network_interface_id is not None:
            pulumi.set(__self__, "network_interface_id", network_interface_id)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The instance ID to attach.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ENI ID to attach.
        """
        return pulumi.get(self, "network_interface_id")

    @network_interface_id.setter
    def network_interface_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "network_interface_id", value)


class NetworkInterfaceAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Alicloud ECS Elastic Network Interface Attachment as a resource to attach ENI to or detach ENI from ECS Instances.

        For information about Elastic Network Interface and how to use it, see [Elastic Network Interface](https://www.alibabacloud.com/help/doc-detail/58496.html).

        ## Example Usage

        Bacis Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "networkInterfaceAttachment"
        number = config.get("number")
        if number is None:
            number = "2"
        vpc = alicloud.vpc.Network("vpc", cidr_block="192.168.0.0/24")
        default_zones = alicloud.get_zones(available_resource_creation="VSwitch")
        vswitch = alicloud.vpc.Switch("vswitch",
            vswitch_name=name,
            cidr_block="192.168.0.0/24",
            availability_zone=default_zones.zones[0].id,
            vpc_id=vpc.id)
        group = alicloud.ecs.SecurityGroup("group", vpc_id=vpc.id)
        instance_type = alicloud.ecs.get_instance_types(availability_zone=default_zones.zones[0].id,
            eni_amount=2)
        default_images = alicloud.ecs.get_images(name_regex="^ubuntu_18.*64",
            most_recent=True,
            owners="system")
        instance = []
        for range in [{"value": i} for i in range(0, number)]:
            instance.append(alicloud.ecs.Instance(f"instance-{range['value']}",
                availability_zone=default_zones.zones[0].id,
                security_groups=[group.id],
                instance_type=instance_type.instance_types[0].id,
                system_disk_category="cloud_efficiency",
                image_id=default_images.images[0].id,
                instance_name=name,
                vswitch_id=vswitch.id,
                internet_max_bandwidth_out=10))
        interface = []
        for range in [{"value": i} for i in range(0, number)]:
            interface.append(alicloud.vpc.NetworkInterface(f"interface-{range['value']}",
                vswitch_id=vswitch.id,
                security_groups=[group.id]))
        attachment = []
        for range in [{"value": i} for i in range(0, number)]:
            attachment.append(alicloud.vpc.NetworkInterfaceAttachment(f"attachment-{range['value']}",
                instance_id=[__item.id for __item in instance][range["index"]],
                network_interface_id=[__item.id for __item in interface][range["index"]]))
        ```

        ## Import

        Network Interfaces Attachment resource can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/networkInterfaceAttachment:NetworkInterfaceAttachment eni eni-abc123456789000:i-abc123456789000
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: The instance ID to attach.
        :param pulumi.Input[str] network_interface_id: The ENI ID to attach.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NetworkInterfaceAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Alicloud ECS Elastic Network Interface Attachment as a resource to attach ENI to or detach ENI from ECS Instances.

        For information about Elastic Network Interface and how to use it, see [Elastic Network Interface](https://www.alibabacloud.com/help/doc-detail/58496.html).

        ## Example Usage

        Bacis Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "networkInterfaceAttachment"
        number = config.get("number")
        if number is None:
            number = "2"
        vpc = alicloud.vpc.Network("vpc", cidr_block="192.168.0.0/24")
        default_zones = alicloud.get_zones(available_resource_creation="VSwitch")
        vswitch = alicloud.vpc.Switch("vswitch",
            vswitch_name=name,
            cidr_block="192.168.0.0/24",
            availability_zone=default_zones.zones[0].id,
            vpc_id=vpc.id)
        group = alicloud.ecs.SecurityGroup("group", vpc_id=vpc.id)
        instance_type = alicloud.ecs.get_instance_types(availability_zone=default_zones.zones[0].id,
            eni_amount=2)
        default_images = alicloud.ecs.get_images(name_regex="^ubuntu_18.*64",
            most_recent=True,
            owners="system")
        instance = []
        for range in [{"value": i} for i in range(0, number)]:
            instance.append(alicloud.ecs.Instance(f"instance-{range['value']}",
                availability_zone=default_zones.zones[0].id,
                security_groups=[group.id],
                instance_type=instance_type.instance_types[0].id,
                system_disk_category="cloud_efficiency",
                image_id=default_images.images[0].id,
                instance_name=name,
                vswitch_id=vswitch.id,
                internet_max_bandwidth_out=10))
        interface = []
        for range in [{"value": i} for i in range(0, number)]:
            interface.append(alicloud.vpc.NetworkInterface(f"interface-{range['value']}",
                vswitch_id=vswitch.id,
                security_groups=[group.id]))
        attachment = []
        for range in [{"value": i} for i in range(0, number)]:
            attachment.append(alicloud.vpc.NetworkInterfaceAttachment(f"attachment-{range['value']}",
                instance_id=[__item.id for __item in instance][range["index"]],
                network_interface_id=[__item.id for __item in interface][range["index"]]))
        ```

        ## Import

        Network Interfaces Attachment resource can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:vpc/networkInterfaceAttachment:NetworkInterfaceAttachment eni eni-abc123456789000:i-abc123456789000
        ```

        :param str resource_name: The name of the resource.
        :param NetworkInterfaceAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NetworkInterfaceAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 network_interface_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = NetworkInterfaceAttachmentArgs.__new__(NetworkInterfaceAttachmentArgs)

            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            if network_interface_id is None and not opts.urn:
                raise TypeError("Missing required property 'network_interface_id'")
            __props__.__dict__["network_interface_id"] = network_interface_id
        super(NetworkInterfaceAttachment, __self__).__init__(
            'alicloud:vpc/networkInterfaceAttachment:NetworkInterfaceAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            network_interface_id: Optional[pulumi.Input[str]] = None) -> 'NetworkInterfaceAttachment':
        """
        Get an existing NetworkInterfaceAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] instance_id: The instance ID to attach.
        :param pulumi.Input[str] network_interface_id: The ENI ID to attach.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NetworkInterfaceAttachmentState.__new__(_NetworkInterfaceAttachmentState)

        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["network_interface_id"] = network_interface_id
        return NetworkInterfaceAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The instance ID to attach.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter(name="networkInterfaceId")
    def network_interface_id(self) -> pulumi.Output[str]:
        """
        The ENI ID to attach.
        """
        return pulumi.get(self, "network_interface_id")

