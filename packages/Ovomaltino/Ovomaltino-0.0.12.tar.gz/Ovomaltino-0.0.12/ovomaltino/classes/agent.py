import typing as tp
import operator as op
import random as r
from ovomaltino.handler.agent_handler import get_myself_data, get_sanction_level, closest, order_influence
from ovomaltino.datatype.agent_type import AgentType
from ovomaltino.utils.influence_type import Influence


class Agent():

    def __init__(self, data: AgentType):
        self.data = data

    def act(self, input_value: tp.Any, interactions: tp.Any, education: Influence,
            religion: Influence, conscience: Influence, family: Influence) -> tp.Any:

        myself = get_myself_data(self, input_value, interactions)
        filter_conscience = [
            r.choice(conscience[0]),
            conscience[1]
        ] if conscience is not None else None

        intuition = [r.choice(interactions), r.uniform(0, 1)]
        results = [get_sanction_level(self, input_value, x[0], x[1])
                   for x in [myself, intuition, religion, education, family, filter_conscience]
                   if x is not None]

        influences_1 = list(filter(lambda x: x[0] == 1, results))
        influences_2 = list(filter(lambda x: x[0] == 2, results))

        if len(influences_1) > 0:
            indexed_influences = list(enumerate(influences_1))
            sorted_final_influence = order_influence(
                indexed_influences, 1, 1
            )

            sorted_biggest_influence = order_influence(
                indexed_influences, 3, 1
            )

            sum_list = []
            for influence in iter(indexed_influences):
                final_influence_position = list(filter(
                    lambda x: x[0] == influence[0],
                    sorted_final_influence
                ))[0][0]

                biggest_influence_position = list(filter(
                    lambda x: x[0] == influence[0],
                    sorted_biggest_influence
                ))[0][0]

                sum_list = op.add(sum_list, [[influence[0], sum([
                    final_influence_position, biggest_influence_position
                ])]])

            action = [list(filter(
                lambda x: x[0] == sorted(sum_list, key=lambda x: x[-1])[0][0],
                indexed_influences
            ))[0][1]]

            ret = action[0][2] if len(action) == 1 else action[r.choice(
                range(0, len(action) - 1)
            )][2]

        else:
            biggest_influence = max([x[1] for x in influences_2])
            action = list(filter(
                lambda x: x[1] == biggest_influence, influences_2
            ))

            ret = action[0][2] if len(action) == 1 else action[r.choice(
                range(0, len(action) - 1)
            )][2]

        self.data['memory'] = self.data['memory'] + [{
            'isLearner': False,
            'inputValue': input_value,
            'action': ret
        }]

        return ret

    def learn(self, leader, leader_action, education, input_value):

        leader_data = [
            leader_action,
            1 - len(self.data['memory']) / len(leader.data['memory'])
        ]

        if education is None:
            self.data['memory'] = self.data['memory'] + [{
                'isLearner': True,
                'inputValue': input_value,
                'action': leader_action
            }]

        elif leader_data[1] / education[1] == 1:
            self.data['memory'] = self.data['memory'] + [{
                'isLearner': True,
                'inputValue': input_value,
                'action': r.choice([leader_action, education[0]])
            }]

        elif leader_data[1] / education[1] > 1:
            self.data['memory'] = self.data['memory'] + [{
                'isLearner': True,
                'inputValue': input_value,
                'action': leader_action
            }]

        else:
            self.data['memory'] = self.data['memory'] + [{
                'isLearner': True,
                'inputValue': input_value,
                'action': education[0]
            }]
