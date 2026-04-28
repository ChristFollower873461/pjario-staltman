---
version: alpha
name: Ledger Desk
description: Quiet operational UI for finance teams reviewing account health.
colors:
  primary: "#162033"
  secondary: "#576071"
  tertiary: "#0F766E"
  neutral: "#F7F9FB"
  surface: "#FFFFFF"
  text: "#162033"
  text-muted: "#667085"
  border: "#D8DEE8"
  success: "#047857"
  warning: "#B45309"
  danger: "#B91C1C"
  on-tertiary: "#FFFFFF"
typography:
  h1:
    fontFamily: Inter
    fontSize: 2rem
    fontWeight: 700
    lineHeight: 1.15
  h2:
    fontFamily: Inter
    fontSize: 1.375rem
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

Ledger Desk is a dense operational tool for finance teams checking account health. The UI should feel calm, exact, and accountable: more control room than marketing page.

## Colors

Use deep ink for persistent structure and text, teal for the primary action, warm warning and danger only for state. Avoid blue-purple gradients, decorative color fields, and low-contrast badges.

## Typography

Inter carries the whole interface. Headings should be compact and scannable. Numeric/account values should stay aligned and easy to compare.

## Layout

Use a restrained grid with stable card and row heights. Keep the primary action visible, keep filters close to results, and avoid oversized hero-style treatment inside the product surface.

## Elevation & Depth

Default to flat surfaces with borders. Use shadow only for overlays, menus, and modal focus.

## Shapes

Use 4px to 12px radii. Do not use large pill cards or novelty rounded containers for core account data.

## Components

Status panels should show loading, empty, error, and success states. Cards use declared spacing and border tokens. Buttons use the primary teal action token and include accessible labels.

## Do's and Don'ts

Do:

- Make account health status immediately scannable.
- Keep controls stable when values load or change.
- Use declared status colors only for meaningful state.

Don't:

- Use generic dashboard card mosaics without hierarchy.
- Hide error recovery.
- Introduce new colors or component variants without updating DESIGN.md.
