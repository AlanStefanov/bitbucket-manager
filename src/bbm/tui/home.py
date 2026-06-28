from __future__ import annotations

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical
from textual.events import Resize
from textual.screen import Screen
from textual.widgets import Static

from ..version import VERSION

CARDS: list[tuple[str, str, str, str]] = [
    ("📦", "Repos", "Explorar y clonar repositorios del workspace", "explorer"),
    ("🔐", "Permisos", "Gestionar accesos de usuarios por repositorio", "permissions"),
    ("✅", "PRs", "Auto-aprobar Pull Requests con reglas", "pr"),
    ("📋", "Migración", "Migrar repos entre workspaces", "migration"),
    ("🗄️", "Archive", "Archivar repos inactivos", "archive"),
    ("🔗", "Deps", "Analizar dependencias entre repos", "deps"),
]


class FeatureCard(Vertical):
    def __init__(self, icon: str, title: str, desc: str, action: str) -> None:
        super().__init__(classes="card")
        self._icon = icon
        self._title = title
        self._desc = desc
        self._action = action
        self.can_focus = True

    def compose(self) -> ComposeResult:
        yield Static(f"[bold #d4d4d4]{self._icon}[/]", classes="card-icon")
        yield Static(f"[bold]{self._title}[/]", classes="card-title")
        yield Static(f"[dim]{self._desc}[/]", classes="card-desc")

    def on_click(self) -> None:
        self._go()

    def _go(self) -> None:
        from .explorer import ExplorerScreen
        from .permissions_screen import PermissionsScreen
        from .pr_screen import PRScreen
        from .migration_screen import MigrationScreen
        from .archive_screen import ArchiveScreen
        from .deps_screen import DepsScreen

        screen_map = {
            "explorer": ExplorerScreen,
            "permissions": PermissionsScreen,
            "pr": PRScreen,
            "migration": MigrationScreen,
            "archive": ArchiveScreen,
            "deps": DepsScreen,
        }
        cls = screen_map.get(self._action)
        if cls:
            self.app.switch_screen(cls())


class HomeScreen(Screen):
    BINDINGS = [
        ("enter", "open", "Abrir"),
        ("up", "up", "Arriba"),
        ("down", "down", "Abajo"),
        ("left", "left", "Izquierda"),
        ("right", "right", "Derecha"),
        ("q", "quit_app", "Salir"),
        ("escape", "quit_app", "Salir"),
    ]

    def compose(self) -> ComposeResult:
        rows: list[Horizontal] = []
        cur: list[FeatureCard] = []

        for i, (icon, title, desc, action) in enumerate(CARDS):
            cur.append(FeatureCard(icon, title, desc, action))
            if len(cur) == 3 or i == len(CARDS) - 1:
                rows.append(Horizontal(*cur, classes="card-row"))
                cur = []

        yield Vertical(
            Static(
                "[bold #10b981]██████╗ ██████╗ ███╗   ███╗[/]"
                "\n[bold #10b981]██╔══██╗██╔══██╗████╗ ████║[/]"
                "\n[bold #10b981]██████╔╝██████╔╝██╔████╔██║[/]"
                "\n[bold #10b981]██╔══██╗██╔══██╗██║╚██╔╝██║[/]"
                "\n[bold #10b981]██████╔╝██████╔╝██║ ╚═╝ ██║[/]"
                "\n[bold #10b981]╚═════╝ ╚═════╝ ╚═╝     ╚═╝[/]",
                id="home-brand",
            ),
            Static(f"[dim]Bitbucket Repository Manager  v{VERSION}[/]", id="home-title"),
            Vertical(*rows, id="home-cards"),
            Static(
                "[dim]Seleccioná con [/dim][#10b981]↑↓←→[/]  [dim]y presioná [/dim][#10b981]Enter[/]  [dim]— [/dim][#10b981]Q[/][dim] / [/dim][#10b981]Esc[/][dim] para salir[/]",
                id="home-hints",
            ),
            id="home-root",
        )

    def on_mount(self) -> None:
        self._apply_responsive(self.size.width, self.size.height)
        self._focus_first()

    def on_screen_resume(self) -> None:
        self._focus_first()

    def on_resize(self, event: Resize) -> None:
        self._apply_responsive(event.size.width, event.size.height)

    def _apply_responsive(self, w: int, h: int) -> None:
        root = self.query_one("#home-root", Vertical)
        if w < 90 or h < 30:
            root.add_class("-compact")
        else:
            root.remove_class("-compact")
        if w < 65 or h < 24:
            root.add_class("-ultra-compact")
        else:
            root.remove_class("-ultra-compact")

    def _cards(self) -> list[FeatureCard]:
        return list(self.query(FeatureCard))

    def _focus_first(self) -> None:
        cards = self._cards()
        if cards:
            cards[0].focus()

    def _idx(self) -> int:
        f = self.focused
        c = self._cards()
        if f in c:
            return c.index(f)
        p = getattr(f, "parent", None)
        if p in c:
            return c.index(p)
        return -1

    def action_open(self) -> None:
        i = self._idx()
        c = self._cards()
        if 0 <= i < len(c):
            c[i]._go()

    def action_left(self) -> None:
        i = self._idx()
        c = self._cards()
        if i > 0:
            c[i - 1].focus()

    def action_right(self) -> None:
        i = self._idx()
        c = self._cards()
        if 0 <= i < len(c) - 1:
            c[i + 1].focus()

    def action_up(self) -> None:
        i = self._idx()
        c = self._cards()
        n = i - 3
        if n >= 0:
            c[n].focus()

    def action_down(self) -> None:
        i = self._idx()
        c = self._cards()
        n = i + 3
        if n < len(c):
            c[n].focus()

    def action_quit_app(self) -> None:
        self.app.exit()
