import os
import csv
import datetime

SSID_NAME = "FEG_Guest"

def get_current_voucher():
    # Grab the raw CSV text from the GitHub environment secret
    csv_data = os.environ.get("WIFI_VOUCHERS_RAW", "")
    if not csv_data:
        return "ERROR: Missing Data"

    # Find current week number (1-52)
    current_week = datetime.date.today().isocalendar()[1]

    # Parse the raw string text as a CSV file
    lines = csv_data.strip().split('\n')
    reader = csv.DictReader(lines)
    
    for row in reader:
        if int(row['week'].strip()) == current_week:
            return row['voucher'].strip()
            
    return "Code Expired"

def build_page(voucher_code):
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            font-weight: 900;
            background-color: #FFFFFF;
            color: #000000;
            margin: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
            overflow: hidden;
        }}
        .wifi-line {{ font-size: 3.5rem; line-height: 1.3; }}
    </style>
    <script>
        // Force Joan frame refresh every 6 hours
        setInterval(function() {{ window.location.reload(); }}, 21600000);
    </script>
</head>
<body>
    <div class="wifi-line">
        Guest Wi-Fi: {SSID_NAME}<br>Code: {voucher_code}
    </div>
</body>
</html>"""

    # Output to index.html for GitHub Pages to serve
    with open("index.html", "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    code = get_current_voucher()
    build_page(code)
