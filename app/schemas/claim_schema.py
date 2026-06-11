from pydantic import BaseModel, Field


class ClaimRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        example="My car was scratched while parked",
        description="Description of the insurance claim"
    )