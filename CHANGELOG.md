# Changelog

## 6.0.0 — 2026-04-26

**Major release synchronising the entire Lince Investor Suite.**

### What's new across the Suite

- **lynx-fund** — brand-new mutual / index fund analysis tool, rejecting
  ETFs and stocks at the resolver level. Surfaces share classes, loads,
  12b-1 fees, manager tenure, persistence, capital-gains tax drag, and
  20-rule passive-investor checklist with tailored tips.
- **lynx-compare-fund** — head-to-head comparison for two mutual / index
  funds. Adds a Boglehead-style Passive-Investor Verdict, plus warnings
  for active-vs-passive, UCITS, soft- / hard-close, and distribution-
  policy mismatches.
- **lynx-theme** — visual theme editor for the entire Suite (GUI + TUI
  only). Edit colours, fonts, alignment, bold / italic / underline /
  blink / marquee for 15 styled areas with live preview. Three built-in
  read-only reference themes (`lynx-mocha`, `lynx-latte`,
  `lynx-high-contrast`). Sets the default theme persisted to
  `$XDG_CONFIG_HOME/lynx-theme/default.json`.
- **i18n** — every Suite CLI now accepts `--language=us|es|it|de|fr|fa`
  and persists the user's choice to `$XDG_CONFIG_HOME/lynx/language.json`.
  GUI apps mount a small bottom-right language toggle (left-click
  cycles, right-click opens a chooser); TUI apps bind `g` to cycle.
  Honours `LYNX_LANG` for ad-hoc shells.
- **Author signature footer** — every txt / html / pdf export now ends
  with the Suite-wide author block: *Borja Tarraso
  &lt;borja.tarraso@member.fsf.org&gt;*. Provided by the new
  `lynx_investor_core.author_footer` module.

### Dashboard

- Two new APP launchables (Lynx Fund, Lynx Compare Fund, Lynx Theme),
  raising the catalogue to **8 apps + 11 sector agents = 19
  launchables**.
- Per-app launch dialect (`run_mode_dialect`, `ui_mode_flags`,
  `accepts_identifier`) so the launcher emits argv each app
  understands; lynx-theme + lynx-portfolio launch correctly from every
  mode.
- `--recommend` now rejects empty queries instead of silently passing.

### Bug fixes

- `__main__.py` of every fund / compare-fund / etf / compare-etf entry
  point now propagates `run_cli`'s return code so non-zero exits are
  visible to shell scripts and CI pipelines.
- Stale-install hygiene: pyproject editable installs now overwrite
  cached site-packages copies cleanly.
- Cosmetic clean-up: remaining "ETF" labels in fund / compare-fund
  GUI / TUI / interactive prompts → "Fund".
- Validation: empty positional ticker, missing second comparison
  ticker, and `--recommend ""` now exit non-zero with a clear message.


## [4.0] - 2026-04-23

Part of **Lince Investor Suite v4.0** coordinated release.

### Added
- URL-safety enforcement for every RSS-sourced news URL and every
  `webbrowser.open(...)` site — powered by
  `lynx_investor_core.urlsafe`.
- Sector-specific ASCII art in easter-egg visuals (replaces the shared
  pickaxe motif that leaked into non-mining sectors).

### Changed
- Aligned every user-visible sector string with the package's real
  sector: titles, subtitles, app class names, splash taglines, news
  keywords, User-Agent headers, themes, export headers, and fortune
  quotes no longer carry template leftovers.
- Depends on `lynx-investor-core>=4.0`.

All notable changes to Lynx Communication Services Analysis are documented here.

## [3.0] - 2026-04-22

Part of **Lince Investor Suite v3.0** coordinated release.

### Added
- Uniform PageUp / PageDown navigation across every UI mode (GUI, TUI,
  interactive, console). Scrolling never goes above the current output
  in interactive and console mode; Shift+PageUp / Shift+PageDown remain
  reserved for the terminal emulator's own scrollback.
- Sector-mismatch warning now appends a `Suggestion: use
  'lynx-investor-<other>' instead.` line sourced from
  `lynx_investor_core.sector_registry`. The original warning text is
  preserved as-is.

### Changed
- TUI wires `lynx_investor_core.pager.PagingAppMixin` and
  `tui_paging_bindings()` into the main application.
- Graphical mode binds `<Prior>` / `<Next>` / `<Control-Home>` /
  `<Control-End>` via `bind_tk_paging()`.
- Interactive mode pages long output through `console_pager()` /
  `paged_print()`.
- Depends on `lynx-investor-core>=2.0`.

## [2.0] - 2026-04-22

Initial release of **Lynx Communication Services Analysis**, part of the **Lince Investor Suite v2.0**.

### Added
- **Comm-services lifecycle stages**: Startup / Subscriber Growth / Scale-Up / Mature / Dominant Platform
- **Comm-services sub-category classification**: Telecom-Wireless, Telecom-Wireline/Fiber, Cable & Satellite, Streaming, Entertainment, Internet Content & Search, Social Media & Interactive Media, Digital Advertising, Ad Agencies, Publishing, Broadcasting, Electronic Gaming
- **Comm-services-specific valuation metrics**: EV/Subscriber, EV/(EBITDA-Capex) (capex-adjusted), FCF Yield, Price per DAU, EV/ARR (subscription approx), EV/Gross-Profit, Rule-of-40-Adjusted EV/Revenue
- **Comm-services-specific profitability metrics**: ARPU & ARPU growth, content amortization intensity, content ROI, operating margin ex-content, advertising/subscription revenue mix, Rule of 40 (digital subsegments), SBC/Revenue, SBC/FCF, GAAP-vs-Adjusted gap
- **Comm-services-specific growth metrics**: Subscribers, subscriber net adds, subscriber growth YoY, MAU, DAU, DAU/MAU engagement ratio, ARR (subscription) growth, content intensity, content growth, ad revenue growth, cost per gross add (CPGA), revenue per subscriber, R&D intensity for internet/gaming
- **Comm-services-specific solvency metrics**: **Net Debt/EBITDA** (sector-critical leverage), capex/revenue, capex/subscriber, content obligations (off-balance), spectrum license book value, deferred revenue ratio, RPO coverage, goodwill/assets (M&A impairment risk)
- **Comm-services-specific efficiency metrics**: Subscriber Acquisition Payback (months), churn rate (annual), ARPU/CPGA ratio (LTV proxy), Rule of X (Altimeter), FCF Conversion
- **Sector Quality scoring**: Moat (network/spectrum/content/engagement, 20pts), Rule-of-40 (20pts), Financial Position/Leverage (15pts), Dilution/SBC (15pts), R&D/Content efficiency (10pts), Unit Economics (10pts), Revenue Predictability (10pts)
- **Severity system with 5 levels**: `***CRITICAL***` (red uppercase), `*WARNING*` (orange), `[WATCH]` (yellow), `[OK]` (green), `[STRONG]` (silver)
- **Impact column** on every metric table: Critical (blinking red), Important (orange), Relevant (yellow), Informational (green), Irrelevant (silver)
- **Sector validation gate**: refuses to analyze non-Communication-Services companies with prominent red-blinking warning, with clear pointer to sibling Lynx specialists
- **Comm-services benchmark context**: XLC headline benchmark + sub-sector ETFs (IYZ, FCOM, FDN, SOCL, PBS, HERO, ESPO, VOX) based on detected sub-sector
- **Comm-services investment disclaimers**: Cord-cutting, ad-cycle sensitivity, content-cost inflation, telecom price wars, antitrust/regulatory action, AI-driven competitive disruption, hit-driven gaming risk, sub-sector-specific guidance (carrier leverage, streaming content obligations, internet/social regulatory risk)
- **Intrinsic value adapted per stage and sub-sector**: DCF for platform/mature, EV/(EBITDA-Capex) + EV/Subscriber for carriers, EV/Subscriber + EV/ARR for streaming, FCF Yield anchor for internet platforms, Reverse DCF for all
- **Comprehensive unit tests** (189 passing): models, calculator, relevance, conclusion, explanations, export, sector validation, storage, edge cases
- **Comm-services-specific test fixtures** (Streaming Corp, Telecom carrier, leverage scenarios, content amortization scenarios)

### Sub-sector tickers covered (representative)
- **Wireless**: T, VZ, TMUS, VOD.L, DTE.DE, TEF.MC, BT.A.L, KDDIY
- **Wireline/Cable**: CMCSA, CHTR, LILA, LBRDA
- **Streaming/Entertainment**: NFLX, DIS, WBD, PARA, FOXA, LGF.A
- **Internet Content/Search**: GOOGL, BIDU
- **Social Media**: META, SNAP, PINS, RDDT, MTCH
- **Digital Advertising / Ad Agencies**: TTD, MGNI, OMC, IPG, WPP, PUB.PA
- **Publishing**: NYT, NWSA
- **Broadcasting**: SBGI, NXST, GTN, IHRT
- **Gaming**: EA, TTWO, RBLX, U, NTDOY

### Changed (vs Information Technology predecessor)
- Package renamed `lynx_tech` → `lynx_comm`
- CLI command renamed `lynx-tech` → `lynx-comm`
- `CompanyStage.GROWTH` label renamed (Hyper-Growth → Subscriber Growth)
- `TechCategory` enum replaced with `CommCategory` (12 comm-services sub-sectors instead of 12 IT sub-sectors)
- `TechQualityIndicators` dataclass renamed to `CommQualityIndicators` with comm-services-specific fields (network_quality_assessment, content_library_assessment, user_engagement_assessment, leverage_assessment, capex_cycle_assessment)
- `tech_category` field renamed to `comm_category`
- IT-only metrics removed/replaced; new comm-services metrics added (ARPU, churn, MAU/DAU, content amort/ROI, CPGA, EV/Subscriber, FCF yield, EV/(EBITDA-Capex), Net Debt/EBITDA, capex/subscriber, spectrum book value, content obligations)
- Tech benchmark (QQQ + IGV/WCLD/CIBR/SMH) replaced with Comm-Services benchmark (XLC + IYZ/FCOM/FDN/SOCL/PBS/HERO/ESPO/VOX)
- Screening checklist rewritten for comm-services (Rule-of-40 pass, moat gross margin, SBC contained, dilution, runway, **leverage discipline (Net Debt/EBITDA)**, **capex discipline**, insider alignment, growth, jurisdiction)
- Conclusion `_score_solvency` adds Net Debt/EBITDA scoring (carrier-tuned thresholds) and capex-build penalty
- Conclusion `_score_growth` adds subscriber growth & engagement (DAU/MAU) signals
- `calc_intrinsic_value` method selection adapted per stage for carriers/cable (EV/(EBITDA-Capex)), streaming (EV/Subscriber + EV/ARR), internet platforms (FCF Yield)

### Retained (from common architecture)
- Progressive rendering across four UI modes (Console, Interactive REPL, Textual TUI, Tkinter GUI)
- Rich-powered tables with relevance-based styling
- TXT / HTML / PDF export (with comm-services-adapted tables and sections)
- Local caching (production mode) and isolated testing mode (`data/` vs `data_test/`)
- SEC filings fetcher
- News fetcher (Yahoo Finance + Google News RSS)
- ISIN resolution, exchange-suffix search, and ticker validation
- BSD-3-Clause license, suite branding, ASCII logo support
