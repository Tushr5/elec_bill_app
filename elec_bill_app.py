
import streamlit as st
import pandas as pd

def calculate_msedcl_bill(units):
    slabs = [
        (100, 4.71, 0.25),
        (200, 10.29, 0.40),
        (200, 14.55, 0.55),
        (500, 16.64, 0.60),
        (float('inf'), 16.64, 0.60)
    ]
    fixed_charges = 639.00
    wheeling_charge_per_unit = 1.17
    electricity_duty_rate = 0.16
    tax_on_sale_per_unit = 0.0
    other_charges = 0.0

    remaining_units = units
    energy_charges = 0.0
    fac_total = 0.0

    for slab_units, rate, fac_rate in slabs:
        if remaining_units <= 0:
            break
        consumed = min(remaining_units, slab_units)
        energy_charges += consumed * rate
        fac_total += consumed * fac_rate
        remaining_units -= consumed

    wheeling_charges = units * wheeling_charge_per_unit
    tax_on_sale = units * tax_on_sale_per_unit
    electricity_duty = energy_charges * electricity_duty_rate

    total_bill = (
        fixed_charges +
        energy_charges +
        wheeling_charges +
        fac_total +
        electricity_duty +
        tax_on_sale +
        other_charges
    )

    bill_data = {
        "Charge Description": [
            "Energy Charges", "FAC", "Wheeling Charges", "Electricity Duty",
            "Tax on Sale", "Fixed Charges", "Other Charges", "Total Bill"
        ],
        "Amount (₹)": [
            round(energy_charges, 2),
            round(fac_total, 2),
            round(wheeling_charges, 2),
            round(electricity_duty, 2),
            round(tax_on_sale, 2),
            round(fixed_charges, 2),
            round(other_charges, 2),
            round(total_bill, 2)
        ]
    }

    return pd.DataFrame(bill_data)

st.set_page_config(page_title="MSEDCL Bill Calculator", layout="centered")
st.title("⚡ Electricity Bill Calculator")
units = st.number_input("Enter units consumed", min_value=0, step=1)
if units > 0:
    bill_df = calculate_msedcl_bill(units)
    st.write("### 📄 Your Bill Breakdown")
    st.dataframe(bill_df, use_container_width=True)
    st.success(f"✅ Total Bill: ₹{bill_df['Amount (₹)'].iloc[-1]:,.2f}")
