#!/usr/bin/python3
"""
Parseur de logs HTTP - lit stdin, accumule tailles et codes de statut.
Affiche les stats toutes les 10 lignes et à l'interruption clavier.
"""
import sys
import re


def print_stats(total_size, status_codes):
    """
    Affiche les métriques accumulées.
    Args:
        total_size (int): Taille totale des fichiers
        status_codes (dict): Codes HTTP et leurs occurrences
    """
    print("File size: {}".format(total_size))

    # Codes triés, on n'affiche que ceux > 0
    for code in sorted(status_codes.keys()):
        if status_codes[code] > 0:
            print("{}: {}".format(code, status_codes[code]))


def main():
    """
    Lit les logs depuis stdin et affiche les stats
    toutes les 10 lignes ou sur interruption clavier.
    """
    total_size = 0
    line_count = 0

    # Regex correspondant au format attendu
    pattern = re.compile(
        r'^\d+\.\d+\.\d+\.\d+ - \[.+\] "GET /projects/260 HTTP/1\.1" \d+ \d+$'
    )

    # Codes HTTP attendus
    status_codes = {
        200: 0, 301: 0, 400: 0, 401: 0,
        403: 0, 404: 0, 405: 0, 500: 0
    }

    try:
        for line in sys.stdin:
            line = line.strip()

            # Ligne ignorée si le format ne correspond pas
            if not pattern.match(line):
                continue

            line_count += 1

            try:
                # Avant-dernier = code, dernier = taille
                parts = line.split()
                status = int(parts[-2])
                file_size = int(parts[-1])

                total_size += file_size

                if status in status_codes:
                    status_codes[status] += 1

            except (ValueError, IndexError):
                continue

            if line_count % 10 == 0:
                print_stats(total_size, status_codes)

    except KeyboardInterrupt:
        # Ctrl+C : affichage des stats finales
        print_stats(total_size, status_codes)


if __name__ == "__main__":
    main()
