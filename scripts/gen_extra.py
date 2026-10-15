# -*- coding: utf-8 -*-
"""Visuels complementaires du profil : carrousel de l'app, borne annotee,
feuille de route et bandeau de chiffres.

Aucune dependance : bibliotheque standard uniquement.
Usage : python scripts/gen_extra.py [dossier_de_sortie]
"""
import base64
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gen_assets import (  # noqa: E402
    POLICE, MONO, INK, INK_SOFT, OCEAN, OCEAN_DARK, OCEAN_LIGHT, MIST, PAPER,
    CORAL, CORAL_DARK, VERT, NUIT, f, entete, mascotte,
)

SORTIE = Path(sys.argv[1] if len(sys.argv) > 1 else "profile/assets")
ECRANS = SORTIE / "ecrans"
SORTIE.mkdir(parents=True, exist_ok=True)


def ecrire(nom, contenu):
    (SORTIE / nom).write_text(contenu, encoding="utf-8")
    print("  %-28s %6d octets" % (nom, len(contenu.encode("utf-8"))))


def creneau(i, n, fondu=0.02):
    """keyTimes d'un element visible pendant le i-eme creneau sur n."""
    d, fin = i / n, (i + 1) / n
    pts = [0.0, d, min(d + fondu, fin), max(fin - fondu, d), fin, 1.0]
    pts = [min(max(p, 0.0), 1.0) for p in pts]
    for k in range(1, len(pts)):           # la suite doit rester croissante
        pts[k] = max(pts[k], pts[k - 1])
    return ";".join(f(p) for p in pts)


# ==========================================================================
# 1. Le carrousel de l'application
# ==========================================================================

ECRANS_LISTE = [
    ("accueil", "Accueil", "le compagnon et les pas du jour"),
    ("quetes", "Quêtes", "quiz, photos, nouveaux lieux, défis"),
    ("carte", "Carte", "bornes et quêtes à proximité"),
    ("amis", "Amis", "invitation par code, rencontres"),
    ("profil", "Profil", "ambition, inventaire, objets rares"),
]


def gen_carrousel():
    W, H = 1000, 470
    T = "16s"
    dispo = [(c, t, s) for c, t, s in ECRANS_LISTE if (ECRANS / ("%s.jpg" % c)).exists()]
    n = len(dispo)
    if not n:
        print("  (pas d'ecrans a embarquer)")
        return

    PX, PY, PW, PH = 390, 26, 220, 418       # cadre du telephone

    s = [entete(W, H, "L'application Scubanion",
                "Carrousel anime : les ecrans de l'application se succedent dans un "
                "telephone, avec leur legende.")]
    s.append("<defs>")
    s.append('<clipPath id="ecran-tel"><rect x="%d" y="%d" width="%d" height="%d" rx="22"/></clipPath>'
             % (PX + 9, PY + 9, PW - 18, PH - 18))
    s.append('<linearGradient id="fond-car" x1="0" y1="0" x2=".6" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
             '</linearGradient>' % (MIST, PAPER))
    s.append("</defs>")
    s.append('<rect width="%d" height="%d" rx="24" fill="url(#fond-car)"/>' % (W, H))

    # halo derriere le telephone
    s.append('<ellipse cx="%d" cy="%d" rx="150" ry="170" fill="%s" opacity=".18"/>'
             % (PX + PW // 2, PY + PH // 2, OCEAN_LIGHT))

    # --- les ecrans, qui se succedent ---
    s.append('<g clip-path="url(#ecran-tel)">')
    s.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
             % (PX + 9, PY + 9, PW - 18, PH - 18, PAPER))
    for i, (code, _, _) in enumerate(dispo):
        b64 = base64.b64encode((ECRANS / ("%s.jpg" % code)).read_bytes()).decode()
        s.append(
            '<image x="%d" y="%d" width="%d" height="%d" preserveAspectRatio="xMidYMid slice" '
            'opacity="0" href="data:image/jpeg;base64,%s" xlink:href="data:image/jpeg;base64,%s">'
            '<animate attributeName="opacity" values="0;0;1;1;0;0" dur="%s" '
            'keyTimes="%s" repeatCount="indefinite"/></image>'
            % (PX + 9, PY + 9, PW - 18, PH - 18, b64, b64, T, creneau(i, n))
        )
    s.append("</g>")

    # --- chassis du telephone ---
    s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="30" fill="none" '
             'stroke="%s" stroke-width="9"/>' % (PX, PY, PW, PH, INK))
    s.append('<rect x="%d" y="%d" width="56" height="9" rx="5" fill="%s"/>'
             % (PX + PW // 2 - 28, PY + 13, INK))

    # --- legendes, a droite ---
    for i, (_, titre, sous) in enumerate(dispo):
        s.append(
            '<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" '
            'dur="%s" keyTimes="%s" repeatCount="indefinite"/>'
            '<text x="660" y="188" font-family="%s" font-size="40" font-weight="800" '
            'fill="%s">%s</text>'
            '<text x="660" y="222" font-family="%s" font-size="17" fill="%s">%s</text>'
            '</g>' % (T, creneau(i, n), POLICE, INK, titre, POLICE, INK_SOFT, sous)
        )

    s.append('<text x="660" y="96" font-family="%s" font-size="15" fill="%s" '
             'letter-spacing="2.2">L’APPLICATION</text>' % (POLICE, OCEAN))
    s.append('<line x1="660" y1="112" x2="716" y2="112" stroke="%s" stroke-width="5" '
             'stroke-linecap="round"/>' % CORAL)

    # --- pastilles de progression ---
    for i in range(n):
        s.append(
            '<circle cx="%d" cy="268" r="6" fill="%s">'
            '<animate attributeName="fill" values="%s;%s;%s;%s" dur="%s" '
            'keyTimes="%s" repeatCount="indefinite"/>'
            '</circle>' % (664 + i * 22, OCEAN_LIGHT, OCEAN_LIGHT, CORAL, CORAL,
                           OCEAN_LIGHT, T, creneau(i, n, 0.004))
        )

    # la mascotte, en bas a droite
    s.append(mascotte(176, 336, 0.60))
    s.append('<text x="660" y="378" font-family="%s" font-size="14.5" fill="%s">'
             'Maquettes du dépôt, pas des images d’illustration.</text>'
             % (POLICE, INK_SOFT))
    s.append('<text x="660" y="400" font-family="%s" font-size="14.5" fill="%s">'
             'Elles servent de référence de design à l’app.</text>'
             % (POLICE, INK_SOFT))

    s.append("</svg>")
    ecrire("app-carrousel.svg", "".join(s))


# ==========================================================================
# 2. La borne, annotee
# ==========================================================================

def gen_borne():
    W, H = 1000, 450
    T = "11s"
    s = [entete(W, H, "La borne Scubanion",
                "Schema anime de la borne : ecran, anneau de LED, lecteur NFC, "
                "microcontroleur, chaque element annote a son tour.")]
    s.append("<defs>")
    s.append('<linearGradient id="fond-b" x1="0" y1="0" x2=".6" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset=".6" stop-color="%s"/>'
             '<stop offset="1" stop-color="%s"/></linearGradient>' % (NUIT, INK, OCEAN_DARK))
    s.append('<linearGradient id="ecr" x1="0" y1="0" x2="0" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/>'
             '</linearGradient>' % (OCEAN, OCEAN_DARK))
    s.append("</defs>")
    s.append('<rect width="%d" height="%d" rx="24" fill="url(#fond-b)"/>' % (W, H))

    BX, BY = 430, 48     # coin haut gauche de la borne
    BW, BH = 150, 334

    s.append('<ellipse cx="%d" cy="%d" rx="110" ry="16" fill="#000" opacity=".30"/>'
             % (BX + BW // 2, BY + BH + 6))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="26" fill="#243d45" '
             'stroke="%s" stroke-width="3"/>' % (BX, BY, BW, BH, OCEAN_DARK))

    # ecran
    s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="14" fill="url(#ecr)"/>'
             % (BX + 16, BY + 20, BW - 32, 150))
    s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="%s" opacity=".9"/>'
             % (BX + 28, BY + 34, BW - 56, 100, MIST))
    s.append('<g transform="translate(%d %d) scale(.5)">'
             '<rect x="-30" y="-4" width="60" height="8" rx="4" fill="%s"/>'
             '<rect x="-19" y="-36" width="38" height="34" rx="4" fill="%s"/>'
             '<rect x="-19" y="-14" width="38" height="8" fill="%s"/></g>'
             % (BX + BW // 2, BY + 96, INK, INK, CORAL))
    s.append('<text x="%d" y="%d" font-family="%s" font-size="12" fill="%s" '
             'text-anchor="middle">Chapeau du Portrait</text>'
             % (BX + BW // 2, BY + 150, POLICE, PAPER))

    # anneau de LED
    cxl, cyl = BX + BW // 2, BY + 212
    s.append('<circle cx="%d" cy="%d" r="30" fill="none" stroke="%s" stroke-width="7" '
             'opacity=".35"/>' % (cxl, cyl, OCEAN_DARK))
    s.append('<circle cx="%d" cy="%d" r="30" fill="none" stroke="%s" stroke-width="7" '
             'stroke-linecap="round" stroke-dasharray="188" stroke-dashoffset="188" '
             'transform="rotate(-90 %d %d)">'
             '<animate attributeName="stroke-dashoffset" values="188;188;0;0;188;188" '
             'dur="%s" keyTimes="0;.12;.30;.72;.80;1" repeatCount="indefinite"/>'
             '</circle>' % (cxl, cyl, VERT, cxl, cyl, T))

    # zone NFC
    s.append('<rect x="%d" y="%d" width="%d" height="46" rx="12" fill="%s" opacity=".22"/>'
             % (BX + 26, BY + 244, BW - 52, OCEAN_LIGHT))
    s.append('<text x="%d" y="%d" font-family="%s" font-size="12" fill="%s" '
             'text-anchor="middle" letter-spacing="1.4">NFC</text>'
             % (BX + BW // 2, BY + 272, POLICE, MIST))
    for i, r in enumerate((14, 24, 34)):
        s.append('<circle cx="%d" cy="%d" r="%d" fill="none" stroke="%s" stroke-width="3" '
                 'opacity="0"><animate attributeName="opacity" values="0;0;.85;0;0" '
                 'dur="%s" keyTimes="0;%s;%s;%s;1" repeatCount="indefinite"/></circle>'
                 % (BX - 4, BY + 266, r, CORAL, T,
                    f(0.06 + i * 0.012), f(0.10 + i * 0.012), f(0.17 + i * 0.012)))

    s.append('<text x="%d" y="%d" font-family="%s" font-size="13" fill="%s" '
             'text-anchor="middle" letter-spacing="2">SCUBANION</text>'
             % (BX + BW // 2, BY + BH - 18, POLICE, OCEAN_LIGHT))

    # --- annotations, l'une apres l'autre ---
    notes = [
        (BX + BW + 10, BY + 70, 700, "Écran", "il montre le lieu et l’objet débloqué", "d"),
        (BX + BW + 10, cyl, 700, "Anneau de LED", "il se remplit pendant la lecture", "d"),
        (BX - 10, BY + 266, 292, "Lecteur NFC", "le téléphone s’approche, rien à saisir", "g"),
        (BX - 10, BY + 150, 292, "Microcontrôleur", "il publie le passage en MQTT", "g"),
    ]
    n = len(notes)
    for i, (ax, ay, tx, titre, sous, sens) in enumerate(notes):
        anc = "start" if sens == "d" else "end"
        s.append('<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0;0" '
                 'dur="%s" keyTimes="%s" repeatCount="indefinite"/>' % (T, creneau(i, n)))
        s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="2.4" '
                 'stroke-dasharray="5 5"/>' % (ax, ay, tx, ay, CORAL))
        s.append('<circle cx="%d" cy="%d" r="5" fill="%s"/>' % (ax, ay, CORAL))
        s.append('<text x="%d" y="%d" font-family="%s" font-size="25" font-weight="700" '
                 'fill="#ffffff" text-anchor="%s">%s</text>'
                 % (tx + (14 if sens == "d" else -14), ay - 4, POLICE, anc, titre))
        s.append('<text x="%d" y="%d" font-family="%s" font-size="15" fill="%s" '
                 'text-anchor="%s">%s</text>'
                 % (tx + (14 if sens == "d" else -14), ay + 20, POLICE, OCEAN_LIGHT, anc, sous))
        s.append("</g>")

    s.append('<text x="40" y="52" font-family="%s" font-size="15" fill="%s" '
             'letter-spacing="2.2">NOTRE SEUL OBJET</text>' % (POLICE, OCEAN_LIGHT))
    s.append('<text x="40" y="420" font-family="%s" font-size="14.5" fill="%s">'
             'Un objet conçu de bout en bout, du microcontrôleur au protocole, '
             'plutôt que deux à moitié.</text>' % (POLICE, MIST))

    s.append("</svg>")
    ecrire("borne.svg", "".join(s))


# ==========================================================================
# 3. La feuille de route
# ==========================================================================

JALONS = [
    ("Cadrage", "sept. – oct. 2026", "fait"),
    ("Jalon zéro", "12 déc. 2026", "encours"),
    ("Soutenance", "13 janv. 2027", "avenir"),
    ("Pilote 10 lieux", "30 juin 2027", "avenir"),
    ("Lancement", "31 déc. 2027", "avenir"),
]


def gen_route():
    W, H = 1000, 230
    y = 112
    x0, x1 = 90, 910
    n = len(JALONS)
    pas = (x1 - x0) / (n - 1)
    avance = 1.4 / (n - 1)          # on est au milieu du jalon 2

    s = [entete(W, H, "Feuille de route",
                "Feuille de route animee : cadrage termine, jalon zero en cours, "
                "puis soutenance, pilote et lancement commercial.")]
    s.append('<rect width="%d" height="%d" rx="24" fill="%s"/>' % (W, H, PAPER))

    s.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="5" '
             'stroke-linecap="round"/>' % (x0, y, x1, y, MIST))
    s.append('<line x1="%d" y1="%d" x2="%s" y2="%d" stroke="%s" stroke-width="5" '
             'stroke-linecap="round" stroke-dasharray="%s" stroke-dashoffset="%s">'
             '<animate attributeName="stroke-dashoffset" values="%s;0" dur="1.6s" '
             'fill="freeze" calcMode="spline" keySplines=".25 .8 .3 1"/></line>'
             % (x0, y, f(x0 + (x1 - x0) * avance), y, CORAL,
                f((x1 - x0) * avance), f((x1 - x0) * avance), f((x1 - x0) * avance)))

    for i, (titre, date, etat) in enumerate(JALONS):
        x = x0 + i * pas
        d = 0.3 + i * 0.16
        if etat == "fait":
            rempli, trait, txt = CORAL, CORAL, INK
        elif etat == "encours":
            rempli, trait, txt = "#ffffff", CORAL, INK
        else:
            rempli, trait, txt = "#ffffff", OCEAN_LIGHT, INK_SOFT

        if etat == "encours":       # il pulse, c'est la ou on en est
            s.append('<circle cx="%s" cy="%d" r="13" fill="none" stroke="%s" stroke-width="3" '
                     'opacity=".55"><animate attributeName="r" values="13;24;13" dur="2.6s" '
                     'repeatCount="indefinite"/><animate attributeName="opacity" '
                     'values=".55;0;.55" dur="2.6s" repeatCount="indefinite"/></circle>'
                     % (f(x), y, CORAL))

        s.append('<circle cx="%s" cy="%d" r="0" fill="%s" stroke="%s" stroke-width="4">'
                 '<animate attributeName="r" values="0;15;12" dur=".5s" begin="%ss" '
                 'fill="freeze" calcMode="spline" keyTimes="0;.7;1" '
                 'keySplines=".3 0 .3 1;.4 0 .6 1"/></circle>'
                 % (f(x), y, rempli, trait, f(d)))

        if etat == "fait":
            s.append('<path d="M%s %d l 4 4 l 7 -8" stroke="#ffffff" stroke-width="3" '
                     'fill="none" stroke-linecap="round" stroke-linejoin="round" opacity="0">'
                     '<animate attributeName="opacity" values="0;1" dur=".3s" begin="%ss" '
                     'fill="freeze"/></path>' % (f(x - 5.5), y, f(d + 0.3)))

        s.append('<g opacity="0"><animate attributeName="opacity" values="0;1" dur=".45s" '
                 'begin="%ss" fill="freeze"/>'
                 '<text x="%s" y="%d" font-family="%s" font-size="19" font-weight="700" '
                 'fill="%s" text-anchor="middle">%s</text>'
                 '<text x="%s" y="%d" font-family="%s" font-size="14" fill="%s" '
                 'text-anchor="middle">%s</text></g>'
                 % (f(d + 0.15), f(x), y - 34, POLICE, txt, titre,
                    f(x), y + 40, POLICE, INK_SOFT, date))

    s.append('<text x="%d" y="38" font-family="%s" font-size="15" fill="%s" '
             'letter-spacing="2.2">OÙ ON EN EST</text>' % (x0 - 10, POLICE, OCEAN))
    s.append('<text x="%d" y="%d" font-family="%s" font-size="14" fill="%s">'
             '6 exigences <tspan font-style="italic">Must</tspan> sur 18 livrées, '
             '9 en revue. Le point dur est matériel : la borne n’est pas encore montée.</text>'
             % (x0 - 10, H - 24, POLICE, INK_SOFT))

    s.append("</svg>")
    ecrire("feuille-de-route.svg", "".join(s))


# ==========================================================================
# 4. Le bandeau de chiffres
# ==========================================================================

CHIFFRES = [
    (["0", "4", "11", "18"], "exigences <i>Must</i>", "périmètre du jalon zéro"),
    (["0", "60", "140", "206"], "tests côté serveur", "règles du jeu et API"),
    (["0", "9", "19", "28"], "PR fusionnées", "revue croisée obligatoire"),
    (["0", "3", "7", "9"], "entretiens terrain", "méthode Toolbox Persona"),
]


def gen_chiffres():
    W, H = 1000, 180
    T = "7s"
    s = [entete(W, H, "Les chiffres du projet",
                "Bandeau anime : les compteurs montent jusqu'a leur valeur.")]
    s.append('<rect width="%d" height="%d" rx="24" fill="%s"/>' % (W, H, INK))

    larg = W / len(CHIFFRES)
    for i, (etapes, libelle, sous) in enumerate(CHIFFRES):
        cx = larg * i + larg / 2
        if i:
            s.append('<line x1="%s" y1="44" x2="%s" y2="%d" stroke="%s" stroke-width="1.5" '
                     'opacity=".28"/>' % (f(larg * i), f(larg * i), H - 44, OCEAN_LIGHT))

        m = len(etapes)
        for k, v in enumerate(etapes):
            # chaque palier n'apparait qu'a son tour, et le dernier reste
            if k == m - 1:
                kt, vals = "0;%s;%s;1" % (f(0.1 + k * 0.06), f(0.14 + k * 0.06)), "0;0;1;1"
            else:
                kt = "0;%s;%s;%s;%s;1" % (f(0.1 + k * 0.06), f(0.105 + k * 0.06),
                                          f(0.135 + k * 0.06), f(0.14 + k * 0.06))
                vals = "0;0;1;1;0;0"
            s.append('<text x="%s" y="86" font-family="%s" font-size="46" font-weight="800" '
                     'fill="#ffffff" text-anchor="middle" opacity="0">'
                     '<animate attributeName="opacity" values="%s" dur="%s" keyTimes="%s" '
                     'repeatCount="indefinite"/>%s</text>'
                     % (f(cx), POLICE, vals, T, kt, v))

        s.append('<text x="%s" y="116" font-family="%s" font-size="17" font-weight="600" '
                 'fill="%s" text-anchor="middle">%s</text>'
                 % (f(cx), POLICE, CORAL, libelle.replace("<i>", "").replace("</i>", "")))
        s.append('<text x="%s" y="138" font-family="%s" font-size="13" fill="%s" '
                 'text-anchor="middle">%s</text>' % (f(cx), POLICE, OCEAN_LIGHT, sous))

    s.append("</svg>")
    ecrire("chiffres.svg", "".join(s))


if __name__ == "__main__":
    print("Generation dans %s" % SORTIE)
    gen_carrousel()
    gen_borne()
    gen_route()
    gen_chiffres()
    print("termine")
