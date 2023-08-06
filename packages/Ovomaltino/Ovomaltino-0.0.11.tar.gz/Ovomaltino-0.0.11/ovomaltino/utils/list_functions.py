import typing as tp


def inputs_outputs(checklist: tp.List) -> tp.Tuple[tp.List, tp.List]:

    inputs = list(dict.fromkeys(checklist))
    outputs = list(len(list(filter(
        lambda y: y == x,
        checklist
    ))) for x in inputs)

    return [inputs, outputs]
