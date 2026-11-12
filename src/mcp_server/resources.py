from pathlib import Path

from pypdf import PdfReader

from logs import logger
from src.mcp_server.app import mcp

BASE_DIR = Path(__file__).resolve().parents[1]

POLICY_FILE = BASE_DIR / "data" / "fictional_employee_policies.pdf"


@mcp.resource("hr://policies/employee-handbook")
def get_employee_handbook() -> str:
    """
    Provides the complete Northstar Works employee policy handbook.
    Includes annual leave, sick leave, working hours,
    remote work, and probation policies.
    """

    if not POLICY_FILE.exists():
        logger.error("Employee policy handbook not found: %s", POLICY_FILE)
        raise FileNotFoundError("Employee policy handbook PDF not found.")

    reader = PdfReader(str(POLICY_FILE))

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""

        pages.append(f"Page {page_number}\n{page_text}")

    handbook_text = "\n\n".join(pages)

    logger.info("Employee handbook resource loaded successfully")

    return handbook_text
