# Pure Storage FlashArray SafeMode Parser

## Goal
Build a Python CLI tool that parses Pure Storage FlashArray CLI text output files and produces a single Excel workbook (.xlsx) with volume-level protection analysis.

## Input
- A root folder path containing one subfolder per array
- Each subfolder is named after the array (e.g., `ashbpasan001/`) and contains individual command output files
- Optionally, a path to an existing output spreadsheet (for persisting Exclude/Reason flags across runs)

### Expected folder structure
```
cli_dumps/
├── ashbpasan001/
│   ├── purearray-eradication-config-list.out
│   ├── purearray-list-space-effective.out
│   ├── purearray-list-space-physical.out
│   ├── purearray-list.out
│   ├── purehgroup-list-connect.out
│   ├── purepgroup-list-retention-lock-pending.out
│   ├── purepgroup-list-retention.out
│   ├── purepgroup-list-schedule.out
│   ├── purepgroup-list-space-total.out
│   ├── purepgroup-list.out
│   └── purevol-list.out
├── utilidor/
│   ├── purearray-eradication-config-list.out
│   ├── ...
│   └── purevol-list.out
└── (35 arrays total)
```

- The **array name** is derived from the subfolder name
- Each `.out` file contains the raw CLI output for that specific command (no timestamp headers needed — the filename identifies the command)
- If a file is missing from a subfolder, log a warning and continue with available data

## Output
A single `.xlsx` file with one worksheet containing all volumes across all arrays.

### Columns

| Column | Source | Description |
|---|---|---|
| Array | parsed from filename | Array hostname |
| Volume Name | `purevol list` | Volume name |
| Provisioned | `purevol list` | Provisioned size (e.g., `10T`, `300G`) |
| Effective Used | `purevol list` | Effective total column from `purevol list --space --effective --total --pending` |
| Max Snap Window | calculated | Maximum number of days of snapshot coverage this volume has across all protection groups it belongs to. 0 if not in any pgroup. See calculation logic below. |
| In SafeMode PGroup | calculated | `Yes` if the volume is a member of at least one ratcheted protection group, `No` otherwise |
| Exclude | persisted | `x` if excluded from risk calculations. Persisted from previous run. |
| Reason | persisted | Free-text reason for exclusion. Persisted from previous run. |
| Risk Level | Excel formula | See formula below |

### Risk Level Formula (Excel)
Assuming row 2, Exclude=G2, In SafeMode PGroup=F2, Max Snap Window=E2:
```
=IF(G2="x","EXCLUDED",IF(F2="No",IF(E2=0,"CRITICAL","AT RISK"),IF(E2>=14,"PROTECTED","PROTECTED (NOT BP)")))
```

## Max Snap Window Calculation
For each protection group a volume belongs to, calculate the total snapshot retention window on source:
- `All For` + `Days` from `purepgroup list --retention` (source row only)
- Example: `All For = 3d`, `Per Day = 1`, `Days = 5` → total = 3 + 5 = 8 days
- Example: `All For = 2w`, `Per Day = 0`, `Days = 0` → total = 14 days
- Example: `All For = 1d`, `Per Day = 1`, `Days = 7` → total = 1 + 7 = 8 days

If a volume is in multiple protection groups, use the maximum snap window across all of them.

If a volume is not in any protection group, Max Snap Window = 0.

## Volume-to-PGroup Membership Resolution
Volumes can be members of a protection group in two ways:

1. **Direct membership**: volume name appears in the Volumes column of `purepgroup list`
2. **Host group membership**: the pgroup lists a Host Group in the `Host Groups` column. To resolve which volumes belong to that host group, use the output of `purehgroup list --connect --csv`, which maps host groups to their connected volumes.

### Resolution chain for host group membership:
```
purepgroup list → Host Group name → purehgroup list --connect --csv → Volume names
```

### Example:
- `purepgroup list` shows `ASH-Pre-Prod-VM-PG` has Host Group `ASHB-ESX-GC-D-HG`
- `purehgroup list --connect --csv` shows:
  ```
  ASHB-ESX-GC-D-HG,245,ashbd-gc-245-A01-n
  ASHB-ESX-GC-D-HG,246,ashbd-gc-246-A01-n
  ```
- Therefore `ashbd-gc-245-A01-n` and `ashbd-gc-246-A01-n` are members of `ASH-Pre-Prod-VM-PG`

### Fallback:
If `purehgroup list --connect --csv` output is not present in the file, log a warning that host-group-to-volume resolution could not be completed for any pgroups using host group membership. Those volumes will show as unprotected (Max Snap Window = 0, In SafeMode PGroup = No) which may overstate risk. The warning should include the pgroup name and host group name so the user knows what data is missing.

### Multi-pgroup membership:
A volume can be a member of multiple protection groups (directly, via host group, or both). When calculating Max Snap Window and In SafeMode PGroup, evaluate ALL pgroups the volume belongs to and use the best values:
- Max Snap Window = maximum across all pgroups
- In SafeMode PGroup = Yes if ANY pgroup is ratcheted

**Note on SafeMode best practice**: pgroups with host group membership (rather than direct volume membership) can cause operational friction when SafeMode is enabled, since host changes get blocked. This is worth flagging but does not change the protection status calculation.

## Persist Logic
1. If an existing spreadsheet path is provided, read it and build a dictionary keyed on `(Array, Volume Name)` → `(Exclude, Reason)`
2. After parsing all CLI files and building the new volume list, carry over Exclude and Reason values for any matching `(Array, Volume Name)` key
3. Volumes no longer present in the CLI output are dropped (not carried forward)
4. New volumes get empty Exclude and Reason fields

## File-to-Command Mapping
Each file in an array's subfolder maps to a specific CLI command:

| Filename | CLI Command |
|---|---|
| `purearray-list.out` | `purearray list` |
| `purearray-list-space-physical.out` | `purearray list --space --physical` |
| `purearray-list-space-effective.out` | `purearray list --space --effective` |
| `purearray-eradication-config-list.out` | `purearray eradication-config list` |
| `purepgroup-list.out` | `purepgroup list` |
| `purepgroup-list-retention-lock-pending.out` | `purepgroup list --retention-lock --pending` |
| `purepgroup-list-schedule.out` | `purepgroup list --schedule` |
| `purepgroup-list-retention.out` | `purepgroup list --retention` |
| `purepgroup-list-space-total.out` | `purepgroup list --space --physical --total` |
| `purehgroup-list-connect.out` | `purehgroup list --connect` |
| `purevol-list.out` | `purevol list --space --effective --total --pending` |

### Parsing format notes
Each file contains the raw fixed-width table output from the CLI command, starting with the column header row followed by data rows. Example (`purepgroup-list-retention-lock-pending.out`):
```
Name                       Retention Lock  Manual Eradication
ASH-Pre-Prod-VM-PG         unlocked        disabled
pgroup-auto                ratcheted       disabled
```

Files may optionally be preceded by a dashed separator line and timestamp line like:
```
------------------------------------------------------------------------
Mar 31 06:06:23 purepgroup list
------------------------------------------------------------------------
Name                       Retention Lock  Manual Eradication
...
```
The parser should skip any lines before the column header row (dashed lines, timestamps, blank lines).

The `purehgroup-list-connect.out` file may be in **either** fixed-width or CSV format. If CSV, it will have a header row like `Name,Lun,Vol`. The parser should auto-detect by checking for commas in the header line.

The parser should handle:
- Extra whitespace or blank lines
- The `(total)` summary row in volume listings (exclude from volume list)
- Multi-line volume lists in `purepgroup-list.out` where continuation lines are indented under the Volumes column
- Multi-row pgroups in schedule and retention files where the pgroup name only appears on the first row and subsequent rows for the same pgroup are indented (e.g., `snap` row followed by `replicate` row, or `source` row followed by `target` row)

## CLI Usage
```bash
python safemode_parser.py --input-dir ./cli_dumps --output ./safemode_report.xlsx [--existing ./safemode_report.xlsx]
```

Where `--input-dir` points to the root folder containing one subfolder per array.

## Formatting
- Use openpyxl for Excel generation
- Header row: bold white text on dark background (#3C3C3B)
- Auto-filter enabled on all columns
- Column widths auto-sized to content
- Risk Level column gets conditional formatting:
  - PROTECTED: green background (#C8E6C0)
  - PROTECTED (NOT BP): yellow-green background (#E8F5C8)
  - AT RISK: yellow background (#FFF3C4)
  - CRITICAL: red background (#F8C4C4)
  - EXCLUDED: gray background (#E0E0E0)
- Font: Arial 10pt throughout
- Freeze top row

## Error Handling
- If a CLI command is missing from a file, log a warning and continue with available data
- If the retention format is unrecognized (not `Xd` or `Xw`), log a warning and default to 0
- If no volumes are found in a file, log a warning and skip that array

## Testing
Include a test that runs against a sample array folder `ashbpasan001/` containing the individual `.out` files and validates:
- 87 volumes parsed (excluding the `(total)` row)
- 8 volumes in pgroup-auto with In SafeMode PGroup = Yes
- 0 volumes with Max Snap Window >= 14 (none meet BP threshold)
- pgroup-auto volumes have Max Snap Window = 8
- Risk Level formula is present in every row
- Missing `.out` files produce warnings but don't crash the parser

## Dependencies
- Python 3.10+
- openpyxl
- argparse
- re (stdlib)
