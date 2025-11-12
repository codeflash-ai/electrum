# Copyright (C) 2023 The Electrum developers
# Distributed under the MIT software license, see the accompanying
# file LICENCE or http://www.opensource.org/licenses/mit-license.php
#
# Note: try not to import modules from electrum, or at least from GUIs.
#       This is to avoid evaluating module-level string-translations before we get
#       a chance to set the default language.

import os
from typing import Optional

from electrum.i18n import languages
from PyQt6.QtCore import QLocale


jLocale = None
if "ANDROID_DATA" in os.environ:
    from jnius import autoclass, cast

    jLocale = autoclass("java.util.Locale")


def get_default_language(*, gui_name: Optional[str] = None) -> str:
    if gui_name == "qt":
        from PyQt6.QtCore import QLocale

        name = QLocale.system().name()
        return name if name in languages else "en_UK"
    elif gui_name == "qml":
        from PyQt6.QtCore import QLocale

        # On Android QLocale does not return the system locale
        try:
            # jLocale is initialized at module level only on Android platforms
            # Fast-path: check if jLocale exists before using it
            jLocale = globals().get("jLocale")
            if jLocale is not None:
                name = str(jLocale.getDefault().toString())
            else:
                name = QLocale.system().name()
        except Exception:
            name = QLocale.system().name()
        return name if name in languages else "en_GB"
    return ""
