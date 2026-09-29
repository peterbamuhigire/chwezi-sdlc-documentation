# Malformed Fixture

## Broken diagram

```mermaid
%% alt: A deliberately malformed flowchart used to prove the build fails.
flowchart LR
  A[Start --> B{{unclosed
  B -->|yes C
```
