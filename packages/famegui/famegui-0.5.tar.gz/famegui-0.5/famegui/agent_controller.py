import logging
import typing

from PySide2 import QtCore

from famegui import models, colorpalette
from famegui.scenario_graph_view_items import AgentGraphItem


class AgentController(QtCore.QObject):
    """ Controller attached to a FAME Agent to sync it with the views """

    model_was_modified = QtCore.Signal()

    def __init__(self, agent: models.Agent):
        super().__init__()
        assert agent is not None
        self.model = agent
        self._scene_item = None
        self.tree_item = None

    @property
    def id(self) -> int:
        return self.model.id

    @property
    def id_str(self) -> str:
        return self.model.id_str

    @property
    def type_name(self) -> str:
        return self.model.type_name

    @property
    def attributes(self) -> typing.Dict[str, str]:
        return self.model.attributes

    @property
    def tooltip_text(self) -> str:
        text = "<font size='4'><b>{}</b></font>".format(self.model.type_name)

        text += "<table border=0 cellpadding=2 style='border-collapse: collapse'><tbody>"
        text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(
            "ID", self.model.id_str)
        for k, v in self.model.attributes.items():
            text += "<tr><td><b>{}</b></td><td>{}</td></tr>".format(k, v)

        text += "</tbody></table>"
        return text

    @property
    def svg_color(self) -> str:
        return colorpalette.color_for_agent_type(self.type_name)

    @property
    def x(self):
        assert self.model.display_xy is not None
        return self.model.display_xy[0]

    @property
    def y(self):
        assert self.model.display_xy is not None
        return self.model.display_xy[1]

    @property
    def scene_item(self) -> AgentGraphItem:
        assert self._scene_item is not None
        return self._scene_item

    def set_scene_item(self, item: AgentGraphItem):
        assert item.type() == AgentGraphItem.Type
        assert self._scene_item is None  # should be attached to an item only once
        self._scene_item = item
        self._scene_item.position_changed = lambda x, y: self._item_position_changed(
            x, y)

    def _item_position_changed(self, x: int, y: int):
        self.model.set_display_xy(x, y)
        self.model_was_modified.emit()
