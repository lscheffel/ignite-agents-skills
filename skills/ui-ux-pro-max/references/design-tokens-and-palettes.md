# UI/UX Pro Max — Design Tokens, Style Guides & Palette Catalogs

> 💡 **Lazy Loading Reference:** This document contains the comprehensive hexadecimal palette catalog, CSS/Tailwind design token specifications, typography scales, and component snippets for support of the `ui-ux-pro-max` skill.

---

## 1. Color Palette Catalog by Domain

### 1.1 SaaS & Enterprise B2B (Clean & Slate)
```css
:root {
  --color-brand-primary: #2563eb;       /* Blue 600 */
  --color-brand-primary-hover: #1d4ed8; /* Blue 700 */
  --color-brand-secondary: #0f172a;     /* Slate 900 */
  
  --color-bg-canvas: #f8fafc;           /* Slate 50 */
  --color-bg-surface: #ffffff;
  --color-border-subtle: #e2e8f0;       /* Slate 200 */
  
  --color-text-primary: #0f172a;        /* Slate 900 */
  --color-text-secondary: #64748b;      /* Slate 500 */
  --color-text-muted: #94a3b8;          /* Slate 400 */
}
```

### 1.2 Dark Mode OLED-Safe
```css
[data-theme="dark"] {
  --color-bg-canvas: #090a0f;           /* Deep Black / OLED Safe */
  --color-bg-surface: #131722;          /* Elevated Surface */
  --color-border-subtle: #232a3b;
  
  --color-text-primary: #f1f5f9;        /* Slate 100 */
  --color-text-secondary: #94a3b8;      /* Slate 400 */
  --color-text-muted: #64748b;          /* Slate 500 */
  
  --color-brand-primary: #3b82f6;       /* Desaturated Blue 500 */
}
```

---

## 2. Spacing and Typography Scale Tokens

```css
:root {
  /* Typography Scale */
  --font-sans: 'Inter', system-ui, -apple-system, sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  
  --text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
  --text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
  --text-base: clamp(1rem, 0.95rem + 0.25vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.6vw, 1.25rem);
  --text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);
  --text-2xl: clamp(1.5rem, 1.3rem + 1vw, 2rem);
  
  /* Grid System & Spacing (8pt Grid) */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-12: 3rem;    /* 48px */
  
  /* Border Radii */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 0.75rem;
  --radius-full: 9999px;
}
```

---

## 3. Visual Style Snippets

### 3.1 Glassmorphism & Backdrop Blur
```css
.glass-panel {
  background: rgba(255, 255, 255, 0.65);
  backdrop-filter: blur(12px) saturate(180%);
  -webkit-backdrop-filter: blur(12px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
}

[data-theme="dark"] .glass-panel {
  background: rgba(19, 23, 34, 0.75);
  border: 1px solid rgba(255, 255, 255, 0.08);
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}
```

---

## 4. Accessibility Matrix WCAG 2.1 AA / AAA

- **Normal Text Contrast:** Minimum 4.5:1 (AA) / 7.0:1 (AAA).
- **Large Text Contrast (18pt+ / 14pt Bold):** Minimum 3.0:1 (AA) / 4.5:1 (AAA).
- **Touch Target:** Minimum of 44x44 CSS pixels for all buttons and clickable areas.
- **Visible Focus:** All interactive elements must have visible outline (`focus-visible: ring-2 ring-offset-2`).