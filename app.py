import os
import json
import ee
import geemap
import solara

# 1. تكوين المفتاح السري بطريقة قائمة الأسطر لتجنب أخطاء تكسير الحروف (Invalid private key)
try:
    private_key_lines = [
        "-----BEGIN PRIVATE KEY-----",
        "MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDT4VkNNjjGYFL+",
        "iQvrKg20CkK4EBAE5SUFD5aJY8dlcoqajr+WapnBRPp+M9WaleOgZIH24KKfqI4b",
        "AenpXcM7OwKDxAxqVylvzegvmZZAv8/mTsgc+v+ZYNKx6m2VzhOBxA4QxHlS/lCO",
        "f1bI6DzefYPE+OMWxZW0HNi+0CQKQjHCGBZelengX2951Yfq67j9q6uEJGrnlJp7",
        "NwmkqbTVJSGsqiXvVSLxCR0OSqeJ/5eZPC0g5r+Gs3pSYDl/ckHQfaSU4AiwHVVT",
        "IKOVw7LraI4l/O6sYNRnmkZH5ktX13MhsYGZYWVlJyfO9C7JjlyZ/vblpYF5hLqJ",
        "yPVHmvvVAgMBAAECggEABlk33YZ6Da+bLQHsN9VLEybvjYD7CeUtG8lgyFMTXr3K",
        "MLawP5CIH4YH6g9231U4ZyORJVWLvzRCCxseksh6w2Pm6mMjFW3xJubI2zbt4pjH",
        "YO42tBpCiFT3Wy9cAzi+gDfgoq37DfqNbVzxZmmsUTpPisUDq44As08zS1xZ3W4a",
        "V71My6tMsG2OudOqKdYFVslneEwbLAT4m17BWwBqN2iXNFxyZiIe3wMCbn7tGtF5",
        "yyEb6eC/J1Kau8kYGUGgHQVvE7bxc54QrUTw2W0VbMXEibmw54LdS/enob/Vo0ud",
        "/P8j/wN2KrroFnNq4ZPEp/4tIeTpCeU+JeYS8XhQIQKBgQD1b7djCkYjiKHx2N7I",
        "TjRi9E8ViHuE5mX9uZ3KOgvuDfHsvvEgPRf0rWWAUIXceFqLQU1tlUv6mlaUp3Du",
        "daFjdY/z7iyxiWjzohMNr983ncKM32ZA4EO9R4lT7xIr1h1xQdeNuxdFXqcE4jfX",
        "iFoqWg7c/Rfyid7vJ9lAzjgAPQKBgQDc/+axYLpIT+LMqzZIWMUs/uD2lNq5k3rt",
        "MUbvJCkRgJDGVs03mFu609eSShXY9vlRGV5Wg3qmqzXSoGW55IXm6yzGiKBUFGK7",
        "jwiHd1lPpg55+dvSiOrLDjZIxaAZXMyRztfeHsMgenmvak0uJVnMgbV2atQu7GUr",
        "ZvLEe2VLeQKBgBIrtzQJ6q9uyi6Rk8zYnWBGHiTF+f8Y36wtNdVm/sMdHTAd4tQ0",
        "MbXXsJATZhWwg2OT7huS1hEzo/1VeDLvWod2iLXSiFSMi8ydzzNQNgJ0F5c+Yt+i",
        "uuEkjrI8HOhJ7dwYt9CybUKhg1QFO4Ulfydri3Yo9sDqHCswlBEMM3ExAoGASysT",
        "OVPQKJZbawf1H6hp8IME23oH50T9c73mBaMEAPr8wyl1Barh0GsLkKt4QOLILEh3",
        "qO9xgU0MsoZx80eCL+ffw+tmtRJ1/puI6CK1Ev1FQUG1/icpzUUZO6lUaiwBPLrg",
        "+6D095AQ4ZRDiiWUJJYdtZhicU9gneGXQzNBYekCgYEAzUMvXnwop0fcWDtFuJih",
        "eLm9y1UjAI+l9xs4Dxb3xkxI0pERf2GTl1cckM/Lax4ggjbCuxXHjCMWUNH9/PQH",
        "s67U+JC1nfj5yvfNk9PJTkWEwtQJclVQrLjsw0ZV+SsBlfyFL0gzJfPJ74lsyRDa",
        "5mXgiYTlGcQ7yEE+kGt7s80=",
        "-----END PRIVATE KEY-----"
    ]
    
    formatted_private_key = "\n".join(private_key_lines)

    cred_dict = {
      "type": "service_account",
      "project_id": "disco-aegis-447417-m6",
      "private_key_id": "91f28fb1de11a1acab13298d8132731c7505dfa6",
      "private_key": formatted_private_key,
      "client_email": "air-459@disco-aegis-447417-m6.iam.gserviceaccount.com",
      "client_id": "106450112114837993756",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/air-459%40disco-aegis-447417-m6.iam.gserviceaccount.com",
      "universe_domain": "googleapis.com"
    }

    # كتابة ملف الاعتماد المؤقت للسيرفر
    key_path = "temp_credentials.json"
    with open(key_path, "w", encoding="utf-8") as f:
        json.dump(cred_dict, f)

    credentials = ee.ServiceAccountCredentials(cred_dict["client_email"], key_path)
    ee.Initialize(credentials=credentials, project=cred_dict["project_id"])
    print("Google Earth Engine initialized successfully!")

except Exception as e:
    print(f"GEE Initialization Error: {e}")

# 2. تحديد منطقة الدراسة (محافظة اللاذقية)
syria_govs = ee.FeatureCollection("FAO/GAUL/2015/level1")
lattakia = syria_govs.filter(ee.Filter.eq('ADM1_NAME', 'Lattakia'))
roi = lattakia.geometry()

# 3. قاموس بيانات الغازات (S5P Datasets)
s5p_datasets = {
    'NO2 (Nitrogen Dioxide)': {
        'collection': 'COPERNICUS/S5P/OFFL/L3_NO2',
        'band': 'tropospheric_NO2_column_number_density',
        'vis': {'min': 0, 'max': 0.00015, 'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}
    },
    'SO2 (Sulfur Dioxide)': {
        'collection': 'COPERNICUS/S5P/OFFL/L3_SO2',
        'band': 'SO2_column_number_density',
        'vis': {'min': -0.0002, 'max': 0.0005, 'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}
    },
    'CO (Carbon Monoxide)': {
        'collection': 'COPERNICUS/S5P/OFFL/L3_CO',
        'band': 'CO_column_number_density',
        'vis': {'min': 0.02, 'max': 0.04, 'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}
    },
    'HCHO (Formaldehyde)': {
        'collection': 'COPERNICUS/S5P/OFFL/L3_HCHO',
        'band': 'tropospheric_HCHO_column_number_density',
        'vis': {'min': 0.0, 'max': 0.0003, 'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}
    },
    'O3 (Ozone)': {
        'collection': 'COPERNICUS/S5P/OFFL/L3_O3',
        'band': 'O3_column_number_density',
        'vis': {'min': 0.12, 'max': 0.15, 'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}
    },
    'Aerosol Index (UVAI)': {
        'collection': 'COPERNICUS/S5P/OFFL/L3_AER_AI',
        'band': 'absorbing_aerosol_index',
        'vis': {'min': -1.0, 'max': 2.0, 'palette': ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}
    }
}

@solara.component
def Page():
    selected_gas, set_selected_gas = solara.use_state('NO2 (Nitrogen Dioxide)')
    
    # إنشاء الخريطة وإضافة الطبقة بناءً على الغاز المحدد باستخدام use_memo مع اعتمادية selected_gas
    def create_map():
        m = geemap.Map(center=[35.0, 38.0], zoom=8, toolbar_ctrl=False, layer_ctrl=True)
        m.add_basemap('Esri.WorldImagery')
        
        # جلب بيانات الغاز المحدد لعام 2025
        data = s5p_datasets[selected_gas]
        dataset = (ee.ImageCollection(data['collection'])
                   .select(data['band'])
                   .filterDate('2025-01-01', '2025-12-31')
                   .mean()
                   .clip(roi))
        
        m.addLayer(dataset, data['vis'], f'{selected_gas} - 2025')
        m.addLayer(lattakia.style(color='black', fillColor='00000000', width=2), {}, 'Lattakia Boundary')
        return m

    # إعادة إنشاء الخريطة نظيفة بالكامل عند أي تغيير في الغاز المختار، مما يمنع نهائياً تضارب الطبقات
    map_widget = solara.use_memo(create_map, [selected_gas])

    solara.Title("Air Quality & Environmental Dashboard - Solara")

    with solara.Column(style={"min-height": "85vh", "padding": "10px"}):
        solara.Markdown(
            "### لوحة التحكم رصد جودة الهواء لمنطقة اللاذقية ",
            style={
                "text-align": "center",                 # محاذاة النص نحو اليمين
                "color": "#1e3a8a",                      # لون النص (أزرق داكن)
                "font-weight": "700",                    # سماكة الخط
                "font-family": "'Cairo', 'Tajawal', sans-serif", # نوع الخط (خطوط عربية عصرية)
                "background-color": "#f8fafc",           # خلفية خفيفة جداً داخل الصندوق
                "border": "2px solid #cbd5e1",           # لون وسمك الإطار (الحواف)
                "border-radius": "10px",                 # تدوير الحواف
                "padding": "12px 20px",                  # المسافات الداخلية للصندوق
                "margin": "0 auto 15px auto",               # دفع الصندوق نحو اليمين داخل الـ Column
                "max-width": "fit-content",              # جعل عرض الصندوق مناسباً لحجم النص فقط
                "box-shadow": "0 2px 4px rgba(0,0,0,0.05)"        # مسافة أسفل العنوان لتنسيق أفضل
            }
        )
        
        
        # حاوية الخريطة مع القائمة العائمة فوقها
        with solara.Card(elevation=2, style={"height": "80vh", "width": "100%", "position": "relative", "padding": "0px"}):
            
            # عرض الخريطة
            solara.display(map_widget)
            
            # لوحة التحكم العائمة فوق الخريطة
            with solara.Row(style={
                "position": "absolute",
                "top": "15px",
                "left": "100px",
                "z-index": "1000",
                "background-color": "rgba(255, 255, 255, 0.95)",
                "padding": "10px 15px",
                "border-radius": "8px",
                "box-shadow": "0 4px 6px rgba(0,0,0,0.15)",
                "align-items": "center",
                "gap": "15px",
                "max-width": "90%"
            }):
                solara.Select(
                    label="اختر المؤشر الجوي",
                    value=selected_gas,
                    values=list(s5p_datasets.keys()),
                    on_value=set_selected_gas,
                    style={"min-width": "220px"}
                )
                solara.Markdown(f"**الطبقة الحالية:** {selected_gas}")
