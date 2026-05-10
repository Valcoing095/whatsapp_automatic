"""
Envío masivo con pywhatkit (abre WhatsApp Web en el navegador por defecto) + pyautogui
para clic en el botón enviar usando una captura send_btn.png (misma idea que tu script).

Instalación:
  pip install -r requirements-pywhatkit.txt

Uso:
  python enviar_masivo_pywhatkit.py
  python enviar_masivo_pywhatkit.py --excel clientes.xlsx

El Excel puede usar columnas: Nombre/nombre, Telefono/Celular/celular, Placa/placa.
Deja send_btn.png en esta carpeta (recorte solo el icono enviar de WhatsApp Web).
"""

from __future__ import annotations

import argparse
import os
import time

import pandas as pd

try:
    import pywhatkit as kit
except ImportError as e:
    raise SystemExit("Instala dependencias: pip install -r requirements-pywhatkit.txt") from e

try:
    import pyautogui as pg
except ImportError as e:
    raise SystemExit("Falta pyautogui: pip install -r requirements-pywhatkit.txt") from e

MENSAJE = (
    """Hola {nombre}, soy Carolina Arboleda de la agencia Sano y Salvo – Chevrolet Caminos. 🚗
Estoy ayudando a varios clientes a pasar su póliza del banco 🏛️ a modalidad individual para que tengan mejor respaldo en caso de siniestro .
¿Te preparo la cotización de tu {placa}? ✨"""
)


def _norm_cols(df: pd.DataFrame) -> dict[str, str]:
    mapping: dict[str, str] = {}
    lower = {str(c).strip().lower(): c for c in df.columns}

    def pick(*names: str) -> str | None:
        for n in names:
            if n.lower() in lower:
                return str(lower[n.lower()])
        return None

    nombre_c = pick("nombre")
    tel_c = pick("telefono", "celular", "teléfono")
    placa_c = pick("placa")
    if not nombre_c or not tel_c or not placa_c:
        raise ValueError(
            "El Excel debe incluir columnas para nombre, teléfono/celular y placa "
            f"(columnas actuales: {list(df.columns)})"
        )
    mapping["nombre"] = nombre_c
    mapping["telefono"] = tel_c
    mapping["placa"] = placa_c
    return mapping


def _numero_pywhatkit(telefono: str) -> str:
    d = "".join(c for c in str(telefono) if c.isdigit())
    if not d:
        return ""
    if d.startswith("57"):
        return f"+{d}"
    if len(d) == 10:
        return f"+57{d}"
    if len(d) == 9:
        return f"+57{d}"
    return f"+{d}"


def _buscar_y_clic_send(send_image: str, intentos: int = 10) -> bool:
    if not os.path.isfile(send_image):
        print(f"Aviso: no existe {send_image} — coloca ahí la captura del botón enviar.")
        return False
    boton = None
    for _ in range(intentos):
        try:
            boton = pg.locateCenterOnScreen(send_image, confidence=0.8)
        except Exception:
            boton = None
        if boton:
            break
        time.sleep(0.5)
    if boton:
        pg.click(boton)
        return True
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--excel",
        default="clientes.xlsx",
        help="Ruta al .xlsx (por defecto clientes.xlsx en el directorio actual)",
    )
    parser.add_argument(
        "--send-image",
        default="send_btn.png",
        help="Imagen del botón enviar para pyautogui",
    )
    parser.add_argument("--wait-kit", type=int, default=12, help="wait_time de pywhatkit")
    parser.add_argument(
        "--tab-close",
        action="store_true",
        help="Pasar tab_close=True a pywhatkit (por defecto False, como tu script)",
    )
    args = parser.parse_args()

    if not os.path.isfile(args.excel):
        raise SystemExit(f"No se encontró el archivo: {args.excel}")

    df = pd.read_excel(args.excel)
    cols = _norm_cols(df)

    for _, row in df.iterrows():
        nombre = str(row[cols["nombre"]]).strip()
        if not nombre or str(nombre).lower() == "nan":
            continue
        telefono = str(row[cols["telefono"]]).replace(" ", "").replace("-", "")
        placa = str(row[cols["placa"]]).strip()
        numero_final = _numero_pywhatkit(telefono)
        if not numero_final or len(numero_final) < 4:
            print(f"Omitido (teléfono vacío o inválido): {nombre}")
            continue

        mensaje_final = MENSAJE.format(nombre=nombre, placa=placa)
        print(f"Enviando mensaje a {nombre} ({numero_final})...")

        try:
            kit.sendwhatmsg_instantly(
                phone_no=numero_final,
                message=mensaje_final,
                wait_time=args.wait_kit,
                tab_close=args.tab_close,
            )
            time.sleep(5)
            if _buscar_y_clic_send(args.send_image):
                print("Mensaje enviado (clic por imagen).")
            else:
                print("No se pudo hacer clic en enviar (revisa send_btn.png y que el chat esté visible).")
            time.sleep(2)
            pg.hotkey("ctrl", "w")
            time.sleep(1)
        except Exception as e:
            print("Error:", e)
            time.sleep(1)

    print("Proceso completado.")


if __name__ == "__main__":
    main()
