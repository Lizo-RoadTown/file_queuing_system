# Curator-side diagrams

Mermaid source files for the diagrams in `../02_methodology.md`. Each `.mmd` file holds one diagram and can be edited or rendered independently of the prose.

| File | Concept | Diagram type |
|---|---|---|
| `01-hta.mmd` | Curator pair hierarchical task analysis | `flowchart TD` |
| `02-artifact-state.mmd` | Curation artifact state (draft, awaiting teammate verification, submitted) | `stateDiagram-v2` |
| `03-submission-sequence.mmd` | PR submission flow: validate, merge, seed issue, update CSV | `sequenceDiagram` |
| `04-layered-architecture.mmd` | Environment, drafting, submission interface | `flowchart TB` |

To render: paste the file's contents into [mermaid.live](https://mermaid.live), or use a Markdown viewer that supports Mermaid (GitHub, VS Code preview).
