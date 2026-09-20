import os
import threading
from urllib.parse import urlparse

from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import platform

KV = """
#:import dp kivy.metrics.dp

<NeonButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0.92, 0.04, 0.20, 1
    color: 1, 1, 1, 1
    bold: True

<DarkButton@Button>:
    background_normal: ""
    background_down: ""
    background_color: 0.12, 0.12, 0.16, 1
    color: 0.9, 0.9, 0.94, 1

BoxLayout:
    orientation: "vertical"
    padding: dp(16)
    spacing: dp(12)

    canvas.before:
        Color:
            rgba: 0.035, 0.035, 0.05, 1
        Rectangle:
            pos: self.pos
            size: self.size

    BoxLayout:
        size_hint_y: None
        height: dp(55)

        Label:
            text: "[b]⚡ NIGHT[/b][color=ff1744]LOAD[/color]"
            markup: True
            font_size: "25sp"
            halign: "left"
            text_size: self.size

        DarkButton:
            text: "⚙"
            size_hint_x: None
            width: dp(48)
            on_release: app.show_page("Configurações")

    BoxLayout:
        id: page_area
        orientation: "vertical"
        spacing: dp(12)

    BoxLayout:
        size_hint_y: None
        height: dp(62)
        spacing: dp(4)

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

HOME = """
BoxLayout:
    orientation: "vertical"
    spacing: dp(13)

    Label:
        text: "[b]Tudo o que você ama,[/b]\\n[color=ff1744]em um só lugar.[/color]"
        markup: True
        font_size: "25sp"
        halign: "left"
        valign: "middle"
        text_size: self.size
        size_hint_y: None
        height: dp(95)

    Label:
        text: "Baixe e organize suas mídias"
        color: 0.58, 0.58, 0.65, 1
        halign: "left"
        size_hint_y: None
        height: dp(24)

    BoxLayout:
        size_hint_y: None
        height: dp(54)
        spacing: dp(6)

        TextInput:
            id: url_input
            hint_text: "Cole o link da mídia..."
            multiline: False
            background_normal: ""
            background_active: ""
            background_color: 0.12, 0.12, 0.16, 1
            foreground_color: 1, 1, 1, 1
            hint_text_color: 0.55, 0.55, 0.62, 1
            cursor_color: 1, 0.08, 0.25, 1
            padding: dp(12)
            on_text_validate: app.start_download("video")

        NeonButton:
            text: "COLAR"
            size_hint_x: None
            width: dp(72)
            on_release: app.paste_link()

    Label:
        text: "[b]DOWNLOAD RÁPIDO[/b]"
        markup: True
        color: 0.85, 0.85, 0.9, 1
        halign: "left"
        size_hint_y: None
        height: dp(28)

    GridLayout:
        cols: 2
        spacing: dp(10)
        size_hint_y: None
        height: dp(125)

        DarkButton:
            text: "♫\\n[color=ff3156][b]MÚSICA MP3[/b][/color]\\nÁudio"
            markup: True
            on_release: app.start_download("audio")

        DarkButton:
            text: "▶\\n[color=ff3156][b]VÍDEO HD[/b][/color]\\nVídeo"
            markup: True
            on_release: app.start_download("video")

    Label:
        text: "[b]ATIVIDADE[/b]"
        markup: True
        color: 0.85, 0.85, 0.9, 1
        halign: "left"
        size_hint_y: None
        height: dp(28)

    BoxLayout:
        orientation: "vertical"
        padding: dp(14)
        spacing: dp(8)
        canvas.before:
            Color:
                rgba: 0.10, 0.10, 0.14, 1
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(16)]

        Label:
            id: status
            text: "⚡ Pronto para começar"
            color: 0.85, 0.85, 0.90, 1
            halign: "left"
            valign: "middle"
            text_size: self.size

        Label:
            text: "Seus arquivos em um só lugar"
            color: 0.52, 0.52, 0.60, 1
            font_size: "12sp"
            halign: "left"

    Widget:
"""

class NightLoadApp(App):
    busy = False

    def build(self):
        self.title = "NightLoad"
        self.root = Builder.load_string(KV)
        self.show_page("Início")
        return self.root

    def show_page(self, page):
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label

        area = self.root.ids.page_area
        area.clear_widgets()

        if page == "Início":
            self.home = Builder.load_string(HOME)
            area.add_widget(self.home)
            return

        view = BoxLayout(
            orientation="vertical",
            spacing=dp(12)
        )

        view.add_widget(Label(
            text=f"[b]{page}[/b]",
            markup=True,
            font_size="25sp",
            size_hint_y=None,
            height=dp(70)
        ))

        descriptions = {
            "Música": "Sua coleção de músicas aparecerá aqui.",
            "Downloads": "Seus downloads aparecerão aqui.",
            "Biblioteca": "Seus arquivos salvos aparecerão aqui.",
            "Configurações": "Configurações do aplicativo."
        }

        view.add_widget(Label(
            text=descriptions.get(page, ""),
            color=(0.7, 0.7, 0.76, 1)
        ))

        area.add_widget(view)

    def set_status(self, message):
        def update(dt):
            if hasattr(self, "home"):
                self.home.ids.status.text = message
        Clock.schedule_once(update)

    def paste_link(self):
        from kivy.core.clipboard import Clipboard
        text = Clipboard.paste()

        if text:
            self.home.ids.url_input.text = text.strip()
            self.set_status("Link inserido. Escolha o formato.")

    def start_download(self, mode):
        self.set_status(
            "Downloader será conectado após configurar "
            "as dependências Android."
        )

if __name__ == "__main__":
    NightLoadApp().run()
