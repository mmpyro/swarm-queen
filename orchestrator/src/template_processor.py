from jinja2 import Template

class TemplateProcessor(object):

    def __init__(self, src_file :str, dst_file :str) -> None:
        super().__init__()
        self.__src_file = src_file
        self.__dst_file = dst_file
        self.__rendered_template = None

    def process(self, config: dict) -> None:
        with open(self.__src_file, 'r') as file:
            template = Template(file.read())
            self.__rendered_template = template.render(config)

        with open(self.__dst_file, 'w') as file:
            file.write(self.__rendered_template)
