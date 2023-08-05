# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['InstanceAttachmentArgs', 'InstanceAttachment']

@pulumi.input_type
class InstanceAttachmentArgs:
    def __init__(__self__, *,
                 child_instance_id: pulumi.Input[str],
                 child_instance_region_id: pulumi.Input[str],
                 child_instance_type: pulumi.Input[str],
                 instance_id: pulumi.Input[str],
                 cen_owner_id: Optional[pulumi.Input[int]] = None,
                 child_instance_owner_id: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a InstanceAttachment resource.
        :param pulumi.Input[str] child_instance_id: The ID of the child instance to attach.
        :param pulumi.Input[str] child_instance_region_id: The region ID of the child instance to attach.
        :param pulumi.Input[str] child_instance_type: The type of the associated network. Valid values: `VPC`, `VBR` and `CCN`.
        :param pulumi.Input[str] instance_id: The ID of the CEN.
        :param pulumi.Input[int] cen_owner_id: The account ID to which the CEN instance belongs.
        :param pulumi.Input[int] child_instance_owner_id: The uid of the child instance. Only used when attach a child instance of other account.
        """
        pulumi.set(__self__, "child_instance_id", child_instance_id)
        pulumi.set(__self__, "child_instance_region_id", child_instance_region_id)
        pulumi.set(__self__, "child_instance_type", child_instance_type)
        pulumi.set(__self__, "instance_id", instance_id)
        if cen_owner_id is not None:
            pulumi.set(__self__, "cen_owner_id", cen_owner_id)
        if child_instance_owner_id is not None:
            pulumi.set(__self__, "child_instance_owner_id", child_instance_owner_id)

    @property
    @pulumi.getter(name="childInstanceId")
    def child_instance_id(self) -> pulumi.Input[str]:
        """
        The ID of the child instance to attach.
        """
        return pulumi.get(self, "child_instance_id")

    @child_instance_id.setter
    def child_instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "child_instance_id", value)

    @property
    @pulumi.getter(name="childInstanceRegionId")
    def child_instance_region_id(self) -> pulumi.Input[str]:
        """
        The region ID of the child instance to attach.
        """
        return pulumi.get(self, "child_instance_region_id")

    @child_instance_region_id.setter
    def child_instance_region_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "child_instance_region_id", value)

    @property
    @pulumi.getter(name="childInstanceType")
    def child_instance_type(self) -> pulumi.Input[str]:
        """
        The type of the associated network. Valid values: `VPC`, `VBR` and `CCN`.
        """
        return pulumi.get(self, "child_instance_type")

    @child_instance_type.setter
    def child_instance_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "child_instance_type", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Input[str]:
        """
        The ID of the CEN.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter(name="cenOwnerId")
    def cen_owner_id(self) -> Optional[pulumi.Input[int]]:
        """
        The account ID to which the CEN instance belongs.
        """
        return pulumi.get(self, "cen_owner_id")

    @cen_owner_id.setter
    def cen_owner_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cen_owner_id", value)

    @property
    @pulumi.getter(name="childInstanceOwnerId")
    def child_instance_owner_id(self) -> Optional[pulumi.Input[int]]:
        """
        The uid of the child instance. Only used when attach a child instance of other account.
        """
        return pulumi.get(self, "child_instance_owner_id")

    @child_instance_owner_id.setter
    def child_instance_owner_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "child_instance_owner_id", value)


@pulumi.input_type
class _InstanceAttachmentState:
    def __init__(__self__, *,
                 cen_owner_id: Optional[pulumi.Input[int]] = None,
                 child_instance_id: Optional[pulumi.Input[str]] = None,
                 child_instance_owner_id: Optional[pulumi.Input[int]] = None,
                 child_instance_region_id: Optional[pulumi.Input[str]] = None,
                 child_instance_type: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 status: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering InstanceAttachment resources.
        :param pulumi.Input[int] cen_owner_id: The account ID to which the CEN instance belongs.
        :param pulumi.Input[str] child_instance_id: The ID of the child instance to attach.
        :param pulumi.Input[int] child_instance_owner_id: The uid of the child instance. Only used when attach a child instance of other account.
        :param pulumi.Input[str] child_instance_region_id: The region ID of the child instance to attach.
        :param pulumi.Input[str] child_instance_type: The type of the associated network. Valid values: `VPC`, `VBR` and `CCN`.
        :param pulumi.Input[str] instance_id: The ID of the CEN.
        :param pulumi.Input[str] status: The associating status of the network.
        """
        if cen_owner_id is not None:
            pulumi.set(__self__, "cen_owner_id", cen_owner_id)
        if child_instance_id is not None:
            pulumi.set(__self__, "child_instance_id", child_instance_id)
        if child_instance_owner_id is not None:
            pulumi.set(__self__, "child_instance_owner_id", child_instance_owner_id)
        if child_instance_region_id is not None:
            pulumi.set(__self__, "child_instance_region_id", child_instance_region_id)
        if child_instance_type is not None:
            pulumi.set(__self__, "child_instance_type", child_instance_type)
        if instance_id is not None:
            pulumi.set(__self__, "instance_id", instance_id)
        if status is not None:
            pulumi.set(__self__, "status", status)

    @property
    @pulumi.getter(name="cenOwnerId")
    def cen_owner_id(self) -> Optional[pulumi.Input[int]]:
        """
        The account ID to which the CEN instance belongs.
        """
        return pulumi.get(self, "cen_owner_id")

    @cen_owner_id.setter
    def cen_owner_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "cen_owner_id", value)

    @property
    @pulumi.getter(name="childInstanceId")
    def child_instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the child instance to attach.
        """
        return pulumi.get(self, "child_instance_id")

    @child_instance_id.setter
    def child_instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "child_instance_id", value)

    @property
    @pulumi.getter(name="childInstanceOwnerId")
    def child_instance_owner_id(self) -> Optional[pulumi.Input[int]]:
        """
        The uid of the child instance. Only used when attach a child instance of other account.
        """
        return pulumi.get(self, "child_instance_owner_id")

    @child_instance_owner_id.setter
    def child_instance_owner_id(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "child_instance_owner_id", value)

    @property
    @pulumi.getter(name="childInstanceRegionId")
    def child_instance_region_id(self) -> Optional[pulumi.Input[str]]:
        """
        The region ID of the child instance to attach.
        """
        return pulumi.get(self, "child_instance_region_id")

    @child_instance_region_id.setter
    def child_instance_region_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "child_instance_region_id", value)

    @property
    @pulumi.getter(name="childInstanceType")
    def child_instance_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of the associated network. Valid values: `VPC`, `VBR` and `CCN`.
        """
        return pulumi.get(self, "child_instance_type")

    @child_instance_type.setter
    def child_instance_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "child_instance_type", value)

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> Optional[pulumi.Input[str]]:
        """
        The ID of the CEN.
        """
        return pulumi.get(self, "instance_id")

    @instance_id.setter
    def instance_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "instance_id", value)

    @property
    @pulumi.getter
    def status(self) -> Optional[pulumi.Input[str]]:
        """
        The associating status of the network.
        """
        return pulumi.get(self, "status")

    @status.setter
    def status(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "status", value)


class InstanceAttachment(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cen_owner_id: Optional[pulumi.Input[int]] = None,
                 child_instance_id: Optional[pulumi.Input[str]] = None,
                 child_instance_owner_id: Optional[pulumi.Input[int]] = None,
                 child_instance_region_id: Optional[pulumi.Input[str]] = None,
                 child_instance_type: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a CEN child instance attachment resource that associate the network(VPC, CCN, VBR) with the CEN instance.

        ->**NOTE:** Available in 1.42.0+

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-testAccCenInstanceAttachmentBasic"
        cen = alicloud.cen.Instance("cen", description="terraform01")
        vpc = alicloud.vpc.Network("vpc", cidr_block="192.168.0.0/16")
        foo = alicloud.cen.InstanceAttachment("foo",
            instance_id=cen.id,
            child_instance_id=vpc.id,
            child_instance_type="VPC",
            child_instance_region_id="cn-beijing")
        ```

        ## Import

        CEN instance can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cen/instanceAttachment:InstanceAttachment example cen-m7i7pjmkon********:vpc-2ze2w07mcy9nz********:VPC:cn-beijing
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] cen_owner_id: The account ID to which the CEN instance belongs.
        :param pulumi.Input[str] child_instance_id: The ID of the child instance to attach.
        :param pulumi.Input[int] child_instance_owner_id: The uid of the child instance. Only used when attach a child instance of other account.
        :param pulumi.Input[str] child_instance_region_id: The region ID of the child instance to attach.
        :param pulumi.Input[str] child_instance_type: The type of the associated network. Valid values: `VPC`, `VBR` and `CCN`.
        :param pulumi.Input[str] instance_id: The ID of the CEN.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: InstanceAttachmentArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a CEN child instance attachment resource that associate the network(VPC, CCN, VBR) with the CEN instance.

        ->**NOTE:** Available in 1.42.0+

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        config = pulumi.Config()
        name = config.get("name")
        if name is None:
            name = "tf-testAccCenInstanceAttachmentBasic"
        cen = alicloud.cen.Instance("cen", description="terraform01")
        vpc = alicloud.vpc.Network("vpc", cidr_block="192.168.0.0/16")
        foo = alicloud.cen.InstanceAttachment("foo",
            instance_id=cen.id,
            child_instance_id=vpc.id,
            child_instance_type="VPC",
            child_instance_region_id="cn-beijing")
        ```

        ## Import

        CEN instance can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cen/instanceAttachment:InstanceAttachment example cen-m7i7pjmkon********:vpc-2ze2w07mcy9nz********:VPC:cn-beijing
        ```

        :param str resource_name: The name of the resource.
        :param InstanceAttachmentArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(InstanceAttachmentArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cen_owner_id: Optional[pulumi.Input[int]] = None,
                 child_instance_id: Optional[pulumi.Input[str]] = None,
                 child_instance_owner_id: Optional[pulumi.Input[int]] = None,
                 child_instance_region_id: Optional[pulumi.Input[str]] = None,
                 child_instance_type: Optional[pulumi.Input[str]] = None,
                 instance_id: Optional[pulumi.Input[str]] = None,
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
            __props__ = InstanceAttachmentArgs.__new__(InstanceAttachmentArgs)

            __props__.__dict__["cen_owner_id"] = cen_owner_id
            if child_instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'child_instance_id'")
            __props__.__dict__["child_instance_id"] = child_instance_id
            __props__.__dict__["child_instance_owner_id"] = child_instance_owner_id
            if child_instance_region_id is None and not opts.urn:
                raise TypeError("Missing required property 'child_instance_region_id'")
            __props__.__dict__["child_instance_region_id"] = child_instance_region_id
            if child_instance_type is None and not opts.urn:
                raise TypeError("Missing required property 'child_instance_type'")
            __props__.__dict__["child_instance_type"] = child_instance_type
            if instance_id is None and not opts.urn:
                raise TypeError("Missing required property 'instance_id'")
            __props__.__dict__["instance_id"] = instance_id
            __props__.__dict__["status"] = None
        super(InstanceAttachment, __self__).__init__(
            'alicloud:cen/instanceAttachment:InstanceAttachment',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cen_owner_id: Optional[pulumi.Input[int]] = None,
            child_instance_id: Optional[pulumi.Input[str]] = None,
            child_instance_owner_id: Optional[pulumi.Input[int]] = None,
            child_instance_region_id: Optional[pulumi.Input[str]] = None,
            child_instance_type: Optional[pulumi.Input[str]] = None,
            instance_id: Optional[pulumi.Input[str]] = None,
            status: Optional[pulumi.Input[str]] = None) -> 'InstanceAttachment':
        """
        Get an existing InstanceAttachment resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[int] cen_owner_id: The account ID to which the CEN instance belongs.
        :param pulumi.Input[str] child_instance_id: The ID of the child instance to attach.
        :param pulumi.Input[int] child_instance_owner_id: The uid of the child instance. Only used when attach a child instance of other account.
        :param pulumi.Input[str] child_instance_region_id: The region ID of the child instance to attach.
        :param pulumi.Input[str] child_instance_type: The type of the associated network. Valid values: `VPC`, `VBR` and `CCN`.
        :param pulumi.Input[str] instance_id: The ID of the CEN.
        :param pulumi.Input[str] status: The associating status of the network.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _InstanceAttachmentState.__new__(_InstanceAttachmentState)

        __props__.__dict__["cen_owner_id"] = cen_owner_id
        __props__.__dict__["child_instance_id"] = child_instance_id
        __props__.__dict__["child_instance_owner_id"] = child_instance_owner_id
        __props__.__dict__["child_instance_region_id"] = child_instance_region_id
        __props__.__dict__["child_instance_type"] = child_instance_type
        __props__.__dict__["instance_id"] = instance_id
        __props__.__dict__["status"] = status
        return InstanceAttachment(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="cenOwnerId")
    def cen_owner_id(self) -> pulumi.Output[Optional[int]]:
        """
        The account ID to which the CEN instance belongs.
        """
        return pulumi.get(self, "cen_owner_id")

    @property
    @pulumi.getter(name="childInstanceId")
    def child_instance_id(self) -> pulumi.Output[str]:
        """
        The ID of the child instance to attach.
        """
        return pulumi.get(self, "child_instance_id")

    @property
    @pulumi.getter(name="childInstanceOwnerId")
    def child_instance_owner_id(self) -> pulumi.Output[int]:
        """
        The uid of the child instance. Only used when attach a child instance of other account.
        """
        return pulumi.get(self, "child_instance_owner_id")

    @property
    @pulumi.getter(name="childInstanceRegionId")
    def child_instance_region_id(self) -> pulumi.Output[str]:
        """
        The region ID of the child instance to attach.
        """
        return pulumi.get(self, "child_instance_region_id")

    @property
    @pulumi.getter(name="childInstanceType")
    def child_instance_type(self) -> pulumi.Output[str]:
        """
        The type of the associated network. Valid values: `VPC`, `VBR` and `CCN`.
        """
        return pulumi.get(self, "child_instance_type")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> pulumi.Output[str]:
        """
        The ID of the CEN.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def status(self) -> pulumi.Output[str]:
        """
        The associating status of the network.
        """
        return pulumi.get(self, "status")

