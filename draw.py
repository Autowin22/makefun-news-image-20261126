#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont

def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    current_line = []
    for word in words:
        test_line = " ".join(current_line + [word])
        if font.getlength(test_line) <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(" ".join(current_line))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
    if current_line:
        lines.append(" ".join(current_line))
    return lines

def main():
    width, height = 1024, 1024
    img = Image.new("RGB", (width, height), "#FFFFFF")
    draw = ImageDraw.Draw(img)

    # Fonts
    font_path_bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font_path_reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

    f_masthead = ImageFont.truetype(font_path_bold, 36)
    f_subdate = ImageFont.truetype(font_path_bold, 13)
    f_lead_head = ImageFont.truetype(font_path_bold, 20)
    f_lead_body = ImageFont.truetype(font_path_reg, 13)
    f_med_head = ImageFont.truetype(font_path_bold, 15)
    f_med_body = ImageFont.truetype(font_path_reg, 11)
    f_small_head = ImageFont.truetype(font_path_bold, 12)
    f_small_body = ImageFont.truetype(font_path_reg, 10)

    # Colors
    c_red = "#990000"
    c_navy = "#000066"
    c_black = "#111111"
    c_gray = "#666666"
    c_box_bg = "#F9F9F9"
    c_border = "#CCCCCC"

    # --- 1. MASTHEAD ---
    # Top header bar
    draw.rectangle([16, 16, 1008, 105], fill=None, outline=c_navy, width=2)
    draw.text((28, 24), "THE WORLD IN ONE PAGE", fill=c_red, font=f_masthead)
    date_text = "THURSDAY, 26 NOVEMBER 2026  |  GLOBAL NEWS EDITION  |  VOL. III, NO. 330"
    draw.text((28, 72), date_text, fill=c_navy, font=f_subdate)

    # --- 2. LEAD STORY (Trump Tariffs) ---
    # Box: y from 115 to 350
    draw.rectangle([16, 115, 1008, 350], fill=c_box_bg, outline=c_border, width=1)
    draw.rectangle([16, 115, 1008, 138], fill=c_navy)
    draw.text((24, 118), "LEAD STORY: TRUMP UNVEILS NEW TARIFFS ON 14 TRADING PARTNERS", fill="#FFFFFF", font=f_subdate)

    # Lead text area (left) and pictogram (right)
    lead_headline = "US IMPOSES BROAD SECTION 301 TARIFFS: CHINA 20%, EU & JAPAN 15%"
    lead_body = (
        "Following an eight-month probe into excess factory capacity and the Supreme Court striking "
        "down earlier duties in February, the US announced new tariffs taking effect after a January 25 hearing. "
        "China faces 20% (rising to 40% if truce breaks), the EU, Japan, South Korea, Taiwan and Switzerland face 15%, "
        "Vietnam 20% (35%), and India 17% (25%). Global stock markets fell sharply on the news."
    )

    # Draw lead text
    y_cursor = 150
    for line in wrap_text(lead_headline, f_lead_head, 680):
        draw.text((28, y_cursor), line, fill=c_black, font=f_lead_head)
        y_cursor += 24

    y_cursor += 6
    for line in wrap_text(lead_body, f_lead_body, 690):
        draw.text((28, y_cursor), line, fill=c_gray, font=f_lead_body)
        y_cursor += 17

    # Lead Pictogram (Tariff / % chart) inside right box [730, 145, 992, 335]
    draw.rectangle([730, 145, 992, 335], fill="#FFFFFF", outline=c_navy, width=2)
    draw.text((745, 155), "TARIFF WALL STRUCTURE", fill=c_red, font=f_small_head)
    # Draw bars representing tariffs
    bars = [("China", 140, 20), ("Vietnam", 115, 20), ("India", 100, 17), ("EU/JP", 85, 15)]
    bx = 750
    by = 185
    for name, bwidth, rate in bars:
        draw.text((bx, by), f"{name}: {rate}%", fill=c_black, font=f_small_body)
        draw.rectangle([bx + 75, by + 2, bx + 75 + bwidth, by + 14], fill=c_red)
        by += 28

    # --- 3. MEDIUM STORIES (Side-by-Side) ---
    # Box 1: Houthi Attack (x: 16 to 504, y: 360 to 570)
    draw.rectangle([16, 360, 504, 570], fill=c_box_bg, outline=c_border, width=1)
    draw.rectangle([16, 360, 504, 382], fill=c_navy)
    draw.text((24, 363), "MIDDLE EAST  ·  OIL MARKETS", fill="#FFFFFF", font=f_subdate)

    m1_head = "HOUTHIS CLAIM STRIKE ON SAUDI'S RAS TANURA REFINERY"
    m1_body = (
        "Riyadh reports four drones intercepted over the kingdom's largest refinery with no injuries. "
        "Brent crude jumped 3.5% to $94.61 a barrel; WTI rose 2% to $83.68 amid escalating regional security fears."
    )
    y_cursor = 394
    for line in wrap_text(m1_head, f_med_head, 320):
        draw.text((28, y_cursor), line, fill=c_black, font=f_med_head)
        y_cursor += 18
    y_cursor += 4
    for line in wrap_text(m1_body, f_med_body, 310):
        draw.text((28, y_cursor), line, fill=c_gray, font=f_med_body)
        y_cursor += 15

    # Oil derrick / flame pictogram in Houthi box
    draw.rectangle([360, 440, 488, 555], fill="#FFFFFF", outline=c_navy, width=1)
    draw.text((370, 445), "BRENT: $94.61", fill=c_red, font=f_small_head)
    # Simple flame/price up icon
    draw.polygon([(424, 470), (444, 510), (404, 510)], fill=c_red)
    draw.line([(375, 530), (410, 500), (440, 515), (475, 470)], fill=c_navy, width=2)

    # Box 2: US Stocks / AI Fears (x: 520 to 1008, y: 360 to 570)
    draw.rectangle([520, 360, 1008, 570], fill=c_box_bg, outline=c_border, width=1)
    draw.rectangle([520, 360, 1008, 382], fill=c_navy)
    draw.text((528, 363), "FINANCIAL MARKETS  ·  WALL STREET", fill="#FFFFFF", font=f_subdate)

    m2_head = "US STOCKS TUMBLE AS FEARS OVER AI INTENSIFY"
    m2_body = (
        "Nasdaq dropped nearly 4% in early trading with all three main US indices down sharply. "
        "Investors re-evaluate high valuations and tech sector exposure as AI enthusiasm encounters headwinds."
    )
    y_cursor = 394
    for line in wrap_text(m2_head, f_med_head, 320):
        draw.text((532, y_cursor), line, fill=c_black, font=f_med_head)
        y_cursor += 18
    y_cursor += 4
    for line in wrap_text(m2_body, f_med_body, 310):
        draw.text((532, y_cursor), line, fill=c_gray, font=f_med_body)
        y_cursor += 15

    # Stock down chart pictogram in Stocks box
    draw.rectangle([864, 440, 992, 555], fill="#FFFFFF", outline=c_navy, width=1)
    draw.text((872, 445), "NASDAQ -4%", fill=c_red, font=f_small_head)
    draw.line([(880, 480), (920, 500), (950, 485), (980, 535)], fill=c_red, width=3)
    draw.rectangle([874, 470, 986, 545], outline=c_border, width=1)


    # --- 4. SMALL STORIES GRID (3 columns x 3 rows) ---
    # y range: 580 to 1008. Total height = 428. 3 rows -> ~136px each.
    # x range: 3 columns: [16, 340], [352, 676], [688, 1008]. Widths ~ 320px each.

    small_stories = [
        ("NETANYAHU BRIBERY CHARGE", "Israeli judges recommend prosecutors drop Case 4000 bribery charge citing considerable difficulties and unlikely conviction; Case 2000 to be reconsidered."),
        ("CAIRO RING ROAD TANKER FIRE", "Fuel tanker overturns and bursts into flames in Giza, Egypt, engulfing 27 vehicles. At least 31 people are killed and 21 injured in the horrific disaster."),
        ("PAKISTANI ASTRONAUT ON TIANGONG", "Muhammad Zeeshan Ali becomes the first foreign astronaut to travel to China's Tiangong space station aboard the historic Shenzhou-24 mission."),
        ("COLOMBIAN POLICE FREE 76 HOSTAGES", "Police storm a supermarket in a dramatic tactical operation, successfully freeing 76 people who had been held hostage for 17 grueling hours."),
        ("RUSSIA WAR TOLL NEARS 500,000", "Official figures released by Moscow indicate total casualties in the ongoing Ukraine conflict have now approached nearly 500,000 personnel."),
        ("NORTH KOREA EXPELS SWISS DIPLOMAT", "Pyongyang expels a Swiss diplomat amid escalating diplomatic tensions and a widening international sanctions dispute."),
        ("MACY'S THANKSGIVING PARADE DELAY", "Iconic New York Thanksgiving Day parade postponed due to severe weather conditions affecting the metropolitan area and wind warnings."),
        ("DURAN DURAN'S ANDY TAYLOR DIES", "Tributes pour in following the death of legendary Duran Duran guitarist Andy Taylor at the age of 65 after a valiant battle with cancer."),
        ("HERA SPACECRAFT VIEWS CRATER", "New high-resolution images from the Hera spacecraft reveal a stadium-sized impact crater on the asteroid targeted to test Earth planetary defenses.")
    ]

    col_coords = [
        (16, 336),   # Col 1
        (352, 672),  # Col 2
        (688, 1008)  # Col 3
    ]
    row_coords = [
        (580, 715),  # Row 1
        (727, 862),  # Row 2
        (874, 1008)  # Row 3
    ]

    for idx, (st_head, st_body) in enumerate(small_stories):
        c_idx = idx % 3
        r_idx = idx // 3
        x1, x2 = col_coords[c_idx]
        y1, y2 = row_coords[r_idx]

        draw.rectangle([x1, y1, x2, y2], fill=c_box_bg, outline=c_border, width=1)
        # Small header bar
        draw.rectangle([x1, y1, x2, y1 + 16], fill=c_navy)
        draw.text((x1 + 6, y1 + 2), st_head[:32], fill="#FFFFFF", font=ImageFont.truetype(font_path_bold, 9))

        sy = y1 + 20
        for line in wrap_text(st_head, f_small_head, x2 - x1 - 12):
            draw.text((x1 + 6, sy), line, fill=c_black, font=f_small_head)
            sy += 14

        sy += 2
        for line in wrap_text(st_body, f_small_body, x2 - x1 - 12):
            draw.text((x1 + 6, sy), line, fill=c_gray, font=f_small_body)
            sy += 12

    # Save output
    out_path = "entry.png"
    img.save(out_path, "PNG")
    print(f"Successfully generated {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    main()
