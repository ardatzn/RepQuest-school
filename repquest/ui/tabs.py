"""The Training, Progress and Hero tab roots. Their menu rows come from ``repquest.routes``."""

from __future__ import annotations

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen

from repquest import theme
from repquest.navigation import HERO, PROGRESS, TRAINING, Tab
from repquest.routes import MENUS
from repquest.ui.home import START_LEVEL, START_XP, XP_FOR_LEVEL_2
from repquest.ui.widgets import AvatarSlot, NavRowGroup, Panel, XpBar, child_page, label, tab_page, title


def _menu_groups(tab: Tab) -> list[NavRowGroup]:
    app = App.get_running_app()
    return [
        NavRowGroup(group.title, [(row.label, lambda screen=row.screen: app.open_screen(screen)) for row in group.rows])
        for group in MENUS[tab.key]
    ]


class MenuScreen(Screen):
    """A tab root with a headline and its menu groups, like the original Training and Progress tabs."""

    tab: Tab

    def __init__(self, **kwargs):
        kwargs.setdefault("name", self.tab.root)
        super().__init__(**kwargs)
        root, content = tab_page(self.tab.label)
        self.add_widget(root)
        self.groups = _menu_groups(self.tab)
        for group in self.groups:
            content.add_widget(group)


class TrainingScreen(MenuScreen):
    tab = TRAINING


class ProgressScreen(MenuScreen):
    tab = PROGRESS


class HeroScreen(Screen):
    """The Hero tab, laid out like the original Avatar Studio root: the large avatar, the game level, then the menu."""

    def __init__(self, **kwargs):
        kwargs.setdefault("name", HERO.root)
        super().__init__(**kwargs)
        root, content, self.top_bar = child_page("HERO")
        self.add_widget(root)

        avatar_box = AnchorLayout(size_hint_y=None, height=dp(200))
        avatar_box.add_widget(AvatarSlot(200))
        content.add_widget(avatar_box)

        facts = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(2))
        facts.add_widget(title(f"Game level {START_LEVEL}", theme.PROGRESSION, halign="center"))
        facts.add_widget(label("Fitness level: Not tested yet", theme.TEXT_BODY, halign="center"))
        facts.bind(minimum_height=facts.setter("height"))
        content.add_widget(facts)

        xp_card = Panel()
        xp_card.add_widget(XpBar(START_LEVEL, START_XP, XP_FOR_LEVEL_2))
        content.add_widget(xp_card)

        self.groups = _menu_groups(HERO)
        for group in self.groups:
            content.add_widget(group)
