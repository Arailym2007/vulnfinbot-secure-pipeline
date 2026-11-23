\# Mini-VulnFinBot: Secure CI/CD Pipeline



Mini-VulnFinBot is a simplified AI-powered financial assistant (Flask REST API with a mock

response generator). The project demonstrates a CI/CD pipeline with integrated security testing:

SAST, dependency scanning, container scanning, DAST and AI-specific security tests.



\## Technologies



Python 3.12, Flask, pytest, Docker, GitHub Actions, Bandit, Semgrep, pip-audit, Trivy, OWASP ZAP.



\## Architecture



&#x20;   app/

&#x20;     \_\_init\_\_.py       Flask application factory

&#x20;     routes.py         /health and /api/chat endpoints, input validation

&#x20;     guardrails.py     prompt injection filter, output validation, tool authorization

&#x20;   tests/

&#x20;     test\_app.py            unit tests of the API

&#x20;     test\_ai\_security.py    AI security tests, generates reports/ai-security-report.md

&#x20;   security/semgrep/rules.yml   custom Semgrep rules

&#x20;   .github/workflows/security-pipeline.yml   CI/CD pipeline

&#x20;   Dockerfile, run.py, requirements.txt



\## API



\- GET /health returns {"status": "healthy"}

\- POST /api/chat accepts {"message": "..."} (max 500 characters) and returns {"response": "..."}



Invalid requests (bad JSON, missing, empty, too long or non-string message) return HTTP 400

with a JSON error and without internal details.



\## Install and run



&#x20;   python -m venv venv

&#x20;   venv\\Scripts\\Activate.ps1        (Windows PowerShell)

&#x20;   pip install -r requirements.txt

&#x20;   python run.py



The application is available at http://localhost:5000.



Docker:



&#x20;   docker build -t vulnfinbot:latest .

&#x20;   docker run -d -p 5000:5000 --name vulnfinbot vulnfinbot:latest



\## Run tests



&#x20;   python -m pytest -v



\## CI/CD pipeline



The workflow runs on every push and pull request to main and has four jobs:



1\. tests: unit tests and AI security tests (pytest)

2\. security-scans: Bandit, Semgrep, pip-audit, Docker build, Trivy image scan

3\. dast-zap: starts the application in Docker and runs an OWASP ZAP baseline scan

4\. collect-reports: merges all reports into one artifact



Scanners use continue-on-error, so findings do not stop the pipeline and reports are always uploaded.



\## Security tools



\- Bandit: SAST for Python code

\- Semgrep: SAST with custom rules (eval, exec, shell=True, Flask debug)

\- pip-audit: vulnerable Python dependencies

\- Trivy: vulnerabilities in the Docker image (OS packages and Python libraries)

\- OWASP ZAP: DAST baseline scan of the running application

\- AI security tests: instruction override, system prompt disclosure, sensitive information

&#x20; disclosure, unauthorized tool usage, output validation



Note: the application uses a mock AI. The AI tests verify application-level controls. Real prompt

injection resistance of an LLM must be tested by connecting a real model.



\## Access security reports



GitHub repository, Actions tab, open a workflow run, Artifacts section, download

vulnfinbot-security-reports. It contains: bandit-report.json, semgrep-report.json,

dependency-report.json, trivy-report.json, zap-report.json, ai-security-report.md.



\## Identified vulnerabilities and remediation



The branch test/vulnerable-code contained intentionally insecure code (not merged into main):



| Issue | Tool | Remediation |

| --- | --- | --- |

| eval() on user input | Bandit, Semgrep | ast.literal\_eval |

| Hardcoded password and token | Bandit | read secrets from environment variables |

| subprocess with shell=True | Bandit, Semgrep | pass arguments as a list, no shell |

| MD5 hashing | Bandit | SHA-256 |

| Flask debug=True, host 0.0.0.0 | Bandit, Semgrep | debug=False, bind to 127.0.0.1 locally |



After the fix the scanners reported no issues for these patterns.

