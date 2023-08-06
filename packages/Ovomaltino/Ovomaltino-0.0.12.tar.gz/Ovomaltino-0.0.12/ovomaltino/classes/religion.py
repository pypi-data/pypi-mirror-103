import random as r
import typing as tp
import operator as op
from ovomaltino.classes.social_fact import SocialFact
from ovomaltino.utils.list_functions import inputs_outputs
from ovomaltino.utils.influence_type import Influence


class Religion(SocialFact):

    def shape(self, input_value: tp.Any, output_value: tp.Any) -> tp.NoReturn:

        [inputs, outputs] = inputs_outputs(output_value)

        for out in iter(outputs):
            if out > 1:
                new_moral = {'inputValue': input_value,
                             'outputValue': inputs[outputs.index(out)]}

                self.data['moral'] = op.add(self.data['moral'], [new_moral])

    def influence(self, input_value: tp.Any) -> tp.Union[Influence, None]:

        filter_list = list(x['outputValue'] for x in filter(
            lambda x: x if x['inputValue'] == input_value else False,
            self.data['moral']
        ))

        if len(filter_list) > 0:
            [inputs, outputs] = inputs_outputs(filter_list)
            max_value = max(outputs)
            action = list(set(list(filter(
                lambda x: outputs[inputs.index(x)] == max_value,
                filter_list
            ))))

            ret = action[0] if len(action) == 1 else action[r.choice(
                range(0, len(action) - 1)
            )]

            suggestion = ret
            coersion = max_value / len(filter_list)
            return (suggestion, coersion)
        else:
            return None
