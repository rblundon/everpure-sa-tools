# SafeMode Volume Protection Chart Generator

## Goal
Build a Python CLI tool that reads the SafeMode volume spreadsheet (produced by the parser) and generates SVG donut charts showing volume protection status per array. Charts are brand-compliant using the Everpure/Pure Storage color system.

## Input
- Path to the SafeMode report spreadsheet (`.xlsx`) produced by the parser
- The spreadsheet has one worksheet with columns: Array, Volume Name, Provisioned, Effective Used, Max Snap Window, In SafeMode PGroup, Exclude, Reason, Risk Level
- Risk Level values: `PROTECTED`, `PROTECTED (NOT BP)`, `AT RISK`, `CRITICAL`, `EXCLUDED`

## Output
One or more SVG files per array, depending on the `--mode` flag:
- `--mode count` → one SVG per array showing volume count by risk level
- `--mode capacity` → one SVG per array showing effective capacity by risk level  
- `--mode both` → one SVG per array with side-by-side donut charts (count + capacity)

Output directory specified by `--output-dir`.

Filename format: `{array_name}_{mode}.svg`

## CLI Usage
```bash
python safemode_charts.py --input ./safemode_report.xlsx --output-dir ./charts --mode both
```

Optional flags:
- `--arrays array1,array2` — generate charts for specific arrays only (default: all)
- `--exclude-from-chart` — if set, volumes marked as Excluded are removed from the chart entirely (default: show as gray "Excluded" slice)
- `--min-pct 2` — slices below this percentage get merged into an "Other" category to keep the chart clean (default: 0, show all)

## Design Specification

### Visual Reference
See the HTML files in `examples/` for the design language being targeted. Key characteristics:
- Donut charts (not solid pies) with a center cutout showing the "protected" percentage
- Clean, modern aesthetic on a cream (#FFF5E3) or white background
- Rounded edges on all elements
- Breakdown legend below each chart

### Color System
Import colors from `everpure_colors.py` (included in the project). Use the `CHART_PALETTE` and `STATUS_COLORS` dictionaries for risk-level-to-color mapping:

| Risk Level | Chart Fill Color | Source |
|---|---|---|
| PROTECTED | Mint Green `#C5E4CC` | `CHART_PALETTE["protected"]` |
| PROTECTED (NOT BP) | Moss Green `#8FA596` | `CHART_PALETTE["protected_not_bp"]` |
| AT RISK | Pure Orange `#FF7023` | `CHART_PALETTE["at_risk"]` |
| CRITICAL | Quartz Pink `#DEA193` | `CHART_PALETTE["critical"]` |  
| EXCLUDED | Stone Gray `#D0C8BA` | `CHART_PALETTE["excluded"]` |

### Typography
- Use "Pure Sans" font (files in `fonts/` directory). If not available, fall back to Arial or sans-serif.
- Embed the font in the SVG using `@font-face` in a `<style>` block with base64-encoded font data, OR reference it as a font-family with a fallback.
- Array name: 20px, bold, Ash Gray `#2D2A27`
- Subtitle (e.g., "87 volumes | 203.88 TB capacity"): 12px, regular, Walnut Brown `#71584C`
- Center percentage: 28px, bold, color matches protection level (green if ≥80%, orange if ≥50%, pink/red if <50%)
- Center label "protected": 10px, regular, Walnut Brown `#71584C`
- Chart title ("By Volume Count" / "By Effective Capacity"): 14px, bold uppercase, Walnut Brown `#71584C`, 0.5px letter-spacing
- Breakdown labels: 12px, regular, Ash Gray `#2D2A27`
- Breakdown values: 12px, bold, Ash Gray `#2D2A27`

### SVG Layout

#### Single mode (`count` or `capacity`)
```
Width: 360px, Height: auto (depends on breakdown rows)

┌──────────────────────────────────────┐
│  Array Name                          │  ← 20px bold
│  87 volumes | 203.88 TB capacity     │  ← 12px subtitle
│                                      │
│         BY VOLUME COUNT              │  ← 14px bold uppercase
│                                      │
│          ┌─────────┐                 │
│         │  ██████  │                 │  ← donut chart, 180px diameter
│         │  9%     │                 │  ← center text
│         │ protected│                 │
│          └─────────┘                 │
│                                      │
│  ● Protected          8 vols (9%)    │  ← breakdown rows
│  ● At Risk           10 vols (11%)   │
│  ● Critical          69 vols (79%)   │
│  ─────────────────────────────────── │
│  Total                87 vols        │
└──────────────────────────────────────┘
```

#### Both mode (side-by-side)
```
Width: 700px, Height: auto

┌─────────────────────────────────────────────────────────────────┐
│  Array Name                                                     │
│  87 volumes | 203.88 TB capacity                                │
│                                                                 │
│    BY VOLUME COUNT           BY EFFECTIVE CAPACITY               │
│                                                                 │
│      ┌────────┐                ┌────────┐                       │
│     │  9%    │              │  <0.1% │                       │
│      └────────┘                └────────┘                       │
│                                                                 │
│  ● Protected    8 (9%)     ● Protected    0.002 TB (<0.1%)      │
│  ● At Risk     10 (11%)    ● At Risk     53.66 TB (66%)         │
│  ● Critical    69 (79%)    ● Critical    27.09 TB (34%)         │
│  ────────────────────────  ──────────────────────────────        │
│  Total         87          Total         80.75 TB                │
└─────────────────────────────────────────────────────────────────┘
```

### Donut Chart Specifications
- Outer radius: 90px (180px diameter)
- Inner radius: 50px (donut hole)
- Stroke between slices: 2px, white (#FFFFFF)
- **Rounded ends on donut slices**: use `stroke-linecap: round` on the arc paths
- Slices drawn as SVG `<path>` arcs, ordered from largest to smallest
- If a single category is 100%, render as a full circle (no arc gaps)
- Minimum arc angle for visibility: 3 degrees (below this, merge into "Other")

### Card Styling
- Background: white `#FFFFFF` with rounded corners (`rx="12"`)
- Subtle drop shadow: `<filter>` with `feDropShadow` — `dx=0 dy=2 stdDeviation=4` at 8% opacity
- Padding: 32px all sides
- Accent bar: 3px tall Pure Orange `#FF7023` bar at the very top of the card, full width, with rounded top corners matching the card

### Breakdown Legend
- Small colored circle (8px diameter) next to each label
- Right-aligned value with percentage in parentheses
- Total row separated by a 1px line in Stone Gray `#D0C8BA`
- Only show risk levels that have non-zero values

### Capacity Formatting
- Values ≥ 1 TB: display as `X.XX TB`
- Values ≥ 1 GB but < 1 TB: display as `X.XX GB`  
- Values < 1 GB: display as `X.XX MB`
- Percentages: round to nearest integer, but show `<0.1%` for very small non-zero values

### Center Percentage Logic
The center percentage shows **only PROTECTED volumes** (not PROTECTED (NOT BP), not AT RISK):
- PROTECTED count or capacity / total count or capacity × 100
- Color: Mint Green `#C5E4CC` if ≥80%, Pure Orange `#FF7023` if ≥50%, Quartz Pink `#DEA193` if <50%
- Display: integer percentage, or `<1%` for values between 0 and 1

## Data Processing

### Effective Used Parsing
The Effective Used column contains human-readable sizes like `9.53T`, `225.88M`, `971.24M`, `1.93T`, `802.21M`. The parser should convert these to a common unit (TB) for capacity calculations:
- `T` suffix → value in TB
- `G` suffix → value / 1024 TB
- `M` suffix → value / (1024 × 1024) TB
- If the value is just a number, assume bytes

### Aggregation
For each array, group volumes by Risk Level and calculate:
- **Count**: number of volumes in each risk level
- **Capacity**: sum of Effective Used (in TB) for each risk level

Volumes with Risk Level = `EXCLUDED` are either:
- Shown as a gray slice (default)
- Removed entirely if `--exclude-from-chart` is set

### Subtitle Generation
Auto-generate from the data:
- Total volume count (excluding EXCLUDED if `--exclude-from-chart`)
- Total effective capacity formatted appropriately
- Example: `"87 volumes  |  80.75 TB effective"`

## SVG Quality Requirements
- All text should use `dominant-baseline` and `text-anchor` for precise positioning
- Use `viewBox` for scalability — SVGs should render crisply at any size
- No external dependencies — the SVG should be fully self-contained
- Colors must exactly match the `everpure_colors.py` values
- Anti-aliasing: use `shape-rendering="geometricPrecision"` on the root SVG

## Dependencies
- Python 3.10+
- openpyxl (for reading the xlsx)
- math (stdlib, for arc calculations)
- base64 (stdlib, for font embedding if needed)
- No matplotlib — generate raw SVG strings directly for maximum control

## File Structure
```
safemode_charts.py          # Main CLI tool
everpure_colors.py          # Color matrix (provided)
fonts/                      # Pure Sans font files
examples/                   # HTML reference files
  volume_protection_dual.html
  safemode_comparison.html
```

## Testing
Run against the ashbpasan001 spreadsheet and verify:
- SVG renders correctly in a browser
- Donut slices sum to 360 degrees
- Breakdown values match the chart slices
- Center percentage matches PROTECTED / total
- Colors match the brand spec exactly
- Font renders correctly (or falls back gracefully)
- Both single and dual chart modes produce valid SVG
