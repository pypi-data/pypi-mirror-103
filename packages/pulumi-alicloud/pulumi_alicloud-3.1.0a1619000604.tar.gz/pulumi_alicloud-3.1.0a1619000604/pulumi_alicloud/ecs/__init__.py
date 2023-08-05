# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .auto_provisioning_group import *
from .auto_snapshot_policy import *
from .command import *
from .copy_image import *
from .dedicated_host import *
from .disk import *
from .disk_attachment import *
from .ecs_key_pair import *
from .ecs_key_pair_attachment import *
from .ecs_launch_template import *
from .ecs_snapshot import *
from .eip import *
from .eip_association import *
from .get_auto_snapshot_policies import *
from .get_commands import *
from .get_dedicated_hosts import *
from .get_disks import *
from .get_ecs_key_pairs import *
from .get_ecs_launch_templates import *
from .get_ecs_snapshots import *
from .get_eips import *
from .get_hpc_clusters import *
from .get_images import *
from .get_instance_type_families import *
from .get_instance_types import *
from .get_instances import *
from .get_key_pairs import *
from .get_network_interfaces import *
from .get_security_group_rules import *
from .get_security_groups import *
from .get_snapshots import *
from .hpc_cluster import *
from .image import *
from .image_copy import *
from .image_export import *
from .image_import import *
from .image_share_permission import *
from .instance import *
from .key_pair import *
from .key_pair_attachment import *
from .launch_template import *
from .reserved_instance import *
from .security_group import *
from .security_group_rule import *
from .snapshot import *
from .snapshot_policy import *
from ._inputs import *
from . import outputs

def _register_module():
    import pulumi
    from .. import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "alicloud:ecs/autoProvisioningGroup:AutoProvisioningGroup":
                return AutoProvisioningGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/autoSnapshotPolicy:AutoSnapshotPolicy":
                return AutoSnapshotPolicy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/command:Command":
                return Command(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/copyImage:CopyImage":
                return CopyImage(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/dedicatedHost:DedicatedHost":
                return DedicatedHost(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/disk:Disk":
                return Disk(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/diskAttachment:DiskAttachment":
                return DiskAttachment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/ecsKeyPair:EcsKeyPair":
                return EcsKeyPair(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/ecsKeyPairAttachment:EcsKeyPairAttachment":
                return EcsKeyPairAttachment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/ecsLaunchTemplate:EcsLaunchTemplate":
                return EcsLaunchTemplate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/ecsSnapshot:EcsSnapshot":
                return EcsSnapshot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/eip:Eip":
                return Eip(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/eipAssociation:EipAssociation":
                return EipAssociation(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/hpcCluster:HpcCluster":
                return HpcCluster(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/image:Image":
                return Image(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/imageCopy:ImageCopy":
                return ImageCopy(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/imageExport:ImageExport":
                return ImageExport(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/imageImport:ImageImport":
                return ImageImport(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/imageSharePermission:ImageSharePermission":
                return ImageSharePermission(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/instance:Instance":
                return Instance(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/keyPair:KeyPair":
                return KeyPair(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/keyPairAttachment:KeyPairAttachment":
                return KeyPairAttachment(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/launchTemplate:LaunchTemplate":
                return LaunchTemplate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/reservedInstance:ReservedInstance":
                return ReservedInstance(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/securityGroup:SecurityGroup":
                return SecurityGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/securityGroupRule:SecurityGroupRule":
                return SecurityGroupRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/snapshot:Snapshot":
                return Snapshot(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "alicloud:ecs/snapshotPolicy:SnapshotPolicy":
                return SnapshotPolicy(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("alicloud", "ecs/autoProvisioningGroup", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/autoSnapshotPolicy", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/command", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/copyImage", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/dedicatedHost", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/disk", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/diskAttachment", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/ecsKeyPair", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/ecsKeyPairAttachment", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/ecsLaunchTemplate", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/ecsSnapshot", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/eip", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/eipAssociation", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/hpcCluster", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/image", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/imageCopy", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/imageExport", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/imageImport", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/imageSharePermission", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/instance", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/keyPair", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/keyPairAttachment", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/launchTemplate", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/reservedInstance", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/securityGroup", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/securityGroupRule", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/snapshot", _module_instance)
    pulumi.runtime.register_resource_module("alicloud", "ecs/snapshotPolicy", _module_instance)

_register_module()
