from pydantic import BaseModel, Field


class CheckCase(BaseModel):
    """
    Represents a single generated test case.
    """

    title: str = Field(description="Short name of the test case")

    description: str = Field(description="Detailed explanation of the test case")

    steps: list[str] = Field(description="Ordered steps to execute the test")

    expected_result: str = Field(
        description="Expected outcome after executing the steps"
    )


class CheckCaseSet(BaseModel):
    """
    Collection of generated test cases.
    """

    testcases: list[CheckCase]
