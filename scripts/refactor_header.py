import os
import glob
from bs4 import BeautifulSoup
import re

CSS_TO_APPEND = """
/* === PAGE META DASHBOARD === */
.page-meta-dashboard {
  margin-bottom: var(--s7);
  display: grid;
  gap: var(--s5);
  background: transparent;
  border-left: 2px solid var(--color-primary);
  padding-left: var(--s5);
}
@media (min-width: 68rem) {
  .page-meta-dashboard {
    grid-template-columns: minmax(0, 2fr) minmax(0, 1fr);
    align-items: start;
    padding-left: var(--s6);
  }
}
.meta-main {
  display: flex;
  flex-direction: column;
  gap: var(--s4);
}
.meta-goal, .meta-prereq {
  font-size: var(--text-base);
  color: var(--color-text-secondary);
  line-height: 1.6;
}
.meta-goal strong, .meta-prereq strong {
  color: var(--color-primary);
  display: block;
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: var(--s1);
}
.meta-sidebar {
  display: flex;
  flex-direction: column;
  gap: var(--s3);
  background: var(--color-surface);
  padding: var(--s5);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
}
.meta-sidebar strong {
  color: var(--color-text-primary);
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.pill-nav {
  display: flex;
  flex-wrap: wrap;
  gap: var(--s2);
}
.pill {
  display: inline-flex;
  align-items: center;
  padding: var(--s1) var(--s3);
  background: var(--color-surface-raised);
  border: 1px solid var(--color-border-soft);
  border-radius: var(--radius-full);
  color: var(--color-text-secondary);
  font-size: var(--text-xs);
  font-weight: 600;
  text-decoration: none;
  transition: all 200ms ease;
}
.pill:hover {
  background: var(--color-primary-soft);
  border-color: var(--color-primary);
  color: var(--color-primary);
  transform: translateY(-1px);
}
"""

def append_css():
    css_path = 'style.css'
    if os.path.exists(css_path):
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if 'PAGE META DASHBOARD' not in content:
            with open(css_path, 'a', encoding='utf-8') as f:
                f.write(CSS_TO_APPEND)
            print("Appended new CSS to style.css")
        else:
            print("CSS already updated.")

def clean_text(strong_tag, container):
    # Extracts text without the leading strong tag content
    if not container: return ""
    # remove the strong tag from string representation, then strip
    text = container.get_text(separator=' ', strip=True)
    if strong_tag:
        strong_text = strong_tag.get_text(strip=True)
        if text.startswith(strong_text):
            text = text[len(strong_text):].strip()
            if text.startswith(':'):
                text = text[1:].strip()
    return text

def refactor_html_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    
    # We only want to refactor pages that have a hero and then these boxes
    hero = soup.find('div', class_='hero')
    if not hero:
        return

    # 1. Remove reading-steps
    reading_steps = soup.find('div', class_='reading-steps')
    if reading_steps:
        reading_steps.decompose()

    # Find all elements between hero and first .card
    # Actually, we can just find all prereq-box, page-intro, related-box
    # and extract data, then remove them.
    
    prereq_text = ""
    goal_text = ""
    links_data = {} # href -> text

    for box in soup.find_all('div', class_='prereq-box'):
        st = box.find('strong')
        prereq_text += clean_text(st, box) + " "
        box.decompose()

    for box in soup.find_all('div', class_='page-intro'):
        st = box.find('strong')
        goal_text += clean_text(st, box) + " "
        box.decompose()

    for box in soup.find_all('div', class_='related-box'):
        # extract links
        for a in box.find_all('a'):
            href = a.get('href')
            text = a.get_text(strip=True)
            if href and text:
                links_data[href] = text
        box.decompose()

    # If we found nothing to wrap, just return
    if not prereq_text.strip() and not goal_text.strip() and not links_data:
        # Save modifications (like removed reading-steps)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        return

    # Create the new dashboard
    dashboard = soup.new_tag('div', **{'class': 'page-meta-dashboard'})
    
    main_col = soup.new_tag('div', **{'class': 'meta-main'})
    
    if goal_text.strip():
        goal_div = soup.new_tag('div', **{'class': 'meta-goal'})
        st = soup.new_tag('strong')
        st.string = "Objectif"
        goal_div.append(st)
        goal_div.append(goal_text.strip())
        main_col.append(goal_div)
        
    if prereq_text.strip():
        prereq_div = soup.new_tag('div', **{'class': 'meta-prereq'})
        st = soup.new_tag('strong')
        st.string = "Prérequis"
        prereq_div.append(st)
        prereq_div.append(prereq_text.strip())
        main_col.append(prereq_div)
        
    dashboard.append(main_col)
    
    if links_data:
        side_col = soup.new_tag('div', **{'class': 'meta-sidebar'})
        st = soup.new_tag('strong')
        st.string = "Liens utiles"
        side_col.append(st)
        
        nav = soup.new_tag('nav', **{'class': 'pill-nav'})
        for href, text in links_data.items():
            a = soup.new_tag('a', href=href, **{'class': 'pill'})
            a.string = text
            nav.append(a)
        side_col.append(nav)
        dashboard.append(side_col)

    # Insert right after hero
    hero.insert_after(dashboard)

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Refactored: {filepath}")


if __name__ == "__main__":
    append_css()
    html_files = glob.glob('*.html')
    for f in html_files:
        try:
            refactor_html_file(f)
        except Exception as e:
            print(f"Error processing {f}: {e}")
