#!C:/Users/moham/AppData/Local/Programs/Python/Python311/python.exe
print("Content-type: text/html\r\n\r\n")

import cgi, cgitb, pymysql
cgitb.enable()

# DB connection
con = pymysql.connect(host="localhost", user="root", password="", database="registerform")
cur = con.cursor()

# Get form input
form = cgi.FieldStorage()
n = form.getvalue('identy')

# Start HTML
print('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>User Details</title>
    <link rel="stylesheet" type="text/css" href="user_details.css">
</head>
<body>
''')

# Validate input
if n is not None:
    try:
        query = "SELECT * FROM pro WHERE id = %s"
        cur.execute(query, (n,))
        rows = cur.fetchall()

        if rows:
            for row in rows:
                print(f'''
                <div class="card">
                    <h2>User Details</h2>
                    <div class="info">
                        <p><span class="label">Full Name:</span> {row[1]}</p>
                        <p><span class="label">Email:</span> {row[2]}</p>
                        <p><span class="label">Username:</span> {row[4]}</p>
                        <p><span class="label">Password:</span> {row[3]}</p>
                        <p><span class="label">Status:</span> {row[5]}</p>
                    </div>
                </div>
                ''')
        else:
            print("<p style='text-align:center; color:red;'>No user found with the given ID.</p>")

    except Exception as e:
        print(f"<p style='color:red;'>Error: {e}</p>")
else:
    print("<p style='text-align:center; color:red;'>No ID provided.</p>")

print('</body></html>')
