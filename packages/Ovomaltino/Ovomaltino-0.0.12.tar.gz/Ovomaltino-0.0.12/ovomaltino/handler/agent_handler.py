import random as r
import typing as tp
from datetime import datetime
from ovomaltino.datatype.agent_type import AgentType
from ovomaltino.handler.mappers import to_agent
from ovomaltino.utils.list_functions import inputs_outputs


def create_new_leader(ovomaltino) -> AgentType:

    return to_agent(ovomaltino.databases['agents'].create({
        'birth': datetime.now().ctime(),
        'progenitor': "I'm the first one, guy",
        'leader': True,
        'becomeLeader': datetime.now().ctime(),
        'life': 100,
        'memory': [],
        'sanctions': [],
        'actions': 0
    }).json())


def create_new_learner(ovomaltino, leader_id: str) -> AgentType:

    return to_agent(ovomaltino.databases['agents'].create({
        'birth': datetime.now().ctime(),
        'progenitor': leader_id,
        'leader': False,
        'life': 100,
        'memory': [],
        'sanctions': [],
        'actions': 0
    }).json())


def upgrade_agent(ovomaltino, learner: AgentType) -> AgentType:

    new_leader_values = {
        'leader': True,
        'becomeLeader': datetime.now().ctime()
    }

    new_leader = learner.data | new_leader_values
    ovomaltino.databases['agents'].update(
        new_leader['_id'], new_leader
    ).json()

    create_new_learner(ovomaltino, new_leader['_id'])
    return new_leader


def check_agent(ovomaltino, agent: AgentType) -> tp.Union[AgentType, tp.Callable]:

    if agent.data['life'] > 0:
        return agent
    else:
        death_values = {'death': datetime.now().ctime(), 'leader': False}
        agent.data = agent.data | death_values
        ovomaltino.databases['agents'].update(
            agent.data['_id'], agent.data
        ).json()

        return upgrade_agent(ovomaltino, to_agent(
            ovomaltino.databases['agents'].get(
                filters={'progenitor': agent.data['_id']}
            ).json()[0]
        ))


def get_sanction_level(agent: AgentType, input_value: tp.Any, action: tp.Any,
                       influence: tp.Tuple[tp.Any, float]) -> tp.Tuple[int, float, tp.Any, float]:

    sanction = list(filter(
        lambda x: x if x['action'] == action and x['input_value'] == input_value else False,
        agent.data['sanctions']
    ))

    if len(sanction) > 0 and sanction[0]['level'] > 0:
        sanction_level = abs(sanction[0]['level'] / sum([
            x['level'] for x in agent.data['sanctions']
            if x['input_value'] == input_value
        ]))

        final_influence = sanction_level / influence
        biggest_value = max([sanction_level, influence])
        return [1, final_influence, action, biggest_value]

    else:
        final_influence = influence
        biggest_value = influence
        return [2, final_influence, action, biggest_value]


def get_myself_data(agent: AgentType, input_value: tp.Any, interactions: tp.Any) -> tp.Union[
        tp.Tuple[tp.Any, float],
        None]:

    memories = list(x['action'] for x in filter(
        lambda x: x if x['inputValue'] == input_value else False,
        agent.data['memory']
    ))

    if len(memories) > 0:
        [inputs, outputs] = inputs_outputs(memories)
        max_value = max(outputs)
        action = list(set(list(filter(
            lambda x: outputs[inputs.index(x)] == max_value,
            memories
        ))))

        ret = action[0] if len(action) == 1 else action[r.choice(
            range(0, len(action) - 1)
        )]

        memory_suggestion = ret
        memory_coersion = max_value / len(memories)
        return [memory_suggestion, memory_coersion]

    else:
        return None


def closest(lst: tp.List[tp.Any], K: float) -> tp.List[tp.Any]:

    return lst[min(range(len(lst)), key=lambda i: abs(lst[i]-K))]


def order_influence(indexed_influence: tp.List, field: str, C: int) -> tp.Callable[[tp.List], tp.List]:

    differ_list = list(map(
        lambda x: [x[0], abs(C - x[1][field])],
        indexed_influence
    ))

    return sorted(differ_list, key=lambda x: x[-1])
