# everpure-sa-tools

Python CLI tools for Pure Storage FlashArray SafeMode analysis and reporting.

---

## Setup

Run once to create the virtual environment and install dependencies:

```bash
bash setup.sh
source .venv/bin/activate
```

---

## safemode_parser.py

Parses Pure Storage FlashArray CLI output files and produces a formatted Excel workbook (`.xlsx`) with volume-level SafeMode protection analysis.

### Input folder structure

```
cli_dumps/
├── ashbpasan001/
│   ├── purearray-eradication-config-list.out
│   ├── purearray-list.out
│   ├── purearray-list-space-effective.out
│   ├── purearray-list-space-physical.out
│   ├── purehgroup-list-connect.out
│   ├── purepgroup-list.out
│   ├── purepgroup-list-retention.out
│   ├── purepgroup-list-retention-lock-pending.out
│   ├── purepgroup-list-schedule.out
│   ├── purepgroup-list-space-total.out
│   └── purevol-list.out
├── utilidor/
│   └── ...
└── (one subfolder per array)
```

### Output columns

| Column | Description |
|---|---|
| Array | Array hostname |
| Volume Name | Volume name |
| Provisioned | Provisioned size |
| Effective Used | Effective total used capacity |
| Max Snap Window | Maximum days of snapshot coverage across all pgroups |
| In SafeMode PGroup | `Yes` if member of at least one ratcheted pgroup |
| Exclude | `x` to exclude from risk calculations (persisted across runs) |
| Reason | Free-text reason for exclusion (persisted across runs) |
| Risk Level | Excel formula: `PROTECTED`, `PROTECTED (NOT BP)`, `AT RISK`, `CRITICAL`, or `EXCLUDED` |

### First run

```bash
python safemode_parser.py \
  --input-dir ./cli_dumps \
  --output ./safemode_report.xlsx
```

### Subsequent runs (preserves Exclude/Reason edits)

If `--output` points to an existing file, Exclude and Reason values are automatically read back from it before overwriting:

```bash
python safemode_parser.py \
  --input-dir ./cli_dumps \
  --output ./safemode_report.xlsx
```

To read persist data from a different file than the output:

```bash
python safemode_parser.py \
  --input-dir ./cli_dumps \
  --output ./safemode_report_new.xlsx \
  --existing ./safemode_report.xlsx
```

### All flags

| Flag | Description |
|---|---|
| `--input-dir` | Root folder containing one subfolder per array (required) |
| `--output` | Output `.xlsx` path (required) |
| `--existing` | Alternate `.xlsx` to read Exclude/Reason from |

---

## safemode_charts.py

Reads the SafeMode report spreadsheet and generates per-array SVG donut charts showing volume protection status. Uses the Everpure/Pure Storage brand color system and Pure Sans font.

### Chart modes

| Mode | Output | Description |
|---|---|---|
| `count` | One SVG per array | Donut by volume count |
| `capacity` | One SVG per array | Donut by effective capacity |
| `both` | One SVG per array | Side-by-side count + capacity donuts |

Output files are named `{array_name}_{mode}.svg`.

### Examples

```bash
# Both donuts side-by-side (default)
python safemode_charts.py \
  --input ./safemode_report.xlsx \
  --output-dir ./charts \
  --mode both

# Volume count only
python safemode_charts.py \
  --input ./safemode_report.xlsx \
  --output-dir ./charts \
  --mode count

# Effective capacity only
python safemode_charts.py \
  --input ./safemode_report.xlsx \
  --output-dir ./charts \
  --mode capacity

# Specific arrays only
python safemode_charts.py \
  --input ./safemode_report.xlsx \
  --output-dir ./charts \
  --mode both \
  --arrays ashbpasan001,utilidor

# Remove excluded volumes from charts entirely
python safemode_charts.py \
  --input ./safemode_report.xlsx \
  --output-dir ./charts \
  --mode both \
  --exclude-from-chart
```

### All flags

| Flag | Description |
|---|---|
| `--input` | SafeMode report `.xlsx` (required) |
| `--output-dir` | Directory for output SVG files (required) |
| `--mode` | `count`, `capacity`, or `both` (default: `both`) |
| `--arrays` | Comma-separated list of array names to include |
| `--exclude-from-chart` | Remove excluded volumes from charts entirely (default: show as gray slice) |
| `--min-pct` | Merge slices below this percentage into Other (default: `0`) |
| `--font-dir` | Path to PureSans `.ttf` files (default: `fonts/Pure_Sans/`) |

### Color reference

| Risk Level | Color | Hex |
|---|---|---|
| Protected | Mint Green | `#C5E4CC` |
| Protected (Not BP) | Moss Green | `#8FA596` |
| At Risk | Pure Orange | `#FF7023` |
| Critical | Clay Pink | `#95685D` |
| Excluded | Stone Gray | `#D0C8BA` |

---

## Running tests

```bash
pytest tests/
```

---

## Full workflow example

```bash
# 1. Set up environment
bash setup.sh
source .venv/bin/activate

# 2. Parse CLI dumps into Excel
python safemode_parser.py --input-dir ./cli_dumps --output ./safemode_report.xlsx

# 3. (Optional) Open safemode_report.xlsx, fill in Exclude/Reason columns, save

# 4. Re-run parser to refresh data while preserving your edits
python safemode_parser.py --input-dir ./cli_dumps --output ./safemode_report.xlsx

# 5. Generate SVG charts
python safemode_charts.py --input ./safemode_report.xlsx --output-dir ./charts --mode both
```
