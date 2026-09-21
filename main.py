import threading
from urllib.parse import urlparse

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.core.clipboard import Clipboard
from kivy.utils import platform

KV = r"""
#:import dp kivy.metrics.dp

<NeonButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: (0.95, 0.02, 0.20, 1) if self.state == "normal" else (0.65, 0.01, 0.12, 1)
    color: 1, 1, 1, 1
    bold: True
    font_size: "14sp"

<DarkButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: (0.075, 0.08, 0.12, 1) if self.state == "normal" else (0.15, 0.08, 0.12, 1)
    color: 0.88, 0.90, 0.96, 1
    font_size: "13sp"

<Panel@BoxLayout>:
    orientation: "vertical"
    padding: dp(14)
    spacing: dp(8)
    size_hint_y: None
    height: self.minimum_height
    canvas.before:
        Color:
            rgba: 0.065, 0.07, 0.105, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(16)]

BoxLayout:
    orientation: "vertical"
    padding: dp(14)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: 0.018, 0.022, 0.038, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(48)
        Label:
            text: "[b]NIGHT[/b][color=ff1744]LOAD[/color]"
            markup: True
            font_size: "25sp"
            halign: "left"
            text_size: self.size
        NeonButton:
            text: "⚙"
            size_hint_x: None
            width: dp(48)
            on_release: app.show_page("Configurações")

    BoxLayout:
        id: page_area
        orientation: "vertical"
        spacing: dp(10)

    BoxLayout:
        size_hint_y: None
        height: dp(58)
        spacing: dp(5)
        DarkButton:
            text: "⌂\\nInício"
            on_release: app.show_page("Início")
        DarkButton:
            text: "♫\\nMúsica"
            on_release: app.show_page("Música")
        DarkButton:
            text: "⇩\\nDownloads"
            on_release: app.show_page("Downloads")
        DarkButton:
            text: "▣\\nBiblioteca"
            on_release: app.show_page("Biblioteca")
"""

HOME = r"""
BoxLayout:
    orientation: "vertical"
    spacing: dp(10)

    Label:
        text: "[b]Mais que um downloader.[/b]\\n[color=ff1744]Sua mídia, do seu jeito.[/color]"
        markup: True
        font_size: "24sp"
        halign: "left"
        valign: "middle"
        text_size: self.size
        size_hint_y: None
        height: dp(82)

    Label:
        text: "Cole um link de mídia que você tem autorização para baixar."
        color: 0.57, 0.60, 0.68, 1
        font_size: "12sp"
        halign: "left"
        text_size: self.size
        size_hint_y: None
        height: dp(34)

    BoxLayout:
        size_hint_y: None
        height: dp(52)
        spacing: dp(6)
        TextInput:
            id: url_input
            hint_text: "Cole a URL aqui..."
            multiline: False
            background_normal: ""
            background_active: ""
            background_color: 0.075, 0.08, 0.12, 1
            foreground_color: 1, 1, 1, 1
            hint_text_color: 0.48, 0.52, 0.60, 1
            cursor_color: 1, 0.08, 0.25, 1
            padding: dp(12), dp(15)
            on_text_validate: app.start_download("video")
        NeonButton:
            text: "COLAR"
            size_hint_x: None
            width: dp(76)
            on_release: app.paste_link()

    Label:
        text: "[b]ESCOLHA O QUE BAIXAR[/b]"
        markup: True
        color: 0.82, 0.84, 0.90, 1
        halign: "left"
        size_hint_y: None
        height: dp(28)

    GridLayout:
        cols: 2
        spacing: dp(10)
        size_hint_y: None
        height: dp(132)

        DarkButton:
            text: "♫\\n[color=ff3156][b]MÚSICA MP3[/b][/color]\\nÁudio"
            markup: True
            on_release: app.start_download("audio")

        DarkButton:
            text: "▶\\n[color=ff3156][b]VÍDEO HD[/b][/color]\\nVídeo"
            markup: True
            on_release: app.start_download("video")

    Label:
        text: "[b]ATALHOS[/b]"
        markup: True
        color: 0.82, 0.84, 0.90, 1
        halign: "left"
        size_hint_y: None
        height: dp(26)

    GridLayout:
        cols: 3
        spacing: dp(7)
        size_hint_y: None
        height: dp(66)
        DarkButton:
            text: "▣\\nBiblioteca"
            on_release: app.show_page("Biblioteca")
        DarkButton:
            text: "⇩\\nDownloads"
            on_release: app.show_page("Downloads")
        DarkButton:
            text: "⚙\\nConfig."
            on_release: app.show_page("Configurações")

    BoxLayout:
        orientation: "vertical"
        padding: dp(13)
        spacing: dp(5)
        canvas.before:
            Color:
                rgba: 0.07, 0.075, 0.11, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(15)]

        Label:
            text: "[b]STATUS[/b]"
            markup: True
            color: 1, 0.18, 0.34, 1
            halign: "left"
            size_hint_y: None
            height: dp(24)

        Label:
            id: status
            text: "⚡ NightLoad pronto"
            color: 0.88, 0.90, 0.95, 1
            halign: "left"
            valign: "middle"
            text_size: self.size

        Label:
            text: "Interface em desenvolvimento"
            color: 0.48, 0.52, 0.60, 1
            font_size: "11sp"
            halign: "left"
            size_hint_y: None
            height: dp(18)

    Widget:
"""

class NightLoadApp(App):
    def build(self):
        self.title = "NightLoad"
        self.root = Builder.load_string(KV)
        self.show_page("Início")
        return self.root

    def show_page(self, page):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button

        area = self.root.ids.page_area
        area.clear_widgets()

        if page == "Início":
            self.home = Builder.load_string(HOME)
            area.add_widget(self.home)
            return

        view = BoxLayout(orientation="vertical", spacing=dp(12))
        title = Label(
            text=f"[b]{page}[/b]",
            markup=True,
            font_size="24sp",
            size_hint_y=None,
            height=dp(48),
            halign="left",
            text_size=(dp(300), None),
        )
        view.add_widget(title)

        descriptions = {
            "Música": "Sua área de música ficará aqui.",
            "Downloads": "Seus downloads aparecerão aqui.",
            "Biblioteca": "Sua biblioteca de arquivos ficará aqui.",
            "Configurações": "Personalize sua experiência.",
        }

        info = Label(
            text=descriptions.get(page, ""),
            color=(0.72, 0.75, 0.82, 1),
            halign="left",
            valign="top",
            text_size=(dp(300), None),
        )
        view.add_widget(info)

        if page == "Configurações":
            for option in [
                "Tema: Preto + vermelho neon",
                "Idioma: Português (Brasil)",
                "Pasta de arquivos: será configurada",
                "Qualidade: opção futura",
            ]:
                item = Button(
                    text=option,
                    size_hint_y=None,
                    height=dp(48),
                    background_normal="",
                    background_color=(0.075, 0.08, 0.12, 1),
                    color=(0.9, 0.92, 0.96, 1),
                )
                view.add_widget(item)

        back = Button(
            text="VOLTAR AO INÍCIO",
            size_hint_y=None,
            height=dp(48),
            background_normal="",
            background_color=(0.95, 0.02, 0.20, 1),
            color=(1, 1, 1, 1),
            bold=True,
        )
        back.bind(on_release=lambda *_: self.show_page("Início"))
        view.add_widget(back)
        area.add_widget(view)

    def paste_link(self):
        try:
            text = Clipboard.paste()
            if hasattr(self, "home") and text:
                self.home.ids.url_input.text = text.strip()
                self.set_status("Link colado. Confira antes de continuar.")
        except Exception:
            self.set_status("Não foi possível acessar a área de transferência.")

    def set_status(self, message):
        if hasattr(self, "home") and "status" in self.home.ids:
            self.home.ids.status.text = message

    def start_download(self, kind):
        if not hasattr(self, "home"):
            return

        url = self.home.ids.url_input.text.strip()
        parsed = urlparse(url)

        if parsed.scheme not in ("http", "https") or not parsed.netloc:
            self.set_status("Cole uma URL válida começando com https://")
            return

        self.set_status(
            "A interface está pronta; o mecanismo de download ainda será conectado. "
            "Use apenas mídias suas ou autorizadas."
        )

if __name__ == "__main__":
    NightLoadApp().run()
