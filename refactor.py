import os
import re

css_content = """
:root {
  /* Typography */
  --font-sans: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
  --text-xs: 0.75rem;
  --text-sm: 0.875rem;
  --text-base: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.25rem;
  --text-2xl: 1.5rem;
  --text-3xl: 2rem;
  --text-4xl: 2.75rem;

  /* Spacing - Fibonacci/Golden Ratio modular scale */
  --s1: 0.25rem;   /* 4px */
  --s2: 0.5rem;    /* 8px */
  --s3: 0.75rem;   /* 12px */
  --s4: 1rem;      /* 16px */
  --s5: 1.618rem;  /* ~26px - RSB Base */
  --s6: 2.618rem;  /* ~42px - VOID Base */
  --s7: 4.236rem;  /* ~68px */
  --s8: 6.854rem;  /* ~110px */

  /* Radii */
  --radius-sm: 0.25rem;
  --radius-md: 0.5rem;
  --radius-lg: 1rem;
  --radius-xl: 1.5rem;
  --radius-full: 9999px;

  /* Z-index */
  --z-base: 0;
  --z-sticky: 200;

  /* Premium Dark Tech Palette */
  --color-bg: #03070E;
  --color-bg-soft: #080E18;
  --color-surface: #0E1624;
  --color-surface-raised: #141F31;
  --color-surface-soft: #19273D;
  --color-border: rgba(255, 255, 255, 0.08);
  --color-border-soft: rgba(255, 255, 255, 0.04);
  --color-text-primary: #F0F4F8;
  --color-text-secondary: #A0B2C6;
  --color-text-muted: #6A819C;
  --color-primary: #38BDF8;
  --color-primary-soft: rgba(56, 189, 248, 0.12);
  --color-success: #34D399;
  --color-warning: #FBBF24;
  --color-error: #F87171;
  --color-violet: #A78BFA;

  /* Shadows */
  --shadow-sm: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
  --shadow-md: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.2);
  --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.3);
}

/* === RESET / BASE === */
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
body {
  margin: 0;
  min-height: 100vh;
  background:
    radial-gradient(circle at 12% 0%, rgba(56,189,248,0.06), transparent 32rem),
    linear-gradient(135deg, var(--color-bg-soft), var(--color-bg));
  color: var(--color-text-primary);
  font-family: var(--font-sans);
  font-size: var(--text-base);
  line-height: 1.618;
}
a { color: inherit; }
a:focus-visible,
button:focus-visible {
  outline: 0.1875rem solid var(--color-primary);
  outline-offset: 0.1875rem;
}
strong { color: var(--color-text-primary); }
p { max-width: 70ch; }

/* === APPLICATION LAYOUT === */
.app-shell {
  width: 100%;
  max-width: 96rem; /* Wider shell */
  margin-inline: auto;
  padding: var(--s6);
  display: grid;
  grid-template-columns: minmax(16rem, 18rem) minmax(0, 1fr);
  gap: var(--s7); /* Mathematical VOID */
  align-items: start;
}
.page { min-width: 0; }
.layout, .content { display: block; }
.layout > .sidebar,
.topmenu,
.breadcrumbs,
.hero .nav,
.footer-nav { display: none; }

/* === SINGLE NAVIGATION === */
.site-nav {
  position: sticky;
  top: var(--s6); /* Spacing harmony */
  z-index: var(--z-sticky);
  max-height: calc(100vh - var(--s7));
  overflow: auto;
  background: rgba(8, 14, 24, 0.7);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--s5);
  box-shadow: var(--shadow-lg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
}
.nav-brand {
  padding: var(--s2) var(--s2) var(--s5);
  margin-bottom: var(--s5);
  border-bottom: 1px solid var(--color-border-soft);
}
.nav-brand strong {
  display: block;
  color: var(--color-primary);
  font-size: var(--text-lg);
  line-height: 1.2;
  font-weight: 800;
  letter-spacing: -0.02em;
}
.nav-brand span {
  display: block;
  margin-top: var(--s2);
  color: var(--color-text-muted);
  font-size: var(--text-xs);
  line-height: 1.5;
  max-width: 24ch;
}
.nav-section { margin-top: var(--s5); }
.nav-section-title {
  margin: 0 0 var(--s3);
  padding-inline: var(--s2);
  color: var(--color-text-muted);
  font-size: var(--text-xs);
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.nav-links {
  display: grid;
  gap: var(--s2);
}
.nav-links a {
  display: flex;
  align-items: center;
  gap: var(--s3);
  min-height: 2.75rem;
  padding: var(--s2) var(--s3);
  border: 1px solid transparent;
  border-radius: var(--radius-lg);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: var(--text-sm);
  line-height: 1.35;
  transition: all 200ms cubic-bezier(0.4, 0, 0.2, 1);
}
.nav-links a:hover {
  background: var(--color-surface-raised);
  border-color: var(--color-border);
  color: var(--color-text-primary);
  transform: translateX(2px);
}
.nav-links a.active {
  background: var(--color-primary-soft);
  border-color: var(--color-primary);
  color: var(--color-primary);
  font-weight: 600;
}
.nav-num {
  flex: 0 0 auto;
  width: 1.75rem;
  height: 1.75rem;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-full);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  color: var(--color-text-muted);
  font-size: var(--text-xs);
  font-weight: 800;
  transition: all 200ms ease;
}
.nav-links a.active .nav-num {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: var(--color-bg);
}
.toc-links {
  max-height: 34vh;
  overflow: auto;
  padding-right: var(--s1);
}
.toc-links a {
  min-height: 2.5rem;
  font-size: var(--text-sm);
}
.toc-links a::before {
  content: "•";
  color: var(--color-primary);
  font-weight: 800;
}
.nav-help {
  margin-top: var(--s6);
  padding: var(--s5) var(--s2) var(--s1);
  border-top: 1px solid var(--color-border-soft);
  color: var(--color-text-muted);
  font-size: var(--text-sm);
  line-height: 1.618;
}

/* === HERO / PAGE INTRO === */
.hero {
  margin-bottom: var(--s7);
  padding: var(--s7) var(--s6);
  background: radial-gradient(circle at top left, rgba(20, 31, 49, 0.8), rgba(14, 22, 36, 0.95));
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  position: relative;
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg, transparent, var(--color-primary), transparent);
  opacity: 0.3;
}
.hero h1 {
  margin: 0;
  max-width: 20ch;
  color: var(--color-text-primary);
  font-size: clamp(var(--text-3xl), 4vw, var(--text-4xl));
  line-height: 1.1;
  letter-spacing: -0.03em;
  font-weight: 800;
}
.hero p {
  margin: var(--s5) 0 0;
  color: var(--color-text-secondary);
  font-size: var(--text-lg);
  line-height: 1.618;
  max-width: 68ch;
}
.tagline,
.nav { display: none; }

.reading-steps {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: var(--s5);
  margin-bottom: var(--s7);
}
.reading-step,
.prereq-box,
.related-box,
.page-intro,
.mobile-note,
.warning,
.page-note {
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--s5);
  color: var(--color-text-secondary);
  box-shadow: var(--shadow-sm);
  font-size: var(--text-base);
  line-height: 1.618;
  transition: transform 200ms ease;
}
.reading-step:hover {
  transform: translateY(-2px);
}
.reading-step strong {
  display: block;
  color: var(--color-primary);
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: var(--s3);
}
.reading-step span { color: var(--color-text-secondary); }
.related-box a,
.prereq-box a { color: var(--color-primary); text-decoration: none; font-weight: 600; }
.warning {
  border-left: 4px solid var(--color-warning);
}

/* === CARDS / CONTENT === */
.card {
  margin: 0 0 var(--s8); /* Massive VOID between sections */
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-md);
  overflow: hidden;
}
.card > header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--s6);
  padding: var(--s6);
  background: linear-gradient(180deg, rgba(255,255,255,0.03), transparent);
  border-bottom: 1px solid var(--color-border-soft);
}
.card > header h2 {
  margin: 0;
  color: var(--color-text-primary);
  font-size: var(--text-2xl);
  line-height: 1.25;
  letter-spacing: -0.02em;
  font-weight: 800;
  max-width: 48ch;
}
.card > header span {
  flex: 0 0 auto;
  max-width: 14rem;
  padding: var(--s2) var(--s4);
  border-radius: var(--radius-full);
  background: var(--color-primary-soft);
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
  font-size: var(--text-xs);
  font-weight: 800;
  letter-spacing: 0.08em;
  line-height: 1.25;
  text-align: center;
  text-transform: uppercase;
}
.chart {
  background: #060A0F;
  padding: var(--s6);
  overflow-x: auto;
  overflow-y: visible;
  border-bottom: 1px solid var(--color-border-soft);
}
.chart svg {
  display: block;
  max-width: 100%;
  height: auto;
  overflow: visible;
}
.chart svg text {
  font-family: var(--font-sans);
  paint-order: stroke;
  stroke: #060A0F;
  stroke-width: 0.06rem;
  stroke-linejoin: round;
}
.explain {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(16rem, 1fr));
  gap: var(--s5);
  padding: var(--s6);
  background: var(--color-bg-soft);
}
.exbox {
  min-width: 0;
  padding: var(--s5);
  background: var(--color-surface-raised);
  border: 1px solid var(--color-border-soft);
  border-radius: var(--radius-lg);
  color: var(--color-text-secondary);
  font-size: var(--text-sm);
  line-height: 1.618;
  overflow-wrap: anywhere;
}
.exbox h4 {
  margin: 0 0 var(--s4);
  color: var(--color-primary);
  font-size: var(--text-xs);
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.exbox.entry h4 { color: var(--color-warning); }
.exbox.invalid h4 { color: var(--color-error); }
.exbox p { margin: 0; max-width: 65ch; }

/* === ACADEMY / PAGE BLOCKS === */
.academy-grid,
.intro-grid,
.section-links,
.home-map {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(18rem, 1fr));
  gap: var(--s5);
  margin-bottom: var(--s7);
}
.academy-grid { padding: var(--s6); background: var(--color-bg-soft); margin-bottom: 0; }
.academy-card,
.intro-card,
.section-link,
.home-card {
  display: flex;
  flex-direction: column;
  padding: var(--s5);
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: var(--text-base);
  line-height: 1.618;
  box-shadow: var(--shadow-sm);
  transition: all 250ms cubic-bezier(0.4, 0, 0.2, 1);
}
.section-link { min-height: 10rem; }
.section-link:hover { 
  transform: translateY(-4px); 
  border-color: var(--color-primary); 
  box-shadow: var(--shadow-md); 
  background: var(--color-surface-raised);
}
.academy-card h3,
.intro-card h3,
.section-link h3,
.home-card h3 {
  margin: 0 0 var(--s4);
  color: var(--color-text-primary);
  font-size: var(--text-xl);
  line-height: 1.25;
  font-weight: 800;
  letter-spacing: -0.01em;
}
.academy-card h4 {
  margin: var(--s5) 0 var(--s3);
  color: var(--color-text-primary);
  font-size: var(--text-xs);
  font-weight: 800;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.academy-card p,
.intro-card p,
.section-link p,
.home-card p { max-width: 65ch; margin: 0; flex-grow: 1; }
.academy-card ul,
.academy-card ol,
.intro-card ul,
.home-card ul {
  margin: var(--s4) 0 0 var(--s5);
  padding: 0;
}
.academy-card li,
.intro-card li,
.home-card li { margin: var(--s2) 0; }
.wide,.two { grid-column: 1 / -1; }
.badge {
  display: inline-flex;
  align-items: center;
  min-height: 1.75rem;
  margin: var(--s4) var(--s2) 0 0;
  padding: var(--s1) var(--s3);
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--color-border);
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
  font-weight: 700;
  letter-spacing: 0.05em;
}
.ok{color:var(--color-success)}.warn{color:var(--color-warning)}.bad{color:var(--color-error)}.muted{color:var(--color-text-muted)}
.table-like {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
  font-size: var(--text-sm);
}
.table-like th,
.table-like td { padding: var(--s4) var(--s5); border-bottom: 1px solid var(--color-border-soft); vertical-align: top; }
.table-like th { background: var(--color-surface-soft); color: var(--color-text-primary); text-align: left; font-weight: 600; }
.table-like tr:last-child th,
.table-like tr:last-child td { border-bottom: 0; }

.rule-block {
  padding: var(--s5) var(--s6);
  background: var(--color-primary-soft);
  border-top: 1px solid var(--color-primary);
  color: var(--color-text-primary);
  font-size: var(--text-sm);
  font-weight: 500;
}
.rule-block strong { color: var(--color-primary); text-transform: uppercase; letter-spacing: 0.05em; margin-right: var(--s2); }

/* === RESPONSIVE === */
@media (max-width: 68rem) {
  .app-shell { grid-template-columns: 1fr; padding: var(--s5); gap: var(--s6); }
  .site-nav { position: relative; top: auto; max-height: none; }
  .toc-links { max-height: none; }
  .hero { padding: var(--s6); }
  .reading-steps { grid-template-columns: 1fr; }
  .card > header { flex-direction: column; gap: var(--s4); }
  .academy-grid { padding: var(--s5); }
}
@media (max-width: 40rem) {
  body { font-size: var(--text-base); }
  .app-shell { padding: var(--s4); }
  .hero { padding: var(--s5); border-radius: var(--radius-lg); }
  .hero h1 { font-size: var(--text-2xl); }
  .site-nav,
  .card { border-radius: var(--radius-lg); }
  .card > header,
  .chart,
  .explain,
  .academy-grid { padding: var(--s4); }
  .card > header h2 { font-size: var(--text-lg); }
  .rule-block { padding: var(--s4); }
}
"""

with open("style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

for filename in os.listdir("."):
    if filename.endswith(".html"):
        with open(filename, "r", encoding="utf-8") as f:
            html = f.read()
        
        # Replace the entire <style>...</style> block
        html = re.sub(r'<style>.*?</style>', '<link rel="stylesheet" href="style.css">', html, flags=re.DOTALL)
        
        # Just in case some have spaces or newlines around it
        html = re.sub(r'\s*<link rel="stylesheet" href="style.css">\s*', '\n<link rel="stylesheet" href="style.css">\n', html)
        
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"Updated {filename}")
