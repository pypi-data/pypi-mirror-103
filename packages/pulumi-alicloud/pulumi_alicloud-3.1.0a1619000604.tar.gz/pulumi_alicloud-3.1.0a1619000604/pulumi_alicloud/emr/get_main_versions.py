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
    'GetMainVersionsResult',
    'AwaitableGetMainVersionsResult',
    'get_main_versions',
]

@pulumi.output_type
class GetMainVersionsResult:
    """
    A collection of values returned by getMainVersions.
    """
    def __init__(__self__, cluster_types=None, emr_version=None, id=None, ids=None, main_versions=None, output_file=None):
        if cluster_types and not isinstance(cluster_types, list):
            raise TypeError("Expected argument 'cluster_types' to be a list")
        pulumi.set(__self__, "cluster_types", cluster_types)
        if emr_version and not isinstance(emr_version, str):
            raise TypeError("Expected argument 'emr_version' to be a str")
        pulumi.set(__self__, "emr_version", emr_version)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if main_versions and not isinstance(main_versions, list):
            raise TypeError("Expected argument 'main_versions' to be a list")
        pulumi.set(__self__, "main_versions", main_versions)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)

    @property
    @pulumi.getter(name="clusterTypes")
    def cluster_types(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "cluster_types")

    @property
    @pulumi.getter(name="emrVersion")
    def emr_version(self) -> Optional[str]:
        """
        The version of the emr cluster instance.
        """
        return pulumi.get(self, "emr_version")

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
        """
        A list of emr instance types IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="mainVersions")
    def main_versions(self) -> Sequence['outputs.GetMainVersionsMainVersionResult']:
        """
        A list of versions of the emr cluster instance. Each element contains the following attributes:
        """
        return pulumi.get(self, "main_versions")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")


class AwaitableGetMainVersionsResult(GetMainVersionsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetMainVersionsResult(
            cluster_types=self.cluster_types,
            emr_version=self.emr_version,
            id=self.id,
            ids=self.ids,
            main_versions=self.main_versions,
            output_file=self.output_file)


def get_main_versions(cluster_types: Optional[Sequence[str]] = None,
                      emr_version: Optional[str] = None,
                      output_file: Optional[str] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetMainVersionsResult:
    """
    The `emr.getMainVersions` data source provides a collection of emr
    main versions available in Alibaba Cloud account when create a emr cluster.

    > **NOTE:** Available in 1.59.0+

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.emr.get_main_versions(cluster_types=[
            "HADOOP",
            "ZOOKEEPER",
        ],
        emr_version="EMR-3.22.0")
    pulumi.export("firstMainVersion", default.main_versions[0].emr_version)
    pulumi.export("thisClusterTypes", default.main_versions[0].cluster_types)
    ```


    :param Sequence[str] cluster_types: The supported clusterType of this emr version.
           Possible values may be any one or combination of these: ["HADOOP", "DRUID", "KAFKA", "ZOOKEEPER", "FLINK", "CLICKHOUSE"]
    :param str emr_version: The version of the emr cluster instance. Possible values: `EMR-4.0.0`, `EMR-3.23.0`, `EMR-3.22.0`.
    """
    __args__ = dict()
    __args__['clusterTypes'] = cluster_types
    __args__['emrVersion'] = emr_version
    __args__['outputFile'] = output_file
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:emr/getMainVersions:getMainVersions', __args__, opts=opts, typ=GetMainVersionsResult).value

    return AwaitableGetMainVersionsResult(
        cluster_types=__ret__.cluster_types,
        emr_version=__ret__.emr_version,
        id=__ret__.id,
        ids=__ret__.ids,
        main_versions=__ret__.main_versions,
        output_file=__ret__.output_file)
