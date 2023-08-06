from typing import TypedDict, Optional, List
from ovomaltino.datatype.agent_memory_type import Memory
from ovomaltino.datatype.sanction_type import Sanctions


class AgentType(TypedDict):

    _id: str
    birth: str
    progenitor: str
    leader: bool
    becomeLeader: Optional[str]
    death: Optional[str]
    life: float
    memory: List[Memory]
    sanctions: List[Sanctions]
    actions: int
