# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle
@'
# Hands-On 1: QA Concepts, Functional Testing & Defect Lifecycle
**Name:** Sharmi | **Register No:** 2117230020206 | **Program:** Digital Nurture 5.0 - Python Full Stack Engineer Track

---

## Task 1: Map Testing Types to a Real System
*(System under test: Course Management API)*

### 1. Test cases by test level

| Test Level | What it Checks | Concrete Test Case |
|---|---|---|
| **Unit Testing** | A single function in isolation | Test the validate_course_code() function directly: pass "CS101" -> expect True; pass "C" -> expect False (too short). No database or API call involved - pure function input/output. |
| **Integration Testing** | Two components working together | Call the create_course() service function and verify it correctly inserts a row into the courses table in PostgreSQL - i.e. the API layer + database layer talking to each other. |
| **System Testing** | Full end-to-end flow | Send a real POST /api/courses/ HTTP request with a JSON body, and verify the response is 201 Created, the response body has the correct fields, AND the row exists in the database afterward. |
| **User Acceptance Testing (UAT)** | Perspective of an actual end user | A college admin logs into the admin panel, fills the "Add New Course" form with real course details, clicks Save, and confirms the course appears in the course listing exactly as expected - without ever seeing the API or database. |

### 2. Functional vs Non-Functional classification

| Test Case | Classification |
|---|---|
| Unit test on validate_course_code() | Functional |
| Integration test on create_course() + DB | Functional |
| System test on POST /api/courses/ | Functional |
| UAT: admin adds a course via UI | Functional |

**Non-functional example:** Performance test - "GET /api/courses/ must return a response in under 500ms when the courses table has 10,000 rows." This doesn't ask "does it work correctly" but "does it work well enough."

### 3. Black-Box vs White-Box Testing

- **Black-Box Testing:** The tester has no knowledge of the internal code - they only see inputs and outputs. E.g. sending various payloads to POST /api/courses/ and checking the HTTP response, without ever opening the source file.
- **White-Box Testing:** The tester knows the internal code structure and designs tests to cover specific logic branches, loops, and conditions inside the function.

**Who does what:** QA testers typically perform black-box testing (testing from the user/API-contract perspective). Developers typically perform white-box testing (unit tests written with knowledge of the internal implementation, aiming for code coverage).

### 4. Formal Test Cases - POST /api/courses/

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC_COURSE_001 | Create a course with valid data | API server running; DB reachable; no existing course with the same code | 1. Send POST /api/courses/ with valid JSON body {code:"CS101", name:"Intro to CS", credits:4} 2. Inspect response | Response status 201 Created; response body contains the created course with a generated id; row exists in DB | | |
| TC_COURSE_002 | Reject duplicate course code | A course with code CS101 already exists | 1. Send POST /api/courses/ with {code:"CS101", ...} again | Response status 400 Bad Request with an error message indicating duplicate course code; no new row created | | |
| TC_COURSE_003 | Reject request with missing required field | API server running | 1. Send POST /api/courses/ with body missing the name field | Response status 422 Unprocessable Entity; error message specifies name is required; no row created | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle

New -> Assigned -> Open -> Fixed -> Retest -> Verified -> Closed

- **New:** Tester logs the defect for the first time.
- **Assigned:** Lead/manager assigns the defect to a developer.
- **Open:** Developer starts working, acknowledges the issue is valid.
- **Fixed:** Developer completes the fix and marks it ready for retest.
- **Retest:** Tester re-executes the original steps against the fix.
- **Verified:** Tester confirms the fix works and the defect no longer reproduces.
- **Closed:** Defect is formally closed and archived.

**Alternate paths:**
- **Rejected:** From "Open," the developer determines the reported behavior is actually correct (not a bug, or a duplicate) and rejects it - it does not go to "Fixed."
- **Deferred:** From "Open" or "Assigned," the team decides the fix is valid but will be postponed to a future release (low impact, tight deadline) - it sits in "Deferred" until picked up again later.

### 6. Severity & Priority Classification

| Bug | Severity | Priority | Justification |
|---|---|---|---|
| (a) POST /api/courses/ returns 500 for all requests | Critical | P1 | Core functionality is completely broken for every user - blocks all course creation. |
| (b) Course names > 150 chars silently truncated, no error | Medium | P3 | Data is corrupted silently, but doesn't crash the system or block usage - an edge case affecting few users. |
| (c) Typo in Swagger /docs description | Low | P4 | Cosmetic only; no functional impact. |
| (d) Login with correct credentials intermittently returns 401 | High | P2 | Affects a core flow (login) unpredictably; hard to reproduce and erodes user trust, even though it doesn't fail every time. |

### 7. Defect Report - Bug (a)

| Field | Value |
|---|---|
| **Defect ID** | DEF-2026-0142 |
| **Title** | POST /api/courses/ returns 500 Internal Server Error for all requests |
| **Environment** | Staging, Ubuntu 22.04, Python 3.11, PostgreSQL 15 |
| **Build Version** | v1.4.2-staging |
| **Severity** | Critical |
| **Priority** | P1 |
| **Steps to Reproduce** | 1. Authenticate as admin. 2. Send POST /api/courses/ with a valid JSON body. 3. Observe the response. |
| **Expected Result** | 201 Created response with the newly created course object. |
| **Actual Result** | 500 Internal Server Error returned for every request, regardless of payload. |
| **Attachments** | screenshot of 500 error |

### 8. Severity vs Priority

**Severity** measures how badly the defect impacts the system's functionality or data. **Priority** measures how urgently it needs to be fixed, based on business impact and timing.

**Example where High Severity != High Priority:** A rarely-used "Export to PDF" feature crashes the entire admin panel (High Severity - it breaks the app), but it's scheduled to be removed in next month's release anyway, so it's marked Low Priority.

**Reverse example:** A cosmetic bug on the CEO's personal dashboard - a misaligned logo - has Low Severity (nothing breaks) but might get High Priority because a stakeholder specifically flagged it.
'@ | Set-Content -Path written_exercises\qa_concepts.md -Encoding UTF8