import jinja2
import os

latex_jinja_env = jinja2.Environment(
        block_start_string = '((*',
        block_end_string = '*))',
        variable_start_string = '(((',
        variable_end_string = ')))',
        comment_start_string = '((=',
        comment_end_string = '=))',
        loader = jinja2.FileSystemLoader(os.path.abspath('.'))
        )

template = latex_jinja_env.get_template('template.tex')
