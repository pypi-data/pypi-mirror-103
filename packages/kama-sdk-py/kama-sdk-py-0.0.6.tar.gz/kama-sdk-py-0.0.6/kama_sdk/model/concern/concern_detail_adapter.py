from typing import List, Any, Dict

from kama_sdk.core.core.utils import pwar
from kama_sdk.model.action.base.action import Action
from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern_set import ConcernSet
from kama_sdk.model.concern.concern_view_adapter import ConcernViewAdapter
from kama_sdk.model.concern.concern_attr_adapter import ConcernAttrAdapter
from kama_sdk.model.operation.operation import Operation


class AttrPanelDescriptor(Model):

  def attr_adapters(self) -> List[ConcernAttrAdapter]:
    return self.inflate_children(
      ConcernAttrAdapter,
      prop=ATTRS_ADAPTERS_KEY,
    )

  def compute_values(self) -> Dict[str, Any]:
    return {a.label: a.compute_value() for a in self.attr_adapters()}


class ConcernDetailAdapter(ConcernViewAdapter):

  def attr_panel_descs(self) -> List[AttrPanelDescriptor]:
    return self.inflate_children(
      AttrPanelDescriptor,
      prop=ATTR_PANEL_DESCRIPTORS_KEY
    )

  def value_panel_descs(self) -> List[ConcernAttrAdapter]:
    return self.inflate_children(
      ConcernAttrAdapter,
      prop=VALUE_PANEL_DESCRIPTORS_KEY
    )

  def related_sets(self) -> List[ConcernSet]:
    return self.inflate_children(
      ConcernSet,
      prop=RELATED_SETS_KEY
    )

  def operations(self) -> List[Operation]:
    return self.inflate_children(
      Operation,
      prop=OPERATIONS_KEY
    )

  def actions(self) -> List[Action]:
    return self.inflate_children(
      Action,
      prop=OPERATIONS_KEY
    )

  def compute_group_data(self, group_type, group_id):
    if group_type == 'attr_panels':
      return self.compute_attr_panel_data(group_id)
    elif group_type == 'value_panels':
      return self.compute_value_panel_data(group_id)
    elif group_type == 'related_sets':
      return self.compute_related_set_data(group_id)

  def compute_attr_panel_data(self, group_id: str):
    finder = lambda p: p.id() == group_id
    if panel_model := next(filter(finder, self.attr_panel_descs())):
      return panel_model.compute_values()
    else:
      pwar(self, f"group {group_id} not found")
      return None

  def compute_value_panel_data(self, group_id: str):
    finder = lambda p: p.id() == group_id
    if panel_model := next(filter(finder, self.value_panel_descs())):
      return panel_model.compute_value()
    else:
      pwar(self, f"group {group_id} not found")
      return None

  def compute_related_set_data(self, group_id: str):
    finder = lambda p: p.id() == group_id
    if model := next(filter(finder, self.related_sets())):
      return model.one_shot_compute()
    else:
      pwar(self, f"group {group_id} not found")
      return None


ATTR_PANEL_DESCRIPTORS_KEY = 'attribute_panels'
VALUE_PANEL_DESCRIPTORS_KEY = 'value_panels'
ATTRS_ADAPTERS_KEY = 'attributes'
OPERATIONS_KEY = 'operations'
ACTIONS_KEY = 'actions'
RELATED_SETS_KEY = 'related_sets'
