# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle

---

## TASK 1: Map Testing Types to a Real System (Course Management API)

### Test Cases for Each Testing Level

#### Unit Testing
- **Test Case:** Test the `validate_course_code()` function in isolation.
- **Description:** Call `validate_course_code("CS101")` and verify it returns `True`. Call it with `""` and verify it returns `False`.
- **Classification:** Functional — tests whether the function does what it should.

#### Integration Testing
- **Test Case:** Test the POST /api/courses/ endpoint together with the database layer.
- **Description:** Send a POST request with valid course data. Verify the response is 201 Created AND the record actually appears in the database.
- **Classification:** Functional — verifies two components work together correctly.

#### System Testing
- **Test Case:** End-to-end flow — register a user, log in, create a course, enroll a student, retrieve enrollment.
- **Description:** Execute the full workflow from login to enrollment retrieval as a complete system test.
- **Classification:** Functional — tests the entire system from start to finish.

#### User Acceptance Testing (UAT)
- **Test Case:** A college admin creates a new course using the API.
- **Description:** From the perspective of a real college admin, POST to /api/courses/ with realistic data (course name, code, department). Verify the course appears in GET /api/courses/.
- **Classification:** Functional — tests from the actual user's perspective.

---

### Non-Functional Test Example
- **Type:** Performance Testing
- **Test:** Send 100 concurrent GET /api/courses/ requests and verify the average response time is under 500ms and no request fails.
- **Classification:** Non-Functional — answers "how fast" not "does it work".

---

### Black-Box vs White-Box Testing

**Black-Box Testing:**
- Tester has NO knowledge of the internal code or implementation.
- Tester only knows the inputs and expected outputs.
- Tests are based on requirements and specifications.
- **Who performs it:** QA testers typically perform black-box testing.
- **Example:** A QA tester sends POST /api/courses/ with valid data and checks the response is 201 — they don't know or care how the code works internally.

**White-Box Testing:**
- Tester has FULL knowledge of the internal code structure.
- Tests are written to cover specific code paths, branches, and conditions.
- **Who performs it:** Developers typically perform white-box testing (unit tests, code coverage).
- **Example:** A developer writes a unit test that specifically tests the `if not course_code:` branch inside the validation function.

---

### Formal Test Cases for POST /api/courses/

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-001 | Create a course with valid data | API is running. Database is empty. Auth token available. | 1. Send POST /api/courses/ with body: `{"name":"Data Structures","code":"CS101","credits":4,"department_id":1}` 2. Check response status code. 3. Check response body. | Status: 201 Created. Body contains `id`, `name`, `code`, `credits`. | | |
| TC-002 | Create a course with missing required field (no code) | API is running. Auth token available. | 1. Send POST /api/courses/ with body: `{"name":"Data Structures","credits":4}` (no `code` field) 2. Check response status code. | Status: 400 Bad Request. Body contains error message mentioning missing field. | | |
| TC-003 | Create a course with duplicate course code | API is running. Course CS101 already exists in database. | 1. Send POST /api/courses/ with body: `{"name":"Another Course","code":"CS101","credits":3}` 2. Check response status code. | Status: 409 Conflict or 400 Bad Request. Body contains error about duplicate code. | | |

---

## TASK 2: Defect Lifecycle & Severity Classification

### Defect Lifecycle