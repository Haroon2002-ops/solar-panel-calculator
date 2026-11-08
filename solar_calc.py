import math

# ---------- SETTINGS (you can change these values) ----------

PANEL_WATT = 585              # Power of one solar panel in watts
PANEL_PRICE_PER_WATT = 42     # Panel price in Rs per watt
EXTRA_COST_FACTOR = 0.50      # Extra 50% for inverter, structure, wiring, installation
PERFORMANCE_RATIO = 0.78      # Real output after heat, dust and inverter losses
DEGRADATION = 0.005           # Panels lose 0.5% output every year
GRID_UNIT_PRICE = 55          # Electricity price in Rs per unit (kWh)
TARIFF_INCREASE = 0.05        # Electricity gets 5% more expensive every year
SYSTEM_YEARS = 25             # Lifetime of the solar system in years

# ---------- SUN DATA ----------

# Average peak sun hours per day for each city
CITIES = {
    "karachi": 5.5,
    "lahore": 5.0,
    "islamabad": 4.9,
    "multan": 5.4,
    "quetta": 5.8,
    "peshawar": 5.0,
}

# Sunlight strength of each month compared to the yearly average
# (summer months are higher, winter months are lower)
MONTH_FACTOR = [0.72, 0.85, 1.02, 1.15, 1.25, 1.25,
                1.08, 1.05, 1.08, 1.05, 0.88, 0.70]

MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

DAYS_IN_MONTH = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


# ---------- FUNCTIONS ----------

def monthly_units(bill):
    """Convert the monthly electricity bill (Rs) into units (kWh)."""
    return bill / GRID_UNIT_PRICE


def system_size_kw(units_month, sun_hours):
    """Calculate the solar system size (kW) needed to cover all your units."""
    daily_units = units_month / 30
    return daily_units / (sun_hours * PERFORMANCE_RATIO)


def panels_needed(kw):
    """Calculate how many panels are needed (always rounded up)."""
    return math.ceil(kw * 1000 / PANEL_WATT)


def system_cost(panels):
    """Calculate the total cost: panels plus inverter, installation, etc."""
    total_watts = panels * PANEL_WATT
    panel_cost = total_watts * PANEL_PRICE_PER_WATT
    return panel_cost * (1 + EXTRA_COST_FACTOR)


def monthly_generation(panels, sun_hours):
    """Return a list of 12 values: units generated in each month."""
    system_kw = panels * PANEL_WATT / 1000
    avg_factor = sum(MONTH_FACTOR) / 12
    result = []
    for i in range(12):
        # Units per day = system size x sun hours x efficiency x month factor
        daily = (system_kw * sun_hours * PERFORMANCE_RATIO
                 * (MONTH_FACTOR[i] / avg_factor))
        result.append(daily * DAYS_IN_MONTH[i])
    return result


def cashflow(panels, sun_hours, years=SYSTEM_YEARS):
    """
    Calculate the running profit or loss for each year.
    Starts negative (you paid for the system) and grows as you save money.
    Returns: list of yearly totals, payback time in years, first-year units.
    """
    cost = system_cost(panels)
    year1_units = sum(monthly_generation(panels, sun_hours))

    total = -cost            # Year 0: you have spent the money
    values = [total]
    payback = None

    for year in range(1, years + 1):
        # Output drops a little every year because of panel aging
        units = year1_units * ((1 - DEGRADATION) ** (year - 1))
        # Electricity price rises every year, so savings grow
        price = GRID_UNIT_PRICE * ((1 + TARIFF_INCREASE) ** (year - 1))
        saving = units * price

        previous_total = total
        total += saving
        values.append(total)

        # Payback = the moment the total crosses zero
        if payback is None and total >= 0:
            payback = (year - 1) + (-previous_total / saving)

    return values, payback, year1_units