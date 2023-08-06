from typing import Dict

from kama_sdk.model.concern.concern_view_adapter import ConcernViewAdapter


class ConcernCardAdapter(ConcernViewAdapter):

  def compute(self) -> Dict:
    return None