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

    def __init__(self, context):
        super(Brew, self).__init__(context)
        output = self._run_command(
            'asdf plugin-list-all',
            error_message='Failed to get known plugins',
            stdout=subprocess.PIPE
        )
        plugins = output.decode('utf-8')
        self._known_plugins = plugins.split()[::2]

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

            if name is None:
                raise ValueError(
                    'Invalid plugin definition: {}'.format(str(plugin))
                )
            elif 'url' not in plugin and name not in self._known_plugins:
                raise ValueError(
                    'Unknown plugin: {}\nPlease provide URL'.format(name)
                )

    def _build_command(self, plugin, url):
        if not url:
            return '{} {}'.format(self._install_command, plugin)
        else:
            return '{} {} {}'.format(self._install_command, plugin, url)

    def _handle_install(self, data):
        for plugin in data:
            language = plugin['plugin']
            self._run_command(
                'asdf plugin-add {} {}'.format(language, plugin.get('url', '')).strip(),
                'Installing {} plugin'.format(language),
                'Failed to install: {} plugin'.format(language)
            )

    def _run_command(self, command, message=None, error_message=None, **kwargs):
        if message is not None:
            self._log.lowinfo(message)

        p = subprocess.Popen(command, cwd=self.cwd, shell=True, **kwargs)
        p.wait()
        output, output_err = p.communicate()

        if output_err is not None:
            if error_message is None:
                error_message = 'Command failed: {}'.format(command)

            raise ValueError(error_message)

        return output
