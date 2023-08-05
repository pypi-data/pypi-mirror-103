# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['MonitorGroupArgs', 'MonitorGroup']

@pulumi.input_type
class MonitorGroupArgs:
    def __init__(__self__, *,
                 monitor_group_name: pulumi.Input[str],
                 contact_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        The set of arguments for constructing a MonitorGroup resource.
        :param pulumi.Input[str] monitor_group_name: The name of the application group.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] contact_groups: The alert group to which alert notifications will be sent.
        """
        pulumi.set(__self__, "monitor_group_name", monitor_group_name)
        if contact_groups is not None:
            pulumi.set(__self__, "contact_groups", contact_groups)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="monitorGroupName")
    def monitor_group_name(self) -> pulumi.Input[str]:
        """
        The name of the application group.
        """
        return pulumi.get(self, "monitor_group_name")

    @monitor_group_name.setter
    def monitor_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "monitor_group_name", value)

    @property
    @pulumi.getter(name="contactGroups")
    def contact_groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The alert group to which alert notifications will be sent.
        """
        return pulumi.get(self, "contact_groups")

    @contact_groups.setter
    def contact_groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "contact_groups", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _MonitorGroupState:
    def __init__(__self__, *,
                 contact_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 monitor_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None):
        """
        Input properties used for looking up and filtering MonitorGroup resources.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] contact_groups: The alert group to which alert notifications will be sent.
        :param pulumi.Input[str] monitor_group_name: The name of the application group.
        """
        if contact_groups is not None:
            pulumi.set(__self__, "contact_groups", contact_groups)
        if monitor_group_name is not None:
            pulumi.set(__self__, "monitor_group_name", monitor_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="contactGroups")
    def contact_groups(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The alert group to which alert notifications will be sent.
        """
        return pulumi.get(self, "contact_groups")

    @contact_groups.setter
    def contact_groups(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "contact_groups", value)

    @property
    @pulumi.getter(name="monitorGroupName")
    def monitor_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the application group.
        """
        return pulumi.get(self, "monitor_group_name")

    @monitor_group_name.setter
    def monitor_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "monitor_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "tags", value)


class MonitorGroup(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 contact_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 monitor_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 __props__=None):
        """
        Provides a Cloud Monitor Service Monitor Group resource.

        For information about Cloud Monitor Service Monitor Group and how to use it, see [What is Monitor Group](https://www.alibabacloud.com/help/en/doc-detail/115030.htm).

        > **NOTE:** Available in v1.113.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.cms.MonitorGroup("example", monitor_group_name="tf-testaccmonitorgroup")
        ```

        ## Import

        Cloud Monitor Service Monitor Group can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cms/monitorGroup:MonitorGroup example <id>
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] contact_groups: The alert group to which alert notifications will be sent.
        :param pulumi.Input[str] monitor_group_name: The name of the application group.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MonitorGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Cloud Monitor Service Monitor Group resource.

        For information about Cloud Monitor Service Monitor Group and how to use it, see [What is Monitor Group](https://www.alibabacloud.com/help/en/doc-detail/115030.htm).

        > **NOTE:** Available in v1.113.0+.

        ## Example Usage

        Basic Usage

        ```python
        import pulumi
        import pulumi_alicloud as alicloud

        example = alicloud.cms.MonitorGroup("example", monitor_group_name="tf-testaccmonitorgroup")
        ```

        ## Import

        Cloud Monitor Service Monitor Group can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:cms/monitorGroup:MonitorGroup example <id>
        ```

        :param str resource_name: The name of the resource.
        :param MonitorGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MonitorGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 contact_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 monitor_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, Any]]] = None,
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
            __props__ = MonitorGroupArgs.__new__(MonitorGroupArgs)

            __props__.__dict__["contact_groups"] = contact_groups
            if monitor_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'monitor_group_name'")
            __props__.__dict__["monitor_group_name"] = monitor_group_name
            __props__.__dict__["tags"] = tags
        super(MonitorGroup, __self__).__init__(
            'alicloud:cms/monitorGroup:MonitorGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            contact_groups: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            monitor_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, Any]]] = None) -> 'MonitorGroup':
        """
        Get an existing MonitorGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] contact_groups: The alert group to which alert notifications will be sent.
        :param pulumi.Input[str] monitor_group_name: The name of the application group.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MonitorGroupState.__new__(_MonitorGroupState)

        __props__.__dict__["contact_groups"] = contact_groups
        __props__.__dict__["monitor_group_name"] = monitor_group_name
        __props__.__dict__["tags"] = tags
        return MonitorGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="contactGroups")
    def contact_groups(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The alert group to which alert notifications will be sent.
        """
        return pulumi.get(self, "contact_groups")

    @property
    @pulumi.getter(name="monitorGroupName")
    def monitor_group_name(self) -> pulumi.Output[str]:
        """
        The name of the application group.
        """
        return pulumi.get(self, "monitor_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, Any]]]:
        return pulumi.get(self, "tags")

