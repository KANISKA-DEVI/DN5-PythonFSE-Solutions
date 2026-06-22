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

| Type | Knowledge of Code | Who Performs It | Example |
|------|-------------------|-----------------|---------|
| **Black-Box Testing** | No knowledge of internal code. Tests based on inputs and expected outputs only. | QA Testers | Send POST /api/courses/ with valid data, check response is 201 — without knowing how the code works internally. |
| **White-Box Testing** | Full knowledge of internal code structure. Tests written to cover specific code paths and branches. | Developers | Write a unit test that specifically tests the `if not course_code:` branch inside the validation function. |

---

### Formal Test Cases for POST /api/courses/

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC-001 | Create a course with valid data | API is running. Database is empty. Auth token available. | 1. Send POST /api/courses/ with body: `{"name":"Data Structures","code":"CS101","credits":4,"department_id":1}` 2. Check response status code. 3. Check response body. | Status: 201 Created. Body contains `id`, `name`, `code`, `credits`. | | |
| TC-002 | Create a course with missing required field (no code) | API is running. Auth token available. | 1. Send POST /api/courses/ with body: `{"name":"Data Structures","credits":4}` (no `code` field). 2. Check response status code. | Status: 400 Bad Request. Body contains error message mentioning missing field. | | |
| TC-003 | Create a course with duplicate course code | API is running. Course CS101 already exists in database. | 1. Send POST /api/courses/ with body: `{"name":"Another Course","code":"CS101","credits":3}`. 2. Check response status code. | Status: 409 Conflict or 400 Bad Request. Body contains error about duplicate code. | | |

---

## TASK 2: Defect Lifecycle & Severity Classification

### Defect Lifecycle

| Step | State | Description |
|------|-------|-------------|
| 1 | 🆕 **NEW** | Bug is reported for the first time |
| 2 | 📋 **ASSIGNED** | Bug is assigned to a developer |
| 3 | 🔓 **OPEN** | Developer starts investigating the bug |
| 4 | ✅ **FIXED** | Developer fixes the bug and updates the ticket |
| 5 | 🔁 **RETEST** | QA retests the fix |
| 6 | ✔️ **VERIFIED** | QA confirms the fix works correctly |
| 7 | 🔒 **CLOSED** | Bug is officially closed |

**Special Paths:**

| Path | Description |
|------|-------------|
| ➡️ **REJECTED** | Developer finds it is not a real bug (works as designed) → Marked Rejected → QA reviews and agrees or escalates |
| ⏸️ **DEFERRED** | Valid bug but not critical for the current release → Moved to product backlog for a future sprint → Marked Deferred |
| 🔄 **REOPEN** | Fix did not work during retest → Bug goes back to ASSIGNED state |

**Complete Flow:**

> 🆕 NEW → 📋 ASSIGNED → 🔓 OPEN → ✅ FIXED → 🔁 RETEST → ✔️ VERIFIED → 🔒 CLOSED

---

### Severity and Priority Classification

| Bug | Severity | Priority | Justification |
|-----|----------|----------|---------------|
| **(a)** POST /api/courses/ returns 500 Internal Server Error for all requests | **Critical** | **P1** | Core feature is completely broken. No workaround exists. Blocks all dependent features. Must be fixed immediately. |
| **(b)** Course names longer than 150 characters are silently truncated | **Medium** | **P2** | Data is lost silently without error. Users are not notified. Could cause reporting issues but system is not broken. |
| **(c)** The /docs Swagger page has a typo in the API description | **Low** | **P3** | Cosmetic issue only. No functional impact. Fix in next sprint. |
| **(d)** Login with correct credentials occasionally returns 401 on first attempt | **High** | **P1** | Intermittent authentication failure affects all users. Hard to reproduce, indicates deeper instability. Users lose trust. |

---

### Complete Defect Report for Bug (a)

| Field | Value |
|-------|-------|
| **Defect ID** | BUG-001 |
| **Title** | POST /api/courses/ returns 500 Internal Server Error for all requests |
| **Environment** | Local development — Windows 11, Python 3.12, Django 5.0 |
| **Build Version** | v1.0.0-beta |
| **Severity** | Critical |
| **Priority** | P1 |
| **Steps to Reproduce** | 1. Start the Django development server (`python manage.py runserver`). 2. Open Postman or Thunder Client. 3. Send POST request to `http://127.0.0.1:8000/api/courses/` with body: `{"name":"Test","code":"CS999","credits":3,"department_id":1}`. 4. Observe the response. |
| **Expected Result** | Response: 201 Created with the new course data in JSON format. |
| **Actual Result** | Response: 500 Internal Server Error. Server console shows `IntegrityError: NOT NULL constraint failed`. |
| **Attachments** | screenshot_of_500_error.png |

---

### Severity vs Priority — Key Difference

| Concept | Definition |
|---------|------------|
| **Severity** | Measures the **impact on the system** — how badly does this break functionality? |
| **Priority** | Measures **how urgently it needs to be fixed** — how soon must we address it? |

**Real-world example where High Severity ≠ High Priority:**

> The company's internal HR portal has a bug where the **"Print Payslip" button is completely broken** (High Severity — core feature is broken). However, payslips are only printed once a month and the next print date is 28 days away.
>
> Meanwhile, a **cosmetic typo exists on the CEO's public-facing dashboard** (Low Severity — just a typo), but a board meeting is tomorrow morning.

| Bug | Severity | Priority | Reason |
|-----|----------|----------|--------|
| Print Payslip broken | High | P2 — Medium | 28 days to fix, no immediate impact |
| CEO dashboard typo | Low | P1 — High | Must be fixed before tomorrow's board meeting |