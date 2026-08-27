#!/usr/bin/env python3
"""
scripts/remediate_batch5_sota.py — Comprehensive Batch 5 Domain SOTA Elevation (ADR-034)
Injects React 19 RSC, WCAG 2.2 AAA math, Touch Target Geometry, Schema.org JSON-LD,
and System Usability Scale (SUS) into the 6 Frontend & UI/UX skills.
"""

from pathlib import Path

BATCH_5_DATA = {
    "react-best-practices": """
## Domain SOTA & Industry Engineering Standards

- **React 19 Architecture:** React Server Components (RSC), Server Actions (`'use server'`), and Client Boundaries (`'use client'`).
- **New Hooks & Primitives:** `use()` hook (promise & context unwrapping), `useActionState()`, `useOptimistic()`, and `useFormStatus()`.
- **Compiler & Memoization:** React Compiler automatic memoization (replacing manual `useMemo` / `useCallback` boilerplate).
- **Security & Data Boundaries:** Server Action argument sanitization, CSRF protection, and zero-bundle server logic.

### Server vs Client Boundary Architecture:

```text
Server Component (Default)                    Client Component ('use client')
      │                                                     │
      ├── Direct DB / Backend Data Access                   ├── Interactive State (useState, useReducer)
      ├── Zero Client JS Bundle Impact                      ├── DOM Event Handlers (onClick, onChange)
      └── Renders Static HTML Tree                          └── Browser APIs & Custom Hooks
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Default to Server Components):** Every component must remain a Server Component by default; add `'use client'` only to leaf components requiring interactive state or browser events.
2. **Rule of Thumb 2 (Server Action Parameter Validation):** All Server Actions must validate incoming parameters with a schema validator (Zod/Valibot) before executing mutations.
3. **Rule of Thumb 3 (Suspense Streaming with Skeleton Fallbacks):** Wrap async data-fetching Server Components in `<Suspense>` boundaries with layout-stable skeleton fallbacks.
4. **Rule of Thumb 4 (Optimistic UI Updates):** Mutating actions should use `useOptimistic()` to render instant UI transitions before server response resolves.
""",

    "ui-ux-pro-max": """
## Domain SOTA & Industry Engineering Standards

- **Accessibility & Contrast:** WCAG 2.2 AAA compliance, Relative Luminance mathematics ($C_{\\text{ratio}} \\ge 7:1$), and APCA (Accessible Perceptual Contrast Algorithm).
- **Modern Layout Engines:** CSS Grid Level 2 (Subgrid), Container Queries (`@container`), and CSS Anchor Positioning.
- **Design Tokens & Systems:** HSL tailored palettes, 8pt spatial grid, fluid typography with `clamp()`, and glassmorphism backdrop filters.
- **Micro-Interactions & Motion:** View Transitions API, CSS scroll-driven animations, and reduced-motion media queries (`prefers-reduced-motion: reduce`).

### WCAG 2.2 Luminance & Contrast Formula:

$$\\text{Contrast Ratio} = \\frac{L_1 + 0.05}{L_2 + 0.05} \\quad \\text{where } L_1 > L_2$$

| Compliance Level | Normal Text ($<18\\text{pt}$) | Large Text ($\\ge 18\\text{pt}$ / $24\\text{px}$) | UI Components / Icons |
|:---|:---:|:---:|:---:|
| **WCAG AA** | $\\ge 4.5:1$ | $\\ge 3.0:1$ | $\\ge 3.0:1$ |
| **WCAG AAA (Enhanced SOTA)** | $\\ge 7.0:1$ | $\\ge 4.5:1$ | $\\ge 4.5:1$ |

### Fluid Typography Clamp Equation:
`font-size: clamp(1rem, 0.75rem + 1.25vw, 1.75rem);`

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (WCAG 2.2 Contrast Mandate):** Body text must achieve at least $4.5:1$ (AA) and preferably $7.0:1$ (AAA) against its direct background color.
2. **Rule of Thumb 2 (Reduced Motion Invariant):** All CSS animations and smooth scrolls must provide a zero-animation fallback under `@media (prefers-reduced-motion: reduce)`.
3. **Rule of Thumb 3 (Subgrid Alignment):** Card lists and form rows with multi-column alignment must use CSS Subgrid to prevent visual misalignment.
4. **Rule of Thumb 4 (Keyboard Navigability):** All interactive elements must have visible, high-contrast focus rings (`:focus-visible`).
""",

    "mobile-design": """
## Domain SOTA & Industry Engineering Standards

- **Platform Guidelines:** Apple Human Interface Guidelines (HIG) and Google Material Design 3 (M3).
- **Ergonomics & Touch Targets:** Minimum $48 \\times 48\\text{dp}$ (Android) / $44 \\times 44\\text{pt}$ (iOS) interactive touch geometry with $8\\text{dp}$ minimum separation.
- **Navigation Topologies:** Bottom Navigation Bar, Modal Bottom Sheets, and Swipe-to-Dismiss gesture physics.
- **Offline-First Resilience:** Local-first reactive databases (WatermelonDB, PowerSync, SQLite) with optimistic offline mutations.

### Touch Target Geometry Invariant:

$$\\text{Width}_{\\text{touch}} \\ge 48\\text{dp}, \\quad \\text{Height}_{\\text{touch}} \\ge 48\\text{dp}, \\quad \\text{Spacing} \\ge 8\\text{dp}$$

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Thumb-Zone Priority):** Place primary actions (FABs, CTAs, Navigation) in the bottom $40\\%$ of the screen for natural one-handed reachability.
2. **Rule of Thumb 2 (Safe Area Insets):** Always respect hardware notches, home indicator bars, and dynamic islands via `safe-area-inset-*` CSS variables or SafeAreaView.
3. **Rule of Thumb 3 (Instant Offline Feedback):** When offline, display immediate optimistic UI state with subtle sync status indicators; never show a full-screen blocking error.
4. **Rule of Thumb 4 (Haptic Feedback):** Provide subtle tactile haptic feedback on destructive actions or critical state confirmations.
""",

    "seo-optimizer": """
## Domain SOTA & Industry Engineering Standards

- **Structured Data:** Schema.org JSON-LD `@graph` architectures (SoftwareApplication, TechArticle, Organization, BreadcrumbList).
- **Core Web Vitals (CWV):** Largest Contentful Paint (LCP $\\le 2.5\\text{s}$), Interaction to Next Paint (INP $\\le 200\\text{ms}$), Cumulative Layout Shift (CLS $\\le 0.1$).
- **Canonical & Crawlability:** Self-referential canonical URLs, automated XML sitemaps, robots.txt directives, and hreflang localization.
- **Social Graph Optimization:** Open Graph (`og:image`, `og:title`) and Twitter Cards (`summary_large_image`).

### Schema.org JSON-LD Technical Specification:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "SoftwareApplication",
      "name": "Ignite Agents Skills",
      "applicationCategory": "DeveloperApplication",
      "operatingSystem": "All",
      "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" }
    }
  ]
}
</script>
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Zero CLS on Images & Fonts):** All `<img>` tags must specify explicit `width` and `height` attributes and use `font-display: swap` to prevent layout shifts.
2. **Rule of Thumb 2 (Single H1 Tag):** Every web page must contain exactly one `<h1>` tag matching the primary search intent.
3. **Rule of Thumb 3 (Valid Structured Data):** Validate all JSON-LD payloads against Google Rich Results Test; zero schema syntax errors allowed.
4. **Rule of Thumb 4 (Meta Description Quality):** Meta descriptions must be between 120 and 160 characters, providing an actionable call to action.
""",

    "artifacts-builder": """
## Domain SOTA & Industry Engineering Standards

- **Single-File Architecture:** Fully self-contained HTML/CSS/JS bundles executable locally without build tools or npm dependencies.
- **Security & Sandboxing:** Strict Content Security Policy (CSP), zero external unsafe scripts, and local `iframe` isolation.
- **Modern Web APIs:** Native Web Components, Canvas 2D / WebGL rendering, CSS Grid & Custom Properties.
- **Reactive State Without Frameworks:** Lightweight Pub/Sub state machines and Proxy-based reactive data binding.

### Vanilla Reactive State Binding Pattern:

```javascript
const state = new Proxy({ count: 0 }, {
  set(target, key, value) {
    target[key] = value;
    document.querySelectorAll(`[data-bind="${key}"]`).forEach(el => el.textContent = value);
    return true;
  }
});
```

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Zero-Build Invariant):** The artifact must execute instantly by double-clicking the `.html` file in any modern browser without requiring `npm install` or local servers.
2. **Rule of Thumb 2 (Sandboxed Security):** Never load external third-party CDN scripts in artifacts; embed styles and scripts inline to guarantee portability and security.
3. **Rule of Thumb 3 (Responsive Fit):** The artifact must fluidly scale from mobile viewport ($360\\text{px}$) to ultra-wide desktop ($2560\\text{px}$).
4. **Rule of Thumb 4 (Rich Aesthetics):** Always use dark mode palettes, vibrant accent gradients, and micro-animations; plain default styling is strictly prohibited.
""",

    "ux-researcher-designer": """
## Domain SOTA & Industry Engineering Standards

- **Empirical Usability Metrics:** System Usability Scale (SUS), Single Ease Question (SEQ), and Task Completion Rate ($TCR \\ge 85\\%$).
- **Heuristic Evaluation:** Jakob Nielsen's 10 Usability Heuristics and Severity Rating (0 to 4).
- **Discovery Frameworks:** Jobs-to-be-Done (JTBD) Outcome-Driven Innovation and Double Diamond user discovery.
- **Information Architecture:** Tree Testing, Open/Closed Card Sorting, and User Journey Mapping.

### System Usability Scale (SUS) Score Equation:

$$\\text{SUS} = 2.5 \\times \\left( \\sum_{i \\in \\text{Odd}} (R_i - 1) + \\sum_{j \\in \\text{Even}} (5 - R_j) \\right) \\in [0, 100]$$

| SUS Score Range | Grade | Usability Quality |
|:---|:---:|:---|
| **$\\ge 80.3$** | **A** | World-Class / Highly Delightful |
| **$68.0 \\le \\text{SUS} < 80.3$** | **B / C** | Industry Average / Acceptable |
| **$< 68.0$** | **D / F** | Deficient / Critical Usability Friction |

### Exhaustive Heuristic Decision Rules:
1. **Rule of Thumb 1 (Five-User Usability Rule):** Testing 5 users uncovers $>85\\%$ of core usability problems (Nielsen Norman Group).
2. **Rule of Thumb 2 (SUS Target $\\ge 75$):** Any new workflow or redesign must achieve an empirical SUS score $\\ge 75$ before production sign-off.
3. **Rule of Thumb 3 (Observe Actions Over Words):** In user interviews, observe actual user behavior rather than relying on what users say they do.
4. **Rule of Thumb 4 (Visibility of System Status):** The interface must always keep users informed about what is happening through appropriate feedback within reasonable time ($T \\le 100\\text{ms}$).
"""
}

def main():
    root = Path(__file__).resolve().parent.parent
    skills_dir = root / "skills"
    
    for skill_name, sota_text in BATCH_5_DATA.items():
        skill_file = skills_dir / skill_name / "SKILL.md"
        if not skill_file.exists():
            print(f"[!] Skill file not found: {skill_file}")
            continue
            
        content = skill_file.read_text(encoding="utf-8")
        if "## Domain SOTA & Industry Engineering Standards" in content:
            print(f"[*] Already has SOTA standards: {skill_name}")
            continue
            
        if "## Operational Verification Checklist" in content:
            parts = content.split("## Operational Verification Checklist", 1)
            new_content = parts[0] + sota_text.strip() + "\n\n## Operational Verification Checklist" + parts[1]
        elif "## Completion Gate" in content:
            parts = content.split("## Completion Gate", 1)
            new_content = parts[0] + sota_text.strip() + "\n\n## Completion Gate" + parts[1]
        else:
            new_content = content + "\n\n" + sota_text.strip()
            
        skill_file.write_text(new_content, encoding="utf-8")
        print(f"[✓] Elevated Domain SOTA for: {skill_name}")

if __name__ == "__main__":
    main()
