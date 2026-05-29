import os
import shutil

def main():
    dirs_to_create = ['css', 'js', 'pages', 'scripts', 'logs']
    for d in dirs_to_create:
        os.makedirs(d, exist_ok=True)

    files = [f for f in os.listdir('.') if os.path.isfile(f)]

    pages_moved = []

    # 1. Move files
    for f in files:
        if f == 'migrate_structure.py':
            continue

        if f.startswith('README_V') and f.endswith('.txt'):
            shutil.move(f, os.path.join('logs', f))
        elif f == 'style.css':
            shutil.move(f, os.path.join('css', f))
        elif f == 'glossary-panel.js':
            shutil.move(f, os.path.join('js', f))
        elif f.endswith('.py'):
            shutil.move(f, os.path.join('scripts', f))
        elif f.endswith('.html') and f != 'index.html':
            shutil.move(f, os.path.join('pages', f))
            pages_moved.append(f)

    print(f"Moved {len(pages_moved)} HTML pages to pages/")
    print("Files moved successfully.")

    # 2. Update index.html
    if os.path.exists('index.html'):
        with open('index.html', 'r', encoding='utf-8') as file:
            content = file.read()

        content = content.replace('href="style.css"', 'href="css/style.css"')
        content = content.replace('src="glossary-panel.js"', 'src="js/glossary-panel.js"')

        for p in pages_moved:
            content = content.replace(f'href="{p}"', f'href="pages/{p}"')
            content = content.replace(f'href="{p}#', f'href="pages/{p}#')

        with open('index.html', 'w', encoding='utf-8') as file:
            file.write(content)
        print("index.html updated.")

    # 3. Update all pages in pages/
    for p in pages_moved:
        page_path = os.path.join('pages', p)
        if os.path.exists(page_path):
            with open(page_path, 'r', encoding='utf-8') as file:
                content = file.read()

            content = content.replace('href="style.css"', 'href="../css/style.css"')
            content = content.replace('src="glossary-panel.js"', 'src="../js/glossary-panel.js"')
            content = content.replace('href="index.html"', 'href="../index.html"')

            with open(page_path, 'w', encoding='utf-8') as file:
                file.write(content)

    print("All internal pages updated.")

if __name__ == '__main__':
    main()
