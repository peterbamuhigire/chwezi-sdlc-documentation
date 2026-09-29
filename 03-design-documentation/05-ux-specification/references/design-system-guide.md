# Design System Guide Reference

## Design Token Taxonomy

Design tokens are the atomic values of a design system. The system shall organize tokens in three layers: Primitive, Semantic, and Component.

The design system shall be treated as a living product with an explicit source of truth.
The specification shall identify where canonical component definitions live and how documentation stays aligned with implementation.

### Color Tokens

**Layer 1 -- Primitives (Palette):**
Raw color values. These shall never be referenced directly in component code.

```
color-blue-50:  #EFF6FF
color-blue-100: #DBEAFE
color-blue-500: #3B82F6
color-blue-700: #1D4ED8
color-blue-900: #1E3A5A
color-gray-50:  #F9FAFB
color-gray-100: #F3F4F6
color-gray-500: #6B7280
color-gray-900: #111827
color-red-500:  #EF4444
color-green-500:#22C55E
color-yellow-500:#EAB308
```

**Layer 2 -- Semantic (Purpose):**
Named by function. Components reference these tokens.

```
color-action-primary:    {color-blue-500}
color-action-secondary:  {color-gray-500}
color-action-destructive:{color-red-500}
color-feedback-success:  {color-green-500}
color-feedback-warning:  {color-yellow-500}
color-feedback-error:    {color-red-500}
color-text-primary:      {color-gray-900}
color-text-secondary:    {color-gray-500}
color-text-inverse:      {color-gray-50}
color-bg-primary:        #FFFFFF
color-bg-secondary:      {color-gray-50}
color-bg-overlay:        rgba(0,0,0,0.5)
color-border-default:    {color-gray-100}
color-border-focus:      {color-blue-500}
```

**Layer 3 -- Component (Scoped):**
Bound to specific component states.

```
button-primary-bg:       {color-action-primary}
button-primary-bg-hover: {color-blue-700}
button-primary-text:     {color-text-inverse}
input-border-default:    {color-border-default}
input-border-focus:      {color-border-focus}
input-border-error:      {color-feedback-error}
```

### Typography Scale

The system shall define a modular type scale. Recommended ratio: 1.25 (Major Third).

| Token | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| `type-display` | 36px | 700 | 1.2 | Page titles, hero text |
| `type-h1` | 30px | 700 | 1.25 | Section headings |
| `type-h2` | 24px | 600 | 1.3 | Subsection headings |
| `type-h3` | 20px | 600 | 1.35 | Card titles, group labels |
| `type-body` | 16px | 400 | 1.5 | Default body text |
| `type-body-sm` | 14px | 400 | 1.5 | Secondary text, table cells |
| `type-caption` | 12px | 400 | 1.4 | Labels, helper text, timestamps |
| `type-code` | 14px | 400 (mono) | 1.6 | Code snippets, technical values |

**Font Families:**
- Primary and monospace families are chosen through the `chwezi-design-engine` engine (`skills/01-typography-and-fonts/`), which owns typeface selection and the banned-font list. The UX specification records the chosen family, its licence, fallback stack and the reason for the choice as a requirement; it does not default to a bare system stack or a banned face (Inter, Roboto, Arial, Open Sans, Lato, Geist, Space Grotesk) as primary type.
- Record which scale values above are placeholders until the design engine confirms them; render and device proof stays `NOT_ASSESSED` until performed.

### Spacing Scale

The system shall use a 4px base unit. All spacing values shall be multiples of 4px.

| Token | Value | Common Usage |
|-------|-------|-------------|
| `space-2xs` | 2px | Micro-adjustments (icon-to-text gap) |
| `space-xs` | 4px | Tight padding (badges, tags) |
| `space-sm` | 8px | Inner padding (buttons, inputs) |
| `space-md` | 16px | Default content padding, gap between form fields |
| `space-lg` | 24px | Section padding, card padding |
| `space-xl` | 32px | Major section gaps |
| `space-2xl` | 48px | Page-level vertical spacing |
| `space-3xl` | 64px | Hero sections, major separators |
| `space-4xl` | 96px | Full-bleed section spacing |

### Elevation / Shadow Levels

| Level | CSS Box-Shadow | Usage |
|-------|---------------|-------|
| 0 | none | Flat elements, inline content |
| 1 | `0 1px 2px rgba(0,0,0,0.05)` | Cards, list items on hover |
| 2 | `0 4px 6px rgba(0,0,0,0.07)` | Dropdowns, popovers |
| 3 | `0 10px 15px rgba(0,0,0,0.10)` | Modals, dialogs |
| 4 | `0 20px 25px rgba(0,0,0,0.15)` | Notifications, toasts |
| 5 | `0 25px 50px rgba(0,0,0,0.25)` | Full-screen overlays |

## Component Documentation Template

For each component in the design system, the system shall produce documentation following this structure:

### Component: [ComponentName]

**Description:** One-sentence purpose statement.

**Anatomy:** Named sub-parts of the component (container, label, helper text, icon, action area, etc.).

**Variants:**

| Variant | Visual Appearance | Use Case |
|---------|-------------------|----------|
| Primary | Filled background, high contrast | Primary actions (Save, Submit) |
| Secondary | Outlined, medium contrast | Secondary actions (Cancel, Back) |
| Ghost | Text-only, no background | Tertiary actions, inline links |
| Destructive | Red-toned, warning emphasis | Irreversible actions (Delete, Remove) |

**Required State Coverage:**

- default
- hover
- focus
- active
- disabled
- loading
- error
- success where applicable

**Usage Guidelines:**

- when to use
- when not to use
- whether a new request should extend this component or justify a new one

**Ownership And Governance:**

- owner
- contribution path
- deprecation note if replacing an older pattern

## Governance Expectations

The specification should define one of these team models explicitly:

- centralized ownership
- federated contribution with central review
- hybrid model

Unstated ownership creates drift.

**States:**

| State | Appearance Change | Trigger |
|-------|-------------------|---------|
| Default | Base appearance | None |
| Hover | Background darkens 10% | Mouse enter |
| Focus | 2px outline using `color-border-focus` | Tab or click |
| Active | Background darkens 15% | Mouse down |
| Disabled | 50% opacity, cursor: not-allowed | `disabled` prop |
| Loading | Content replaced with spinner, width preserved | `loading` prop |

**Props:**

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| variant | `'primary' \| 'secondary' \| 'ghost' \| 'destructive'` | `'primary'` | Visual variant |
| size | `'sm' \| 'md' \| 'lg'` | `'md'` | Size preset |
| disabled | `boolean` | `false` | Disables interaction |
| loading | `boolean` | `false` | Shows loading state |

**Do / Don't:**
- DO use a single primary action per view context.
- DO NOT use destructive variant for reversible actions.
- DO provide a visible label; icon-only buttons shall include `aria-label`.

**Accessibility:**
- Role: `button` (native `<button>` element preferred).
- Keyboard: `Enter` and `Space` shall activate. `Tab` shall focus.
- Screen Reader: Label shall announce the action. Loading state shall announce "Loading" via `aria-live`.

## Pattern Documentation

### Layout Patterns

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| Dashboard | KPI row + chart area + activity feed | Overview screens |
| List-Detail | Split pane (list left, detail right) or stacked (mobile) | Entity management |
| Master-Detail | Persistent master list with inline detail panel | Email, messaging |
| Full-Screen Modal | Overlay with scrollable content area | Complex forms, wizards |
| Split View | Equal or weighted columns for comparison | Side-by-side editing |

### Form Patterns

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| Single-Page Form | All fields visible, single submit | Short forms (login, contact) |
| Multi-Step Wizard | Step indicator + one group per step + navigation | Long forms (onboarding, checkout) |
| Inline Editing | Click-to-edit fields within a detail view | Quick updates to existing records |
| Search with Filters | Search bar + filter panel (sidebar or dropdown) | List refinement |

### Data Display Patterns

| Pattern | Structure | Use Case |
|---------|-----------|----------|
| Data Table | Sortable columns, pagination, row actions | Structured tabular data |
| Card Grid | Responsive grid of cards with image + metadata | Visual catalog, gallery |
| Timeline | Chronological vertical list with timestamps | Activity log, history |
| Tree View | Expandable/collapsible hierarchy | File systems, org charts |
