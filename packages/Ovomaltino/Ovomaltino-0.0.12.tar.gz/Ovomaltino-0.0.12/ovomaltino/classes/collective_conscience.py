import operator as op
import random as r
import typing as tp
import functools as ftls
from ovomaltino.classes.social_fact import SocialFact
from ovomaltino.datatype.agent_type import AgentType
from ovomaltino.utils.list_functions import inputs_outputs
from ovomaltino.utils.influence_type import Influence


class CollectiveConscience(SocialFact):

    def shape(self, input_value: tp.Any, output_value: tp.Any) -> tp.NoReturn:

        outputs = sorted(list(dict.fromkeys(output_value)))
        new_moral = {'inputValue': input_value,
                     'outputValue': outputs}

        self.data['moral'] = op.add(self.data['moral'], [new_moral])

    def influence(self, input_value: tp.Any) -> tp.Union[Influence, None]:

        filter_list = list(x['outputValue'] for x in filter(
            lambda x: x if x['inputValue'] == input_value else False,
            self.data['moral']
        ))

        if len(filter_list) > 0:
            inputs = list(dict.fromkeys(
                ''.join(map(str, x)) for x in filter_list
            ))

            outputs = list(len(list(filter(
                lambda y: ''.join(map(str, y)) == x,
                filter_list
            ))) for x in inputs)

            max_value = max(outputs)
            action = list(filter(
                lambda x: outputs[
                    inputs.index(''.join(map(str, x)))
                ] == max_value,
                filter_list
            ))

            ret = action[0] if len(action) == 1 else action[r.choice(
                range(0, len(action) - 1)
            )]

            suggestion = ret
            coersion = max_value / len(filter_list)
            return (suggestion, coersion)
        else:
            return None

    def sanction(self, agents: tp.List[AgentType], input_value: tp.Any,
                 influence: Influence, actions: tp.List[tp.Any]) -> tp.NoReturn:

        def apply(agent: AgentType, action: tp.Any) -> tp.NoReturn:

            if action in influence[0]:
                check_sanction = list(filter(
                    lambda x: x['action'] == action and x['input_value'] == input_value,
                    agent.data['sanctions']
                ))

                if len(check_sanction) > 0:
                    for sanction in iter(agent.data['sanctions']):
                        if sanction['action'] == action and sanction['input_value'] == input_value and sanction['level'] > 0 and sanction['level'] - self.sanction_level > 0:
                            sanction['level'] -= self.sanction_level

                        elif sanction['action'] == action and sanction['input_value'] == input_value and sanction['level'] > 0 and sanction['level'] - self.sanction_level < 0:
                            sanction['level'] = 0

                        else:
                            pass

                else:
                    pass

            else:
                check_sanction = list(filter(
                    lambda x: x['action'] in influence[0] and x['input_value'] == input_value,
                    agent.data['sanctions']
                ))

                if len(check_sanction) > 0:
                    for sanction in iter(agent.data['sanctions']):
                        if sanction['action'] in influence[0] and sanction['input_value'] == input_value and sanction['level'] > 0:
                            sanction['level'] += self.sanction_level
                else:
                    for i in influence[0]:
                        agent.data['sanctions'] = agent.data['sanctions'] + [{
                            'input_value': input_value,
                            'action': i,
                            'level': self.sanction_level
                        }]

        if influence is not None:
            list(map(apply, agents, actions))
        else:
            pass
