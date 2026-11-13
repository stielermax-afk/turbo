"""Erzeugt die App-Icons für Turbo (icon-180/192/512.png) mit Pillow."""
import math
from pathlib import Path

from PIL import Image, ImageDraw

ZIEL = Path(__file__).parent
GRUND = (10, 12, 15)
SPUR = (38, 44, 53)
ORANGE = (255, 106, 31)
GEHAEUSE = (44, 51, 61)
SCHACHT = (5, 6, 7)
SCHAUFEL = (198, 206, 216)
NABE = (236, 240, 244)


def icon(groesse: int) -> Image.Image:
    s = groesse * 4  # Supersampling für glatte Kanten
    bild = Image.new("RGB", (s, s), GRUND)
    z = ImageDraw.Draw(bild)
    m = s / 2

    def kreis(r, farbe):
        z.ellipse((m - r, m - r, m + r, m + r), fill=farbe)

    # Ladedruck-Bogen (270°, unten offen), zu zwei Dritteln gefüllt
    r = s * 0.37
    breite = round(s * 0.045)
    kasten = (m - r, m - r, m + r, m + r)
    z.arc(kasten, start=135, end=405, fill=SPUR, width=breite)
    z.arc(kasten, start=135, end=315, fill=ORANGE, width=breite)

    kreis(s * 0.285, GEHAEUSE)
    kreis(s * 0.225, SCHACHT)

    # Verdichterrad: gebogene Schaufeln als Vielecke
    for i in range(9):
        w = math.radians(i * 40)
        punkte = []
        for rr, versatz in ((0.05, -0.30), (0.13, 0.05), (0.205, 0.42), (0.205, 0.62), (0.12, 0.38), (0.05, 0.30)):
            a = w + versatz
            punkte.append((m + math.cos(a) * s * rr, m + math.sin(a) * s * rr))
        z.polygon(punkte, fill=SCHAUFEL)

    kreis(s * 0.06, NABE)
    kreis(s * 0.024, GEHAEUSE)

    return bild.resize((groesse, groesse), Image.LANCZOS)


if __name__ == "__main__":
    for g in (180, 192, 512):
        pfad = ZIEL / f"icon-{g}.png"
        icon(g).save(pfad, optimize=True)
        print("geschrieben:", pfad.name)
