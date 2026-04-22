# Modification: Excluded Volume Handling

## Summary
Modify the existing `safemode_charts.py` to remove excluded volumes from the donut chart calculations and display them as a footnote instead of a chart slice.

## Current Behavior
Excluded volumes are shown as a gray slice in the donut chart, counted in the total, and included in percentage calculations.

## New Behavior

### 1. Remove excluded volumes from the donut chart
- Volumes with Risk Level = `EXCLUDED` are **not** rendered as a pie slice
- The donut chart only shows: PROTECTED, PROTECTED (NOT BP), AT RISK, CRITICAL
- All percentages are recalculated against the **non-excluded total** (both count and capacity)
- The center percentage is recalculated against the non-excluded total

### 2. Remove excluded volumes from the breakdown legend
- The breakdown rows only list non-excluded risk levels
- The Total row at the bottom reflects the non-excluded total
- Example:
  ```
  ● Protected        8 vols (31%)
  ● At Risk         10 vols (38%)
  ● Critical         8 vols (31%)
  ─────────────────────────────────
  Total              26 vols
  ```

### 3. Add an exclusion footnote
If any volumes are excluded, add a footnote line **below** the total row with:
- The count of excluded volumes
- The total effective capacity of excluded volumes
- Styled distinctly from the breakdown rows

Format:
```
ℹ {count} volumes excluded ({capacity})
```

Example:
```
ℹ 61 volumes excluded (3.3 TB)
```

#### Footnote styling:
- Font size: 11px, regular weight
- Color: Walnut Brown `#71584C` (same as `TEXT_SECONDARY` from `everpure_colors.py`)
- Prefix with an info icon — use the literal character `ℹ` or a small SVG circle-i icon in Stone Gray `#D0C8BA`
- Add 8px top margin between the total row divider and the footnote
- If zero volumes are excluded, do not render the footnote at all

### 4. Update the subtitle
The subtitle should reflect the non-excluded counts:
```
{non_excluded_count} volumes  |  {non_excluded_capacity} effective
```

If there are exclusions, do NOT mention them in the subtitle — the footnote handles that.

### 5. Remove the `--exclude-from-chart` flag
This flag is no longer needed since excluding from the chart is now the default (and only) behavior. Remove it from argparse and any related conditional logic.

## Example: ashbpasan001

### Before (current behavior with gray slice):
```
Chart shows 87 volumes total
● Protected         8 vols  (9%)
● At Risk          10 vols (11%)
● Critical         69 vols (79%)
● Excluded          0 vols  (0%)    ← gray slice if any
Total              87 vols
```

### After (new behavior, assuming 61 volumes excluded):
```
Chart shows 26 volumes
● Protected         8 vols (31%)
● At Risk          10 vols (38%)
● Critical          8 vols (31%)
─────────────────────────────────
Total              26 vols

ℹ 61 volumes excluded (3.3 TB)
```

## Side-by-side mode (`--mode both`)
Apply the same logic to both charts independently. The footnote only needs to appear once, below the left chart's breakdown (or centered below both if layout allows). Both charts share the same exclusion set since it's the same array.

## Edge Cases
- **All volumes excluded**: Display an empty donut (full circle in Stone Gray `#D0C8BA`) with center text "N/A" and footnote showing all volumes excluded. No breakdown rows.
- **No volumes excluded**: No footnote rendered. Behavior identical to current output.
- **100% of non-excluded volumes in one category**: Render as a full circle in that category's color (no arc gap needed).

## Files to Modify
- `safemode_charts.py` — main changes
- No changes needed to `everpure_colors.py`
