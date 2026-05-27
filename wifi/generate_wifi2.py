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
            background-color: #111111; /* Sleek dark frame backdrop */
            color: #FFFFFF;           /* High contrast text */
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            text-align: center;
            overflow: hidden;
            box-sizing: border-box;
        }

        /* Inner container that centers everything and scales neatly */
        .container {{
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            padding-top: 50px; /* Leaves room for top header text overlays */
            box-sizing: border-box;
        }

        /* Large, prominent credentials layout */
        .wifi-line {{ 
            font-size: 4.2rem; 
            line-height: 1.4; 
            letter-spacing: 0.5px;
            margin-bottom: 25px;
        }}

        /* Clean highlight variation for the actual access code */
        .code-highlight {{
            color: #FFFFFF;
            background-color: #222222;
            padding: 4px 20px;
            border-radius: 8px;
            border: 2px solid #444444;
            display: inline-block;
            margin-top: 10px;
        }}

        /* Grounded branding footer zone */
        .logo-footer {{
            margin-top: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
        }}

        /* Explicit sizing constraints for the raw transparent PNG asset */
        .logo-img {{
            height: 110px;
            width: auto;
            object-fit: contain;
            /* Subtle image filtering trick to make the dark gray Vulcan text pop against dark themes */
            filter: brightness(1.4); 
        }}
    </style>
    <script>
        // Force frame refresh every 6 hours
        setInterval(function() {{ window.location.reload(); }}, 21600000);
    </script>
</head>
<body>
    <div class="container">
        <div class="wifi-line">
            Guest Wi-Fi<br>
            <span style="font-weight: 400; font-size: 3.2rem; color: #AAAAAA;">{SSID_NAME}</span><br>
            <div class="code-highlight">Code: {voucher_code}</div>
        </div>
        
        <div class="logo-footer">
            <img class="logo-img" src="https://vulcanequipment.github.io/assets/Vulcan_V.png" alt="Vulcan Logo">
        </div>
    </div>
</body>
</html>"""

    # Output to a unique file path so we don't clobber the legacy frame layouts
    output_path = os.path.join(os.path.dirname(__file__), "wifi2.html")

    with open(output_path, "w") as f:
        f.write(html_content)


if __name__ == "__main__":
    code = get_current_voucher()
    build_page(code)
