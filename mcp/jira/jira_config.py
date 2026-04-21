import os


def get_jira_config():
    """
    Load Jira configuration from environment variables (.env)
    """
    return {
        "base_url": os.getenv("JIRA_BASE_URL", "http://mock-jira.local"),
        "user_email": os.getenv("JIRA_USER_EMAIL", "mock@mock.com"),
        "api_token": os.getenv("JIRA_API_TOKEN", "mock-token"),
        "project_key": os.getenv("JIRA_PROJECT_KEY", "MOCK"),
        "use_mock": os.getenv("JIRA_USE_MOCK", "true").lower() == "true",
    }


# Example usage in a tool or client
if __name__ == "__main__":
    config = get_jira_config()
    if config["use_mock"]:
        print("Using mock Jira data.")
    else:
        print(f"Connecting to Jira at {config['base_url']} as {config['user_email']}")
