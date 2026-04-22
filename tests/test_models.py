"""Unit tests for data models and classification functions (Communication Services)."""

import pytest
from lynx_comm.models import (
    CompanyProfile, CompanyStage, CompanyTier, CommCategory,
    JurisdictionTier, Relevance, Severity, AnalysisReport,
    ValuationMetrics, SolvencyMetrics, GrowthMetrics,
    CommQualityIndicators, ShareStructure, MarketIntelligence,
    FinancialStatement, AnalysisConclusion,
    classify_tier, classify_stage, classify_category, classify_jurisdiction,
    format_severity, format_impact, SEVERITY_STYLE, IMPACT_STYLE,
)


class TestClassifyTier:
    def test_mega_cap(self):
        assert classify_tier(300_000_000_000) == CompanyTier.MEGA

    def test_large_cap(self):
        assert classify_tier(50_000_000_000) == CompanyTier.LARGE

    def test_mid_cap(self):
        assert classify_tier(5_000_000_000) == CompanyTier.MID

    def test_small_cap(self):
        assert classify_tier(1_000_000_000) == CompanyTier.SMALL

    def test_micro_cap(self):
        assert classify_tier(100_000_000) == CompanyTier.MICRO

    def test_nano_cap(self):
        assert classify_tier(10_000_000) == CompanyTier.NANO

    def test_none_returns_nano(self):
        assert classify_tier(None) == CompanyTier.NANO

    def test_zero_returns_nano(self):
        assert classify_tier(0) == CompanyTier.NANO

    def test_negative_returns_nano(self):
        assert classify_tier(-100) == CompanyTier.NANO


class TestClassifyStage:
    def test_platform_from_description(self):
        assert classify_stage("dominant platform leading social network", 50_000_000_000,
                              {"marketCap": 300_000_000_000}) == CompanyStage.PLATFORM

    def test_mature_by_profit_margin(self):
        assert classify_stage("mature established carrier", 10_000_000_000,
                              {"marketCap": 50_000_000_000, "profitMargins": 0.25}) == CompanyStage.MATURE

    def test_growth_hyper(self):
        assert classify_stage("rapid subscriber growth streaming service", 100_000_000,
                              {"revenueGrowth": 0.40}) == CompanyStage.GROWTH

    def test_scale_by_revenue(self):
        assert classify_stage("national 5G rollout wireless carrier", 800_000_000,
                              {"revenueGrowth": 0.15}) == CompanyStage.SCALE

    def test_startup_low_revenue(self):
        assert classify_stage("pre-revenue social platform", 0) == CompanyStage.STARTUP

    def test_none_description(self):
        assert classify_stage(None, None) == CompanyStage.STARTUP

    def test_empty_description(self):
        assert classify_stage("", 0) == CompanyStage.STARTUP


class TestClassifyCategory:
    def test_telecom_wireless(self):
        assert classify_category("major US wireless carrier operating a 5G network",
                                 "Telecom Services") == CommCategory.TELECOM_WIRELESS

    def test_telecom_wireline(self):
        assert classify_category("fiber-to-the-home broadband internet provider",
                                 "Telecom Services") == CommCategory.TELECOM_WIRELINE

    def test_cable_satellite(self):
        assert classify_category("major cable operator with cable television service",
                                 "Telecom Services") == CommCategory.CABLE_SATELLITE

    def test_streaming(self):
        assert classify_category("subscription video on demand streaming service",
                                 "Entertainment") == CommCategory.STREAMING

    def test_entertainment(self):
        assert classify_category("film studio with movie production and theatrical releases",
                                 "Entertainment") == CommCategory.ENTERTAINMENT

    def test_internet_content(self):
        assert classify_category("search engine and internet content platform",
                                 "Internet Content & Information") == CommCategory.INTERNET_CONTENT

    def test_social_media(self):
        assert classify_category("global social network and messaging platform",
                                 "Interactive Media & Services") == CommCategory.SOCIAL_MEDIA

    def test_digital_advertising(self):
        assert classify_category("programmatic advertising ad exchange demand-side platform",
                                 "Advertising") == CommCategory.DIGITAL_ADVERTISING

    def test_ad_agency(self):
        assert classify_category("global advertising agency holding company",
                                 "Advertising Agencies") == CommCategory.AD_AGENCY

    def test_publishing(self):
        assert classify_category("digital publishing newspaper journalism",
                                 "Publishing") == CommCategory.PUBLISHING

    def test_broadcasting(self):
        assert classify_category("local broadcast television tv station operator",
                                 "Broadcasting") == CommCategory.BROADCASTING

    def test_gaming(self):
        assert classify_category("video game publisher of mobile gaming franchises",
                                 "Electronic Gaming & Multimedia") == CommCategory.GAMING

    def test_other_when_no_match(self):
        assert classify_category("generic company", None) == CommCategory.OTHER

    def test_none_inputs(self):
        assert classify_category(None, None) == CommCategory.OTHER


class TestClassifyJurisdiction:
    def test_us_tier1(self):
        assert classify_jurisdiction("United States") == JurisdictionTier.TIER_1

    def test_ireland_tier1(self):
        assert classify_jurisdiction("Ireland") == JurisdictionTier.TIER_1

    def test_israel_tier1(self):
        assert classify_jurisdiction("Israel") == JurisdictionTier.TIER_1

    def test_taiwan_tier1(self):
        assert classify_jurisdiction("Taiwan") == JurisdictionTier.TIER_1

    def test_india_tier2(self):
        assert classify_jurisdiction("India") == JurisdictionTier.TIER_2

    def test_spain_tier2(self):
        assert classify_jurisdiction("Spain") == JurisdictionTier.TIER_2

    def test_unknown_country_tier3(self):
        assert classify_jurisdiction("SomeCountry") == JurisdictionTier.TIER_3

    def test_none_unknown(self):
        assert classify_jurisdiction(None) == JurisdictionTier.UNKNOWN


class TestDataModels:
    def test_analysis_report_defaults(self):
        r = AnalysisReport(profile=CompanyProfile(ticker="TEST", name="Test"))
        assert r.valuation is None
        assert r.market_intelligence is None
        assert r.financials == []
        assert r.fetched_at != ""

    def test_company_profile_defaults(self):
        p = CompanyProfile(ticker="X", name="X Corp")
        assert p.tier == CompanyTier.NANO
        assert p.stage == CompanyStage.STARTUP
        assert p.comm_category == CommCategory.OTHER
        assert p.jurisdiction_tier == JurisdictionTier.UNKNOWN

    def test_solvency_metrics_defaults(self):
        s = SolvencyMetrics()
        assert s.cash_runway_years is None
        assert s.burn_as_pct_of_market_cap is None
        assert s.goodwill_to_assets is None
        assert s.deferred_revenue_ratio is None

    def test_market_intelligence_defaults(self):
        mi = MarketIntelligence()
        assert mi.insider_transactions == []
        assert mi.risk_warnings == []
        assert mi.disclaimers == []

    def test_comm_quality_defaults(self):
        tq = CommQualityIndicators()
        assert tq.quality_score is None
        assert tq.moat_assessment is None
        assert tq.rule_of_40_assessment is None


class TestSeverityFormatting:
    def test_critical_severity_format(self):
        s = format_severity(Severity.CRITICAL)
        assert "***CRITICAL***" in s
        assert "bold red" in s

    def test_warning_severity_format(self):
        s = format_severity(Severity.WARNING)
        assert "*WARNING*" in s
        assert "#ff8800" in s

    def test_watch_severity_format(self):
        s = format_severity(Severity.WATCH)
        assert "[WATCH]" in s
        assert "yellow" in s

    def test_ok_severity_format(self):
        s = format_severity(Severity.OK)
        assert "[OK]" in s
        assert "green" in s

    def test_strong_severity_format(self):
        s = format_severity(Severity.STRONG)
        assert "[STRONG]" in s
        assert "grey" in s or "silver" in s.lower()


class TestImpactFormatting:
    def test_critical_impact_blinks(self):
        s = format_impact(Relevance.CRITICAL)
        assert "Critical" in s
        assert "blink" in s

    def test_important_impact_orange(self):
        s = format_impact(Relevance.IMPORTANT)
        assert "Important" in s
        assert "#ff8800" in s

    def test_relevant_impact_yellow(self):
        s = format_impact(Relevance.RELEVANT)
        assert "Relevant" in s
        assert "yellow" in s

    def test_contextual_impact_green(self):
        s = format_impact(Relevance.CONTEXTUAL)
        assert "Informational" in s
        assert "green" in s

    def test_irrelevant_impact_silver(self):
        s = format_impact(Relevance.IRRELEVANT)
        assert "Irrelevant" in s
        assert "grey" in s or "silver" in s.lower()
