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
            /* Light gray background for better e-ink contrast */
            background-color: #EAEAEA; 
            color: #111111; 
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
            overflow: hidden;
            box-sizing: border-box;
        }}

        .container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            padding-top: 50px;
            box-sizing: border-box;
        }}

        .wifi-line {{ 
            font-size: 4.2rem; 
            line-height: 1.4; 
            letter-spacing: 0.5px;
            margin-bottom: 25px;
        }}

        /* Dark box to make the voucher code pop against the light gray background */
        .code-highlight {{
            color: #FFFFFF;
            background-color: #222222;
            padding: 8px 25px;
            border-radius: 12px;
            display: inline-block;
            margin-top: 15px;
        }}

        .logo-footer {{
            margin-top: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        .logo-img {{
            height: 110px;
            width: auto;
            object-fit: contain;
            /* Logo looks best as-is, remove brightness filter for standard icon */
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="wifi-line">
            Guest Wi-Fi<br>
            <span style="font-weight: 400; font-size: 3.2rem; color: #555555;">SSID:{SSID_NAME}</span><br>
            <div class="code-highlight">Code: {voucher_code}</div>
        </div>
        
        <div class="logo-footer">
            <img class="logo-img" src="https://vulcanequipment.github.io/assets/Vulcan_V.png" alt="Vulcan Logo">
        </div>
    </div>
</body>
</html>"""

    output_path = os.path.join(os.path.dirname(__file__), "wifi2.html")
    with open(output_path, "w") as f:
        f.write(html_content)


if __name__ == "__main__":
    code = get_current_voucher()
    build_page(code)
