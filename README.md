# Privacy Disclosures Pipeline

Standalone pipeline for preparing, standardizing, and harmonizing iOS privacy labels and Android safety forms using bundled disclosure exports and taxonomy reference files.

## Overview

This repository packages a cross-platform disclosure workflow built around app-store privacy disclosures. It prepares the iOS privacy-label taxonomy, prepares the Android safety-form taxonomy, standardizes platform-level disclosure exports, and then harmonizes both platforms into a shared common-label space for comparison.

The repository is designed to be runnable without live store scraping. Instead of depending on current App Store or Play Store access, it uses bundled sample disclosure exports, taxonomy mappings, abbreviation maps, and app metadata. That makes the repo inspectable and reproducible while keeping the full workflow self-contained.

## Purpose

The repository does four things:

1. Prepare the iOS and Android disclosure taxonomies together with the cross-platform reference maps.
2. Prepare the wide iOS privacy-label export into a stable app-level dataset with metadata and row-level diagnostics.
3. Prepare the wide Android safety-form export into a stable app-level dataset with deduplication, metadata, and row-level diagnostics.
4. Harmonize both platforms into a shared common-label space and generate cross-platform summary tables.

The main outputs are taxonomy tables, prepared wide disclosure tables, harmonized long disclosure tables, and cross-platform summary outputs.

## Key Definitions

- `IOS Privacy Label`: the disclosure framework shown on App Store pages that groups data usage into categories such as tracking, linked data, and data not linked to the user.
- `Android Safety Form`: the disclosure framework shown on Google Play pages that summarizes data collection, sharing, and security practices.
- `Taxonomy`: the structured label system used to organize disclosure categories and data types.
- `Cross-Platform Harmonization`: the process of mapping iOS and Android disclosure categories into a shared comparison framework.
- `Wide` vs `Long`: tabular layouts where `wide` data stores many indicators as columns, while `long` data stores one disclosure observation per row.

## Data Access Notes

The raw input data is not tracked in this repository. If you'd like to discuss the sample data structure, expected schema, or reproduction details, feel free to contact me.

## Pipeline Stages

### Stage 1: Prepare Reference Data

This stage reads the Android-to-iOS translation table, the privacy-label abbreviation file, the app metadata sample, and the sample platform log sheet. It also reconstructs the iOS privacy-label taxonomy and Android safety-form taxonomy inside the repo.

Primary outputs:

- Output file: `output/exports/001_prepare_reference_data/ios_privacy_labels_map.csv`
- Output file: `output/exports/001_prepare_reference_data/android_safety_forms_map.csv`
- Output file: `output/exports/001_prepare_reference_data/privacy_label_abbreviation_map.csv`
- Output file: `output/exports/001_prepare_reference_data/prepared_taxonomy_translation_map.csv`
- Output file: `output/exports/001_prepare_reference_data/prepared_app_metadata.csv`
- Output file: `output/exports/001_prepare_reference_data/platform_registry_summary.csv`

### Stage 2: Prepare iOS Privacy Labels

This stage reads the bundled iOS privacy-label export, converts the wide disclosure indicators to deterministic integer flags, attaches app metadata, and computes row-level diagnostics such as total positive disclosure indicators.

Primary outputs:

- Output file: `output/exports/002_prepare_ios_privacy_labels/prepared_ios_privacy_labels.csv`
- Output file: `output/exports/002_prepare_ios_privacy_labels/ios_disclosure_summary.csv`
- Output file: `output/exports/002_prepare_ios_privacy_labels/ios_category_summary.csv`

### Stage 3: Prepare Android Safety Forms

This stage reads the bundled Android safety-form export, collapses repeated app rows to one app-level record, preserves positive disclosure indicators, attaches app metadata, and computes row-level diagnostics.

Primary outputs:

- Output file: `output/exports/003_prepare_android_safety_forms/prepared_android_safety_forms.csv`
- Output file: `output/exports/003_prepare_android_safety_forms/android_disclosure_summary.csv`
- Output file: `output/exports/003_prepare_android_safety_forms/android_category_summary.csv`

### Stage 4: Harmonize Cross-Store Disclosures

This stage maps iOS disclosure indicators into the common-label space using the privacy-label abbreviation table and maps Android disclosure indicators into the same label space using the Android-to-iOS translation table. It then builds cross-platform comparison tables.

Primary outputs:

- Output file: `output/exports/004_harmonize_cross_store_disclosures/harmonized_ios_disclosures_long.csv`
- Output file: `output/exports/004_harmonize_cross_store_disclosures/harmonized_android_disclosures_long.csv`
- Output file: `output/exports/004_harmonize_cross_store_disclosures/cross_platform_common_label_summary.csv`
- Output file: `output/exports/004_harmonize_cross_store_disclosures/platform_disclosure_summary.csv`

## Repository Structure

```text
privacy-disclosures-pipeline/
├── .env
├── .env.example
├── .gitignore
├── README.md
├── pyproject.toml
├── requirements.txt
├── scripts/
│   ├── 001_prepare_reference_data.py
│   ├── 002_prepare_ios_privacy_labels.py
│   ├── 003_prepare_android_safety_forms.py
│   ├── 004_harmonize_cross_store_disclosures.py
│   ├── 00A_run_all.py
│   ├── check_env.py
│   ├── run_pipeline.py
│   └── setup_env.py
├── src/
│   └── project/
│       ├── __init__.py
│       ├── config.py
│       ├── env.py
│       ├── io.py
│       ├── logger.py
│       ├── paths.py
│       ├── settings.py
│       ├── utils.py
│       ├── validation.py
│       ├── analysis/
│       │   ├── __init__.py
│       │   └── summary_statistics.py
│       ├── disclosures/
│       │   ├── __init__.py
│       │   ├── harmonization.py
│       │   └── taxonomies.py
│       └── pipelines/
│           ├── __init__.py
│           ├── harmonize_cross_store_disclosures.py
│           ├── prepare_android_safety_forms.py
│           ├── prepare_ios_privacy_labels.py
│           └── prepare_reference_data.py
├── tests/
│   ├── conftest.py
│   ├── test_harmonization.py
│   ├── test_prepare_android_safety_forms.py
│   ├── test_prepare_ios_privacy_labels.py
│   ├── test_summary_statistics.py
│   ├── test_taxonomies.py
│   └── test_validation.py
├── input/
│   ├── android_safety_forms_sample/
│   ├── ios_privacy_labels_sample/
│   └── reference/
└── output/
    ├── exports/
    ├── figures/
    ├── logs/
    └── tables/
```

## Setup

Create and activate a local virtual environment if you want an isolated project environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Then run:

```bash
python3 scripts/setup_env.py
```

On the first run, `scripts/setup_env.py` copies `.env.example` to a repo-local `.env` if the file does not already exist. The setup script also creates the expected project directories and installs the packages listed in `requirements.txt`.

## Run The Pipeline

Run the full pipeline:

```bash
python3 scripts/run_pipeline.py --all
```

Run a single stage:

```bash
python3 scripts/run_pipeline.py --stage 004_harmonize_cross_store_disclosures
```

Each script can also be run directly, but later stages depend on prior-stage outputs being present.

## Required Inputs

- IOS privacy-label sample export at `IOS_PRIVACY_LABELS_PATH`
- Android safety-form sample export at `ANDROID_SAFETY_FORMS_PATH`
- Android-to-IOS taxonomy translation table at `ANDROID_TO_IOS_MAP_PATH`
- Privacy-label abbreviation file at `PRIVACY_LABEL_ABBREVIATIONS_PATH`
- App metadata sample at `APP_META_PATH`
- Platform app log sheet sample at `APP_LOG_SHEET_PATH`

Raw inputs and generated outputs are ignored by the top-level `.gitignore`. The repo expects local files under `input/` or paths set through the repo-local `.env`.

If you keep the inputs inside the repository, the expected local structure is:

```text
input/
├── ios_privacy_labels_sample/
│   └── ios_privacy_labels_sample.csv
├── android_safety_forms_sample/
│   └── android_safety_forms_sample.csv
└── reference/
    ├── android_to_ios_taxonomy_map_sample.csv
    ├── app_log_sheet_sample.csv
    ├── app_meta_sample.csv
    └── privacy_label_term_abbr_sample.xlsx
```

## Input Data Examples

The sample input files are wide. The two platform exports contain base app fields plus hundreds of taxonomy-generated indicator columns. The exact indicator-column sets are defined by the Stage 1 taxonomy outputs.

At a high level, the underlying source data looks different on each platform:

- On the App Store, the privacy disclosure appears as a nested disclosure section for each app. The page groups items under headings such as `Data Used to Track You`, `Data Linked to You`, and `Data Not Linked to You`, then nests those under purposes such as `App Functionality` or `Analytics`, and then under data-type and data-item labels such as `Contact Info -> Email Address`.
- On Google Play, the data safety disclosure appears as a structured disclosure section for each app. The page groups items under headings such as `Data shared`, `Data collected`, and `Security practices`, then nests those under categories such as `Location` or `App activity`, then under data types such as `Approximate location` or `App interactions`, and then under purposes such as `Analytics` or `App functionality`.

The bundled inputs in this repo were prepared as local sample files for this pipeline:

- Sample file: `ios_privacy_labels_sample.csv` is a sample iOS privacy-label export.
- Sample file: `android_safety_forms_sample.csv` is a sample Android safety-form export.
- Sample file: `android_to_ios_taxonomy_map_sample.csv` and `privacy_label_term_abbr_sample.xlsx` provide the cross-platform taxonomy mappings used by the harmonization stage.
- Sample file: `app_meta_sample.csv` is a filtered metadata sample restricted to app IDs relevant to the bundled platform samples.
- Sample file: `app_log_sheet_sample.csv` is a sample platform registry sheet used for reference and validation.

So in this repository, the “raw” inputs are raw relative to the harmonization pipeline itself: they are exported versions of those store-page disclosures and supporting reference files, not live store pages.

### Example iOS Raw Export Base Columns

These columns appear before the generated disclosure indicators in the iOS export.

| app_id | Platform | App_Name | Seller | Category | Price | Languages | App_Information | Version_History | Privacy_Labels | URL | NoDetailsProvided | DataNotCollected |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1000000001` | `iOS` | `Sample Health Tracker 12+` | `Example Mobile Labs` | `Health & Fitness` | `Free` | `English` | `Short app description...` | `Version 2.1; Version 2.0` | `Data Used to Track You ...` | `https://apps.apple.com/...` | `0` | `0` |
| `1000000002` | `iOS` | `Demo Weather Notes 4+` | `Northshore Apps` | `Weather` | `Free` | `English` | `Short app description...` | `Version 1.4; Version 1.3` | `No Details Provided` | `https://apps.apple.com/...` | `1` | `0` |

Representative generated indicator columns:

| DataUsedtoTrackYou_Identifiers_UserID | DataLinkedtoYou_AppFunctionality_ContactInfo_EmailAddress | DataLinkedtoYou_Analytics_UsageData_ProductInteraction | DataNotLinkedtoYou_Third-PartyAdvertising_Diagnostics_CrashData |
| --- | --- | --- | --- |
| `1` | `0` | `1` | `0` |
| `0` | `0` | `0` | `0` |

### Example Android Raw Export Base Columns

These columns appear before the generated disclosure indicators in the Android export.

| app_id | Platform | App_Name | Seller | Safety_Forms | URL | Nodatacollected | Nodatasharedwiththirdparties |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `com.example.notes` | `Android` | `Sample Notes` | `Example Mobile Labs` | `Data shared ...` | `https://play.google.com/...` | `0` | `0` |
| `com.demo.timer` | `Android` | `Demo Focus Timer` | `Northshore Apps` | `No data collected` | `https://play.google.com/...` | `1` | `1` |

Representative generated indicator columns:

| Datashared_Appactivity_Appinteractions_Analytics | Datacollected_Personalinfo_Emailaddress_Appfunctionality | Securitypractices_Dataisencryptedintransit |
| --- | --- | --- |
| `1` | `0` | `1` |
| `0` | `0` | `1` |

### Example `android_to_ios_taxonomy_map_sample.csv`

| item_name | lab1 | lab2 | lab3 | lab4 | label |
| --- | --- | --- | --- | --- | --- |
| `Data collected_App activity_App interactions_Analytics` | `dc` | `UsgData` | `PdIa` | `Anly` | `dc_Anly_UsgData_PdIa` |
| `Data shared_Location_Approximate location_App functionality` | `du2tu` | `Loc` | `CoarseLoc` | `AppFn` | `du2tu_AppFn_Loc_CoarseLoc` |

### Example `privacy_label_term_abbr_sample.xlsx`

| Source Term | Common Label |
| --- | --- |
| `DataUsedtoTrackYou_Contact Info_Name` | `du2tu_CtcIf_Name` |
| `DataLinkedtoYou_Analytics_Usage Data_Product Interaction` | `dl2u_Anly_UsgData_PdIa` |

### Example `app_meta_sample.csv`

| app_id | publisher_id | cross_store_app_id | parent_company_id | category_ids | category_id | category_name | subcategory_id | subcategory_name | age_restrictions | initial_release_date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `com.example.notes` | `1001` | `1000000001` | `9001` | `[39,25]` | `39` | `Applications` | `25` | `Productivity` | `Everyone` | `14oct2014` |
| `1000000001` | `1002` | `` | `9002` | `[2,6]` | `2` | `Health & Fitness` | `6` | `Health` | `12+` | `02jan2019` |

## Output Structure

The pipeline writes stage outputs under:

```text
output/
├── exports/
│   ├── 001_prepare_reference_data/
│   ├── 002_prepare_ios_privacy_labels/
│   ├── 003_prepare_android_safety_forms/
│   └── 004_harmonize_cross_store_disclosures/
└── logs/
```

## Output Examples

### Example `ios_privacy_labels_map.csv`

| Column Name | Element | Privacy Label | Data Use | Data Type | Data Item |
| --- | --- | --- | --- | --- | --- |
| `DataUsedtoTrackYou_Identifiers_UserID` | `Data Used to Track You -> Identifiers -> User ID` | `Data Used to Track You` | `` | `Identifiers` | `User ID` |
| `DataLinkedtoYou_AppFunctionality_ContactInfo_EmailAddress` | `Data Linked to You -> App Functionality -> Contact Info -> Email Address` | `Data Linked to You` | `App Functionality` | `Contact Info` | `Email Address` |

### Example `android_safety_forms_map.csv`

| Column Name | Item Name | Element | Safety Form | Security Practice | Data Category | Data Type | Data Purpose |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Datashared_Location_Approximatelocation_Accountmanagement` | `Data shared_Location_Approximate location_Account management` | `Data shared -> Location -> Approximate location -> Account management` | `Data shared` | `` | `Location` | `Approximate location` | `Account management` |
| `Securitypractices_Dataisencryptedintransit` | `Data is encrypted in transit` | `Security practices -> Data is encrypted in transit` | `Security practices` | `Data is encrypted in transit` | `` | `` | `` |

### Example `prepared_ios_privacy_labels.csv`

This file retains the full raw iOS export schema and appends:

- `Disclosure Indicator Count`
- `Positive Disclosure Columns`
- Field: `category_name`
- Field: `subcategory_name`
- Field: `cross_store_app_id`
- Field: `initial_release_date`
- `Metadata Match Found`

Example appended fields:

| app_id | App_Name | Disclosure Indicator Count | Positive Disclosure Columns | category_name | subcategory_name | cross_store_app_id | initial_release_date | Metadata Match Found |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `1000000001` | `Sample Health Tracker 12+` | `3` | `DataUsedtoTrackYou_Identifiers_UserID \| DataLinkedtoYou_Analytics_UsageData_ProductInteraction` | `Health & Fitness` | `Health` | `` | `02jan2019` | `1` |
| `1000000002` | `Demo Weather Notes 4+` | `1` | `NoDetailsProvided` | `Applications` | `Weather` | `` | `15feb2020` | `1` |

### Example `prepared_android_safety_forms.csv`

This file retains the app-level Android export schema after deduplication and appends:

- `Disclosure Indicator Count`
- `Positive Disclosure Columns`
- Field: `category_name`
- Field: `subcategory_name`
- Field: `cross_store_app_id`
- Field: `initial_release_date`
- `Metadata Match Found`

Example appended fields:

| app_id | App_Name | Disclosure Indicator Count | Positive Disclosure Columns | category_name | subcategory_name | cross_store_app_id | initial_release_date | Metadata Match Found |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `com.example.notes` | `Sample Notes` | `4` | `Datashared_Appactivity_Appinteractions_Analytics \| Securitypractices_Dataisencryptedintransit` | `Applications` | `Productivity` | `1000000001` | `14oct2014` | `1` |
| `com.demo.timer` | `Demo Focus Timer` | `2` | `Nodatacollected \| Nodatasharedwiththirdparties` | `Applications` | `Productivity` | `` | `11mar2021` | `1` |

### Example `harmonized_ios_disclosures_long.csv`

| app_id | App_Name | Seller | category_name | Source Column | Indicator Value | Platform | Common Label |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `1000000001` | `Sample Health Tracker 12+` | `Example Mobile Labs` | `Health & Fitness` | `DataUsedtoTrackYou_Identifiers_UserID` | `1` | `iOS` | `du2tu_Idf_UserID` |
| `1000000002` | `Demo Weather Notes 4+` | `Northshore Apps` | `Weather` | `NoDetailsProvided` | `1` | `iOS` | `ndp` |

### Example `harmonized_android_disclosures_long.csv`

| app_id | App_Name | Seller | category_name | Source Column | Indicator Value | Platform | Item Name | Common Label |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `com.example.notes` | `Sample Notes` | `Example Mobile Labs` | `Applications` | `Datashared_Appactivity_Appinteractions_Analytics` | `1` | `Android` | `Data shared_App activity_App interactions_Analytics` | `du2tu_UsgData_PdIa` |
| `com.demo.timer` | `Demo Focus Timer` | `Northshore Apps` | `Applications` | `Nodatacollected` | `1` | `Android` | `No data collected` | `UNMAPPED` |

### Example `cross_platform_common_label_summary.csv`

| Common Label | Android App Count | iOS App Count | Total App Count |
| --- | --- | --- | --- |
| `dnc` | `1` | `4` | `5` |
| `dl2u_Anly_Id_UserID` | `0` | `4` | `4` |

### Example `platform_disclosure_summary.csv`

| section | metric | value | notes |
| --- | --- | --- | --- |
| `harmonized_ios` | `positive_common_label_rows` | `68` | `Positive iOS disclosure rows after mapping to common labels.` |
| `harmonized_android` | `positive_common_label_rows` | `33` | `Positive Android disclosure rows after mapping to common labels.` |

## Configuration

The repository ships with a tracked `.env.example` template. `scripts/setup_env.py` copies that template to a local `.env` on first run, and you can then edit `.env` for machine-specific paths or row limits.

The main runtime settings are:

- `IOS_PRIVACY_LABELS_PATH`
- `ANDROID_SAFETY_FORMS_PATH`
- `ANDROID_TO_IOS_MAP_PATH`
- `PRIVACY_LABEL_ABBREVIATIONS_PATH`
- `APP_META_PATH`
- `APP_LOG_SHEET_PATH`
- `MAX_IOS_ROWS`
- `MAX_ANDROID_ROWS`
- `RUNTIME_MODE`

## Tests

Run the unit tests with:

```bash
python3 -m pytest
```

The test suite is unit-level. It covers taxonomy construction, platform preparation, harmonization, validation, and summary-statistics helpers, but it does not act as a full integration test of every written output file.

## Limitations

- The repo is designed around bundled sample exports and reference files, not live store scraping.
- The iOS and Android raw exports are intentionally wide and can be cumbersome to inspect directly without the Stage 1 taxonomy maps.
- The bundled Android sample is smaller than the bundled iOS sample, so the cross-platform comparison is illustrative rather than balanced.
- Some Android rows may remain `UNMAPPED` in the harmonized output when a direct common-label translation is unavailable.
