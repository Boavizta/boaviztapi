# Contribution tl;dr

Check this points if you want to do a pull request :

 * [ ] Is my code written in [PEP8](https://www.python.org/dev/peps/pep-0008/)?
 * [ ] Are the tests passing (`make test`)?
 * [ ] Is my feature or bug fix unit tested?
 * [ ] Does each of my commits represent an atomic functionality or bug fix?
 * [ ] Is my feature or bug fix related to an issue?
 * [ ] Are the pre-commit checks set up and passing (`make pre-commit-install pre-commit`)?

# Code organization

We tried to keep the code organization as simple as possible. Here is an overview of the main folders:

```mermaid
flowchart TD
	A[boaviztapi/]
	A --> B[routers/]
	A --> C[dto/]
	A --> D[models/]
	A --> E[data/]
	A --> F[compute/]

	B --> B1[API routes and OpenAPI docs in openapi_doc/]
	C --> C1[input/output schemas and mapping helpers at API boundaries]
	D --> D1[core domain models and business logic for impact computation]
	E --> E1[data access helpers and reference datasets]
	F --> F1[computation orchestration and verbose result formatting]
```

# Tests organization

The test tree mirrors the source tree. Add new tests in the matching folder so navigation stays predictable.

```mermaid
flowchart TD
	S[boaviztapi/] --> SR[routers/]
	S --> SD[dto/]
	S --> SM[models/]
	S --> SDA[data/]
	S --> SC[compute/]
	S --> SU[utils/]

	T[tests/] --> TA[api/]
	T --> TU[unit/]
	T --> TD[data/]
	T --> TC[conftest.py]

	SR -. endpoint tests .-> TA
	SD -. unit tests .-> TU1[unit/dto/]
	SM -. unit tests .-> TU2[unit/compute/models/]
	SDA -. fixtures + test datasets .-> TD
	SC -. unit tests .-> TU3[unit/compute/]
	SU -. unit tests .-> TU4[unit/utils/]
```

Some rules:

* Add as many tests as possible when contributing. For example, if you are fixing a bug, add the bug report as a new test case.
* For a source module under `boaviztapi/<area>/...`, create tests under `tests/unit/<area>/...`. 
* API behavior for routers belongs in `tests/api/`.
* Test-only datasets and fixtures go in `tests/data/`.
* Keep test filenames aligned with source behavior (for example `test_<feature>.py`).
