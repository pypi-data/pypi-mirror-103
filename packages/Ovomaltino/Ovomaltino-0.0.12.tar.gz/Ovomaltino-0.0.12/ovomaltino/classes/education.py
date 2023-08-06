import random as r
import typing as tp
import operator as op
from ovomaltino.classes.social_fact import SocialFact
from ovomaltino.utils.list_functions import inputs_outputs
from ovomaltino.utils.influence_type import Influence


class Education(SocialFact):

    def shape(self, input_value: tp.Any, output_value: tp.Any,
              old_value: tp.Any, new_value: tp.Any) -> tp.NoReturn:

        def change(test_value: tp.Any):

            if test_value == old_value:
                return new_value
            elif test_value == new_value:
                return old_value
            else:
                return test_value

        new_input_value = list(map(change, input_value))
        new_moral = {'inputValue': new_input_value,
                     'outputValue': output_value}

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
