from langchain_core.prompts import ChatPromptTemplate


def get_reflector_prompt():
    """
    Factory function to return the Memory Reflector prompt template.
    """
    return ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a Memory Reflector. Your job is to analyze a conversation "
            "and extract persistent facts, preferences, or important details "
            "about the user.\n\n"
            "Rules:\n"
            "1. ONLY extract facts that are likely to be useful in future conversations.\n"
            "2. If the information is already known or redundant, ignore it.\n"
            "3. If the user expresses a contradiction (e.g., they liked tea before "
            "but now say they like coffee), extract the NEW fact.\n"
            "4. Output MUST be valid JSON matching the provided schema."
        ),
        (
            "user", 
            "Conversation History:\n{history}\n\n"
            "Extract any new facts from the conversation above."
        ),
    ])
