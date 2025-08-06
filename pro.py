#!C:/Users/moham/AppData/Local/Programs/Python/Python311/python.exe
print("Content-Type: text/html\r\n\r\n")

import cgi, cgitb, pymysql, sys
cgitb.enable()

form = cgi.FieldStorage()

# Sanitize inputs
username = form.getvalue("username", "").strip()
password = form.getvalue("password", "").strip()
status = form.getvalue("status", "").strip()
fullname = form.getvalue("fullname", "").strip()
contactnumber = form.getvalue("phone", "").strip()
email = form.getvalue("email", "").strip()
submit = form.getvalue("submit")
logined = form.getvalue("login")

# MySQL connection
con = pymysql.connect(host="localhost", user="root", password="", database="registerform")
cur = con.cursor()

# ---------------------- SIGNUP ----------------------
if submit and fullname and contactnumber and email and username and password:
    try:
        q = """INSERT INTO pro (fullname, contact, email, username, password, status) 
               VALUES (%s, %s, %s, %s, %s, %s)"""
        cur.execute(q, (fullname, contactnumber, email, username, password, "new"))
        con.commit()
        print("<script>alert('Successfully Registered');</script>")
    except Exception as e:
        print(f"<script>alert('Signup Error: {str(e)}');</script>")

# ---------------------- LOGIN ----------------------
if logined and username and password:
    try:
        q = "SELECT ID FROM pro WHERE username=%s AND password=%s"
        cur.execute(q, (username, password))
        result = cur.fetchone()
        if result:
            user_id = result[0]
            print(f"<script>alert('Login successful'); window.location='/Project/dashboard.py?identy={user_id}';</script>")
            sys.exit()
        else:
            print("<script>alert('Invalid login credentials');</script>")
    except Exception as e:
        print(f"<script>alert('Login Error: {str(e)}');</script>")

# ---------------------- STATUS UPDATE ----------------------
if username and status and not submit and not logined:
    try:
        q = "UPDATE pro SET status=%s WHERE username=%s"
        cur.execute(q, (status, username))
        con.commit()
        print("Status updated successfully.")
    except Exception as e:
        print(f"Error updating status: {str(e)}")

# ---------------------- INITIAL UI PAGE ----------------------
if not logined:
    print('''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <title>UniLink Portal</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" />
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  <style>
    * {
      margin: 0; padding: 0; box-sizing: border-box;
      font-family: 'Poppins', sans-serif;
    }
    body {
      background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
      height: 100vh;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      color: white;
    }
    .login-trigger {
      color: #00d4ff;
      font-size: 20px;
      padding: 12px 24px;
      border: 2px solid #00d4ff;
      border-radius: 4px;
      cursor: pointer;
      background: transparent;
      transition: 0.4s;
    }
    .login-trigger:hover {
      background: #00d4ff;
      color: #000;
    }
    .overlay {
      position: fixed;
      top: 0; left: 0;
      width: 100%; height: 100%;
      background: rgba(0,0,0,0.85);
      display: none;
      justify-content: center;
      align-items: center;
    }
    .overlay.show { display: flex; }
    .login-box {
      width: 350px;
      background: #000;
      padding: 30px;
      border-radius: 10px;
      box-shadow: 0 0 10px #00d4ff;
    }
    .user-box { margin-bottom: 20px; }
    .user-box input {
      width: 100%;
      padding: 10px;
      border-radius: 25px;
      border: 1px solid #00d4ff;
      background: transparent;
      color: white;
    }
    .user-box label {
      margin-bottom: 5px;
      display: block;
      font-size: 14px;
    }
    .btn-blue {
      background: #00d4ff;
      color: #000;
      border-radius: 25px;
      padding: 10px 20px;
      border: none;
    }
    .extra-options {
      display: flex;
      justify-content: space-between;
      font-size: 13px;
    }
    .extra-options a {
      color: #ff1493;
      text-decoration: none;
    }
    .extra-options a:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

<h2>Welcome to UniLink Portal</h2>

<button class="login-trigger" onclick="showLogin()">Login</button>
<button class="btn btn-primary mt-3" onclick="showModal()">Update Status</button>

<!-- Login Form -->
<div class="overlay" id="loginForm">
  <div class="login-box">
    <h3 class="text-center">LOGIN</h3>
    <form method="POST">
      <div class="user-box">
        <label>Username</label>
        <input type="text" name="username" required />
      </div>
      <div class="user-box">
        <label>Password</label>
        <input type="password" name="password" required />
      </div>
      <input type="hidden" name="login" value="1" />
      <div class="text-center mb-2">
        <button type="submit" class="btn-blue">Sign In</button>
      </div>
      <div class="extra-options">
        <a class="forgot-link">Forgot Password?</a>
        <a class="signup-link" onclick="showSignup()">Sign Up</a>
      </div>
    </form>
  </div>
</div>

<!-- Signup Form -->
<div class="overlay" id="signupForm">
  <div class="login-box">
    <h3 class="text-center">SIGN UP</h3>
    <form method="POST" enctype="multipart/form-data">
      <div class="user-box">
        <label>Full Name</label>
        <input type="text" name="fullname" required />
      </div>
      <div class="user-box">
        <label>Email</label>
        <input type="email" name="email" required />
      </div>
      <div class="user-box">
        <label>Contact</label>
        <input type="tel" name="phone" required />
      </div>
      <div class="user-box">
        <label>Username</label>
        <input type="text" name="username" required />
      </div>
      <div class="user-box">
        <label>Password</label>
        <input type="password" name="password" required />
      </div>
      <input type="hidden" name="submit" value="submit" />
      <div class="text-center mb-2">
        <button type="submit" class="btn-blue">Sign Up</button>
      </div>
      <div class="text-center">
        <a onclick="showLogin()" class="signup-back-link">Back to Login</a>
      </div>
    </form>
  </div>
</div>

<!-- Status Modal -->
<div class="modal fade" id="statusModal" tabindex="-1">
  <div class="modal-dialog modal-dialog-centered">
    <div class="modal-content bg-dark text-white border border-info">
      <div class="modal-header">
        <h5 class="modal-title">Update Status</h5>
        <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
      </div>
      <div class="modal-body">
        <input type="text" id="modal-username" placeholder="Enter Username" class="form-control mb-3">
      </div>
      <div class="modal-footer">
        <button class="btn btn-success" onclick="updateStatus('accepted')">Accept</button>
        <button class="btn btn-danger" onclick="updateStatus('rejected')">Reject</button>
      </div>
    </div>
  </div>
</div>

<script>
  function showLogin() {
    document.getElementById("loginForm").classList.add("show");
    document.getElementById("signupForm").classList.remove("show");
  }
  function showSignup() {
    document.getElementById("signupForm").classList.add("show");
    document.getElementById("loginForm").classList.remove("show");
  }
  function showModal() {
    var modal = new bootstrap.Modal(document.getElementById('statusModal'));
    modal.show();
  }
  function updateStatus(statusValue) {
    var username = document.getElementById("modal-username").value;
    if (!username) {
      alert("Please enter a username.");
      return;
    }
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/Project/dashboard.py", true);
    xhr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    xhr.onload = function () {
      if (xhr.status === 200) {
        alert("Status updated to: " + statusValue);
        bootstrap.Modal.getInstance(document.getElementById('statusModal')).hide();
        location.reload();
      } else {
        alert("Status update failed.");
      }
    };
    xhr.send("username=" + encodeURIComponent(username) + "&status=" + encodeURIComponent(statusValue));
  }
</script>

</body>
</html>
''')

# --------- Clean up ----------
cur.close()
con.close()
