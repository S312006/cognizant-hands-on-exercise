# Hands-On 2: S@'
# Hands-On 2: SDLC vs TDLC - V-Model & Agile QA Integration
**Name:** Sharmi | **Register No:** 2117230020206 | **Program:** Digital Nurture 5.0 - Python Full Stack Engineer Track

---

## Task 1: V-Model Mapping

### 9. V-Model Diagram (ASCII)

Requirements  -----------------------------  Acceptance Testing
    \                                              /
System Design ----------------------------  System Testing
      \                                        /
 Architecture Design --------------------  Integration Testing
        \                                  /
    Module Design --------------  Unit Testing
          \                            /
                    Coding

Left side = development phases (top to bottom: Requirements -> System Design -> Architecture Design -> Module Design -> Coding). Right side = corresponding testing phases (bottom to top: Unit Testing -> Integration Testing -> System Testing -> Acceptance Testing). Coding sits at the bottom vertex connecting both sides.

### 10. SDLC phase -> Test artifact produced

| SDLC Phase | Test Artifact Produced |
|---|---|
| Requirements | Acceptance Test Plan is prepared during this phase |
| System Design | System Test Plan is prepared, based on overall system behavior |
| Architecture Design | Integration Test Plan is prepared, covering module-to-module interfaces |
| Module Design | Unit Test Plan / test case specs are prepared for individual functions |
| Coding | Actual test scripts (unit tests) are written alongside the code |

### 11. Entry & Exit Criteria per TDLC phase

| Testing Phase | Entry Criteria | Exit Criteria |
|---|---|---|
| **Unit Testing** | Module code is complete and compiles; unit test plan is ready | All unit test cases executed; code coverage target met (e.g. 80%); no open critical defects in the unit |
| **Integration Testing** | All required unit-tested modules are available; integration test plan is ready | All module interfaces tested; no critical/high defects open in integration points |
| **System Testing** | Application is fully integrated and deployed to test environment; system test plan is ready | All planned system test cases executed; defect count below threshold; no open critical/high defects |
| **Acceptance Testing (UAT)** | System testing is complete and signed off; UAT environment is ready with production-like data | Business/end users have validated all acceptance criteria; sign-off obtained from stakeholders |

### 12. Two early QA engagement points in the Course Management API project

1. **During Requirements Review** - QA reviews the requirements document for ambiguity, testability, and missing edge cases (e.g. "what happens if two admins create a course with the same code simultaneously?") before a single line of code is written.
2. **During Architecture/API Design Review** - QA reviews the proposed API contract (request/response schemas, status codes) and flags inconsistencies early, so integration tests can be planned in parallel with development instead of after.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Three problems with Waterfall (test-after-development) for the Course Management API

1. Defects found late are far more expensive to fix - a design flaw discovered during system testing may require reworking the database schema, affecting already-completed code.
2. Testers are idle during development and then overloaded right before release, creating a testing bottleneck under deadline pressure.
3. Feedback from testing arrives too late to influence design decisions - if the requirements were ambiguous, the misunderstanding isn't caught until the "finished" product fails testing.

### 14. QA role in Agile ceremonies

| Ceremony | QA Engineer's Role |
|---|---|
| **Sprint Planning** | Defines acceptance criteria for each user story alongside the team, so "done" is clearly testable from day one |
| **Daily Standup** | Reports blocking issues - e.g. a broken build, an environment problem, or a defect blocking further test execution |
| **Sprint Review** | Performs demo testing - validates the working software live, alongside the developer's demo, from a user's perspective |
| **Retrospective** | Contributes process improvement ideas - e.g. flags recurring flaky tests or suggests earlier QA involvement next sprint |

### 15. Shift-Left practices applied to the Course Management API

| Practice | Application |
|---|---|
| (a) Reviewing requirements for testability | QA reviews the "Add Course" user story upfront and asks: "what's the expected behavior for a duplicate course code?" - catching a gap before coding starts |
| (b) Writing test cases before code (TDD/BDD) | Write the Given-When-Then scenario for course creation before the endpoint is implemented, so the developer codes against a clear contract |
| (c) Static code analysis | Run a linter/type checker (e.g. mypy, flake8) on every commit via CI, catching bugs before the code even reaches a tester |
| (d) API contract testing before integration | Validate the OpenAPI/Swagger schema for /api/courses/ against a contract-testing tool before the frontend team starts building against it |

### 16. Acceptance Criteria in Given-When-Then (Gherkin)

**User Story:** As a college admin, I want to create a new course, so that students can enroll in it.

Scenario: Successfully create a new course (happy path)
  Given I am logged in as a college admin
  When I submit a course with a unique code, name, and credit count
  Then the course is created
  And I see a success confirmation
  And the course appears in the course listing

Scenario: Reject duplicate course code
  Given a course with code "CS101" already exists
  When I submit a new course with code "CS101"
  Then I see an error message indicating the course code is already in use
  And no new course is created

Scenario: Reject missing required fields
  Given I am logged in as a college admin
  When I submit a course form with the "name" field left blank
  Then I see a validation error indicating "name" is required
  And no course is created
'@ | Set-Content -Path written_exercises\v_model_analysis.md -Encoding UTF8
