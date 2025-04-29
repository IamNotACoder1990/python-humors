from jinja2 import Template

def render_config(template_path, variables):
    with open(template_path) as file:
        template = Template(file.read())
    return template.render(variables)

# Example usage:
# output = render_config("router.j2", {"hostname": "R1"})
