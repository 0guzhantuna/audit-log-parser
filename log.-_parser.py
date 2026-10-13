import re
import json
from datetime import datetime

# 1. Log dosyasını oku
with open("server_logs.txt", "r") as file:
    logs = file.readlines()

ip_counts = {}

for line in logs:
    if "FAILED_LOGIN" in line:
        ip_match = re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", line)
        if ip_match:
            ip_address = ip_match.group()
            if ip_address in ip_counts:
                ip_counts[ip_address] += 1
            else:
                ip_counts[ip_address] = 1

# 2. JSON için kurumsal rapor şablonu (Sözlük/Dictionary yapısı) oluştur
report_data = {
    "report_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "critical_threats": [],
    "ignored_events": []
}

# 3. IP'leri kurallara göre JSON şablonundaki ilgili listelere ekle
for ip, count in ip_counts.items():
    event_details = {"ip_address": ip, "failed_attempts": count}
    
    if count >= 2:
        report_data["critical_threats"].append(event_details)
    else:
        report_data["ignored_events"].append(event_details)

# 4. Veriyi JSON dosyası olarak kaydet ("w" = write/yazma modu)
with open("threat_report.json", "w", encoding="utf-8") as json_file:
    json.dump(report_data, json_file, indent=4, ensure_ascii=False)

print("✅ Analiz başarıyla tamamlandı! Sonuçlar 'threat_report.json' dosyasına kaydedildi.")