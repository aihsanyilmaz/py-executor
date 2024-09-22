# Asenkron Python Çalıştırıcı API

Bu FastAPI tabanlı uygulama, dinamik Python kodu yürütme için asenkron bir API sağlar. Uygulama, `files/` dizininde bulunan Python betiklerini çalıştırabilir ve sonuçları asenkron olarak işler. Gerçek zamanlı bildirimler için Pusher entegrasyonu kullanılmıştır, böylece uzun süren işlemlerin ilerlemesi ve sonuçları anında istemcilere iletilebilir.

## Temel Özellikler

- Asenkron kod yürütme: `asyncio` kullanarak eşzamansız işlem yapabilme
- Dinamik dosya yükleme: `files/` dizinindeki Python betiklerini çalıştırabilme
- Gerçek zamanlı bildirimler: Pusher ile işlem durumu ve sonuçlarını anlık iletme
- RESTful API: FastAPI ile hızlı ve modern bir API arayüzü
- API Güvenliği: API anahtarı tabanlı kimlik doğrulama
- Yapılandırılabilir: Çevresel değişkenler ile esnek konfigürasyon
- Docker desteği: Kolay dağıtım ve ölçeklendirme için Dockerfile içerir

## Proje Yapısı

Proje yapısı aşağıdaki gibidir:

```
app/
├── files/
│   └── example.py  # Örnek Python betiği
├── main.py
├── dependencies.py
├── process.py
├── execution.log
├── Dockerfile
└── README.md
```

`files/` dizini, çalıştırılacak Python betiklerini içerir. `example.py` dosyası, API'nin nasıl kullanılacağını gösteren bir örnek betik olarak sunulmuştur.

## Kurulum ve Çalıştırma

### Docker ile Kurulum

1. Projeyi klonlayın:
   ```
   git clone <repo-url>
   cd <proje-dizini>
   ```

2. Docker imajını oluşturun:
   ```
   docker build -t asenkron-python-api .
   ```

3. Docker konteynerini çalıştırın:
   ```
   docker run -p 8000:8000 asenkron-python-api
   ```

### Manuel Kurulum

1. Gerekli bağımlılıkları yükleyin:
   ```
   pip install -r requirements.txt
   ```

2. Uygulamayı çalıştırın:
   ```
   uvicorn main:app --reload
   ```

## Kullanım

1. Python betiğinizi `files/` dizinine yerleştirin.
2. API'yi kullanarak betiğinizi çalıştırın (detaylar için `/docs` endpoint'ini ziyaret edin).
3. Sonuçları Pusher üzerinden gerçek zamanlı olarak alın.

Örnek olarak, `files/example.py` dosyasını çalıştırmak için API'yi kullanabilirsiniz.

## API Dokümantasyonu

API dokümantasyonuna erişmek ve tüm endpoint'leri görmek için:
- Swagger UI: `http://your-domain/docs`

## Pusher Entegrasyonu

Uygulama, gerçek zamanlı bildirimler için Pusher kullanmaktadır. Pusher ayarlarınızı `.env` dosyasında yapılandırabilirsiniz.

## Güvenlik

- Tüm API istekleri, `X-API-KEY` header'ı ile doğrulanmalıdır.
- API anahtarınızı güvende tutun ve düzenli olarak değiştirin.
- `.env` dosyasını asla version control sistemine eklemeyin.

## Katkıda Bulunma

Hata raporları, özellik istekleri ve pull request'ler için lütfen GitHub üzerinden iletişime geçin.

## Lisans

[MIT Lisansı](LICENSE)
