from enum import IntEnum


class RarityEnum(IntEnum):
    """Mapping of items quality to their IDs"""
    poor = 0
    common = 1
    uncommon = 2
    rare = 3
    epic = 4
    legendary = 5
    artifact = 6
    heirloom = 7


class SlotEnum(IntEnum):
    """Mapping of item slots to their IDs as for wotlk.ezhead.org DB"""
    head = 1
    neck = 2
    shoulder = 3
    body = 4
    chest = 5
    waist = 6
    legs = 7
    feet = 8
    wrist = 9
    hands = 10
    fingers = 11
    trinkets = 12
    weapon = 13
    shield = 14
    gun = 15
    cloaks = 16
    two_handed = 17
    tabard = 19
    main_hand = 21
    off_hand = 22
    ammunition = 24
    relics = 28
