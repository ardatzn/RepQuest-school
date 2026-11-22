"""Building blocks shared by every screen, modelled on the original RepQuest components.

Cards and buttons have sharp corners, a 1dp border and the dark palette from ``repquest.theme``. Text uses the
monospace type scale. Student screens can use these widgets too.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

from kivy.app import App
from kivy.core.text import Label as CoreLabel
from kivy.core.window import Window
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp
from kivy.properties import BooleanProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget

from repquest import theme
from repquest.navigation import TABS

_font_ready = False
_line_ratio = 1.17


def ensure_font() -> None:
    """Registers the monospace font once and measures its natural line height."""
    global _font_ready, _line_ratio
    if _font_ready:
        return
    theme.register_font()
    probe = CoreLabel(text="Ag", font_name=theme.FONT_NAME, font_size=100)
    probe.refresh()
    if probe.texture is not None and probe.texture.height:
        _line_ratio = probe.texture.height / 100
    _font_ready = True


def _line_height(style: theme.TextStyle) -> float:
    return max(1.0, theme.font_px(style.line_height) / (theme.font_px(style.size) * _line_ratio))


# --------------------------------------------------------------------------------------------------------------------
# Text


class Text(Label):
    """Text in one of the theme styles. With ``wrap`` it fills its width and grows to fit; otherwise it sizes itself."""

    def __init__(self, text: str = "", style: theme.TextStyle = theme.BODY, color=theme.TEXT_BODY, wrap: bool = True,
                 **kwargs):
        ensure_font()
        kwargs.setdefault("markup", True)
        kwargs.setdefault("halign", "left")
        kwargs.setdefault("valign", "middle")
        super().__init__(
            text=text,
            font_name=theme.FONT_NAME,
            font_size=theme.font_px(style.size),
            bold=style.bold,
            line_height=_line_height(style),
            color=color,
            **kwargs,
        )
        self._wrap = wrap
        if style.bold and theme.fake_bold:
            # A 1px stroke on each side, close to the stroke Android adds for fake bold.
            self.outline_width = max(1, round(self.font_size / 64))
            self.outline_color = self.color[:3]
            self.bind(color=lambda *_: setattr(self, "outline_color", self.color[:3]))
        if wrap:
            self.size_hint_y = None
            self.bind(width=self._wrap_to_width, texture_size=self._fit_height)
        else:
            self.size_hint = (None, None)
            self.bind(texture_size=self.setter("size"))

    def _wrap_to_width(self, *_args) -> None:
        self.text_size = (self.width, None)

    def _fit_height(self, *_args) -> None:
        # The fake-bold outline widens the texture; the line keeps the style's line height.
        self.height = self.texture_size[1] - 2 * (self.outline_width or 0)


def headline(text: str, **kwargs) -> Text:
    return Text(text, theme.HEADLINE, theme.TEXT_PRIMARY, **kwargs)


def title(text: str, color=theme.TEXT_PRIMARY, **kwargs) -> Text:
    return Text(text, theme.TITLE, color, **kwargs)


def body(text: str, color=theme.TEXT_BODY, **kwargs) -> Text:
    return Text(text, theme.BODY, color, **kwargs)


def label(text: str, color=theme.TEXT_BODY, **kwargs) -> Text:
    return Text(text, theme.LABEL, color, **kwargs)


def caption(text: str, color=theme.TEXT_SECONDARY, **kwargs) -> Text:
    return Text(text, theme.CAPTION, color, **kwargs)


def bullet_list(items: Sequence[str]) -> BoxLayout:
    """One row per item, with wrapped lines indented under the text, not under the bullet."""
    box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(4))
    for item in items:
        row = BoxLayout(size_hint_y=None, spacing=dp(4))
        row.add_widget(Text("·", theme.BODY, theme.TEXT_SECONDARY, size_hint_x=None, width=theme.font_px(20), halign="center",
                            pos_hint={"top": 1}))
        text = body(item)
        row.add_widget(text)
        text.bind(height=lambda _text, height, row=row: setattr(row, "height", height))
        box.add_widget(row)
    box.bind(minimum_height=box.setter("height"))
    return box


def spacer(height: float = 8) -> Widget:
    return Widget(size_hint_y=None, height=dp(height))


def padded(widget: Widget, top: float = 0, bottom: float = 0) -> BoxLayout:
    """``widget`` with extra space above and below it, in dp."""
    box = BoxLayout(orientation="vertical", size_hint_y=None, padding=(0, dp(top), 0, dp(bottom)))
    box.add_widget(widget)
    box.bind(minimum_height=box.setter("height"))
    return box


class Wordmark(BoxLayout):
    """The REPQUEST wordmark: bold monospace with 4sp letter spacing."""

    def __init__(self, text: str = "REPQUEST", **kwargs):
        super().__init__(orientation="horizontal", size_hint=(None, None), spacing=theme.font_px(theme.WORDMARK_LETTER_SPACING),
                         **kwargs)
        self.text = text
        for letter in text:
            self.add_widget(Text(letter, theme.WORDMARK, theme.TEXT_PRIMARY, wrap=False))
        self.bind(minimum_width=self.setter("width"), minimum_height=self.setter("height"))


# --------------------------------------------------------------------------------------------------------------------
# Surfaces


class Surface:
    """Mixin that paints a fill with a sharp border behind the widget."""

    def init_surface(self, fill, border=None, border_width: float = 1) -> None:
        with self.canvas.before:
            self._border_color = Color(*(border or fill))
            self._border_rect = Rectangle()
            self._fill_color = Color(*fill)
            self._fill_rect = Rectangle()
        self._border_width = dp(border_width) if border else 0
        self.bind(pos=self._redraw_surface, size=self._redraw_surface)

    def set_surface(self, fill=None, border=None, border_width: float | None = None) -> None:
        if fill is not None:
            self._fill_color.rgba = fill
        if border is not None:
            self._border_color.rgba = border
        if border_width is not None:
            self._border_width = dp(border_width)
        self._redraw_surface()

    def _redraw_surface(self, *_args) -> None:
        b = self._border_width
        self._border_rect.pos, self._border_rect.size = self.pos, self.size
        self._fill_rect.pos = (self.x + b, self.y + b)
        self._fill_rect.size = (max(0, self.width - 2 * b), max(0, self.height - 2 * b))


class Panel(Surface, BoxLayout):
    """A card: surface fill, 1dp border, 12dp padding, 8dp spacing. Grows to fit its children."""

    def __init__(self, fill=theme.SURFACE, border=theme.DIVIDER, **kwargs):
        kwargs.setdefault("orientation", "vertical")
        kwargs.setdefault("padding", dp(12))
        kwargs.setdefault("spacing", dp(8))
        super().__init__(size_hint_y=None, **kwargs)
        self.bind(minimum_height=self.setter("height"))
        self.init_surface(fill, border)


class Divider(Widget):
    def __init__(self, color=theme.DIVIDER, **kwargs):
        super().__init__(size_hint_y=None, height=dp(1), **kwargs)
        with self.canvas:
            Color(*color)
            self._rect = Rectangle()
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_args) -> None:
        self._rect.pos, self._rect.size = self.pos, self.size


# --------------------------------------------------------------------------------------------------------------------
# Icons, drawn with lines so they never depend on a font


class Icon(Widget):
    """A line icon in a square box. ``kind`` is one of: chevron_right, back, person."""

    def __init__(self, kind: str, size: float = 24, color=theme.TEXT_SECONDARY, **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(size), dp(size)), **kwargs)
        self.kind = kind
        with self.canvas:
            self._color = Color(*color)
        self._lines: list[Line] = []
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_args) -> None:
        for line in self._lines:
            self.canvas.remove(line)
        x, y, s = self.x, self.y, self.width
        stroke = max(1.0, s / 14)

        def point(px: float, py: float) -> tuple[float, float]:  # 0..1 from the top-left corner
            return x + px * s, y + (1 - py) * s

        if self.kind == "chevron_right":
            shapes = [[*point(0.38, 0.25), *point(0.62, 0.5), *point(0.38, 0.75)]]
        elif self.kind == "back":
            shapes = [[*point(0.2, 0.5), *point(0.82, 0.5)], [*point(0.5, 0.2), *point(0.2, 0.5), *point(0.5, 0.8)]]
        else:  # person
            shapes = []
        with self.canvas:
            self._lines = [Line(points=points, width=stroke, joint="miter", cap="square") for points in shapes]
            if self.kind == "person":
                cx, cy = point(0.5, 0.33)
                self._lines.append(Line(circle=(cx, cy, s * 0.17), width=stroke))
                bx, by = point(0.5, 0.95)
                self._lines.append(Line(ellipse=(bx - s * 0.32, by, s * 0.64, s * 0.5, -90, 90), width=stroke))


class PixelHero(Widget):
    """A simple pixel-art lifter for the avatar slot. A placeholder until Duru's avatar feature draws the real one."""

    PIXELS = (
        "....hhhh....",
        "...hhhhhh...",
        "...hssssh...",
        "...sesses...",
        "...ssssss...",
        "....ssss....",
        "..bbbbbbbb..",
        ".sbbbbbbbbs.",
        ".sbbbbbbbbs.",
        ".s.bbbbbb.s.",
        "...dddddd...",
        "...dddddd...",
        "...dd..dd...",
        "...ss..ss...",
        "...ss..ss...",
        "..www..www..",
    )
    PALETTE = {
        "h": (0.20, 0.16, 0.16, 1),
        "s": (0.88, 0.66, 0.47, 1),
        "e": theme.BACKGROUND,
        "b": theme.PRIMARY,
        "d": (0.28, 0.31, 0.35, 1),
        "w": theme.TEXT_PRIMARY,
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_args) -> None:
        self.canvas.clear()
        rows, cols = len(self.PIXELS), len(self.PIXELS[0])
        cell = int(min(self.width / cols, self.height / rows))
        if cell <= 0:
            return
        left = self.x + (self.width - cell * cols) / 2
        top = self.y + (self.height + cell * rows) / 2
        with self.canvas:
            for r, row in enumerate(self.PIXELS):
                for c, key in enumerate(row):
                    if key in self.PALETTE:
                        Color(*self.PALETTE[key])
                        Rectangle(pos=(left + c * cell, top - (r + 1) * cell), size=(cell, cell))


class AvatarSlot(Surface, Widget):
    """The square avatar frame of the original app with the placeholder hero inside."""

    def __init__(self, size: float = 72, **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(size), dp(size)), **kwargs)
        self.init_surface(theme.SURFACE_VARIANT, theme.DIVIDER)
        self._hero = PixelHero()
        self.add_widget(self._hero)
        self.bind(pos=self._place, size=self._place)

    def _place(self, *_args) -> None:
        inset = self.width * 0.16
        self._hero.pos = (self.x + inset, self.y + inset)
        self._hero.size = (self.width - 2 * inset, self.height - 2 * inset)


class FlowRow(BoxLayout):
    """Children side by side, the first at the left and the rest at the right, while they fit on one line.

    When they don't fit, each child takes its own line, like the FlowRow of the original app. Children keep their
    natural width (``size_hint_x=None``).
    """

    def __init__(self, items: Sequence[Widget], spacing: float = 8, **kwargs):
        super().__init__(size_hint_y=None, **kwargs)
        self.items = list(items)
        self._gap = dp(spacing)
        self.bind(width=self._arrange)
        for item in self.items:
            item.bind(size=self._arrange)
        self._arrange()

    def _arrange(self, *_args) -> None:
        needed = sum(item.width for item in self.items) + self._gap * (len(self.items) - 1)
        one_line = needed <= self.width or self.width <= 1
        self.clear_widgets()
        if one_line:
            self.orientation = "horizontal"
            self.spacing = 0
            for index, item in enumerate(self.items):
                if index == 1:
                    self.add_widget(Widget())
                item.pos_hint = {"center_y": 0.5}
                self.add_widget(item)
            self.height = max(item.height for item in self.items)
        else:
            self.orientation = "vertical"
            self.spacing = dp(2)
            for item in self.items:
                item.pos_hint = {"x": 0}
                self.add_widget(item)
            self.height = sum(item.height for item in self.items) + self.spacing * (len(self.items) - 1)


class XpBar(BoxLayout):
    """``XP to level N   x / y XP`` above a 14dp bar with a purple fill."""

    def __init__(self, level: int, xp_into_level: int, xp_for_next_level: int, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, spacing=dp(4), **kwargs)
        self.add_widget(FlowRow([
            label(f"XP to level {level + 1}", wrap=False),
            label(f"{xp_into_level} / {xp_for_next_level} XP", theme.PROGRESSION, wrap=False),
        ]))
        self._fraction = max(0.0, min(1.0, xp_into_level / xp_for_next_level)) if xp_for_next_level else 0.0
        self.add_widget(_Bar(self._fraction))
        self.bind(minimum_height=self.setter("height"))


class _Bar(Surface, Widget):
    def __init__(self, fraction: float, **kwargs):
        super().__init__(size_hint_y=None, height=dp(14), **kwargs)
        self.init_surface(theme.BACKGROUND, theme.OUTLINE)
        self.fraction = fraction
        with self.canvas:
            Color(*theme.PROGRESSION)
            self._fill = Rectangle()
        self.bind(pos=self._redraw_fill, size=self._redraw_fill)

    def _redraw_fill(self, *_args) -> None:
        b = dp(1)
        self._fill.pos = (self.x + b, self.y + b)
        self._fill.size = (max(0, (self.width - 2 * b) * self.fraction), max(0, self.height - 2 * b))


# --------------------------------------------------------------------------------------------------------------------
# Buttons and menu rows


class QuestButton(Surface, ButtonBehavior, BoxLayout):
    """The original PrimaryButton (blue fill) or SecondaryButton (outlined): sharp, at least 48dp tall."""

    def __init__(self, text: str, primary: bool = False, on_release: Callable[[], None] | None = None, **kwargs):
        super().__init__(size_hint_y=None, padding=(dp(16), dp(12)), **kwargs)
        self.primary = primary
        self._fill = theme.PRIMARY if primary else theme.SURFACE
        self._pressed = theme.PRIMARY_PRESSED if primary else theme.SURFACE_VARIANT
        self.init_surface(self._fill, theme.PRIMARY_LIGHT)
        self.label = Text(text, theme.BUTTON, theme.TEXT_PRIMARY if primary else theme.PRIMARY_LIGHT, halign="center")
        self.add_widget(self.label)
        self.label.bind(height=self._fit)
        self._fit()
        self.bind(state=lambda *_: self.set_surface(fill=self._pressed if self.state == "down" else self._fill))
        if on_release is not None:
            self.bind(on_release=lambda *_: on_release())

    @property
    def text(self) -> str:
        return self.label.text

    def _fit(self, *_args) -> None:
        self.height = max(dp(48), self.label.height + dp(24))


class TextButton(ButtonBehavior, BoxLayout):
    """A borderless text action such as ``Avatar Studio`` on the Home progress card."""

    def __init__(self, text: str, on_release: Callable[[], None] | None = None, **kwargs):
        super().__init__(size_hint=(None, None), padding=(dp(8), dp(8)), **kwargs)
        self.label = Text(text, theme.BUTTON, theme.PRIMARY_LIGHT, wrap=False)
        self.add_widget(self.label)
        self.label.bind(size=self._fit)
        self._fit()
        if on_release is not None:
            self.bind(on_release=lambda *_: on_release())

    @property
    def text(self) -> str:
        return self.label.text

    def _fit(self, *_args) -> None:
        self.width = self.label.width + dp(16)
        self.height = max(dp(48), self.label.height + dp(16))


class NavRow(Surface, ButtonBehavior, BoxLayout):
    """One menu row: a title-sized label and a chevron, at least 56dp tall."""

    def __init__(self, text: str, on_release: Callable[[], None] | None = None, **kwargs):
        super().__init__(size_hint_y=None, padding=(dp(16), dp(14)), spacing=dp(8), **kwargs)
        self.init_surface(theme.SURFACE)
        self.label = title(text)
        self.add_widget(self.label)
        chevron_box = BoxLayout(size_hint=(None, 1), width=dp(20))
        chevron_box.add_widget(Widget())
        chevron_box.add_widget(Icon("chevron_right", 20))
        chevron_box.add_widget(Widget())
        chevron_box.orientation = "vertical"
        self.add_widget(chevron_box)
        self.label.bind(height=self._fit)
        self._fit()
        self.bind(state=lambda *_: self.set_surface(fill=theme.SURFACE_VARIANT if self.state == "down" else theme.SURFACE))
        if on_release is not None:
            self.bind(on_release=lambda *_: on_release())

    @property
    def text(self) -> str:
        return self.label.text

    def _fit(self, *_args) -> None:
        self.height = max(dp(56), self.label.height + dp(28))


class NavRowGroup(BoxLayout):
    """A captioned group of menu rows in one bordered card, like the Training and Progress menus of the original."""

    def __init__(self, group_title: str, rows: Sequence[tuple[str, Callable[[], None]]], **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, spacing=dp(8), **kwargs)
        self.title = group_title
        heading_box = BoxLayout(size_hint_y=None, padding=(dp(4), 0))
        heading_label = caption(group_title)
        heading_box.add_widget(heading_label)
        heading_label.bind(height=lambda *_: setattr(heading_box, "height", heading_label.height))
        self.add_widget(heading_box)

        card = Panel(padding=dp(1), spacing=0)
        self.rows: list[NavRow] = []
        for index, (text, callback) in enumerate(rows):
            if index:
                card.add_widget(Divider())
            row = NavRow(text, callback)
            self.rows.append(row)
            card.add_widget(row)
        self.add_widget(card)
        self.bind(minimum_height=self.setter("height"))


class IconButton(ButtonBehavior, BoxLayout):
    """A 48dp touch target with a 24dp line icon."""

    def __init__(self, kind: str, color=theme.TEXT_PRIMARY, on_release: Callable[[], None] | None = None, **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(48), dp(48)), padding=dp(12), **kwargs)
        self.add_widget(Icon(kind, 24, color))
        if on_release is not None:
            self.bind(on_release=lambda *_: on_release())


# --------------------------------------------------------------------------------------------------------------------
# Page layouts


class TopBar(BoxLayout):
    """A child screen's header: a 48dp Back arrow and the headline title, with an optional line under the title."""

    def __init__(self, title_text: str, on_back: Callable[[], None], subtitle: str | None = None, **kwargs):
        super().__init__(orientation="horizontal", size_hint_y=None, padding=(0, dp(8)), spacing=dp(8), **kwargs)
        arrow_column = BoxLayout(orientation="vertical", size_hint_x=None, width=dp(48))
        self.back_button = IconButton("back", theme.TEXT_PRIMARY, on_back)
        arrow_column.add_widget(self.back_button)
        arrow_column.add_widget(Widget())
        self.add_widget(arrow_column)

        texts = BoxLayout(orientation="vertical", size_hint_y=None, spacing=dp(2), padding=(0, dp(8), 0, 0),
                          pos_hint={"top": 1})
        self.title_label = headline(title_text)
        texts.add_widget(self.title_label)
        self.subtitle_label = None
        if subtitle:
            self.subtitle_label = label(subtitle, theme.TEXT_BODY)
            texts.add_widget(self.subtitle_label)
        texts.bind(minimum_height=texts.setter("height"))
        self.add_widget(texts)
        texts.bind(height=self._fit)
        self._texts = texts
        self._fit()

    def _fit(self, *_args) -> None:
        self.height = max(dp(48), self._texts.height) + dp(16)


def _scroll_body(padding, spacing: float = 16) -> tuple[ScrollView, BoxLayout]:
    scroll = ScrollView(do_scroll_x=False, bar_width=dp(4), bar_color=theme.DIVIDER, bar_inactive_color=theme.DIVIDER)
    content = BoxLayout(orientation="vertical", size_hint_y=None, padding=padding, spacing=dp(spacing))
    content.bind(minimum_height=content.setter("height"))
    scroll.add_widget(content)
    return scroll, content


def tab_page(page_title: str | None = None) -> tuple[Widget, BoxLayout]:
    """A tab's root screen: one scrolling column with 16dp padding and spacing, headed by ``page_title``."""
    scroll, content = _scroll_body(dp(16))
    if page_title:
        # The original pads the headline 8dp above and 4dp below; Kivy places one-line text slightly lower in its
        # line, so 0dp below gives the same measured position for the first menu group.
        content.add_widget(padded(headline(page_title), top=8, bottom=0))
    return scroll, content


def child_page(page_title: str, on_back: Callable[[], None] | None = None,
               subtitle: str | None = None) -> tuple[Widget, BoxLayout, TopBar]:
    """A screen opened from a menu: a fixed top bar with Back, then a scrolling column. Returns (root, body, bar)."""
    if on_back is None:
        def on_back() -> None:
            App.get_running_app().go_back()
    root = BoxLayout(orientation="vertical", padding=(dp(16), dp(8), dp(16), 0))
    bar = TopBar(page_title, on_back, subtitle)
    root.add_widget(bar)
    root.add_widget(spacer(8))
    scroll, content = _scroll_body((0, 0, 0, dp(16)))
    root.add_widget(scroll)
    return root, content, bar


# --------------------------------------------------------------------------------------------------------------------
# Bottom navigation


class TabItem(Surface, ButtonBehavior, BoxLayout):
    selected = BooleanProperty(False)

    def __init__(self, tab_key: str, text: str, **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, padding=(dp(8), dp(8)), spacing=dp(4), **kwargs)
        self.tab_key = tab_key
        self.init_surface(theme.SURFACE)
        # The layout guarantees a one-line label in the row and grid; only the column fallback wraps it.
        self.label = Text(text, theme.LABEL, theme.TEXT_SECONDARY, halign="center", wrap=True)
        self.add_widget(self.label)
        indicator_row = BoxLayout(size_hint_y=None, height=dp(2))
        indicator_row.add_widget(Widget())
        self.indicator = _Indicator()
        indicator_row.add_widget(self.indicator)
        indicator_row.add_widget(Widget())
        self.add_widget(indicator_row)
        self.label.bind(height=self._fit)
        self.bind(selected=self._show_selected)
        self._fit()
        self._show_selected()

    @property
    def text(self) -> str:
        return self.label.text

    def _fit(self, *_args) -> None:
        self.height = max(dp(56), self.label.height + dp(2) + dp(4) + dp(16))

    def _show_selected(self, *_args) -> None:
        self.set_surface(fill=theme.SURFACE_VARIANT if self.selected else theme.SURFACE)
        self.label.color = theme.TEXT_PRIMARY if self.selected else theme.TEXT_SECONDARY
        self.indicator.set_surface(fill=theme.PRIMARY_LIGHT if self.selected else theme.SURFACE_VARIANT[:3] + (0,))


class _Indicator(Surface, Widget):
    def __init__(self, **kwargs):
        super().__init__(size_hint=(None, None), size=(dp(28), dp(2)), **kwargs)
        self.init_surface((0, 0, 0, 0))


def choose_bar_layout(widest_label_px: float, available_px: float, item_padding_px: float) -> str:
    """The widest arrangement in which every tab label fits on one line: ``row``, ``grid`` (2x2) or ``column``."""
    if widest_label_px + item_padding_px <= available_px / 4:
        return "row"
    if widest_label_px + item_padding_px <= available_px / 2:
        return "grid"
    return "column"


class BottomBar(Surface, BoxLayout):
    """The four tabs: Home, Training, Progress, Hero. One row when the labels fit, else a 2x2 grid, else a column."""

    selected = StringProperty(TABS[0].key)

    def __init__(self, on_select: Callable[[str], None], **kwargs):
        super().__init__(orientation="vertical", size_hint_y=None, **kwargs)
        ensure_font()
        self.init_surface(theme.SURFACE)
        self._on_select = on_select
        self.layout = ""
        self.items: dict[str, TabItem] = {}
        self._build("row")
        self.bind(width=self._relayout, selected=self._show_selected)

    def _widest_label_px(self) -> float:
        widths = []
        for tab in TABS:
            probe = CoreLabel(text=tab.label, font_name=theme.FONT_NAME, font_size=theme.font_px(theme.LABEL.size))
            probe.refresh()
            widths.append(probe.texture.width if probe.texture is not None else 0)
        return max(widths)

    def _relayout(self, *_args) -> None:
        if self.width <= 1:
            return
        layout = choose_bar_layout(self._widest_label_px(), self.width, dp(16))
        if layout != self.layout:
            self._build(layout)

    def _build(self, layout: str) -> None:
        self.layout = layout
        self.clear_widgets()
        self.add_widget(Divider())
        if layout == "row":
            holder = GridLayout(cols=4, size_hint_y=None)
        elif layout == "grid":
            holder = GridLayout(cols=2, size_hint_y=None)
        else:
            holder = GridLayout(cols=1, size_hint_y=None)
        holder.bind(minimum_height=holder.setter("height"))
        self.items = {}
        for tab in TABS:
            item = TabItem(tab.key, tab.label)
            item.bind(on_release=lambda button: self._on_select(button.tab_key))
            self.items[tab.key] = item
            holder.add_widget(item)
        if layout == "column":
            scroll = ScrollView(do_scroll_x=False, size_hint_y=None)
            scroll.add_widget(holder)
            holder.bind(height=lambda *_: setattr(scroll, "height", min(holder.height, Window.height * 0.4)))
            self.add_widget(scroll)
            content_height = lambda: scroll.height  # noqa: E731
        else:
            self.add_widget(holder)
            content_height = lambda: holder.height  # noqa: E731

        def fit(*_args) -> None:
            self.height = content_height() + dp(1)

        holder.bind(height=fit)
        fit()
        self._show_selected()

    def _show_selected(self, *_args) -> None:
        for key, item in self.items.items():
            item.selected = key == self.selected
