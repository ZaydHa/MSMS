from gui.main_dashboard import launch
from app.admin_utils import init_logger, backup_data

if __name__ == "__main__":
    init_logger("msms.log")                 # logging first
    backup_data("msms.json", "backups")     # safe copy before the session
    launch()                                # start Streamlit UI
