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

__all__ = ['StoreArgs', 'Store']

@pulumi.input_type
class StoreArgs:
    def __init__(__self__, *,
                 project: pulumi.Input[str],
                 append_meta: Optional[pulumi.Input[bool]] = None,
                 auto_split: Optional[pulumi.Input[bool]] = None,
                 enable_web_tracking: Optional[pulumi.Input[bool]] = None,
                 max_split_shard_count: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 retention_period: Optional[pulumi.Input[int]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a Store resource.
        :param pulumi.Input[str] project: The project name to the log store belongs.
        :param pulumi.Input[bool] append_meta: Determines whether to append log meta automatically. The meta includes log receive time and client IP address. Default to true.
        :param pulumi.Input[bool] auto_split: Determines whether to automatically split a shard. Default to true.
        :param pulumi.Input[bool] enable_web_tracking: Determines whether to enable Web Tracking. Default false.
        :param pulumi.Input[int] max_split_shard_count: The maximum number of shards for automatic split, which is in the range of 1 to 64. You must specify this parameter when autoSplit is true.
        :param pulumi.Input[str] name: The log store, which is unique in the same project.
        :param pulumi.Input[int] retention_period: The data retention time (in days). Valid values: [1-3650]. Default to 30. Log store data will be stored permanently when the value is "3650".
        :param pulumi.Input[int] shard_count: The number of shards in this log store. Default to 2. You can modify it by "Split" or "Merge" operations. [Refer to details](https://www.alibabacloud.com/help/doc-detail/28976.htm)
        """
        pulumi.set(__self__, "project", project)
        if append_meta is not None:
            pulumi.set(__self__, "append_meta", append_meta)
        if auto_split is not None:
            pulumi.set(__self__, "auto_split", auto_split)
        if enable_web_tracking is not None:
            pulumi.set(__self__, "enable_web_tracking", enable_web_tracking)
        if max_split_shard_count is not None:
            pulumi.set(__self__, "max_split_shard_count", max_split_shard_count)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if retention_period is not None:
            pulumi.set(__self__, "retention_period", retention_period)
        if shard_count is not None:
            pulumi.set(__self__, "shard_count", shard_count)

    @property
    @pulumi.getter
    def project(self) -> pulumi.Input[str]:
        """
        The project name to the log store belongs.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: pulumi.Input[str]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="appendMeta")
    def append_meta(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines whether to append log meta automatically. The meta includes log receive time and client IP address. Default to true.
        """
        return pulumi.get(self, "append_meta")

    @append_meta.setter
    def append_meta(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "append_meta", value)

    @property
    @pulumi.getter(name="autoSplit")
    def auto_split(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines whether to automatically split a shard. Default to true.
        """
        return pulumi.get(self, "auto_split")

    @auto_split.setter
    def auto_split(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_split", value)

    @property
    @pulumi.getter(name="enableWebTracking")
    def enable_web_tracking(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines whether to enable Web Tracking. Default false.
        """
        return pulumi.get(self, "enable_web_tracking")

    @enable_web_tracking.setter
    def enable_web_tracking(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_web_tracking", value)

    @property
    @pulumi.getter(name="maxSplitShardCount")
    def max_split_shard_count(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of shards for automatic split, which is in the range of 1 to 64. You must specify this parameter when autoSplit is true.
        """
        return pulumi.get(self, "max_split_shard_count")

    @max_split_shard_count.setter
    def max_split_shard_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_split_shard_count", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The log store, which is unique in the same project.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> Optional[pulumi.Input[int]]:
        """
        The data retention time (in days). Valid values: [1-3650]. Default to 30. Log store data will be stored permanently when the value is "3650".
        """
        return pulumi.get(self, "retention_period")

    @retention_period.setter
    def retention_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retention_period", value)

    @property
    @pulumi.getter(name="shardCount")
    def shard_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of shards in this log store. Default to 2. You can modify it by "Split" or "Merge" operations. [Refer to details](https://www.alibabacloud.com/help/doc-detail/28976.htm)
        """
        return pulumi.get(self, "shard_count")

    @shard_count.setter
    def shard_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "shard_count", value)


@pulumi.input_type
class _StoreState:
    def __init__(__self__, *,
                 append_meta: Optional[pulumi.Input[bool]] = None,
                 auto_split: Optional[pulumi.Input[bool]] = None,
                 enable_web_tracking: Optional[pulumi.Input[bool]] = None,
                 max_split_shard_count: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 retention_period: Optional[pulumi.Input[int]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None,
                 shards: Optional[pulumi.Input[Sequence[pulumi.Input['StoreShardArgs']]]] = None):
        """
        Input properties used for looking up and filtering Store resources.
        :param pulumi.Input[bool] append_meta: Determines whether to append log meta automatically. The meta includes log receive time and client IP address. Default to true.
        :param pulumi.Input[bool] auto_split: Determines whether to automatically split a shard. Default to true.
        :param pulumi.Input[bool] enable_web_tracking: Determines whether to enable Web Tracking. Default false.
        :param pulumi.Input[int] max_split_shard_count: The maximum number of shards for automatic split, which is in the range of 1 to 64. You must specify this parameter when autoSplit is true.
        :param pulumi.Input[str] name: The log store, which is unique in the same project.
        :param pulumi.Input[str] project: The project name to the log store belongs.
        :param pulumi.Input[int] retention_period: The data retention time (in days). Valid values: [1-3650]. Default to 30. Log store data will be stored permanently when the value is "3650".
        :param pulumi.Input[int] shard_count: The number of shards in this log store. Default to 2. You can modify it by "Split" or "Merge" operations. [Refer to details](https://www.alibabacloud.com/help/doc-detail/28976.htm)
        """
        if append_meta is not None:
            pulumi.set(__self__, "append_meta", append_meta)
        if auto_split is not None:
            pulumi.set(__self__, "auto_split", auto_split)
        if enable_web_tracking is not None:
            pulumi.set(__self__, "enable_web_tracking", enable_web_tracking)
        if max_split_shard_count is not None:
            pulumi.set(__self__, "max_split_shard_count", max_split_shard_count)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if project is not None:
            pulumi.set(__self__, "project", project)
        if retention_period is not None:
            pulumi.set(__self__, "retention_period", retention_period)
        if shard_count is not None:
            pulumi.set(__self__, "shard_count", shard_count)
        if shards is not None:
            pulumi.set(__self__, "shards", shards)

    @property
    @pulumi.getter(name="appendMeta")
    def append_meta(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines whether to append log meta automatically. The meta includes log receive time and client IP address. Default to true.
        """
        return pulumi.get(self, "append_meta")

    @append_meta.setter
    def append_meta(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "append_meta", value)

    @property
    @pulumi.getter(name="autoSplit")
    def auto_split(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines whether to automatically split a shard. Default to true.
        """
        return pulumi.get(self, "auto_split")

    @auto_split.setter
    def auto_split(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_split", value)

    @property
    @pulumi.getter(name="enableWebTracking")
    def enable_web_tracking(self) -> Optional[pulumi.Input[bool]]:
        """
        Determines whether to enable Web Tracking. Default false.
        """
        return pulumi.get(self, "enable_web_tracking")

    @enable_web_tracking.setter
    def enable_web_tracking(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "enable_web_tracking", value)

    @property
    @pulumi.getter(name="maxSplitShardCount")
    def max_split_shard_count(self) -> Optional[pulumi.Input[int]]:
        """
        The maximum number of shards for automatic split, which is in the range of 1 to 64. You must specify this parameter when autoSplit is true.
        """
        return pulumi.get(self, "max_split_shard_count")

    @max_split_shard_count.setter
    def max_split_shard_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "max_split_shard_count", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The log store, which is unique in the same project.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def project(self) -> Optional[pulumi.Input[str]]:
        """
        The project name to the log store belongs.
        """
        return pulumi.get(self, "project")

    @project.setter
    def project(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "project", value)

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> Optional[pulumi.Input[int]]:
        """
        The data retention time (in days). Valid values: [1-3650]. Default to 30. Log store data will be stored permanently when the value is "3650".
        """
        return pulumi.get(self, "retention_period")

    @retention_period.setter
    def retention_period(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "retention_period", value)

    @property
    @pulumi.getter(name="shardCount")
    def shard_count(self) -> Optional[pulumi.Input[int]]:
        """
        The number of shards in this log store. Default to 2. You can modify it by "Split" or "Merge" operations. [Refer to details](https://www.alibabacloud.com/help/doc-detail/28976.htm)
        """
        return pulumi.get(self, "shard_count")

    @shard_count.setter
    def shard_count(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "shard_count", value)

    @property
    @pulumi.getter
    def shards(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['StoreShardArgs']]]]:
        return pulumi.get(self, "shards")

    @shards.setter
    def shards(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['StoreShardArgs']]]]):
        pulumi.set(self, "shards", value)


class Store(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 append_meta: Optional[pulumi.Input[bool]] = None,
                 auto_split: Optional[pulumi.Input[bool]] = None,
                 enable_web_tracking: Optional[pulumi.Input[bool]] = None,
                 max_split_shard_count: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 retention_period: Optional[pulumi.Input[int]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        ## Import

        Log store can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:log/store:Store example tf-log:tf-log-store
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] append_meta: Determines whether to append log meta automatically. The meta includes log receive time and client IP address. Default to true.
        :param pulumi.Input[bool] auto_split: Determines whether to automatically split a shard. Default to true.
        :param pulumi.Input[bool] enable_web_tracking: Determines whether to enable Web Tracking. Default false.
        :param pulumi.Input[int] max_split_shard_count: The maximum number of shards for automatic split, which is in the range of 1 to 64. You must specify this parameter when autoSplit is true.
        :param pulumi.Input[str] name: The log store, which is unique in the same project.
        :param pulumi.Input[str] project: The project name to the log store belongs.
        :param pulumi.Input[int] retention_period: The data retention time (in days). Valid values: [1-3650]. Default to 30. Log store data will be stored permanently when the value is "3650".
        :param pulumi.Input[int] shard_count: The number of shards in this log store. Default to 2. You can modify it by "Split" or "Merge" operations. [Refer to details](https://www.alibabacloud.com/help/doc-detail/28976.htm)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: StoreArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        ## Import

        Log store can be imported using the id, e.g.

        ```sh
         $ pulumi import alicloud:log/store:Store example tf-log:tf-log-store
        ```

        :param str resource_name: The name of the resource.
        :param StoreArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(StoreArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 append_meta: Optional[pulumi.Input[bool]] = None,
                 auto_split: Optional[pulumi.Input[bool]] = None,
                 enable_web_tracking: Optional[pulumi.Input[bool]] = None,
                 max_split_shard_count: Optional[pulumi.Input[int]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 project: Optional[pulumi.Input[str]] = None,
                 retention_period: Optional[pulumi.Input[int]] = None,
                 shard_count: Optional[pulumi.Input[int]] = None,
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
            __props__ = StoreArgs.__new__(StoreArgs)

            __props__.__dict__["append_meta"] = append_meta
            __props__.__dict__["auto_split"] = auto_split
            __props__.__dict__["enable_web_tracking"] = enable_web_tracking
            __props__.__dict__["max_split_shard_count"] = max_split_shard_count
            __props__.__dict__["name"] = name
            if project is None and not opts.urn:
                raise TypeError("Missing required property 'project'")
            __props__.__dict__["project"] = project
            __props__.__dict__["retention_period"] = retention_period
            __props__.__dict__["shard_count"] = shard_count
            __props__.__dict__["shards"] = None
        super(Store, __self__).__init__(
            'alicloud:log/store:Store',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            append_meta: Optional[pulumi.Input[bool]] = None,
            auto_split: Optional[pulumi.Input[bool]] = None,
            enable_web_tracking: Optional[pulumi.Input[bool]] = None,
            max_split_shard_count: Optional[pulumi.Input[int]] = None,
            name: Optional[pulumi.Input[str]] = None,
            project: Optional[pulumi.Input[str]] = None,
            retention_period: Optional[pulumi.Input[int]] = None,
            shard_count: Optional[pulumi.Input[int]] = None,
            shards: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['StoreShardArgs']]]]] = None) -> 'Store':
        """
        Get an existing Store resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] append_meta: Determines whether to append log meta automatically. The meta includes log receive time and client IP address. Default to true.
        :param pulumi.Input[bool] auto_split: Determines whether to automatically split a shard. Default to true.
        :param pulumi.Input[bool] enable_web_tracking: Determines whether to enable Web Tracking. Default false.
        :param pulumi.Input[int] max_split_shard_count: The maximum number of shards for automatic split, which is in the range of 1 to 64. You must specify this parameter when autoSplit is true.
        :param pulumi.Input[str] name: The log store, which is unique in the same project.
        :param pulumi.Input[str] project: The project name to the log store belongs.
        :param pulumi.Input[int] retention_period: The data retention time (in days). Valid values: [1-3650]. Default to 30. Log store data will be stored permanently when the value is "3650".
        :param pulumi.Input[int] shard_count: The number of shards in this log store. Default to 2. You can modify it by "Split" or "Merge" operations. [Refer to details](https://www.alibabacloud.com/help/doc-detail/28976.htm)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _StoreState.__new__(_StoreState)

        __props__.__dict__["append_meta"] = append_meta
        __props__.__dict__["auto_split"] = auto_split
        __props__.__dict__["enable_web_tracking"] = enable_web_tracking
        __props__.__dict__["max_split_shard_count"] = max_split_shard_count
        __props__.__dict__["name"] = name
        __props__.__dict__["project"] = project
        __props__.__dict__["retention_period"] = retention_period
        __props__.__dict__["shard_count"] = shard_count
        __props__.__dict__["shards"] = shards
        return Store(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="appendMeta")
    def append_meta(self) -> pulumi.Output[Optional[bool]]:
        """
        Determines whether to append log meta automatically. The meta includes log receive time and client IP address. Default to true.
        """
        return pulumi.get(self, "append_meta")

    @property
    @pulumi.getter(name="autoSplit")
    def auto_split(self) -> pulumi.Output[Optional[bool]]:
        """
        Determines whether to automatically split a shard. Default to true.
        """
        return pulumi.get(self, "auto_split")

    @property
    @pulumi.getter(name="enableWebTracking")
    def enable_web_tracking(self) -> pulumi.Output[Optional[bool]]:
        """
        Determines whether to enable Web Tracking. Default false.
        """
        return pulumi.get(self, "enable_web_tracking")

    @property
    @pulumi.getter(name="maxSplitShardCount")
    def max_split_shard_count(self) -> pulumi.Output[Optional[int]]:
        """
        The maximum number of shards for automatic split, which is in the range of 1 to 64. You must specify this parameter when autoSplit is true.
        """
        return pulumi.get(self, "max_split_shard_count")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The log store, which is unique in the same project.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def project(self) -> pulumi.Output[str]:
        """
        The project name to the log store belongs.
        """
        return pulumi.get(self, "project")

    @property
    @pulumi.getter(name="retentionPeriod")
    def retention_period(self) -> pulumi.Output[Optional[int]]:
        """
        The data retention time (in days). Valid values: [1-3650]. Default to 30. Log store data will be stored permanently when the value is "3650".
        """
        return pulumi.get(self, "retention_period")

    @property
    @pulumi.getter(name="shardCount")
    def shard_count(self) -> pulumi.Output[Optional[int]]:
        """
        The number of shards in this log store. Default to 2. You can modify it by "Split" or "Merge" operations. [Refer to details](https://www.alibabacloud.com/help/doc-detail/28976.htm)
        """
        return pulumi.get(self, "shard_count")

    @property
    @pulumi.getter
    def shards(self) -> pulumi.Output[Sequence['outputs.StoreShard']]:
        return pulumi.get(self, "shards")

