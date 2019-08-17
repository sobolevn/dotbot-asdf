import os
import sys
import subprocess

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import dotbot


class Brew(dotbot.Plugin):
    _supported_directives = [
        'asdf',
    ]

    _install_command = 'asdf plugin-add'

    # API methods

    def can_handle(self, directive):
        return directive in self._supported_directives

    def handle(self, _directive, data):
        try:
            self._validate_plugins(data)
            self._handle_install(data)
            return True
        except ValueError as e:
            self._log.error(e)
            return False

    # Utility

    @property
    def cwd(self):
        return self._context.base_directory()

    # Inner logic

    def _validate_plugins(self, plugins):
        for plugin in plugins:
            name = plugin.get('plugin', None)
            url = plugin.get('url', None)

            if not name:
                raise ValueError(
                    '{} is not valid plugin definition'.format(str(plugin))
                )


    def _build_command(self, plugin, url):
        if not url:
            return '{} {}'.format(self._install_command, plugin)
        else:
            return '{} {} {}'.format(self._install_command, plugin, url)

    def _handle_install(self, data):
        for plugin in data:
            p = subprocess.Popen(
                self._build_command(plugin['plugin'], plugin.get('url', None)),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                shell=True,
                cwd=self.cwd
            )
            p.wait()
            _, output_err = p.communicate()

            if output_err != None:
                message = 'Failed to install: ' + plugin['plugin']
                raise ValueError(message + ' ')

