from .enums import RarityEnum, SlotEnum

# Resulting GS of item of certain type is multiplied by the corresponding coefficient below
SLOT_COEFFICIENTS = {
    SlotEnum.head: 1,
    SlotEnum.neck: 0.5625,
    SlotEnum.shoulder: 0.75,
    SlotEnum.body: 0,
    SlotEnum.chest: 1,
    SlotEnum.waist: 0.75,
    SlotEnum.legs: 1,
    SlotEnum.feet: 0.75,
    SlotEnum.wrist: 0.5625,
    SlotEnum.hands: 0.75,
    SlotEnum.fingers: 0.5625,
    SlotEnum.trinkets: 0.5625,
    SlotEnum.weapon: 1,
    SlotEnum.shield: 1,
    SlotEnum.gun: 0.3164,
    SlotEnum.cloaks: 0.5625,
    SlotEnum.two_handed: 2,
    SlotEnum.tabard: 0,
    SlotEnum.main_hand: 1,
    SlotEnum.off_hand: 1,
    SlotEnum.ammunition: 0,
    SlotEnum.relics: 0.3164
}

# The data struct is used in GS calculation. See gear_score.models.Item._count_gs
GS_COEFFICIENTS = {
    'HIGH_LEVEL': {
        RarityEnum.epic: {'subtrahend': 91.45, 'divisor': 0.65},
        RarityEnum.rare: {'subtrahend': 81.375, 'divisor': 0.8125},
        RarityEnum.uncommon: {'subtrahend': 73, 'divisor': 1}
    },
    'LOW_LEVEL': {
        RarityEnum.epic: {'subtrahend': 26, 'divisor': 1.2},
        RarityEnum.rare: {'subtrahend': 0.75, 'divisor': 1.8},
        RarityEnum.uncommon: {'subtrahend': 8, 'divisor': 2},
        RarityEnum.common: {'subtrahend': 0, 'divisor': 2.25}
    }
}
