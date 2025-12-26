import os
import urllib.parse

def generate_file_list(directory):
    file_list = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_list.append(os.path.join(root, filename))
    return file_list


def generate_html(directory):
    file_list = generate_file_list(directory)
    username = os.path.basename(directory)
    base_url = f"/static/uploads/{username}/"
    
    html_content = f"""
    <html>
    <head>
        <script src="/static/main.js"></script>
        <link rel="stylesheet" href="/static/base.css" />
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: var(--second-color);
                color: var(--primary-color);
                padding: 20px;
            }}
            h1 {{
                border-bottom: 2px solid var(--primary-color);
                padding-bottom: 10px;
                margin-bottom: 20px;
            }}
            ul {{
                list-style: none;
                padding-left: 0;
            }}
            li {{
                margin-bottom: 10px;
            }}
            a {{
                color: var(--primary-color);
                text-decoration: none;
                font-weight: bold;
                padding: 6px 10px;
                border: 1px solid var(--primary-color);
                border-radius: 4px;
                transition: background-color 0.3s, color 0.3s;
            }}
            a:hover {{
                background-color: var(--primary-color);
                color: var(--second-color);
            }}
        </style>
    </head>
    <body>
        <h1>Files for {username}</h1>
        <ul>
    """

    for file_path in file_list:
        filename = os.path.basename(file_path)
        url_path = base_url + urllib.parse.quote(filename)
        html_content += f'<li><a href="{url_path}" download>{filename}</a></li>'

    html_content += """
        </ul>
    </body>
    </html>
    """
    return html_content
