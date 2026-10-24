# Monoprint Homebrew tap

Install the signed and notarized macOS app and its `monoprint` command-line tool:

```sh
brew install --cask ozanvos/tap/monoprint
```

Requires an Apple Silicon Mac running macOS 12 or newer. Intel Macs are not
supported by the current release. Linux downloads are available on the
[Monoprint website](https://monoprint.7ea.st/#downloads).

The app includes automatic updates. To update explicitly through Homebrew:

```sh
brew update
brew upgrade --cask --greedy monoprint
```

If you installed Monoprint manually, Homebrew will refuse to overwrite the
existing app. Use `--adopt` only when it is identical to the current release,
or move the existing application aside before installing. Your saved draft
is separate from the app bundle.

```sh
brew uninstall --cask monoprint
```

Uninstalling retains the saved draft and preferences. `--zap` explicitly removes
them too.

## Maintenance

The update workflow checks the latest stable upstream release daily and can be
run manually. It verifies the release manifest, archive digest and signed
GitHub build provenance against the tagged source commit before updating the
cask. macOS CI audits the cask, installs it, checks its signature and notarization,
renders a PNG with the installed CLI, and uninstalls it before publishing updates.
The workflow uses only this repository's GitHub token; no cross-repository
credential is needed.

Source and issues: [ozanvos/monoprint](https://github.com/ozanvos/monoprint).
