from werkzeug.utils import cached_property

from kama_sdk.core.core.utils import any2bool
from kama_sdk.model.glance.graphic_and_text_glance import GraphicAndTextGlance
from kama_sdk.model.supplier.predicate.predicate import Predicate


class PredicateGlance(GraphicAndTextGlance):
  @cached_property
  def view_type(self) -> str:
    return "resource"

  @cached_property
  def predicate(self):
    return self.inflate_child(
      Predicate,
      prop=PREDICATE_KEY,
      resolve_kod=False
    )

  def eval_result(self) -> bool:
    return any2bool(self.predicate.resolve())

  def content_spec(self):
    success = self.eval_result()
    self.patch({'outcome': success})
    return super(PredicateGlance, self).content_spec()


PREDICATE_KEY = 'predicate'
