try:
    from tubemonitor.settings.local_settings import *
except ImportError:
    from .settings import *