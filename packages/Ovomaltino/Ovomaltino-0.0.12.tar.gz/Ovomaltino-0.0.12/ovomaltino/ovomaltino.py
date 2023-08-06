import typing as tp
import random as r
from datetime import datetime
from requests import request, Response
from ovomaltino.classes.education import Education
from ovomaltino.classes.religion import Religion
from ovomaltino.classes.family import Family
from ovomaltino.classes.agent import Agent
from ovomaltino.classes.collective_conscience import CollectiveConscience
from ovomaltino.database.database import Database
from ovomaltino.datatype.response_type import ResponseType
from ovomaltino.datatype.agent_type import AgentType
from ovomaltino.handler.ovomaltino_handler import load_social_facts, load_groups, save
from ovomaltino.handler.group_handler import calculate_action
from ovomaltino.handler.mappers import to_agent
from ovomaltino.utils.list_functions import inputs_outputs


class Ovomaltino():

    def __init__(self, api_url: str, api_port: str, api_version: str) -> tp.NoReturn:
        self.api = api_url
        self.port = api_port
        self.version = api_version
        self.url = f'{api_url}:{api_port}/api/{api_version}/'
        self.databases = {'agents': Database(self.url, 'agents'),
                          'consciences': Database(self.url, 'consciences'),
                          'families': Database(self.url, 'families'),
                          'educations': Database(self.url, 'educations'),
                          'religions': Database(self.url, 'religions')}
        self.conscience = CollectiveConscience('conscience', 3)
        self.family = Family('family', 1)
        self.education = Education('education', 1)
        self.religion = Religion('religion', 1)
        self.groups = []
        self.loadedAt = False

    def load(self, num_groups: int, interactions: tp.Any, responses: tp.List[ResponseType]) -> tp.NoReturn:

        if self.isconnected():
            load_social_facts(self)
            self.groups = load_groups(self, num_groups)
            self.loadedAt = datetime.now().ctime()
            self.num_groups = num_groups
            self.interactions = interactions
            self.responses = responses
        else:
            return "Can't connect in API"

    def reload(self) -> tp.NoReturn:

        if self.loadedAt != False:
            return self.load(self.num_groups, self.interactions, self.responses)
        else:
            return "Ovomaltino wasn't loaded yet"

    def get_leaders(self) -> tp.List[Agent]:

        return list(map(lambda group: group.leader, self.groups))

    def get_learners(self) -> tp.List[Agent]:

        return list(map(lambda group: group.leader, self.groups))

    def get_agent(self, agent_id) -> Agent:

        return Agent(to_agent(self.databases['agents'].get({'_id': agent_id}).json()[0]))

    def process(self, input_value: tp.Any) -> tp.NoReturn:

        backup = self

        def rollback():
            return backup

        education_influence = self.education.influence(input_value)
        religion_influence = self.religion.influence(input_value)
        family_influence = self.family.influence(input_value)
        conscience_influence = self.conscience.influence(input_value)
        actions_suggestion = calculate_action(
            self, input_value, conscience_influence,
            education_influence, family_influence, religion_influence
        )

        [inputs, outputs] = inputs_outputs(actions_suggestion)
        max_value = max(outputs)
        action = list(set(list(filter(
            lambda x: outputs[inputs.index(x)] == max_value,
            actions_suggestion
        ))))

        ret = action[0] if len(action) == 1 else action[r.choice(
            range(0, len(action) - 1)
        )]

        return {'response': ret,
                'save': lambda: save(self),
                'rollback': rollback}

    def observe(self, input_value: tp.Any, output_value: tp.Any,
                old_value: tp.Any, new_value: tp.Any) -> tp.NoReturn:

        self.education.shape(input_value, output_value, old_value, new_value)
        self.databases['educations'].update(
            self.education.data['_id'],
            self.education.data
        )

    def consequence(self, value: tp.Any) -> tp.Callable[[], tp.NoReturn]:

        def apply(agent: AgentType):
            agent.data['life'] += self.responses[value]['consequence']

        list(map(apply, list(x.leader for x in self.groups)))
        return {'save': lambda: save(self)}

    def isconnected(self) -> bool:

        try:
            res: Response = request('GET', self.url)
            return res.status_code == 200
        except:
            return False

    def isloaded(self) -> bool:
        return self.loadedAt != False
