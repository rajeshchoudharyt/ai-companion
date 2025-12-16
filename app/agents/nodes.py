# import requests
from app.agents.schemas import UserMemory
from utils.tools import llm
from app.agents.agent import WorkingState

# basic input message normalizer
def input_normalizer(state: WorkingState):
    return { "query": "".join(state.query.strip())}


def memory_extractor(state: WorkingState):
    structured_llm = llm.with_structured_output(UserMemory)
    structured_llm.invoke(
        f'''
        Follow below steps to extract user memories:

        Step 1: 
        - Extract user preferences and facts from the below user messages.
        - Consider existing memories while extracting new memory.
        - Extract memories only from the most recent user messages.
        - If no new memory is found, return an empty list.
            Example: {{ memory: [] }}
        - Extract memories in the form of subject, predicate, object, context and type(preferences or facts) in the below format.
        - Extract only memories worth remembering or can be stored for long term.

        Step 2:
        - Analyse the user emotion only for the last user message.
        - Consider the context of the conversation to determine the emotion.
        - Identify the point of trigger for the emotion if aplicable.
        - Describe the emotion in the below dimensions with values between 0.0 to 1.0.
        - If no specific emotion is detected, return an empty dictionary.
            Example: {{ emotion: {{}} }}

        Output Format:
        {{
            memory: [
                {{
                    subject: str,
                    predicate: str,
                    object: str,
                    context: str,
                    type: "preferences" | "facts"
                }}
            ],
            emotion: {{
                emotion: str,
                trigger: str | "",
                valence: Pleasantness of the emotional tone,
                arousal: Intensity of the emotion,
                dominance: Perceived control over the emotion,
                confidence: Level of certainty in belief,
                warmth: Affection, friendliness and care,
                trust: Expectation of safety or openness from others,
                empathy: Recognition of another's emotional state,
                engagement: Willingness to continue interaction,
                playfulness: Non-serious, light-heartedness, exploratory tone
            }} 
        }}

        Existing Memories:
        {state.memory}

        User Messages:
        {state.messages}

        '''
    )