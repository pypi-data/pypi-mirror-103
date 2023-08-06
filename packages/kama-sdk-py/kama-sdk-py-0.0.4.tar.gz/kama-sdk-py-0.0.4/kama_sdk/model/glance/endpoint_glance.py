from typing import Tuple, Optional

from werkzeug.utils import cached_property

from kama_sdk.core.core.types import EndpointDict
from kama_sdk.core.core.utils import pwar
from kama_sdk.model.glance import graphic_and_text_glance as prt_cls, glance
from kama_sdk.model.glance.graphic_and_text_glance import GraphicAndTextGlance


class EndpointGlance(GraphicAndTextGlance):

  @cached_property
  def title(self):
    return super(EndpointGlance, self).title or 'Webpage'

  @cached_property
  def line_two(self):
    if explicit := super(EndpointGlance, self).line_two:
      return explicit
    else:
      url = self.endpoint.get('url') if self.endpoint else None
      return url or 'No URL'

  @cached_property
  def line_three(self):
    if explicit := super(EndpointGlance, self).line_three:
      return explicit
    else:
      _type = self.endpoint.get('svc_type') if self.endpoint else None
      return _type or 'Type Unknown'

  @cached_property
  def url_intent(self) -> str:
    if explicit := super(EndpointGlance, self).url_intent:
      return explicit
    elif self.endpoint and self.endpoint.get('url'):
      return f"http://{self.endpoint.get('url')}"

  @cached_property
  def endpoint(self) -> Optional[EndpointDict]:
    try:
      return self.get_prop(ENDPOINT_DATA_KEY)
    except:
      pwar(self, "endpoint load failed", True)
      return None

  @cached_property
  def legend_type(self) -> str:
    if explicit := self.config.get(glance.LEGEND_TYPE_KEY):
      return explicit
    else:
      if self.is_working():
        return 'default'
      else:
        return 'status'

  @cached_property
  def legend_icon(self) -> str:
    if explicit := super(EndpointGlance, self).legend_icon:
      return explicit
    else:
      if self.is_working():
        return self.get_prop(ICON_CONNECTED_KEY, 'open_in_new')
      # else:
      #   return self.get_prop(ICON_NOT_CONNECTED_KEY, 'error_outline')

  @cached_property
  def legend_text(self) -> str:
    if explicit := super(EndpointGlance, self).legend_text:
      return explicit
    else:
      return 'Launch' if self.is_working() else 'Site Offline'

  @cached_property
  def legend_emotion(self) -> str:
    if explicit := self.config.get(glance.LEGEND_EMOTION_KEY):
      return explicit
    else:
      return 'primaryColor' if self.is_working() else 'warning2'

  def is_working(self) -> bool:
    if data := self.endpoint:
      return data.get('url') is not None
    else:
      return False

  @cached_property
  def port_forward_spec(self):
    if data := self.endpoint:
      return data.get('port_forward_spec')
    else:
      return None

  def graphic_and_type(self) -> Tuple[str, str]:
    exp_graphic = self.config.get(prt_cls.GRAPHIC_KEY)
    exp_graphic_type = self.config.get(prt_cls.GRAPHIC_TYPE_KEY)

    if exp_graphic:
      return exp_graphic, exp_graphic_type or 'image'
    else:
      return 'language', 'icon'

  @cached_property
  def graphic_type(self):
    return self.graphic_and_type()[1]

  @cached_property
  def graphic(self):
    return self.graphic_and_type()[0]

  def content_spec(self):
    self.patch({'endpoint': self.endpoint})
    return super(EndpointGlance, self).content_spec()


ENDPOINT_DATA_KEY = 'endpoint'
SITE_LOGO_KEY = 'site_logo'
ICON_CONNECTED_KEY = 'icon_not_connected'
ICON_NOT_CONNECTED_KEY = 'icon_not_connected'
