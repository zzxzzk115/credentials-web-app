import base64
import os
import mimetypes
from urllib.request import pathname2url


def _get_config_dict(config_file_path: str) -> dict:
    config_dict = {}
    if not os.path.exists(config_file_path):
        return config_dict
    with open(config_file_path) as f:
        config_lines = f.readlines()
        for line in config_lines:
            clean_line = line.strip('\n')
            splitted_line = clean_line.split(',')
            if len(splitted_line) >= 2:
                config_item_key = splitted_line[0]
                config_item_value = splitted_line[1]
                config_dict[config_item_key] = config_item_value
    return config_dict    


def get_rendered_html(html_file_path : str, config_dict_file_path : str) -> str:
    result_html = ''
    if not os.path.exists(html_file_path):
        return result_html
    with open(html_file_path) as f:
        result_html = f.read()
        config_dict = _get_config_dict(config_dict_file_path)
        for key in config_dict:
            result_html = result_html.replace('{{!' + key + '}}', config_dict[key])
    return result_html


def get_rendered_html_native(html_content : str, config_dict : dict) -> str:
    result_html = html_content
    for key in config_dict:
        result_html = result_html.replace('{{!' + key + '}}', config_dict[key])
    return result_html


def get_attachment(attachment_file_path : str):
    if not os.path.exists(attachment_file_path):
        return None
    with open(attachment_file_path, "rb") as f:
        attachment_json = {
            'content': base64.standard_b64encode(f.read()).decode('utf-8'),
            'type': mimetypes.guess_type(pathname2url(attachment_file_path))[0],
            'name': os.path.basename(attachment_file_path)
        }
        print(attachment_json)
        return attachment_json
    

def test_template():
    html = open('test/template/example.html', 'r').read()
    config_dict = _get_config_dict('test/template/example_config.txt')
    rendered_html = get_rendered_html(html, config_dict)
    print('Rendered Template HTML:\n')
    print(rendered_html)
    return rendered_html