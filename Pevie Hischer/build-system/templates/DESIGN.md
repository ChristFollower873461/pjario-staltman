---
version: alpha
name: Replace With Product Name
description: Agent-readable visual identity for frontend implementation and review.
colors:
  primary: "#111827"
  secondary: "#4B5563"
  tertiary: "#2563EB"
  neutral: "#F9FAFB"
  surface: "#FFFFFF"
  text: "#111827"
  text-muted: "#6B7280"
  border: "#E5E7EB"
  success: "#047857"
  warning: "#B45309"
  danger: "#B91C1C"
  on-tertiary: "#FFFFFF"
typography:
  h1:
    fontFamily: Inter
    fontSize: 2.25rem
    fontWeight: 700
    lineHeight: 1.15
  h2:
    fontFamily: Inter
    fontSize: 1.5rem
    fontWeight: 650
    lineHeight: 1.25
  body-md:
    fontFamily: Inter
    fontSize: 1rem
    fontWeight: 400
    lineHeight: 1.5
  label:
    fontFamily: Inter
    fontSize: 0.875rem
    fontWeight: 600
    lineHeight: 1.3
rounded:
  sm: 4px
  md: 8px
  lg: 12px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
components:
  page:
    backgroundColor: "{colors.neutral}"
    textColor: "{colors.text}"
  app-header:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.surface}"
    padding: "{spacing.md}"
  button-primary:
    backgroundColor: "{colors.tertiary}"
    textColor: "{colors.on-tertiary}"
    rounded: "{rounded.md}"
    padding: "10px 16px"
  card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.lg}"
    padding: "{spacing.lg}"
  divider:
    backgroundColor: "{colors.border}"
    height: 1px
  status-muted:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-muted}"
  status-info:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.secondary}"
  status-success:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.success}"
  status-warning:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.warning}"
  status-danger:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.danger}"
---

## Overview

This file is the product taste contract for frontend agents and reviewers. Replace the starter values before production use, then keep the file short enough to read before every non-trivial UI change.

State the product, audience, job-to-be-done, and emotional posture in two or three concrete sentences. Name any reference products or screenshots that define the target quality bar.

## Colors

Describe how each token should be used. Be explicit about interaction colors, semantic colors, neutral surfaces, and colors that are forbidden or reserved.

- **Primary:** Core text, persistent navigation, and high-emphasis structure.
- **Secondary:** Metadata, supporting labels, dividers, and lower-emphasis UI.
- **Tertiary:** Primary action and active state.
- **Neutral/surface:** Page backgrounds and content surfaces.

## Typography

Document the type hierarchy and when to use each level. Include any rules for numbers, dense data, labels, empty states, and marketing or editorial copy.

## Layout

Define spacing rhythm, responsive behavior, max content widths, grid rules, and how dense operational surfaces differ from lighter editorial or onboarding surfaces.

## Elevation & Depth

Describe when surfaces may use borders, shadows, translucency, or depth. Prefer restrained elevation unless the product explicitly calls for a more expressive visual language.

## Shapes

State border-radius rules and component shape expectations. Name exceptions clearly so agents do not invent one-off rounded styles.

## Components

List canonical components and expected states: buttons, cards, inputs, navigation, modals, tables, lists, loading, empty, error, and retry states.

## Do's and Don'ts

Do:

- Use declared tokens or explain why a new token/component is needed.
- Preserve the brand and tone posture.
- Cover loading, empty, error, and success states when relevant.
- Compare implementation screenshots against reference direction.

Don't:

- Rely on color alone for meaning.
- Introduce one-off colors, spacing, typography, or component forks without justification.
- Use generic AI defaults when the product has a defined visual language.
