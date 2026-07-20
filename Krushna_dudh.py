import streamlit as st
import pandas as pd
import calendar as cal
from fpdf import FPDF
import tempfile
import os

def generate_block_timetable(data, year, month):
    """
    Generate block-style timetable:
    Each route has blocks of continuous dates with same vehicle.
    (KEEPING LOGIC AS YOU PROVIDED — DO NOT CHANGE)
    """
# --- Flexible assignment for any Excel change ---
    routes = data['RUTE NAME'].dropna().tolist()
    vehicles = data['GADI_NUMBER'].dropna().tolist()

# Assign fixed vehicles = number of routes
    fixed_vehicle_count = len(routes)
    fixed_vehicles = vehicles[:fixed_vehicle_count]
    backup_vehicles = vehicles[fixed_vehicle_count:]

    days_in_month = cal.monthrange(year, month)[1]

    # Pre-assign holidays for fixed vehicles
    holidays = {v: [] for v in fixed_vehicles}
    for i, v in enumerate(fixed_vehicles):
        day = (i % 5) + 6
        while len(holidays[v]) < 5 and day <= days_in_month:
            holidays[v].append(day)
            day += 6

    timetable_blocks = {}
    backup_index = 0

    for r_idx, route in enumerate(routes):
        vehicle = fixed_vehicles[r_idx % len(fixed_vehicles)]
        blocks = []
        start_day = 1
        current_vehicle = vehicle

        for day in range(1, days_in_month + 1):
            # Check if vehicle changes (holiday)
            if day in holidays[vehicle]:
                assigned_vehicle = f"{backup_vehicles[backup_index]} (H)"
                backup_index = (backup_index + 1) % len(backup_vehicles)
            else:
                assigned_vehicle = vehicle

            # If vehicle changes, end previous block
            if assigned_vehicle != current_vehicle:
                blocks.append({"start": start_day, "end": day-1, "vehicle": current_vehicle})
                current_vehicle = assigned_vehicle
                start_day = day

            # Handle last day
            if day == days_in_month:
                blocks.append({"start": start_day, "end": day, "vehicle": current_vehicle})

        timetable_blocks[route] = blocks

    return timetable_blocks

def generate_summary(timetable_blocks, fixed_vehicles, days_in_month):
    """
    Summary: Count working days vs holidays for each vehicle
    (keeps your original semantics)
    """
    summary = []
    for v in fixed_vehicles:
        work_days = 0
        for route_blocks in timetable_blocks.values():
            for block in route_blocks:
                if v in block['vehicle'] and "(H)" not in block['vehicle']:
                    work_days += block['end'] - block['start'] + 1
        holidays = days_in_month - work_days
        summary.append({"Vehicle": v, "Working Days": work_days, "Holidays": holidays})
    return pd.DataFrame(summary)

# ----------------- PDF layout----------------- #
class CompactPDF(FPDF):
    def header(self):
        # Title header
        self.set_font("Arial", "B", 14)
        self.cell(0, 8, "Krishna Dudh Vehicle Timetable", ln=True, align="C")
        self.ln(2)

    def draw_route_blocks_compact(self, route_name, blocks, month_name, columns_per_row=4):
        """
        Draw blocks in rows. columns_per_row controls how many boxes per row (default 4).
        Does NOT alter block content/logic.
        """
        # some layout params
        left_margin = 15
        right_margin = 15
        page_width = self.w - left_margin - right_margin
        gap = 6  # horizontal gap between boxes
        vgap = 6  # vertical gap between rows of boxes
        box_height = 18

        # compute box width such that 'columns_per_row' fit in page_width with gaps
        box_width = (page_width - (columns_per_row - 1) * gap) / columns_per_row

        # Title for route
        self.set_font("Arial", "B", 12)
        # ensure space before a route; if near bottom add page
        if self.get_y() > (self.h - 60):
            self.add_page()
        self.set_x(left_margin)
        self.cell(0, 6, f"Route: {route_name}", ln=True)
        self.ln(2)

        # Prepare rows of boxes
        rows = []
        cur_row = []
        for b in blocks:
            cur_row.append(b)
            if len(cur_row) == columns_per_row:
                rows.append(cur_row)
                cur_row = []
        if cur_row:
            rows.append(cur_row)

        # Draw each row
        for row in rows:
            x = left_margin
            y = self.get_y()
            max_box_height_in_row = box_height

            for b in row:
                # fill color based on holiday marker
                if "(H)" in b["vehicle"]:
                    self.set_fill_color(255, 153, 153)  # light red fill
                    text_color = (80, 30, 30)
                else:
                    self.set_fill_color(153, 255, 153)  # light green fill
                    text_color = (20, 60, 20)

                # draw rect with fill
                self.set_xy(x, y)
                self.rect(x, y, box_width, max_box_height_in_row, style="DF")

                # write centered text inside the box
                self.set_xy(x + 1, y + 2)
                self.set_text_color(*text_color)
                self.set_font("Arial", "B", 9)
                # vehicle line
                # Use multi_cell but limit width to box_width-2, center alignment
                self.multi_cell(box_width - 2, 5, b["vehicle"], border=0, align='C')
                # date line (smaller)
                self.set_font("Arial", "", 8)
                date_line = f"{b['start']}-{b['end']} {month_name}"
                # move cursor just below previous multi_cell for the same x
                # To center date line we compute left offset
                current_x = self.get_x()  # after multi_cell it moved; we will set back
                self.set_xy(x + 1, y + 10)
                self.multi_cell(box_width - 2, 4, date_line, border=0, align='C')

                # reset x to next box position
                self.set_text_color(0, 0, 0)
                x += box_width + gap

            # after finishing row, move Y to next row position
            self.set_xy(left_margin, y + max_box_height_in_row + vgap)

        # small gap after route
        self.ln(4)
        # restore fill/text color defaults
        self.set_text_color(0, 0, 0)

def generate_pdf_compact_arranged(timetable_blocks, month_name, year, file_path, columns_per_row=4):
    pdf = CompactPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()
    pdf.set_font("Arial", "", 10)

    # legend
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 5, f"Month: {month_name}   Year: {year}", ln=True)
    pdf.ln(2)
    pdf.set_font("Arial", "", 9)
    pdf.cell(0, 5, "Notation: Green = Assigned vehicle  |  Red = Backup/Holiday (H)", ln=True)
    pdf.ln(4)

    for route, blocks in timetable_blocks.items():
        pdf.draw_route_blocks_compact(route, blocks, month_name, columns_per_row=columns_per_row)
    pdf.set_font("Arial","",10)
    pdf.cell(40, 8, "Date : ", border=0)
    pdf.ln(12)
    pdf.set_font("Arial","",10)
    pdf.cell(40, 5, "Signature : ",border=0)
    pdf.ln(12)
    
    pdf.output(file_path)

# ----------------- Streamlit UI ----------------- #
st.set_page_config(page_title="Krishna Dudh Vehicle Timetable", page_icon="🚛",layout="wide")
st.title("🚍 Krishna Dudh - Vehicle-Route Timetable")

uploaded_file = st.file_uploader("Upload Excel file (with 'RUTE NAME' and 'GADI_NUMBER')", type=["xlsx"])

# allow flexible year input
year = st.number_input("Year", min_value=2000, max_value=2100, value=2025, step=1)
months = list(cal.month_name)[1:]
selected_month = st.selectbox("Select Month", months)
month_num = months.index(selected_month) + 1
days_in_month = cal.monthrange(year, month_num)[1]

if uploaded_file:
    data = pd.read_excel(uploaded_file)

    if st.button("Generate Timetable"):
        # keep your block generation logic unchanged
        timetable_blocks = generate_block_timetable(data, year, month_num)

        # show compact textual preview in app
        st.subheader(f"Time Table preview - {selected_month} {year}")
        for route, blocks in timetable_blocks.items():
            block_text = " | ".join([f"{b['start']}-{b['end']} {selected_month}: {b['vehicle']}" for b in blocks])
            st.markdown(f"**{route}** → {block_text}")

        # generate and offer PDF download (4 columns per row)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            generate_pdf_compact_arranged(timetable_blocks, selected_month, year, tmp_file.name, columns_per_row=4)
            pdf_bytes = open(tmp_file.name, "rb").read()
            st.download_button("⬇️ Download Timetable PDF", data=pdf_bytes,
                               file_name=f"compact_timetable_{year}_{month_num}.pdf",
                               mime="application/pdf")
            # cleanup temp file
            try:
                os.remove(tmp_file.name)
            except Exception:
                pass

                # ---------- Generate Complete CSV Timetable ----------
        st.subheader("📥 Download Complete Monthly Timetable (CSV)")

        all_rows = []
        for route, blocks in timetable_blocks.items():
            for b in blocks:
                for day in range(b["start"], b["end"] + 1):
                    all_rows.append({
                        "Date": f"{year}-{month_num:02d}-{day:02d}",
                        "Route": route,
                        "Vehicle": b["vehicle"].replace(" (H)", "")
                    })

        full_timetable_df = pd.DataFrame(all_rows)
        st.dataframe(full_timetable_df)

        csv_all = full_timetable_df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Full Month Timetable (CSV)",
                           data=csv_all,
                           file_name=f"timetable_{year}_{month_num}.csv",
                           mime="text/csv")


        # Summary
        fixed_vehicles = data['GADI_NUMBER'].dropna().tolist()[:14]
        summary = generate_summary(timetable_blocks, fixed_vehicles, days_in_month)
        st.subheader("📊 Vehicle Work & Holiday Summary")
        st.dataframe(summary)
        csv_summary = summary.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download Vehicle Summary CSV", data=csv_summary,
                           file_name=f"summary_{year}_{month_num}.csv", mime="text/csv")
        
        




