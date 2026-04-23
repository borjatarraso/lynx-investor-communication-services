"""Lynx Communication Services — Fundamental analysis for telecom, wireless, cable, streaming, internet, social media, advertising & gaming companies."""

__version__ = "5.3"
__author__ = "Borja Tarraso"
__author_email__ = "borja.tarraso@member.fsf.org"
__year__ = "2026"
__license__ = "BSD-3-Clause"

SUITE_NAME = "Lince Investor Suite"
SUITE_VERSION = "5.3"
SUITE_LABEL = f"{SUITE_NAME} v{SUITE_VERSION}"
APP_NAME = "Lynx Communication Services Analysis"

LICENSE_TEXT = """\
BSD 3-Clause License

Copyright (c) 2026, Borja Tarraso <borja.tarraso@member.fsf.org>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE."""


def _load_logo_ascii() -> str:
    """Load the ASCII logo from img/logo_ascii.txt."""
    from pathlib import Path
    logo_path = Path(__file__).resolve().parent.parent / "img" / "logo_ascii.txt"
    try:
        return logo_path.read_text()
    except FileNotFoundError:
        return ""


def get_about_text() -> dict:
    """Return structured about information."""
    return {
        "name": APP_NAME,
        "suite": SUITE_NAME,
        "suite_version": SUITE_VERSION,
        "suite_label": SUITE_LABEL,
        "version": __version__,
        "author": __author__,
        "email": __author_email__,
        "year": __year__,
        "license": __license__,
        "license_text": LICENSE_TEXT,
        "logo_ascii": _load_logo_ascii(),
        "description": (
            "Fundamental analysis specialized for Communication Services: "
            "wireless & wireline telecom, cable & satellite, streaming & "
            "entertainment, internet content & search, social media, "
            "interactive media, digital advertising, publishing and "
            "electronic gaming companies. Evaluates operators across "
            "lifecycle stages from emerging platform to mature carrier "
            "using comm-services-specific metrics: ARPU, churn, subscriber "
            "net adds, MAU/DAU engagement, content amortization intensity, "
            "network capex/sales, FCF yield, net debt/EBITDA, content ROI, "
            "ad revenue per user, and more.\n\n"
            "Part of the Lince Investor Suite."
        ),
    }
