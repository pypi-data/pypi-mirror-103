import base64
import json
from typing import List, Dict

from flask import Blueprint, jsonify

from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern_view_adapter import ConcernViewAdapter
from kama_sdk.model.concern.concern_detail_adapter import ConcernDetailAdapter
from kama_sdk.model.concern.concern_set import ConcernSet
from kama_sdk.model.concern.concern_super_set import ConcernSuperSet
from kama_sdk.serializers import concern_ser

controller = Blueprint('concerns_controller', __name__)

BASE_PATH = '/api/concerns'
DETAIL_PATH = f'{BASE_PATH}/details/<b64_enc_reconstructor>'


@controller.route(f'{BASE_PATH}/super_sets/<super_set_id>')
def get_category_sets(super_set_id):
  super_set: ConcernSuperSet = ConcernSuperSet.inflate(super_set_id)
  if super_set:
    sets: List[ConcernSet] = super_set.concern_sets
    serialize = lambda s: concern_ser.serialize_set_meta(s)
    return jsonify(data=list(map(serialize, sets)))
  else:
    return jsonify({'error': f"no such category {super_set_id}"}), 400


@controller.route(f'{BASE_PATH}/sets/<concern_set_id>')
def get_set_meta(concern_set_id):
  concern_set: ConcernSet = ConcernSet.inflate(concern_set_id)
  if concern_set:
    meta = concern_ser.serialize_set_meta(concern_set, True)
    return jsonify(data=meta)
  else:
    return jsonify({'error': f"no such set {concern_set_id}"}), 400


@controller.route(f'{BASE_PATH}/sets/<concern_set_id>/data')
def get_set_data(concern_set_id):
  concern_set: ConcernSet = Model.inflate(concern_set_id)
  if concern_set:
    data = concern_set.one_shot_compute()
    return jsonify(data=data)
  else:
    return jsonify({'error': f"no such set {concern_set_id}"}), 400


@controller.route(f'{BASE_PATH}/cards/<b64_enc_str>')
def get_card(b64_enc_str):
  reconstructor = base64.b64decode(b64_enc_str)
  if adapter := ConcernDetailAdapter.reconstruct(reconstructor):
    data = adapter.compute()
    return jsonify(data=data)
  else:
    return jsonify({'error': f"no adapter", 'r': reconstructor}), 400


@controller.route(DETAIL_PATH)
def get_detail_meta(b64_enc_reconstructor):
  if adapter := get_adapter(b64_enc_reconstructor):
    serialized = concern_ser.ser_detail_meta(adapter)
    return jsonify(data=serialized)
  else:
    return jsonify({'error': f"no adapter"}), 400


@controller.route(f'{DETAIL_PATH}/data/<group_type>/<group_id>')
def get_detail_group_value(b64_enc_reconstructor, group_type, group_id):
  adapter: ConcernDetailAdapter = get_adapter(b64_enc_reconstructor)
  if adapter:
    data = adapter.compute_group_data(group_type, group_id)
    return jsonify(data=data)
  else:
    return jsonify({'error': f"no adapter"}), 400


def decode_seed(b64_enc_str: str) -> Dict:
  utc_str = base64.b64decode(b64_enc_str)
  return json.loads(utc_str)


def get_adapter(b64_enc_constructor: str):
  utf_reconstructor = base64.b64decode(b64_enc_constructor)
  reconstructor = json.loads(utf_reconstructor)
  return ConcernViewAdapter.reconstruct(reconstructor)
