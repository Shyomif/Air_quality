import os
import json
import ee
import geemap
import solara

# 1. تهيئة GEE مع معالجة حصرية لتنسيق المفتاح ليتوافق مع بايثون الحديثة
try:
    cred_dict = {
      "type": "service_account",
      "project_id": "disco-aegis-447417-m6",
      "private_key_id": "91f28fb1de11a1acab13298d8132731c7505dfa6",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDT4VkNNjjGYFL+\niQvrKg20CkK4EBAE5SUFD5aJY8dlcoqajr+WapnBRPp+M9WaleOgZIH24KKfqI4b\nAenpXcM7OwKDxAxqVylvzegvmZZAv8/mTsgc+v+ZYNKx6m2VzhOBxA4QxHlS/lCO\nf1bI6DzefYPE+OMWxZW0HNi+0CQKQjHCGBZelengX2951Yfq67j9q6uEJGrnlJp7\nNwmkqbTVJSGsqiXvVSLxCR0OSqeJ/5eZPC0g5r+Gs3pSYDl/ckHQfaSU4AiwHVVT\nIKOVw7LraI4l/O6sYNRnmkZH5ktX13MhsYGZYWVlJyfO9C7JjlyZ/vblpYF5hLqJ\nyPVHmvvVAgMBAAECggEABlk33YZ6Da+bLQHsN9VLEybvjYD7CeUtG8lgyFMTXr3K\nMlawP5CIH4YH6g9231U4ZyORJVWLvzRCCxseksh6w2Pm6mMjFW3xJubI2zbt4pjH\nYO42tBpCiFT3Wy9cAzi+gDfgoq37DfqNbVzxZmmsUTpPisUDq44As08zS1xZ3W4a\nV71My6tMsG2OudOqKdYFVslneEwbLAT4m17BWwBqN2iXNFxyZiIe3wMCbn7tGtF5\nyyEb6eC/J1Kau8kYGUGgHQVvE7bxc54QrUTw2W0VbMXEibmw54LdS/enob/Vo0ud\n/P8j/wN2KrroFnNq4ZPEp/4tIeTpCeU+JeYS8XhQIQKBgQD1b7djCkYjiKHx2N7I\nTjRi9E8ViHuE5mX9uZ3KOgvuDfHsvvEgPRf0rWWAUIXceFqLQU1tlUv6mlaUp3Du\ndaFjdY/z7iyxiWjzohMNr983ncKM32ZA4EO9R4lT7xIr1h1xQdeNuxdFXqcE4jfX\niFoqWg7c/Rfyid7vJ9lAzjgAPQKBgQDc/+axYLpIT+LMqzZIWMUs/uD2lNq5k3rt\nMUbvJCkRgJDGVs03mFu609eSShXY9vlRGV5Wg3qmqzXSoGW55IXm6yzGiKBUFGK7\njwiHd1lPpg55+dvSiOrLDjZIxaAZXMyRztfeHsMgenmvak0uJVnMgbV2atQu7GUr\nZvLEe2VLeQKBgBIrtzQJ6q9uyi6Rk8zYnWBGHiTF+f8Y36wtNdVm/sMdHTAd4tQ0\nMbXXsJATZhWwg2OT7huS1hEzo/1VeDLvWod2iLXSiFSMi8ydzzNQNgJ0F5c+Yt+i\nuuEkjrI8HOhJ7dwYt9CybUKhg1QFO4Ulfydri3Yo9sDqHCswlBEMM3ExAoGASysT\nOVPQKJZbawf1H6hp8IME23oH50T9c73mBaMEAPr8wyl1Barh0GsLkKt4QOLILEh3\nqO9xgU0MsoZx80eCL+ffw+tmtRJ1/puI6CK1Ev1FQUG1/icpzUUZO6lUaiwBPLrg\n+6D095AQ4ZRDiiWUJJYdtZhicU9gneGXQzNBYekCgYEAzUMvXnwop0fcWDtFuJih\neLm9y1UjAI+l9xs4Dxb3xkxI0pERf2GTl1cckM/Lax4ggjbCuxXHjCMWUNH9/PQH\ns67U+JC1nfj5yvfNk9PJTkWEwtQJclVQrLjsw0ZV+SsBlfyFL0gzJfPJ74lsyRDa\n5mXgiYTlGcQ7yEE+kGt7s80=\n-----END PRIVATE KEY-----\n",
      "client_email": "air-459@disco-aegis-447417-m6.iam.gserviceaccount.com",
      "client_id": "106450112114837993756",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/air-459%40disco-aegis-447417-m6.iam.gserviceaccount.com",
      "universe_domain": "googleapis.com"
    }

    # تصحيح فواصل الأسطر بدقة فائقة لمنع خطأ التوقيع
    raw_key = cred_dict["private_key"]
    if "\\n" in raw_key:
        raw_key = raw_key.replace("\\n", "\n")
    cred_dict["private_key"] = raw_key

    # كتابة ملف الاعتماد المؤقت
    key_path = "temp_credentials.json"
    with open(key_path, "w", encoding="utf-8") as f:
        json.dump(cred_dict, f)

    # استخدام طريقة التهيئة المباشرة عبر بيانات الاعتماد
    credentials = ee.ServiceAccountCredentials(cred_dict["client_email"], key_path)
    ee.Initialize(credentials=credentials, project=cred_dict["project_id"])
    print("Google Earth Engine initialized successfully via Service Account!")

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
