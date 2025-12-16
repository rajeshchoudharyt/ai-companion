from pydantic import BaseModel, Field
from typing import List, Literal, TypedDict

class Fivetuple(BaseModel):
    subject: str
    predicate: str
    object: str
    context: str
    type:  Literal["preferences", "facts"]

class Emotion(BaseModel):
    emotion: str
    trigger: str = ""
    valence: float = Field(ge=0.0, le=1.0)
    arousal: float = Field(ge=0.0, le=1.0)
    dominance: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    warmth: float = Field(ge=0.0, le=1.0)
    trust: float = Field(ge=0.0, le=1.0)
    empathy: float = Field(ge=0.0, le=1.0)
    engagement: float = Field(ge=0.0, le=1.0)
    playfulness: float = Field(ge=0.0, le=1.0)

class UserMemory(BaseModel):
    memory: List[Fivetuple]
    emotion: Emotion

class Message(TypedDict):
    role: Literal['system', 'user', 'assistant', 'tool']
    content: str
