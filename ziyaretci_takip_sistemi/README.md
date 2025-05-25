
# 📌 Proje Başlığı

> Ziyaretçi Takip Sistemi

---

## 🧾 Proje Tanıtımı

Bu uygulama, kullanıcıların ziyaretçi kayıtlarını kolayca oluşturup yönetebileceği bir sistemdir. Kullanıcılar, ziyaretçi bilgilerini ekleyebilir, güncelleyebilir ve silebilir. Ayrıca, kayıtlı ziyaretçilerin listesini görüntüleyebilirler.

---

## 🚀 Proje Özellikleri
 
- 🔐 Kullanıcı kayıt ve giriş işlemleri
- 📅 Ziyaretçi ekleyebilme
- 📝 Ziyaretçi bilgilerini düzenleyebilme ve silebilme
- 🔍 Kayıtlı ziyaretçileri listeleyebilme
- 📦 SQLite veritabanı ile kalıcı veri saklama

---

## ⚙️ Kurulum ve Çalıştırma

### ✅ Gereksinimler
Örneğin:  

Bu projeyi çalıştırmak için bilgisayarınızda aşağıdaki yazılımlar kurulu olmalıdır:

- Python 3.x
- Flask
- Flask-Login
- Flask-SQLAlchemy
- Werkzeug

Ayrıca aşağıdaki kütüphaneler kullanılmaktadır:

- flask
- flask-login
- flask-sqlalchemy
- werkzeug



> Not: Bu kütüphaneleri `requirements.txt` dosyasından otomatik olarak yükleyebilirsiniz.

### 🚀 Uygulamayı Başlatma
Örneğin: 
Uygulama tarayıcınızda http://127.0.0.1:5000/ adresinde çalışacaktır.


## 📂 Proje Dosya Yapısı
```
ziyaretci_takip/
├── first week/
│   ├── app.py                     # Ana Python uygulama dosyası
│   ├── db2json.py                 # Kullanıcıları JSON'a aktaran dosya
│   ├── db3json.py                 # Ziyaretçileri JSON'a aktaran dosya
│   ├── instance/
│   │   └── users.db               # SQLite veritabanı dosyası
│   ├── README.md                   # Proje açıklama dosyası
│   ├── requirements.txt            # Gerekli Python paketlerini içeren dosya
│   ├── static/                     # Statik dosyalar (CSS, JS, resimler)
│   │   ├── base.css                # Uygulamaya ait stil dosyası
│   │   ├── from.css                # Form stil dosyası
│   │   └── index.css               # Anasayfa stil dosyası
│   └── templates/                  # HTML şablonlarının bulunduğu klasör
│       ├── base.html               # Temel HTML yapısı
│       ├── dashboard.html          # Kullanıcı kontrol paneli
│       ├── index.html              # Anasayfa
│       ├── login.html              # Giriş formu
│       ├── register.html           # Kayıt formu
│       ├── users.html              # Kullanıcı listesi
│       ├── user_update.html        # Kullanıcı güncelleme formu
│       ├── visitor_add.html        # Yeni ziyaretçi ekleme formu
│       ├── visitor_list.html       # Ziyaretçi listesi
│       └── visitor_update.html      # Ziyaretçi güncelleme formu
└── users.json                      # Kullanıcı verilerini içeren JSON dosyası
└── ziyaretci.json                  # Ziyaretçi verilerini içeren JSON dosyası
```















