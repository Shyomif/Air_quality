import ee
import geemap
import solara

import os
import json
import ee

# 1. تهيئة محرك GEE (دعم التشغيل المحلي والسحابي عبر Service Account)
try:
    cred_json = os.environ.get("GEE_CREDENTIALS")
    if cred_json:
        # إذا كنا على Render (يقرأ المفتاح من متغيرات البيئة)
        cred_dict = json.loads(cred_json)
        with open("temp_credentials.json", "w") as f:
            json.dump(cred_dict, f)
        
        credentials = ee.ServiceAccountCredentials(cred_dict["client_email"], "temp_credentials.json")
        ee.Initialize(credentials)
    else:
        # التشغيل المحلي على جهازك
        try:
            ee.Initialize(project="disco-aegis-447417-m6")
        except Exception:
            ee.Initialize()
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
