"""Small building blocks used by the shared screens and by every student screen."""

from __future__ import annotations

from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from repquest import theme


class TextBlock(Label):
    """A label that wraps to its width and grows to fit its text. Supports Kivy markup."""

    def __init__(self, text: str = "", font_size: float | None = None, color=theme.TEXT_BODY, **kwargs):
        kwargs.setdefault("markup", True)
        kwargs.setdefault("halign", "left")
        kwargs.setdefault("valign", "top")
        super().__init__(
            text=text,
            font_size=font_size if font_size is not None else sp(15),
            color=color,
            size_hint_y=None,
            **kwargs,
        )
        self.bind(width=self._wrap, texture_size=self._fit)

    def _wrap(self, *_args) -> None:
        self.text_size = (self.width, None)

    def _fit(self, *_args) -> None:
        self.height = self.texture_size[1]


def heading(text: str) -> TextBlock:
    """A screen title."""
    return TextBlock(text, font_size=sp(26), color=theme.TEXT_PRIMARY, bold=True)


def section_label(text: str) -> TextBlock:
    """A small upper-case section label, like the ones on the original RepQuest home screen."""
    return TextBlock(text.upper(), font_size=sp(13), color=theme.TEXT_SECONDARY, bold=True)


def caption(text: str) -> TextBlock:
    return TextBlock(text, font_size=sp(13), color=theme.TEXT_SECONDARY)


def bullet_list(items) -> TextBlock:
    return TextBlock("\n".join(f"•  {item}" for item in items))


def spacer(height: float = 8) -> Widget:
    return Widget(size_hint_y=None, height=dp(height))


class _RoundedBackground:
    """Mixin that paints a rounded rectangle behind the widget."""

    def _init_background(self, fill) -> None:
        with self.canvas.before:
            self._bg_color = Color(*fill)
            self._bg_rect = RoundedRectangle(radius=[dp(10)])
        self.bind(pos=self._redraw_background, size=self._redraw_background)

    def _redraw_background(self, *_args) -> None:
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size


class Card(_RoundedBackground, BoxLayout):
    """A rounded surface that grows to fit its children."""

    def __init__(self, fill=theme.SURFACE, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("padding", dp(14))
        kwargs.setdefault("spacing", dp(6))
        super().__init__(size_hint_y=None, **kwargs)
        self.bind(minimum_height=self.setter("height"))
        self._init_background(fill)


class MenuButton(_RoundedBackground, Button):
    """A full-width menu row. ``text`` may use markup and several lines."""

    def __init__(self, fill=theme.SURFACE, pressed=theme.SURFACE_VARIANT, **kwargs):
        kwargs.setdefault("markup", True)
        kwargs.setdefault("halign", "left")
        kwargs.setdefault("valign", "middle")
        kwargs.setdefault("font_size", sp(16))
        super().__init__(
            size_hint_y=None,
            background_normal="",
            background_down="",
            background_color=(0, 0, 0, 0),
            color=theme.TEXT_PRIMARY,
            padding=(0, dp(12)),
            **kwargs,
        )
        self._fill, self._pressed = fill, pressed
        self._init_background(fill)
        self.bind(width=self._wrap, texture_size=self._fit, state=self._show_state)

    def _wrap(self, *_args) -> None:
        self.text_size = (self.width - dp(32), None)

    def _fit(self, *_args) -> None:
        # texture_size already includes the vertical padding.
        self.height = max(dp(56), self.texture_size[1])

    def _show_state(self, *_args) -> None:
        self._bg_color.rgba = self._pressed if self.state == "down" else self._fill


def page(title: str, show_back: bool = True) -> tuple[BoxLayout, BoxLayout]:
    """A full screen with an optional header bar and a scrolling body. Returns (root, body)."""
    root = BoxLayout(orientation="vertical")
    if show_back:
        bar = BoxLayout(size_hint_y=None, height=dp(56), padding=(dp(8), dp(6)), spacing=dp(8))
        back = Button(
            text="‹  Home",
            size_hint_x=None,
            width=dp(104),
            font_size=sp(16),
            background_normal="",
            background_color=theme.SURFACE_VARIANT,
            color=theme.PRIMARY_LIGHT,
        )
        back.bind(on_release=lambda *_: App.get_running_app().go_home())
        bar.add_widget(back)
        title_label = Label(text=title, font_size=sp(16), color=theme.TEXT_SECONDARY, shorten=True,
                            shorten_from="right", halign="left", valign="middle")
        title_label.bind(size=lambda label, size: setattr(label, "text_size", size))
        bar.add_widget(title_label)
        root.add_widget(bar)
    scroll = ScrollView(do_scroll_x=False, bar_width=dp(4))
    body = BoxLayout(
        orientation="vertical",
        size_hint_y=None,
        padding=(dp(20), dp(16), dp(20), dp(28)),
        spacing=dp(12),
    )
    body.bind(minimum_height=body.setter("height"))
    scroll.add_widget(body)
    root.add_widget(scroll)
    return root, body
