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

__all__ = ['ClusterAlterGroupArgs', 'ClusterAlterGroup']

@pulumi.input_type
class ClusterAlterGroupArgs:
    def __init__(__self__, *,
                 cluster_id: pulumi.Input[str],
                 annotations: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 group_interval_seconds: Optional[pulumi.Input[int]] = None,
                 group_wait_seconds: Optional[pulumi.Input[int]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recipients: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterAlterGroupRecipientArgs']]]] = None,
                 repeat_interval_seconds: Optional[pulumi.Input[int]] = None):
        """
        The set of arguments for constructing a ClusterAlterGroup resource.
        :param pulumi.Input[str] cluster_id: Alert group Cluster ID
        :param pulumi.Input[Mapping[str, Any]] annotations: Annotations of the resource
        :param pulumi.Input[str] description: Alert group description
        :param pulumi.Input[int] group_interval_seconds: Alert group interval seconds
        :param pulumi.Input[int] group_wait_seconds: Alert group wait seconds
        :param pulumi.Input[Mapping[str, Any]] labels: Labels of the resource
        :param pulumi.Input[str] name: Alert group name
        :param pulumi.Input[Sequence[pulumi.Input['ClusterAlterGroupRecipientArgs']]] recipients: Alert group recipients
        :param pulumi.Input[int] repeat_interval_seconds: Alert group repeat interval seconds
        """
        pulumi.set(__self__, "cluster_id", cluster_id)
        if annotations is not None:
            pulumi.set(__self__, "annotations", annotations)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if group_interval_seconds is not None:
            pulumi.set(__self__, "group_interval_seconds", group_interval_seconds)
        if group_wait_seconds is not None:
            pulumi.set(__self__, "group_wait_seconds", group_wait_seconds)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if recipients is not None:
            pulumi.set(__self__, "recipients", recipients)
        if repeat_interval_seconds is not None:
            pulumi.set(__self__, "repeat_interval_seconds", repeat_interval_seconds)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> pulumi.Input[str]:
        """
        Alert group Cluster ID
        """
        return pulumi.get(self, "cluster_id")

    @cluster_id.setter
    def cluster_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "cluster_id", value)

    @property
    @pulumi.getter
    def annotations(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Annotations of the resource
        """
        return pulumi.get(self, "annotations")

    @annotations.setter
    def annotations(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "annotations", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Alert group description
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="groupIntervalSeconds")
    def group_interval_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Alert group interval seconds
        """
        return pulumi.get(self, "group_interval_seconds")

    @group_interval_seconds.setter
    def group_interval_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "group_interval_seconds", value)

    @property
    @pulumi.getter(name="groupWaitSeconds")
    def group_wait_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Alert group wait seconds
        """
        return pulumi.get(self, "group_wait_seconds")

    @group_wait_seconds.setter
    def group_wait_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "group_wait_seconds", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Labels of the resource
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Alert group name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def recipients(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterAlterGroupRecipientArgs']]]]:
        """
        Alert group recipients
        """
        return pulumi.get(self, "recipients")

    @recipients.setter
    def recipients(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterAlterGroupRecipientArgs']]]]):
        pulumi.set(self, "recipients", value)

    @property
    @pulumi.getter(name="repeatIntervalSeconds")
    def repeat_interval_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Alert group repeat interval seconds
        """
        return pulumi.get(self, "repeat_interval_seconds")

    @repeat_interval_seconds.setter
    def repeat_interval_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "repeat_interval_seconds", value)


@pulumi.input_type
class _ClusterAlterGroupState:
    def __init__(__self__, *,
                 annotations: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 group_interval_seconds: Optional[pulumi.Input[int]] = None,
                 group_wait_seconds: Optional[pulumi.Input[int]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recipients: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterAlterGroupRecipientArgs']]]] = None,
                 repeat_interval_seconds: Optional[pulumi.Input[int]] = None):
        """
        Input properties used for looking up and filtering ClusterAlterGroup resources.
        :param pulumi.Input[Mapping[str, Any]] annotations: Annotations of the resource
        :param pulumi.Input[str] cluster_id: Alert group Cluster ID
        :param pulumi.Input[str] description: Alert group description
        :param pulumi.Input[int] group_interval_seconds: Alert group interval seconds
        :param pulumi.Input[int] group_wait_seconds: Alert group wait seconds
        :param pulumi.Input[Mapping[str, Any]] labels: Labels of the resource
        :param pulumi.Input[str] name: Alert group name
        :param pulumi.Input[Sequence[pulumi.Input['ClusterAlterGroupRecipientArgs']]] recipients: Alert group recipients
        :param pulumi.Input[int] repeat_interval_seconds: Alert group repeat interval seconds
        """
        if annotations is not None:
            pulumi.set(__self__, "annotations", annotations)
        if cluster_id is not None:
            pulumi.set(__self__, "cluster_id", cluster_id)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if group_interval_seconds is not None:
            pulumi.set(__self__, "group_interval_seconds", group_interval_seconds)
        if group_wait_seconds is not None:
            pulumi.set(__self__, "group_wait_seconds", group_wait_seconds)
        if labels is not None:
            pulumi.set(__self__, "labels", labels)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if recipients is not None:
            pulumi.set(__self__, "recipients", recipients)
        if repeat_interval_seconds is not None:
            pulumi.set(__self__, "repeat_interval_seconds", repeat_interval_seconds)

    @property
    @pulumi.getter
    def annotations(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Annotations of the resource
        """
        return pulumi.get(self, "annotations")

    @annotations.setter
    def annotations(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "annotations", value)

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> Optional[pulumi.Input[str]]:
        """
        Alert group Cluster ID
        """
        return pulumi.get(self, "cluster_id")

    @cluster_id.setter
    def cluster_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "cluster_id", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Alert group description
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter(name="groupIntervalSeconds")
    def group_interval_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Alert group interval seconds
        """
        return pulumi.get(self, "group_interval_seconds")

    @group_interval_seconds.setter
    def group_interval_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "group_interval_seconds", value)

    @property
    @pulumi.getter(name="groupWaitSeconds")
    def group_wait_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Alert group wait seconds
        """
        return pulumi.get(self, "group_wait_seconds")

    @group_wait_seconds.setter
    def group_wait_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "group_wait_seconds", value)

    @property
    @pulumi.getter
    def labels(self) -> Optional[pulumi.Input[Mapping[str, Any]]]:
        """
        Labels of the resource
        """
        return pulumi.get(self, "labels")

    @labels.setter
    def labels(self, value: Optional[pulumi.Input[Mapping[str, Any]]]):
        pulumi.set(self, "labels", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Alert group name
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def recipients(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ClusterAlterGroupRecipientArgs']]]]:
        """
        Alert group recipients
        """
        return pulumi.get(self, "recipients")

    @recipients.setter
    def recipients(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ClusterAlterGroupRecipientArgs']]]]):
        pulumi.set(self, "recipients", value)

    @property
    @pulumi.getter(name="repeatIntervalSeconds")
    def repeat_interval_seconds(self) -> Optional[pulumi.Input[int]]:
        """
        Alert group repeat interval seconds
        """
        return pulumi.get(self, "repeat_interval_seconds")

    @repeat_interval_seconds.setter
    def repeat_interval_seconds(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "repeat_interval_seconds", value)


warnings.warn("""rancher2.ClusterAlterGroup has been deprecated in favor of rancher2.ClusterAlertGroup""", DeprecationWarning)


class ClusterAlterGroup(pulumi.CustomResource):
    warnings.warn("""rancher2.ClusterAlterGroup has been deprecated in favor of rancher2.ClusterAlertGroup""", DeprecationWarning)

    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 annotations: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 group_interval_seconds: Optional[pulumi.Input[int]] = None,
                 group_wait_seconds: Optional[pulumi.Input[int]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recipients: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterAlterGroupRecipientArgs']]]]] = None,
                 repeat_interval_seconds: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        """
        Create a ClusterAlterGroup resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, Any]] annotations: Annotations of the resource
        :param pulumi.Input[str] cluster_id: Alert group Cluster ID
        :param pulumi.Input[str] description: Alert group description
        :param pulumi.Input[int] group_interval_seconds: Alert group interval seconds
        :param pulumi.Input[int] group_wait_seconds: Alert group wait seconds
        :param pulumi.Input[Mapping[str, Any]] labels: Labels of the resource
        :param pulumi.Input[str] name: Alert group name
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterAlterGroupRecipientArgs']]]] recipients: Alert group recipients
        :param pulumi.Input[int] repeat_interval_seconds: Alert group repeat interval seconds
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ClusterAlterGroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Create a ClusterAlterGroup resource with the given unique name, props, and options.
        :param str resource_name: The name of the resource.
        :param ClusterAlterGroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ClusterAlterGroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 annotations: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 cluster_id: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 group_interval_seconds: Optional[pulumi.Input[int]] = None,
                 group_wait_seconds: Optional[pulumi.Input[int]] = None,
                 labels: Optional[pulumi.Input[Mapping[str, Any]]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 recipients: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterAlterGroupRecipientArgs']]]]] = None,
                 repeat_interval_seconds: Optional[pulumi.Input[int]] = None,
                 __props__=None):
        pulumi.log.warn("""ClusterAlterGroup is deprecated: rancher2.ClusterAlterGroup has been deprecated in favor of rancher2.ClusterAlertGroup""")
        if opts is None:
            opts = pulumi.ResourceOptions()
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.version is None:
            opts.version = _utilities.get_version()
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ClusterAlterGroupArgs.__new__(ClusterAlterGroupArgs)

            __props__.__dict__["annotations"] = annotations
            if cluster_id is None and not opts.urn:
                raise TypeError("Missing required property 'cluster_id'")
            __props__.__dict__["cluster_id"] = cluster_id
            __props__.__dict__["description"] = description
            __props__.__dict__["group_interval_seconds"] = group_interval_seconds
            __props__.__dict__["group_wait_seconds"] = group_wait_seconds
            __props__.__dict__["labels"] = labels
            __props__.__dict__["name"] = name
            __props__.__dict__["recipients"] = recipients
            __props__.__dict__["repeat_interval_seconds"] = repeat_interval_seconds
        super(ClusterAlterGroup, __self__).__init__(
            'rancher2:index/clusterAlterGroup:ClusterAlterGroup',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            annotations: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            cluster_id: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            group_interval_seconds: Optional[pulumi.Input[int]] = None,
            group_wait_seconds: Optional[pulumi.Input[int]] = None,
            labels: Optional[pulumi.Input[Mapping[str, Any]]] = None,
            name: Optional[pulumi.Input[str]] = None,
            recipients: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterAlterGroupRecipientArgs']]]]] = None,
            repeat_interval_seconds: Optional[pulumi.Input[int]] = None) -> 'ClusterAlterGroup':
        """
        Get an existing ClusterAlterGroup resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[Mapping[str, Any]] annotations: Annotations of the resource
        :param pulumi.Input[str] cluster_id: Alert group Cluster ID
        :param pulumi.Input[str] description: Alert group description
        :param pulumi.Input[int] group_interval_seconds: Alert group interval seconds
        :param pulumi.Input[int] group_wait_seconds: Alert group wait seconds
        :param pulumi.Input[Mapping[str, Any]] labels: Labels of the resource
        :param pulumi.Input[str] name: Alert group name
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['ClusterAlterGroupRecipientArgs']]]] recipients: Alert group recipients
        :param pulumi.Input[int] repeat_interval_seconds: Alert group repeat interval seconds
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ClusterAlterGroupState.__new__(_ClusterAlterGroupState)

        __props__.__dict__["annotations"] = annotations
        __props__.__dict__["cluster_id"] = cluster_id
        __props__.__dict__["description"] = description
        __props__.__dict__["group_interval_seconds"] = group_interval_seconds
        __props__.__dict__["group_wait_seconds"] = group_wait_seconds
        __props__.__dict__["labels"] = labels
        __props__.__dict__["name"] = name
        __props__.__dict__["recipients"] = recipients
        __props__.__dict__["repeat_interval_seconds"] = repeat_interval_seconds
        return ClusterAlterGroup(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def annotations(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        Annotations of the resource
        """
        return pulumi.get(self, "annotations")

    @property
    @pulumi.getter(name="clusterId")
    def cluster_id(self) -> pulumi.Output[str]:
        """
        Alert group Cluster ID
        """
        return pulumi.get(self, "cluster_id")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Alert group description
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="groupIntervalSeconds")
    def group_interval_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        Alert group interval seconds
        """
        return pulumi.get(self, "group_interval_seconds")

    @property
    @pulumi.getter(name="groupWaitSeconds")
    def group_wait_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        Alert group wait seconds
        """
        return pulumi.get(self, "group_wait_seconds")

    @property
    @pulumi.getter
    def labels(self) -> pulumi.Output[Mapping[str, Any]]:
        """
        Labels of the resource
        """
        return pulumi.get(self, "labels")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Alert group name
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def recipients(self) -> pulumi.Output[Optional[Sequence['outputs.ClusterAlterGroupRecipient']]]:
        """
        Alert group recipients
        """
        return pulumi.get(self, "recipients")

    @property
    @pulumi.getter(name="repeatIntervalSeconds")
    def repeat_interval_seconds(self) -> pulumi.Output[Optional[int]]:
        """
        Alert group repeat interval seconds
        """
        return pulumi.get(self, "repeat_interval_seconds")

