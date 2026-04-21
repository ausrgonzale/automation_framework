from pydantic import BaseModel, Field


class TestCase(BaseModel):
        __test__ = False
    """
    Represents a single generated test case.
    """

    title: str = Field(
        description="Short name of the test case"
    )

    description: str = Field(
        description="Detailed explanation of the test case"
    )

    steps: list[str] = Field(
        description="Ordered steps to execute the test"
    )

    expected_result: str = Field(
        description="Expected outcome after executing the steps"
    )

class TestCaseSet(BaseModel):
        __test__ = False
    """
    Collection of generated test cases.
    """

    testcases: list[TestCase]