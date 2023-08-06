import typing as tp
import itertools as ittls
from ovomaltino.datatype.group_type import GroupType
from ovomaltino.datatype.agent_type import AgentType
from ovomaltino.classes.agent import Agent
from ovomaltino.classes.groups import Group
from ovomaltino.handler.mappers import to_agent
from ovomaltino.agent_handler import create_new_leader, create_new_learner
from ovomaltino.utils.influence_type import Influence


def create_new_group(ovomaltino) -> GroupType:

    leader = Agent(create_new_leader(ovomaltino))
    learner = Agent(create_new_learner(ovomaltino, leader.data['_id']))
    return Group(leader, learner)


def fill_group(ovomaltino, leader: AgentType) -> Group:

    return Group(leader, Agent(to_agent(ovomaltino.databases['agents'].get(filters={'progenitor': leader.data['_id']}).json()[0])))


def calculate_action(ovomaltino, input_value: tp.Any, conscience_influence: Influence,
                     education_influence: Influence, family_influence: Influence,
                     religion_influence: Influence) -> tp.List[tp.Any]:

    actions = [group.leader.act(input_value, ovomaltino.interactions, education_influence, religion_influence,
                                conscience_influence, family_influence)
               for group in ovomaltino.groups]

    list(map(lambda group, act, education, input_value: group.learner.learn(group.leader, act, education, input_value),
             ovomaltino.groups, actions, ittls.repeat(education_influence), ittls.repeat(input_value)))

    list(map(lambda sf, input_value, actions: sf.shape(input_value, actions),
             list([ovomaltino.conscience, ovomaltino.religion, ovomaltino.family]),
             ittls.repeat(input_value),
             ittls.repeat(actions)))

    list(map(lambda sf, agent, input_value, influence_value, action_value: sf.sanction(agent, input_value, influence_value, action_value),
             list([ovomaltino.conscience, ovomaltino.education,
                   ovomaltino.family, ovomaltino.religion]),
             ittls.repeat(list(x.leader for x in ovomaltino.groups)),
             ittls.repeat(input_value),
             list([conscience_influence, education_influence,
                   family_influence, religion_influence]),
             ittls.repeat(actions)))

    return actions
