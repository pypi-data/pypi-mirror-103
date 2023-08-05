# Copyright (C) NIWA & British Crown (Met Office) & Contributors.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Configuration file for jupyterhub.

from pathlib import Path
import pkg_resources

from cylc.uiserver import __file__ as uis_pkg


# the command the hub should spawn (i.e. the cylc uiserver itself)
c.Spawner.cmd = ['cylc', 'uiserver']

# the spawner to invoke this command
c.JupyterHub.spawner_class = 'jupyterhub.spawner.LocalProcessSpawner'

# this auto-spawns uiservers without user interaction
c.JupyterHub.implicit_spawn_seconds = 0.01

# apply cylc styling to jupyterhub
c.JupyterHub.logo_file = str(Path(uis_pkg).parent / 'logo.svg')
c.JupyterHub.log_datefmt = '%Y-%m-%dT%H:%M:%S'  # ISO8601 (expanded)
c.JupyterHub.template_paths = [
    # custom HTML templates
    pkg_resources.resource_filename(
        'cylc.uiserver',
        'templates'
    )
]
