# Design System Specification: The Kinetic Explorer

This design system is built to transform complex logistical data into an inspiring, editorial-grade travel experience. We move beyond the "utility app" aesthetic, treating the UI as a **Kinetic Explorer**—a living, breathing graph of human experience that balances tech-forward precision with the expansive soul of global travel.

## 1. Creative North Star: The Intelligent Cartographer
The design system is guided by "The Intelligent Cartographer." This means every layout should feel like a custom-mapped journey. We avoid rigid, "boxed-in" templates in favor of **Intentional Asymmetry** and **Tonal Depth**. By overlapping high-definition travel photography with precision data visualizations, we create a sense of movement and connection. 

The goal is to make the user feel like they are not just looking at a database, but navigating a sophisticated, interconnected world of possibilities.

---

## 2. Colors & Surface Philosophy
Our palette utilizes Deep Action Blues and Nature Greens to signify trust and adventure. However, the premium feel is achieved not through the colors themselves, but through how they are layered.

### The "No-Line" Rule
Standard UI relies on 1px borders to separate content. **In this system, 1px solid borders are strictly prohibited for sectioning.** Boundaries must be defined through:
- **Background Transitions:** Use a shift from `surface` to `surface_container_low` to define a new region.
- **Negative Space:** Use the Spacing Scale (specifically `8` to `12`) to create clear cognitive breaks.

### Surface Hierarchy & Nesting
Treat the UI as a physical stack of semi-transparent layers.
- **Base Layer:** `surface` (#f9f9ff) for the widest areas.
- **Content Plates:** `surface_container_low` for primary content areas.
- **Elevated Insights:** `surface_container_highest` for cards or interactive modules.
Each "inner" container should move up or down one tier in the surface scale to create a "nested" depth that feels organic rather than mechanical.

### The "Glass & Gradient" Rule
To inject "soul" into the tech-forward aesthetic:
- **Glassmorphism:** Use semi-transparent `surface_container_lowest` with a `backdrop-blur` (20px-40px) for floating navigation or overlays.
- **Signature Gradients:** Main Action buttons and Hero sections should utilize a subtle linear gradient (135°) from `primary` (#003d9b) to `primary_container` (#0052cc). This prevents the "flat" look of low-end SaaS products.

---

## 3. Typography: The Editorial Voice
We use a high-contrast typographic pairing to balance technical reliability with an adventurous spirit.

*   **Display & Headlines (Plus Jakarta Sans):** Used for "The Hook." These should be bold, expansive, and clean. Use `display-lg` for hero moments to create an editorial, magazine-like feel.
*   **Body & Labels (Inter):** Our workhorse. It provides a "tech-forward" and highly legible foundation for itineraries, flight data, and logistical details.

**Hierarchy Strategy:** 
- Use `display-sm` for section headers, paired with `label-md` in all-caps (letter-spacing: 0.05rem) as an eyebrow tag.
- Maintain a minimum of `1.4rem` (4) spacing between headlines and body text to allow the typography to "breathe."

---

## 4. Elevation & Depth
We eschew traditional drop shadows for **Tonal Layering**.

*   **The Layering Principle:** Depth is achieved by "stacking." A `surface_container_lowest` card sitting on a `surface_container_low` background creates a natural lift.
*   **Ambient Shadows:** If a floating element (like a modal) is required, use an extra-diffused shadow: `box-shadow: 0 20px 40px rgba(4, 27, 60, 0.06)`. Note the use of the `on-surface` color (#041b3c) at a very low opacity to mimic natural light.
*   **The "Ghost Border" Fallback:** If accessibility requires a stroke, use a "Ghost Border": the `outline_variant` token at 15% opacity. Never use 100% opaque borders.

---

## 5. Components

### Buttons
- **Primary:** Gradient from `primary` to `primary_container`, `DEFAULT` (8px) rounded corners, `label-md` weight.
- **Secondary:** Transparent background with a `Ghost Border`. Use `primary` for the text color.
- **Tertiary:** No background or border. Use `primary` text with a subtle underline or arrow icon to indicate direction.

### Cards & Lists
- **Rule:** No divider lines. 
- **Execution:** Separate list items using `surface_container_low` as a background hover state. Use the `spacing-3` value between vertical content blocks. 
- **Visual Accent:** For TravelGraph-specific cards, incorporate a "Node & Edge" motif in the corner of the card using a subtle `outline_variant` stroke at 10% opacity.

### Navigation & Tooltips
- **Glassmorphism:** Navigation bars should use `surface_container_lowest` at 80% opacity with a heavy backdrop blur.
- **Tooltips:** Use `inverse_surface` with `inverse_on_surface` text for high-contrast data callouts on maps.

### Input Fields
- Avoid boxed inputs. Use a subtle background shift (`surface_container_high`) with a bottom-only 2px focus state in `primary`. This maintains the clean, "map-like" aesthetic.

---

## 6. Do’s and Don’ts

### Do:
- **Use Intentional Asymmetry:** Let images bleed off the edge of the container or overlap text to create a sense of "adventure."
- **Leverage Whitespace:** Treat whitespace as a luxury. Use `16` and `20` spacing tokens to separate major content themes.
- **Incorporate "Graph" Accents:** Use subtle node-and-edge patterns (0.5pt lines) in the background of data-heavy sections to reinforce the platform's connectivity.

### Don’t:
- **Don't use dividers:** Never use a `<hr>` or a 1px border to separate list items. Use spacing or tonal shifts.
- **Don't use generic shadows:** Avoid the default "black" drop shadow. Always tint shadows with the `on_surface` color for a high-end feel.
- **Don't crowd the imagery:** High-quality photography needs space. Ensure text overlays have enough `backdrop-filter` or a gradient scrim to ensure the `display-lg` typography remains the hero.
- **Don't use "Full" rounding for everything:** Reserve `rounded-full` for chips and pills. Use the `DEFAULT` (8px) or `lg` (16px) for cards to maintain a structured, "smart" feel.