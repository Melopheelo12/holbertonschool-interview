#!/usr/bin/python3
"""
Parseur de logs HTTP.

Lit les lignes depuis stdin, accumule la taille totale des fichiers
et le nombre d'occurrences de chaque code de statut HTTP.
Affiche les statistiques toutes les 10 lignes valides, et une dernière
fois à l'interruption clavier (Ctrl+C).

Format de ligne attendu :
    <IP> - [<date>] "GET /projects/260 HTTP/1.1" <code> <taille>

Exemple :
    127.0.0.1 - [2024-01-01] "GET /projects/260 HTTP/1.1" 200 1024

Utilisation :
    cat access.log | ./0-stats.py
    python3 -c "import random; ..." | ./0-stats.py
"""
import sys


def print_stats(total_size, status_codes):
    """Affiche les métriques accumulées sur stdout.

    Imprime d'abord la taille totale des fichiers, puis la liste
    des codes HTTP dont le compteur est strictement positif,
    triés par ordre croissant.

    Args:
        total_size (int): Somme des tailles de fichiers lues jusqu'ici.
        status_codes (dict): Dictionnaire {code (int): occurrences (int)}.
            Seuls les codes dont la valeur est > 0 sont affichés.

    Returns:
        None
    """
    print("File size: {}".format(total_size))

    for code in sorted(status_codes.keys()):
        if status_codes[code] > 0:
            print("{}: {}".format(code, status_codes[code]))


def is_valid_line(parts):
    """Vérifie qu'une ligne découpée respecte le format attendu.

    Effectue la validation sans expression régulière, en inspectant
    chaque champ individuellement après un split() sur les espaces.

    Format attendu (9 champs minimum) :
        <IP> - [<date>] "GET /projects/260 HTTP/1.1" <code> <taille>
        [0]  [1]  [2]    [3]       [4]         [5]    [-2]   [-1]

    Champs vérifiés :
        - parts[0]  : adresse IPv4 (4 blocs numériques séparés par des points)
        - parts[1]  : tiret littéral "-"
        - parts[4]  : méthode HTTP entre guillemets : '"GET'
        - parts[5]  : chemin de la ressource : '/projects/260'
        - parts[6]  : version HTTP fermante : 'HTTP/1.1"'
        - parts[-2] : code de statut (doit être convertible en int)
        - parts[-1] : taille du fichier (doit être convertible en int)

    Args:
        parts (list[str]): Liste de chaînes issue du split() de la ligne brute.

    Returns:
        bool: True si la ligne est valide, False sinon.
    """
    if len(parts) < 7:
        return False

    # Validation de l'adresse IP
    ip_blocks = parts[0].split(".")
    if len(ip_blocks) != 4:
        return False
    for block in ip_blocks:
        if not block.isdigit():
            return False

    # Validation des champs fixes
    if parts[1] != "-":
        return False
    if parts[4] != '"GET':
        return False
    if parts[5] != "/projects/260":
        return False
    if parts[6] != 'HTTP/1.1"':
        return False

    # Validation des champs numériques (code + taille)
    try:
        int(parts[-2])
        int(parts[-1])
    except ValueError:
        return False

    return True


def main():
    """Point d'entrée : lit stdin et orchestre l'accumulation des stats.

    Pour chaque ligne lue depuis stdin :
        1. Supprime les espaces en début/fin (strip).
        2. Découpe la ligne en champs (split).
        3. Ignore la ligne si elle ne respecte pas le format (is_valid_line).
        4. Incrémente le compteur de lignes valides.
        5. Ajoute la taille du fichier au total.
        6. Incrémente le compteur du code HTTP si celui-ci est suivi.
        7. Affiche les stats tous les 10 lignes valides.

    En cas d'interruption clavier (Ctrl+C / KeyboardInterrupt),
    affiche les statistiques finales avant de terminer.

    Returns:
        None
    """
    total_size = 0
    line_count = 0

    status_codes = {
        200: 0, 301: 0, 400: 0, 401: 0,
        403: 0, 404: 0, 405: 0, 500: 0
    }

    try:
        for line in sys.stdin:
            line = line.strip()
            parts = line.split()

            if not is_valid_line(parts):
                continue

            line_count += 1

            status = int(parts[-2])
            file_size = int(parts[-1])

            total_size += file_size

            if status in status_codes:
                status_codes[status] += 1

            if line_count % 10 == 0:
                print_stats(total_size, status_codes)

    except KeyboardInterrupt:
        print_stats(total_size, status_codes)


if __name__ == "__main__":
    main()
