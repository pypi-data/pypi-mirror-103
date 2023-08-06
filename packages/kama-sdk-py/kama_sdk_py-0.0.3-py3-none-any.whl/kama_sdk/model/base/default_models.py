def default_model_classes():
  from kama_sdk.model.supplier.base.misc_suppliers import FormattedDateSupplier
  from kama_sdk.model.variable.manifest_variable import ManifestVariable
  from kama_sdk.model.input.generic_input import GenericInput
  from kama_sdk.model.supplier.ext.misc.latest_vendor_injection_supplier import LatestVendorInjectionSupplier
  from kama_sdk.model.input.slider_input import SliderInput
  from kama_sdk.model.operation.operation import Operation
  from kama_sdk.model.operation.stage import Stage
  from kama_sdk.model.operation.step import Step
  from kama_sdk.model.operation.field import Field
  from kama_sdk.model.variable.generic_variable import GenericVariable
  from kama_sdk.model.supplier.ext.biz.resource_selector import ResourceSelector
  from kama_sdk.model.operation.operation_run_simulator import OperationRunSimulator
  from kama_sdk.model.action.base.multi_action import MultiAction
  from kama_sdk.model.input.checkboxes_input import CheckboxesInput
  from kama_sdk.model.input.checkboxes_input import CheckboxInput
  from kama_sdk.model.supplier.predicate.multi_predicate import MultiPredicate
  from kama_sdk.model.supplier.base.supplier import Supplier
  from kama_sdk.model.supplier.ext.misc.http_data_supplier import HttpDataSupplier
  from kama_sdk.model.supplier.ext.biz.resources_supplier import ResourcesSupplier
  from kama_sdk.model.input.checkboxes_input import SelectInput
  from kama_sdk.model.supplier.ext.misc.service_endpoint_supplier import ServiceEndpointSupplier
  from kama_sdk.model.supplier.ext.misc.random_string_supplier import RandomStringSupplier
  from kama_sdk.model.supplier.ext.biz.master_config_supplier import MasterConfigSupplier
  from kama_sdk.model.action.base.action import Action
  from kama_sdk.model.supplier.ext.prometheus.prom_vector_to_first_value_supplier import PromVectorToFirstValueSupplier
  from kama_sdk.model.supplier.ext.prometheus.prom_matrix_to_series_supplier import PromMatrixToSeriesSupplier
  from kama_sdk.model.humanizer.quantity_humanizer import QuantityHumanizer
  from kama_sdk.model.humanizer.cores_humanizer import CoresHumanizer
  from kama_sdk.model.humanizer.bytes_humanizer import BytesHumanizer
  from kama_sdk.model.action.ext.manifest.await_outkomes_settled_action import AwaitOutkomesSettledAction
  from kama_sdk.model.action.ext.manifest.await_predicates_settled_action import AwaitPredicatesSettledAction
  from kama_sdk.model.action.ext.manifest.kubectl_apply_action import KubectlApplyAction
  from kama_sdk.model.action.ext.manifest.template_manifest_action import TemplateManifestAction
  from kama_sdk.model.action.ext.update.update_actions import FetchUpdateAction
  from kama_sdk.model.action.ext.update.update_actions import CommitKteaFromUpdateAction
  from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicateAction
  from kama_sdk.model.action.ext.misc.run_predicates_action import RunPredicatesAction

  from kama_sdk.model.action.ext.misc.wait_action import WaitAction
  from kama_sdk.model.action.ext.misc.delete_resources_action import DeleteResourceAction
  from kama_sdk.model.action.ext.misc.delete_resources_action import DeleteResourcesAction
  from kama_sdk.model.action.ext.manifest.kubectl_dry_run_action import KubectlDryRunAction
  from kama_sdk.model.action.ext.misc.create_backup_action import CreateBackupAction
  from kama_sdk.model.supplier.base.props_supplier import PropsSupplier
  from kama_sdk.model.supplier.base.switch import Switch
  from kama_sdk.model.action.ext.update.fetch_latest_injection_action import FetchLatestInjectionsAction
  from kama_sdk.model.supplier.predicate.format_predicate import FormatPredicate
  from kama_sdk.model.supplier.predicate.common_predicates import TruePredicate
  from kama_sdk.model.supplier.predicate.common_predicates import FalsePredicate
  from kama_sdk.model.supplier.predicate.predicate import Predicate
  from kama_sdk.model.action.ext.manifest.patch_manifest_vars_action import PatchManifestVarsAction
  from kama_sdk.model.action.ext.update.update_actions import LoadVarDefaultsFromKtea
  from kama_sdk.model.action.ext.manifest.patch_manifest_vars_action import WriteManifestVarsAction
  from kama_sdk.model.supplier.base.misc_suppliers import SumSupplier
  from kama_sdk.model.supplier.base.misc_suppliers import MergeSupplier
  from kama_sdk.model.supplier.base.misc_suppliers import ListFlattener
  from kama_sdk.model.supplier.base.misc_suppliers import ListPluck
  from kama_sdk.model.supplier.base.misc_suppliers import IfThenElse
  from kama_sdk.model.supplier.ext.prometheus.prom_supplier import PromDataSupplier
  from kama_sdk.model.supplier.ext.misc.redactor import Redactor
  from kama_sdk.model.supplier.ext.vis.series_summary_supplier import SeriesSummarySupplier
  from kama_sdk.model.supplier.ext.vis.pod_statuses_supplier import PodStatusSummariesSupplier
  from kama_sdk.model.supplier.base.provider import Provider
  from kama_sdk.model.supplier.base.misc_suppliers import ListFilter
  from kama_sdk.model.concern.concern import Concern
  from kama_sdk.model.concern.concern_table import ConcernTable

  from kama_sdk.model.concern.concern_set import ConcernSet
  from kama_sdk.model.concern.concern_view_adapter import ConcernViewAdapter
  from kama_sdk.model.concern.concern_card_adapter import ConcernCardAdapter
  from kama_sdk.model.concern.concern_detail_adapter import ConcernDetailAdapter
  from kama_sdk.model.concern.concern_super_set import ConcernSuperSet
  from kama_sdk.model.concern.concern_grid import ConcernGrid
  from kama_sdk.model.concern.concern_attr_adapter import ConcernAttrAdapter

  return [
    Operation,
    Stage,
    Step,
    Field,

    GenericVariable,
    ManifestVariable,
    ResourceSelector,

    GenericInput,
    SliderInput,
    SelectInput,
    CheckboxesInput,
    CheckboxInput,

    Predicate,
    FormatPredicate,
    MultiPredicate,
    TruePredicate,
    FalsePredicate,

    Supplier,
    Provider,
    PropsSupplier,
    FormattedDateSupplier,
    Switch,
    MergeSupplier,
    HttpDataSupplier,
    ResourcesSupplier,
    RandomStringSupplier,
    MasterConfigSupplier,
    SumSupplier,
    ServiceEndpointSupplier,
    LatestVendorInjectionSupplier,
    ListFlattener,
    ListFilter,
    ListPluck,
    IfThenElse,
    Redactor,

    PromDataSupplier,
    PromMatrixToSeriesSupplier,
    PromVectorToFirstValueSupplier,
    SeriesSummarySupplier,
    PodStatusSummariesSupplier,

    Action,
    MultiAction,
    PatchManifestVarsAction,
    WriteManifestVarsAction,
    LoadVarDefaultsFromKtea,
    FetchLatestInjectionsAction,
    AwaitOutkomesSettledAction,
    AwaitPredicatesSettledAction,
    KubectlApplyAction,
    TemplateManifestAction,
    FetchUpdateAction,
    CommitKteaFromUpdateAction,
    RunPredicateAction,
    RunPredicatesAction,
    WaitAction,
    DeleteResourceAction,
    DeleteResourcesAction,
    KubectlDryRunAction,
    CreateBackupAction,

    Concern,
    ConcernSuperSet,
    ConcernSet,
    ConcernTable,
    ConcernGrid,
    ConcernViewAdapter,
    ConcernCardAdapter,
    ConcernDetailAdapter,
    ConcernAttrAdapter,

    QuantityHumanizer,
    BytesHumanizer,
    CoresHumanizer,

    OperationRunSimulator
  ]
