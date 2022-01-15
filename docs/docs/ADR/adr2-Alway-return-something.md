# Always return something

## Status

- ACCEPTED : [X]
- IMPLEMENTED: [X]
- DEPRECATED: [ ]


## Context

Issue : #6

The api must return an impact independently on the level of knowledge of the user. 
If a user send incomplete data the API **must** return an impact either with specific or default data completing the user request.

## Decision

Initial implementation

## Consequences

* Default data must exist for each data used in a workflow.