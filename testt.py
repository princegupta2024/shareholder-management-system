import pandas as pd
import mysql.connector

try:
    # Excel File Read
    df = pd.read_excel(
        "data/sample_500.xlsm",
        engine="openpyxl"
    )

    # NaN ko None mein convert karo
    df = df.where(pd.notnull(df), None)

    # MySQL Connection
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="kinheridencecompanydb"
    )

    cursor = conn.cursor()

    query = """
    INSERT INTO shareholder_data (
        sr_no,
        shareholder_type,
        shareholder_category,
        shareholder_details,
        shareholder_name,
        security_type,
        security_class,
        folio_reference_no,
        dp_client_account_no,
        nationality_country,
        gender,
        identifier_type,
        identification_no,
        occupation,
        security_count,
        nominal_value,
        total_amount
    )
    VALUES (
        %s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s
    )
    """

    success_count = 0
    failed_count = 0

    for index, row in df.iterrows():

        try:

            values = (
                int(row['Sr. No.']) if row['Sr. No.'] is not None else None,
                row['Type of shareholder/ debenture holder'],
                row['Category of shareholder'],
                row['Details of shareholder/ debenture holder'],
                row['Name of shareholder/ debenture holder'],
                row['Type of security held'],
                row['Class of security held'],
                str(row['Folio Number / Reference Number']) if row['Folio Number / Reference Number'] is not None else None,
                str(row['DP ID-Client Id-Account Number']) if row['DP ID-Client Id-Account Number'] is not None else None,
                row['Nationality/ Country of incorporation'],
                row['Gender'],
                row['Type of Identifier'],
                str(row['Identification No.']) if row['Identification No.'] is not None else None,
                row['Occupation'],
                int(float(row['Number of security held'])) if row['Number of security held'] is not None else None,
                float(row['Nominal value per security']) if row['Nominal value per security'] is not None else None,
                float(row['Total amount of securities held (in INR)']) if row['Total amount of securities held (in INR)'] is not None else None
            )

            # NaN ko None mein convert karo
            values = tuple(
                None if pd.isna(v) else v
                for v in values
            )

            cursor.execute(query, values)
            success_count += 1

        except Exception as row_error:
            
            failed_count += 1

            print("\n====================")
            print(f"Row Number : {index + 1}")
            print(f"Sr No      : {row['Sr. No.']}")
            print("Data       :", values)
            print("Error      :", row_error)
            print("====================")

    conn.commit()

    print("\n=================================")
    print("Import Completed")
    print("=================================")
    print(f"Success Records : {success_count}")
    print(f"Failed Records  : {failed_count}")

except FileNotFoundError:
    print("Excel file not found.")

except mysql.connector.Error as db_error:
    print("Database Error:", db_error)

except Exception as e:
    print("Error:", e)

finally:
    try:
        cursor.close()
        conn.close()
    except:
        pass