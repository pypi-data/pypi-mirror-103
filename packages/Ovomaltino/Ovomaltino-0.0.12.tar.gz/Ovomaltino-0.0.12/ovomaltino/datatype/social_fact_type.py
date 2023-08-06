from typing import TypedDict, List
from ovomaltino.datatype.social_fact_moral_type import MoralType


class SocialFactType(TypedDict):

    _id: str
    name: str
    moral: List[MoralType]
    sanction_level: int
