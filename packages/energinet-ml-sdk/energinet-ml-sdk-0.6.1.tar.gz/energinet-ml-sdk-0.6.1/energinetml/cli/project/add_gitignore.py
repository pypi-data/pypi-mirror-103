import os
import click
from shutil import copyfile

from energinetml.settings import GITIGNORE_PATH

from ..utils import discover_project


# -- CLI Command -------------------------------------------------------------


@click.command()
@discover_project()
def add_gitignore_lines(project):
    """
    Add ML specific lines to .gitignore file.
    \f

    :param energinetml.Project project:
    """
    fp = os.path.join(project.path, '.gitignore')

    copyfile(GITIGNORE_PATH, fp)
