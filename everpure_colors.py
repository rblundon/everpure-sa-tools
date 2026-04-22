# Everpure (Pure Storage) Brand Color Matrix
# Source: Brand Guidelines - Color (April 2026)
# Usage: Import this module for consistent brand-compliant color usage
#        in chart generation, dashboard rendering, and presentation output.

# ═══════════════════════════════════════════════════════════════
# PRIMARY COLOR
# ═══════════════════════════════════════════════════════════════
PURE_ORANGE = "#FF7023"  # PMS 2018 C — hero color, signals action/energy

# ═══════════════════════════════════════════════════════════════
# NEUTRAL PALETTE
# ═══════════════════════════════════════════════════════════════
CLOUD_WHITE = "#FFF5E3"  # PMS 9043 C — backgrounds, breathing room
STONE_GRAY  = "#D0C8BA"  # PMS 2331 C — borders, subtle dividers
ASH_GRAY    = "#2D2A27"  # PMS Black 7 C — primary text, headers

# ═══════════════════════════════════════════════════════════════
# SECONDARY PALETTE
# ═══════════════════════════════════════════════════════════════
# Greens
MINT_GREEN  = "#C5E4CC"  # PMS 566 C
MOSS_GREEN  = "#8FA596"  # PMS 4185 C
BASIL_GREEN = "#5A6359"  # PMS 417 C

# Pinks
ROSE_PINK   = "#F2CDC4"  # PMS 196 C
QUARTZ_PINK = "#DEA193"  # PMS 2338 C
CLAY_PINK   = "#95685D"  # PMS 4040 C

# Browns
CINNAMON_BROWN = "#BD673D"  # PMS 7566 C
WALNUT_BROWN   = "#71584C"  # PMS 4272 C

# ═══════════════════════════════════════════════════════════════
# EXTENDED PALETTE — 10-step tonal ranges (000=lightest, 900=darkest)
# For digital/UI use. Verified from brand portal swatch export.
# ═══════════════════════════════════════════════════════════════

EXTENDED = {
    "pure_orange": {
        "000": "#FFE2D3", "100": "#FFCFB6", "200": "#FFB891", "300": "#FFA06C",
        "400": "#FF8848", "500": "#FF7023",  # = PURE_ORANGE
        "600": "#D55D1D", "700": "#AA4B17", "800": "#803812", "900": "#55250C",
    },
    "cinnamon_brown": {
        "000": "#F2E1D8", "100": "#E9CCBE", "200": "#DEB39E", "300": "#D39A7E",
        "400": "#C8805D", "500": "#BD673D",  # = CINNAMON_BROWN
        "600": "#9E5633", "700": "#7E4529", "800": "#5F341F", "900": "#3F2214",
    },
    "walnut_brown": {
        "000": "#E3DEDB", "100": "#D0C7C3", "200": "#B8ABA5", "300": "#A09088",
        "400": "#89746A", "500": "#71584C",  # = WALNUT_BROWN
        "600": "#5E493F", "700": "#4B3B33", "800": "#392C26", "900": "#261D19",
    },
    "mint_green": {
        "000": "#F3FAF5", "100": "#ECF6EE", "200": "#E2F1E5", "300": "#D8EDDD",
        "400": "#CFE8D4", "500": "#C5E4CC",  # = MINT_GREEN
        "600": "#A4BEAA", "700": "#839888", "800": "#637266", "900": "#424C44",
    },
    "moss_green": {
        "000": "#E9EDEA", "100": "#DAE1DC", "200": "#C7D2CA", "300": "#B4C3B9",
        "400": "#A2B4A7", "500": "#8FA596",  # = MOSS_GREEN
        "600": "#77897D", "700": "#5F6E64", "800": "#48534B", "900": "#303732",
    },
    "basil_green": {
        "000": "#DEE0DE", "100": "#C8CBC8", "200": "#ACB1AC", "300": "#919790",
        "400": "#767D75", "500": "#5A6359",  # = BASIL_GREEN
        "600": "#4B534A", "700": "#3C423B", "800": "#2D322D", "900": "#1E211E",
    },
    "rose_pink": {
        "000": "#FCF5F3", "100": "#FBEEEB", "200": "#F8E6E1", "300": "#F6DED8",
        "400": "#F4D5CE", "500": "#F2CDC4",  # = ROSE_PINK
        "600": "#CAABA3", "700": "#A18983", "800": "#796762", "900": "#514441",
    },
    "quartz_pink": {
        "000": "#F8ECE9", "100": "#F4E0DB", "200": "#EED0C9", "300": "#E9C0B7",
        "400": "#E3B1A5", "500": "#DEA193",  # = QUARTZ_PINK
        "600": "#B9867B", "700": "#946B62", "800": "#6F514A", "900": "#4A3631",
    },
    "clay_pink": {
        "000": "#EAE1DF", "100": "#DCCDC9", "200": "#CAB3AE", "300": "#B89A93",
        "400": "#A78178", "500": "#95685D",  # = CLAY_PINK
        "600": "#7C574E", "700": "#63453E", "800": "#4B342F", "900": "#32231F",
    },
    "cloud_white": {
        "000": "#FFFDF9", "100": "#FFFCF6", "200": "#FFFAF1", "300": "#FFF8EC",
        "400": "#FFF7E8", "500": "#FFF5E3",  # = CLOUD_WHITE
        "600": "#D5CCBD", "700": "#AAA397", "800": "#807B72", "900": "#55524C",
    },
    "stone_gray": {
        "000": "#F6F4F1", "100": "#EFEDE8", "200": "#E7E3DC", "300": "#E0DAD1",
        "400": "#D8D1C5", "500": "#D0C8BA",  # = STONE_GRAY
        "600": "#ADA79B", "700": "#8B857C", "800": "#68645D", "900": "#45433E",
    },
    "ash_gray": {
        "000": "#D5D4D4", "100": "#B9B8B7", "200": "#969493", "300": "#73716F",
        "400": "#504E4B", "500": "#2D2A27",  # = ASH_GRAY
        "600": "#262321", "700": "#1E1C1A", "800": "#171514", "900": "#0F0E0D",
    },
}

# ═══════════════════════════════════════════════════════════════
# SEMANTIC COLORS — for SafeMode dashboard usage
# Maps risk/status levels to brand-compliant colors
# ═══════════════════════════════════════════════════════════════

STATUS_COLORS = {
    # Protected / Pass — Mint Green family
    "protected": {
        "bg": EXTENDED["mint_green"]["000"],     # #F3FAF5
        "fg": EXTENDED["moss_green"]["500"],      # #8FA596
        "fill": EXTENDED["mint_green"]["500"],    # #C5E4CC
    },
    # Protected but not best practice — Moss Green family
    "protected_not_bp": {
        "bg": EXTENDED["moss_green"]["100"],      # #DAE1DC
        "fg": EXTENDED["basil_green"]["500"],     # #5A6359
        "fill": EXTENDED["moss_green"]["300"],    # #B4C3B9
    },
    # At Risk / Warning — Pure Orange family
    "at_risk": {
        "bg": EXTENDED["pure_orange"]["000"],     # #FFE2D3
        "fg": EXTENDED["cinnamon_brown"]["600"],  # #9E5633
        "fill": EXTENDED["pure_orange"]["300"],   # #FFA06C
    },
    # Critical / Fail — Pink/Clay family
    "critical": {
        "bg": EXTENDED["rose_pink"]["100"],       # #FBEEEB
        "fg": EXTENDED["clay_pink"]["500"],       # #95685D
        "fill": EXTENDED["quartz_pink"]["500"],   # #DEA193
    },
    # Excluded — Stone Gray family
    "excluded": {
        "bg": EXTENDED["stone_gray"]["100"],      # #EFEDE8
        "fg": EXTENDED["walnut_brown"]["500"],    # #71584C
        "fill": EXTENDED["stone_gray"]["300"],    # #E0DAD1
    },
}

# ═══════════════════════════════════════════════════════════════
# CHART PALETTE — ordered for pie/bar charts
# ═══════════════════════════════════════════════════════════════

CHART_PALETTE = {
    "protected":        MINT_GREEN,
    "protected_not_bp": MOSS_GREEN,
    "at_risk":          PURE_ORANGE,
    "critical":         CLAY_PINK,
    "excluded":         STONE_GRAY,
}

# ═══════════════════════════════════════════════════════════════
# TYPOGRAPHY COLORS
# ═══════════════════════════════════════════════════════════════

TEXT_PRIMARY   = ASH_GRAY       # #2D2A27 — body text, headings
TEXT_SECONDARY = WALNUT_BROWN   # #71584C — subtitles, captions
TEXT_ON_DARK   = CLOUD_WHITE    # #FFF5E3 — text on dark backgrounds
TEXT_ACCENT    = PURE_ORANGE    # #FF7023 — links, highlights

# ═══════════════════════════════════════════════════════════════
# BACKGROUND COLORS
# ═══════════════════════════════════════════════════════════════

BG_PRIMARY   = CLOUD_WHITE  # #FFF5E3 — page background
BG_CARD      = "#FFFFFF"    # white cards on cream background
BG_DARK      = ASH_GRAY     # #2D2A27 — dark sections, headers
BG_ACCENT    = PURE_ORANGE  # #FF7023 — accent bars, dividers

# ═══════════════════════════════════════════════════════════════
# PALETTE RULES (from brand guidelines)
# ═══════════════════════════════════════════════════════════════
#
# DO:
#   - Use Pure Orange with intent: to draw attention, signal action, inject energy
#   - Use neutrals for balance, calm, clarity, and space
#   - Let orange lead when it needs to, rest when it doesn't
#   - Use extended palette for functional UI only, not brand marketing
#
# DON'T:
#   - Introduce colors outside the palette
#   - Use colors as gradients
#   - Use type with poor contrast
#   - Overdo the number of colors
#   - Alter opacity of colors
#


# ═══════════════════════════════════════════════════════════════
# NOTES
# ═══════════════════════════════════════════════════════════════
#
# All 120 extended palette values (12 families × 10 steps) plus
# all core and secondary palette values are verified from the
# brand portal source (brand.purestorage.com, April 2026).
#
# Font: "Pure Sans" is the brand typeface.
