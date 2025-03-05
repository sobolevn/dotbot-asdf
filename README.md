# dotbot-asdf

Install [`asdf`](https://github.com/asdf-vm/asdf) plugins and programming languages with `dotbot`.

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

## Usage

Add required options to your [`install.conf.yaml`](/example.yaml):

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

### Setting Default Versions

With asdf 0.16.0+, you can set default versions using either the `default` parameter (recommended) or the legacy `global` parameter:

```yaml
# This example installs python 3.7.4, nodejs 12.10 and ruby 2.6.4:
- asdf:
  - plugin: python
    url: https://github.com/tuvistavie/asdf-python.git
    default: 3.7.4  # For asdf 0.16.0+ (recommended)
    versions:
      - 3.7.4
  - plugin: nodejs
    url: https://github.com/asdf-vm/asdf-nodejs.git
    global: 12.10  # Legacy syntax, still supported for backward compatibility
    versions:
      - 12.10
  - plugin: ruby
    url: https://github.com/asdf-vm/asdf-ruby.git
    default: 2.6.4
    versions:
      - 2.6.4
```

### Advanced Configuration (asdf 0.16.0+)

You can also set versions in the current directory or parent directories:

```yaml
- asdf:
  - plugin: python
    url: https://github.com/tuvistavie/asdf-python.git
    versions:
      - 3.10.4
      - 3.11.0
    default: 3.10.4  # Set in home directory (replaces global)
    local: 3.11.0    # Set in current directory
  - plugin: nodejs
    url: https://github.com/asdf-vm/asdf-nodejs.git
    versions:
      - lts-hydrogen
    parent:  # Set in parent directory
      version: lts-hydrogen
```

### ASDF Location Configuration

It's also possible to configure the location for asdf in case asdf itself was
installed as part of the dotbot install process. This will cause the plugin to
source the provided script before every asdf command.
Only the first instance of `asdf_path` in the configuration will be respected.

```yaml
- asdf:
  - asdf_path: /opt/asdf-vm/asdf.sh
  - plugin: python
    default: 3.10.4
    versions:
      - 3.10.4
```

## ASDF 0.16.0+ Compatibility

This plugin is fully compatible with asdf 0.16.0+ and supports the new command structure:

- The deprecated `asdf global` command has been replaced with `asdf set --home`
- The plugin supports both the older `global` parameter and the newer `default` parameter for backward compatibility
- New features like setting versions in parent directories (`parent.version`) are supported

For more information on asdf 0.16.0+ changes, see the [asdf upgrade guide](https://asdf-vm.com/guide/upgrading-to-v0.16.html).

## License

MIT. See [LICENSE](/LICENSE) for more details.
