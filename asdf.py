import subprocess
from os import getenv

import dotbot


class Brew(dotbot.Plugin):
    _supported_directives = ["asdf"]
    _known_plugins = []
    _has_checked_known_plugins = False

    def __init__(self, context):
        super(Brew, self).__init__(context)

    @property
    def known_plugins(self):
        # Would love to use @cached_property but keeping python 2.7 compatibility
        if self._has_checked_known_plugins:
            return self._known_plugins

        output = self._run_command(
            "asdf plugin-list-all",
            error_message="Failed to get known plugins",
            stdout=subprocess.PIPE,
        )
        plugins = output.decode("utf-8") # type: ignore
        for plugin in plugins.split()[::2]:
            self._known_plugins.append(plugin)

        self._has_checked_known_plugins = True
        return self._known_plugins

    @property
    def asdf_location(self):
        return getattr(self, "_asdf_location", None)

    @asdf_location.setter
    def asdf_location(self, location):
        self._asdf_location = location

    # API methods

    def can_handle(self, directive):
        return directive in self._supported_directives

    def handle(self, _directive, data):
        for item in data:
            if item.get("asdf_path", False):
                self.asdf_location = item.get("asdf_path")
                break

        plugins = [node for node in data if node.get("plugin", None)]

        try:
            self._validate_plugins(plugins)
            self._handle_install(plugins)
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
            name = plugin.get("plugin", None)

            if name is None:
                raise ValueError("Invalid plugin definition: {}".format(str(plugin)))
            elif "url" not in plugin and name not in self.known_plugins:
                raise ValueError("Unknown plugin: {}\nPlease provide URL".format(name))

    def _handle_install(self, data):
        for plugin in data:
            language = plugin["plugin"]
            self._log.info("Installing " + language)
            self._run_command(
                "asdf plugin-add {} {}".format(language, plugin.get("url", "")).strip(),
                "Installing {} plugin".format(language),
                "Failed to install: {} plugin".format(language),
            )

            if "versions" in plugin:
                for version in plugin["versions"]:
                    self._run_command(
                        "asdf install {} {}".format(language, version),
                        "Installing {} {}".format(language, version),
                        "Failed to install: {} {}".format(language, version),
                    )

            if "global" in plugin:
                global_version = plugin["global"]
                self._run_command(
                    "asdf global {} {}".format(language, global_version),
                    "Setting global {} {}".format(language, global_version),
                    "Failed setting global: {} {}".format(language, global_version),
                )
            else:
                self._log.lowinfo("No {} versions to install".format(language))

    def _system_sh_is_dash(self):
        """Debian has replaced bash with dash as the system shell, and has
        removed the ability to switch it back ref
        https://launchpad.net/debian/+source/dash/0.5.11+git20210903+057cd650a4ed-4.

        dash doesn't have any way to source files, which is why we need to check for it.
        If the `type source` command returns 127, that means the shell doesn't support source.
        """

        dash_check = subprocess.Popen(
            "type source", shell=True, stdout=subprocess.DEVNULL
        ).wait()
        return dash_check == 127

    def _run_command(self, command, message=None, error_message=None, **kwargs):
        if message is not None:
            self._log.lowinfo(message)

        if self.asdf_location:
            command = f"source {self.asdf_location} && {command}"
        if self._system_sh_is_dash():
            # dash doesn't overwrite $SHELL so lets try to use that.
            shell = getenv("SHELL", default="/usr/bin/bash")
            self._log.debug(f"dash detected, attempting to use user shell {shell}")
            command = '{0} -c "{1}"'.format(shell, command)

        self._log.debug(command)
        p = subprocess.Popen(command, cwd=self.cwd, shell=True, **kwargs)
        p.wait()
        output, output_err = p.communicate()

        if output_err is not None:
            if error_message is None:
                error_message = "Command failed: {}".format(command)

            raise ValueError(error_message)

        return output
