# from flask import Flask, render_template, request, jsonify
from flask import Flask, render_template, request, jsonify, send_file
import pandas as pd
import mysql.connector
import os

app = Flask(__name__)

# Database Connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="kinheridencecompanydb"
    )


# Dashboard Home
@app.route('/')
def home():

    conn = get_connection()
    cursor = conn.cursor()

    # Total Records
    cursor.execute("SELECT COUNT(*) FROM shareholder_data")
    total_records = cursor.fetchone()[0]

    # Total Amount
    cursor.execute("""
    SELECT IFNULL(SUM(total_amount),0)
    FROM shareholder_data
    """)
    total_amount = cursor.fetchone()[0]

    # Table Records
    cursor.execute("""
    SELECT
    sr_no,
    shareholder_name,
    shareholder_category,
    nationality_country,
    total_amount
    FROM shareholder_data
    ORDER BY sr_no DESC
    """)

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        records=records,
        total_records=total_records,
        total_amount=total_amount
    )


# Upload Excel
@app.route('/upload', methods=['POST'])
def upload():

    file = request.files['file']

    os.makedirs("uploads", exist_ok=True)

    filepath = os.path.join("uploads", file.filename)

    file.save(filepath)

    df = pd.read_excel(filepath, engine="openpyxl")
    df = df.where(pd.notnull(df), None)

    conn = get_connection()
    cursor = conn.cursor()

    success_count = 0

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
    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    for index, row in df.iterrows():

        try:

            values = (
                row['Sr. No.'],
                row['Type of shareholder/ debenture holder'],
                row['Category of shareholder'],
                row['Details of shareholder/ debenture holder'],
                row['Name of shareholder/ debenture holder'],
                row['Type of security held'],
                row['Class of security held'],
                row['Folio Number / Reference Number'],
                row['DP ID-Client Id-Account Number'],
                row['Nationality/ Country of incorporation'],
                row['Gender'],
                row['Type of Identifier'],
                row['Identification No.'],
                row['Occupation'],
                row['Number of security held'],
                row['Nominal value per security'],
                row['Total amount of securities held (in INR)']
            )

            values = tuple(
                None if pd.isna(v) else v
                for v in values
            )

            cursor.execute(query, values)
            success_count += 1

        except Exception as e:
            print(f"Row {index+1} Error:", e)

    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({
        "message": f"{success_count} Records Imported Successfully"
    })


# Search Shareholder
@app.route('/search')
def search():

    keyword = request.args.get('keyword', '')

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
        sr_no,
        shareholder_name,
        shareholder_category,
        nationality_country,
        total_amount
        FROM shareholder_data
        WHERE shareholder_name LIKE %s
    """, (f"%{keyword}%",))

    records = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "dashboard.html",
        records=records,
        total_records=len(records)
    )
    
    
    from flask import send_file
import os

@app.route('/download')
def download():

    conn = get_connection()

    query = "SELECT * FROM shareholder_data"

    df = pd.read_sql(query, conn)

    conn.close()

    os.makedirs("exports", exist_ok=True)

    file_path = "exports/shareholders.xlsx"

    df.to_excel(file_path, index=False)

    return send_file(
        file_path,
        as_attachment=True
    )


if __name__ == '__main__':
    app.run(debug=True)