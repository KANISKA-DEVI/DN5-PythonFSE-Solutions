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
NEW
│
▼
ASSIGNED  ←─────────────────────────────────────────┐
│                                                   │
▼                                                   │
OPEN (Developer investigates)                        │
│                                                   │
├──► REJECTED (Not a bug / cannot reproduce)        │
│                                                   │
├──► DEFERRED (Valid bug but fixed later)           │
│                                                   │
▼                                                   │
FIXED (Developer fixes and updates ticket)           │
│                                                   │
▼                                                   │
RETEST (QA retests the fix)                          │
│                                                   │
├──► REOPEN (Fix didn't work) ─────────────────────┘
│
▼
VERIFIED (QA confirms fix works)
│
▼
CLOSED


**Rejected path:** Bug is assigned → Developer finds it is not a defect (works as designed) → Marked REJECTED → QA reviews and agrees or escalates.

**Deferred path:** Bug is valid but not critical for the current release → Moved to the product backlog for a future sprint → Marked DEFERRED.

---

### Severity and Priority Classification

**(a) POST /api/courses/ returns 500 Internal Server Error for all requests**
- **Severity:** Critical — the core feature is completely broken, system is unusable
- **Priority:** P1 — must be fixed immediately before any release
- **Justification:** All course creation fails. No workaround exists. Blocks all dependent features.

**(b) Course names longer than 150 characters are silently truncated**
- **Severity:** Medium — data is lost silently without error, which is unexpected behaviour
- **Priority:** P2 — should be fixed soon; misleads users into thinking their data was saved correctly
- **Justification:** Users are not notified of data loss. Could cause issues in reporting, but system is not broken.

**(c) The /docs Swagger page has a typo in the API description**
- **Severity:** Low — cosmetic issue, does not affect functionality
- **Priority:** P3 — fix in the next sprint; not urgent
- **Justification:** No functional impact. Only affects documentation readability.

**(d) Login with correct credentials occasionally returns 401 on first attempt (intermittent)**
- **Severity:** High — authentication failure, even intermittent, affects all users
- **Priority:** P1 — must be fixed urgently despite intermittent nature
- **Justification:** Intermittent bugs are hard to reproduce and often indicate deeper instability (race condition, session issue). Users lose trust when login randomly fails.

---

### Complete Defect Report for Bug (a)

| Field | Value |
|---|---|
| **Defect ID** | BUG-001 |
| **Title** | POST /api/courses/ returns 500 Internal Server Error for all requests |
| **Environment** | Local development — Windows 11, Python 3.12, Django 5.0 |
| **Build Version** | v1.0.0-beta |
| **Severity** | Critical |
| **Priority** | P1 |
| **Steps to Reproduce** | 1. Start the Django development server (`python manage.py runserver`). 2. Open Postman or Thunder Client. 3. Send POST request to `http://127.0.0.1:8000/api/courses/` with body: `{"name":"Test","code":"CS999","credits":3,"department_id":1}`. 4. Observe the response. |
| **Expected Result** | Response: 201 Created with the new course data in JSON format. |
| **Actual Result** | Response: 500 Internal Server Error. Server console shows `IntegrityError: NOT NULL constraint failed: courses_course.department_id` |
| **Attachments** | screenshot_of_500_error.png |

---

### Severity vs Priority — Key Difference

**Severity** measures the **impact on the system** — how badly does this break functionality?

**Priority** measures **how urgently it needs to be fixed** — how soon must we address it?

**Real-world example where High Severity ≠ High Priority:**

> The company's internal HR portal has a bug where the "Print Payslip" button is completely broken (High Severity — core feature is broken). However, payslips are printed only once a month, and the next print date is 28 days away. Meanwhile, a cosmetic typo exists on the CEO's public-facing dashboard presentation page (Low Severity — just a typo), but a board meeting is tomorrow.
>
> In this case: the CEO dashboard typo has **Low Severity but High Priority (P1)** because it must be fixed before tomorrow's meeting. The payslip bug has **High Severity but Medium Priority (P2)** because there are 28 days to fix it with no immediate impact.

---