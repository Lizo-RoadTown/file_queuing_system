# Reviewer-side diagrams

Mermaid source files for the diagrams in `../02_methodology.md`. Each `.mmd` file holds one diagram and can be edited or rendered independently of the prose.

| File | Concept | Diagram type |
|---|---|---|
| `01-hta.mmd` | Reviewer 2 hierarchical task analysis | `flowchart TD` |
| `02-state-machine.mmd` | Issue label state machine | `stateDiagram-v2` |
| `03a-approve-sequence.mmd` | Happy path: `/approve` direct to complete | `sequenceDiagram` |
| `03b-dispute-sequence.mmd` | Dispute branch: `/dispute` followed by `/complete`, `/reject`, or `/reopen` | `sequenceDiagram` |
| `04-layered-architecture.mmd` | UI layer, orchestration layer, data layer | `flowchart TB` |

To render: paste the file's contents into [mermaid.live](https://mermaid.live), or use a Markdown viewer that supports Mermaid (GitHub, VS Code preview).
