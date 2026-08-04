# Privacy Disclosures Pipeline

Standalone pipeline that prepares, standardizes, and harmonizes iOS privacy labels and Android
safety forms into one shared common-label space for cross-platform comparison.

## Why this matters

App-store privacy disclosures use two different frameworks (Apple's privacy labels and Google's
safety forms), so the same practice is described in incompatible taxonomies. This pipeline
reconstructs both taxonomies inside the repo, converts each platform's wide disclosure export into
stable app-level indicators, and maps both into one shared label space — reproducibly and offline,
with no live store scraping.

## Quickstart

```bash
python setup_env.py                 # create .venv, install deps, write .env from .env.example
source .venv/bin/activate
python run_all.py                   # run the data/ then analysis/ stages in order
pytest                              # run the tests
```

The repo ships small **synthetic** sample inputs under `input/` (including the abbreviation
workbook as `.xlsx`, read via `openpyxl`) and defaults to `RUNTIME_MODE=sample`, so everything
above runs fully offline.

## Stages

Run in order by `run_all.py`; each writes a Markdown log to `logs/`.

| Script | Does | Writes to |
|--------|------|-----------|
| `data/d001_prepare_reference_data.py` | Reconstruct the iOS and Android taxonomies; prepare the abbreviation (Excel), translation, metadata, and registry maps | `output/data-output/` |
| `data/d002_prepare_ios_privacy_labels.py` | Convert the wide iOS export to typed indicators, diagnostics, and attached metadata | `output/data-output/` |
| `data/d003_prepare_android_safety_forms.py` | Same for Android, collapsing repeated app rows to one profile per app | `output/data-output/` |
| `data/d004_harmonize_cross_store_disclosures.py` | Map both platforms' positive disclosures into the shared common-label space | `output/data-output/` |
| `analysis/a001_build_summaries.py` | Build per-platform disclosure/category summaries and the cross-platform comparison | `output/analysis-output/` |

The shared taxonomy-building lives in `src/taxonomies.py`; the shared prepare-and-map logic in
`src/harmonization.py` (used by stages 2, 3, and 4).

## Layout

```text
src/          shared code: settings (config + paths + taxonomy templates), io, logger, utils, validation, taxonomies, harmonization
data/         d001–d004 data-processing scripts
analysis/     a001 summary script
input/        committed synthetic samples: iOS/Android exports, reference CSVs, and an .xlsx abbreviation map (real data gitignored)
output/       data-output/ and analysis-output/ (gitignored)
logs/         one <script>.md per run
tests/        pytest (t001–t006)
```

## How harmonization works

Each platform's wide indicator columns are named by a compact path token (e.g.
`DataUsedtoTrackYou_Identifiers_UserID`). Stage 4 melts the positive indicators to long form, then:

- **iOS** columns map to a common label directly through the abbreviation map.
- **Android** columns map to an item name through the taxonomy map, then to a common label through
  the Android-to-iOS translation map; anything without a match becomes `UNMAPPED`.

The cross-platform summary then counts unique apps per common label on each platform.

## Data & reproducibility

- Inputs: iOS and Android disclosure exports, an app-metadata CSV, an Android-to-iOS translation
  CSV, an abbreviation `.xlsx`, and a registry log CSV — all declared in `src/settings.py`.
- The committed samples are synthetic and internally consistent: they exercise the Android dedup, a
  label shared across both platforms, an iOS-only label, and an unmapped Android row; real inputs
  are gitignored.

## Testing

```bash
pytest
```

Tests cover the taxonomy and reference-map builders, both prepare stages, the common-label
harmonization (including the unmapped fallback), the summary builders, and the shared helpers.

## License

Apache-2.0. See [LICENSE](LICENSE) and [NOTICE](NOTICE).
