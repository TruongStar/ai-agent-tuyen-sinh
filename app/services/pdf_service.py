from pathlib import Path
from app.core.settings import settings

class PDFService:
    @staticmethod
    def save_uploaded_files(uploaded_files):
        Path(settings.pdf_dir).mkdir(parents=True, exist_ok=True)
        saved = []
        for file in uploaded_files:
            safe_name = Path(file.name).name
            target = Path(settings.pdf_dir) / safe_name
            target.write_bytes(file.getbuffer())
            saved.append(str(target))
        return saved

    @staticmethod
    def list_pdfs():
        Path(settings.pdf_dir).mkdir(parents=True, exist_ok=True)
        return sorted(Path(settings.pdf_dir).glob("*.pdf"))

    @staticmethod
    def delete_pdf(filename: str):
        target = Path(settings.pdf_dir) / Path(filename).name
        if target.exists():
            target.unlink()
            return True
        return False
