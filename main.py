from dotenv import load_dotenv
from engine.engine import Engine
from utilities.logger import Logger

load_dotenv()

def main():
    Logger.log("Application starting", component="MAIN")
    try:
        engine = Engine()
        Logger.log("Engine initialized", component="MAIN")
        engine.run()
        Logger.log("Application finished successfully", component="MAIN")
    except Exception as e:
        Logger.error(f"Fatal error in main: {e}", component="MAIN")
        raise

if __name__ == "__main__":
    main()
