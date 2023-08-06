from typing import Dict, Any, Optional, List, TypeVar

from werkzeug.utils import cached_property

from kama_sdk.core.core import utils
from kama_sdk.model.supplier.base import supplier
from kama_sdk.model.supplier.base.supplier import Supplier

T = TypeVar('T', bound='Predicate')

class Predicate(Supplier):

  @classmethod
  def inflate_with_literal(cls, expr: str, **kwargs) -> Optional[T]:
    operator, rest = expr.split("?")
    if '|' in rest:
      parts = rest.split('|')
      other_params = {
        CHECK_AGAINST_KEY: parts[1],
        CHALLENGE_KEY: parts[0]
      }
    else:
      other_params = {CHECK_AGAINST_KEY: rest}

    return cls.inflate_with_config({
      OPERATOR_KEY: operator,
      **other_params
    }, **kwargs)

  @cached_property
  def serializer_type(self) -> str:
    return supplier.SER_IDENTITY

  def many_policy(self) -> str:
    return self.resolve_prop(ON_MANY_KEY, lookback=0)

  def challenge(self) -> Any:
    # we need a new @wiz_property with custom caching logic
    return self.resolve_prop(CHALLENGE_KEY)

  def check_against(self) -> Optional[Any]:
    return self.resolve_prop(CHECK_AGAINST_KEY)

  def operator(self) -> str:
    return self.get_prop(OPERATOR_KEY, '==')

  def is_optimist(self) -> bool:
    return self.get_prop(IS_OPTIMISTIC_KEY, False)

  def is_pessimist(self) -> bool:
    return not self.is_optimist()

  def tone(self) -> str:
    return self.get_prop(TONE_KEY, 'error')

  def reason(self) -> str:
    return self.get_prop(REASON_KEY, '')

  def resolve(self) -> bool:
    return perform_comparison(
      self.operator(),
      self.challenge(),
      self.check_against(),
      self.many_policy()
    )

  def error_extras(self) -> Dict:
    return self.resolve_prop(ERROR_EXTRAS_KEY, depth=100) or {}


def perform_comparison(_name: str, challenge, against, on_many) -> bool:
  if utils.listlike(challenge) and on_many:
    run = lambda v: standard_comparison(_name, v, against)
    results: List[bool] = list(map(run, challenge))
    if on_many == 'each_true':
      return set(results) == {True}
    elif on_many == 'each_false':
      return set(results) == {False}
    elif on_many == 'some_true':
      return True in results
    elif on_many == 'some_false':
      return False in results
    else:
      print(f"[kama_sdk:predicate] bad many policy {on_many}")
  else:
    return standard_comparison(_name, challenge, against)


def standard_comparison(_name: str, challenge: Any, against: Any) -> bool:
  challenge = utils.unmuck_primitives(challenge)
  against = utils.unmuck_primitives(against)

  try:
    if _name in ['equals', 'equal', 'eq', '==', '=']:
      return challenge == against

    elif _name in ['not-equals', 'not-equal', 'neq', '!=', '=/=']:
      return not challenge == against

    elif _name in ['is-in', 'in']:
      return challenge in against

    elif _name in ['contains']:
      return against in challenge

    elif _name in ['only', 'contains-only']:
      return set(challenge) == {against}

    elif _name in ['is-greater-than', 'greater-than', 'gt', '>']:
      return challenge > against

    elif _name in ['gte', '>=']:
      return challenge >= against

    elif _name in ['is-less-than', 'less-than', 'lt', '<']:
      return challenge < against

    elif _name in ['lte', '<=']:
      return challenge <= against

    if _name in ['truthy', 'truthiness']:
      return utils.any2bool(challenge)

    elif _name in ['presence', 'defined', 'is-defined']:
      return bool(challenge)

    elif _name in ['undefined', 'is-undefined']:
      return not challenge

    print(f"Don't know operator {_name}")
    return False
  except:
    return False


CHALLENGE_KEY = 'challenge'
OPERATOR_KEY = 'operator'
CHECK_AGAINST_KEY = 'check_against'
ON_MANY_KEY = 'many_policy'
TONE_KEY = 'tone'
REASON_KEY = 'reason'
IS_OPTIMISTIC_KEY = 'optimistic'
TAGS = 'tags'
ERROR_EXTRAS_KEY = 'error_extras'
APP_STATUS_PRED_ID = 'sdk.predicate.app_status'

