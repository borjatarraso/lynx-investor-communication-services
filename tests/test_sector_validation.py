"""Tests for the sector validation gate (Communication Services)."""

import pytest
from lynx_comm.core.analyzer import _validate_sector, SectorMismatchError
from lynx_comm.models import CompanyProfile


class TestSectorValidation:
    """Sector validation blocks non-Communication-Services companies."""

    def _profile(self, ticker="T", sector=None, industry=None, desc=None):
        return CompanyProfile(ticker=ticker, name=f"{ticker} Corp",
                              sector=sector, industry=industry, description=desc)

    # --- Should ALLOW ---
    def test_communication_services_telecom(self):
        _validate_sector(self._profile(sector="Communication Services", industry="Telecom Services"))

    def test_communication_services_wireless(self):
        _validate_sector(self._profile(sector="Communication Services",
                                       industry="Wireless Communications"))

    def test_communication_services_cable(self):
        _validate_sector(self._profile(sector="Communication Services",
                                       industry="Telecom Services - Cable"))

    def test_communication_services_internet(self):
        _validate_sector(self._profile(sector="Communication Services",
                                       industry="Internet Content & Information"))

    def test_communication_services_entertainment(self):
        _validate_sector(self._profile(sector="Communication Services", industry="Entertainment"))

    def test_communication_services_advertising(self):
        _validate_sector(self._profile(sector="Communication Services",
                                       industry="Advertising Agencies"))

    def test_communication_services_publishing(self):
        _validate_sector(self._profile(sector="Communication Services", industry="Publishing"))

    def test_communication_services_broadcasting(self):
        _validate_sector(self._profile(sector="Communication Services", industry="Broadcasting"))

    def test_communication_services_gaming(self):
        _validate_sector(self._profile(sector="Communication Services",
                                       industry="Electronic Gaming & Multimedia"))

    def test_communication_services_interactive_media(self):
        _validate_sector(self._profile(sector="Communication Services",
                                       industry="Interactive Media & Services"))

    def test_streaming_keyword_in_description(self):
        _validate_sector(self._profile(sector="Other", industry="Other",
                                       desc="Operates a subscription video on demand streaming service"))

    def test_wireless_carrier_keyword_in_description(self):
        _validate_sector(self._profile(sector="Other", industry="Other",
                                       desc="Major US wireless carrier operating a 5G network"))

    def test_internet_platform_keyword_in_description(self):
        _validate_sector(self._profile(sector="Other", industry="Other",
                                       desc="Internet content & search platform with advertising revenue"))

    def test_gaming_publisher_keyword_in_description(self):
        _validate_sector(self._profile(sector="Other", industry="Other",
                                       desc="Video game publisher of mobile gaming franchises"))

    # --- Should BLOCK ---
    def test_information_technology_blocked(self):
        """IT companies are routed to the Information Technology specialist."""
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Technology",
                                           industry="Software - Application"))

    def test_basic_materials_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Basic Materials", industry="Gold"))

    def test_energy_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Energy", industry="Uranium"))

    def test_financial_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Financial Services", industry="Banks"))

    def test_healthcare_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Healthcare", industry="Drug Manufacturers"))

    def test_consumer_cyclical_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Consumer Cyclical", industry="Auto Manufacturers"))

    def test_real_estate_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Real Estate", industry="REIT"))

    def test_industrials_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Industrials", industry="Aerospace & Defense"))

    def test_utilities_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="Utilities", industry="Utilities - Regulated Electric"))

    def test_all_none_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile())

    def test_empty_strings_blocked(self):
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(sector="", industry="", desc=""))

    def test_mining_company_blocked(self):
        """A mining company with sector 'Basic Materials' should be blocked."""
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(
                sector="Basic Materials", industry="Gold",
                desc="Gold mining exploration and drill program"))

    def test_software_keyword_alone_blocked(self):
        """Pure software descriptions should NOT match (route to IT specialist)."""
        with pytest.raises(SectorMismatchError):
            _validate_sector(self._profile(
                sector="Technology", industry="Software - Application",
                desc="Subscription software platform for enterprise CRM"))

    def test_error_message_content(self):
        with pytest.raises(SectorMismatchError, match="outside the scope"):
            _validate_sector(self._profile(sector="Basic Materials", industry="Gold"))

    def test_error_suggests_another_agent(self):
        """Wrong-sector warning appends a 'use lynx-investor-*' line."""
        with pytest.raises(SectorMismatchError) as exc:
            _validate_sector(self._profile(
                sector="Healthcare", industry="Biotechnology"))
        message = str(exc.value)
        assert "Suggestion" in message
        assert "lynx-investor-healthcare" in message

    def test_error_never_suggests_self(self):
        with pytest.raises(SectorMismatchError) as exc:
            _validate_sector(self._profile(
                sector="Utilities", industry="Utilities—Regulated Electric"))
        message = str(exc.value)
        assert "use 'lynx-investor-communication-services'" not in message
