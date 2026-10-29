import os
import sys
from datetime import datetime

# Kích hoạt ANSI escape sequence và UTF-8 trên Windows
if sys.platform == "win32":
    os.system("")
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

class Colors:
    CYAN = "\033[96m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"

class AppLogger:
    def __init__(self, name: str = "KidSpeak"):
        self.name = name

    def _timestamp(self) -> str:
        return datetime.now().strftime("%H:%M:%S")

    def show_banner(self, app_name: str = "KidSpeak-Backend", version: str = "1.0.0", env: str = "development"):
        banner = rf"""{Colors.CYAN}{Colors.BOLD}
  _  ___     _ ____                    _    
 | |/ (_) __| / ___| _ __   ___   __ _| | __
 | ' /| |/ _` \___ \| '_ \ / _ \ / _` | |/ /
 | . \| | (_| |___) | |_) |  __/ (_| | | <  
 |_|\_\_|\__,_|____/| .__/ \___|\__,_|_|\_\ 
                    |_|                     {Colors.RESET}
{Colors.BLUE}{Colors.BOLD}🎙️  KidSpeak - AI-powered Vietnamese Pronunciation Platform{Colors.RESET}
{Colors.DIM}----------------------------------------------------------------------{Colors.RESET}
  {Colors.BOLD}Application:{Colors.RESET} {app_name}  |  {Colors.BOLD}Version:{Colors.RESET} {version}  |  {Colors.BOLD}Env:{Colors.RESET} {env}
{Colors.DIM}----------------------------------------------------------------------{Colors.RESET}"""
        print(banner)

    def info(self, msg: str):
        print(f"{Colors.DIM}[{self._timestamp()}]{Colors.RESET} {Colors.BLUE}ℹ️  INFO:{Colors.RESET} {msg}")

    def success(self, msg: str):
        print(f"{Colors.DIM}[{self._timestamp()}]{Colors.RESET} {Colors.GREEN}✅ SUCCESS:{Colors.RESET} {msg}")

    def warning(self, msg: str):
        print(f"{Colors.DIM}[{self._timestamp()}]{Colors.RESET} {Colors.YELLOW}⚠️  WARNING:{Colors.RESET} {msg}")

    def error(self, msg: str):
        print(f"{Colors.DIM}[{self._timestamp()}]{Colors.RESET} {Colors.RED}❌ ERROR:{Colors.RESET} {msg}")

    def minio_connected(self, details: str):
        print(f"{Colors.DIM}[{self._timestamp()}]{Colors.RESET} {Colors.GREEN}🪣 MinIO:{Colors.RESET} {details} (Connected)")

    def minio_error(self, err: str):
        print(f"{Colors.DIM}[{self._timestamp()}]{Colors.RESET} {Colors.RED}🪣 MinIO ERROR:{Colors.RESET} {err}")

    def db_connected(self, details: str = "PostgreSQL"):
        print(f"{Colors.DIM}[{self._timestamp()}]{Colors.RESET} {Colors.GREEN}🔌 DATABASE:{Colors.RESET} {details} connected successfully!")

    def db_error(self, err: str):
        print(f"{Colors.DIM}[{self._timestamp()}]{Colors.RESET} {Colors.RED}🔌 DATABASE ERROR:{Colors.RESET} {err}")

logger = AppLogger()
