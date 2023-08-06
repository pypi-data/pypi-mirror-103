import typing as tp
from abc import ABC, abstractmethod
from ovomaltino.database.database import Database
from ovomaltino.datatype.social_fact_type import SocialFactType
from ovomaltino.datatype.agent_type import AgentType
from ovomaltino.handler.mappers import to_social_fact
from ovomaltino.utils.influence_type import Influence


class SocialFact(ABC):

    def __init__(self, name: str, sanction_level: int) -> bool:
        self.name = name
        self.sanction_level = sanction_level
        self.data = False

    def iscreated(self, db: Database) -> bool:

        try:
            res = db.get(sort='createdAt:desc', offset=0, limit=1).json()
            return len(res) == 1
        except:
            return False

    def register(self, db: Database, obj: SocialFactType) -> bool:

        try:
            self.data = to_social_fact(db.create(obj).json())
            return True
        except:
            return False

    def sanction(self, agents: tp.List[AgentType], input_value: tp.Any,
                 influence: Influence, actions: tp.List[tp.Any]) -> tp.NoReturn:

        def apply(agent: AgentType, action: tp.Any) -> tp.NoReturn:

            if influence[0] == action:
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
                    lambda x: x['action'] == influence[0] and x['input_value'] == input_value,
                    agent.data['sanctions']
                ))

                if len(check_sanction) > 0:
                    for sanction in iter(agent.data['sanctions']):
                        if sanction['action'] == influence[0] and sanction['input_value'] == input_value and sanction['level'] > 0:
                            sanction['level'] += self.sanction_level
                else:
                    agent.data['sanctions'] = agent.data['sanctions'] + [{
                        'input_value': input_value,
                        'action': influence[0],
                        'level': self.sanction_level
                    }]

        if influence is not None:
            list(map(apply, agents, actions))
        else:
            pass

    @abstractmethod
    def shape(self, input_value: tp.Any, output_value: tp.Any) -> tp.NoReturn:
        pass

    @abstractmethod
    def influence(self, input_value: tp.Any):
        pass
