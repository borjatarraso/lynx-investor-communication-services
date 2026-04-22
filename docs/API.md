# Lynx Communication Services Analysis -- API Reference

Public Python API for the `lynx_comm` package (v2.0).

## Package Structure

```
lynx_comm/
├── __init__.py          # Version, about text
├── __main__.py          # Entry point
├── cli.py               # CLI argument parser
├── display.py           # Rich console display
├── interactive.py       # Interactive REPL mode
├── easter.py            # Hidden features
├── models.py            # Data models
├── core/
│   ├── analyzer.py      # Analysis orchestrator + sector validation gate
│   ├── conclusion.py    # Verdict synthesis
│   ├── fetcher.py       # yfinance data fetching
│   ├── news.py          # News aggregation
│   ├── reports.py       # SEC/SEDAR filing fetching
│   ├── storage.py       # Cache management
│   └── ticker.py        # Ticker resolution
├── metrics/
│   ├── calculator.py    # Metric calculations
│   ├── relevance.py     # Metric relevance by stage/tier
│   ├── explanations.py  # Metric educational content
│   └── sector_insights.py # Communication Services industry insights
├── export/
│   ├── __init__.py      # Export dispatcher
│   ├── txt_export.py    # Plain text export
│   ├── html_export.py   # HTML export
│   └── pdf_export.py    # PDF export
├── gui/
│   └── app.py           # Tkinter GUI
└── tui/
    ├── app.py           # Textual TUI
    └── themes.py        # TUI color themes
```

---

## Core API

### Analysis (`lynx_comm.core.analyzer`)

#### `run_full_analysis`

```python
def run_full_analysis(
    identifier: str,
    download_reports: bool = True,
    download_news: bool = True,
    max_filings: int = 10,
    verbose: bool = False,
    refresh: bool = False,
) -> AnalysisReport
```

Run a complete fundamental analysis for a Communication Services company.
Convenience wrapper around `run_progressive_analysis` with `on_progress=None`.

**Parameters:**

| Parameter | Type | Default | Description |
|---|---|---|---|
| `identifier` | `str` | required | Ticker symbol (`TMUS`), ISIN (`US8725901040`), or company name (`Netflix`). |
| `download_reports` | `bool` | `True` | Fetch SEC filings. |
| `download_news` | `bool` | `True` | Fetch recent news articles. |
| `max_filings` | `int` | `10` | Maximum number of filings to download locally. |
| `verbose` | `bool` | `False` | Enable verbose console output. |
| `refresh` | `bool` | `False` | Force re-fetch from network even if cached data exists. |

**Returns:** `AnalysisReport` -- fully populated report dataclass.
**Raises:** `SectorMismatchError` if the company is not in Communication Services.

**Example:**

```python
from lynx_comm.core.analyzer import run_full_analysis

report = run_full_analysis("TMUS")
print(report.profile.name)             # "T-Mobile US, Inc."
print(report.profile.tier.value)       # "Mega Cap"
print(report.profile.comm_category.value)  # "Telecom Services — Wireless"
print(report.solvency.net_debt_to_ebitda)
```

---

#### `run_progressive_analysis`

```python
def run_progressive_analysis(
    identifier: str,
    download_reports: bool = True,
    download_news: bool = True,
    max_filings: int = 10,
    verbose: bool = False,
    refresh: bool = False,
    on_progress: Optional[Callable[[str, AnalysisReport], None]] = None,
) -> AnalysisReport
```

Same as `run_full_analysis`, but accepts a progress callback invoked
after each analysis stage completes. Used by the TUI and GUI to update the
display incrementally.

**Callback stages** (passed as the first `str` argument):

`"profile"` | `"financials"` | `"valuation"` | `"profitability"` |
`"solvency"` | `"growth"` | `"share_structure"` | `"comm_quality"` |
`"intrinsic_value"` | `"market_intelligence"` | `"filings"` | `"news"` |
`"conclusion"` | `"complete"`

#### `SectorMismatchError`

Raised by `_validate_sector` (called inside `run_progressive_analysis`) when
the resolved company is not in Communication Services. The CLI catches this
and prints a prominent red-blinking warning that points at sibling Lynx
specialists (Information Technology, Energy, Basic Materials, etc.).

---

### Conclusion (`lynx_comm.core.conclusion`)

#### `generate_conclusion`

```python
def generate_conclusion(report: AnalysisReport) -> AnalysisConclusion
```

Synthesize a scored verdict from a completed `AnalysisReport`.

Scoring weights are determined by the company's `(stage, tier)` combination.
Mature carriers weight solvency (leverage) and FCF heavily; growth-stage
streaming weights growth and unit economics; internet platforms balance
growth, profitability, and quality.

**Returns:** `AnalysisConclusion` with:

- `overall_score` -- 0-100 composite score.
- `verdict` -- one of `"Strong Buy"`, `"Buy"`, `"Hold"`, `"Caution"`, `"Avoid"`.
- `summary` -- one-paragraph narrative.
- `category_scores` -- dict with scores for `valuation`, `profitability`, `solvency`, `growth`, `comm_quality`.
- `category_summaries` -- dict with human-readable summary per category.
- `strengths` / `risks` -- lists of up to 6 key points each.
- `tier_note` / `stage_note` -- explanations of why certain metrics matter for this company.
- `screening_checklist` -- dict of boolean pass/fail/None checks (e.g. `cash_runway_18m`, `low_dilution`, `leverage_discipline`, `capex_discipline`, `insider_alignment`).

---

## Data Models (`lynx_comm.models`)

All models are Python `dataclasses`. Every numeric field defaults to `None`
(meaning "not available") unless otherwise noted.

### Enums

| Enum | Values |
|---|---|
| `CompanyTier` | `MEGA`, `LARGE`, `MID`, `SMALL`, `MICRO`, `NANO` |
| `CompanyStage` | `STARTUP`, `GROWTH` (= "Subscriber Growth"), `SCALE`, `MATURE`, `PLATFORM` |
| `CommCategory` | `TELECOM_WIRELESS`, `TELECOM_WIRELINE`, `CABLE_SATELLITE`, `STREAMING`, `ENTERTAINMENT`, `INTERNET_CONTENT`, `SOCIAL_MEDIA`, `DIGITAL_ADVERTISING`, `AD_AGENCY`, `PUBLISHING`, `BROADCASTING`, `GAMING`, `OTHER` |
| `JurisdictionTier` | `TIER_1` (Strong IP & Stable Regulation), `TIER_2` (Moderate Regulatory Risk), `TIER_3` (High Regulatory / Geopolitical Risk), `UNKNOWN` |
| `Relevance` | `CRITICAL`, `IMPORTANT`, `RELEVANT`, `CONTEXTUAL`, `IRRELEVANT` |
| `Severity` | `CRITICAL`, `WARNING`, `WATCH`, `OK`, `STRONG`, `NA` |

### Core Dataclasses

#### `CompanyProfile`

| Field | Type | Description |
|---|---|---|
| `ticker` | `str` | Resolved ticker symbol. |
| `name` | `str` | Company name. |
| `isin` | `Optional[str]` | ISIN code if resolved. |
| `sector` | `Optional[str]` | Sector (e.g. `"Communication Services"`). |
| `industry` | `Optional[str]` | Industry (e.g. `"Telecom Services"`). |
| `country` | `Optional[str]` | Country of domicile. |
| `exchange` | `Optional[str]` | Primary exchange. |
| `currency` | `Optional[str]` | Reporting currency. |
| `market_cap` | `Optional[float]` | Market capitalization. |
| `description` | `Optional[str]` | Company description from filings. |
| `website` | `Optional[str]` | Corporate website. |
| `employees` | `Optional[int]` | Number of employees. |
| `tier` | `CompanyTier` | Market-cap tier (default `NANO`). |
| `stage` | `CompanyStage` | Communication Services lifecycle stage (default `STARTUP`). |
| `comm_category` | `CommCategory` | Primary comm-services sub-category (default `OTHER`). |
| `jurisdiction_tier` | `JurisdictionTier` | Jurisdiction risk tier (default `UNKNOWN`). |
| `jurisdiction_country` | `Optional[str]` | Country used for jurisdiction classification. |

#### `ValuationMetrics`

Traditional + comm-services-specific valuation ratios.

Standard fields: `pe_trailing`, `pe_forward`, `pb_ratio`, `ps_ratio`, `p_fcf`,
`ev_ebitda`, `ev_revenue`, `ev_gross_profit`, `peg_ratio`, `dividend_yield`,
`earnings_yield`, `enterprise_value`, `market_cap`, `price_to_tangible_book`,
`price_to_ncav`, `cash_to_market_cap`.

**Communication Services-specific:**
- `ev_to_subscriber` — EV / total subscribers (telecom, streaming, cable)
- `ev_to_arr` — EV / annualized recurring subscription revenue
- `ev_per_employee` — productivity-adjusted scale check
- `ev_to_ebitda_capex_adj` — EV / (EBITDA - capex), capex-adjusted
- `fcf_yield` — FCF / market cap (mature carriers, ad-platforms)
- `price_per_dau` — market cap / DAU (social/internet)
- `rule_of_40_adj_multiple` — quality-normalized EV/Sales

#### `ProfitabilityMetrics`

Standard fields: `roe`, `roa`, `roic`, `gross_margin`, `operating_margin`,
`net_margin`, `fcf_margin`, `ebitda_margin`.

**Communication Services-specific:**
- `arpu` — Average Revenue Per User/subscriber
- `arpu_growth_yoy` — ARPU YoY growth
- `content_amort_intensity` — content amortization / revenue (streaming/media)
- `content_roi` — revenue per dollar of content amortization
- `operating_margin_ex_content` — operating margin stripping content amort
- `advertising_revenue_pct`, `subscription_revenue_pct` — revenue mix decomposition
- `rule_of_40`, `rule_of_40_ebitda` — quality gate for digital subsegments
- `magic_number` — sales efficiency proxy
- `sbc_to_revenue`, `sbc_to_fcf`, `gaap_vs_adj_gap` — dilution/SBC drag

#### `SolvencyMetrics`

Standard fields: `debt_to_equity`, `debt_to_ebitda`, `current_ratio`,
`quick_ratio`, `interest_coverage`, `altman_z_score`, `net_debt`,
`total_debt`, `total_cash`, `cash_burn_rate`, `cash_runway_years`,
`working_capital`, `cash_per_share`, `tangible_book_value`, `ncav`,
`ncav_per_share`, `quarterly_burn_rate`, `burn_as_pct_of_market_cap`.

**Communication Services-specific:**
- `net_debt_to_ebitda` — leverage discipline (carriers/cable critical)
- `capex_to_revenue` — network buildout intensity
- `capex_to_subscriber` — network capex per subscriber
- `spectrum_license_book_value` — wireless spectrum on balance sheet
- `content_obligations` — off-balance content commitments (streaming)
- `rpo_coverage`, `deferred_revenue_ratio` — forward subscription visibility
- `goodwill_to_assets` — M&A impairment risk
- `cash_coverage_months` — cash runway in months

#### `GrowthMetrics`

Standard fields: `revenue_growth_yoy`, `revenue_cagr_3y`, `revenue_cagr_5y`,
`earnings_growth_yoy`, `earnings_cagr_3y`, `earnings_cagr_5y`,
`fcf_growth_yoy`, `book_value_growth_yoy`, `dividend_growth_5y`,
`shares_growth_yoy`, `shares_growth_3y_cagr`, `fully_diluted_shares`,
`dilution_ratio`.

**Communication Services-specific:**
- `subscribers`, `subscriber_net_adds`, `subscriber_growth_yoy`
- `mau`, `dau`, `dau_mau_ratio` (engagement)
- `arr_growth_yoy` — subscription revenue growth (streaming)
- `net_revenue_retention`, `gross_revenue_retention` — where disclosed
- `content_intensity`, `content_growth_yoy` — content investment
- `rd_intensity`, `rd_growth_yoy` — R&D commitment (internet/gaming)
- `sales_marketing_intensity`, `cost_per_gross_add` — subscriber acquisition cost
- `advertising_revenue_growth_yoy` — ad cycle exposure
- `employee_growth_yoy`, `revenue_per_employee`, `revenue_per_subscriber`
- `operating_leverage`

#### `EfficiencyMetrics`

Standard fields: `asset_turnover`, `inventory_turnover`,
`receivables_turnover`, `days_sales_outstanding`, `days_inventory`,
`cash_conversion_cycle`.

**Communication Services-specific:**
- `cac_payback_months` — subscriber acquisition payback
- `churn_rate_annual` — annualized subscriber churn
- `arpu_to_cpga_ratio` — LTV/CAC proxy
- `rule_of_x_score` — Altimeter Rule of X
- `fcf_conversion` — FCF / Net Income

#### `CommQualityIndicators`

Composite quality score (0-100) plus qualitative assessments. Notable fields:

`quality_score`, `management_quality`, `insider_ownership_pct`,
`founder_led`, `moat_assessment`, `moat_type`, `competitive_position`,
`network_quality_assessment` (spectrum/fiber/5G), `content_library_assessment`
(streaming/media), `user_engagement_assessment` (DAU/MAU & ad-pricing),
`unit_economics` (ARPU/Churn/CPGA), `platform_position`, `financial_position`,
`dilution_risk`, `leverage_assessment` (Net Debt/EBITDA), `capex_cycle_assessment`
(build vs harvest), `rule_of_40_assessment`, `sbc_risk_assessment`,
`catalyst_density`, `near_term_catalysts`, `revenue_predictability`,
`roic_history`, `gross_margin_history`, `arpu_history`, `churn_history`.

(`rd_efficiency_assessment` is also populated as an alias for the network/content
investment narrative for backward-compatible display rendering.)

#### `IntrinsicValue`

Multiple intrinsic-value methods adapted by sub-sector and stage.

Fields: `dcf_value`, `graham_number`, `lynch_fair_value`, `ncav_value`,
`asset_based_value`, `ev_sales_implied_price`, `reverse_dcf_growth`,
`current_price`, `margin_of_safety_dcf`, `margin_of_safety_graham`,
`margin_of_safety_ncav`, `margin_of_safety_asset`, `margin_of_safety_ev_sales`,
`primary_method`, `secondary_method`.

The `primary_method` adapts per stage:
- **PLATFORM**: DCF + EV/EBITDA peer multiple
- **MATURE**: DCF + P/FCF + EV/(EBITDA-Capex) peer multiple
- **SCALE**: EV/EBITDA peer multiple + DCF (carrier/streaming early)
- **GROWTH**: EV/Subscriber + EV/Revenue (Rule-of-40 adj) + Reverse DCF
- **STARTUP**: Cash + Option Value + Peer EV/Revenue or EV/MAU

#### `ShareStructure`, `InsiderTransaction`, `MarketIntelligence`

Same field layout as the IT sibling — comm-services-specific touchpoints:
- `MarketIntelligence.benchmark_*` defaults to **XLC** (Communication
  Services Select Sector SPDR) instead of QQQ.
- `MarketIntelligence.sector_etf_*` / `peer_etf_*` are populated based on
  the detected `CommCategory` (e.g. IYZ for wireless, FDN for internet, SOCL
  for social, PBS for media, HERO/ESPO for gaming).
- `MarketIntelligence.disclaimers` is sub-sector-aware (carrier leverage,
  streaming content commitments, internet/social regulatory risk, gaming
  hit-driven risk).

#### `FinancialStatement`

Per-period statement. Standard fields plus comm-services-specific:
`research_development`, `selling_general_admin`, `stock_based_compensation`,
`deferred_revenue`, `goodwill`, `intangibles`, `content_amortization`,
`content_assets`, `advertising_revenue`, `subscription_revenue`,
`licensing_revenue`.

#### `AnalysisConclusion`

Scored verdict produced by `generate_conclusion`.

Fields: `overall_score`, `verdict`, `summary`, `category_scores`,
`category_summaries`, `strengths`, `risks`, `tier_note`, `stage_note`,
`screening_checklist`.

The 10-point `screening_checklist` keys: `rule_of_40_pass`,
`moat_gross_margin`, `sbc_contained`, `low_dilution`, `cash_runway_18m`,
`leverage_discipline` (Net Debt/EBITDA <4.0x), `capex_discipline`
(capex/revenue <30%), `insider_alignment`, `positive_revenue_growth`,
`tier_1_2_jurisdiction`.

#### `Filing`, `NewsArticle`, `AnalysisReport`

Standard container types for filings, news articles, and the top-level
report bundle. `AnalysisReport.comm_quality` (instead of the IT sibling's
`tech_quality`) holds the `CommQualityIndicators` block.

---

## Classification Helpers (`lynx_comm.models`)

#### `classify_tier(market_cap)`

| Threshold | Tier |
|---|---|
| >= $200B | Mega Cap |
| >= $10B | Large Cap |
| >= $2B | Mid Cap |
| >= $300M | Small Cap |
| >= $50M | Micro Cap |
| < $50M or None | Nano Cap |

#### `classify_stage(description, revenue, info=None)`

Returns `CompanyStage` based on description keywords (dominant platform,
established carrier, scaling, subscriber/user growth, startup) with
revenue/profit-margin/growth fallbacks. Returns `STARTUP` for None inputs.

#### `classify_category(description, industry=None)`

Identify primary `CommCategory` from description and industry text using
keyword frequency scoring. Word-boundary matching for short keywords to
avoid false positives.

#### `classify_jurisdiction(country, description=None)`

Returns `JurisdictionTier`:
- **Tier 1**: US, Canada, UK, Ireland, Germany, France, Netherlands, Sweden,
  Denmark, Finland, Norway, Switzerland, Luxembourg, Belgium, Austria,
  Australia, New Zealand, Japan, South Korea, Singapore, Israel, Taiwan
- **Tier 2**: Spain, Portugal, Italy, Poland, Hong Kong, India, Brazil,
  Mexico, South Africa, Chile, Uruguay, Turkey, etc.
- **Tier 3**: Everything else (when country is provided).

---

## Metrics Calculator (`lynx_comm.metrics.calculator`)

| Function | Returns |
|---|---|
| `calc_valuation(info, statements, tier, stage)` | `ValuationMetrics` |
| `calc_profitability(info, statements, tier, stage)` | `ProfitabilityMetrics` |
| `calc_solvency(info, statements, tier, stage)` | `SolvencyMetrics` |
| `calc_growth(statements, tier, stage, info=None)` | `GrowthMetrics` |
| `calc_efficiency(info, statements, tier)` | `EfficiencyMetrics` |
| `calc_share_structure(info, statements, growth, tier, stage)` | `ShareStructure` |
| `calc_comm_quality(profitability, growth, solvency, share_structure, statements, info, tier, stage)` | `CommQualityIndicators` |
| `calc_intrinsic_value(info, statements, growth, solvency, tier, stage, discount_rate=0.10, terminal_growth=0.03)` | `IntrinsicValue` |
| `calc_market_intelligence(info, ticker_obj, solvency, share_structure, growth, tier, stage)` | `MarketIntelligence` |

---

## Relevance System (`lynx_comm.metrics.relevance`)

#### `get_relevance(metric_key, tier, category="valuation", stage=CompanyStage.GROWTH)`

Look up the relevance level of a metric given the company's tier and stage.

**Stage overrides take precedence** over tier-based lookups, because
lifecycle stage is the primary analytical axis.

`category` ∈ `{"valuation", "profitability", "solvency", "growth",
"comm_quality", "share_structure", "efficiency"}`.

**Stage-driven examples:**

- `arpu`, `subscriber_net_adds` are `CRITICAL` for Subscriber Growth, Scale, Mature, Platform; `IMPORTANT` for Startup.
- `net_debt_to_ebitda` is `CRITICAL` from Subscriber Growth onward (carrier/cable critical).
- `pe_trailing` is `IRRELEVANT` for Startup, Hyper-Growth; `CRITICAL` for Mature/Platform.
- `dau_mau_ratio` is `CRITICAL` for Subscriber Growth, Scale, Mature, Platform.
- `content_amort_intensity` is `CRITICAL` for Subscriber Growth, Scale, Mature.

---

## Storage (`lynx_comm.core.storage`)

Two isolated data directories: `data/` (production) and `data_test/` (testing).
Standard helpers: `set_mode`, `get_mode`, `is_testing`, `has_cache`,
`load_cached_report`, `save_analysis_report`, `list_cached_tickers`,
`drop_cache_ticker`, `drop_cache_all`.

---

## Ticker Resolution (`lynx_comm.core.ticker`)

#### `resolve_identifier(identifier)` → `(ticker, isin | None)`

Resolves user input to a ticker. Accepts ticker symbols (`TMUS`, `VOD.L`),
ISIN codes (`US8725901040`, 12-character format), or company names
(`"T-Mobile US"`, `"Netflix"`).

Strategy: ISIN search → name search → direct ticker probe → exchange-suffix
scan → broadened search. Raises `ValueError` if no match is found.

#### `search_companies(query, max_results=10)` → `list[SearchResult]`

Search via yfinance.

---

## Export (`lynx_comm.export`)

#### `export_report(report, fmt, output_path=None)` → `Path`

Export to TXT, HTML, or PDF. Uses comm-services-adapted tables and section
ordering. PDF requires `weasyprint` (install via the `pdf` extra).

```python
from lynx_comm.export import ExportFormat, export_report
```

---

## Sector Insights (`lynx_comm.metrics.sector_insights`)

#### `get_sector_insight(sector)` → `SectorInsight | None`

Returns sector-level analysis guidance (overview, critical metrics, key
risks, what-to-watch, typical valuation ranges). Available: `"Communication Services"`.

#### `get_industry_insight(industry)` → `IndustryInsight | None`

Available industries: `"Telecom Services"`, `"Telecom Services - Cable"`,
`"Entertainment"`, `"Internet Content & Information"`,
`"Internet Content & Information - Social"`, `"Advertising Agencies"`,
`"Publishing"`, `"Broadcasting"`, `"Electronic Gaming & Multimedia"`,
`"Electronic Gaming & Multimedia - UGC"`.

---

## Usage Examples

### 1. Basic Analysis

```python
from lynx_comm.core.analyzer import run_full_analysis
from lynx_comm.core.conclusion import generate_conclusion

report = run_full_analysis("TMUS")

print(f"{report.profile.name} ({report.profile.ticker})")
print(f"Tier: {report.profile.tier.value}")
print(f"Stage: {report.profile.stage.value}")
print(f"Sub-Sector: {report.profile.comm_category.value}")
print(f"Jurisdiction: {report.profile.jurisdiction_tier.value}")

conclusion = generate_conclusion(report)
print(f"Score: {conclusion.overall_score}/100 -- {conclusion.verdict}")
```

### 2. Progressive Analysis with Callback

```python
from lynx_comm.core.analyzer import run_progressive_analysis

def progress_handler(stage: str, report):
    if stage == "profile":
        print(f"Analyzing: {report.profile.name}")
    elif stage == "solvency":
        nde = report.solvency.net_debt_to_ebitda
        if nde is not None:
            print(f"Net Debt / EBITDA: {nde:.1f}x")
    elif stage == "complete":
        print("Analysis complete.")

report = run_progressive_analysis("VZ", on_progress=progress_handler)
```

### 3. Accessing Specific Metrics

```python
report = run_full_analysis("NFLX")

# Profitability — content economics
if report.profitability:
    p = report.profitability
    print(f"Operating margin: {p.operating_margin:.1%}")
    print(f"Operating margin ex-content: {p.operating_margin_ex_content:.1%}")
    print(f"Content amortization intensity: {p.content_amort_intensity:.1%}")
    print(f"Content ROI: {p.content_roi:.2f}x")

# Solvency — leverage discipline
if report.solvency:
    s = report.solvency
    print(f"Net Debt / EBITDA: {s.net_debt_to_ebitda:.2f}x")
    print(f"Capex / Revenue: {s.capex_to_revenue:.1%}")

# Valuation — comm-services lenses
if report.valuation:
    v = report.valuation
    print(f"FCF Yield: {v.fcf_yield:.2%}")
    print(f"EV / (EBITDA - Capex): {v.ev_to_ebitda_capex_adj:.1f}x")
    print(f"EV / Subscriber: ${v.ev_to_subscriber:,.0f}")

# Intrinsic value
if report.intrinsic_value:
    iv = report.intrinsic_value
    print(f"Primary method: {iv.primary_method}")
    print(f"Current price: ${iv.current_price:.2f}")
```

### 4. Checking Metric Relevance

```python
from lynx_comm.metrics.relevance import get_relevance
from lynx_comm.models import CompanyTier, CompanyStage, Relevance

# For a Mature mega-cap carrier, leverage and FCF yield are critical
tier = CompanyTier.MEGA
stage = CompanyStage.MATURE

assert get_relevance("net_debt_to_ebitda", tier, "solvency", stage) == Relevance.CRITICAL
assert get_relevance("fcf_yield", tier, "valuation", stage) == Relevance.CRITICAL

# For a Subscriber-Growth-stage streaming small-cap, ARPU and churn dominate
tier = CompanyTier.SMALL
stage = CompanyStage.GROWTH
assert get_relevance("arpu", tier, "profitability", stage) == Relevance.CRITICAL
assert get_relevance("churn_rate_annual", tier, "efficiency", stage) == Relevance.CRITICAL
assert get_relevance("pe_trailing", tier, "valuation", stage) == Relevance.IRRELEVANT
```

### 5. Exporting Reports

```python
from pathlib import Path
from lynx_comm.core.analyzer import run_full_analysis
from lynx_comm.export import ExportFormat, export_report

report = run_full_analysis("GOOGL")

# Export as HTML (default path: data/GOOGL/report_<timestamp>.html)
html_path = export_report(report, ExportFormat.HTML)

# Export as plain text to a custom path
txt_path = export_report(report, ExportFormat.TXT, Path("./googl_report.txt"))

# Export as PDF (requires weasyprint)
pdf_path = export_report(report, ExportFormat.PDF)
```
