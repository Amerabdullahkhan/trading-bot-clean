from app.dashboard import ConsoleDashboard
from app.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    dashboard = ConsoleDashboard(settings.default_symbols)
    dashboard.render()