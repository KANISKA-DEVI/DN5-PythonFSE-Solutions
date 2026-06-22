# Hands-On 2: SDLC vs TDLC — V-Model & Agile QA Integration

---

## TASK 1: V-Model Mapping

### V-Model Diagram
DEVELOPMENT PHASES (Left Side)        TESTING PHASES (Right Side)
─────────────────────────────         ──────────────────────────────
Requirements Analysis         ──────► Acceptance Testing (UAT)
│                                       │
System Design                 ──────► System Testing
│                                       │
Architecture Design           ──────► Integration Testing
│                                       │
Module Design                 ──────► Unit Testing
│                                       │
┌─── CODING ───┐
└──────────────┘
(bottom vertex)


**How to read:** Each development phase on the LEFT corresponds to a testing phase on the RIGHT. The test plans are CREATED during the development phase but EXECUTED later.

---

### Test Artifacts Produced During Each Development Phase

| Development Phase | Test Artifact Created | Testing Phase |
|---|---|---|
| Requirements Analysis | Acceptance Test Plan — defines what the user must be able to do | User Acceptance Testing |
| System Design | System Test Plan — defines end-to-end test scenarios | System Testing |
| Architecture Design | Integration Test Plan — defines how components are tested together | Integration Testing |
| Module Design | Unit Test Cases — defines tests for individual functions/classes | Unit Testing |
| Coding | Actual code + unit tests written | Execution begins (bottom of V) |

---

### Entry and Exit Criteria for Each Testing Level

#### Unit Testing
- **Entry Criteria:** Module/function code is complete. Developer has performed basic desk-checking. Unit test cases are written and reviewed.
- **Exit Criteria:** All planned unit tests executed. Code coverage ≥ 80%. Zero open Critical/High defects at unit level.

#### Integration Testing
- **Entry Criteria:** All individual modules have passed unit testing. Integration test cases are prepared. Test environment is configured.
- **Exit Criteria:** All integration test cases executed. All inter-module interfaces verified. No Critical defects open.

#### System Testing
- **Entry Criteria:** All integration tests have passed. System test environment mirrors production. System test plan approved.
- **Exit Criteria:** All planned system test cases executed. Defect count below agreed threshold. No open Critical or High defects.

#### User Acceptance Testing (UAT)
- **Entry Criteria:** System testing complete and signed off. UAT environment ready. Business users available for testing.
- **Exit Criteria:** All acceptance criteria met. Business stakeholders have signed off. Any open defects are documented and accepted by the business.

---

### Two Early QA Engagement Points in the V-Model

**1. Requirements Phase (Left Side — Before Any Code):**
QA engineers should review requirements for ambiguity, testability, and completeness. For the Course Management API, QA would review: "Is the requirement 'course code must be unique' testable? What happens if a duplicate is submitted — what exact error code and message is expected?" Catching this early prevents rework later.

**2. System Design Phase (Left Side — Before Development):**
QA should review the system design to identify integration risks. For the Course Management API, QA would ask: "How does the enrollment endpoint interact with the course service? What happens if the course service is unavailable during enrollment?" These questions shape integration test cases before any code is written.

---

## TASK 2: Agile QA and Shift-Left Testing

### 3 Problems with Waterfall Testing for the Course Management API

1. **Late defect discovery:** If testing only starts after 3 months of development, a fundamental design flaw (e.g., the enrollment endpoint cannot handle concurrent requests) is discovered when fixing it requires rewriting core architecture — extremely expensive.

2. **Time compression at the end:** Developers often take longer than planned, so testing time gets compressed. For the Course Management API, this means critical tests like authentication and security might be skipped or rushed.

3. **No feedback loop:** Developers write code for months without knowing if it meets user expectations. When QA finally tests, they may find the API design is not what the college admin users actually need — entire features may be discarded.

---

### QA Role in Each Agile Ceremony

| Ceremony | QA Engineer's Role |
|---|---|
| **Sprint Planning** | Helps define clear Acceptance Criteria for each user story. Asks "How will we know this is done?" For the Course Management API, QA defines: "POST /api/courses/ must return 201 with course data and a Location header." |
| **Daily Standup** | Reports blocking issues: "I cannot test the enrollment endpoint because the course service is returning 500 — blocking me since yesterday." This surfaces blockers immediately instead of hiding them. |
| **Sprint Review** | Tests the demo in real-time. Verifies that completed stories actually meet the acceptance criteria. May find issues during the live demo that automated tests missed. |
| **Retrospective** | Suggests process improvements: "We keep finding authentication bugs late — can we add a security checklist to the definition of done?" Continuously improves the QA process. |

---

### 4 Shift-Left Practices Applied to the Course Management API

**(a) Reviewing Requirements for Testability:**
Before sprint starts, QA reviews: "POST /api/courses/ creates a course." QA asks: what fields are required? What validation rules apply? What status codes are expected? This makes requirements testable and prevents ambiguous implementations.

**(b) Writing Test Cases Before Code (TDD/BDD):**
QA writes test cases for the enrollment endpoint BEFORE the developer codes it. The developer then writes code to make those tests pass. This ensures the code is designed to be testable from the start, not retrofitted for testing later.

**(c) Static Code Analysis:**
Tools like `flake8`, `pylint`, and `bandit` (security) are run on every code commit in the CI pipeline. This catches code quality issues, security vulnerabilities (SQL injection patterns), and style violations before the code is even reviewed by a human.

**(d) API Contract Testing Before Integration:**
Using tools like Pact or Postman Collection tests, the agreed API contract (endpoint URLs, request/response schemas) is tested before the frontend team integrates with the backend. This catches breaking changes early — for example, if the backend team renames `course_id` to `id`, contract tests fail immediately.

---

### Acceptance Criteria in Given-When-Then (Gherkin) Format

**User Story:** "As a college admin, I want to create a new course, so that students can enroll in it."

**Scenario 1: Happy Path**
```gherkin
Given the college admin is authenticated with a valid JWT token
And the database contains a department with id 1
When the admin sends a POST request to /api/courses/ with body:
  | name          | "Data Structures & Algorithms" |
  | code          | "CS101"                        |
  | credits       | 4                              |
  | department_id | 1                              |
Then the response status code should be 201 Created
And the response body should contain the created course with a generated id
And the response headers should contain a Location header pointing to the new course
```

**Scenario 2: Duplicate Course Code**
```gherkin
Given the college admin is authenticated
And a course with code "CS101" already exists in the database
When the admin sends a POST request to /api/courses/ with code "CS101"
Then the response status code should be 409 Conflict or 400 Bad Request
And the response body should contain an error message indicating the course code already exists
```

**Scenario 3: Missing Required Fields**
```gherkin
Given the college admin is authenticated
When the admin sends a POST request to /api/courses/ with body:
  | name    | "Data Structures" |
  | credits | 4                 |
  (note: "code" field is missing)
Then the response status code should be 400 Bad Request or 422 Unprocessable Entity
And the response body should contain a validation error mentioning the missing "code" field
```

---