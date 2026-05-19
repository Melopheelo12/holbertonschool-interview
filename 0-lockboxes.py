#!/usr/bin/python3
"""
0-lockboxes.py

Détermine si toutes les boîtes peuvent être ouvertes.
"""


def canUnlockAll(boxes):
    """
    Vérifie si toutes les boîtes peuvent être déverrouillées.

    Args:
        boxes (list of lists): chaque boîte contient des clés
        qui ouvrent d'autres boîtes.

    Returns:
        bool: True si toutes les boîtes peuvent être ouvertes,
        sinon False.
    """

    n = len(boxes)

    unlocked = set([0])

    keys = [0]

    while keys:

        current_box = keys.pop()

        for key in boxes[current_box]:

            if key < n and key not in unlocked:

                unlocked.add(key)

                keys.append(key)

    return len(unlocked) == n
