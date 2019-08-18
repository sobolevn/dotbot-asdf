# dotbot-asdf

Install [`asdf`](https://github.com/asdf-vm/asdf) plugins with `dotbot`.


## Prerequirements

This plugin requires [`dotbot`](https://github.com/anishathalye/dotbot/) to be installed.

Also, at runtime this plugin requires `asdf` command to be installed.


## Installation

1. Run:

```bash
git submodule add https://github.com/sobolevn/dotbot-asdf.git
```

2. Modify your `./install` with new plugin directory:

```bash
"${BASEDIR}/${DOTBOT_DIR}/${DOTBOT_BIN}" -d "${BASEDIR}" --plugin-dir dotbot-asdf -c "${CONFIG}" "${@}"
```

3. Add required options to your [`install.conf.yaml`](/example.yaml):

```yaml
# This example uses python, nodejs and ruby plugins:

- asdf:
    - plugin: python
      url: https://github.com/tuvistavie/asdf-python.git
    - plugin: nodejs
      url: https://github.com/asdf-vm/asdf-nodejs.git
    - plugin: ruby
      url: https://github.com/asdf-vm/asdf-ruby.git
```

Plugins can also be specified with just a name for [known plugins](https://asdf-vm.com/#/plugins-all?id=plugin-list):

```yaml
# This example uses python, nodejs and ruby plugins:

- asdf:
    - plugin: python
    - plugin: nodejs
    - plugin: ruby
```

That's it!


## License

MIT. See [LICENSE](/LICENSE) for more details.
