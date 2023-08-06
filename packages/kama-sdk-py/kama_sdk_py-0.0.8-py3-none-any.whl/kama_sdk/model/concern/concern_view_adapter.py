from typing import TypeVar

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import Reconstructor
from kama_sdk.model.base.model import Model
from kama_sdk.model.concern.concern import Concern
from kama_sdk.model.concern import concern as concern_module

T = TypeVar('T', bound='ConcernViewAdapter')


class ConcernViewAdapter(Model):

  @cached_property
  def concern_shell(self) -> Concern:
    return self.inflate_child(
      Concern,
      prop=CONCERN_SHELL_KEY
    )

  @classmethod
  def reconstruct(cls, reconstructor: Reconstructor):
    adapter: T = cls.inflate(reconstructor['adapter_ref'])
    concern = adapter.concern_shell.patch({
      concern_module.SEED_KEY: reconstructor['seed']
    })
    return adapter.patch({'concern': concern})


CONCERN_SHELL_KEY = 'concern_shell'
