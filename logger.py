class Logger:
    @staticmethod
    def info(message):
        print(f"INFO: {message}")

    @staticmethod
    def debug(message):
        print(f"DEBUG: {message}")

    @staticmethod
    def error(message):
        print(f"ERROR: {message}")
