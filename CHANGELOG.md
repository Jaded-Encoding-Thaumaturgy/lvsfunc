# Changelog

The dev will try to keep this as up-to-date as he can,
but makes no promises.

## 0.10.4

[Full diff since v0.10.3][diff-0.10.4]

### Features

- `presets.mv`: add `autoselect_blksize` and `mv_refine_kwargs` for resolution-aware MVTools block size calculation ([90e1ab4]).
- `util.set_vs_affinity`: configure VapourSynth worker threads, CPU affinity, and framebuffer cache limits ([bd296a2]).
- `models`: resample scaled output back to the input format using the configured scaler ([9464cb8]).

### Documentation

- Convert public docstrings to Google style ([ad64b47]).
- Standardize on American English in user-facing text ([ad64b47]).

### Packaging and tooling

- Model tests: pin mlrt to `Backend.ORT_CPU` instead of autoselect ([8bb4e7b]).
- Mypy stubs: add `Backend.ORT_CPU` to `vsscale.mlrt` ([8bb4e7b]).
- Lint: split `poe lint` into discrete tasks ([42dafa0]).
- Lint: Add `poe lint-ci`, and run it from CI ([42dafa0]).
- Expand model tests for post-scale format restoration ([9464cb8]).

## 0.10.3

[Full diff since v0.10.2][diff-0.10.3]

### Breaking changes

- `comparison.stack_compare`: Reworked ([efa7995], [6e187ab]).
- `comparison.diff_between_clips_stack`: deprecated in favor of `stack_compare` ([efa7995]).

### Features

- `decorators`: add `initialize_inputs` and `finalize_clips` ([3fdfcc7]).
- `presets.mv`: add `LightMVPresets`, `SlocCurves`, and `autoselect_pel` MVTools and DFTTest helpers ([3ac9eb0]).
- `util.sloc_curve_to_graph`: plot `DFTTest.SLocation` curves ([3ac9eb0]).

### Fixes

- `comparison.comparison_shots`: fix crash when only named clips are passed with `height <= 10` ([9bb8544]).
- `comparison.stack_compare`: always apply the half-height cap when the requested height exceeds the source clip ([6e187ab]).
- `util.sloc_curve_to_graph`: use the Agg matplotlib backend so plotting works headlessly ([5767088]).

### Packaging and tooling

- Bump `vsjetpack` to `>=2.0.0` ([285d932]).
- Set `index-strategy = "unsafe-best-match"` to work around a vs-wheel resolve issue ([285d932]).
- Packaging: optional GPU extras `cl`, `nvidia`, and `amd` ([285d932]).
- Dependencies: add `matplotlib` for `sloc_curve_to_graph` ([3ac9eb0]).
- Add `codespell` dev dependency, `codespell` config, and `poe spell` ([fda4273]).
- Pytest: ignore VS API3 deprecation warnings in plugin stderr ([bcd7f34]).
- Expand tests for `comparison`, `decorators`, `presets`, `color`, `models`, and `util` ([5767088]).

## 0.10.2

[Full diff since v0.10.1][diff-0.10.2]

### Features

- `models`: move ONNX wrappers onto vsscale `BaseOnnxScalerRGB` ([#179][pr-179], [a5a787f]).

### Fixes

- `FindDiff`: fix `diff_ranges` being shared across multiple `FindDiff` instances ([e8a2d08]).
- `FindDiff`: raise when no differences are found *or* the result list is empty ([8c7a152]).
- `RGBColor.scale_value`: fix reversed argument order ([57c4643]).
- `comparison.Split._smart_crop`: fix unconditional error after cropping ([b9b9fb6]).
- Fix mutable defaults in `deblock`, `diff`, and `nn` ([dfb6efc]).
- `models`: warn when an ignored `model` path is passed; deprecate `apply()` ([66d684a]).

### Packaging and tooling

- Overhaul dev dependencies and lockfile ([e312106]).
- Bump `vsjetpack` to `2.0.0rc2` ([96e4fdc]).
- Add `poe lint` task (vsstubs, isort, ruff, mypy, pytest) ([e312106], [0bcbfbe]).
- Add minimal mypy stubs for `kagefunc` and `vsscale` ([0bcbfbe], [2ba4371]).
- Extend mypy coverage to `tests/` ([e312106]).
- Add `vsstubs generate` in the lint workflow ([25bf2c7]).
- Trigger workflows on `**.py*` path changes ([3ea759f]).
- Lint and typing fixes across `lvsfunc` ([0bcbfbe]).
- Add tests for `diff`, `comparison`, `models`, and `util` ([555ccc2], [8f77ebe], [ddf2bd7]).

## 0.10.1

[Full diff since v0.10.0][diff-0.10.1]

### Features

- `FindDiff.get_diff_full`: return src, ref, and diff clips limited to differing frames (thanks @Kapppa! [#175][pr-175], [5489ae9])
- `comparison`: port `Direction` back from vstools (thanks @Ichunjo! [#174][pr-174], [ec9e7eb]).

### Fixes

- `FindDiff`: pass `post_processor` through to the comparison pipeline ([0290416]).
- `FindDiff`: use validated clips after input normalization ([6f54c16]).

### Packaging and tooling

- Add initial pytest coverage (`tests/test_color.py`) ([b55d635]).
- Enable **ruff** and **mypy** in CI ([ea21c18]).

## 0.10.0

[Full diff since v0.9.1][diff-0.10.0]

### Breaking changes

- Remove the `lvsfunc.dependency` submodule ([a9c8738])
  - Helpers for missing plugins/packages
    are [obsolete as of VS R74][vs-r74],
    and this was only ever a POC anyway.
    Anyone who relied on this submodule (why?)
    should be switching over to PyPi- (or better yet, uv)-based dependency control instead.
- Bump minimum `vsjetpack[basic]` version to **1.5.0** ([a63038e]).

### Features

- `overlay_sign`: replace `IMWRI` call with `BestSource` ([c821a1b]).
- `overlay_sign`: drop the resample check (no-op via `vskernels`) ([c821a1b]).
- `comparison_shots`: recommend vsview over vspreview ([f87f480]).
- `RGBColor`: validate RGB reference clips ([11b2dfc]).

### Fixes

- `Base1xModel`: correct swapped package names in DependencyNotFound error ([007e270]).
- `overlay_sign`: remove redundant guard ([3644340]).

### Packaging and tooling

- Switch to a **uv**-managed project ([60a08c4]).
- Update GitHub Actions
  (rename the Python version env var, drop redundant twine check, disable automerge for now) ([71679b2]).
- Move `renovate.json` to the repo root ([71679b2]).
- Add `CONTRIBUTING.md` and contributing instructions ([913cb34]).

### Documentation

- Update **README** ([7d35868], [21cd940]).
- Replace IEW references with **JET** where I forgot to do so previously ([8768cb6]).
- Bump copyright year ([b4eee33]).

## v0.9.1 and below

Not tracked.
Please check [Releases][releases] for old changelogs.

[//]: (Commits-to-make-the-actual-text-less-noisy)
[releases]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/releases
[vs-r74]: https://www.vapoursynth.com/2026/03/26/new-packaging-and-install-methods-in-r74/

[007e270]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/007e270
[0290416]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/0290416
[0bcbfbe]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/0bcbfbe
[11b2dfc]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/11b2dfc
[21cd940]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/21cd940
[25bf2c7]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/25bf2c7
[285d932]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/285d932
[2ba4371]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/2ba4371
[3644340]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/3644340
[3ac9eb0]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/3ac9eb0
[3ea759f]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/3ea759f
[3fdfcc7]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/3fdfcc7
[42dafa0]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/42dafa0
[5489ae9]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/5489ae9
[555ccc2]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/555ccc2
[5767088]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/5767088
[57c4643]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/57c4643
[60a08c4]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/60a08c4
[66d684a]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/66d684a
[6e187ab]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/6e187ab
[6f54c16]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/6f54c16
[71679b2]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/71679b2
[7d35868]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/7d35868
[8768cb6]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/8768cb6
[8bb4e7b]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/8bb4e7b
[8c7a152]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/8c7a152
[8f77ebe]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/8f77ebe
[90e1ab4]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/90e1ab4
[913cb34]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/913cb34
[9464cb8]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/9464cb8
[96e4fdc]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/96e4fdc
[9bb8544]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/9bb8544
[a5a787f]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/a5a787f
[a63038e]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/a63038e
[a9c8738]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/a9c8738
[ad64b47]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/ad64b47
[b4eee33]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/b4eee33
[b55d635]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/b55d635
[b9b9fb6]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/b9b9fb6
[bcd7f34]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/bcd7f34
[bd296a2]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/bd296a2
[c821a1b]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/c821a1b
[ddf2bd7]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/ddf2bd7
[dfb6efc]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/dfb6efc
[e312106]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/e312106
[e8a2d08]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/e8a2d08
[ea21c18]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/ea21c18
[ec9e7eb]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/ec9e7eb
[efa7995]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/efa7995
[f87f480]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/f87f480
[fda4273]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/commit/fda4273

[pr-174]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/pull/174
[pr-175]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/pull/175
[pr-179]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/pull/179

[diff-0.10.0]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/compare/v0.9.1...v0.10.0
[diff-0.10.1]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/compare/v0.10.0...v0.10.1
[diff-0.10.2]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/compare/v0.10.1...v0.10.2
[diff-0.10.3]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/compare/v0.10.2...v0.10.3
[diff-0.10.4]: https://github.com/Jaded-Encoding-Thaumaturgy/lvsfunc/compare/v0.10.3...master
