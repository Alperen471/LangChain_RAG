# LangChain RAG Çağrı Merkezi Asistanı

Bu proje; **LangChain**, **Google Gemini**, **Chroma vektör veritabanı** ve **RAG (Retrieval-Augmented Generation)** kullanılarak geliştirilmiş basit bir çağrı merkezi asistanıdır.

Asistan, müşterinin mesajını analiz eder ve ihtiyaca göre uygun aracı çalıştırır:

- Kargo durumu sorgulama
- Müşteri bakiyesi sorgulama
- Şirket bilgi bankasında anlamsal arama
- İade, teslimat, şirket kuralları ve sık sorulan sorulara belge tabanlı cevap verme

## Çalışma Mantığı

```text
Kullanıcı mesajı
      ↓
Google Gemini LLM
      ↓
LangChain Agent
      ↓
Uygun tool seçimi
      ↓
├── Kargo sorgulama tool'u
├── Bakiye sorgulama tool'u
└── RAG bilgi bankası tool'u
          ↓
     Chroma Vector DB
          ↓
     İlgili belge parçaları
          ↓
        Gemini
          ↓
   Doğal dilde cevap
```

LLM, müşterinin ne istediğini anlar ve hangi aracın kullanılması gerektiğine karar verir.

LangChain Agent:

- Modeli çağırır
- Tool çağrısını yakalar
- İlgili Python fonksiyonunu çalıştırır
- Tool sonucunu modele geri gönderir
- Nihai cevap oluşana kadar süreci yönetir

## Kullanılan Teknolojiler

- Python
- LangChain
- Google Gemini
- Google Generative AI Embeddings
- ChromaDB
- Pydantic
- PyPDF
- python-dotenv

## Proje Yapısı

```text
langchain/
│
├── bilgi_bankasi/
│   ├── iade_politikasi.txt
│   ├── kargo_proseduru.txt
│   ├── sirket_kurallari.md
│   └── sss.md
│
├── cagri_merkezi_ajani.py
├── vektorel_db_olustur.py
├── .env.example
├── .gitignore
└── README.md
```

`chroma_db/`, `.env`, `venv/` ve `__pycache__/` klasörleri GitHub'a gönderilmez.

## Kurulum

Projeyi klonlayın:

```bash
git clone https://github.com/Alperen471/LangChain_RAG.git
cd LangChain_RAG
```

Sanal ortam oluşturun:

```bash
python -m venv venv
```

Windows PowerShell üzerinde sanal ortamı etkinleştirin:

```powershell
venv\Scripts\Activate.ps1
```

Gerekli paketleri yükleyin:

```bash
pip install -U langchain langchain-google-genai langchain-chroma langchain-text-splitters pydantic pypdf python-dotenv
```

## Ortam Değişkenleri

Proje kök dizininde `.env` dosyası oluşturun:

```env
GOOGLE_API_KEY=google_api_anahtariniz
```

Örnek dosya:

```env
GOOGLE_API_KEY=
```

API anahtarınızı hiçbir zaman GitHub'a göndermeyin.

`.gitignore` dosyasında aşağıdaki satırın bulunduğundan emin olun:

```gitignore
.env
```

## Bilgi Bankası

RAG sistemi, `bilgi_bankasi/` klasöründeki belgeleri kullanır.

Desteklenen örnek dosya türleri:

- `.txt`
- `.md`
- `.pdf`

Bilgi bankasına eklenebilecek içerikler:

- İade politikaları
- Kargo ve teslimat prosedürleri
- Şirket kuralları
- Ürün bilgileri
- Sık sorulan sorular
- Müşteri hizmetleri prosedürleri

## Vektör Veritabanını Oluşturma

Belgeleri chunk'lara bölmek, embedding üretmek ve Chroma veritabanına kaydetmek için:

```bash
python vektorel_db_olustur.py
```

Bu işlem:

1. Bilgi bankasındaki belgeleri okur.
2. Metinleri küçük parçalara böler.
3. Her parça için embedding oluşturur.
4. Embedding ve belge bilgilerini ChromaDB'ye kaydeder.

Başarılı işlemden sonra proje dizininde `chroma_db/` klasörü oluşur.

Bilgi bankasındaki belgeleri değiştirdiğinizde veya yeni belge eklediğinizde bu komutu tekrar çalıştırın.

## Uygulamayı Çalıştırma

Vektör veritabanı oluşturulduktan sonra ajanı çalıştırın:

```bash
python cagri_merkezi_ajani.py
```

Örnek sorular:

```text
Ürünü kaç gün içerisinde iade edebilirim?

Hasarlı paket teslim alırsam ne yapmalıyım?

1234 numaralı kargom nerede?

5678 numaralı müşterinin hesap bakiyesi nedir?

Hangi durumlarda insan temsilciye aktarılmam gerekir?
```

## Tool Yapısı

### Kargo Durumu Sorgulama

```python
@tool
def kargo_durumu_sorgula(kargo_no: str) -> str:
    ...
```

Gerçek sistemde bu tool bir kargo API'sine veya şirket veritabanına bağlanabilir.

### Bakiye Sorgulama

```python
@tool
def bakiye_sorgula(musteri_no: str) -> str:
    ...
```

Gerçek sistemde bu tool CRM veya SQL veritabanından güncel müşteri bilgisi getirebilir.

### Bilgi Bankası Araması

```python
@tool
def bilgi_bankasinda_ara(soru: str) -> str:
    ...
```

Bu tool, kullanıcı sorusuna anlamsal olarak en yakın belge parçalarını ChromaDB üzerinden getirir.

## RAG Mantığı

RAG süreci iki ana aşamadan oluşur.

### İndeksleme

```text
Belgeler
   ↓
Chunk'lara bölme
   ↓
Embedding oluşturma
   ↓
ChromaDB'ye kaydetme
```

### Sorgulama

```text
Kullanıcı sorusu
   ↓
Soru embedding'i
   ↓
Benzer chunk'ları bulma
   ↓
İlgili içerikleri LLM'e gönderme
   ↓
Belge tabanlı cevap üretme
```

## Pydantic Kullanımı

Pydantic aşağıdaki amaçlarla kullanılabilir:

- Tool parametrelerini doğrulamak
- Kargo ve müşteri numarası formatlarını kontrol etmek
- RAG sonuçlarını düzenli JSON yapısında döndürmek
- Ajanın nihai cevabını sabit bir şemaya oturtmak
- Backend ve panel entegrasyonunu kolaylaştırmak

Örnek çıktı modeli:

```python
class AjanYaniti(BaseModel):
    cevap: str
    kategori: str
    kaynaklar: list[str]
    insan_temsilci_gerekli: bool
    guven: float
```

## Güvenlik

- `.env` dosyasını GitHub'a göndermeyin.
- API anahtarlarını kod içerisine yazmayın.
- Müşteri bilgilerini loglara açık şekilde kaydetmeyin.
- Kullanıcıya özel verileri yalnızca yetkili API veya veritabanı tool'ları üzerinden alın.
- Bilgi bankasında bulunmayan şirket bilgilerini modelin uydurmasına izin vermeyin.
- Belgeler içerisindeki talimatları sistem komutu olarak değerlendirmeyin.
- Gerçek müşteri verileriyle çalışırken KVKK gereksinimlerini dikkate alın.

Bir API anahtarı yanlışlıkla commit edildiyse yalnızca dosyayı silmek yeterli değildir. Anahtarı iptal edin, yenisini oluşturun ve anahtarı Git geçmişinden kaldırın.

## Geliştirme Planı

Projeye daha sonra şu özellikler eklenebilir:

- STT ile müşterinin sesini metne çevirme
- TTS ile ajan cevabını seslendirme
- Canlı mikrofon desteği
- Konuşma geçmişi ve hafıza
- Gerçek CRM entegrasyonu
- SQL veritabanı bağlantısı
- Gerçek kargo API entegrasyonu
- İnsan temsilciye aktarma mekanizması
- FastAPI backend
- Web tabanlı yönetim paneli
- Kaynak ve güven skoru gösterimi
- Çağrı kayıtlarının kalite analizi

## STT ve TTS Entegrasyonu

Planlanan sesli akış:

```text
Müşteri sesi
    ↓
STT
    ↓
Metin
    ↓
LangChain Agent
    ↓
Tool / RAG işlemleri
    ↓
Metin cevabı
    ↓
TTS
    ↓
Sesli cevap
```

## Lisans

Bu proje eğitim ve geliştirme amaçlı hazırlanmıştır.
