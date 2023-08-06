import base64
import json
from typing import Dict

from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern_attr_adapter import ConcernAttrAdapter
from kama_sdk.model.concern.concern_detail_adapter import ConcernDetailAdapter, AttrPanelDescriptor
from kama_sdk.model.concern.concern_set import ConcernSet
from kama_sdk.model.concern.concern_table import ConcernTable

def encode_seed(seed_dict: Dict) -> str:
  utf_json = json.dumps(seed_dict)
  return base64.b64encode(utf_json)


def ser_simple_child(model: Model) -> Dict:
  return {
    'id': model.id(),
    'title': model.title,
    'info': model.info
  }


def ser_attr_meta(model: ConcernAttrAdapter) -> Dict:
  return {
    'label': model.label,
    'title': model.title,
    'info': model.info
  }


def ser_attr_panel(model: AttrPanelDescriptor) -> Dict:
  return {
    **ser_simple_child(model),
    'attributes': list(map(ser_attr_meta, model.attr_adapters()))
  }


def serialize_set_meta(concern_set: ConcernSet, seeds=False):
  bundle = {
    **ser_simple_child(concern_set),
    'one_shot': concern_set.is_one_shot,
    'view_type': concern_set.view_type()
  }

  serialized_cols = None
  serialized_seeds = None

  if isinstance(concern_set, ConcernTable):
    serialized_cols = concern_set.column_definitions

  if seeds and concern_set.is_one_shot:
    seeds = concern_set.compute_concern_seeds()
    serialized_seeds = list(map(encode_seed, seeds))

  bundle['columns'] = serialized_cols
  bundle['seeds'] = serialized_seeds

  return bundle


def ser_detail_meta(adapter: ConcernDetailAdapter) -> Dict:
  attr_panel_descs = adapter.attr_panel_descs()
  value_panel_descs = adapter.value_panel_descs()
  related_set_descs = adapter.related_sets()

  return {
    'id': adapter.id(),
    'title': adapter.title,
    'info': adapter.info,
    'attr_panels': list(map(ser_attr_panel, attr_panel_descs)),
    'value_panels': list(map(ser_simple_child, value_panel_descs)),
    'related_sets': list(map(serialize_set_meta, related_set_descs)),
    'actions': list(map(ser_simple_child, adapter.actions())),
    'operations': list(map(ser_simple_child, adapter.operations()))
  }
