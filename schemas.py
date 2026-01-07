from pydantic import BaseModel, Field

class ChangeClassification(BaseModel):
    change_type: str = Field(
        description="NEW_OBLIGATION, MODIFIED_OBLIGATION, CLARIFICATION, DEADLINE_CHANGE, NO_IMPACT"
    )
    summary: str
    confidence: float
