import flet as ft
from flet_audio import Audio
import threading

def normalizar_tecla(k: str) -> str:
    k = (k or "").lower()
    if k == "space":
        return " "
    return k.replace(" ", "").replace("-", "")

def mostrar_nota_visual(pagina, teclado, label, nombre_nota, texto_mostrar, recursos, teclado_base):
    img_url = recursos.get(nombre_nota, {}).get("img")
    if not img_url:
        return
    teclado.src = img_url
    label.value = f"🎵 {texto_mostrar} 🎵"
    label.visible = True
    pagina.update()


    def resetear():
        teclado.src = teclado_base
        label.visible = False
        pagina.update()
    threading.Timer(0.5, resetear).start()
    
RECURSOS = {
    "Do":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Do.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Do.wav"},
    "Re":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Re.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Re.wav"},
    "Mi":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Mi.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Mi.wav"},
    "Fa":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Fa.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Fa.wav"},
    "Sol": {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Sol.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Sol.wav"},
    "La":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/La.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/La.wav"},
    "Si":  {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Si.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Si.wav"},
    "Do2": {"img": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Do2.png",
            "wav": "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Do2.wav"},
}

TECLADO_BASE = "https://raw.githubusercontent.com/Prof-Luis1986/Recursos_Teclado/main/Teclado.png"

NOTAS = [
    {"nombre": "Do",   "mostrar": "Do", "teclas": ["w"]},
    {"nombre": "Re",   "mostrar": "Re", "teclas": ["a"]},
    {"nombre": "Mi",   "mostrar": "Mi", "teclas": ["s"]},
    {"nombre": "Fa",   "mostrar": "Fa", "teclas": ["d"]},
    {"nombre": "Sol",  "mostrar": "Sol","teclas": ["f"]},
    {"nombre": "La",   "mostrar": "La", "teclas": ["g"]},
    {"nombre": "Si",   "mostrar": "Si", "teclas": [" ", "space"]},
    {"nombre": "Do2",  "mostrar": "Do", "teclas": ["arrowright", "arrow right", "arrow-right"]},
]


def main(pagina: ft.Page):
    pagina.title = "Piano Makey Makey"
    pagina.bgcolor = "blue"
    pagina.window_width = 800
    pagina.window_height = 450
    pagina.window_resizable = False
    pagina.padding = 0
    pagina.spacing = 0

    teclado = ft.Image(src=TECLADO_BASE, width=800, height=300)
    nota_label = ft.Text(
        value="",
        size=40,
        color="red",
        weight="bold",
        text_align="center",
        visible=False,
    )

    # Layout: label arriba, teclado abajo
    pagina.add(
        ft.Column(
            [
                ft.Container(content=nota_label, alignment=ft.alignment.center, height=100),
                teclado,
            ],
            alignment="center",
            horizontal_alignment="center",
            spacing=10,
        )
    )
    
    
    tecla_a_nota = {}
    for n in NOTAS:
        for t in n["teclas"]:
            tecla_a_nota[normalizar_tecla(t)] = {"nombre": n["nombre"], "mostrar": n["mostrar"]}

    nombre_a_audio = {}
    for nombre, urls in RECURSOS.items():
        reproductor = Audio(src=urls["wav"])
        nombre_a_audio[nombre] = reproductor
        pagina.overlay.append(reproductor)
        
    def al_presionar_tecla(evento: ft.KeyboardEvent):
        tecla_norm = normalizar_tecla(evento.key)
        nota_info = tecla_a_nota.get(tecla_norm)
        if not nota_info:
            return  # tecla no mapeada
        nombre_nota = nota_info["nombre"]
        texto_mostrar = nota_info["mostrar"]

        reproductor = nombre_a_audio.get(nombre_nota)
        if reproductor:
            reproductor.play()
            mostrar_nota_visual(
                pagina, teclado, nota_label,
                nombre_nota, texto_mostrar,
                RECURSOS , TECLADO_BASE
            )
    pagina.on_keyboard_event = al_presionar_tecla
    pagina.update()
    
ft.app(target=main)