from werkzeug.utils import cached_property

from kama_sdk.model.glance.glance import Glance


class GraphicAndTextGlance(Glance):

  @cached_property
  def view_type(self):
    return 'resource'

  @cached_property
  def line_one(self):
    return self.get_prop(LINE_ONE_KEY)

  @cached_property
  def line_two(self):
    return self.get_prop(LINE_TWO_KEY)

  @cached_property
  def line_three(self):
    return self.get_prop(LINE_THREE_KEY)

  @cached_property
  def graphic(self):
    return self.get_prop(GRAPHIC_KEY)

  @cached_property
  def graphic_type(self):
    return self.get_prop(GRAPHIC_TYPE_KEY, 'icon')

  @cached_property
  def graphic_emotion(self):
    return self.get_prop(GRAPHIC_EMOTION_KEY, 'primaryColor')

  @cached_property
  def small_graphic(self) -> bool:
    return self.get_prop(SMALL_GRAPHIC_KEY, False)

  def content_spec(self):
    return {
      'graphic_type': self.graphic_type,
      'graphic': self.graphic,
      'line_one': self.line_one,
      'small': self.small_graphic,
      'line_two': self.line_two,
      'line_three': self.line_three,
      'graphic_emotion': self.graphic_emotion
    }


LINE_ONE_KEY = 'line_one'
LINE_TWO_KEY = 'line_two'
LINE_THREE_KEY = 'line_three'
GRAPHIC_KEY = 'graphic'
GRAPHIC_TYPE_KEY = 'graphic_type'
GRAPHIC_EMOTION_KEY = 'graphic_emotion'
SMALL_GRAPHIC_KEY = 'small_graphic'
