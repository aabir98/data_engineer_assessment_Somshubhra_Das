import os
import json
import mysql.connector
from mysql.connector import Error

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "db_user",
    "password": "6equj5_db_user",
    "database": "home_db"
}

def connect_db():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            print("connected to MySQL DB")
        return conn
    except Error as e:
        print(f"connection error: {e}")
        exit(1)

def run_etl():
    conn = connect_db()
    cur = conn.cursor()

    json_path = os.path.join("data", "fake_property_data_new.json")
    print(f"reading data from {json_path}")
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"found {len(data)} property records")

    for prop in data:
        cur.execute("""
            INSERT INTO property (
                property_title, address, market, flood, street_address, city, state, zip,
                property_type, highway, train, tax_rate, sqft_basement, htw, pool, commercial,
                water, sewage, year_built, sqft_mu, sqft_total, parking, bed, bath,
                basementyesno, layout, rent_restricted, neighborhood_rating,
                latitude, longitude, subdivision, taxes, school_average
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (
            prop.get("Property_Title"), prop.get("Address"), prop.get("Market"),
            prop.get("Flood"), prop.get("Street_Address"), prop.get("City"),
            prop.get("State"), prop.get("Zip"), prop.get("Property_Type"),
            prop.get("Highway"), prop.get("Train"), prop.get("Tax_Rate"),
            prop.get("SQFT_Basement"), prop.get("HTW"), prop.get("Pool"),
            prop.get("Commercial"), prop.get("Water"), prop.get("Sewage"),
            prop.get("Year_Built"), prop.get("SQFT_MU"), str(prop.get("SQFT_Total")),
            prop.get("Parking"), prop.get("Bed"), prop.get("Bath"),
            prop.get("BasementYesNo"), prop.get("Layout"), prop.get("Rent_Restricted"),
            prop.get("Neighborhood_Rating"), prop.get("Latitude"), prop.get("Longitude"),
            prop.get("Subdivision"), prop.get("Taxes"), prop.get("School_Average")
        ))
        property_id = cur.lastrowid

        cur.execute("""
            INSERT INTO leads (
                property_id, reviewed_status, most_recent_status, source, occupancy,
                net_yield, irr, selling_reason, seller_retained_broker, final_reviewer
            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
        """, (
            property_id,
            prop.get("Reviewed_Status"), prop.get("Most_Recent_Status"),
            prop.get("Source"), prop.get("Occupancy"), prop.get("Net_Yield"),
            prop.get("IRR"), prop.get("Selling_Reason"),
            prop.get("Seller_Retained_Broker"), prop.get("Final_Reviewer")
        ))

        for v in prop.get("Valuation", []):
            cur.execute("""
                INSERT INTO valuation (
                    property_id, list_price, previous_rent, zestimate, arv,
                    expected_rent, rent_zestimate, low_fmr, high_fmr, redfin_value
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """, (
                property_id, v.get("List_Price"), v.get("Previous_Rent"),
                v.get("Zestimate"), v.get("ARV"), v.get("Expected_Rent"),
                v.get("Rent_Zestimate"), v.get("Low_FMR"),
                v.get("High_FMR"), v.get("Redfin_Value")
            ))

        for h in prop.get("HOA", []):
            cur.execute("""
                INSERT INTO hoa (property_id, hoa, hoa_flag)
                VALUES (%s,%s,%s);
            """, (property_id, h.get("HOA"), h.get("HOA_Flag")))

        for r in prop.get("Rehab", []):
            cur.execute("""
                INSERT INTO rehab (
                    property_id, underwriting_rehab, rehab_calculation, paint, flooring_flag,
                    foundation_flag, roof_flag, hvac_flag, kitchen_flag, bathroom_flag,
                    appliances_flag, windows_flag, landscaping_flag, trashout_flag
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);
            """, (
                property_id, r.get("Underwriting_Rehab"), r.get("Rehab_Calculation"),
                r.get("Paint"), r.get("Flooring_Flag"), r.get("Foundation_Flag"),
                r.get("Roof_Flag"), r.get("HVAC_Flag"), r.get("Kitchen_Flag"),
                r.get("Bathroom_Flag"), r.get("Appliances_Flag"), r.get("Windows_Flag"),
                r.get("Landscaping_Flag"), r.get("Trashout_Flag")
            ))

        conn.commit()

    print("etl complte")
    cur.close()
    conn.close()

if __name__ == "__main__":
    run_etl()
