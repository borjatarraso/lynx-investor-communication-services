# Lynx Communication Services Analysis

> Fundamental analysis specialized for telecom, wireless, cable, streaming, internet, social media, advertising, publishing, broadcasting, and gaming companies.

Part of the **Lince Investor Suite**.

## Overview

Lynx Communication Services is a comprehensive fundamental analysis tool built specifically for the Communication Services sector. It evaluates companies across all lifecycle stages — from early-stage startups to dominant carriers and Big Internet platforms — using comm-services-specific metrics, valuation methods, and risk assessments.

### Key Features

- **Stage-Aware Analysis**: Automatically classifies companies as Startup, Subscriber Growth, Scale-Up, Mature / Cash-Generative, or Dominant Platform — and adapts all metrics and scoring accordingly
- **Comm-Services-Specific Metrics**: ARPU & ARPU growth, subscriber net adds & growth, MAU/DAU & engagement (DAU/MAU), churn rate, content amortization intensity, content ROI, capex/subscriber, EV/Subscriber, EV/(EBITDA-Capex), FCF yield, Net Debt/EBITDA, Cost per Gross Add (CPGA), Rule of 40 (digital subsegments), SBC/Revenue, SBC/FCF
- **Sub-Sector Detection**: Automatic identification of Wireless Telecom, Wireline/Fiber, Cable & Satellite, Streaming, Entertainment, Internet Content & Search, Social Media, Digital Advertising, Ad Agencies, Publishing, Broadcasting, or Electronic Gaming
- **5-Level Relevance System**: Critical, Important, Relevant, Informational, Irrelevant — plus an **Impact column** with colored labels (blinking red / orange / yellow / green / silver)
- **5-Level Severity System**: `***CRITICAL***` (red), `*WARNING*` (orange), `[WATCH]` (yellow), `[OK]` (green), `[STRONG]` (silver)
- **Market Intelligence**: Insider transactions (with 10b5-1 plan awareness), institutional holders, analyst consensus, short interest, price technicals with golden/death cross detection, XLC + sub-sector ETF comparison (IYZ, FCOM, FDN, SOCL, PBS, HERO, ESPO)
- **10-Point Comm-Services Screening Checklist**: Rule-of-40 pass, moat gross margin, SBC contained, dilution, cash runway, Net Debt/EBITDA leverage discipline, capex discipline, insider alignment, growth, jurisdiction
- **Jurisdiction Risk Classification**: Tier 1/2/3 based on spectrum policy, content regulation, data privacy, and antitrust posture
- **Multiple Interface Modes**: Console CLI, Interactive REPL, Textual TUI, Tkinter GUI
- **Export**: TXT, HTML, and PDF report generation
- **Sector & Industry Insights**: Deep context for Wireless, Cable, Streaming, Internet Content, Social Media, Digital Advertising, Publishing, Broadcasting, Gaming

### Target Companies

Designed for analyzing companies like:
- **Mega-Cap Internet Platforms**: Alphabet (GOOGL), Meta (META), Netflix (NFLX), Disney (DIS)
- **Tier-1 Wireless Carriers**: T-Mobile US (TMUS), Verizon (VZ), AT&T (T), Vodafone (VOD), Deutsche Telekom (DTE.DE)
- **Cable & Broadband**: Comcast (CMCSA), Charter (CHTR), Liberty Latin America (LILA)
- **Streaming & Media**: Netflix (NFLX), Disney (DIS), Warner Bros Discovery (WBD), Paramount (PARA), Fox (FOXA)
- **Social & Interactive Media**: Snap (SNAP), Pinterest (PINS), Reddit (RDDT), Match Group (MTCH)
- **Digital Advertising / Ad Agencies**: Trade Desk (TTD), Magnite (MGNI), Omnicom (OMC), Interpublic (IPG), WPP (WPP), Publicis (PUB.PA)
- **Publishing**: New York Times (NYT), News Corp (NWSA)
- **Broadcasting**: Sinclair (SBGI), Nexstar (NXST), iHeartMedia (IHRT)
- **Electronic Gaming**: Electronic Arts (EA), Take-Two (TTWO), Roblox (RBLX), Unity (U), Nintendo (NTDOY)

## Installation

```bash
# Clone the repository
git clone https://github.com/borjatarraso/lynx-investor-communication-services.git
cd lynx-investor-communication-services

# Install in editable mode (creates the `lynx-comm` command)
pip install -e .
```

### Dependencies

| Package        | Purpose                              |
|----------------|--------------------------------------|
| yfinance       | Financial data from Yahoo Finance    |
| requests       | HTTP calls (OpenFIGI, EDGAR, etc.)   |
| beautifulsoup4 | HTML parsing for SEC filings         |
| rich           | Terminal tables and formatting       |
| textual        | Full-screen TUI framework            |
| feedparser     | News RSS feed parsing                |
| pandas         | Data analysis                        |
| numpy          | Numerical computing                  |

All dependencies are installed automatically via `pip install -e .`.

## Usage

### Direct Execution
```bash
# Via the runner script
./lynx-investor-communication-services.py -p TMUS

# Via Python
python3 lynx-investor-communication-services.py -p NFLX

# Via pip-installed command
lynx-comm -p GOOGL
```

### Execution Modes

| Flag | Mode | Description |
|------|------|-------------|
| `-p` | Production | Uses `data/` for persistent cache |
| `-t` | Testing | Uses `data_test/` (isolated, always fresh) |

### Interface Modes

| Flag | Interface | Description |
|------|-----------|-------------|
| (none) | Console | Progressive CLI output |
| `-i` | Interactive | REPL with commands |
| `-tui` | TUI | Textual terminal UI with themes |
| `-x` | GUI | Tkinter graphical interface |

### Examples

```bash
# Analyze a tier-1 wireless carrier
lynx-comm -p TMUS

# Force fresh data download
lynx-comm -p NFLX --refresh

# Search by company name
lynx-comm -p "Disney"

# Interactive mode
lynx-comm -p -i

# Export HTML report
lynx-comm -p GOOGL --export html

# Explain a metric
lynx-comm --explain arpu
lynx-comm --explain net_debt_to_ebitda
lynx-comm --explain content_amort_intensity

# Skip filings and news for faster analysis
lynx-comm -t VZ --no-reports --no-news
```

## Severity & Impact System

Every metric displays a **Severity tag** and an **Impact column**.

### Severity Levels

| Severity        | Marker          | Color           | Meaning                  |
|-----------------|-----------------|-----------------|--------------------------|
| `***CRITICAL***` | uppercase, red bold | Red             | Urgent red flag          |
| `*WARNING*`     | italic          | Orange          | Significant concern      |
| `[WATCH]`       | bracketed       | Yellow          | Needs monitoring         |
| `[OK]`          | bracketed       | Green           | Normal range             |
| `[STRONG]`      | bracketed       | Silver / Grey   | Excellent signal         |

### Impact Column

| Impact          | Color (text)      |
|-----------------|-------------------|
| Critical        | Blinking red      |
| Important       | Orange            |
| Relevant        | Yellow            |
| Informational   | Green             |
| Irrelevant      | Grey / Silver     |

## Analysis Sections

1. **Company Profile** — Tier, lifecycle stage, comm-services sub-sector, jurisdiction classification
2. **Sector & Industry Insights** — Comm-services-specific context and benchmarks
3. **Valuation Metrics** — Traditional + sector-specific (EV/Subscriber, EV/(EBITDA-Capex), FCF Yield, Price/DAU, EV/ARR, EV/Gross-Profit, R40-Adj EV/Rev)
4. **Profitability Metrics** — ROE/ROIC/margins + ARPU & ARPU growth, content amortization intensity, content ROI, operating margin ex-content, ad/subscription revenue mix, Rule of 40 (digital), SBC drag
5. **Solvency & Survival** — Net Debt/EBITDA (sector-critical), interest coverage, cash runway, capex/revenue, capex/subscriber, content obligations, spectrum book value, goodwill/assets
6. **Growth & Engagement** — Revenue growth, subscriber net adds & growth, ARPU growth, MAU/DAU engagement, content/ad/subscription growth, R&D & content intensity, productivity
7. **Share Structure** — Outstanding/diluted shares, insider/institutional ownership, SBC Overhang Risk, Dual-Class flag (common in this sector)
8. **Sector Quality** — Moat (network/spectrum/content/engagement), Rule-of-40 verdict, capex cycle assessment, leverage assessment, unit economics (ARPU/Churn/CPGA), platform position, founder-led signal
9. **Intrinsic Value** — DCF, EV/(EBITDA-Capex) peer comp, EV/Subscriber, FCF yield, Reverse DCF (method selection by sub-sector and stage)
10. **Market Intelligence** — Analysts, short interest, technicals, insider trades, comm-services benchmark (XLC + sub-sector ETF such as IYZ for telecom, FDN for internet, SOCL for social, PBS for media, HERO/ESPO for gaming)
11. **Financial Statements** — 5-year annual summary with R&D, SBC, content amortization, deferred revenue
12. **SEC Filings** — Downloadable regulatory filings
13. **News** — Yahoo Finance + Google News RSS
14. **Assessment Conclusion** — Weighted score, verdict, strengths/risks, 10-point comm-services screening checklist
15. **Communication Services Disclaimers** — Stage- and sub-sector-specific risk disclosures

## Relevance System

Each metric is classified by importance for the company's lifecycle stage:

| Level | Prefix | Impact Column    | Meaning |
|-------|--------|------------------|---------|
| **Critical**    | `*`      | Blinking Red    | Must-check for this stage |
| **Important**   | `!`      | Orange          | Primary metric |
| **Relevant**    | normal   | Yellow          | Important context |
| **Informational** (Contextual) | dimmed | Green | Background only |
| **Irrelevant**  | hidden   | Silver          | Not meaningful for this stage |

Example: For a Subscriber-Growth-stage streaming company, ARPU/Churn/Net Adds is **Critical** while traditional P/E is **Irrelevant**. For a Mature carrier, Net Debt/EBITDA, FCF yield, and dividend coverage dominate.

## Scoring Methodology

The overall score (0-100) is a weighted average of 5 categories, with weights adapted by both company tier AND lifecycle stage:

| Stage | Valuation | Profitability | Solvency | Growth | Sector Quality |
|-------|-----------|---------------|----------|--------|--------------|
| Startup | 5-10% | 5% | 35-40% | 15-20% | 30-35% |
| Subscriber Growth | 10-15% | 10-15% | 15-25% | 30% | 25% |
| Scale-Up | 15-20% | 15-20% | 15-20% | 20-25% | 25% |
| Mature / Cash-Generative | 20-25% | 20-25% | 10-15% | 15-20% | 25% |
| Dominant Platform | 25% | 25% | 10% | 15% | 25% |

Verdicts: Strong Buy (>=75), Buy (>=60), Hold (>=45), Caution (>=30), Avoid (<30).

## Project Structure

```
lynx-investor-communication-services/
├── lynx-investor-communication-services.py  # Runner script
├── pyproject.toml                            # Build configuration
├── requirements.txt                          # Dependencies
├── img/                                      # Logo images
├── data/                                     # Production cache
├── data_test/                                # Testing cache
├── docs/                                     # Documentation
│   └── API.md                                # API reference
├── robot/                                    # Robot Framework tests
│   ├── cli_tests.robot
│   ├── api_tests.robot
│   └── export_tests.robot
├── tests/                                    # Unit tests
└── lynx_comm/                                # Main package
```

## Testing

```bash
# Unit tests
pytest tests/ -v

# Robot Framework acceptance tests
robot robot/
```

## License

BSD 3-Clause License. See LICENSE in source.

## Author

**Borja Tarraso** — borja.tarraso@member.fsf.org
