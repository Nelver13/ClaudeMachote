#!/usr/bin/env python3
"""
app/main.py — Panel de control multi-proyecto del Sistema IA.

Accesible desde:
  - PC local: http://localhost:8550
  - Red local: http://<ip>:8550
  - Internet: activar tunnel con --tunnel

Uso:
  python sistema-ia/app/main.py
  python sistema-ia/app/main.py --tunnel   (expone via ngrok)
"""
import argparse
import json
import re
import sys
import socket
import subprocess
from pathlib import Path
from datetime import datetime

TUNNEL_URL: str | None = None
APP_PORT: int = 8550


def _ip_local() -> str:
    """Obtiene la IP local de la interfaz de red activa."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def _qr_url(data: str) -> str:
    """URL de imagen QR via servicio externo (sin dependencias)."""
    return f"https://api.qrserver.com/v1/create-qr-code/?size=250x250&data={data}"

try:
    import flet as ft
except ImportError:
    print("ERROR: flet no instalado.")
    print("  pip install flet pyngrok")
    sys.exit(1)

# ── CONFIGURACIÓN ────────────────────────────────────────────────────────────

APP_DIR = Path(__file__).parent.resolve()
SIA_DIR = APP_DIR.parent
PROYECTOS_FILE = APP_DIR / "proyectos.json"

# ── MODELO ───────────────────────────────────────────────────────────────────

class Proyecto:
    def __init__(self, ruta: Path):
        self.ruta = Path(ruta).resolve()
        self.estado = self._leer_estado()

    def _leer_estado(self) -> dict:
        p = self.ruta / "ESTADO.md"
        if not p.exists():
            return {}
        data = {}
        for linea in p.read_text(encoding="utf-8").splitlines():
            linea = linea.strip()
            if linea.startswith("[") and ":" in linea:
                clave = linea[1:linea.index(":")]
                valor = linea[linea.index(":")+1:].rstrip("]").strip()
                data[clave] = valor
        return data

    @property
    def nombre(self) -> str:
        return self.estado.get("PROJ", self.ruta.name)

    @property
    def modulo(self) -> str:
        return self.estado.get("MODULO", "—")

    @property
    def plan(self) -> str:
        return self.estado.get("PLAN", "—")

    @property
    def progreso(self) -> str:
        return self.estado.get("PROGRESO", "0%")

    @property
    def estado_plan(self) -> str:
        return self.estado.get("ESTADO_PLAN", "—")

    @property
    def next_task(self) -> str:
        return self.estado.get("NEXT_TASK", "—")

    @property
    def ia_activa(self) -> str:
        """Devuelve qué IA debe continuar según roles + estado."""
        ep = self.estado_plan.lower()
        roles = {
            "CLAUDE": self.estado.get("ROL_CLAUDE", ""),
            "KIMI": self.estado.get("ROL_KIMI", ""),
            "CODEX": self.estado.get("ROL_CODEX", ""),
            "GEMINI": self.estado.get("ROL_GEMINI", ""),
        }

        if "discusion" in ep:
            buscar = "ARQUITECTO"
        elif "ejecucion" in ep or "revision" in ep:
            buscar = "DESARROLLADOR"
        else:
            return "Nadie (sin plan activo)"

        for ia, rol in roles.items():
            if buscar.upper() in rol.upper():
                return ia
        return "Nadie (rol no asignado)"

    def leer_discusiones(self) -> list[dict]:
        dir_disc = self.ruta / "sistema-ia" / "discusiones"
        if not dir_disc.exists():
            return []
        items = []
        for mod_dir in sorted(dir_disc.iterdir()):
            if not mod_dir.is_dir() or mod_dir.name == "bugs":
                continue
            for vfile in sorted(mod_dir.glob("*.md")):
                items.append({
                    "modulo": mod_dir.name,
                    "archivo": vfile.name,
                    "nombre": vfile.stem,
                })
        return items

    def leer_planes(self) -> list[dict]:
        dir_planes = self.ruta / "sistema-ia" / "planes"
        if not dir_planes.exists():
            return []
        items = []
        for mod_dir in sorted(dir_planes.iterdir()):
            if not mod_dir.is_dir():
                continue
            for vfile in sorted(mod_dir.glob("*.md")):
                items.append({
                    "modulo": mod_dir.name,
                    "archivo": vfile.name,
                    "nombre": vfile.stem,
                })
        return items

    def leer_bugs(self) -> str:
        p = self.ruta / "sistema-ia" / "discusiones" / "bugs" / "backlog.md"
        if p.exists():
            return p.read_text(encoding="utf-8")
        return "Sin bugs reportados."

    def enviar_comando(self, texto: str):
        handoff = self.ruta / "sistema-ia" / "handoff"
        handoff.mkdir(parents=True, exist_ok=True)
        f = handoff / f"comando_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        f.write_text(f"# Comando desde app\n**Fecha:** {datetime.now().isoformat()}\n\n{texto}\n", encoding="utf-8")
        return f.name


# ── PROYECTOS REGISTRADOS ────────────────────────────────────────────────────

def cargar_proyectos() -> list[Proyecto]:
    if not PROYECTOS_FILE.exists():
        auto = SIA_DIR.parent
        if (auto / "ESTADO.md").exists():
            return [Proyecto(auto)]
        return []
    data = json.loads(PROYECTOS_FILE.read_text(encoding="utf-8"))
    return [Proyecto(p["ruta"]) for p in data]


def guardar_proyectos(proyectos: list[Proyecto]):
    data = [{"nombre": p.nombre, "ruta": str(p.ruta)} for p in proyectos]
    PROYECTOS_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


# ── UI MÓVIL ─────────────────────────────────────────────────────────────────

def main(page: ft.Page):
    page.title = "Sistema IA"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 15
    page.scroll = ft.ScrollMode.AUTO

    proyectos = cargar_proyectos()
    proyecto_actual = proyectos[0] if proyectos else None
    tab_actual = "Estado"

    # ── QR ───────────────────────────────────────────────────────────────────
    ip = _ip_local()
    url_local = f"http://{ip}:{APP_PORT}"
    url_tun = TUNNEL_URL or ""

    qr_local = ft.Image(src=_qr_url(url_local), width=220, height=220)
    qr_tun = ft.Image(src=_qr_url(url_tun), width=220, height=220) if url_tun else None

    # ── Controles principales ────────────────────────────────────────────────
    dropdown_proyectos = ft.Dropdown(
        label="Proyecto",
        expand=True,
        options=[ft.dropdown.Option(str(p.ruta), p.nombre) for p in proyectos],
        value=str(proyecto_actual.ruta) if proyecto_actual else None,
    )

    txt_nuevo_proyecto = ft.TextField(label="Agregar ruta", expand=True, height=50)
    lbl_status = ft.Text(size=16, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)

    lbl_estado = ft.Text(size=18, weight=ft.FontWeight.BOLD)
    lbl_ia = ft.Text(size=22, color=ft.Colors.GREEN_400, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER)
    lbl_progreso = ft.Text(size=16)
    lbl_modulo = ft.Text(size=16)
    lbl_plan = ft.Text(size=16)
    lbl_next = ft.Text(size=16)

    txt_comando = ft.TextField(label="Comando", hint_text="sigue / plan / ok", expand=True, height=50)
    lbl_resultado = ft.Text(size=14, color=ft.Colors.GREY_400, text_align=ft.TextAlign.CENTER)

    content_area = ft.Column(expand=True, spacing=10)

    def refrescar_dropdown():
        dropdown_proyectos.options = [ft.dropdown.Option(str(p.ruta), p.nombre) for p in proyectos]
        if proyecto_actual:
            dropdown_proyectos.value = str(proyecto_actual.ruta)
        page.update()

    def on_change_proyecto(e):
        nonlocal proyecto_actual
        for p in proyectos:
            if str(p.ruta) == e.control.value:
                proyecto_actual = p
                mostrar_tab(tab_actual)
                break

    dropdown_proyectos.on_change = on_change_proyecto

    def mostrar_tab(tab: str):
        nonlocal tab_actual
        tab_actual = tab
        content_area.controls.clear()
        if not proyecto_actual:
            content_area.controls.append(ft.Text("Agregá un proyecto primero.", size=18, text_align=ft.TextAlign.CENTER))
            page.update()
            return

        ep = proyecto_actual.estado_plan
        ia = proyecto_actual.ia_activa

        lbl_estado.value = f"Estado: {ep}"
        lbl_ia.value = f"→ {ia} debe continuar"
        lbl_progreso.value = f"Progreso: {proyecto_actual.progreso}"
        lbl_modulo.value = f"Módulo: {proyecto_actual.modulo}"
        lbl_plan.value = f"Plan: {proyecto_actual.plan}"
        lbl_next.value = f"Próxima tarea: {proyecto_actual.next_task}"

        if tab == "Estado":
            content_area.controls.extend([
                lbl_ia,
                ft.Divider(),
                lbl_estado,
                lbl_progreso,
                lbl_modulo,
                lbl_plan,
                lbl_next,
                ft.Divider(),
                ft.Row([txt_comando, ft.Button("Enviar", height=50, on_click=enviar_comando_click)]),
                lbl_resultado,
            ])
        elif tab == "Discusiones":
            disc = proyecto_actual.leer_discusiones()
            if disc:
                for d in disc:
                    content_area.controls.append(
                        ft.Button(f"{d['modulo']}/{d['archivo']}", height=45, expand=True)
                    )
            else:
                content_area.controls.append(ft.Text("Sin discusiones.", size=18))
        elif tab == "Planes":
            planes = proyecto_actual.leer_planes()
            if planes:
                for p in planes:
                    content_area.controls.append(
                        ft.Button(f"{p['modulo']}/{p['archivo']}", height=45, expand=True)
                    )
            else:
                content_area.controls.append(ft.Text("Sin planes.", size=18))
        elif tab == "Bugs":
            content_area.controls.append(
                ft.Text(proyecto_actual.leer_bugs(), selectable=True, size=16)
            )
        page.update()

    def agregar_proyecto_click(e):
        ruta = Path(txt_nuevo_proyecto.value.strip())
        if not ruta.exists() or not (ruta / "ESTADO.md").exists():
            lbl_status.value = "Ruta inválida"
            lbl_status.color = ft.Colors.RED_400
            page.update()
            return
        nuevo = Proyecto(ruta)
        if any(p.ruta == nuevo.ruta for p in proyectos):
            lbl_status.value = "Ya está agregado"
            lbl_status.color = ft.Colors.ORANGE_400
            page.update()
            return
        proyectos.append(nuevo)
        guardar_proyectos(proyectos)
        refrescar_dropdown()
        proyecto_actual = nuevo
        mostrar_tab("Estado")
        txt_nuevo_proyecto.value = ""
        lbl_status.value = f"{nuevo.nombre} agregado"
        lbl_status.color = ft.Colors.GREEN_400
        page.update()

    def enviar_comando_click(e):
        if not proyecto_actual:
            return
        texto = txt_comando.value.strip()
        if not texto:
            return
        nombre = proyecto_actual.enviar_comando(texto)
        lbl_resultado.value = f"Guardado en handoff/{nombre}"
        txt_comando.value = ""
        lbl_status.value = "Comando enviado"
        lbl_status.color = ft.Colors.GREEN_400
        page.update()

    # ── Layout vertical (amigable para móvil) ────────────────────────────────

    tab_buttons = ft.Row([
        ft.Button("Estado", height=50, expand=True, on_click=lambda e: mostrar_tab("Estado")),
        ft.Button("Discusiones", height=50, expand=True, on_click=lambda e: mostrar_tab("Discusiones")),
        ft.Button("Planes", height=50, expand=True, on_click=lambda e: mostrar_tab("Planes")),
        ft.Button("Bugs", height=50, expand=True, on_click=lambda e: mostrar_tab("Bugs")),
    ], scroll=ft.ScrollMode.AUTO)

    qr_section = ft.Column([
        ft.Text("Escaneá para abrir en el celular", size=18, weight=ft.FontWeight.BOLD, text_align=ft.TextAlign.CENTER),
        qr_local,
        ft.Text(url_local, size=14, text_align=ft.TextAlign.CENTER, selectable=True),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    if qr_tun:
        qr_section.controls.extend([
            ft.Divider(),
            ft.Text("Internet", size=16, weight=ft.FontWeight.BOLD),
            qr_tun,
            ft.Text(url_tun, size=14, text_align=ft.TextAlign.CENTER, selectable=True),
        ])

    page.add(ft.Column([
        qr_section,
        ft.Divider(),
        ft.Text("Proyecto activo", size=18, weight=ft.FontWeight.BOLD),
        ft.Row([dropdown_proyectos], height=50),
        ft.Row([txt_nuevo_proyecto, ft.IconButton(icon=ft.Icons.ADD, on_click=agregar_proyecto_click)], height=50),
        lbl_status,
        ft.Divider(),
        tab_buttons,
        content_area,
    ], spacing=10, expand=True, horizontal_alignment=ft.CrossAxisAlignment.STRETCH))

    if proyecto_actual:
        mostrar_tab("Estado")


# ── TUNNEL / SERVIDOR ────────────────────────────────────────────────────────

def iniciar_tunnel(puerto: int) -> str | None:
    global TUNNEL_URL
    try:
        from pyngrok import ngrok
        tun = ngrok.connect(puerto, "http")
        TUNNEL_URL = tun.public_url
        print(f"[app] Tunnel público: {TUNNEL_URL}")
        print(f"[app] QR público: {_qr_url(TUNNEL_URL)}")
        return TUNNEL_URL
    except ImportError:
        print("[app] pyngrok no instalado. Sin tunnel.")
        print("  pip install pyngrok")
    except Exception as e:
        print(f"[app] Error tunnel: {e}")
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tunnel", action="store_true", help="Exponer via ngrok")
    parser.add_argument("--port", type=int, default=8550, help="Puerto local")
    parser.add_argument("--headless", action="store_true", help="Solo servidor, no abrir navegador")
    args = parser.parse_args()

    APP_PORT = args.port

    if args.tunnel:
        iniciar_tunnel(args.port)

    view = ft.AppView.WEB_BROWSER if not args.headless else ft.AppView.WEB_BROWSER
    if args.headless:
        print(f"[app] Servidor en http://localhost:{args.port}")
        print(f"[app] Modo headless — abrí manualmente el navegador.")

    ft.run(main, view=view, port=args.port)
