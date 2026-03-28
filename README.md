# Automation Platform

## Overview

The **Automation Platform** is a Python-based framework designed to support automated software testing, utilities, and AI-assisted development workflows. It provides a modular architecture for building reusable automation components such as agents, utilities, test runners, and integrations.

This repository currently includes:

* An AI-powered coding agent
* File system utilities
* Excel CRUD automation utilities
* Tool-based command execution framework
* Environment-based configuration management
* Scalable project structure for future automation features

The platform is being developed as part of a professional automation engineering portfolio and is designed to evolve into a production-ready automation framework.

---

## Project Structure

```
automation/
│
├── coding_agent/
│   ├── agent.py
│   └── __init__.py
│
├── utilities/
│   ├── excel_crud.py
│   └── __init__.py
│
├── tests/
│   └── test_excel_crud.py
│
├── documentation/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Features

Current capabilities:

* AI coding agent with tool execution
* File read/write/edit utilities
* Bash command execution
* Excel CRUD automation
* Modular architecture for reusable automation components
* Environment-based secret management
* Ready for CI/CD integration

Planned enhancements:

* Test execution orchestration
* Logging and monitoring
* Configuration management
* Plugin-style tool registration
* CI pipeline integration
* Automated reporting
* Test data management utilities

---

## Requirements

Python:

```
Python 3.12+
```

Dependencies:

```
anthropic
pydantic
python-dotenv
openpyxl
pandas
pytest
```

Install dependencies:

```
pip install -r requirements.txt
```

---

## Environment Configuration

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_api_key_here
```

The application loads environment variables using:

```
python-dotenv
```

Important:

```
The .env file must never be committed to version control.
```

---

## Running the Coding Agent

Activate the virtual environment:

```
source .venv/bin/activate
```

Run the agent:

```
python coding_agent/agent.py
```

Exit the agent:

```
exit
```

or

```
quit
```

---

## Development Workflow

Standard workflow:

```
Activate virtual environment
Make code changes
Run tests
Commit changes
Push to repository
```

Example:

```
pytest
git add .
git commit -m "Add new utility function"
git push
```

---

## Testing

Run the test suite:

```
pytest
```

Future enhancements:

* Unit tests
* Integration tests
* Utility validation tests
* Agent behavior tests

---

## Security Notes

Sensitive data must be stored in:

```
.env
```

Never commit:

* API keys
* Secrets
* Tokens
* Credentials

---

## Future Roadmap

Planned platform capabilities:

* AI-driven test generation
* Test execution orchestration
* Reporting and analytics
* Test data management
* CI/CD automation
* Plugin-based architecture
* Multi-environment configuration

---

## License

This project is intended for educational and professional portfolio use.
