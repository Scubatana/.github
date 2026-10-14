# -*- coding: utf-8 -*-
"""Genere les SVG animes du profil de l'organisation Scubatana.

Tout est dessine ici, a la main : la mascotte est un vectoriel parametrable,
les animations sont en SMIL (c'est ce que GitHub sait jouer dans un README).
Aucune dependance : bibliotheque standard uniquement.

Usage : python scripts/gen_assets.py [dossier_de_sortie]
"""
import base64
import math
import sys
from pathlib import Path

SORTIE = Path(sys.argv[1] if len(sys.argv) > 1 else "profile/assets")
AVATARS = Path(sys.argv[2]) if len(sys.argv) > 2 else SORTIE / "avatars"
SORTIE.mkdir(parents=True, exist_ok=True)

POLICE = "ui-sans-serif, -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'Cascadia Code', Consolas, Menlo, monospace"

# Palette du projet : maquettes, application et films de borne
INK = "#1E3A42"
INK_SOFT = "#4C6B73"
OCEAN = "#2F6B7A"
OCEAN_DARK = "#204E5A"
OCEAN_LIGHT = "#8FB9C2"
MIST = "#DCEBEE"
PAPER = "#F5FAFB"
CORAL = "#F0855A"
CORAL_DARK = "#D96A41"
VERT = "#34C77B"
NUIT = "#16282E"


def f(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


# ==========================================================================
# La mascotte : une baleine a masque de plongee, dessinee en vectoriel
# ==========================================================================

def mascotte(x=0, y=0, taille=1.0, ident="m", ondes=True, flotte=True,
             chapeau=False, yeux="ouverts"):
    """Rend la mascotte. L'origine est son centre ; elle tient dans 150 x 130."""
    s = []
    g = ['<g transform="translate(%s %s) scale(%s)">' % (f(x), f(y), f(taille))]

    if flotte:
        g = ['<g transform="translate(%s %s)">' % (f(x), f(y)),
             '<g transform="scale(%s)">' % f(taille),
             '<g>',
             '<animateTransform attributeName="transform" type="translate" '
             'values="0 0; 0 -5; 0 0; 0 4; 0 0" dur="4.4s" repeatCount="indefinite" '
             'calcMode="spline" keyTimes="0;.25;.5;.75;1" '
             'keySplines=".4 0 .6 1;.4 0 .6 1;.4 0 .6 1;.4 0 .6 1"/>']

    s.append("".join(g))

    # --- nageoire caudale, derriere le corps ---
    s.append(
        '<g transform="translate(-72 6)">'
        '<animateTransform attributeName="transform" type="rotate" '
        'values="-8 10 0; 10 10 0; -8 10 0" dur="2.6s" repeatCount="indefinite" '
        'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
        '<path d="M20 0 C 6 -28 -18 -34 -26 -24 C -16 -12 -14 -3 -16 2 '
        'C -14 8 -16 16 -26 28 C -18 38 6 28 20 5 Z" '
        'fill="url(#%s-corps)" stroke="%s" stroke-width="3.2" stroke-linejoin="round"/>'
        '</g>' % (ident, INK)
    )

    # --- aileron dorsal ---
    s.append(
        '<path d="M-10 -40 C -4 -74 14 -88 30 -84 C 22 -70 16 -56 14 -38 Z" '
        'fill="url(#%s-corps)" stroke="%s" stroke-width="3.2" stroke-linejoin="round"/>'
        % (ident, INK)
    )

    # --- corps ---
    s.append(
        '<ellipse cx="0" cy="0" rx="56" ry="48" fill="url(#%s-corps)" '
        'stroke="%s" stroke-width="3.4"/>' % (ident, INK)
    )
    # ventre clair
    s.append('<ellipse cx="2" cy="22" rx="38" ry="24" fill="%s" opacity=".85"/>' % PAPER)
    # reflet
    s.append('<ellipse cx="-24" cy="-26" rx="13" ry="8" fill="#fff" opacity=".45" '
             'transform="rotate(-28 -24 -26)"/>')

    # --- nageoire laterale ---
    s.append(
        '<g transform="translate(-34 26)">'
        '<animateTransform attributeName="transform" type="rotate" '
        'values="0 0 0; 16 0 0; 0 0 0" dur="2.6s" repeatCount="indefinite" '
        'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
        '<path d="M0 0 C -12 10 -14 22 -6 26 C 2 24 8 14 8 4 Z" '
        'fill="%s" stroke="%s" stroke-width="3" stroke-linejoin="round"/>'
        '</g>' % (OCEAN, INK)
    )

    # --- masque de plongee ---
    s.append('<path d="M-52 -8 L -62 -4 M52 -8 L 62 -4" stroke="%s" stroke-width="5" '
             'stroke-linecap="round" fill="none"/>' % INK_SOFT)
    s.append(
        '<rect x="-46" y="-26" width="92" height="40" rx="17" '
        'fill="%s" fill-opacity=".30" stroke="%s" stroke-width="3.4"/>' % (MIST, INK)
    )
    # verres
    for cx in (-23, 23):
        s.append('<ellipse cx="%d" cy="-6" rx="18" ry="15" fill="%s" fill-opacity=".55" '
                 'stroke="%s" stroke-width="2.6"/>' % (cx, PAPER, INK_SOFT))

    # --- yeux ---
    if yeux == "ouverts":
        for cx in (-23, 23):
            s.append('<circle cx="%d" cy="-6" r="7.5" fill="%s"/>' % (cx, INK))
            s.append('<circle cx="%d" cy="-9" r="2.6" fill="#fff"/>' % (cx - 3))
        # clignement
        s.append(
            '<g fill="%s">'
            '<rect x="-41" y="-22" width="36" height="17" rx="8" opacity="0">'
            '<animate attributeName="opacity" values="0;0;1;0;0" dur="5.2s" '
            'keyTimes="0;.86;.9;.94;1" repeatCount="indefinite"/></rect>'
            '<rect x="5" y="-22" width="36" height="17" rx="8" opacity="0">'
            '<animate attributeName="opacity" values="0;0;1;0;0" dur="5.2s" '
            'keyTimes="0;.86;.9;.94;1" repeatCount="indefinite"/></rect>'
            '</g>' % MIST
        )
    else:  # yeux contents, en arc
        for cx in (-23, 23):
            s.append('<path d="M%d -10 q 7 -9 14 0" stroke="%s" stroke-width="4.5" '
                     'fill="none" stroke-linecap="round"/>' % (cx - 7, INK))

    # --- tuba ---
    s.append(
        '<path d="M44 -14 C 60 -16 66 -28 66 -44 L 66 -70" stroke="%s" stroke-width="7" '
        'fill="none" stroke-linecap="round"/>' % INK_SOFT
    )
    s.append('<rect x="59" y="-50" width="14" height="9" rx="3" fill="%s"/>' % OCEAN_LIGHT)

    # --- ondes au bout du tuba ---
    if ondes:
        for i, r in enumerate((10, 19, 28)):
            s.append(
                '<path d="M%d %d a %d %d 0 0 1 %d %d" stroke="%s" stroke-width="4" '
                'fill="none" stroke-linecap="round" opacity="0">'
                '<animate attributeName="opacity" values="0;.95;0" dur="2.1s" '
                'begin="%ss" repeatCount="indefinite"/>'
                '</path>' % (66 - r, -70, r, r, r, -r, OCEAN_LIGHT, f(i * 0.26))
            )

    # --- chapeau haut de forme, la recompense du musee ---
    if chapeau:
        s.append(
            '<g transform="translate(2 -62) rotate(-8)">'
            '<rect x="-30" y="-4" width="60" height="8" rx="4" fill="%s"/>'
            '<rect x="-19" y="-36" width="38" height="34" rx="4" fill="%s"/>'
            '<rect x="-19" y="-14" width="38" height="8" fill="%s"/>'
            '</g>' % (INK, INK, CORAL)
        )

    # 3 groupes ouverts quand elle flotte (translate, scale, animation), 1 sinon
    s.append("</g>" * (3 if flotte else 1))
    return "".join(s)


def degrade_mascotte(ident="m"):
    return (
        '<linearGradient id="%s-corps" x1="0" y1="0" x2=".35" y2="1">'
        '<stop offset="0" stop-color="#9DC6CE"/>'
        '<stop offset=".55" stop-color="#6FA3AE"/>'
        '<stop offset="1" stop-color="#4A8491"/>'
        '</linearGradient>' % ident
    )


def entete(w, h, titre, desc):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
        'viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">'
        '<title>%s</title><desc>%s</desc>' % (w, h, w, h, titre, titre, desc)
    )


def ecrire(nom, contenu):
    (SORTIE / nom).write_text(contenu, encoding="utf-8")
    print("  %-28s %6d octets" % (nom, len(contenu.encode("utf-8"))))


# ==========================================================================
# 1. Le logo
# ==========================================================================

def gen_logo():
    W, H = 1000, 320
    s = [entete(W, H, "Scubanion",
                "Logo anime : la mascotte flotte, les ondes du tuba pulsent, "
                "les lettres de Scubanion tombent une a une et un trait corail se trace.")]
    s.append("<defs>")
    s.append(degrade_mascotte("logo"))
    s.append('<linearGradient id="fond" x1="0" y1="0" x2=".7" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset=".6" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>' % (NUIT, INK, OCEAN_DARK))
    s.append('<radialGradient id="halo" cx=".5" cy=".5" r=".5">'
             '<stop offset="0" stop-color="%s" stop-opacity=".40"/>'
             '<stop offset="1" stop-color="%s" stop-opacity="0"/></radialGradient>' % (OCEAN, OCEAN))
    s.append("</defs>")

    s.append('<rect width="%d" height="%d" rx="28" fill="url(#fond)"/>' % (W, H))

    # bulles qui montent
    for i, (bx, br, bd, bb) in enumerate([
        (120, 5, 7.0, 0.0), (210, 3, 8.5, 1.8), (300, 4, 6.4, 3.4),
        (760, 4, 7.6, 0.9), (850, 6, 9.0, 2.6), (920, 3, 6.8, 4.4),
    ]):
        s.append(
            '<circle cx="%d" cy="%d" r="%d" fill="%s" opacity="0">'
            '<animate attributeName="cy" values="%d;-20" dur="%ss" begin="%ss" repeatCount="indefinite"/>'
            '<animate attributeName="opacity" values="0;.5;.5;0" dur="%ss" begin="%ss" repeatCount="indefinite"/>'
            '</circle>' % (bx, H + 10, br, OCEAN_LIGHT, H + 10, f(bd), f(bb), f(bd), f(bb))
        )

    s.append('<ellipse cx="215" cy="160" rx="150" ry="130" fill="url(#halo)"/>')
    s.append(mascotte(215, 158, 1.08, ident="logo"))

    # --- le mot, lettre par lettre ---
    # Une seule balise <text> : les lettres gardent leur chasse naturelle, et
    # chaque <tspan> tombe a son tour.
    s.append('<text x="412" y="150" font-family="%s" font-size="86" font-weight="800" '
             'fill="#ffffff">' % POLICE)
    for i, c in enumerate("Scubanion"):
        d = 0.14 * i
        s.append(
            '<tspan opacity="0">'
            '<animate attributeName="opacity" values="0;1" dur=".3s" begin="%ss" fill="freeze"/>'
            '<animate attributeName="dy" values="-40;8;0" dur=".5s" begin="%ss" fill="freeze" '
            'calcMode="spline" keyTimes="0;.7;1" keySplines=".3 0 .4 1;.3 1 .5 1"/>'
            '%s</tspan>' % (f(d), f(d), c)
        )
    s.append('</text>')

    # trait corail qui se trace
    s.append(
        '<line x1="412" y1="182" x2="902" y2="182" stroke="%s" stroke-width="7" '
        'stroke-linecap="round" stroke-dasharray="490" stroke-dashoffset="490">'
        '<animate attributeName="stroke-dashoffset" values="490;0" dur=".9s" '
        'begin="1.5s" fill="freeze" calcMode="spline" keySplines=".2 .7 .3 1"/>'
        '</line>' % CORAL
    )

    s.append(
        '<text x="412" y="233" font-family="%s" font-size="30" fill="%s" opacity="0">'
        '<animate attributeName="opacity" values="0;1" dur=".7s" begin="2.1s" fill="freeze"/>'
        'Il ne grandit que si <tspan fill="%s" font-weight="700">toi</tspan> tu sors.</text>'
        % (POLICE, MIST, CORAL)
    )
    s.append(
        '<text x="412" y="272" font-family="%s" font-size="19" fill="%s" opacity="0" '
        'letter-spacing="1.6">'
        '<animate attributeName="opacity" values="0;.75" dur=".7s" begin="2.4s" fill="freeze"/>'
        'COMPAGNON VIRTUEL &#183; BORNES CONNECT&#201;ES &#183; PARIS</text>'
        % (POLICE, OCEAN_LIGHT)
    )

    s.append("</svg>")
    ecrire("logo-scubanion.svg", "".join(s))


# ==========================================================================
# 2. La banniere : l'histoire en une animation
# ==========================================================================

def gen_banniere():
    W, H = 1000, 380
    SOL = 300
    T = "13s"          # duree du cycle complet
    s = [entete(W, H, "Comment marche Scubanion",
                "Animation : un joueur marche, son compteur de pas monte et son compagnon "
                "grandit ; il approche son telephone d'une borne, qui lui debloque un "
                "chapeau exclusif au lieu.")]

    s.append("<defs>")
    s.append(degrade_mascotte("ban"))
    s.append('<linearGradient id="ciel" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
             '</linearGradient>' % (MIST, PAPER))
    s.append('<linearGradient id="ecran" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
             '</linearGradient>' % (OCEAN, OCEAN_DARK))
    s.append("</defs>")

    s.append('<rect width="%d" height="%d" rx="28" fill="url(#ciel)"/>' % (W, H))

    # --- immeubles, en fond ---
    for bx, bw, bh, op in [(60, 90, 150, .16), (170, 60, 110, .12), (250, 110, 180, .17),
                           (380, 70, 130, .12), (470, 95, 165, .15), (600, 64, 120, .11)]:
        s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" opacity="%s"/>'
                 % (bx, SOL - bh, bw, bh, OCEAN, op))
        for r in range(2, bh // 34):
            for c in range(1, max(2, bw // 30)):
                s.append('<rect x="%d" y="%d" width="9" height="12" rx="2" fill="%s" opacity="%s"/>'
                         % (bx + c * 26, SOL - bh + r * 30, PAPER, f(float(op) * 2.4)))

    # --- trottoir ---
    s.append('<rect x="0" y="%d" width="%d" height="%d" fill="%s" opacity=".10"/>'
             % (SOL, W, H - SOL, OCEAN_DARK))
    s.append('<line x1="0" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="3" opacity=".45"/>'
             % (SOL, W, SOL, OCEAN_LIGHT))

    # ================= LA BORNE =================
    bx = 790
    s.append('<g transform="translate(%d %d)">' % (bx, SOL))
    s.append('<ellipse cx="0" cy="4" rx="54" ry="9" fill="%s" opacity=".18"/>' % INK)
    s.append('<rect x="-40" y="-190" width="80" height="190" rx="18" fill="%s"/>' % INK)
    s.append('<rect x="-31" y="-178" width="62" height="86" rx="10" fill="url(#ecran)"/>')
    # ecran au repos
    s.append('<g id="ecran-repos">'
             '<text x="0" y="-140" font-family="%s" font-size="13" fill="%s" '
             'text-anchor="middle">Approche</text>'
             '<text x="0" y="-124" font-family="%s" font-size="13" fill="%s" '
             'text-anchor="middle">ton t&#233;l&#233;phone</text>'
             '<animate attributeName="opacity" values="1;1;0;0;1" dur="%s" '
             'keyTimes="0;.42;.46;.93;1" repeatCount="indefinite"/></g>'
             % (POLICE, MIST, POLICE, MIST, T))
    # ecran qui revele le tableau
    s.append('<g opacity="0">'
             '<animate attributeName="opacity" values="0;0;1;1;0" dur="%s" '
             'keyTimes="0;.44;.5;.9;1" repeatCount="indefinite"/>'
             '<rect x="-27" y="-174" width="54" height="78" rx="6" fill="%s"/>'
             '<rect x="-21" y="-168" width="42" height="56" rx="3" fill="%s" opacity=".5"/>'
             '<circle cx="0" cy="-146" r="13" fill="%s" opacity=".35"/>'
             '<g transform="translate(0 -158) scale(.42)">'
             '<rect x="-30" y="-4" width="60" height="8" rx="4" fill="%s"/>'
             '<rect x="-19" y="-36" width="38" height="34" rx="4" fill="%s"/>'
             '<rect x="-19" y="-14" width="38" height="8" fill="%s"/></g>'
             '</g>' % (T, MIST, OCEAN_LIGHT, PAPER, INK, INK, CORAL))

    # anneau de LED, qui se remplit au passage
    s.append('<circle cx="0" cy="-60" r="19" fill="none" stroke="%s" stroke-width="5" opacity=".4"/>'
             % OCEAN_DARK)
    s.append('<circle cx="0" cy="-60" r="19" fill="none" stroke="%s" stroke-width="5" '
             'stroke-linecap="round" stroke-dasharray="119" stroke-dashoffset="119" '
             'transform="rotate(-90 0 -60)">'
             '<animate attributeName="stroke-dashoffset" values="119;119;0;0;119" dur="%s" '
             'keyTimes="0;.44;.56;.93;1" repeatCount="indefinite"/></circle>' % (VERT, T))
    s.append('<text x="0" y="-18" font-family="%s" font-size="12" fill="%s" '
             'text-anchor="middle" letter-spacing="1.2">SCUBANION</text>' % (POLICE, OCEAN_LIGHT))
    s.append("</g>")

    # ondes NFC au moment du passage
    for i, r in enumerate((22, 36, 50)):
        s.append(
            '<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="3.4" opacity="0">'
            '<animate attributeName="opacity" values="0;0;.9;0;0" dur="%s" '
            'keyTimes="0;%s;%s;%s;1" repeatCount="indefinite"/>'
            '</circle>' % (bx - 52, SOL - 92, r, CORAL, T,
                           f(0.42 + i * 0.012), f(0.46 + i * 0.012), f(0.52 + i * 0.012))
        )

    # ================= LE JOUEUR ET SON COMPAGNON =================
    s.append('<g>')
    s.append('<animateTransform attributeName="transform" type="translate" '
             'values="-210 0; 505 0; 505 0; -210 0" dur="%s" '
             'keyTimes="0;.42;.95;1" repeatCount="indefinite" '
             'calcMode="spline" keySplines=".35 0 .25 1;0 0 1 1;0 0 1 1"/>' % T)

    # ombre
    s.append('<ellipse cx="180" cy="%d" rx="26" ry="7" fill="%s" opacity=".18"/>' % (SOL + 2, INK))

    # jambes
    for i, sens in enumerate((1, -1)):
        s.append(
            '<line x1="180" y1="%d" x2="180" y2="%d" stroke="%s" stroke-width="9" '
            'stroke-linecap="round">'
            '<animateTransform attributeName="transform" type="rotate" '
            'values="%d 180 %d; %d 180 %d; %d 180 %d" dur=".62s" repeatCount="indefinite" '
            'calcMode="spline" keyTimes="0;.5;1" keySplines=".45 0 .55 1;.45 0 .55 1"/>'
            '</line>' % (SOL - 56, SOL, OCEAN_DARK,
                         22 * sens, SOL - 56, -22 * sens, SOL - 56, 22 * sens, SOL - 56)
        )
    # corps, tete, bras tendu vers le telephone
    s.append('<rect x="168" y="%d" width="24" height="56" rx="11" fill="%s"/>' % (SOL - 108, OCEAN))
    s.append('<circle cx="180" cy="%d" r="17" fill="%s"/>' % (SOL - 124, CORAL))
    s.append('<line x1="186" y1="%d" x2="212" y2="%d" stroke="%s" stroke-width="8" '
             'stroke-linecap="round"/>' % (SOL - 96, SOL - 86, OCEAN))

    # telephone dans la main
    s.append('<g transform="translate(212 %d)">' % (SOL - 92))
    s.append('<rect x="-10" y="-17" width="21" height="34" rx="5" fill="%s"/>' % INK)
    s.append('<rect x="-7.5" y="-14" width="16" height="28" rx="3" fill="%s"/>' % PAPER)
    # le chapeau qui tombe dans le telephone a la fin
    s.append('<g opacity="0" transform="translate(0 -3) scale(.3)">'
             '<animate attributeName="opacity" values="0;0;1;1" dur="%s" '
             'keyTimes="0;.63;.68;1" repeatCount="indefinite"/>'
             '<rect x="-30" y="-4" width="60" height="8" rx="4" fill="%s"/>'
             '<rect x="-19" y="-36" width="38" height="34" rx="4" fill="%s"/>'
             '<rect x="-19" y="-14" width="38" height="8" fill="%s"/></g>'
             % (T, INK, INK, CORAL))
    s.append("</g>")

    # compteur de pas, au-dessus du joueur
    s.append('<g transform="translate(180 %d)">' % (SOL - 158))
    s.append('<rect x="-46" y="-21" width="92" height="33" rx="16" fill="#ffffff" opacity=".92"/>')
    pas = ["147", "1 206", "2 480", "3 915", "5 000"]
    n = len(pas)
    for i, v in enumerate(pas):
        # chaque valeur apparait a son tour, pendant la marche
        k0 = 0.03 + i * (0.38 / n)
        k1 = k0 + (0.38 / n)
        s.append(
            '<text x="0" y="2" font-family="%s" font-size="19" font-weight="700" '
            'fill="%s" text-anchor="middle" opacity="0">'
            '<animate attributeName="opacity" values="0;0;1;1;0;0" dur="%s" '
            'keyTimes="0;%s;%s;%s;%s;1" repeatCount="indefinite"/>%s</text>'
            % (POLICE, INK, T, f(max(k0 - 0.004, 0)), f(k0), f(k1),
               f(min(k1 + 0.004, 0.999)), v)
        )
    s.append('<text x="0" y="2" font-family="%s" font-size="19" font-weight="700" '
             'fill="%s" text-anchor="middle" opacity="0">'
             '<animate attributeName="opacity" values="0;0;1;1;0" dur="%s" '
             'keyTimes="0;.41;.45;.93;1" repeatCount="indefinite"/>5 000 pas</text>'
             % (POLICE, VERT, T))
    s.append("</g>")

    # le compagnon, qui suit et grandit
    s.append('<g transform="translate(108 %d)">' % (SOL - 72))
    s.append('<animateTransform attributeName="transform" type="scale" '
             'values=".30;.30;.46;.46" dur="%s" keyTimes="0;.1;.42;1" '
             'repeatCount="indefinite" additive="sum"/>' % T)
    s.append(mascotte(0, 0, 1.0, ident="ban", ondes=False))
    s.append("</g>")

    s.append("</g>")  # fin du groupe joueur

    # ================= LE BANDEAU DE FIN =================
    s.append('<g opacity="0">'
             '<animate attributeName="opacity" values="0;0;1;1;0" dur="%s" '
             'keyTimes="0;.70;.76;.93;1" repeatCount="indefinite"/>'
             '<rect x="250" y="38" width="500" height="74" rx="22" fill="%s" opacity=".95"/>'
             '<text x="500" y="72" font-family="%s" font-size="25" font-weight="700" '
             'fill="#ffffff" text-anchor="middle">Chapeau du Portrait &#8212; d&#233;bloqu&#233; !</text>'
             '<text x="500" y="97" font-family="%s" font-size="16" fill="%s" '
             'text-anchor="middle">Exclusif au mus&#233;e. On ne l\'obtient qu\'en y allant.</text>'
             '</g>' % (T, INK, POLICE, POLICE, OCEAN_LIGHT))

    s.append("</svg>")
    ecrire("banniere.svg", "".join(s))


# ==========================================================================
# 3. La boucle : pas -> XP -> quete -> borne -> recompense
# ==========================================================================

def gen_boucle():
    W, H = 1000, 380
    cx, cy, R = 500, 190, 95
    etapes = [
        ("Tu marches", "le téléphone compte"),
        ("Il grandit", "chaque pas vaut de l'XP"),
        ("Une quête", "à moins de 500 m"),
        ("Une borne", "chez un partenaire"),
        ("Un objet", "exclusif au lieu"),
    ]
    n = len(etapes)
    T = 10.0

    s = [entete(W, H, "La boucle Scubanion",
                "Diagramme anime : marcher fait grandir le compagnon, qui envoie vers "
                "une quete, puis vers une borne, qui debloque un objet exclusif, "
                "ce qui redonne envie de marcher.")]
    s.append("<defs>" + degrade_mascotte("bcl") + "</defs>")
    s.append('<rect width="%d" height="%d" rx="24" fill="%s"/>' % (W, H, PAPER))

    # anneau
    s.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="2.5" '
             'stroke-dasharray="7 9" opacity=".55"/>' % (cx, cy, R, OCEAN_LIGHT))

    # point qui parcourt la boucle
    s.append('<circle r="7" fill="%s">'
             '<animateMotion dur="%ss" repeatCount="indefinite" '
             'path="M %d %d a %d %d 0 1 1 -0.1 0"/></circle>'
             % (CORAL, f(T), cx, cy - R, R, R))

    for i, (titre, sous) in enumerate(etapes):
        a = -math.pi / 2 + i * 2 * math.pi / n
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        d = i * T / n
        # Le keyTimes doit aller jusqu'a 1, sinon SMIL ignore l'animation :
        # la pastille s'allume au passage du point, puis reste blanche.
        s.append(
            '<circle cx="%s" cy="%s" r="15" fill="%s" stroke="%s" stroke-width="3">'
            '<animate attributeName="fill" values="%s;%s;%s;%s" dur="%ss" begin="%ss" '
            'repeatCount="indefinite" keyTimes="0;.05;.17;1"/>'
            '<animate attributeName="r" values="15;20;15;15" dur="%ss" begin="%ss" '
            'repeatCount="indefinite" keyTimes="0;.05;.17;1"/>'
            '</circle>' % (f(x), f(y), "#ffffff", OCEAN, "#ffffff", CORAL, "#ffffff",
                           "#ffffff", f(T), f(d), f(T), f(d))
        )
        s.append('<text x="%s" y="%s" font-family="%s" font-size="15" font-weight="700" '
                 'fill="%s" text-anchor="middle">%d</text>'
                 % (f(x), f(y + 5), POLICE, OCEAN_DARK, i + 1))

        # etiquette, poussee vers l'exterieur
        lx = cx + (R + 64) * math.cos(a)
        ly = cy + (R + 64) * math.sin(a)
        anc = "middle"
        if abs(math.cos(a)) > 0.3:
            anc = "start" if math.cos(a) > 0 else "end"
        s.append('<text x="%s" y="%s" font-family="%s" font-size="17" font-weight="700" '
                 'fill="%s" text-anchor="%s">%s</text>'
                 % (f(lx), f(ly), POLICE, INK, anc, titre))
        s.append('<text x="%s" y="%s" font-family="%s" font-size="13" fill="%s" '
                 'text-anchor="%s">%s</text>'
                 % (f(lx), f(ly + 18), POLICE, INK_SOFT, anc, sous))

    # la mascotte, au centre
    s.append(mascotte(cx, cy + 4, 0.55, ident="bcl", ondes=False, yeux="contents"))

    s.append("</svg>")
    ecrire("boucle.svg", "".join(s))


# ==========================================================================
# 4. Les cartes d'equipe
# ==========================================================================

EQUIPE = [
    ("Picsou06", "Evan Dalmasso", "Application mobile", "produit et relation utilisateur"),
    ("CodeByHaamza", "Hamza Karrouchi", "Back-end et données", "plateforme, API, modèle"),
    ("Tiretinium", "Thomas Bandieras", "CI/CD et infrastructure", "tests, images, déploiement"),
    ("shalee-pnt", "Shaleena Lesueur", "Borne IoT", "matériel, NFC, MQTT"),
]


def gen_equipe():
    W, H = 340, 300
    for login, nom, lot, sous in EQUIPE:
        fichier = AVATARS / ("%s.jpg" % login)
        s = [entete(W, H, "%s — %s" % (nom, lot),
                    "Carte d'equipe : %s, %s." % (nom, lot.lower()))]
        s.append('<defs><clipPath id="rond-%s"><circle cx="170" cy="104" r="54"/></clipPath>'
                 '<linearGradient id="cg-%s" x1="0" y1="0" x2=".4" y2="1">'
                 '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
                 '</linearGradient></defs>' % (login, login, INK, OCEAN_DARK))
        s.append('<rect width="%d" height="%d" rx="22" fill="url(#cg-%s)"/>' % (W, H, login))

        # anneau qui tourne lentement autour de l'avatar
        s.append('<circle cx="170" cy="104" r="62" fill="none" stroke="%s" stroke-width="3" '
                 'stroke-dasharray="14 10" opacity=".65">'
                 '<animateTransform attributeName="transform" type="rotate" '
                 'from="0 170 104" to="360 170 104" dur="22s" repeatCount="indefinite"/>'
                 '</circle>' % CORAL)

        if fichier.exists():
            b64 = base64.b64encode(fichier.read_bytes()).decode()
            s.append('<image x="116" y="50" width="108" height="108" '
                     'clip-path="url(#rond-%s)" preserveAspectRatio="xMidYMid slice" '
                     'href="data:image/jpeg;base64,%s" xlink:href="data:image/jpeg;base64,%s"/>'
                     % (login, b64, b64))
        else:
            s.append('<circle cx="170" cy="104" r="54" fill="%s"/>' % OCEAN)

        s.append('<text x="170" y="196" font-family="%s" font-size="21" font-weight="700" '
                 'fill="#ffffff" text-anchor="middle">%s</text>' % (POLICE, nom))
        s.append('<text x="170" y="222" font-family="%s" font-size="15" font-weight="600" '
                 'fill="%s" text-anchor="middle">%s</text>' % (POLICE, CORAL, lot))
        s.append('<text x="170" y="243" font-family="%s" font-size="12.5" fill="%s" '
                 'text-anchor="middle">%s</text>' % (POLICE, OCEAN_LIGHT, sous))
        s.append('<text x="170" y="272" font-family="%s" font-size="12.5" fill="%s" '
                 'text-anchor="middle">@%s</text>' % (MONO, MIST, login))

        s.append("</svg>")
        ecrire("equipe-%s.svg" % login, "".join(s))


if __name__ == "__main__":
    print("Generation dans %s" % SORTIE)
    gen_logo()
    gen_banniere()
    gen_boucle()
    gen_equipe()
    print("termine")
