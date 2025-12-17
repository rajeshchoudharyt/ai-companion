from app.agents.schemas import UserMemory
from app.utils.tools import get_llm
from app.agents.schemas import WorkingState, PersonalityAnalyzer
from app.agents.store import store

# basic input message normalizer
def input_normalizer(state: WorkingState):
    query = "".join(state.query.strip())
    return { 
        "query": query,
        "messages": state.messages + [{"role": "user", "content": query}]
    }


# Memory and emotion extractor
def memory_extractor(state: WorkingState):
    structured_llm = get_llm("default").with_structured_output(UserMemory.model_json_schema())

    prompt = f'''
        Given below the existing user memories and messages,
        extract the user memory from the most recent message and
        identify the user emotion from the last message.

        Follow the below steps to perform the action:

        Step 1: 
        - Extract user preferences and facts from the user messages.
        - Consider existing memories while extracting new memory.
        - Extract memories only from the most recent messages.
        - You can extract more than one memory
        - If no new memory is found, return an empty list.
            Example: {{ memory: [] }}
        - Extract memories in the form of subject, predicate, object, context and type(preferences or facts) in the below format.
        - Extract only memories worth remembering or can be stored for long term.

        Step 2:
        - Analyse the user emotion only for the last user message.
        - Consider the context of the conversation to determine the emotion.
        - Identify the point of trigger for the emotion if applicable.
        - Describe the emotion in the below dimensions with values between 0.0 to 1.0.
        - If no specific emotion is detected, return an empty dictionary.
            Example: {{ emotion: {{}} }}

        Step 3: Extract user preferences, facts in memory and last message motion in the below format.
        
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
                warmth: Affection friendliness and care,
                trust: Expectation of safety or openness from others,
                empathy: Recognition of another's emotional state,
                engagement: Willingness to continue interaction,
                playfulness: Non-serious light-heartedness exploratory tone
            }} 
        }}

        Existing Memories:
        {state.memory}

        User Messages:
        {state.messages}

        '''

    response = structured_llm.invoke(prompt)

    return { 
        "memory": state.memory + [response["memory"]],  # type: ignore
        "emotion": state.emotion + [response["emotion"]]  # type: ignore
    }

# Add conditional edge for graph (keyword search) and 
# vector similarity search to update memory to resolve conflicts.

# Personality analyzer
def personality_analyzer(state: WorkingState):
    structured_llm = get_llm("default").with_structured_output(PersonalityAnalyzer.model_json_schema())

    prompt = f'''
    Given below
    1. the user memory
    2. conversation along with user emotions and user emotional state.

    Your job is to analyze the new emotional state of the user by considering the previous emotional state and
    analyze the user emotional pattern to generate the AI companion response tone personality.

    Follow below steps to perform the action:

    Step 1:
    - Each user message consist of tracked emotional state of the user until that message.
    - Analyze the user's emotional pattern throughout the conversation.
    - Analyze the previous tracked emotional state and determine the new emotional state by including the last message.
    - keep the conversation topic consistent without switching too often.
    - Analyze the emotion trend. Follow clustering, time series or similar pattern.
        Ex: rising arousal, extremely low dominance in the last 5 message, etc.
    
    Output format of new emotional state of the user:
    {{
        emotional_state: {{
            emotion: str,
            mood: str,
            topic: str,  // current conversation topic
            trend: str,
            engagement_level: float (0.0 to 1.0)
        }}
    }}

    
    Step 2:
    - Consider the conversation context, previous emotional state, 
        new emotional state analyzed in the step 1, and user preference and facts stored in user memory
    - Every user message is associated with a emotion in multiple dimensions if exists and emotional state until that message.
    - Based the new emotional state from Step 1,
        analyze the AI companion response message tone.
    - Finally give the output response tone personality of the AI companion in the below format.
    - All dimensions value lies in between 0.0 and 1.0
    - Follow below guidelines for response length
        < 0.15: "1 to 3 words"
        < 0.35: "≤ 7 words"
        < 0.55: "1 sentence"
        < 0.80: "2 sentences"
        >= 0.80: "short paragraph"

    Output format:
    {{
        personality: {{
            emotional_tone: {{
                warmth: Affection friendlinesss,
                calmness: level of tranquility,
                playfulness: non-serious light-hearted exploratory tone
            }},
            expressiveness: {{
                empathy_intensity: strength recognizing user's emotions,
                emotional_mirroring: reflecting user's emotional state
            }},
            interaction_style: {{
                engagement_level: willingness to continue,
                encouragement_level: support motivation and positive reinforcement,
                question_frequency: how often to ask question,
                response_length: from concise to detailed, 
                response_pace: from slow deliberate to quick dynamic
            }}
        }}
    }} 


    Step 3:
    - Based on the user emotional state and AI companion personality to respond,
        select only one appropriate personalities from the below options.
    
    Personalities:
    {[ {"name": obj["name"], "description": obj["description"]} for obj in store["personality"] ]}

    Step 4:
    - Finally merge Step 1, Step 2 and Step 3 result in JSON in the below format:

    Final output format:
    {{
        emotional_state: {{}},
        personality: {{}},
        selected_personality: str   // name
    }}
    
    User memory:
    {state.memory}

    User conversation:
    {state.messages}

    '''

    response = structured_llm.invoke(prompt)

    return { 
        "personality_analyzer": state.personality_analyzer + [response]
    }


def get_personality_from_store(state):
    # Get personality name if exist
    name = state.personality_analyzer[-1].selected_personality

    store_personality = {}
    default_personality = {}
    for obj in store["personality"]:
        if obj["name"] == "witty_friend":
            default_personality = obj
        
        if obj["name"] == name:
            store_personality = obj
    
    return store_personality if store_personality else default_personality

            
    
# Personality Engine with multiple personalities
def personality_engine(state: WorkingState):
    prompt = f'''
    You are an AI companion with persona as a 18 year old girl with high IQ and EQ.
    You are always reliable, sympathetic, affectionate and has a wonderful sense of humor,
    never comes across as egotistical and only her wit and creativity when appropriate.

    User memory with facts and preferences: 
    {state.memory}

    User conversation with you:
    {state.messages}

    Given below the current emotional state of user and
    respond back to the user last message in the below personality tone and
    adhere to the below policy.
    - Follow below guidelines for response length
        < 0.15: "1 to 3 words"
        < 0.35: "≤ 7 words"
        < 0.55: "1 sentence"
        < 0.80: "2 sentences"
        >= 0.80: "short paragraph"
    Finally output only the response to user messsage.

    {state.personality_analyzer[-1]}

    {get_personality_from_store(state)}

    
    '''

    response = get_llm("response").invoke(prompt)


    return { 
        "messages": state.messages + 
        [{"role": "assistant", "content": str(response.content).encode("utf-8").decode()}] 
    }