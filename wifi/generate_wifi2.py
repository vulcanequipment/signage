import os
import csv
import datetime

SSID_NAME = "FEG_Guest"

def get_current_voucher():
    csv_data = os.environ.get("WIFI_VOUCHERS_RAW", "").strip()
    if not csv_data:
        return "ERROR: Missing Data"

    current_week = datetime.date.today().isocalendar()[1]

    # Cleanly filter out accidental empty lines or spaces from the secret block
    lines = [line.strip() for line in csv_data.split('\n') if line.strip()]
    
    reader = csv.DictReader(lines)
    
    for row in reader:
        try:
            if int(row['week'].strip()) == current_week:
                return row['voucher'].strip()
        except (ValueError, KeyError):
            continue # Skip corrupted rows cleanly without throwing a hard process error
            
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
    output_path = os.path.join(os.path.dirname(__file__), "wifi2.html")

    with open(output_path, "w") as f:
        f.write(html_content)


if __name__ == "__main__":
    code = get_current_voucher()
    build_page(code)
