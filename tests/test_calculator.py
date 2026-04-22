"""Unit tests for the metrics calculator."""

import pytest
from lynx_comm.models import (
    CompanyStage, CompanyTier, FinancialStatement,
    GrowthMetrics, ProfitabilityMetrics, ShareStructure, SolvencyMetrics,
)
from lynx_comm.metrics.calculator import (
    calc_valuation, calc_profitability, calc_solvency, calc_growth,
    calc_efficiency, calc_share_structure, calc_comm_quality,
    calc_intrinsic_value,
)


@pytest.fixture
def sample_info():
    return {
        "currentPrice": 5.0, "marketCap": 500_000_000,
        "sharesOutstanding": 100_000_000, "totalCash": 200_000_000,
        "totalDebt": 10_000_000, "priceToBook": 2.0,
        "trailingPE": 15.0, "enterpriseValue": 310_000_000,
        "enterpriseToEbitda": 8.0, "returnOnEquity": 0.12,
        "grossMargins": 0.45, "profitMargins": 0.10,
        "currentRatio": 3.0, "debtToEquity": 20.0,
        "heldPercentInsiders": 0.15,
        "heldPercentInstitutions": 0.40,
        "floatShares": 85_000_000,
    }


@pytest.fixture
def sample_statements():
    return [
        FinancialStatement(period="2025", revenue=50_000_000, net_income=5_000_000,
                           total_assets=300_000_000, total_equity=200_000_000,
                           total_cash=200_000_000, total_liabilities=100_000_000,
                           current_assets=250_000_000, current_liabilities=50_000_000,
                           operating_cash_flow=-20_000_000, free_cash_flow=-25_000_000,
                           shares_outstanding=100_000_000, eps=0.05,
                           book_value_per_share=2.0, operating_income=8_000_000),
        FinancialStatement(period="2024", revenue=40_000_000, net_income=3_000_000,
                           total_assets=280_000_000, total_equity=190_000_000,
                           total_cash=180_000_000, operating_cash_flow=-15_000_000,
                           shares_outstanding=95_000_000),
    ]


class TestCalcValuation:
    def test_basic_valuation(self, sample_info, sample_statements):
        v = calc_valuation(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert v.pe_trailing == 15.0
        assert v.pb_ratio == 2.0
        assert v.market_cap == 500_000_000

    def test_cash_to_market_cap(self, sample_info, sample_statements):
        v = calc_valuation(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert v.cash_to_market_cap == pytest.approx(0.4, abs=0.01)

    def test_empty_info(self):
        v = calc_valuation({}, [], CompanyTier.NANO, CompanyStage.STARTUP)
        assert v.pe_trailing is None
        assert v.cash_to_market_cap is None


class TestCalcSolvency:
    def test_cash_burn_detected(self, sample_info, sample_statements):
        s = calc_solvency(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert s.cash_burn_rate is not None
        assert s.cash_burn_rate < 0

    def test_cash_runway_calculated(self, sample_info, sample_statements):
        s = calc_solvency(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert s.cash_runway_years is not None
        assert s.cash_runway_years > 0

    def test_ncav_calculated(self, sample_info, sample_statements):
        s = calc_solvency(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert s.ncav is not None
        # NCAV = current_assets - total_liabilities = 250M - 100M = 150M
        assert s.ncav == 150_000_000

    def test_burn_pct_of_market_cap(self, sample_info, sample_statements):
        s = calc_solvency(sample_info, sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert s.burn_as_pct_of_market_cap is not None
        assert s.burn_as_pct_of_market_cap > 0


class TestCalcGrowth:
    def test_revenue_growth(self, sample_statements):
        g = calc_growth(sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert g.revenue_growth_yoy is not None
        assert g.revenue_growth_yoy == pytest.approx(0.25, abs=0.01)

    def test_share_dilution(self, sample_statements):
        g = calc_growth(sample_statements, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert g.shares_growth_yoy is not None
        assert g.shares_growth_yoy > 0  # 100M vs 95M = dilution

    def test_empty_statements(self):
        g = calc_growth([], CompanyTier.NANO, CompanyStage.STARTUP)
        assert g.revenue_growth_yoy is None

    def test_single_statement(self):
        g = calc_growth([FinancialStatement(period="2025")], CompanyTier.NANO, CompanyStage.STARTUP)
        assert g.revenue_growth_yoy is None


class TestCalcShareStructure:
    def test_share_assessment(self, sample_info, sample_statements):
        g = GrowthMetrics()
        ss = calc_share_structure(sample_info, sample_statements, g, CompanyTier.MICRO, CompanyStage.GROWTH)
        assert ss.shares_outstanding == 100_000_000
        assert ss.insider_ownership_pct == 0.15
        assert ss.share_structure_assessment is not None
        # With 100M shares, comm-services-tier threshold classifies as "Standard"
        assert "Standard" in ss.share_structure_assessment or "Tight" in ss.share_structure_assessment

    def test_hyper_diluted_structure(self):
        info = {"sharesOutstanding": 12_000_000_000, "impliedSharesOutstanding": 12_500_000_000}
        ss = calc_share_structure(info, [], GrowthMetrics(), CompanyTier.MEGA, CompanyStage.MATURE)
        assert "Hyper-Diluted" in ss.share_structure_assessment or "Mega Float" in ss.share_structure_assessment


class TestCalcCommQuality:
    def test_quality_score_range(self, sample_info, sample_statements):
        g = GrowthMetrics(shares_growth_yoy=0.02, rd_intensity=0.15, revenue_growth_yoy=0.25)
        s = SolvencyMetrics(cash_runway_years=5.0, cash_burn_rate=-10_000_000, ncav=100_000_000,
                            tangible_book_value=200_000_000)
        ss = ShareStructure(insider_ownership_pct=0.15, share_structure_assessment="Standard (100-500M shares)")
        p = ProfitabilityMetrics(gross_margin=0.75, rule_of_40=55.0, magic_number=1.1)
        m = calc_comm_quality(p, g, s, ss, sample_statements, sample_info,
                              CompanyTier.MID, CompanyStage.GROWTH)
        assert 0 <= m.quality_score <= 100
        assert m.competitive_position is not None
        assert m.moat_assessment is not None
        assert m.rule_of_40_assessment is not None

    def test_empty_inputs(self):
        m = calc_comm_quality(ProfitabilityMetrics(), GrowthMetrics(), SolvencyMetrics(),
                              ShareStructure(), [], {}, CompanyTier.NANO, CompanyStage.STARTUP)
        assert m.quality_score is not None


class TestCommServicesSpecificMetrics:
    """Coverage for comm-services-specific calculations: leverage, FCF yield,
    capex-adjusted EBITDA, content amortization intensity."""

    def test_net_debt_to_ebitda_carrier(self):
        info = {"marketCap": 100_000_000_000, "enterpriseValue": 250_000_000_000}
        stmts = [FinancialStatement(period="2025", revenue=120_000_000_000,
                                    ebitda=40_000_000_000, total_debt=150_000_000_000,
                                    total_cash=10_000_000_000, capital_expenditure=-22_000_000_000,
                                    free_cash_flow=10_000_000_000)]
        s = calc_solvency(info, stmts, CompanyTier.MEGA, CompanyStage.MATURE)
        # Net debt 140B / EBITDA 40B = 3.5x — typical mature carrier leverage
        assert s.net_debt_to_ebitda == pytest.approx(3.5, abs=0.05)
        # Capex 22B / Revenue 120B = ~18% — heavy network capex
        assert s.capex_to_revenue == pytest.approx(0.183, abs=0.01)

    def test_fcf_yield_internet_platform(self):
        info = {"marketCap": 1_500_000_000_000, "enterpriseValue": 1_400_000_000_000}
        stmts = [FinancialStatement(period="2025", revenue=300_000_000_000,
                                    ebitda=110_000_000_000, capital_expenditure=-50_000_000_000,
                                    free_cash_flow=70_000_000_000, gross_profit=170_000_000_000)]
        v = calc_valuation(info, stmts, CompanyTier.MEGA, CompanyStage.PLATFORM)
        # FCF yield = 70B / 1.5T = ~4.7%
        assert v.fcf_yield == pytest.approx(0.047, abs=0.005)
        # EV/(EBITDA-Capex) = 1.4T / (110B-50B) = 23.3x
        assert v.ev_to_ebitda_capex_adj == pytest.approx(23.3, abs=0.5)

    def test_content_amort_intensity_streaming(self):
        info = {"marketCap": 250_000_000_000}
        stmts = [FinancialStatement(period="2025", revenue=35_000_000_000,
                                    operating_income=8_000_000_000,
                                    content_amortization=15_000_000_000)]
        from lynx_comm.metrics.calculator import calc_profitability as _calc_prof
        p = _calc_prof(info, stmts, CompanyTier.MEGA, CompanyStage.MATURE)
        # Content amort 15B / revenue 35B = ~43%
        assert p.content_amort_intensity == pytest.approx(0.428, abs=0.01)
        # Operating margin ex-content = (8B + 15B) / 35B = ~66%
        assert p.operating_margin_ex_content == pytest.approx(0.657, abs=0.01)
        # Content ROI = revenue / amort = 35B/15B = 2.33x
        assert p.content_roi == pytest.approx(2.33, abs=0.05)


class TestCalcIntrinsicValue:
    def test_method_selection_mature(self, sample_info, sample_statements):
        iv = calc_intrinsic_value(sample_info, sample_statements, GrowthMetrics(),
                                  SolvencyMetrics(), CompanyTier.MID, CompanyStage.MATURE)
        assert "DCF" in (iv.primary_method or "") or "FCF" in (iv.primary_method or "")

    def test_method_selection_growth(self, sample_info, sample_statements):
        iv = calc_intrinsic_value(sample_info, sample_statements, GrowthMetrics(),
                                  SolvencyMetrics(), CompanyTier.MICRO, CompanyStage.GROWTH)
        assert "EV" in (iv.primary_method or "")

    def test_method_selection_startup(self, sample_info, sample_statements):
        iv = calc_intrinsic_value(sample_info, sample_statements, GrowthMetrics(),
                                  SolvencyMetrics(), CompanyTier.NANO, CompanyStage.STARTUP)
        assert "Cash" in (iv.primary_method or "")
