from ovomaltino.datatype.agent_type import AgentType


class Group():

    def __init__(self, leader: AgentType, learner: AgentType):
        self.leader = leader
        self.learner = learner
