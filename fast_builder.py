from random import choice
from typing import List

from basic_genetic import BasicGenetic, BEST_GENES
from models import Action, Ability, Build, PublicInfo, DistrictType
from player import Player


class FastBuilder(BasicGenetic):
    def __init__(self, genes=None):
        if genes is not None:
            best_genes = genes
        else:
            best_genes = BEST_GENES
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
