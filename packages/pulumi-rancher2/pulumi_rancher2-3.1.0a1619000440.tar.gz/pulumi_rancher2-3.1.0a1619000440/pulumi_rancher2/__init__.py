# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

# Export this package's modules as members:
from .active_directory import *
from .app import *
from .app_v2 import *
from .auth_config_adfs import *
from .auth_config_azure_ad import *
from .auth_config_free_ipa import *
from .auth_config_github import *
from .auth_config_keycloak import *
from .auth_config_okta import *
from .auth_config_open_ldap import *
from .auth_config_ping import *
from .bootstrap import *
from .catalog import *
from .catalog_v2 import *
from .certificate import *
from .cloud_credential import *
from .cluster import *
from .cluster_alert_group import *
from .cluster_alert_rule import *
from .cluster_alter_group import *
from .cluster_alter_rule import *
from .cluster_driver import *
from .cluster_logging import *
from .cluster_role_template_binding import *
from .cluster_sync import *
from .cluster_template import *
from .etcd_backup import *
from .feature import *
from .get_app import *
from .get_catalog import *
from .get_catalog_v2 import *
from .get_certificate import *
from .get_cloud_credential import *
from .get_cluster import *
from .get_cluster_alert_group import *
from .get_cluster_alter_rule import *
from .get_cluster_driver import *
from .get_cluster_logging import *
from .get_cluster_role_template_binding import *
from .get_cluster_scan import *
from .get_cluster_template import *
from .get_etcd_backup import *
from .get_global_dns_provider import *
from .get_global_role import *
from .get_global_role_binding import *
from .get_multi_cluster_app import *
from .get_namespace import *
from .get_node_driver import *
from .get_node_pool import *
from .get_node_template import *
from .get_notifier import *
from .get_pod_security_policy_template import *
from .get_project import *
from .get_project_alert_group import *
from .get_project_alert_rule import *
from .get_project_logging import *
from .get_project_role_template_binding import *
from .get_registry import *
from .get_role_tempalte import *
from .get_role_template import *
from .get_secret import *
from .get_secret_v2 import *
from .get_setting import *
from .get_user import *
from .global_dns import *
from .global_dns_provider import *
from .global_role import *
from .global_role_binding import *
from .multi_cluster_app import *
from .namespace import *
from .node_driver import *
from .node_pool import *
from .node_template import *
from .notifier import *
from .pod_security_policy_template import *
from .project import *
from .project_alert_group import *
from .project_alert_rule import *
from .project_logging import *
from .project_role_template_binding import *
from .provider import *
from .registry import *
from .role_tempalte import *
from .secret import *
from .secret_v2 import *
from .setting import *
from .token import *
from .user import *
from ._inputs import *
from . import outputs

# Make subpackages available:
from . import (
    config,
)

def _register_module():
    import pulumi
    from . import _utilities


    class Module(pulumi.runtime.ResourceModule):
        _version = _utilities.get_semver_version()

        def version(self):
            return Module._version

        def construct(self, name: str, typ: str, urn: str) -> pulumi.Resource:
            if typ == "rancher2:index/activeDirectory:ActiveDirectory":
                return ActiveDirectory(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/app:App":
                return App(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/appV2:AppV2":
                return AppV2(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/authConfigAdfs:AuthConfigAdfs":
                return AuthConfigAdfs(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/authConfigAzureAd:AuthConfigAzureAd":
                return AuthConfigAzureAd(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/authConfigFreeIpa:AuthConfigFreeIpa":
                return AuthConfigFreeIpa(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/authConfigGithub:AuthConfigGithub":
                return AuthConfigGithub(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/authConfigKeycloak:AuthConfigKeycloak":
                return AuthConfigKeycloak(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/authConfigOkta:AuthConfigOkta":
                return AuthConfigOkta(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/authConfigOpenLdap:AuthConfigOpenLdap":
                return AuthConfigOpenLdap(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/authConfigPing:AuthConfigPing":
                return AuthConfigPing(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/bootstrap:Bootstrap":
                return Bootstrap(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/catalog:Catalog":
                return Catalog(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/catalogV2:CatalogV2":
                return CatalogV2(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/certificate:Certificate":
                return Certificate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/cloudCredential:CloudCredential":
                return CloudCredential(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/cluster:Cluster":
                return Cluster(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/clusterAlertGroup:ClusterAlertGroup":
                return ClusterAlertGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/clusterAlertRule:ClusterAlertRule":
                return ClusterAlertRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/clusterAlterGroup:ClusterAlterGroup":
                return ClusterAlterGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/clusterAlterRule:ClusterAlterRule":
                return ClusterAlterRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/clusterDriver:ClusterDriver":
                return ClusterDriver(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/clusterLogging:ClusterLogging":
                return ClusterLogging(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/clusterRoleTemplateBinding:ClusterRoleTemplateBinding":
                return ClusterRoleTemplateBinding(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/clusterSync:ClusterSync":
                return ClusterSync(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/clusterTemplate:ClusterTemplate":
                return ClusterTemplate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/etcdBackup:EtcdBackup":
                return EtcdBackup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/feature:Feature":
                return Feature(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/globalDns:GlobalDns":
                return GlobalDns(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/globalDnsProvider:GlobalDnsProvider":
                return GlobalDnsProvider(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/globalRole:GlobalRole":
                return GlobalRole(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/globalRoleBinding:GlobalRoleBinding":
                return GlobalRoleBinding(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/multiClusterApp:MultiClusterApp":
                return MultiClusterApp(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/namespace:Namespace":
                return Namespace(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/nodeDriver:NodeDriver":
                return NodeDriver(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/nodePool:NodePool":
                return NodePool(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/nodeTemplate:NodeTemplate":
                return NodeTemplate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/notifier:Notifier":
                return Notifier(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/podSecurityPolicyTemplate:PodSecurityPolicyTemplate":
                return PodSecurityPolicyTemplate(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/project:Project":
                return Project(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/projectAlertGroup:ProjectAlertGroup":
                return ProjectAlertGroup(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/projectAlertRule:ProjectAlertRule":
                return ProjectAlertRule(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/projectLogging:ProjectLogging":
                return ProjectLogging(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/projectRoleTemplateBinding:ProjectRoleTemplateBinding":
                return ProjectRoleTemplateBinding(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/registry:Registry":
                return Registry(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/roleTempalte:RoleTempalte":
                return RoleTempalte(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/secret:Secret":
                return Secret(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/secretV2:SecretV2":
                return SecretV2(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/setting:Setting":
                return Setting(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/token:Token":
                return Token(name, pulumi.ResourceOptions(urn=urn))
            elif typ == "rancher2:index/user:User":
                return User(name, pulumi.ResourceOptions(urn=urn))
            else:
                raise Exception(f"unknown resource type {typ}")


    _module_instance = Module()
    pulumi.runtime.register_resource_module("rancher2", "index/activeDirectory", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/app", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/appV2", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/authConfigAdfs", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/authConfigAzureAd", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/authConfigFreeIpa", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/authConfigGithub", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/authConfigKeycloak", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/authConfigOkta", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/authConfigOpenLdap", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/authConfigPing", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/bootstrap", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/catalog", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/catalogV2", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/certificate", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/cloudCredential", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/cluster", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/clusterAlertGroup", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/clusterAlertRule", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/clusterAlterGroup", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/clusterAlterRule", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/clusterDriver", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/clusterLogging", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/clusterRoleTemplateBinding", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/clusterSync", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/clusterTemplate", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/etcdBackup", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/feature", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/globalDns", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/globalDnsProvider", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/globalRole", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/globalRoleBinding", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/multiClusterApp", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/namespace", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/nodeDriver", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/nodePool", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/nodeTemplate", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/notifier", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/podSecurityPolicyTemplate", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/project", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/projectAlertGroup", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/projectAlertRule", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/projectLogging", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/projectRoleTemplateBinding", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/registry", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/roleTempalte", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/secret", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/secretV2", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/setting", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/token", _module_instance)
    pulumi.runtime.register_resource_module("rancher2", "index/user", _module_instance)


    class Package(pulumi.runtime.ResourcePackage):
        _version = _utilities.get_semver_version()

        def version(self):
            return Package._version

        def construct_provider(self, name: str, typ: str, urn: str) -> pulumi.ProviderResource:
            if typ != "pulumi:providers:rancher2":
                raise Exception(f"unknown provider type {typ}")
            return Provider(name, pulumi.ResourceOptions(urn=urn))


    pulumi.runtime.register_resource_package("rancher2", Package())

_register_module()
