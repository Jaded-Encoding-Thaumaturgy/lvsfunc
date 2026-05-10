# Changelog

The dev will try to keep this as up-to-date as he can,
but makes no promises.

## 0.10.0 (unreleased)

### Breaking changes

- Remove the `lvsfunc.dependency` submodule
  - Helpers for missing plugins/packages
    are [obsolete as of VS R74](https://www.vapoursynth.com/2026/03/26/new-packaging-and-install-methods-in-r74/),
    and this was only ever a POC anyway.
    Anyone who relied on this submodule (why?)
    should be switching over to PyPi-based dependency control instead.

### Features

- `overlay_sign`: replace `IMWRI` call with `BestSource`.
- `overlay_sign`: drop the resample check (no-op via `vskernels`).
- `comparison_shots`: recommend vsview over vspreview.
- `RGBColor`: validate RGB reference clips.

### Fixes

- `Base1xModel`: correct swapped package names in DependencyNotFound error.

### Packaging and tooling

- Switch to a **uv**-managed project.
- Update GitHub Actions.
- Add `CONTRIBUTING.md` and contributing instructions.

### Documentation

- Update **README**.
- Replace IEW references with **JET** where I forgot to do so previously.
- Bump copyright year.

## v0.9.1 and below

Not tracked.
Please check [Releases](https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/releases) for old changelogs.
