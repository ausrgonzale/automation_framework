from services.testcase_generation_service import CheckcaseGenerationService


class DummyRepo:
    def save(self, testcases, source=None):
        self.saved = testcases


def test_service_priority_field():
    repo = DummyRepo()
    service = CheckcaseGenerationService(repo)
    extra_fields = {
        "summary": "Priority Service",
        "description": "Service test",
        "acceptance_criteria": "Should have priority",
        "related_to": [],
        "priority": "Blocker",
        "language": "Python",
        "tool": "Pytest",
    }
    testcases = service.generate_testcases(
        requirement="Service requirement",
        user_story_id="SVC-1",
        extra_fields=extra_fields,
        testcase_index=0,
    )
    assert testcases
    assert testcases[0]["Priority"] == "Blocker"
