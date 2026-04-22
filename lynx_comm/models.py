"""Data models for Lynx Communication Services — telecom, streaming, internet, social, advertising & gaming fundamental analysis."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


# ---------------------------------------------------------------------------
# Company tier classification (market cap based)
# ---------------------------------------------------------------------------

class CompanyTier(str, Enum):
    MEGA = "Mega Cap"
    LARGE = "Large Cap"
    MID = "Mid Cap"
    SMALL = "Small Cap"
    MICRO = "Micro Cap"
    NANO = "Nano Cap"


def classify_tier(market_cap: Optional[float]) -> CompanyTier:
    if market_cap is None or market_cap <= 0:
        return CompanyTier.NANO
    if market_cap >= 200_000_000_000:
        return CompanyTier.MEGA
    if market_cap >= 10_000_000_000:
        return CompanyTier.LARGE
    if market_cap >= 2_000_000_000:
        return CompanyTier.MID
    if market_cap >= 300_000_000:
        return CompanyTier.SMALL
    if market_cap >= 50_000_000:
        return CompanyTier.MICRO
    return CompanyTier.NANO


# ---------------------------------------------------------------------------
# Communication Services company lifecycle stage classification
# ---------------------------------------------------------------------------

class CompanyStage(str, Enum):
    STARTUP = "Startup / Early-Stage"
    GROWTH = "Subscriber Growth"
    SCALE = "Scale-Up"
    MATURE = "Mature / Cash-Generative"
    PLATFORM = "Dominant Platform"


# ---------------------------------------------------------------------------
# Communication Services sub-sector classification
# ---------------------------------------------------------------------------

class CommCategory(str, Enum):
    TELECOM_WIRELESS = "Telecom Services — Wireless"
    TELECOM_WIRELINE = "Telecom Services — Wireline / Fiber"
    CABLE_SATELLITE = "Cable & Satellite"
    STREAMING = "Streaming & On-Demand Video"
    ENTERTAINMENT = "Entertainment / Diversified Media"
    INTERNET_CONTENT = "Internet Content & Search"
    SOCIAL_MEDIA = "Social Media & Interactive Media"
    DIGITAL_ADVERTISING = "Digital Advertising"
    AD_AGENCY = "Advertising Agencies / Marketing"
    PUBLISHING = "Publishing / News Media"
    BROADCASTING = "Broadcasting / Radio & TV"
    GAMING = "Electronic Gaming & Multimedia"
    OTHER = "Other Communication Services"


# ---------------------------------------------------------------------------
# Regulatory / jurisdiction tiering (Comm services lens: spectrum, content rules, data privacy, antitrust)
# ---------------------------------------------------------------------------

class JurisdictionTier(str, Enum):
    TIER_1 = "Tier 1 — Strong IP & Stable Regulation"
    TIER_2 = "Tier 2 — Moderate Regulatory Risk"
    TIER_3 = "Tier 3 — High Regulatory / Geopolitical Risk"
    UNKNOWN = "Unknown"


class Relevance(str, Enum):
    CRITICAL = "critical"
    IMPORTANT = "important"
    RELEVANT = "relevant"
    CONTEXTUAL = "contextual"
    IRRELEVANT = "irrelevant"


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    WATCH = "WATCH"
    OK = "OK"
    STRONG = "STRONG"
    NA = "N/A"


# ---------------------------------------------------------------------------
# Presentation helpers for Severity and Relevance (colors + wrappers)
# ---------------------------------------------------------------------------

SEVERITY_STYLE = {
    Severity.CRITICAL: {"wrap": ("***", "***"), "color": "bold red",  "label": "CRITICAL"},
    Severity.WARNING:  {"wrap": ("*", "*"),     "color": "#ff8800",   "label": "WARNING"},
    Severity.WATCH:    {"wrap": ("[", "]"),     "color": "yellow",    "label": "WATCH"},
    Severity.OK:       {"wrap": ("[", "]"),     "color": "green",     "label": "OK"},
    Severity.STRONG:   {"wrap": ("[", "]"),     "color": "grey70",    "label": "STRONG"},
    Severity.NA:       {"wrap": ("[", "]"),     "color": "grey50",    "label": "N/A"},
}


def format_severity(sev: "Severity") -> str:
    """Return a Rich-markup formatted severity tag.

    CRITICAL -> [bold red]***CRITICAL***[/]
    WARNING  -> [#ff8800]*WARNING*[/]
    WATCH    -> [yellow][WATCH][/]
    OK       -> [green][OK][/]
    STRONG   -> [grey70][STRONG][/]
    """
    style = SEVERITY_STYLE.get(sev, SEVERITY_STYLE[Severity.NA])
    pre, post = style["wrap"]
    label = style["label"]
    if sev == Severity.CRITICAL:
        label = label.upper()
    return f"[{style['color']}]{pre}{label}{post}[/]"


def severity_plain(sev: "Severity") -> str:
    """Plain-text severity token (no markup)."""
    style = SEVERITY_STYLE.get(sev, SEVERITY_STYLE[Severity.NA])
    pre, post = style["wrap"]
    label = style["label"]
    if sev == Severity.CRITICAL:
        label = label.upper()
    return f"{pre}{label}{post}"


IMPACT_STYLE = {
    Relevance.CRITICAL:   {"color": "blink bold red",  "label": "Critical"},
    Relevance.IMPORTANT:  {"color": "#ff8800",         "label": "Important"},
    Relevance.RELEVANT:   {"color": "yellow",          "label": "Relevant"},
    Relevance.CONTEXTUAL: {"color": "green",           "label": "Informational"},
    Relevance.IRRELEVANT: {"color": "grey70",          "label": "Irrelevant"},
}


def format_impact(rel: "Relevance") -> str:
    """Return Rich-markup formatted impact label for tables."""
    style = IMPACT_STYLE.get(rel, IMPACT_STYLE[Relevance.RELEVANT])
    return f"[{style['color']}]{style['label']}[/]"


def impact_plain(rel: "Relevance") -> str:
    style = IMPACT_STYLE.get(rel, IMPACT_STYLE[Relevance.RELEVANT])
    return style["label"]


# ---------------------------------------------------------------------------
# Core data models
# ---------------------------------------------------------------------------

@dataclass
class CompanyProfile:
    ticker: str
    name: str
    isin: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    country: Optional[str] = None
    exchange: Optional[str] = None
    currency: Optional[str] = None
    market_cap: Optional[float] = None
    description: Optional[str] = None
    website: Optional[str] = None
    employees: Optional[int] = None
    tier: CompanyTier = CompanyTier.NANO
    stage: CompanyStage = CompanyStage.STARTUP
    comm_category: CommCategory = CommCategory.OTHER
    jurisdiction_tier: JurisdictionTier = JurisdictionTier.UNKNOWN
    jurisdiction_country: Optional[str] = None


@dataclass
class ValuationMetrics:
    pe_trailing: Optional[float] = None
    pe_forward: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    p_fcf: Optional[float] = None
    ev_ebitda: Optional[float] = None
    ev_revenue: Optional[float] = None
    ev_gross_profit: Optional[float] = None
    peg_ratio: Optional[float] = None
    dividend_yield: Optional[float] = None
    earnings_yield: Optional[float] = None
    enterprise_value: Optional[float] = None
    market_cap: Optional[float] = None
    price_to_tangible_book: Optional[float] = None
    price_to_ncav: Optional[float] = None
    cash_to_market_cap: Optional[float] = None
    # Communication Services-specific valuation
    ev_to_subscriber: Optional[float] = None        # EV / subscriber (telecom, streaming, cable)
    ev_to_arr: Optional[float] = None               # EV / annualized recurring revenue (streaming/SaaS-like)
    ev_per_employee: Optional[float] = None
    ev_to_ebitda_capex_adj: Optional[float] = None  # EV / (EBITDA - capex), capex-heavy telecom adj.
    fcf_yield: Optional[float] = None               # FCF / market cap (mature carriers, ad-platforms)
    price_per_dau: Optional[float] = None           # Market cap / daily active users (social/internet)
    rule_of_40_adj_multiple: Optional[float] = None


@dataclass
class ProfitabilityMetrics:
    roe: Optional[float] = None
    roa: Optional[float] = None
    roic: Optional[float] = None
    gross_margin: Optional[float] = None
    operating_margin: Optional[float] = None
    net_margin: Optional[float] = None
    fcf_margin: Optional[float] = None
    ebitda_margin: Optional[float] = None
    # Communication Services-specific profitability
    rule_of_40: Optional[float] = None              # Growth + FCF margin (digital/streaming subsectors)
    rule_of_40_ebitda: Optional[float] = None
    arpu: Optional[float] = None                    # Average revenue per user/subscriber (USD)
    arpu_growth_yoy: Optional[float] = None         # ARPU YoY growth %
    content_amort_intensity: Optional[float] = None # Content amortization / revenue (streaming/media)
    content_roi: Optional[float] = None             # (Content revenue - amortization) / amortization
    operating_margin_ex_content: Optional[float] = None  # Op margin excluding content amort
    advertising_revenue_pct: Optional[float] = None # Ad revenue as % of total
    subscription_revenue_pct: Optional[float] = None # Recurring/subscription revenue % of total
    magic_number: Optional[float] = None
    gaap_vs_adj_gap: Optional[float] = None
    sbc_to_revenue: Optional[float] = None
    sbc_to_fcf: Optional[float] = None


@dataclass
class SolvencyMetrics:
    debt_to_equity: Optional[float] = None
    debt_to_ebitda: Optional[float] = None
    current_ratio: Optional[float] = None
    quick_ratio: Optional[float] = None
    interest_coverage: Optional[float] = None
    altman_z_score: Optional[float] = None
    net_debt: Optional[float] = None
    total_debt: Optional[float] = None
    total_cash: Optional[float] = None
    cash_burn_rate: Optional[float] = None
    cash_runway_years: Optional[float] = None
    working_capital: Optional[float] = None
    cash_per_share: Optional[float] = None
    tangible_book_value: Optional[float] = None
    ncav: Optional[float] = None
    ncav_per_share: Optional[float] = None
    quarterly_burn_rate: Optional[float] = None
    burn_as_pct_of_market_cap: Optional[float] = None
    # Communication Services-specific solvency (capex/leverage focus for telecom/cable)
    cash_coverage_months: Optional[float] = None
    capex_to_revenue: Optional[float] = None        # Network capex intensity (telecom/cable)
    capex_to_subscriber: Optional[float] = None     # Network capex per subscriber
    net_debt_to_ebitda: Optional[float] = None      # Leverage — critical for telecom/cable
    spectrum_license_book_value: Optional[float] = None  # Wireless spectrum on balance sheet
    content_obligations: Optional[float] = None     # Off-balance content commitments (streaming)
    rpo_coverage: Optional[float] = None
    goodwill_to_assets: Optional[float] = None      # M&A-heavy sector — content/spectrum acquisitions
    deferred_revenue_ratio: Optional[float] = None


@dataclass
class GrowthMetrics:
    revenue_growth_yoy: Optional[float] = None
    revenue_cagr_3y: Optional[float] = None
    revenue_cagr_5y: Optional[float] = None
    earnings_growth_yoy: Optional[float] = None
    earnings_cagr_3y: Optional[float] = None
    earnings_cagr_5y: Optional[float] = None
    fcf_growth_yoy: Optional[float] = None
    book_value_growth_yoy: Optional[float] = None
    dividend_growth_5y: Optional[float] = None
    shares_growth_yoy: Optional[float] = None
    shares_growth_3y_cagr: Optional[float] = None
    fully_diluted_shares: Optional[float] = None
    dilution_ratio: Optional[float] = None
    # Communication Services-specific growth (subscribers, engagement, ARPU, content)
    subscribers: Optional[float] = None             # Total subscribers (telecom, streaming, cable)
    subscriber_net_adds: Optional[float] = None     # Net new subs in latest period
    subscriber_growth_yoy: Optional[float] = None   # Subscriber YoY growth %
    mau: Optional[float] = None                     # Monthly active users (social/internet)
    dau: Optional[float] = None                     # Daily active users
    dau_mau_ratio: Optional[float] = None           # Engagement ratio
    arr_growth_yoy: Optional[float] = None          # Recurring/subscription revenue growth (streaming)
    net_revenue_retention: Optional[float] = None   # Where disclosed
    gross_revenue_retention: Optional[float] = None
    content_intensity: Optional[float] = None       # Content investment / revenue (streaming/media)
    content_growth_yoy: Optional[float] = None      # Content spend YoY change
    rd_intensity: Optional[float] = None            # R&D / revenue (internet content, gaming, AI-heavy carriers)
    rd_growth_yoy: Optional[float] = None           # R&D spend YoY change
    sales_marketing_intensity: Optional[float] = None
    cost_per_gross_add: Optional[float] = None      # CPGA — subscriber acquisition cost (telecom/streaming)
    advertising_revenue_growth_yoy: Optional[float] = None  # Ad revenue growth (search, social, broadcast)
    employee_growth_yoy: Optional[float] = None
    revenue_per_employee: Optional[float] = None
    revenue_per_subscriber: Optional[float] = None  # Total rev / subs (overlaps ARPU)
    operating_leverage: Optional[float] = None


@dataclass
class EfficiencyMetrics:
    asset_turnover: Optional[float] = None
    inventory_turnover: Optional[float] = None
    receivables_turnover: Optional[float] = None
    days_sales_outstanding: Optional[float] = None
    days_inventory: Optional[float] = None
    cash_conversion_cycle: Optional[float] = None
    # Communication Services-specific efficiency
    rule_of_x_score: Optional[float] = None
    cac_payback_months: Optional[float] = None      # Subscriber acquisition payback (months)
    churn_rate_annual: Optional[float] = None       # Annualized subscriber churn % (lower = better)
    arpu_to_cpga_ratio: Optional[float] = None      # ARPU / Cost per gross add (LTV proxy)
    fcf_conversion: Optional[float] = None          # FCF / Net income


@dataclass
class CommQualityIndicators:
    """Quality scoring specific to Communication Services companies."""
    quality_score: Optional[float] = None
    management_quality: Optional[str] = None
    insider_ownership_pct: Optional[float] = None
    founder_led: Optional[str] = None
    moat_assessment: Optional[str] = None
    moat_type: Optional[str] = None                       # Network effects / spectrum / content library / switching costs
    competitive_position: Optional[str] = None
    network_quality_assessment: Optional[str] = None      # Spectrum, fiber footprint, 5G coverage
    content_library_assessment: Optional[str] = None      # IP/content depth (streaming/media)
    user_engagement_assessment: Optional[str] = None      # DAU/MAU, time spent, ad pricing power
    rd_efficiency_assessment: Optional[str] = None        # R&D / content efficiency narrative
    unit_economics: Optional[str] = None                  # ARPU/Churn/CPGA economics
    platform_position: Optional[str] = None
    financial_position: Optional[str] = None
    dilution_risk: Optional[str] = None
    leverage_assessment: Optional[str] = None             # Net debt/EBITDA — telecom/cable critical
    capex_cycle_assessment: Optional[str] = None          # Network buildout vs harvest phase
    rule_of_40_assessment: Optional[str] = None
    sbc_risk_assessment: Optional[str] = None
    catalyst_density: Optional[str] = None
    near_term_catalysts: list[str] = field(default_factory=list)
    revenue_predictability: Optional[str] = None          # Subscription mix vs ad cyclicality
    roic_history: list[Optional[float]] = field(default_factory=list)
    gross_margin_history: list[Optional[float]] = field(default_factory=list)
    arpu_history: list[Optional[float]] = field(default_factory=list)
    churn_history: list[Optional[float]] = field(default_factory=list)


@dataclass
class IntrinsicValue:
    dcf_value: Optional[float] = None
    graham_number: Optional[float] = None
    lynch_fair_value: Optional[float] = None
    ncav_value: Optional[float] = None
    asset_based_value: Optional[float] = None
    ev_sales_implied_price: Optional[float] = None
    reverse_dcf_growth: Optional[float] = None
    current_price: Optional[float] = None
    margin_of_safety_dcf: Optional[float] = None
    margin_of_safety_graham: Optional[float] = None
    margin_of_safety_ncav: Optional[float] = None
    margin_of_safety_asset: Optional[float] = None
    margin_of_safety_ev_sales: Optional[float] = None
    primary_method: Optional[str] = None
    secondary_method: Optional[str] = None


@dataclass
class ShareStructure:
    shares_outstanding: Optional[float] = None
    fully_diluted_shares: Optional[float] = None
    warrants_outstanding: Optional[float] = None
    options_outstanding: Optional[float] = None
    rsu_outstanding: Optional[float] = None
    insider_ownership_pct: Optional[float] = None
    institutional_ownership_pct: Optional[float] = None
    float_shares: Optional[float] = None
    dual_class_structure: Optional[bool] = None
    share_structure_assessment: Optional[str] = None
    sbc_overhang_risk: Optional[str] = None


@dataclass
class InsiderTransaction:
    insider: str = ""
    position: str = ""
    transaction_type: str = ""
    shares: Optional[float] = None
    value: Optional[float] = None
    date: str = ""


@dataclass
class MarketIntelligence:
    """Market sentiment, insider activity, institutional holdings, and technicals."""
    insider_transactions: list[InsiderTransaction] = field(default_factory=list)
    net_insider_shares_3m: Optional[float] = None
    insider_buy_signal: Optional[str] = None

    top_holders: list[str] = field(default_factory=list)
    institutions_count: Optional[int] = None
    institutions_pct: Optional[float] = None

    analyst_count: Optional[int] = None
    recommendation: Optional[str] = None
    target_high: Optional[float] = None
    target_low: Optional[float] = None
    target_mean: Optional[float] = None
    target_upside_pct: Optional[float] = None

    shares_short: Optional[float] = None
    short_pct_of_float: Optional[float] = None
    short_ratio_days: Optional[float] = None
    short_squeeze_risk: Optional[str] = None

    price_current: Optional[float] = None
    price_52w_high: Optional[float] = None
    price_52w_low: Optional[float] = None
    pct_from_52w_high: Optional[float] = None
    pct_from_52w_low: Optional[float] = None
    price_52w_range_position: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    above_sma_50: Optional[bool] = None
    above_sma_200: Optional[bool] = None
    golden_cross: Optional[bool] = None
    beta: Optional[float] = None
    avg_volume: Optional[float] = None
    volume_10d_avg: Optional[float] = None
    volume_trend: Optional[str] = None

    projected_dilution_annual_pct: Optional[float] = None
    projected_shares_in_2y: Optional[float] = None
    financing_warning: Optional[str] = None

    # Communication Services benchmark context (XLC / VOX / FCOM)
    benchmark_name: Optional[str] = None
    benchmark_ticker: Optional[str] = None
    benchmark_price: Optional[float] = None
    benchmark_52w_high: Optional[float] = None
    benchmark_52w_low: Optional[float] = None
    benchmark_52w_position: Optional[float] = None
    benchmark_ytd_change: Optional[float] = None

    sector_etf_name: Optional[str] = None
    sector_etf_ticker: Optional[str] = None
    sector_etf_price: Optional[float] = None
    sector_etf_3m_perf: Optional[float] = None
    peer_etf_name: Optional[str] = None
    peer_etf_ticker: Optional[str] = None
    peer_etf_price: Optional[float] = None
    peer_etf_3m_perf: Optional[float] = None

    risk_warnings: list[str] = field(default_factory=list)
    disclaimers: list[str] = field(default_factory=list)


@dataclass
class FinancialStatement:
    period: str
    revenue: Optional[float] = None
    cost_of_revenue: Optional[float] = None
    gross_profit: Optional[float] = None
    operating_income: Optional[float] = None
    net_income: Optional[float] = None
    ebitda: Optional[float] = None
    interest_expense: Optional[float] = None
    total_assets: Optional[float] = None
    total_liabilities: Optional[float] = None
    total_equity: Optional[float] = None
    total_debt: Optional[float] = None
    total_cash: Optional[float] = None
    current_assets: Optional[float] = None
    current_liabilities: Optional[float] = None
    operating_cash_flow: Optional[float] = None
    capital_expenditure: Optional[float] = None
    free_cash_flow: Optional[float] = None
    dividends_paid: Optional[float] = None
    shares_outstanding: Optional[float] = None
    eps: Optional[float] = None
    book_value_per_share: Optional[float] = None
    # Communication Services-specific financial line items
    research_development: Optional[float] = None         # R&D (internet/gaming/streaming tech)
    selling_general_admin: Optional[float] = None
    stock_based_compensation: Optional[float] = None
    deferred_revenue: Optional[float] = None             # Prepaid subscriptions / advance billings
    goodwill: Optional[float] = None                     # M&A-heavy sector
    intangibles: Optional[float] = None                  # Spectrum licenses, customer relationships, content IP
    content_amortization: Optional[float] = None         # Streaming/media content amort expense
    content_assets: Optional[float] = None               # Capitalized content on balance sheet
    advertising_revenue: Optional[float] = None
    subscription_revenue: Optional[float] = None
    licensing_revenue: Optional[float] = None


@dataclass
class AnalysisConclusion:
    overall_score: float = 0.0
    verdict: str = ""
    summary: str = ""
    category_scores: dict = field(default_factory=dict)
    category_summaries: dict = field(default_factory=dict)
    strengths: list = field(default_factory=list)
    risks: list = field(default_factory=list)
    tier_note: str = ""
    stage_note: str = ""
    screening_checklist: dict = field(default_factory=dict)


@dataclass
class MetricExplanation:
    key: str
    full_name: str
    description: str
    why_used: str
    formula: str
    category: str


@dataclass
class Filing:
    form_type: str
    filing_date: str
    period: str
    url: str
    description: Optional[str] = None
    local_path: Optional[str] = None


@dataclass
class NewsArticle:
    title: str
    url: str
    published: Optional[str] = None
    source: Optional[str] = None
    summary: Optional[str] = None
    local_path: Optional[str] = None


@dataclass
class AnalysisReport:
    profile: CompanyProfile
    valuation: Optional[ValuationMetrics] = None
    profitability: Optional[ProfitabilityMetrics] = None
    solvency: Optional[SolvencyMetrics] = None
    growth: Optional[GrowthMetrics] = None
    efficiency: Optional[EfficiencyMetrics] = None
    comm_quality: Optional[CommQualityIndicators] = None
    intrinsic_value: Optional[IntrinsicValue] = None
    share_structure: Optional[ShareStructure] = None
    market_intelligence: Optional[MarketIntelligence] = None
    financials: list[FinancialStatement] = field(default_factory=list)
    filings: list[Filing] = field(default_factory=list)
    news: list[NewsArticle] = field(default_factory=list)
    fetched_at: str = field(default_factory=lambda: datetime.now().isoformat())


# ---------------------------------------------------------------------------
# Stage classification helpers (Communication Services lifecycle)
# ---------------------------------------------------------------------------

_STAGE_KEYWORDS = {
    CompanyStage.PLATFORM: [
        "dominant platform", "global platform", "ecosystem", "market-leading carrier",
        "leading social network", "largest streaming", "search dominance",
        "incumbent operator", "tier-1 carrier", "national carrier",
    ],
    CompanyStage.MATURE: [
        "mature", "free cash flow positive", "buyback", "dividend",
        "cash-generative", "established carrier", "legacy media", "profitable",
        "harvest phase", "stable subscriber base",
    ],
    CompanyStage.SCALE: [
        "scaling", "expanding internationally", "scale-up",
        "profitability pathway", "expanding subscriber base", "national rollout",
        "5G rollout", "fiber expansion",
    ],
    CompanyStage.GROWTH: [
        "subscriber growth", "user growth", "rapid growth", "hypergrowth",
        "land and expand", "subscription growth", "MAU growth", "DAU growth",
        "viral growth",
    ],
    CompanyStage.STARTUP: [
        "startup", "early stage", "seed", "pre-revenue", "emerging",
        "venture-backed", "newly public",
    ],
}


_CATEGORY_KEYWORDS = {
    CommCategory.TELECOM_WIRELESS: [
        "wireless carrier", "mobile network operator", "mno", "5g network",
        "lte network", "cellular service", "wireless service", "mobile carrier",
        "spectrum license", "wireless subscribers",
    ],
    CommCategory.TELECOM_WIRELINE: [
        "wireline", "fiber-to-the-home", "fttp", "fiber broadband",
        "fixed-line", "landline", "ilec", "clec", "fiber optic network",
        "broadband internet provider",
    ],
    CommCategory.CABLE_SATELLITE: [
        "cable operator", "cable television", "satellite tv", "msv",
        "satellite communications", "set-top box", "dbs", "pay-tv",
        "multichannel video",
    ],
    CommCategory.STREAMING: [
        "streaming", "subscription video", "svod", "video on demand",
        "ott video", "streaming service", "direct-to-consumer streaming",
        "over-the-top",
    ],
    CommCategory.ENTERTAINMENT: [
        "film studio", "entertainment", "movie production", "tv production",
        "theatrical", "box office", "diversified media", "studio",
        "theme park",
    ],
    CommCategory.INTERNET_CONTENT: [
        "search engine", "internet content", "online portal",
        "internet platform", "web search", "online services",
    ],
    CommCategory.SOCIAL_MEDIA: [
        "social media", "social network", "messaging platform",
        "interactive media", "user-generated content", "ugc",
        "online community", "dating app",
    ],
    CommCategory.DIGITAL_ADVERTISING: [
        "digital advertising", "ad tech", "programmatic advertising",
        "ad exchange", "demand-side platform", "supply-side platform",
        "online advertising",
    ],
    CommCategory.AD_AGENCY: [
        "advertising agency", "marketing services", "media agency",
        "creative agency", "public relations", "marketing communications",
        "advertising holding",
    ],
    CommCategory.PUBLISHING: [
        "publishing", "newspaper", "magazine", "news media",
        "digital publishing", "journalism", "book publisher",
    ],
    CommCategory.BROADCASTING: [
        "broadcasting", "broadcast television", "radio broadcasting",
        "tv station", "radio station", "free-to-air",
    ],
    CommCategory.GAMING: [
        "video game", "electronic gaming", "gaming publisher",
        "interactive entertainment", "esports", "mobile gaming",
        "console gaming", "game studio",
    ],
}


_TIER_1_JURISDICTIONS = {
    "united states", "usa", "canada", "united kingdom", "uk", "ireland",
    "germany", "france", "netherlands", "sweden", "denmark", "finland",
    "norway", "switzerland", "luxembourg", "belgium", "austria",
    "australia", "new zealand", "japan", "south korea", "singapore",
    "israel", "taiwan",
}

_TIER_2_JURISDICTIONS = {
    "spain", "portugal", "italy", "poland", "czech republic", "estonia",
    "latvia", "lithuania", "hungary", "greece", "cyprus",
    "hong kong", "india", "brazil", "mexico", "south africa", "chile",
    "uruguay", "turkey",
}


def classify_stage(description: Optional[str], revenue: Optional[float],
                   info: Optional[dict] = None) -> CompanyStage:
    if description is None:
        description = ""
    desc_lower = description.lower()

    rev = revenue or 0
    info = info or {}
    profit_margin = info.get("profitMargins")
    growth = info.get("revenueGrowth")

    if rev < 10_000_000 and (growth is None or growth < 0.10):
        return CompanyStage.STARTUP

    for stage in [CompanyStage.PLATFORM, CompanyStage.MATURE, CompanyStage.SCALE,
                  CompanyStage.GROWTH, CompanyStage.STARTUP]:
        for kw in _STAGE_KEYWORDS[stage]:
            if kw.lower() in desc_lower:
                return stage

    mcap = info.get("marketCap") or 0
    if mcap >= 200_000_000_000:
        return CompanyStage.PLATFORM
    if profit_margin is not None and profit_margin > 0.20 and mcap >= 10_000_000_000:
        return CompanyStage.MATURE
    if growth is not None and growth > 0.30:
        return CompanyStage.GROWTH
    if rev >= 500_000_000:
        return CompanyStage.SCALE
    return CompanyStage.GROWTH


def classify_category(description: Optional[str],
                      industry: Optional[str] = None) -> CommCategory:
    import re
    text = ((description or "") + " " + (industry or "")).lower()
    scores: dict[CommCategory, int] = {}
    for cat, keywords in _CATEGORY_KEYWORDS.items():
        count = 0
        for kw in keywords:
            kw_lower = kw.lower()
            if len(kw_lower) <= 3:
                if re.search(r'\b' + re.escape(kw_lower) + r'\b', text):
                    count += 1
            else:
                if kw_lower in text:
                    count += 1
        if count > 0:
            scores[cat] = count
    if scores:
        return max(scores, key=scores.get)
    return CommCategory.OTHER


def classify_jurisdiction(country: Optional[str],
                          description: Optional[str] = None) -> JurisdictionTier:
    if not country:
        return JurisdictionTier.UNKNOWN
    c_lower = country.lower().strip()
    desc_lower = (description or "").lower()
    for j in _TIER_1_JURISDICTIONS:
        if j in c_lower or j in desc_lower:
            return JurisdictionTier.TIER_1
    for j in _TIER_2_JURISDICTIONS:
        if j in c_lower or j in desc_lower:
            return JurisdictionTier.TIER_2
    return JurisdictionTier.TIER_3


# Backwards-compat aliases — kept for callers that still import the old names.
classify_commodity = classify_category  # pragma: no cover
Commodity = CommCategory  # pragma: no cover
