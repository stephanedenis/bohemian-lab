"""
Expérience 010 — Acquisition des données empiriques du pendule.

Lit les trames JSON émises par l'ESP32 embarqué (port série ou MQTT)
et les enregistre dans un fichier CSV structuré dans data/empirique/.

La chaîne d'acquisition :
    ESP32 (firmware/) → série JSON @ 100 Hz → ce script → CSV

Usage :
    # Mode série (recommandé)
    python experiments/010_acquisition.py --port /dev/ttyUSB0 --type test_principal

    # Mode série avec options complètes
    python experiments/010_acquisition.py \\
        --port /dev/ttyUSB0 \\
        --type test_principal \\
        --operateur "S. Denis" \\
        --duree 600 \\
        --notes "Premier essai extérieur"

    # Mode MQTT (Wi-Fi)
    python experiments/010_acquisition.py \\
        --mqtt --broker 192.168.1.100 \\
        --type reference_vide

Documentation : docs/08_acquisition.md
Format CSV :   data/empirique/README.md
"""
import argparse
import json
import signal
import sys
import time
from datetime import datetime
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════
# Constantes
# ═══════════════════════════════════════════════════════════════════════

DOSSIER_SORTIE = Path(__file__).resolve().parent.parent / "data" / "empirique"

TYPES_ESSAI: list[str] = [
    "calibration",
    "reference_vide",
    "reference_fantome",
    "test_principal",
    "controle_inversion",
    "controle_argon",
    "controle_vide",
]

# Colonnes du fichier CSV de sortie
COLONNES_CSV: list[str] = [
    "timestamp_ms",
    "psd_urad",
    "P_mbar",
    "Pr_mW",
    "lum_mV",
    "T_paroi_C",
    "I_mag_mA",
    "V_bat_V",
    "duty_vanne",
    "duty_RF",
    "commande_mag",
    "etat",
]

# Mapping des champs JSON ESP32 → colonnes CSV
MAPPING_JSON: dict[str, str] = {
    "t": "timestamp_ms",
    "psd": "psd_urad",
    "P": "P_mbar",
    "Pr": "Pr_mW",
    "lum": "lum_mV",
    "T": "T_paroi_C",
    "I": "I_mag_mA",
    "V": "V_bat_V",
    "dv": "duty_vanne",
    "dr": "duty_RF",
    "mag": "commande_mag",
    "st": "etat",
}

# Mapping des codes d'état courts → noms longs
ETATS: dict[str, str] = {
    "I": "INIT",
    "P": "POMPAGE",
    "L": "PLASMA",
    "M": "MESURE",
    "E": "ERREUR",
    "F": "FIN",
}

# Fréquence d'échantillonnage attendue
FE_HZ: int = 100

# Paramètres par défaut du pendule (§3.6)
KAPPA_DEFAULT: float = 1e-5      # N·m/rad
L_BRAS_DEFAULT: float = 0.200    # m
T0_DEFAULT: float = 444.3        # s


# ═══════════════════════════════════════════════════════════════════════
# Génération du nom de fichier
# ═══════════════════════════════════════════════════════════════════════

def generer_nom_fichier(type_essai: str, dossier: Path = DOSSIER_SORTIE) -> Path:
    """Génère le nom du fichier CSV selon la convention de nommage.

    Format : AAAA-MM-JJ_HHhMM_type_NNN.csv

    Args:
        type_essai: Type d'essai (voir TYPES_ESSAI).
        dossier: Dossier de sortie.

    Returns:
        Chemin complet du fichier CSV.
    """
    maintenant = datetime.now()
    prefixe = maintenant.strftime("%Y-%m-%d_%Hh%M")

    # Trouver le prochain numéro séquentiel
    patron = f"{prefixe}_{type_essai}_*.csv"
    existants = list(dossier.glob(patron))
    numero = len(existants) + 1

    nom = f"{prefixe}_{type_essai}_{numero:03d}.csv"
    return dossier / nom


# ═══════════════════════════════════════════════════════════════════════
# En-tête de métadonnées
# ═══════════════════════════════════════════════════════════════════════

def ecrire_entete(
    fichier,
    type_essai: str,
    operateur: str = "",
    duree_s: float = 0,
    notes: str = "",
    pression_initiale: float = 0.0,
    t0_s: float = T0_DEFAULT,
    kappa: float = KAPPA_DEFAULT,
    l_bras: float = L_BRAS_DEFAULT,
) -> None:
    """Écrit les métadonnées en en-tête du fichier CSV.

    Les lignes de métadonnées commencent par '#' et sont ignorées
    par pandas.read_csv(comment='#').

    Args:
        fichier: Objet fichier ouvert en écriture.
        type_essai: Type d'essai.
        operateur: Nom de l'opérateur.
        duree_s: Durée prévue de l'acquisition (s).
        notes: Notes libres.
        pression_initiale: Pression initiale (mbar).
        t0_s: Période du pendule (s).
        kappa: Constante de torsion (N·m/rad).
        l_bras: Longueur du bras de levier (m).
    """
    maintenant = datetime.now().isoformat()

    fichier.write(f"# bohemian-lab — données empiriques\n")
    fichier.write(f"# date: {maintenant}\n")
    fichier.write(f"# type: {type_essai}\n")
    fichier.write(f"# operateur: {operateur}\n")
    fichier.write(f"# pression_initiale_mbar: {pression_initiale:.2f}\n")
    fichier.write(f"# T0_s: {t0_s:.1f}\n")
    fichier.write(f"# kappa_Nm_rad: {kappa:.2e}\n")
    fichier.write(f"# L_bras_m: {l_bras:.3f}\n")
    fichier.write(f"# duree_s: {duree_s:.0f}\n")
    fichier.write(f"# fe_Hz: {FE_HZ}\n")
    fichier.write(f"# firmware_version: 1.0.0\n")
    fichier.write(f"# notes: {notes}\n")

    # Ligne d'en-tête CSV
    fichier.write(",".join(COLONNES_CSV) + "\n")


# ═══════════════════════════════════════════════════════════════════════
# Conversion trame JSON → ligne CSV
# ═══════════════════════════════════════════════════════════════════════

def json_vers_csv(trame: dict) -> str:
    """Convertit une trame JSON ESP32 en ligne CSV.

    Args:
        trame: Dictionnaire issu du parsing JSON de la trame série.

    Returns:
        Ligne CSV formatée (sans retour à la ligne).
    """
    valeurs: list[str] = []
    for col in COLONNES_CSV:
        # Trouver la clé JSON correspondante
        cle_json = None
        for k, v in MAPPING_JSON.items():
            if v == col:
                cle_json = k
                break

        if cle_json and cle_json in trame:
            val = trame[cle_json]
            # Convertir le code d'état court en nom long
            if col == "etat" and isinstance(val, str):
                val = ETATS.get(val, val)
            valeurs.append(str(val))
        else:
            valeurs.append("")

    return ",".join(valeurs)


# ═══════════════════════════════════════════════════════════════════════
# Acquisition série
# ═══════════════════════════════════════════════════════════════════════

def acquisition_serie(
    port: str,
    fichier_csv: Path,
    type_essai: str,
    operateur: str = "",
    duree_max: float = 0,
    notes: str = "",
    baudrate: int = 115200,
    attendre_mesure: bool = True,
) -> dict:
    """Acquisition des données via port série USB.

    Lit les trames JSON de l'ESP32 et les écrit en CSV.

    Args:
        port: Port série (ex: '/dev/ttyUSB0').
        fichier_csv: Chemin du fichier CSV de sortie.
        type_essai: Type d'essai.
        operateur: Nom de l'opérateur.
        duree_max: Durée maximale (s), 0 = infini.
        notes: Notes libres.
        baudrate: Vitesse du port série.
        attendre_mesure: Si True, attend l'état MESURE pour enregistrer.

    Returns:
        Statistiques de l'acquisition (nombre de lignes, durée, etc.).
    """
    try:
        import serial
    except ImportError:
        print("❌ Module 'pyserial' requis : pip install pyserial")
        sys.exit(1)

    stats = {
        "lignes": 0,
        "erreurs_json": 0,
        "debut": time.time(),
        "fin": 0,
        "pression_initiale": 0.0,
    }

    print(f"📡 Connexion série → {port} @ {baudrate} bps")
    ser = serial.Serial(port, baudrate, timeout=1)
    time.sleep(2)  # Attente reset ESP32

    # Ouvrir le fichier CSV
    fichier_csv.parent.mkdir(parents=True, exist_ok=True)

    enregistrement_actif = not attendre_mesure
    premiere_ligne = True

    with open(fichier_csv, "w", encoding="utf-8") as f:
        # L'en-tête sera écrit au début de l'enregistrement

        print("⏳ En attente de données...")
        if attendre_mesure:
            print("   (enregistrement démarre à l'état MESURE)")
        print("   Ctrl+C pour arrêter\n")

        try:
            while True:
                ligne = ser.readline().decode("utf-8", errors="replace").strip()
                if not ligne:
                    continue

                # Ignorer les lignes qui ne sont pas du JSON
                if not ligne.startswith("{"):
                    continue

                try:
                    trame = json.loads(ligne)
                except json.JSONDecodeError:
                    stats["erreurs_json"] += 1
                    continue

                # Vérifier l'état
                etat = trame.get("st", "")

                # Détection de l'état FIN → arrêt
                if etat == "F":
                    print("\n🏁 État FIN reçu — arrêt de l'acquisition")
                    break

                # Attendre l'état MESURE pour commencer
                if attendre_mesure and not enregistrement_actif:
                    if etat == "M":
                        enregistrement_actif = True
                        stats["pression_initiale"] = trame.get("P", 0)
                        print("✅ État MESURE détecté — enregistrement démarré")
                    else:
                        # Afficher l'état actuel
                        etat_nom = ETATS.get(etat, etat)
                        print(f"\r   État : {etat_nom}  "
                              f"P={trame.get('P', 0):.2f} mbar  "
                              f"T={trame.get('T', 0):.1f} °C", end="")
                        continue

                # Première ligne → écrire l'en-tête
                if premiere_ligne:
                    ecrire_entete(
                        f,
                        type_essai=type_essai,
                        operateur=operateur,
                        duree_s=duree_max,
                        notes=notes,
                        pression_initiale=stats["pression_initiale"],
                    )
                    premiere_ligne = False

                # Convertir et écrire
                ligne_csv = json_vers_csv(trame)
                f.write(ligne_csv + "\n")
                stats["lignes"] += 1

                # Flush périodique (toutes les 100 lignes = 1 s)
                if stats["lignes"] % 100 == 0:
                    f.flush()

                # Affichage temps réel
                t_s = trame.get("t", 0) / 1000
                psd = trame.get("psd", 0)
                if stats["lignes"] % 10 == 0:
                    print(f"\r   📊 {stats['lignes']:>8d} lignes  "
                          f"t={t_s:>7.1f}s  "
                          f"θ={psd:>8.2f} µrad  "
                          f"P={trame.get('P', 0):.2f} mbar  "
                          f"Pr={trame.get('Pr', 0):.1f} mW", end="")

                # Vérifier la durée maximale
                if duree_max > 0 and t_s >= duree_max:
                    print(f"\n⏱️  Durée maximale atteinte ({duree_max:.0f} s)")
                    break

        except KeyboardInterrupt:
            print("\n\n⛔ Acquisition interrompue par l'opérateur")

    ser.close()
    stats["fin"] = time.time()

    return stats


# ═══════════════════════════════════════════════════════════════════════
# Acquisition MQTT
# ═══════════════════════════════════════════════════════════════════════

def acquisition_mqtt(
    broker: str,
    fichier_csv: Path,
    type_essai: str,
    operateur: str = "",
    duree_max: float = 0,
    notes: str = "",
    port_mqtt: int = 1883,
) -> dict:
    """Acquisition des données via MQTT (Wi-Fi).

    S'abonne au topic bohemian/capteurs et enregistre en CSV.

    Args:
        broker: Adresse du broker MQTT.
        fichier_csv: Chemin du fichier CSV de sortie.
        type_essai: Type d'essai.
        operateur: Nom de l'opérateur.
        duree_max: Durée maximale (s), 0 = infini.
        notes: Notes libres.
        port_mqtt: Port du broker MQTT.

    Returns:
        Statistiques de l'acquisition.
    """
    try:
        import paho.mqtt.client as paho_mqtt
    except ImportError:
        print("❌ Module 'paho-mqtt' requis : pip install paho-mqtt")
        sys.exit(1)

    stats = {
        "lignes": 0,
        "erreurs_json": 0,
        "debut": time.time(),
        "fin": 0,
        "pression_initiale": 0.0,
    }

    fichier_csv.parent.mkdir(parents=True, exist_ok=True)
    f = open(fichier_csv, "w", encoding="utf-8")
    premiere_ligne = True

    def on_message(client, userdata, msg):
        nonlocal premiere_ligne

        try:
            trame = json.loads(msg.payload.decode("utf-8"))
        except json.JSONDecodeError:
            stats["erreurs_json"] += 1
            return

        if premiere_ligne:
            ecrire_entete(
                f,
                type_essai=type_essai,
                operateur=operateur,
                duree_s=duree_max,
                notes=notes,
            )
            premiere_ligne = False

        ligne_csv = json_vers_csv(trame)
        f.write(ligne_csv + "\n")
        stats["lignes"] += 1

        if stats["lignes"] % 100 == 0:
            f.flush()

        if stats["lignes"] % 10 == 0:
            t_s = trame.get("t", 0) / 1000
            print(f"\r   📊 {stats['lignes']:>8d} lignes  "
                  f"t={t_s:>7.1f}s  "
                  f"θ={trame.get('psd', 0):>8.2f} µrad", end="")

    print(f"📡 Connexion MQTT → {broker}:{port_mqtt}")
    client = paho_mqtt.Client(client_id="bohemian-acquisition")
    client.on_message = on_message
    client.connect(broker, port_mqtt)
    client.subscribe("bohemian/capteurs")

    print("⏳ En attente de trames MQTT...")
    print("   Ctrl+C pour arrêter\n")

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n\n⛔ Acquisition interrompue par l'opérateur")

    client.disconnect()
    f.close()
    stats["fin"] = time.time()

    return stats


# ═══════════════════════════════════════════════════════════════════════
# Point d'entrée
# ═══════════════════════════════════════════════════════════════════════

def main() -> None:
    """Point d'entrée principal — parsing des arguments et lancement."""
    parser = argparse.ArgumentParser(
        description="Acquisition des données du pendule — Bohemian Lab",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples :
  python 010_acquisition.py --port /dev/ttyUSB0 --type test_principal
  python 010_acquisition.py --mqtt --broker 192.168.1.100 --type calibration
  python 010_acquisition.py --port COM3 --type reference_vide --duree 600
        """,
    )

    # Mode de connexion
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--port", type=str,
                       help="Port série (ex: /dev/ttyUSB0, COM3)")
    group.add_argument("--mqtt", action="store_true",
                       help="Mode MQTT (Wi-Fi)")

    # MQTT
    parser.add_argument("--broker", type=str, default="192.168.1.100",
                        help="Adresse du broker MQTT (défaut: 192.168.1.100)")

    # Type d'essai
    parser.add_argument("--type", type=str, required=True,
                        choices=TYPES_ESSAI,
                        help="Type d'essai")

    # Options
    parser.add_argument("--operateur", type=str, default="",
                        help="Nom de l'opérateur")
    parser.add_argument("--duree", type=float, default=0,
                        help="Durée maximale en secondes (0 = infini)")
    parser.add_argument("--notes", type=str, default="",
                        help="Notes libres sur la session")
    parser.add_argument("--baudrate", type=int, default=115200,
                        help="Vitesse du port série (défaut: 115200)")
    parser.add_argument("--no-wait", action="store_true",
                        help="Ne pas attendre l'état MESURE pour enregistrer")

    args = parser.parse_args()

    # Générer le nom du fichier
    fichier_csv = generer_nom_fichier(args.type)

    print("╔════════════════════════════════════════════════════════════╗")
    print("║  Bohemian Lab — Acquisition des données empiriques       ║")
    print("╚════════════════════════════════════════════════════════════╝\n")
    print(f"  Type d'essai : {args.type}")
    print(f"  Fichier      : {fichier_csv.relative_to(fichier_csv.parent.parent.parent)}")
    print(f"  Durée max    : {'∞' if args.duree == 0 else f'{args.duree:.0f} s'}")
    print()

    # Lancer l'acquisition
    if args.port:
        stats = acquisition_serie(
            port=args.port,
            fichier_csv=fichier_csv,
            type_essai=args.type,
            operateur=args.operateur,
            duree_max=args.duree,
            notes=args.notes,
            baudrate=args.baudrate,
            attendre_mesure=not args.no_wait,
        )
    else:
        stats = acquisition_mqtt(
            broker=args.broker,
            fichier_csv=fichier_csv,
            type_essai=args.type,
            operateur=args.operateur,
            duree_max=args.duree,
            notes=args.notes,
        )

    # Résumé
    duree = stats["fin"] - stats["debut"]
    taille = fichier_csv.stat().st_size if fichier_csv.exists() else 0

    print("\n" + "═" * 60)
    print("  RÉSUMÉ — Acquisition 010")
    print("═" * 60)
    print(f"""
  Fichier         : {fichier_csv.name}
  Lignes          : {stats['lignes']:,d}
  Durée           : {duree:.1f} s
  Taille          : {taille / 1024:.1f} Ko
  Erreurs JSON    : {stats['erreurs_json']}
  Fréquence moy.  : {stats['lignes'] / max(duree, 1):.1f} Hz
""")

    if stats["lignes"] > 0:
        print(f"  ✅ Données enregistrées → {fichier_csv}")
        print(f"     Prochaine étape : python experiments/011_analyse_empirique.py {fichier_csv}")
    else:
        print("  ⚠️  Aucune donnée enregistrée !")

    print()


if __name__ == "__main__":
    main()
