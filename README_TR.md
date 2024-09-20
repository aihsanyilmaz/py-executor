# Selenium Service

Bu proje, Flask tabanlı bir API ile Selenium Grid kullanarak otomasyon testleri çalıştırmak için altyapı sağlar. Hizmet bir Selenium Hub içerir ve Chrome tarayıcılarını destekler. [flask/packages/example.py](flask/packages/example.py) dosyasını inceleyerek kullanımınızı genişletebilirsiniz.

## Proje Yapısı
```
selenium-service/
│
├── flask/ # Flask uygulaması
│ ├── app.py # Ana Flask uygulaması
│ ├── run.py # Selenium işlemlerini yöneten modül
│ ├── fatals.py # Hata yönetimi modülü
│ ├── packages/ # Çalıştırılabilir Python scriptleri
│ └── README.txt # Flask API kullanım kılavuzu
│
├── docker-compose.yml # Docker Compose konfigürasyonu
└── .env # Ortam değişkenleri
```

## Kurulum

1. Projeyi klonlayın:
   ```
   git clone https://github.com/aihsanyilmaz/selenium-service.git
   cd selenium-service
   ```

2. `.env` dosyasını oluşturun ve gerekli değişkenleri ayarlayın:
   ```
   cp example.env .env
   ```
   `.env` dosyasını düzenleyerek gerekli değerleri girin.

3. Docker Compose ile servisleri başlatın:
   ```
   docker-compose up -d
   ```

## Kullanım

### Flask API

Flask API'sinin kullanımı hakkında detaylı bilgi için lütfen [Flask API Kullanım Kılavuzu](flask/README_TR.md) dosyasına bakın.

### Selenium Grid

Selenium Grid, `http://localhost:4444` adresinde çalışır. Bu adresi kullanarak Selenium testlerinizi çalıştırabilirsiniz.

### VNC ile Chrome Node'larına Erişim

Chrome node'larına VNC ile erişmek için:

1. VNC istemcisi kullanarak `localhost:5900`, `localhost:5901`, vb. adreslerine bağlanın.
2. Şifre olarak "secret" kullanın.

Not: VNC port aralığı `.env` dosyasında `VNC_PORT_START` ve `VNC_PORT_END` değişkenleri ile belirlenir.

## Konfigürasyon

Proje konfigürasyonu `.env` dosyası üzerinden yapılır. Önemli konfigürasyon değişkenleri:

- `CHROME_NODES`: Oluşturulacak Chrome node sayısı
- `VNC_PORT_START` ve `VNC_PORT_END`: VNC portları için kullanılacak port aralığı
- `PUSHER_*`: Pusher konfigürasyonu (gerçek zamanlı bildirimler için)
- `AUTH_HASH`: API kimlik doğrulaması için kullanılan hash

## Geliştirme

Yeni paketler eklemek için:

1. `flask/packages/` dizini altında yeni bir Python dosyası oluşturun.
2. Dosya içinde `boot` fonksiyonunu tanımlayın.
3. Selenium ve Pusher fonksiyonlarını kullanarak istediğiniz işlemleri gerçekleştirin.

Örnek bir paket için `flask/packages/example.py` dosyasına bakabilirsiniz.

## Sorun Giderme

- Eğer servislerin başlatılmasında sorun yaşıyorsanız, `docker-compose logs` komutunu kullanarak hata mesajlarını kontrol edin.
- VNC bağlantısında sorun yaşıyorsanız, firewall ayarlarınızı kontrol edin ve gerekli portların açık olduğundan emin olun.

## Katkıda Bulunma

1. Bu repository'yi fork edin
2. Yeni bir feature branch oluşturun (`git checkout -b feature/AmazingFeature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some AmazingFeature'`)
4. Branch'inizi push edin (`git push origin feature/AmazingFeature`)
5. Bir Pull Request oluşturun

## Lisans

Bu proje [MIT Lisansı](LICENSE) altında lisanslanmıştır.