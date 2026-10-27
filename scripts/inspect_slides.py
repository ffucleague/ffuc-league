import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'C:\Users\Mark Borrego\Desktop\FFUC_Website\index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.findall(r'<section\s+id=["\']([^"\']+)["\'][^>]*>', text)
print('Sections found:', sections)

pills = re.findall(r'<button\s+onclick=["\']goToSlide\((\d+)\)["\'][^>]*>(.*?)</button>', text, re.DOTALL)
for idx, html in pills:
    clean = re.sub(r'<[^>]+>', '', html).strip()
    print(f'Slide {idx}: {clean}')
