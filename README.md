# Krushna Dudh Vehicle Management System 🐄🚚  
**A custom-built fleet scheduling and automation system for Krushna Dudh Sangh, Islampur**

🔗 **Live Demo (Internal Use):** [Streamlit App](https://krushna-dudh-vehicle-mangament-system-updated.streamlit.app/)  
📂 **Repository (Implementation):** [GitHub](https://github.com/Vedika-Sd/Krushna-Dudh-Vehicle-mangament-system)

---

## 🏢 About the Project  

The **Krushna Dudh Vehicle Management System** is a specialized web application designed to automate the **daily vehicle timetable management** for *Krushna Dudh Sangh, Islampur*.  

Earlier, route schedules and vehicle assignments were manually created on paper or Excel, which often caused **conflicts, overlaps, and time delays**. We worked closely with the organization to understand their real-world challenges and **built a reliable, automated system** that now saves hours of manual planning every single day.  

---

## 🚩 Real Problem We Solved  

Before automation, the process involved:  
- Manually preparing daily vehicle schedules  
- Frequent route conflicts (same driver/vehicle assigned twice)  
- Long hours spent updating or reassigning routes  

This system eliminated all of those pain points by offering a **smart, conflict-free, and instantly updatable** timetable interface.  

---

## Working Video

https://github.com/user-attachments/assets/b8eb5ca4-ad58-41e3-8d6f-682542f5bc6e

You may see demo video in 2x speeded manual 

---
## 💡 Our Solution & Impact  

- 🕒 **Automation:** Replaced manual scheduling with one-click TIMETABLE generation for month.  
- 🚫 **Error-Free Scheduling:** Detects and prevents duplicate vehicle/driver bookings.  
- 📊 **Visual Dashboard:** Simple, interactive view of all active routes and vehicles.  
- ⏱️ **Time Saved:** Reduced planning time from *3–4 hours* daily to *just a few minutes*.  
- 💪 **Reliability:** Ensures smooth delivery operations and route transparency.  

> We worked hard to automate this task — from understanding problem to validating every scheduling rule — ensuring the system truly fits Krushna Dudh’s real need.

---

## 🌟 Key Features  

- 📅 **Monthly Excel Upload:**  
  Admin can upload an Excel sheet each month containing fixed routes and assigned vehicles.  

- ⚙️ **Automatic Timetable Generation:**  
  The system intelligently generates a **complete monthly timetable** for every route, minimizing manual effort.  

- 🧾 **Downloadable PDF Output:**  
  Each timetable is **exportable in a compact, color-coded PDF format** that’s easy to print and share.  

- 📊 **Vehicle Summary Report:**  
  Automatically generates a monthly **summary of each vehicle’s working hours and holidays**, ensuring transparency in workload distribution.  

- 🔄 **Smart Spare Vehicle Management:**  
  When a vehicle is unavailable or on holiday, the system **automatically replaces it with a spare vehicle**, balancing the total work hours across all vehicles efficiently.  

---

> 💡 Together, these features ensure that **Krushna Dudh Sangh’s daily and monthly vehicle operations are fully automated, consistent, and fair — saving hours of manual planning while ensuring equal workload for every vehicle.**

---

## 🧩 Tech Stack  

| Component | Technology Used |
|------------|-----------------|
| Frontend & Backend | **Python (Streamlit)** |
| Data Handling | **pandas**, Python built-ins |
| Deployment | **Streamlit Cloud** |
| Version Control | **GitHub** |

---

## ⚙️ System Flow  

1. **Data Input:** Admin enters or imports driver/vehicle details.  
2. **Scheduling Logic:** System automatically checks and assigns vehicles to routes.  
3. **Conflict Prevention:** No vehicle/driver can be booked for two routes at once.  
4. **Dashboard:** Displays the full day’s timetable in real time.
5. **PDF Download**: Prinatble compact size pdf genrates

---

## 🧭 Installation (For Internal Use Only)

```
# 1. Clone the private repository
git clone https://github.com/Vedika-Sd/Krushna-Dudh-Vehicle-mangament-system.git
cd Krushna-Dudh-Vehicle-mangament-system

# 2. (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run Krushna_dudh.py
```

## Team

- Vedika Sardeshmuk
- Dnyneshwari Pawar
