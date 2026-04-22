# Development Guide

## Architecture

The application shares core architecture with other Lynx specialists (Information Technology, Basic Materials, Energy, etc.) but applies Communication-Services-specific domain logic end-to-end.

### Data Flow

```
User Input (ticker/ISIN/name)
    ↓
CLI/Interactive/TUI/GUI → cli.py
    ↓
analyzer.py: run_progressive_analysis()
    ↓
ticker.py: resolve_identifier() → (ticker, isin)
    ↓
storage.py: check cache → return if cached
    ↓
fetcher.py: yfinance data (profile + financials, incl. R&D, SBC, deferred revenue, goodwill, content amortization)
    ↓
models.py: classify_stage / classify_category / classify_jurisdiction
    ↓
analyzer.py: _validate_sector() — block non-Communication-Services tickers
    ↓
calculator.py: calc_valuation / profitability / solvency / growth / efficiency
    ↓
calculator.py: calc_share_structure + calc_comm_quality
    ↓
calculator.py: calc_market_intelligence (insider, analyst, short, technicals, XLC + sub-sector ETF)
    ↓
calculator.py: calc_intrinsic_value (DCF, EV/(EBITDA-Capex), EV/Subscriber, FCF Yield, Reverse DCF)
    ↓
[parallel] reports.py + news.py
    ↓
conclusion.py: generate_conclusion() → verdict + 10-point comm-services screening
    ↓
storage.py: save_analysis_report()
    ↓
display.py / tui/app.py / gui/app.py / export/* → render with severity + impact columns
```

### Key Design Decisions

1. **Sub-sector dispersion**: Communication Services is bimodal — high-leverage capex-heavy carriers vs asset-light ad-driven internet platforms. Most decisions in the codebase pivot on `CommCategory` (the detected sub-sector) so that thresholds, ETFs, disclaimers, valuation methods, and quality assessment all adapt.

2. **Stage > Tier**: Lifecycle stage (Startup → Subscriber Growth → Scale → Mature → Platform) is the primary analysis axis. The relevance system prioritizes stage overrides over tier-based fallbacks.

3. **ARPU/Churn/Net Adds as the operational triangle**: For subscription-driven sub-sectors (carriers, streaming, cable broadband), ARPU × subscriber retention × net adds is the unit-economics fingerprint. Most disclosed company KPIs flow into these fields.

4. **Net Debt/EBITDA as the headline solvency metric**: Carriers and cable operators run leveraged by design. Net Debt/EBITDA (target <3.5x for investment-grade carriers, <4.0x for cable) is the most-watched leverage metric, scored explicitly in `_score_solvency`.

5. **Capex-adjusted EBITDA for capex-heavy carriers**: `EV/(EBITDA - Capex)` exposes the true cash economics of telecom and cable during 5G/fiber build cycles, where reported EV/EBITDA can look deceptively cheap.

6. **Content amortization intensity for streaming/media**: A single non-cash line item can dwarf reported leverage. We compute content_amort_intensity, content_roi, and operating_margin_ex_content to expose the streaming/media P&L's true shape.

7. **Rule of 40 selectively applied**: The Rule of 40 (revenue growth + FCF margin) is computed for all sub-sectors but is most meaningful for digital subsegments (streaming, internet platforms, social, growth-stage gaming). Carriers and agencies are scored against different anchors.

8. **SBC as structural dilution for tech-leaning subsegments**: Internet, social, and gaming companies dilute heavily via SBC (often 10-25% of revenue). We compute SBC/Revenue and SBC/FCF to expose paper-vs-cash gaps. Carriers and agencies have minimal SBC.

9. **Severity + Impact dual-axis display**: Every metric row shows BOTH a severity tag (how bad is this reading?) and an impact column (how much does this metric matter for this stage?). The two are independent.

10. **Progressive Rendering**: The analyzer emits progress callbacks so UIs can render sections as data arrives.

11. **Reverse DCF sanity check**: We compute the growth rate implied by the current price to spot priced-in expectations.

### Adding New Metrics

1. Add field to the appropriate dataclass in `models.py`
2. Calculate in `calculator.py` (in the relevant `calc_*` function)
3. Add relevance entry in `relevance.py` (`_STAGE_OVERRIDES` and tier tables)
4. Add explanation in `explanations.py`
5. Add display row in `display.py`, `tui/app.py`, `gui/app.py`
6. Add export row in `export/html_export.py` and `export/txt_export.py`

### Adding New Comm-Services Sub-Categories

1. Add to `CommCategory` enum in `models.py`
2. Add keywords to `_CATEGORY_KEYWORDS`
3. Add sub-sector ETFs to `_CATEGORY_ETFS` in `calculator.py`
4. Add industry insight in `sector_insights.py`
5. Update sector validation regex in `analyzer.py` if it represents a new keyword family

### Adding New Stages

1. Add to `CompanyStage` enum
2. Add keywords to `_STAGE_KEYWORDS` in `models.py`
3. Add weights to `_WEIGHTS` in `conclusion.py`
4. Add relevance overrides in `relevance.py`
5. Update method selection in `calc_intrinsic_value`

## Running Tests

```bash
# Python unit tests
pytest tests/ -v --tb=short

# Robot Framework (requires robotframework)
pip install robotframework
robot --outputdir results robot/

# Syntax check all files
python -c "import py_compile, glob; [py_compile.compile(f, doraise=True) for f in glob.glob('lynx_comm/**/*.py', recursive=True)]"
```

## Code Style

- Python 3.10+ with type hints
- Dataclasses for all data models
- Rich for console rendering
- Textual for TUI
- Tkinter for GUI (dark theme)

## Severity & Impact System

The dual-axis display is implemented in `lynx_comm/display.py`:

- `_SEVERITY_FMT` → maps `Severity.*` to `[color]***CRITICAL***[/]`, `[color]*WARNING*[/]`, `[color][WATCH][/]` etc.
- `_IMPACT_DISPLAY` → maps `Relevance.*` to `[blink bold red]Critical[/]`, `[#ff8800]Important[/]`, etc.

Both are shown as separate columns in every metric table, alongside the Value and Assessment columns.
