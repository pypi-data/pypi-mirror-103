import random as r
import operator as op
import typing as tp
from ovomaltino.classes.groups import Group
from ovomaltino.classes.agent import Agent
from ovomaltino.classes.social_fact import SocialFact
from ovomaltino.database.database import Database
from ovomaltino.handler.mappers import to_social_fact, to_agent
from ovomaltino.handler.group_handler import create_new_group, fill_group
from ovomaltino.handler.agent_handler import check_agent


def load_social_facts(ovomaltino) -> tp.NoReturn:

    def check_social_facts(sf: tp.Tuple[int, SocialFact], dbs: tp.List[Database]) -> tp.Union[SocialFact, tp.Callable]:

        if sf[1].data == False:

            res = dbs[sf[0]].get(offset=0, limit=1).json()

            if len(res) == 1:
                sf[1].data = to_social_fact(res[0])
            else:
                sf[1].register(dbs[sf[0]], {
                    'name': sf[1].name,
                    'moral': [],
                    'sanction_level': sf[1].sanction_level
                })

        else:
            pass

    dbs = [ovomaltino.databases['families'], ovomaltino.databases['educations'],
           ovomaltino.databases['religions'], ovomaltino.databases['consciences']]

    [check_social_facts(sf, dbs)
     for sf in enumerate([ovomaltino.family, ovomaltino.education, ovomaltino.religion, ovomaltino.conscience])]


def load_groups(ovomaltino, num_groups: int) -> tp.NoReturn:

    try:
        res = ovomaltino.databases['agents'].get(
            filters={'leader': True}, offset=0, limit=num_groups
        ).json()

        if len(res) == num_groups:
            valid_agents = [check_agent(ovomaltino, Agent(to_agent(x)))
                            for x in res]
            return [fill_group(ovomaltino, agent) for agent in valid_agents]
        else:
            valid_agents = [check_agent(ovomaltino, Agent(to_agent(x)))
                            for x in res]

            partial_groups = [fill_group(ovomaltino, agent)
                              for agent in valid_agents]

            new_groups = [create_new_group(ovomaltino)
                          for x in range(0, num_groups - len(res))]

            return op.add(partial_groups, new_groups)

    except:
        raise SystemError


def save(ovomaltino) -> tp.NoReturn:

    ovomaltino.databases['consciences'].update(
        ovomaltino.conscience.data['_id'],
        ovomaltino.conscience.data
    )

    ovomaltino.databases['families'].update(
        ovomaltino.family.data['_id'],
        ovomaltino.family.data
    )

    ovomaltino.databases['educations'].update(
        ovomaltino.education.data['_id'],
        ovomaltino.education.data
    )

    ovomaltino.databases['religions'].update(
        ovomaltino.religion.data['_id'],
        ovomaltino.religion.data
    )

    list(map(lambda x: ovomaltino.databases['agents'].update(x.data['_id'], x.data), list(
        x.leader for x in ovomaltino.groups
    )))

    list(map(lambda x: ovomaltino.databases['agents'].update(x.data['_id'], x.data), list(
        x.learner for x in ovomaltino.groups
    )))
