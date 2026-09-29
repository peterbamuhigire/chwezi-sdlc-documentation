# diagram_trace fixtures (M10-07-T03)

Synthetic test material. `base/` is a minimal workspace with a registry. Each folder under `cases/` holds the IR files placed in `base/03-design-documentation/01-high-level-design/diagrams/` for one test; `valid` must raise no `diagram/*` finding and every other case must raise exactly the code it is named after.
