from typing import List
from ovomaltino.datatype.social_fact_type import SocialFactType
from ovomaltino.datatype.agent_type import AgentType


def to_social_fact(obj: dict) -> SocialFactType:

    filters: List[str] = ['createdAt', 'updatedAt', '__v']
    return {k: v for k, v in obj.items() if k not in filters}


def to_agent(obj: dict) -> AgentType:

    filters: List[str] = ['createdAt', 'updatedAt', '__v']
    return {k: v for k, v in obj.items() if k not in filters}
