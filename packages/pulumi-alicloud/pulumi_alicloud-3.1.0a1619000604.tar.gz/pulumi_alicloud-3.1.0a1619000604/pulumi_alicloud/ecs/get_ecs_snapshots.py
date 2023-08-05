# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs

__all__ = [
    'GetEcsSnapshotsResult',
    'AwaitableGetEcsSnapshotsResult',
    'get_ecs_snapshots',
]

@pulumi.output_type
class GetEcsSnapshotsResult:
    """
    A collection of values returned by getEcsSnapshots.
    """
    def __init__(__self__, category=None, dry_run=None, encrypted=None, id=None, ids=None, kms_key_id=None, name_regex=None, names=None, output_file=None, resource_group_id=None, snapshot_link_id=None, snapshot_name=None, snapshot_type=None, snapshots=None, source_disk_type=None, status=None, tags=None, type=None, usage=None):
        if category and not isinstance(category, str):
            raise TypeError("Expected argument 'category' to be a str")
        pulumi.set(__self__, "category", category)
        if dry_run and not isinstance(dry_run, bool):
            raise TypeError("Expected argument 'dry_run' to be a bool")
        pulumi.set(__self__, "dry_run", dry_run)
        if encrypted and not isinstance(encrypted, bool):
            raise TypeError("Expected argument 'encrypted' to be a bool")
        pulumi.set(__self__, "encrypted", encrypted)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if kms_key_id and not isinstance(kms_key_id, str):
            raise TypeError("Expected argument 'kms_key_id' to be a str")
        pulumi.set(__self__, "kms_key_id", kms_key_id)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if snapshot_link_id and not isinstance(snapshot_link_id, str):
            raise TypeError("Expected argument 'snapshot_link_id' to be a str")
        pulumi.set(__self__, "snapshot_link_id", snapshot_link_id)
        if snapshot_name and not isinstance(snapshot_name, str):
            raise TypeError("Expected argument 'snapshot_name' to be a str")
        pulumi.set(__self__, "snapshot_name", snapshot_name)
        if snapshot_type and not isinstance(snapshot_type, str):
            raise TypeError("Expected argument 'snapshot_type' to be a str")
        pulumi.set(__self__, "snapshot_type", snapshot_type)
        if snapshots and not isinstance(snapshots, list):
            raise TypeError("Expected argument 'snapshots' to be a list")
        pulumi.set(__self__, "snapshots", snapshots)
        if source_disk_type and not isinstance(source_disk_type, str):
            raise TypeError("Expected argument 'source_disk_type' to be a str")
        pulumi.set(__self__, "source_disk_type", source_disk_type)
        if status and not isinstance(status, str):
            raise TypeError("Expected argument 'status' to be a str")
        pulumi.set(__self__, "status", status)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if type and not isinstance(type, str):
            raise TypeError("Expected argument 'type' to be a str")
        pulumi.set(__self__, "type", type)
        if usage and not isinstance(usage, str):
            raise TypeError("Expected argument 'usage' to be a str")
        pulumi.set(__self__, "usage", usage)

    @property
    @pulumi.getter
    def category(self) -> Optional[str]:
        return pulumi.get(self, "category")

    @property
    @pulumi.getter(name="dryRun")
    def dry_run(self) -> Optional[bool]:
        return pulumi.get(self, "dry_run")

    @property
    @pulumi.getter
    def encrypted(self) -> Optional[bool]:
        return pulumi.get(self, "encrypted")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="kmsKeyId")
    def kms_key_id(self) -> Optional[str]:
        return pulumi.get(self, "kms_key_id")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="snapshotLinkId")
    def snapshot_link_id(self) -> Optional[str]:
        return pulumi.get(self, "snapshot_link_id")

    @property
    @pulumi.getter(name="snapshotName")
    def snapshot_name(self) -> Optional[str]:
        return pulumi.get(self, "snapshot_name")

    @property
    @pulumi.getter(name="snapshotType")
    def snapshot_type(self) -> Optional[str]:
        return pulumi.get(self, "snapshot_type")

    @property
    @pulumi.getter
    def snapshots(self) -> Sequence['outputs.GetEcsSnapshotsSnapshotResult']:
        return pulumi.get(self, "snapshots")

    @property
    @pulumi.getter(name="sourceDiskType")
    def source_disk_type(self) -> Optional[str]:
        return pulumi.get(self, "source_disk_type")

    @property
    @pulumi.getter
    def status(self) -> Optional[str]:
        return pulumi.get(self, "status")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, Any]]:
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter
    def type(self) -> Optional[str]:
        return pulumi.get(self, "type")

    @property
    @pulumi.getter
    def usage(self) -> Optional[str]:
        return pulumi.get(self, "usage")


class AwaitableGetEcsSnapshotsResult(GetEcsSnapshotsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetEcsSnapshotsResult(
            category=self.category,
            dry_run=self.dry_run,
            encrypted=self.encrypted,
            id=self.id,
            ids=self.ids,
            kms_key_id=self.kms_key_id,
            name_regex=self.name_regex,
            names=self.names,
            output_file=self.output_file,
            resource_group_id=self.resource_group_id,
            snapshot_link_id=self.snapshot_link_id,
            snapshot_name=self.snapshot_name,
            snapshot_type=self.snapshot_type,
            snapshots=self.snapshots,
            source_disk_type=self.source_disk_type,
            status=self.status,
            tags=self.tags,
            type=self.type,
            usage=self.usage)


def get_ecs_snapshots(category: Optional[str] = None,
                      dry_run: Optional[bool] = None,
                      encrypted: Optional[bool] = None,
                      ids: Optional[Sequence[str]] = None,
                      kms_key_id: Optional[str] = None,
                      name_regex: Optional[str] = None,
                      output_file: Optional[str] = None,
                      resource_group_id: Optional[str] = None,
                      snapshot_link_id: Optional[str] = None,
                      snapshot_name: Optional[str] = None,
                      snapshot_type: Optional[str] = None,
                      source_disk_type: Optional[str] = None,
                      status: Optional[str] = None,
                      tags: Optional[Mapping[str, Any]] = None,
                      type: Optional[str] = None,
                      usage: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetEcsSnapshotsResult:
    """
    This data source provides the Ecs Snapshots of the current Alibaba Cloud user.

    > **NOTE:** Available in v1.120.0+.

    ## Example Usage

    Basic Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    example = alicloud.ecs.get_ecs_snapshots(ids=["s-bp1fvuxxxxxxxx"],
        name_regex="tf-test")
    pulumi.export("firstEcsSnapshotId", example.snapshots[0].id)
    ```


    :param str category: The category of the snapshot.
    :param bool dry_run: Specifies whether to check the validity of the request without actually making the request.
    :param bool encrypted: Whether the snapshot is encrypted.
    :param Sequence[str] ids: A list of Snapshot IDs.
    :param str kms_key_id: The kms key id.
    :param str name_regex: A regex string to filter results by Snapshot name.
    :param str resource_group_id: The resource group id.
    :param str snapshot_link_id: The snapshot link id.
    :param str snapshot_name: Snapshot Display Name.
    :param str snapshot_type: Snapshot creation type.
    :param str source_disk_type: Source disk attributes.
    :param str status: The status of the snapshot.
    :param Mapping[str, Any] tags: The tags.
    :param str usage: A resource type that has a reference relationship.
    """
    __args__ = dict()
    __args__['category'] = category
    __args__['dryRun'] = dry_run
    __args__['encrypted'] = encrypted
    __args__['ids'] = ids
    __args__['kmsKeyId'] = kms_key_id
    __args__['nameRegex'] = name_regex
    __args__['outputFile'] = output_file
    __args__['resourceGroupId'] = resource_group_id
    __args__['snapshotLinkId'] = snapshot_link_id
    __args__['snapshotName'] = snapshot_name
    __args__['snapshotType'] = snapshot_type
    __args__['sourceDiskType'] = source_disk_type
    __args__['status'] = status
    __args__['tags'] = tags
    __args__['type'] = type
    __args__['usage'] = usage
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:ecs/getEcsSnapshots:getEcsSnapshots', __args__, opts=opts, typ=GetEcsSnapshotsResult).value

    return AwaitableGetEcsSnapshotsResult(
        category=__ret__.category,
        dry_run=__ret__.dry_run,
        encrypted=__ret__.encrypted,
        id=__ret__.id,
        ids=__ret__.ids,
        kms_key_id=__ret__.kms_key_id,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        output_file=__ret__.output_file,
        resource_group_id=__ret__.resource_group_id,
        snapshot_link_id=__ret__.snapshot_link_id,
        snapshot_name=__ret__.snapshot_name,
        snapshot_type=__ret__.snapshot_type,
        snapshots=__ret__.snapshots,
        source_disk_type=__ret__.source_disk_type,
        status=__ret__.status,
        tags=__ret__.tags,
        type=__ret__.type,
        usage=__ret__.usage)
