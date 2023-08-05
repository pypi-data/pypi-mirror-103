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
    'GetLoadBalancersResult',
    'AwaitableGetLoadBalancersResult',
    'get_load_balancers',
]

@pulumi.output_type
class GetLoadBalancersResult:
    """
    A collection of values returned by getLoadBalancers.
    """
    def __init__(__self__, address=None, id=None, ids=None, master_availability_zone=None, name_regex=None, names=None, network_type=None, output_file=None, resource_group_id=None, slave_availability_zone=None, slbs=None, tags=None, vpc_id=None, vswitch_id=None):
        if address and not isinstance(address, str):
            raise TypeError("Expected argument 'address' to be a str")
        pulumi.set(__self__, "address", address)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if master_availability_zone and not isinstance(master_availability_zone, str):
            raise TypeError("Expected argument 'master_availability_zone' to be a str")
        pulumi.set(__self__, "master_availability_zone", master_availability_zone)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if names and not isinstance(names, list):
            raise TypeError("Expected argument 'names' to be a list")
        pulumi.set(__self__, "names", names)
        if network_type and not isinstance(network_type, str):
            raise TypeError("Expected argument 'network_type' to be a str")
        pulumi.set(__self__, "network_type", network_type)
        if output_file and not isinstance(output_file, str):
            raise TypeError("Expected argument 'output_file' to be a str")
        pulumi.set(__self__, "output_file", output_file)
        if resource_group_id and not isinstance(resource_group_id, str):
            raise TypeError("Expected argument 'resource_group_id' to be a str")
        pulumi.set(__self__, "resource_group_id", resource_group_id)
        if slave_availability_zone and not isinstance(slave_availability_zone, str):
            raise TypeError("Expected argument 'slave_availability_zone' to be a str")
        pulumi.set(__self__, "slave_availability_zone", slave_availability_zone)
        if slbs and not isinstance(slbs, list):
            raise TypeError("Expected argument 'slbs' to be a list")
        pulumi.set(__self__, "slbs", slbs)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if vpc_id and not isinstance(vpc_id, str):
            raise TypeError("Expected argument 'vpc_id' to be a str")
        pulumi.set(__self__, "vpc_id", vpc_id)
        if vswitch_id and not isinstance(vswitch_id, str):
            raise TypeError("Expected argument 'vswitch_id' to be a str")
        pulumi.set(__self__, "vswitch_id", vswitch_id)

    @property
    @pulumi.getter
    def address(self) -> Optional[str]:
        """
        Service address of the SLB.
        """
        return pulumi.get(self, "address")

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
        A list of slb IDs.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="masterAvailabilityZone")
    def master_availability_zone(self) -> Optional[str]:
        """
        Master availability zone of the SLBs.
        """
        return pulumi.get(self, "master_availability_zone")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def names(self) -> Sequence[str]:
        """
        A list of slb names.
        """
        return pulumi.get(self, "names")

    @property
    @pulumi.getter(name="networkType")
    def network_type(self) -> Optional[str]:
        """
        Network type of the SLB. Possible values: `vpc` and `classic`.
        """
        return pulumi.get(self, "network_type")

    @property
    @pulumi.getter(name="outputFile")
    def output_file(self) -> Optional[str]:
        return pulumi.get(self, "output_file")

    @property
    @pulumi.getter(name="resourceGroupId")
    def resource_group_id(self) -> Optional[str]:
        return pulumi.get(self, "resource_group_id")

    @property
    @pulumi.getter(name="slaveAvailabilityZone")
    def slave_availability_zone(self) -> Optional[str]:
        """
        Slave availability zone of the SLBs.
        """
        return pulumi.get(self, "slave_availability_zone")

    @property
    @pulumi.getter
    def slbs(self) -> Sequence['outputs.GetLoadBalancersSlbResult']:
        """
        A list of SLBs. Each element contains the following attributes:
        """
        return pulumi.get(self, "slbs")

    @property
    @pulumi.getter
    def tags(self) -> Optional[Mapping[str, Any]]:
        """
        A map of tags assigned to the SLB instance.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="vpcId")
    def vpc_id(self) -> Optional[str]:
        """
        ID of the VPC the SLB belongs to.
        """
        return pulumi.get(self, "vpc_id")

    @property
    @pulumi.getter(name="vswitchId")
    def vswitch_id(self) -> Optional[str]:
        """
        ID of the VSwitch the SLB belongs to.
        """
        return pulumi.get(self, "vswitch_id")


class AwaitableGetLoadBalancersResult(GetLoadBalancersResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLoadBalancersResult(
            address=self.address,
            id=self.id,
            ids=self.ids,
            master_availability_zone=self.master_availability_zone,
            name_regex=self.name_regex,
            names=self.names,
            network_type=self.network_type,
            output_file=self.output_file,
            resource_group_id=self.resource_group_id,
            slave_availability_zone=self.slave_availability_zone,
            slbs=self.slbs,
            tags=self.tags,
            vpc_id=self.vpc_id,
            vswitch_id=self.vswitch_id)


def get_load_balancers(address: Optional[str] = None,
                       ids: Optional[Sequence[str]] = None,
                       master_availability_zone: Optional[str] = None,
                       name_regex: Optional[str] = None,
                       network_type: Optional[str] = None,
                       output_file: Optional[str] = None,
                       resource_group_id: Optional[str] = None,
                       slave_availability_zone: Optional[str] = None,
                       tags: Optional[Mapping[str, Any]] = None,
                       vpc_id: Optional[str] = None,
                       vswitch_id: Optional[str] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLoadBalancersResult:
    """
    This data source provides the server load balancers of the current Alibaba Cloud user.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_alicloud as alicloud

    default = alicloud.slb.LoadBalancer("default")
    slbs_ds = alicloud.slb.get_load_balancers(name_regex="sample_slb")
    pulumi.export("firstSlbId", slbs_ds.slbs[0].id)
    ```


    :param str address: Service address of the SLBs.
    :param Sequence[str] ids: A list of SLBs IDs.
    :param str master_availability_zone: Master availability zone of the SLBs.
    :param str name_regex: A regex string to filter results by SLB name.
    :param str network_type: Network type of the SLBs. Valid values: `vpc` and `classic`.
    :param str resource_group_id: The Id of resource group which SLB belongs.
    :param str slave_availability_zone: Slave availability zone of the SLBs.
    :param Mapping[str, Any] tags: A map of tags assigned to the SLB instances. The `tags` can have a maximum of 5 tag. It must be in the format:
           ```python
           import pulumi
           import pulumi_alicloud as alicloud
           
           tagged_instances = alicloud.slb.get_load_balancers(tags={
               "tagKey1": "tagValue1",
               "tagKey2": "tagValue2",
           })
           ```
    :param str vpc_id: ID of the VPC linked to the SLBs.
    :param str vswitch_id: ID of the VSwitch linked to the SLBs.
    """
    __args__ = dict()
    __args__['address'] = address
    __args__['ids'] = ids
    __args__['masterAvailabilityZone'] = master_availability_zone
    __args__['nameRegex'] = name_regex
    __args__['networkType'] = network_type
    __args__['outputFile'] = output_file
    __args__['resourceGroupId'] = resource_group_id
    __args__['slaveAvailabilityZone'] = slave_availability_zone
    __args__['tags'] = tags
    __args__['vpcId'] = vpc_id
    __args__['vswitchId'] = vswitch_id
    if opts is None:
        opts = pulumi.InvokeOptions()
    if opts.version is None:
        opts.version = _utilities.get_version()
    __ret__ = pulumi.runtime.invoke('alicloud:slb/getLoadBalancers:getLoadBalancers', __args__, opts=opts, typ=GetLoadBalancersResult).value

    return AwaitableGetLoadBalancersResult(
        address=__ret__.address,
        id=__ret__.id,
        ids=__ret__.ids,
        master_availability_zone=__ret__.master_availability_zone,
        name_regex=__ret__.name_regex,
        names=__ret__.names,
        network_type=__ret__.network_type,
        output_file=__ret__.output_file,
        resource_group_id=__ret__.resource_group_id,
        slave_availability_zone=__ret__.slave_availability_zone,
        slbs=__ret__.slbs,
        tags=__ret__.tags,
        vpc_id=__ret__.vpc_id,
        vswitch_id=__ret__.vswitch_id)
