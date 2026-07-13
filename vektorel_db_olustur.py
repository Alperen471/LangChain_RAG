import os
import shutil
from pathlib import Path

import pypdf
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


BASE_DIR = Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"
DOCUMENTS_DIR = BASE_DIR / "bilgi_bankasi"
DATABASE_DIR = BASE_DIR / "chroma_db"

COLLECTION_NAME = "cagri_merkezi_bilgi_bankasi"


load_dotenv(dotenv_path=ENV_PATH)


def belgeleri_yukle() -> list[Document]:
    """
    bilgi_bankasi klasöründeki PDF, TXT ve MD dosyalarını okur.
    """

    belgeler: list[Document] = []

    if not DOCUMENTS_DIR.exists():
        raise FileNotFoundError(
            f"Bilgi bankası klasörü bulunamadı: {DOCUMENTS_DIR}"
        )

    for dosya_yolu in DOCUMENTS_DIR.rglob("*"):
        if not dosya_yolu.is_file():
            continue

        uzanti = dosya_yolu.suffix.lower()

        try:
            if uzanti == ".pdf":
                pdf_reader = pypdf.PdfReader(str(dosya_yolu))

                for sayfa_no, sayfa in enumerate(
                    pdf_reader.pages,
                    start=1,
                ):
                    metin = sayfa.extract_text() or ""

                    if not metin.strip():
                        continue

                    belgeler.append(
                        Document(
                            page_content=metin,
                            metadata={
                                "source": dosya_yolu.name,
                                "page": sayfa_no,
                                "type": "pdf",
                            },
                        )
                    )

            elif uzanti in {".txt", ".md"}:
                metin = dosya_yolu.read_text(
                    encoding="utf-8"
                )

                if not metin.strip():
                    continue

                belgeler.append(
                    Document(
                        page_content=metin,
                        metadata={
                            "source": dosya_yolu.name,
                            "type": uzanti.removeprefix("."),
                        },
                    )
                )

        except Exception as hata:
            print(f"Dosya okunamadı: {dosya_yolu.name}")
            print(f"Hata: {hata}")

    return belgeler


def vektor_veritabani_olustur() -> None:
    if not os.getenv("GEMINI_API_KEY"):
        raise ValueError(
            "GEMINI_API_KEY .env dosyasında bulunamadı."
        )

    belgeler = belgeleri_yukle()

    if not belgeler:
        raise ValueError(
            "Bilgi bankasında işlenecek belge bulunamadı."
        )

    print(f"Okunan belge/sayfa sayısı: {len(belgeler)}")

    metin_bolucu = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        add_start_index=True,
    )

    parcalar = metin_bolucu.split_documents(belgeler)

    print(f"Oluşturulan metin parçası sayısı: {len(parcalar)}")

    # Bu script tekrar çalıştırıldığında eski indeks silinir.
    if DATABASE_DIR.exists():
        shutil.rmtree(DATABASE_DIR)

    embedding_modeli = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001"
    )

    vektor_db = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embedding_modeli,
        persist_directory=str(DATABASE_DIR),
    )

    eklenen_idler = vektor_db.add_documents(
        documents=parcalar
    )

    print(
        f"{len(eklenen_idler)} parça vektör "
        "veritabanına kaydedildi."
    )
    print(f"Veritabanı konumu: {DATABASE_DIR}")


if __name__ == "__main__":
    vektor_veritabani_olustur()