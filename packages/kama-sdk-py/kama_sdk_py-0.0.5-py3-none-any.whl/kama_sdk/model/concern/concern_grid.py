from typing import List

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import Reconstructor
from kama_sdk.model.concern.concern_view_adapter import ConcernViewAdapter
from kama_sdk.model.concern.concern_card_adapter import ConcernCardAdapter
from kama_sdk.model.concern.concern_set import ConcernSet


class ConcernGrid(ConcernSet):

  def compute_partial(self):
    pass

  def compute_concern_seeds(self):
    return

  def compute_single(self, tuple_id: str):
    pass

  @cached_property
  def reconstructors(self) -> List[Reconstructor]:
    return self.get_prop(CARDS_KEY, [])

  def one_shot_compute(self):
    output = []
    for reconstructor in self.reconstructors:
      adapter = ConcernCardAdapter.reconstruct(reconstructor)
      output.append(adapter.compute())
    return output


  def compute(self):
    return {}

  @classmethod
  def view_type(cls) -> str:
    return 'grid'


CARDS_KEY = 'cards'