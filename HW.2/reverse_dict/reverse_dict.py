import typing as tp


def revert(dct: tp.Mapping[str, str]) -> dict[str, list[str]]:
    """
    :param dct: dictionary to revert in format {key: value}
    :return: reverted dictionary {value: [key1, key2, key3]}
    """
    values = {val for val in dct.values()}
    return {val: [key for key, value in dct.items() if value is val] for val in values}
