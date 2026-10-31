# Design Handoff Reference

## Annotation Standards

### Spacing Annotations

The system shall annotate spacing using design token names, not raw pixel values.

**Correct:**
```
Padding: space-lg (24px)
Gap between items: space-md (16px)
Margin top: space-xl (32px)
```

**Incorrect:**
```
Padding: 24px
Gap between items: 16px
Margin top: 32px
```

The pixel value may appear in parentheses for developer convenience, but the token name shall be the primary reference. If the design system token values change, the implementation shall update automatically through the token system.

### Color Annotations

The system shall reference semantic color tokens, not hex codes or RGB values.

**Correct:**
```
Background: color-action-primary
Text: color-text-inverse
Border: color-border-focus
```

**Incorrect:**
```
Background: #3B82F6
Text: #FFFFFF
Border: #3B82F6
```

### Interaction State Documentation

For every interactive component, the system shall annotate all applicable states:

| State | Required Annotations |
|-------|---------------------|
| Default | Background color token, text color token, border style, shadow level |
| Hover | Background change (token reference), cursor style, transition duration |
| Focus | Outline style (color token, width, offset), box-shadow if applicable |
| Active | Background change (token reference), scale transform if applicable |
| Disabled | Opacity value, cursor style (`not-allowed`), tooltip explaining why |
| Loading | Spinner/skeleton placement, width preservation rule, aria-live announcement |
| Error | Border color token (`color-feedback-error`), error message placement, icon |

The handoff shall make it clear whether the documented state behavior is the canonical source or whether implementation tokens/components own the final truth.
If implementation is canonical, the handoff shall reference that source directly.

### Responsive Behavior Annotations

For each screen or component, the system shall document layout changes at each breakpoint:

| Breakpoint | Layout Change | Notes |
|------------|--------------|-------|
| Mobile (320-767px) | Single column, stacked elements, hamburger menu | Touch targets >= 44px |
| Tablet (768-1023px) | Two-column where applicable, collapsible sidebar | Adapt table to scrollable |
| Desktop (1024px+) | Full multi-column layout, persistent navigation | Hover states active |

## Asset Delivery Requirements

### Format Specifications

| Asset Type | Primary Format | Fallback Format | Why |
|------------|---------------|-----------------|-----|
| Icons | SVG | PNG @2x | SVG for scalability and color manipulation via CSS |
| Illustrations | SVG | PNG @2x | SVG for responsive scaling; PNG fallback for complex illustrations |
| Photographs | WebP | JPEG | WebP for smaller file size; JPEG for browser compatibility |
| Logos | SVG | PNG @2x (transparent) | SVG for crisp rendering at any size |
| Favicons | SVG + ICO | PNG 32x32, 180x180 | Multi-format for cross-browser and device support |

### Naming Convention

The system shall enforce a consistent asset naming scheme:

```
{type}-{name}-{variant}-{size}.{ext}
```

**Examples:**
```
icon-search-default-24.svg
icon-search-active-24.svg
icon-close-default-16.svg
illustration-empty-state-orders.svg
photo-hero-landing-desktop.webp
photo-hero-landing-mobile.webp
logo-full-color.svg
logo-monochrome-white.svg
```

**Rules:**
- All lowercase, hyphen-separated.
- No spaces or special characters.
- Size suffix for icons (16, 20, 24, 32, 48).
- Variant suffix for state-dependent assets (default, active, disabled).
- Context suffix for responsive assets (mobile, tablet, desktop).

### Resolution Requirements

| Device Category | Scale Factor | Delivery Requirement |
|----------------|-------------|---------------------|
| Standard displays | 1x | Base resolution |
| High-DPI displays (Retina) | 2x | 2x resolution for raster assets |
| Ultra-high-DPI | 3x | 3x resolution for mobile app icons and key imagery |
| Vector assets | n/a | SVG preferred; no raster scaling needed |

## Developer Acceptance Criteria Template

For each screen or component delivered in the handoff, the system shall define acceptance criteria:

### Source Of Truth Parity

- The delivered screen uses documented tokens rather than ad hoc raw values.
- Shared components match the current design-system documentation.
- Any intentional deviation is listed explicitly with approval owner and remediation plan.

### Visual Fidelity

| Criterion | Threshold | Verification Method |
|-----------|-----------|---------------------|
| Layout accuracy | Within 2px of design specification | Visual diff tool (Percy, Chromatic, or manual overlay) |
| Color accuracy | Exact token match (no hard-coded hex values) | Code review: grep for hex values outside token definitions |
| Typography accuracy | Correct token for family, size, weight, line-height | Code review: verify token usage |
| Spacing accuracy | Correct token for all margins, paddings, gaps | Code review: verify token usage |
| Icon rendering | Correct icon, correct size, correct color token | Visual inspection at 1x and 2x |

### Interaction Fidelity

| Criterion | Threshold | Verification Method |
|-----------|-----------|---------------------|
| Hover state | Matches design spec within 50ms timing tolerance | Manual interaction test |
| Focus state | Visible focus ring using correct token | Keyboard tab-through test |
| Active state | Matches design spec | Manual click/tap test |
| Disabled state | Correct opacity, cursor, tooltip | Manual test with disabled prop |
| Loading state | Correct spinner/skeleton, width preserved | Manual test with loading prop |
| Transition timing | Within 50ms of specified duration | DevTools animation inspection |

### Responsive Fidelity

| Criterion | Threshold | Verification Method |
|-----------|-----------|---------------------|
| Mobile layout (320px) | No horizontal scroll, single column, touch targets >= 44px | Device testing or responsive mode |
| Mobile layout (767px) | Breakpoint transition is smooth, no layout jump | Browser resize test |
| Tablet layout (768px) | Correct column adaptation, navigation state | Device testing or responsive mode |
| Desktop layout (1024px) | Full layout renders correctly | Standard desktop browser |
| Desktop layout (1440px+) | Content width constrained, no excessive stretching | Wide viewport test |

### Accessibility Fidelity

| Criterion | Standard | Verification Method |
|-----------|----------|---------------------|
| Color contrast | >= 4.5:1 normal text, >= 3:1 large text | axe-core or Lighthouse audit |
| Keyboard navigation | All interactive elements reachable and operable | Manual keyboard walkthrough |
| Screen reader | Labels, roles, and live regions correct | NVDA or VoiceOver test |
| Focus order | Logical tab sequence matching visual layout | Manual keyboard walkthrough |
| Reduced motion | Animations disabled when `prefers-reduced-motion: reduce` | OS setting toggle test |

## Implementation Verification Checklist

The system shall provide this checklist for each component or screen after implementation:

- [ ] All design tokens consumed from the shared token system (no hard-coded values).
- [ ] Visual appearance matches high-fidelity design at all three breakpoints.
- [ ] All interactive states implemented (default, hover, focus, active, disabled, loading).
- [ ] Transitions and animations match specified timing and easing.
- [ ] WCAG 2.2 AA automated audit passes (axe-core or Lighthouse score >= 90).
- [ ] Keyboard navigation functions correctly for all interactive elements.
- [ ] Screen reader announces labels, roles, and state changes correctly.
- [ ] Assets use correct format, naming convention, and resolution.
- [ ] Responsive layout adapts correctly at mobile, tablet, and desktop breakpoints.
- [ ] `prefers-reduced-motion` disables non-essential animations.
- [ ] Component props match the design system specification.
- [ ] Edge cases handled (empty states, error states, loading states, long content).
