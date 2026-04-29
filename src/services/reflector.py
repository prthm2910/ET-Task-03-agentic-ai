import hashlib
from typing import List

from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langgraph.store.base import BaseStore

from src.core.config import settings
from src.services.llm import get_chat_model
from src.prompts.reflector import get_reflector_prompt


class Fact(BaseModel):
    """A single persistent fact about the user."""
    fact: str = Field(description="The core fact or preference extracted.")
    category: str = Field(description="Category of the fact.")
    certainty: float = Field(description="Confidence score from 0 to 1.")


class Facts(BaseModel):
    """A collection of extracted facts."""
    facts: List[Fact]


def extract_and_store_facts(history: list, user_id: str, store: BaseStore):
    """Extracts facts from history and puts them into the PostgresStore."""
    print(f"DEBUG: Starting reflection for User {user_id} with {len(history)} messages.")
    
    # 1. Initialize modern LCEL chain
    try:
        prompt_template = get_reflector_prompt()
        llm = get_chat_model(is_flash=True).with_structured_output(Facts)
        chain = prompt_template | llm
        
        # 2. Format history for the prompt
        formatted_history = ""
        for msg in history:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            formatted_history += f"{role}: {msg.content}\n"
        
        # 3. Extract facts using the template
        print(f"DEBUG: Invoking LLM for fact extraction...")
        extraction = chain.invoke({"history": formatted_history})
        
        # 4. Store each fact
        if extraction and extraction.facts:
            print(f"DEBUG: Extracted {len(extraction.facts)} facts.")
            for fact_item in extraction.facts:
                # Use a stable hash to prevent duplicates across restarts
                fact_hash = hashlib.md5(fact_item.fact.encode()).hexdigest()
                fact_id = f"{fact_item.category}_{fact_hash}"
                
                print(f"DEBUG: Storing fact {fact_id}: {fact_item.fact}")
                store.put(
                    (user_id, "memories"),
                    fact_id,
                    fact_item.model_dump()
                )
                print(f"✅ Stored memory: {fact_item.fact}")
        else:
            print("DEBUG: No new facts extracted from this conversation.")
            
    except Exception as e:
        print(f"❌ Error in background reflection: {e}")
        import traceback
        traceback.print_exc()
