"""Entry-point registration for the Lince Investor Suite plugin system.

Exposed via ``pyproject.toml`` under the ``lynx_investor_suite.agents``
entry-point group. See :mod:`lynx_investor_core.plugins` for the
discovery contract.

The lynx_comm package does not (yet) expose APP_TAGLINE / PROG_NAME
at module level, so the plugin encodes them here directly.
"""

from __future__ import annotations

from lynx_investor_core.plugins import SectorAgent

from lynx_comm import __version__


def register() -> SectorAgent:
    """Return this agent's descriptor for the plugin registry."""
    return SectorAgent(
        name="lynx-investor-communication-services",
        short_name="comm",
        sector="Communication Services",
        tagline="Telecom, Media, Internet, Gaming & Publishing",
        prog_name="lynx-comm",
        version=__version__,
        package_module="lynx_comm",
        entry_point_module="lynx_comm.__main__",
        entry_point_function="main",
        icon="\U0001f4e1",  # satellite antenna
    )
