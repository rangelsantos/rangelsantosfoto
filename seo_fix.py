import os
import re

def add_lazy_loading(html_content, is_index=False):
    # Regex to find <img> tags
    img_pattern = re.compile(r'<img\s+[^>]*>', re.IGNORECASE)
    
    def replacer(match):
        img_tag = match.group(0)
        
        # Skip logical images
        if ('loading=' in img_tag.lower() or 
            'class="logo-img"' in img_tag or 
            'embedsocial' in img_tag.lower() or
            'src="assets/rangel-santos-logo' in img_tag or
            'src="../assets/rangel-santos-logo' in img_tag or
            'src="https://embedsocial' in img_tag):
            return img_tag

        if img_tag.endswith('/>'):
            new_tag = img_tag[:-2] + ' loading="lazy">'
        else:
            new_tag = img_tag[:-1] + ' loading="lazy">'
            
        return new_tag

    return img_pattern.sub(replacer, html_content)

def add_breadcrumb_schema(html_content, page_url, page_name):
    if '<!-- Schema Breadcrumb -->' in html_content:
        return html_content
        
    schema = f"""
    <!-- Schema Breadcrumb -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://rangelsantos.com.br/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "{page_name}",
          "item": "{page_url}"
        }}
      ]
    }}
    </script>
    <link rel="icon" """

    return html_content.replace('<link rel="icon" ', schema)

def add_blog_schema(html_content, page_url, title, image_url, publish_date):
    if '<!-- Schema Article -->' in html_content:
        return html_content

    schema = f"""
    <!-- Schema Breadcrumb -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BreadcrumbList",
      "itemListElement": [
        {{
          "@type": "ListItem",
          "position": 1,
          "name": "Home",
          "item": "https://rangelsantos.com.br/"
        }},
        {{
          "@type": "ListItem",
          "position": 2,
          "name": "Trabalhos",
          "item": "https://rangelsantos.com.br/trabalhos.html"
        }},
        {{
          "@type": "ListItem",
          "position": 3,
          "name": "{title}",
          "item": "{page_url}"
        }}
      ]
    }}
    </script>
    <!-- Schema Article -->
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "BlogPosting",
      "mainEntityOfPage": {{
        "@type": "WebPage",
        "@id": "{page_url}"
      }},
      "headline": "{title}",
      "image": "{image_url}",  
      "author": {{
        "@type": "Person",
        "name": "Rangel Santos"
      }},
      "publisher": {{
        "@type": "Organization",
        "name": "Rangel Santos Fotografia",
        "logo": {{
          "@type": "ImageObject",
          "url": "https://rangelsantos.com.br/assets/rangel-santos-logo-white.png"
        }}
      }},
      "datePublished": "{publish_date}",
      "dateModified": "{publish_date}"
    }}
    </script>
    <link rel="icon" """

    return html_content.replace('<link rel="icon" ', schema)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    filename = os.path.basename(filepath)
    is_index = filename == 'index.html'
    
    content = add_lazy_loading(content, is_index)

    pages_map = {
        'portfolio.html': 'Portfólio',
        'casamento.html': 'Casamento',
        'ensaios.html': 'Ensaios',
        'retratos.html': 'Retratos',
        'trabalhos.html': 'Trabalhos',
        'proposta-casamento.html': 'Proposta',
        'contato.html': 'Contato'
    }

    if filename in pages_map:
        page_url = f"https://rangelsantos.com.br/{filename}"
        content = add_breadcrumb_schema(content, page_url, pages_map[filename])
        
    elif 'trabalhos' in filepath.replace('\\', '/') and filename.endswith('.html') and filename != 'trabalhos.html':
        title_match = re.search(r'<title>(.*?)</title>', content)
        title = title_match.group(1).split('|')[0].strip() if title_match else filename.replace('.html', '')
        
        img_match = re.search(r'<meta property="og:image" content="(.*?)">', content)
        image_url = img_match.group(1) if img_match else "https://rangelsantos.com.br/assets/rangel-santos-logo-white.png"
        
        page_url = f"https://rangelsantos.com.br/trabalhos/{filename}"
        publish_date = "2024-01-01"
        
        content = add_blog_schema(content, page_url, title, image_url, publish_date)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = r"c:\Users\Rangel Santos\Desktop\Rangel Santos Fotografia\rangelsantosfoto"

for root, _, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.html') and "node_modules" not in root and ".git" not in root:
            filepath = os.path.join(root, file)
            print(f"Processando {filepath}")
            process_file(filepath)

print("Finalizado!")
