import html2text


def convert_to_html(file_content):
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.bypass_tables = True
    html_content = h.handle(file_content)
    
    return html_content
