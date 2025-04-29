import yaml
from jinja2 import Environment, FileSystemLoader
import os

def load_variables(yaml_path):
    with open(yaml_path, 'r') as file:
        return yaml.safe_load(file)

def render_template(template_dir, template_file, variables):
    env = Environment(loader=FileSystemLoader(template_dir), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template_file)
    return template.render(**variables)

def write_output(output_text, output_path):
    with open(output_path, 'w') as file:
        file.write(output_text)
    print(f"[✔] Rendered config saved to {output_path}")

def main():
    # Define paths
    template_dir = os.path.join(os.path.dirname(__file__), 'examples')
    template_file = 'template.j2'
    vars_file = os.path.join(template_dir, 'vars.yaml')
    output_file = os.path.join(template_dir, 'generated_config.txt')

    # Load data and render
    variables = load_variables(vars_file)
    rendered_output = render_template(template_dir, template_file, variables)
    write_output(rendered_output, output_file)

if __name__ == '__main__':
    main()
