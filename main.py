import matplotlib.pyplot as plt
import solar_calc as sc

# ---------- USER INPUT ----------

# Show the list of available cities
print("Cities:", ", ".join(c.title() for c in sc.CITIES))

city = input("Apna shehar: ").strip().lower()

# Keep asking until the user types a city from the list
while city not in sc.CITIES:
    city = input("List mein se shehar likho: ").strip().lower()

bill = float(input("Monthly bijli ka bill (Rs): "))

# Peak sun hours for the chosen city
sun = sc.CITIES[city]

# ---------- CALCULATIONS ----------

units = sc.monthly_units(bill)                    # Bill converted into units (kWh)
kw = sc.system_size_kw(units, sun)                # Required system size in kW
panels = sc.panels_needed(kw)                     # Number of panels needed
cost = sc.system_cost(panels)                     # Total cost of the system
gen = sc.monthly_generation(panels, sun)          # Units generated in each month
flow, payback, year1 = sc.cashflow(panels, sun)   # Profit or loss over 25 years

# ---------- PRINT REPORT ----------

print("\n===== SOLAR REPORT =====")
print(f"Shehar: {city.title()} ({sun} sun hours/din)")
print(f"Monthly units: {units:.0f}")
print(f"Zaroori system: {kw:.1f} kW")
print(f"Panels: {panels} x {sc.PANEL_WATT}W = {panels * sc.PANEL_WATT / 1000:.2f} kW")
print(f"Total cost: Rs {cost:,.0f}")
print(f"Pehle saal ki bijli: {year1:,.0f} units")
print(f"Pehle saal ki bachat: Rs {year1 * sc.GRID_UNIT_PRICE:,.0f}")
print(f"Payback: {payback:.1f} saal")
print(f"25 saal ka net faida: Rs {flow[-1]:,.0f}")

# ---------- GRAPHS ----------

# Create one window with two graphs side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5))

# Left graph: units generated in each month, red line = your monthly need
ax1.bar(sc.MONTH_NAMES, gen, color="orange")
ax1.axhline(units, color="red", linestyle="--", label="Monthly zaroorat")
ax1.set_title("Mahine ke hisaab se solar generation")
ax1.set_ylabel("Units (kWh)")
ax1.legend()

# Right graph: running profit over the years
# The point where the green line crosses the red line (zero) is the payback time
ax2.plot(range(len(flow)), flow, color="green")
ax2.axhline(0, color="red", linestyle="--")
ax2.set_title("25 saal ka cumulative net faida")
ax2.set_xlabel("Saal")
ax2.set_ylabel("Rs")
ax2.grid(True)

plt.tight_layout()
# Save the graph as an image (used in README)
plt.savefig("solar_report.png", dpi=150)
plt.show()