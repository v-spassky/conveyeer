
"""
This module instantiates standart enumeration of electrical items denotations.
"""


GOST2710_ELECTRICAL_ITEMS_DENOTATIONS = {
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'L', 'M', 'P', 'Q', 'R',
    'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AF', 'AK',
    'AKB', 'AKS', 'AKV', 'AKZ', 'AR', 'AV', 'AW', 'BA', 'BB', 'BD', 'BE',
    'BF', 'BC', 'BK', 'BL', 'BM', 'BP', 'BQ', 'BR', 'BS', 'BV', 'BT',
    'BVA', 'BW', 'CB', 'CG', 'DA', 'DD', 'DS', 'DT', 'EK', 'EL', 'ET',
    'FA', 'FP', 'FU', 'FV', 'GB', 'GC', 'GE', 'GEA', 'HA', 'HG', 'HL',
    'HLA', 'HLG', 'HLR', 'HLW', 'HY', 'KA', 'KH', 'KK', 'KM', 'KT', 'KV',
    'KA0', 'KAT', 'KAW', 'KAZ', 'KB', 'KBS', 'KCC', 'KCT', 'KF', 'KHA',
    'KLP', 'KQ', 'KQC', 'KQT', 'KQQ', 'KQS', 'KS', 'KSG', 'KSH', 'KSS',
    'KSV', 'KZ', 'KVZ', 'KW', 'LL', 'LG', 'LR', 'PF', 'PI', 'PK', 'PR',
    'PS', 'PT', 'PV', 'PW', 'PA', 'PC', 'PG', 'PHE', 'PVA', 'QF', 'QK',
    'QS', 'QN', 'QR', 'QW', 'RK', 'RP', 'RS', 'RU', 'RR', 'SA', 'SB',
    'SF', 'SAB', 'SAC', 'SC', 'SN', 'SS', 'SQ', 'SQA', 'SQC', 'SQK',
    'SQM', 'SQT', 'SQY', 'SX', 'SL', 'SP', 'SQ', 'SR', 'SK', 'TA', 'TS',
    'TV', 'TAN', 'TL', 'TLV', 'TS', 'TUV', 'TAV', 'UB', 'UR', 'UI', 'UZ',
    'UA', 'UF', 'UV', 'VD', 'VL', 'VT', 'VS', 'WE', 'WK', 'WS', 'WT',
    'WU', 'WA', 'XA', 'XP', 'XS', 'XT', 'XW', 'XB', 'XG', 'XN', 'YA',
    'YB', 'YC', 'YH', 'YAB', 'YAC', 'YAT', 'YMC', 'ZL', 'ZQ', 'ZA', 'ZF',
    'ZV',
}


def gost2710_denotations() -> set:
    """
    Returns the full list of electrical items denotations 
    listed in ГОСТ 2.710 standart.
    """

    return GOST2710_ELECTRICAL_ITEMS_DENOTATIONS


def gost2710_denotations_except(excluded_denotations: set) -> set:
    """
    Returns the full list of electrical items denotations 
    listed in ГОСТ 2.710 standart except the denotations given as argument.
    """

    return GOST2710_ELECTRICAL_ITEMS_DENOTATIONS - excluded_denotations


def gost2710_denotations_with_added(added_denotations: set) -> set:
    """
    Returns the full list of electrical items denotations 
    listed in ГОСТ 2.710 standart with added custom 
    denotations given as argument.
    """

    return GOST2710_ELECTRICAL_ITEMS_DENOTATIONS | added_denotations
