from pydantic import BaseModel, Field
from typing import Literal, TypedDict

# ------------------------- User memory -------------------------

class Fivetuple(BaseModel):
    subject: str
    predicate: str
    object: str
    context: str
    type:  Literal["preference", "fact"]

class Emotion(BaseModel):
    emotion: str
    trigger: str
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
    memory: list[Fivetuple | list] = []
    emotion: Emotion | dict


# ------------------------- Graph state -------------------------

class EmotionalState(BaseModel):
    emotion: str
    mood: str
    topic: str
    trend: str 
    engagement_level: float = Field(ge=0.0, le=1.0)

class Message(TypedDict):
    role: Literal['system', 'user', 'assistant', 'tool']
    content: str


class WorkingState(BaseModel):
    memory: list[Fivetuple | list] = []
    messages: list[Message] = []
    query: str = ""
    emotion: list[Emotion | dict] = []
    personality_analysis: list[PersonalityAnalyzer | dict] = []
   

# ------------------------- Personality schema -------------------------

class EmotionalTone(BaseModel):
    warmth: float = Field(ge=0.0, le=1.0)
    calmness: float = Field(ge=0.0, le=1.0)
    playfulness: float = Field(ge=0.0, le=1.0)

class Expressiveness(BaseModel):
    empathy_intensity: float = Field(ge=0.0, le=1.0)
    emotional_mirroring: float = Field(ge=0.0, le=1.0)

class Interaction_style(BaseModel):
    engagement_level: float = Field(ge=0.0, le=1.0)
    encouragement_level: float = Field(ge=0.0, le=1.0)
    question_frequency: float = Field(ge=0.0, le=1.0)
    response_length: float = Field(ge=0.0, le=1.0)
    response_pace: float = Field(ge=0.0, le=1.0)

class Personality(BaseModel):
    emotional_tone: EmotionalTone
    expressiveness: Expressiveness
    interaction_style: Interaction_style


# ------------------------- Personality analyzer schema -------------------------

class PersonalityAnalyzer(BaseModel):
    emotional_state: EmotionalState | dict
    personality: Personality | dict
    selected_personality: str
