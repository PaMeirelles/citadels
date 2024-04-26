from random import choice
from typing import List

from basic_genetic import BasicGenetic
from models import Action, Ability, Build, PublicInfo, Resource, DistrictType
from player import Player


def get_best_fast_builder():
    genes = [0.8097353164231837, 0.9491063568344036, 0.379127453165517, 1.0930914698122582, 0.21752728270739707,
             0.572800879043732, 1.3251915624193629, -0.25935536225209604]

    return FastBuilder(genes)


class FastBuilder(BasicGenetic):
    def __init__(self, genes=None):
        if genes is not None:
            best_genes = genes
        else:
            best_genes = [0.9783701214983467, 0.9665306151785001, 0.6122460569228687, 1.0678189251978236,
                          0.3282948123261767,
                          0.599630362630095, 1.1112367557854417, 0.25914538633473455]
        super().__init__(best_genes[0], best_genes[1], best_genes[2], best_genes[3], best_genes[4], best_genes[5],
                         best_genes[6], best_genes[7])

    def choose_action(self, options: List[Action], public_info: PublicInfo, myself: Player) -> Action:
        types = set([x.district_type for x in myself.districts])

        fills = None
        doesnt_fill = None
        for op in options:
            if isinstance(op, Ability):
                return op
            elif isinstance(op, Build):
                if op.district.cost > myself.gold:
                    continue
                if op.district.district_type in types or op.district.district_type == DistrictType.Special:
                    if not doesnt_fill:
                        doesnt_fill = op
                    else:
                        if op.district.cost > doesnt_fill.district.cost:
                            doesnt_fill = op
                else:
                    if not fills:
                        fills = op
                    else:
                        if op.district.cost > fills.district.cost:
                            fills = op

        if fills:
            return fills
        if doesnt_fill:
            return doesnt_fill
        return choice(options)
