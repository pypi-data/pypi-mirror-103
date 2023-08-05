# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from . import _utilities
from . import outputs
from ._inputs import *

__all__ = ['ClusterSyncArgs', 'ClusterSync']

@pulumi.input_type
class ClusterSyncArgs:
    def __init__(__self__, *,
                 cluster_id: pulumi.Input[str],
                 node_pool_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 state_confirm: Optional[pulumi.Input[int]] = None,
                 synced: Optional[pulumi.Input[bool]] = None,
                 wait_catalogs: Optional[pulumi.Input[bool]] = None,
                 wait_monitoring: Optional[pulumi.Input[bool]] = None):
        """
        The set of arguments for constructing a ClusterSync resource.
        :param pulumi.Input[str] cluster_id: The Cluster ID of the node (string).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] node_pool_ids: The node pool IDs used by the cluster id (list)
        :param pulumi.Input[int] state_confirm: Wait until active status is confirmed a number of times (wait interval of 5s). Default: `1` means no confirmation (int)
        :param pulumi.Input[bool] wait_catalogs: Wait until all catalogs are downloaded and active. Default: `false` (bool)
        :param pulumi.Input[bool] wait_monitoring: Wait until monitoring is up and running. Default: `false` (bool)
        """
        pulumi.set(__self__, "cluster_id", cluster_id)
        if node_pool_ids is not None:
            pulumi.set(__self__, "node_pool_ids", node_pool_ids)
        if state_confirm is not None:
            pulumi.set(__self__, "state_confirm", state_confirm)
        if synced is not None:
            pulumi.set(__self__, "synced", synced)
        if wait_catalogs is not None:
            pulumi.set(__self__, "wait_catalogs", wait_catalogs)
        if wait_monitoring is not None:
            pulumi.set(__self__, "wait_monitoring", wait_monitoring)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> pulumi.Input[str]:
        """
        The Cluster ID of the node (string).
        """
        return pulumi.get(self, "cluster_id")

    @cluster_id.setter
    def cluster_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_id", value)

    @property
    @pulumi.getter(name="nodePoolIds")
    def node_pool_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The node pool IDs used by the cluster id (list)
        """
        return pulumi.get(self, "node_pool_ids")

    @node_pool_ids.setter
    def node_pool_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "node_pool_ids", value)

    @property
    @pulumi.getter(name="stateConfirm")
    def state_confirm(self) -> Optional[pulumi.Input[int]]:
        """
        Wait until active status is confirmed a number of times (wait interval of 5s). Default: `1` means no confirmation (int)
        """
        return pulumi.get(self, "state_confirm")

    @state_confirm.setter
    def state_confirm(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "state_confirm", value)

    @property
    @pulumi.getter
    def synced(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "synced")

    @synced.setter
    def synced(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "synced", value)

    @property
    @pulumi.getter(name="waitCatalogs")
    def wait_catalogs(self) -> Optional[pulumi.Input[bool]]:
        """
        Wait until all catalogs are downloaded and active. Default: `false` (bool)
        """
        return pulumi.get(self, "wait_catalogs")

    @wait_catalogs.setter
    def wait_catalogs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wait_catalogs", value)

    @property
    @pulumi.getter(name="waitMonitoring")
    def wait_monitoring(self) -> Optional[pulumi.Input[bool]]:
        """
        Wait until monitoring is up and running. Default: `false` (bool)
        """
        return pulumi.get(self, "wait_monitoring")

    @wait_monitoring.setter
    def wait_monitoring(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wait_monitoring", value)


@pulumi.input_type
class _ClusterSyncState:
    def __init__(__self__, *,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 default_project_id: Optional[pulumi.Input[str]] = None,
                 kube_config: Optional[pulumi.Input[str]] = None,
                 node_pool_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 nodes: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterSyncNodeArgs']]]] = None,
                 state_confirm: Optional[pulumi.Input[int]] = None,
                 synced: Optional[pulumi.Input[bool]] = None,
                 system_project_id: Optional[pulumi.Input[str]] = None,
                 wait_catalogs: Optional[pulumi.Input[bool]] = None,
                 wait_monitoring: Optional[pulumi.Input[bool]] = None):
        """
        Input properties used for looking up and filtering ClusterSync resources.
        :param pulumi.Input[str] cluster_id: The Cluster ID of the node (string).
        :param pulumi.Input[str] default_project_id: (Computed) Default project ID for the cluster sync (string)
        :param pulumi.Input[str] kube_config: (Computed/Sensitive) Kube Config generated for the cluster sync (string)
        :param pulumi.Input[Sequence[pulumi.Input[str]]] node_pool_ids: The node pool IDs used by the cluster id (list)
        :param pulumi.Input[Sequence[pulumi.Input['ClusterSyncNodeArgs']]] nodes: (Computed) The cluster nodes (list).
        :param pulumi.Input[int] state_confirm: Wait until active status is confirmed a number of times (wait interval of 5s). Default: `1` means no confirmation (int)
        :param pulumi.Input[str] system_project_id: (Computed) System project ID for the cluster sync (string)
        :param pulumi.Input[bool] wait_catalogs: Wait until all catalogs are downloaded and active. Default: `false` (bool)
        :param pulumi.Input[bool] wait_monitoring: Wait until monitoring is up and running. Default: `false` (bool)
        """
        if cluster_id is not None:
            pulumi.set(__self__, "cluster_id", cluster_id)
        if default_project_id is not None:
            pulumi.set(__self__, "default_project_id", default_project_id)
        if kube_config is not None:
            pulumi.set(__self__, "kube_config", kube_config)
        if node_pool_ids is not None:
            pulumi.set(__self__, "node_pool_ids", node_pool_ids)
        if nodes is not None:
            pulumi.set(__self__, "nodes", nodes)
        if state_confirm is not None:
            pulumi.set(__self__, "state_confirm", state_confirm)
        if synced is not None:
            pulumi.set(__self__, "synced", synced)
        if system_project_id is not None:
            pulumi.set(__self__, "system_project_id", system_project_id)
        if wait_catalogs is not None:
            pulumi.set(__self__, "wait_catalogs", wait_catalogs)
        if wait_monitoring is not None:
            pulumi.set(__self__, "wait_monitoring", wait_monitoring)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Cluster ID of the node (string).
        """
        return pulumi.get(self, "cluster_id")

    @cluster_id.setter
    def cluster_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_id", value)

    @property
    @pulumi.getter(name="defaultProjectId")
    def default_project_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) Default project ID for the cluster sync (string)
        """
        return pulumi.get(self, "default_project_id")

    @default_project_id.setter
    def default_project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "default_project_id", value)

    @property
    @pulumi.getter(name="kubeConfig")
    def kube_config(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed/Sensitive) Kube Config generated for the cluster sync (string)
        """
        return pulumi.get(self, "kube_config")

    @kube_config.setter
    def kube_config(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kube_config", value)

    @property
    @pulumi.getter(name="nodePoolIds")
    def node_pool_ids(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        The node pool IDs used by the cluster id (list)
        """
        return pulumi.get(self, "node_pool_ids")

    @node_pool_ids.setter
    def node_pool_ids(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "node_pool_ids", value)

    @property
    @pulumi.getter
    def nodes(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterSyncNodeArgs']]]]:
        """
        (Computed) The cluster nodes (list).
        """
        return pulumi.get(self, "nodes")

    @nodes.setter
    def nodes(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterSyncNodeArgs']]]]):
        pulumi.set(self, "nodes", value)

    @property
    @pulumi.getter(name="stateConfirm")
    def state_confirm(self) -> Optional[pulumi.Input[int]]:
        """
        Wait until active status is confirmed a number of times (wait interval of 5s). Default: `1` means no confirmation (int)
        """
        return pulumi.get(self, "state_confirm")

    @state_confirm.setter
    def state_confirm(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "state_confirm", value)

    @property
    @pulumi.getter
    def synced(self) -> Optional[pulumi.Input[bool]]:
        return pulumi.get(self, "synced")

    @synced.setter
    def synced(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "synced", value)

    @property
    @pulumi.getter(name="systemProjectId")
    def system_project_id(self) -> Optional[pulumi.Input[str]]:
        """
        (Computed) System project ID for the cluster sync (string)
        """
        return pulumi.get(self, "system_project_id")

    @system_project_id.setter
    def system_project_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "system_project_id", value)

    @property
    @pulumi.getter(name="waitCatalogs")
    def wait_catalogs(self) -> Optional[pulumi.Input[bool]]:
        """
        Wait until all catalogs are downloaded and active. Default: `false` (bool)
        """
        return pulumi.get(self, "wait_catalogs")

    @wait_catalogs.setter
    def wait_catalogs(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wait_catalogs", value)

    @property
    @pulumi.getter(name="waitMonitoring")
    def wait_monitoring(self) -> Optional[pulumi.Input[bool]]:
        """
        Wait until monitoring is up and running. Default: `false` (bool)
        """
        return pulumi.get(self, "wait_monitoring")

    @wait_monitoring.setter
    def wait_monitoring(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "wait_monitoring", value)


class ClusterSync(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 node_pool_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 state_confirm: Optional[pulumi.Input[int]] = None,
                 synced: Optional[pulumi.Input[bool]] = None,
                 wait_catalogs: Optional[pulumi.Input[bool]] = None,
                 wait_monitoring: Optional[pulumi.Input[bool]] = None,
                 __props__=None):
        """
        Create a ClusterSync resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_id: The Cluster ID of the node (string).
        :param pulumi.Input[Sequence[pulumi.Input[str]]] node_pool_ids: The node pool IDs used by the cluster id (list)
        :param pulumi.Input[int] state_confirm: Wait until active status is confirmed a number of times (wait interval of 5s). Default: `1` means no confirmation (int)
        :param pulumi.Input[bool] wait_catalogs: Wait until all catalogs are downloaded and active. Default: `false` (bool)
        :param pulumi.Input[bool] wait_monitoring: Wait until monitoring is up and running. Default: `false` (bool)
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterSyncArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a ClusterSync resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param ClusterSyncArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterSyncArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 node_pool_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 state_confirm: Optional[pulumi.Input[int]] = None,
                 synced: Optional[pulumi.Input[bool]] = None,
                 wait_catalogs: Optional[pulumi.Input[bool]] = None,
                 wait_monitoring: Optional[pulumi.Input[bool]] = None,
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
            __props__ = ClusterSyncArgs.__new__(ClusterSyncArgs)

            if cluster_id is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_id'")
            __props__.__dict__["cluster_id"] = cluster_id
            __props__.__dict__["node_pool_ids"] = node_pool_ids
            __props__.__dict__["state_confirm"] = state_confirm
            __props__.__dict__["synced"] = synced
            __props__.__dict__["wait_catalogs"] = wait_catalogs
            __props__.__dict__["wait_monitoring"] = wait_monitoring
            __props__.__dict__["default_project_id"] = None
            __props__.__dict__["kube_config"] = None
            __props__.__dict__["nodes"] = None
            __props__.__dict__["system_project_id"] = None
        super(ClusterSync, __self__).__init__(
            'rancher2:index/clusterSync:ClusterSync',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            cluster_id: Optional[pulumi.Input[str]] = None,
            default_project_id: Optional[pulumi.Input[str]] = None,
            kube_config: Optional[pulumi.Input[str]] = None,
            node_pool_ids: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
            nodes: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterSyncNodeArgs']]]]] = None,
            state_confirm: Optional[pulumi.Input[int]] = None,
            synced: Optional[pulumi.Input[bool]] = None,
            system_project_id: Optional[pulumi.Input[str]] = None,
            wait_catalogs: Optional[pulumi.Input[bool]] = None,
            wait_monitoring: Optional[pulumi.Input[bool]] = None) -> 'ClusterSync':
        """
        Get an existing ClusterSync resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] cluster_id: The Cluster ID of the node (string).
        :param pulumi.Input[str] default_project_id: (Computed) Default project ID for the cluster sync (string)
        :param pulumi.Input[str] kube_config: (Computed/Sensitive) Kube Config generated for the cluster sync (string)
        :param pulumi.Input[Sequence[pulumi.Input[str]]] node_pool_ids: The node pool IDs used by the cluster id (list)
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterSyncNodeArgs']]]] nodes: (Computed) The cluster nodes (list).
        :param pulumi.Input[int] state_confirm: Wait until active status is confirmed a number of times (wait interval of 5s). Default: `1` means no confirmation (int)
        :param pulumi.Input[str] system_project_id: (Computed) System project ID for the cluster sync (string)
        :param pulumi.Input[bool] wait_catalogs: Wait until all catalogs are downloaded and active. Default: `false` (bool)
        :param pulumi.Input[bool] wait_monitoring: Wait until monitoring is up and running. Default: `false` (bool)
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ClusterSyncState.__new__(_ClusterSyncState)

        __props__.__dict__["cluster_id"] = cluster_id
        __props__.__dict__["default_project_id"] = default_project_id
        __props__.__dict__["kube_config"] = kube_config
        __props__.__dict__["node_pool_ids"] = node_pool_ids
        __props__.__dict__["nodes"] = nodes
        __props__.__dict__["state_confirm"] = state_confirm
        __props__.__dict__["synced"] = synced
        __props__.__dict__["system_project_id"] = system_project_id
        __props__.__dict__["wait_catalogs"] = wait_catalogs
        __props__.__dict__["wait_monitoring"] = wait_monitoring
        return ClusterSync(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> pulumi.Output[str]:
        """
        The Cluster ID of the node (string).
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter(name="defaultProjectId")
    def default_project_id(self) -> pulumi.Output[str]:
        """
        (Computed) Default project ID for the cluster sync (string)
        """
        return pulumi.get(self, "default_project_id")

    @property
    @pulumi.getter(name="kubeConfig")
    def kube_config(self) -> pulumi.Output[str]:
        """
        (Computed/Sensitive) Kube Config generated for the cluster sync (string)
        """
        return pulumi.get(self, "kube_config")

    @property
    @pulumi.getter(name="nodePoolIds")
    def node_pool_ids(self) -> pulumi.Output[Optional[Sequence[str]]]:
        """
        The node pool IDs used by the cluster id (list)
        """
        return pulumi.get(self, "node_pool_ids")

    @property
    @pulumi.getter
    def nodes(self) -> pulumi.Output[Sequence['outputs.ClusterSyncNode']]:
        """
        (Computed) The cluster nodes (list).
        """
        return pulumi.get(self, "nodes")

    @property
    @pulumi.getter(name="stateConfirm")
    def state_confirm(self) -> pulumi.Output[Optional[int]]:
        """
        Wait until active status is confirmed a number of times (wait interval of 5s). Default: `1` means no confirmation (int)
        """
        return pulumi.get(self, "state_confirm")

    @property
    @pulumi.getter
    def synced(self) -> pulumi.Output[Optional[bool]]:
        return pulumi.get(self, "synced")

    @property
    @pulumi.getter(name="systemProjectId")
    def system_project_id(self) -> pulumi.Output[str]:
        """
        (Computed) System project ID for the cluster sync (string)
        """
        return pulumi.get(self, "system_project_id")

    @property
    @pulumi.getter(name="waitCatalogs")
    def wait_catalogs(self) -> pulumi.Output[Optional[bool]]:
        """
        Wait until all catalogs are downloaded and active. Default: `false` (bool)
        """
        return pulumi.get(self, "wait_catalogs")

    @property
    @pulumi.getter(name="waitMonitoring")
    def wait_monitoring(self) -> pulumi.Output[Optional[bool]]:
        """
        Wait until monitoring is up and running. Default: `false` (bool)
        """
        return pulumi.get(self, "wait_monitoring")

