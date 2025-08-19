import sys
import os

# root directory to sys.path to allow relative imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
sys.path.insert(0, project_root)

from app.config.config import Config
from app.models.user import Base
from sqlalchemy import create_engine

def init_db():
    """Creates the tables in the database."""
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)
    print("✅ Database initialized.")

def reset_db(auto_confirm=False):
    """Drops all tables and recreates them."""
    engine = create_engine(Config.SQLALCHEMY_DATABASE_URL, echo=True)
    print("⚠️  This will delete all existing tables and data.")
    if auto_confirm:
        confirm = "yes"
    else:
        confirm = input("Are you sure? (yes/no): ")
    if confirm.lower() in ['yes', 'y', 'sí', 'si']:
        Base.metadata.drop_all(bind=engine)
        print("✅ Tables dropped.")
        Base.metadata.create_all(bind=engine)
        print("✅ Database reinitialized.")
    else:
        print("❌ Operation cancelled.")

def print_help():
    print("Usage: python init_db.py [FLAG]")
    print("Available flags:")
    print("  --help     Show this help")
    print("  --reset    Drop all tables and recreate them (requires confirmation)")
    print("  --fresh    Same as --reset but without confirmation")
    print("If no flag is provided, it will only create the tables if they do not exist.")

if __name__ == "__main__":
    valid_flags = ["--reset", "--fresh", "--help"]
    if len(sys.argv) > 1:
        flag = sys.argv[1]
        if flag == "--reset":
            reset_db()
        elif flag == "--fresh":
            reset_db(auto_confirm=True)
        elif flag == "--help":
            print_help()
        else:
            print(f"❌ Invalid flag: {flag}")
            print_help()
            print("No action was performed.")
    else:
        init_db()
