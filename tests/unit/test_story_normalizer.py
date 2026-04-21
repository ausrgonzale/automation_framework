from ai.utils.story_normalizer import StoryNormalizer


def test_normalize_jira_story():
    raw = {
        "key": "JIRA-123",
        "summary": "User login",
        "description": "As a user, I want to log in.",
        "acceptanceCriteria": "User can log in with valid credentials.",
        "tool": "Playwright",
        "language": "Python",
    }
    norm = StoryNormalizer.normalize(raw)
    assert norm["id"] == "JIRA-123"
    assert norm["summary"] == "User login"
    assert norm["acceptance_criteria"] == "User can log in with valid credentials."
    assert norm["tool"] == "Playwright"
    assert norm["language"] == "Python"


def test_normalize_excel_story():
    raw = {
        "story_id": "EXCEL-1",
        "title": "Registration",
        "details": "As a user, I want to register.",
        "criteria": "User can register with email.",
        "framework": "Selenium",
        "lang": "Java",
    }
    norm = StoryNormalizer.normalize(raw)
    assert norm["id"] == "EXCEL-1"
    assert norm["summary"] == "Registration"
    assert norm["acceptance_criteria"] == "User can register with email."
    assert norm["tool"] == "Selenium"
    assert norm["language"] == "Java"


def test_to_prompt():
    norm = {
        "id": "JIRA-1",
        "summary": "Login",
        "description": "Login feature.",
        "acceptance_criteria": "Valid login.",
        "tool": "Playwright",
        "language": "Python",
    }
    prompt = StoryNormalizer.to_prompt(norm)
    assert "Jira ID: JIRA-1" in prompt
    assert "Summary: Login" in prompt
    assert "Tool: Playwright" in prompt
    assert "Language: Python" in prompt


def test_normalize_priority_excel():
    raw = {
        "story_id": "EXCEL-2",
        "title": "Priority Test",
        "details": "Test priority normalization.",
        "criteria": "Priority is set.",
        "framework": "Selenium",
        "lang": "Java",
        "priority": "High",
    }
    norm = StoryNormalizer.normalize(raw)
    assert norm.get("priority") == "High"


def test_normalize_priority_jira():
    raw = {
        "key": "JIRA-456",
        "summary": "Priority Jira",
        "description": "Jira priority normalization.",
        "acceptanceCriteria": "Priority is set.",
        "tool": "Playwright",
        "language": "Python",
        "priority": "Medium",
    }
    norm = StoryNormalizer.normalize(raw)
    assert norm.get("priority") == "Medium"
