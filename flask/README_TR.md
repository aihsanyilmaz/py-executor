API Kullanım Dökümanı
=====================

Bu API, çeşitli işlemleri gerçekleştirmek için tasarlanmıştır. Tüm istekler için kimlik doğrulama gereklidir.

Kimlik Doğrulama
----------------
Tüm istekler için 'X-Auth-Hash' header'ı gereklidir. Bu header'ın değeri, size verilen özel hash ile eşleşmelidir.

Örnek:
X-Auth-Hash: your_secret_hash_here

Endpoints
---------

1. Uygulama Durumu Kontrolü
   URL: /
   Metod: GET
   Açıklama: Uygulamanın çalışıp çalışmadığını kontrol eder.
   Dönüş: "Merhaba, Flask uygulaması çalışıyor!"

2. Fonksiyon Çalıştırma
   URL: /run
   Metod: POST
   Açıklama: Belirtilen dosyadaki 'boot' fonksiyonunu çalıştırır.
   Gerekli Alanlar:
     - process_id: İşlem için benzersiz bir tanımlayıcı
     - file_path: Çalıştırılacak dosyanın yolu
   Opsiyonel Alanlar:
     - args: Fonksiyona gönderilecek argümanlar listesi
     - kwargs: Fonksiyona gönderilecek anahtar kelimeli argümanlar sözlüğü
     - callback_url: Hata durumunda bildirim gönderilecek URL
   Örnek İstek Gövdesi:
   {
     "process_id": "12345",
     "file_path": "packages/example.py",
     "args": [1, 2, 3],
     "kwargs": {"param1": "value1"},
     "callback_url": "http://example.com/callback"
   }
   Dönüş: İşlemin başlatıldığını belirten bir mesaj ve process_id

3. Fatal Hataları Listeleme
   URL: /fatals
   Metod: GET
   Açıklama: Kaydedilmiş tüm fatal hata dosyalarını listeler.
   Dönüş: Fatal hata dosyalarının listesi

4. Fatal Hata Detayları
   URL: /fatals/<filename>
   Metod: GET
   Açıklama: Belirtilen fatal hata dosyasının içeriğini gösterir.
   Dönüş: Hata detaylarını içeren JSON verisi

5. Fatal Hata Kaydını Silme
   URL: /fatals/<filename>
   Metod: DELETE
   Açıklama: Belirtilen fatal hata dosyasını siler.
   Dönüş: 
     Başarılı ise: Silme işleminin başarılı olduğunu belirten bir mesaj
     Başarısız ise: Hata mesajı

Hata Kodları
------------
- 400 Bad Request: Gerekli alanlar eksik veya hatalı
- 401 Unauthorized: Kimlik doğrulama başarısız
- 404 Not Found: İstenen kaynak bulunamadı
- 500 Internal Server Error: Sunucu tarafında bir hata oluştu

Notlar
------
- Tüm istekler ve yanıtlar JSON formatındadır.
- Hata durumunda, hata mesajı 'error' alanında döndürülür.
- '/run' endpoint'i asenkron çalışır. İşlem hemen başlatılır ve kontrol geri döndürülür.
- Fatal hatalar 'fatals' dizininde .txt dosyaları olarak saklanır.
- Fatal hata kayıtları DELETE isteği ile silinebilir, ancak bu işlem geri alınamaz.
- Çalıştırılan dosyalar içerisinde Pusher kullanılarak gerçek zamanlı bildirimler gönderilebilir.

Pusher Kullanımı
----------------
Çalıştırılan dosyalar içerisinde Pusher kullanılabilir. Bu, gerçek zamanlı bildirimler göndermek için kullanışlıdır.

Pusher Kullanım Örneği:
Çalıştırılan Python dosyası içerisinde aşağıdaki gibi Pusher kullanılabilir:

```python
def boot(*args, **kwargs):
    # Pusher event'i tetikleme
    safe_trigger('my-channel', 'my-event', {'message': 'İşlem başladı'})
    
    # Ana işlevsellik burada yer alır
    # ...

    # İşlem tamamlandığında başka bir event tetikleme
    safe_trigger('my-channel', 'process-completed', {'message': 'İşlem tamamlandı'})
```

`safe_trigger` fonksiyonu, Pusher client'ın mevcut olup olmadığını kontrol eder ve güvenli bir şekilde event'i tetikler. Bu fonksiyon otomatik olarak enjekte edilir, bu nedenle doğrudan kullanılabilir.

Parametreler:
- İlk parametre: Kanal adı
- İkinci parametre: Event adı
- Üçüncü parametre: Gönderilecek veri (dict formatında)

Not: Pusher kullanımı opsiyoneldir. Eğer Pusher yapılandırılmamışsa, `safe_trigger` çağrıları sessizce yok sayılır ve hata oluşturmaz.

Selenium Kullanımı
------------------
Çalıştırılan dosyalar içerisinde Selenium kullanılarak uzak bir tarayıcıda işlemler yapılabilir. Selenium ile ilgili gerekli importlar ve driver oluşturma işlevi otomatik olarak sağlanmaktadır.

Selenium Kullanım Örneği:
Çalıştırılan Python dosyası içerisinde aşağıdaki gibi Selenium kullanılabilir:

```python
def boot(*args, **kwargs):
    driver = get_selenium_driver()
    
    driver.get("https://www.example.com")
    title = driver.title
    
    driver.quit()
    
    return {"status": "success", "title": title}
```

Kullanılabilir Selenium Öğeleri:
- get_selenium_driver(): Selenium WebDriver nesnesini döndürür
- By: Selenium'un By sınıfı
- WebDriverWait: Selenium'un WebDriverWait sınıfı
- EC: Selenium'un expected_conditions modülü

Not:
- Selenium Hub'a bağlantı otomatik olarak yapılandırılmıştır.
- İşlemler tamamlandıktan sonra mutlaka driver.quit() çağrısı yaparak tarayıcıyı kapatın.
- Hata yönetimi için try-except blokları kullanmanız önerilir.
