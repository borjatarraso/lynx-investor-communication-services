"""Communication-Services-focused sector and industry insights."""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SectorInsight:
    sector: str; overview: str; critical_metrics: list[str] = field(default_factory=list)
    key_risks: list[str] = field(default_factory=list); what_to_watch: list[str] = field(default_factory=list)
    typical_valuation: str = ""

@dataclass
class IndustryInsight:
    industry: str; sector: str; overview: str; critical_metrics: list[str] = field(default_factory=list)
    key_risks: list[str] = field(default_factory=list); what_to_watch: list[str] = field(default_factory=list)
    typical_valuation: str = ""

_SECTORS: dict[str, SectorInsight] = {}
_INDUSTRIES: dict[str, IndustryInsight] = {}

def _add_sector(sector, overview, cm, kr, wtw, tv):
    _SECTORS[sector.lower()] = SectorInsight(sector=sector, overview=overview, critical_metrics=cm, key_risks=kr, what_to_watch=wtw, typical_valuation=tv)

def _add_industry(industry, sector, overview, cm, kr, wtw, tv):
    _INDUSTRIES[industry.lower()] = IndustryInsight(industry=industry, sector=sector, overview=overview, critical_metrics=cm, key_risks=kr, what_to_watch=wtw, typical_valuation=tv)


# ── Sector overview ──────────────────────────────────────────────
_add_sector("Communication Services",
    "Communication Services is a hybrid sector merging legacy telecom (high-capex, high-leverage, low-growth, high-dividend) with internet platforms (asset-light, ad-driven, network-effect moats) and entertainment/streaming (content-IP-driven, content-amortization heavy). The sector splits sharply by sub-industry: integrated carriers (T, VZ, TMUS, DTE) compete on network coverage, ARPU, and capex efficiency; internet platforms (GOOGL, META) compete on engagement (DAU/MAU) and ad pricing; streaming (NFLX, DIS, WBD) competes on content library, churn, and ARPU; gaming (EA, TTWO, RBLX) on hit-rate and live-services monetization. The Rule of 40 still applies to digital subsegments; for telecom, FCF yield, dividend coverage, and net debt/EBITDA dominate.",
    ["ARPU & ARPU growth", "Subscriber net adds & churn", "DAU/MAU engagement (digital)", "FCF margin / FCF yield", "Net debt / EBITDA (telecom/cable)", "Capex / Revenue (network buildout)", "Content amortization intensity (streaming)", "Operating margin"],
    ["Cord-cutting / pay-TV decline accelerating", "Ad cycle reversals (multi-quarter downturns)", "Streaming content cost inflation eroding margins", "Telecom price wars compressing ARPU", "Antitrust / regulatory action (Big Tech, M&A)", "5G / fiber capex cycle peak vs harvest mismatch", "iOS privacy & cookie deprecation reducing ad attribution", "AI-driven competitive disruption (search, content)"],
    ["Postpaid net adds & churn (wireless)", "Streaming subscriber net adds & churn", "Ad pricing & impression growth (search/social)", "Engagement metrics (DAU/MAU, time-spent)", "Content amortization vs revenue", "5G capex peak timing", "Spectrum auction outcomes", "Dividend coverage & buyback cadence"],
    "Highly bimodal: telecom/cable trade at EV/EBITDA 6-9x (capex-heavy, leveraged); internet platforms 12-22x; streaming 18-30x at growth, 8-15x mature. P/E 12-20x mature platforms; dividend-paying carriers offer 4-7% yield with capex-constrained growth.")


# ── Telecom Services — Wireless ───────────────────────────────────
_add_industry("Telecom Services", "Communication Services",
    "Wireless and wireline carriers (AT&T, Verizon, T-Mobile US, BT, Vodafone, Telefonica, KDDI). Capital-intensive (spectrum + tower + fiber). 3-5 year capex cycles tied to G-transitions (4G→5G→6G). Stable ARPU with low single-digit subscriber growth. Mature carriers prioritize FCF, dividend, and deleveraging over growth. T-Mobile US is the structural growth outlier (Sprint integration + 5G mid-band lead).",
    ["Wireless postpaid net adds (>0 = winning share)", "Postpaid phone churn (<1.0% = best-in-class)", "Service ARPU & ARPU growth", "Capex / Revenue (15-25% during 5G build)", "Net debt / EBITDA (target <3.0x)", "FCF & FCF yield (5-8%+)", "Dividend coverage from FCF"],
    ["Price-war intensification (postpaid promo escalation)", "Spectrum auction overpayment", "Fiber overbuild compressing wireline ROI", "Cord-cutting on bundled services", "Tower lease cost inflation", "Macro consumer downgrades (prepaid shift)", "Cable wireless MVNO erosion of subscriber base"],
    ["Postpaid phone net adds (zero-sum with peers)", "Churn trends quarter-over-quarter", "Service revenue ex-equipment growth", "Capex peak vs harvest signaling", "Fiber subscriber adds", "Promotional intensity"],
    "EV/EBITDA 6-9x; FCF yield 5-8%; dividend yield 4-7%. Premium to peers for share-takers (TMUS); discount for declining ARPU + leverage.")


# ── Cable & Satellite ─────────────────────────────────────────────
_add_industry("Telecom Services - Cable", "Communication Services",
    "Cable and satellite operators (Comcast, Charter, Liberty Latin America, DirecTV, Dish). Built on legacy video, increasingly broadband-and-mobile-first as cord-cutting compresses video. Strong free cash flow generation; broadband HSD ARPU offsetting video losses. MVNO wireless layer (Comcast Xfinity Mobile, Charter Spectrum Mobile) is a recent growth driver but capacity-constrained.",
    ["Broadband net adds (declining post-2022 saturation)", "Broadband ARPU & growth", "Video subscriber losses (managing decline)", "Mobile lines added (MVNO economics)", "FCF margin & coverage", "Capex / Revenue (10-15%)", "Net debt / EBITDA (typically 4-5x)"],
    ["Fiber overbuild (T, Frontier, AT&T) compressing pricing", "FWA (T-Mobile, Verizon 5G home internet) taking share", "Video losses accelerating", "MVNO economics squeezed by carrier wholesale rates", "Programming cost inflation", "High leverage — refinancing risk"],
    ["Broadband net adds (fiber/FWA take-rate)", "Video sub-loss cadence", "Wireless line adds & ARPU", "Capex per home passed", "Spectrum auction outcomes for cable wireless"],
    "EV/EBITDA 6-9x; FCF yield 6-10%. Discount for declining broadband adds; premium for fiber overbuild defenders.")


# ── Streaming & On-Demand Video ───────────────────────────────────
_add_industry("Entertainment", "Communication Services",
    "Streaming, film/TV studios, theme parks, and diversified media (Netflix, Disney, Warner Bros Discovery, Paramount, Fox, Lions Gate). Streaming has become the dominant lens. Netflix is profitable and FCF-positive; legacy studios still in transition with high content amortization and subscriber losses on legacy linear. Content amortization runs 35-55% of revenue. Subscriber net adds, ARPU, and churn are the canonical KPIs.",
    ["Streaming subscriber net adds & churn", "ARPU & ARPU growth (ad-tier dilution)", "Content amortization / revenue (35-55%)", "Operating margin (Netflix >25%; legacy <10%)", "FCF & FCF margin", "Content ROI (revenue / amortization)", "Engagement (hours per subscriber)"],
    ["Subscriber growth saturation in mature markets (US, UK)", "Password-sharing crackdowns one-time benefit", "Content cost inflation (sports rights, talent)", "Linear TV / cable bundle decline", "Theatrical box-office volatility", "Streaming consolidation pressure", "Ad-tier ARPU dilution"],
    ["Net subscriber adds by region (LATAM, APAC = growth)", "Churn trends post-price-hike", "Content slate ROI signals", "Ad-tier penetration & monetization", "Linear vs streaming OIBDA crossover", "Live sports rights renewal cycles"],
    "EV/EBITDA 12-25x for streaming-pure; 6-12x for legacy media in transition. Netflix premium to peers reflects FCF + operating leverage.")


# ── Internet Content & Search ────────────────────────────────────
_add_industry("Internet Content & Information", "Communication Services",
    "Search, internet portals, online services (Alphabet/Google, Baidu, Yandex, Yahoo). Platform economics with massive operating leverage. Ad revenue is dominant; cloud/other-bets diversifying. AI search disruption (ChatGPT, Perplexity) is the central thesis question. Very high gross margin (50-60%); operating margin 25-35% mature.",
    ["Ad revenue growth (search, YouTube, network)", "Operating margin (target >25%)", "FCF margin (>20%)", "Capex intensity (AI infrastructure 15-25%)", "EV/EBITDA", "Other Bets contribution"],
    ["AI-search erosion of query monetization", "Antitrust remedies (search default deals)", "Ad cycle reversals", "iOS / cookie deprecation impact on attribution", "Cloud price competition", "AI capex intensity outpacing revenue ramp"],
    ["Search query volume & monetization rate", "YouTube ad + subscription growth", "AI capex growth & cloud revenue acceleration", "Court rulings on antitrust remedies", "Ad pricing power"],
    "EV/EBITDA 14-20x; P/E 22-28x; FCF yield anchor (3-5%). Premium for cloud growth & operating leverage.")


# ── Social Media & Interactive Media ──────────────────────────────
_add_industry("Internet Content & Information - Social", "Communication Services",
    "Social and interactive media (Meta, Snap, Pinterest, Reddit, Match Group). Engagement-driven — DAU/MAU and time-spent are the leading indicators of ad pricing power. Reels, Shorts, TikTok-style short-form video have reshaped the competitive landscape. AI ad-targeting is the durable moat.",
    ["DAU & MAU growth", "DAU/MAU ratio (engagement, target >65%)", "ARPU by region (US/CA highest)", "Ad impressions × price growth decomposition", "Operating margin (>30% mature)", "FCF margin"],
    ["TikTok / short-form competitive displacement", "Regulatory action (Section 230, child safety, antitrust)", "iOS privacy compressing attribution", "Reality Labs / metaverse capex burn (Meta)", "Ad cycle reversals", "Brand-safety boycotts"],
    ["DAU growth & engagement metrics", "Ad pricing vs impressions decomposition", "Reels / short-form monetization closing gap", "AI-driven ad-targeting incremental ROI", "Reality Labs operating losses cadence"],
    "EV/EBITDA 12-18x; P/E 18-25x. Premium for engagement leadership; discount for capex burn (Reality Labs).")


# ── Digital Advertising / Ad Tech ─────────────────────────────────
_add_industry("Advertising Agencies", "Communication Services",
    "Advertising holding companies and ad-tech (WPP, Omnicom, Publicis, Interpublic, Trade Desk, Magnite). Holding companies are mature, FCF-stable, dividend-paying — facing structural disruption from in-house brand teams + AI creative. Ad-tech (Trade Desk especially) is growth + margin expansion play.",
    ["Organic revenue growth (low single digits for holdcos)", "Operating margin (holdcos 14-18%)", "FCF / Net income conversion", "Take rate (ad-tech)", "Customer concentration"],
    ["AI creative compressing agency model", "In-house brand teams reducing fees", "Ad cycle reversals", "Big Tech walled gardens (Meta, Google, Amazon) absorbing budgets", "Programmatic disintermediation"],
    ["Organic growth vs reported (FX & M&A adjusted)", "AI productivity initiative results", "Ad-tech take rate trends", "Connected TV (CTV) ad spend share"],
    "Holdcos: P/E 9-13x, dividend 3-5%. Ad-tech: EV/EBITDA 18-28x at high growth, EV/Sales 5-12x.")


# ── Publishing / News Media ───────────────────────────────────────
_add_industry("Publishing", "Communication Services",
    "Newspapers, magazines, news media in digital transition (NYT, News Corp, Gannett, dpa). Digital subscription is the survival path — print revenue continues a structural decline. Best operators (NYT) demonstrate that high-quality journalism can be a recurring-revenue, operating-leverage business.",
    ["Digital subscriber net adds & churn", "Digital ARPU", "Subscription revenue mix (target >50%)", "Operating margin (improving from negative to 15%+)", "FCF margin"],
    ["Print decline outpacing digital growth", "Aggregator (Apple News, Google) revenue-share squeeze", "Algorithmic content commoditization", "Ad spend continued shift to platforms", "Trust / political polarization affecting brand"],
    ["Digital sub net adds & ARPU", "Print decline cadence", "Data licensing deals with downstream platforms", "Bundling strategies (NYT cooking, athletic, games)"],
    "P/E 18-30x for digital winners (NYT); 5-10x for print-heavy declining names; EV/EBITDA 8-14x.")


# ── Broadcasting / Radio & TV ────────────────────────────────────
_add_industry("Broadcasting", "Communication Services",
    "Local TV broadcasters and radio (Sinclair, Nexstar, Gray, iHeartMedia, Cumulus). Highly cyclical via political ad spend (presidential election years 2x non-political). Cord-cutting is structural headwind; retransmission consent fees provide partial offset. High leverage common.",
    ["Core advertising revenue", "Political advertising revenue (election cycle)", "Retransmission revenue & growth", "Operating margin", "Net debt / EBITDA (often 4-6x)"],
    ["Cord-cutting reducing retrans fee base", "Political ad spend fragmentation (digital migration)", "FCC regulatory changes", "Advertising migration to streaming", "Refinancing risk on high leverage"],
    ["Political ad revenue cadence (presidential year vs midterm)", "Retransmission consent renewal outcomes", "Local advertising trends"],
    "EV/EBITDA 5-8x; P/E volatile (election-cycle distortion). Highly cyclical.")


# ── Gaming / Interactive Entertainment ────────────────────────────
_add_industry("Electronic Gaming & Multimedia", "Communication Services",
    "Video game publishers and developers (Electronic Arts, Take-Two, Activision Blizzard pre-merger, Roblox, Unity, Nintendo). Mix of franchise publishers (annualized series like FIFA, GTA) and platform/UGC (Roblox, Unity). Live-services and microtransactions have shifted the model from packaged unit sales to recurring engagement.",
    ["Bookings vs revenue (deferred recognition)", "Live-services / recurring revenue mix (target >70%)", "DAU & monthly engagement", "ARPU / ARPDAU (avg revenue per daily user)", "Operating margin", "Hit-driven content release calendar"],
    ["Hit-driven failure (single major release miss)", "Mobile platform fee changes (Apple/Google 30%)", "Live-services churn / fatigue", "Talent retention & studio M&A integration", "Console refresh cycles"],
    ["Bookings cadence vs guidance", "Live-services engagement & monetization", "Franchise refresh (GTA VI, etc.) timing", "Mobile platform fee regulation"],
    "EV/EBITDA 12-20x for steady franchise publishers; 25x+ for live-services growth (RBLX); P/E 18-30x.")


# ── Gaming - Mobile/UGC ───────────────────────────────────────────
_add_industry("Electronic Gaming & Multimedia - UGC", "Communication Services",
    "User-generated-content gaming and mobile platforms (Roblox, Unity, Take-Two/Zynga). Platform economics with creator-revenue-share model. DAU and bookings are the dual KPIs. Heavy SBC dilution common.",
    ["DAU growth", "Bookings growth (>15%)", "ARPDAU (engagement monetization)", "Operating margin (path to profitability)", "SBC / Revenue (often 25-35%)", "FCF margin"],
    ["DAU growth deceleration in mature regions", "Creator payout economics squeezing margins", "Platform fee regulation", "Heavy SBC dilution", "Content moderation / child safety"],
    ["DAU growth by region", "Bookings growth & ARPDAU trend", "SBC / revenue trajectory", "Margin path to GAAP profitability"],
    "EV/Sales 5-10x at 15%+ bookings growth; EV/EBITDA elusive due to SBC. Premium for engagement leadership.")


def get_sector_insight(sector: str | None) -> SectorInsight | None:
    return _SECTORS.get(sector.lower()) if sector else None

def get_industry_insight(industry: str | None) -> IndustryInsight | None:
    return _INDUSTRIES.get(industry.lower()) if industry else None

def list_sectors() -> list[str]:
    return sorted(s.sector for s in _SECTORS.values())

def list_industries() -> list[str]:
    return sorted(i.industry for i in _INDUSTRIES.values())
