#Credits to Mistium for the logger which is from OriginChats.

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    GRAY = '\033[90m'

class Logger:
    @staticmethod
    def add(message: str):
        """Log an addition/creation action"""
        print(f"{Colors.GREEN}[+]{Colors.RESET} {message}")
    
    @staticmethod
    def get(message: str):
        """Log a retrieval/query action"""
        print(f"{Colors.BLUE}[?]{Colors.RESET} {message}")
    
    @staticmethod
    def info(message: str):
        """Log general information"""
        print(f"{Colors.CYAN}[i]{Colors.RESET} {message}")
    
    @staticmethod
    def warning(message: str):
        """Log warnings"""
        print(f"{Colors.YELLOW}[!]{Colors.RESET} {message}")
    
    @staticmethod
    def error(message: str):
        """Log errors"""
        print(f"{Colors.RED}[ERROR]{Colors.RESET} {message}")
    
    @staticmethod
    def success(message: str):
        """Log success messages"""
        print(f"{Colors.GREEN}[✓]{Colors.RESET} {message}")

    @staticmethod
    def like(message: str):
        """Log like action"""
        print(f"{Colors.BLUE}[♥]{Colors.RESET} {message}")

    @staticmethod
    def cont(message: str):
        """Log continue action"""
        print(f"{message}")
