from extensions import celery 
import pymysql
from utility.format_utils import format_mobile_number, format_email

# @celery.task
# def hrpears_connect(DB_HOST,DB_USER,DB_PASSWORD,DB_NAME,DB_TABLE):
#     if not DB_TABLE.isidentifier():
#         raise ValueError("Invalid table name provided.")

#     connection = pymysql.connect(
#             host=DB_HOST,
#             user=DB_USER,
#             password=DB_PASSWORD,
#             database=DB_NAME,
#             cursorclass=pymysql.cursors.DictCursor
#         )
#     try:
#         with connection.cursor() as cursor:
#             query = f"SELECT first_name, last_name, middle_name, email, mobile_no FROM {DB_TABLE}"
#             cursor.execute(query)
#             raw_data = cursor.fetchall()
#             formatted_data = []
#             for row in raw_data:
#                 last_name = row["last_name"].upper() if row["last_name"] else ""
#                 first_name = row["first_name"].upper() if row["first_name"] else ""
#                 middle_name = row["middle_name"].upper() if row["middle_name"] else ""
#                 formatted_name = f"{last_name}, {first_name} {middle_name}".strip()
#                 formatted_mobile = format_mobile_number(row["mobile_no"])
#                 formatted_email = format_email(row["email"])
#                 formatted_data.append({
#                     "name": formatted_name,
#                     "email": formatted_email,
#                     "mobile_no": formatted_mobile
#                 })
#             return formatted_data

#     finally:
#         if 'connection' in locals() and connection.open:
#             connection.close()