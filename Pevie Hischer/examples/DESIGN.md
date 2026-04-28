---
version: alpha
name: Pevie Example Product
description: Example visual identity used to validate the Pevie DESIGN.md workflow.
colors:
  primary: "#102033"
  secondary: "#5B6472"
  tertiary: "#0E7490"
  neutral: "#F6F8FA"
  surface: "#FFFFFF"
  text: "#102033"
  text-muted: "#5B6472"
  border: "#D9E0E7"
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

Pevie Example Product is a calm operations dashboard for teams that need to scan status quickly and act with confidence. The visual direction is precise, quiet, and sturdy rather than decorative.

## Colors

Use deep ink for primary text, slate for metadata, cyan for primary action, and near-white neutrals for surfaces. Do not introduce purple-blue gradients, novelty accent colors, or low-contrast pastel controls.

## Typography

Inter is used throughout. Headings should be clear and compact. Body text should stay readable in dense panels, tables, and repeated operational workflows.

## Layout

Use predictable grids, restrained spacing, and stable dimensions for repeated controls. Dense work surfaces should prioritize scanning and comparison over marketing composition.

## Elevation & Depth

Prefer flat surfaces with borders. Use shadows only for active overlays, menus, or modal focus.

## Shapes

Use 4px to 12px radii. Avoid pill-heavy layouts unless the control is a compact status token or segmented option.

## Components

Buttons, cards, inputs, tables, loading states, empty states, and error states should use declared tokens and canonical spacing. Error and retry states should include clear next actions.

## Do's and Don'ts

Do:

- Keep operational surfaces quiet and scannable.
- Use cyan action color deliberately.
- Preserve stable dimensions for controls and repeated rows.

Don't:

- Use generic AI gradient backgrounds.
- Invent one-off card styles.
- Hide primary actions behind decorative layouts.
