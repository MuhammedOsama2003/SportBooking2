from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# بيانات الأماكن
all_facilities = [
    {"id": 1, "name": "صاله مغطاه شبين الكوم"},
    {"id": 2, "name": "استاد ستي كلوب"},
    {"id": 3, "name": "ملعب اسكواش منوف"},
    {"id": 4, "name": "ملعب اسكواش قويسنا"},
    {"id": 5, "name": "صاله جيم في قويسنا"},
    {"id": 6, "name": "صاله جيم البور شبين"},
    {"id": 7, "name": "حمام سباحه شبين 1"},
    {"id": 8, "name": "حمام سباحه شبين الكوم"},
    {"id": 9, "name": "ملعب كرة قدم الشهداء"},
    {"id": 10,"name": "ملعب الكبتانو بنها"},
    {"id": 11,"name": "ملعب الجمهوريه"}
]

# الصفحة الرئيسية
@app.route("/")
def home():
    return render_template("index.html")

# صفحة الأماكن
@app.route("/facilities")
def facilities_page(): # ⬅️ إلى هذا الاسم
    # نمرر all_facilities إلى القالب تحت اسم facilities
    return render_template("facilities.html", facilities=all_facilities)

# صفحة الحجز
@app.route("/booking", methods=["GET", "POST"])
def booking():
    success = False
    facility_id = request.args.get("facility")
    facility = None
    if facility_id:
        facility = next((f for f in all_facilities if str(f["id"]) == facility_id), None)

    if request.method == "POST":
        name = request.form.get("fullname")
        phone = request.form.get("phone")
        email = request.form.get("email")
        datetime = request.form.get("datetime")
        facility_name = request.form.get("facility")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO bookings (name, phone, email, datetime, facility)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, email, datetime, facility_name))
        conn.commit()
        conn.close()
        success = True

    return render_template("booking.html", facility=facility, success=success)

# تسجيل الدخول
@app.route("/login", methods=["GET", "POST"]) # <--- يجب إضافة methods=["GET", "POST"] هنا
def login():
    if request.method == "POST":
        # هنا يتم استلام بيانات تسجيل الدخول
        username = request.form.get("username")
        password = request.form.get("password")
        
        # ⚠️ في هذه النقطة، يجب إضافة منطق التحقق من اسم المستخدم وكلمة المرور في قاعدة البيانات.
        
        # مثال بسيط لمنطق التحقق (بعد أن يتم تنفيذه)
        # إذا كان التحقق ناجحًا:
        # return redirect("/") 
        # إذا كان التحقق فاشلًا:
        # return render_template("login.html", error="بيانات تسجيل الدخول غير صحيحة")

        # مبدئيًا، يمكنك تركه هكذا حتى إضافة منطق قاعدة البيانات الفعلي
        return redirect("/") # تحويل مؤقت إلى الصفحة الرئيسية بعد إرسال النموذج

    return render_template("login.html")


# تسجيل حساب
@app.route("/register", methods=["GET", "POST"])  # <--- إضافة methods=["GET", "POST"]
def register():
    if request.method == "POST":
        # ⚠️ هنا يتم إضافة منطق معالجة بيانات التسجيل (مثل تخزينها في قاعدة البيانات)
        # اسمح لي أن أضيف لك بنية بسيطة للكود هنا
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # ... (منطق التحقق وحفظ المستخدم في قاعدة البيانات)

        # بعد التسجيل الناجح، قم بتحويل المستخدم إلى صفحة تسجيل الدخول
        return redirect("/login") 

    # إذا كانت طريقة الطلب GET، اعرض النموذج
    return render_template("register.html")
# إنشاء قاعدة البيانات وجدول الحجوزات
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            datetime TEXT,
            facility TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    app.run(debug=True, port=5001)  # تم إضافة port=5001
  

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
# استيراد أدوات الأمان لتشفير وفك تشفير كلمات المرور
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
# يجب تعيين مفتاح سري لإدارة الجلسات (Sessions) بشكل آمن
app.config['SECRET_KEY'] = 'your_strong_and_secret_key_here_12345'

# بيانات الأماكن (تم تغيير الاسم لتجنب التعارض)
all_facilities = [
    {"id": 1, "name": "صاله مغطاه شبين الكوم"},
    {"id": 2, "name": "استاد ستي كلوب"},
    {"id": 3, "name": "ملعب اسكواش منوف"},
    {"id": 4, "name": "ملعب اسكواش قويسنا"},
    {"id": 5, "name": "صاله جيم في قويسنا"},
    {"id": 6, "name": "صاله جيم البور شبين"},
    {"id": 7, "name": "حمام سباحه شبين 1"},
    {"id": 8, "name": "حمام سباحه شبين الكوم"},
    {"id": 9, "name": "ملعب كرة قدم الشهداء"},
    {"id": 10,"name": "ملعب الكبتانو بنها"},
    {"id": 11,"name": "ملعب الجمهوريه"}
]

# الصفحة الرئيسية
@app.route("/")
def home():
    # تمرير حالة تسجيل الدخول للقالب
    return render_template("index.html", user_id=session.get('user_id'))

# صفحة الأماكن
@app.route("/facilities")
def facilities_page():
    # استخدام all_facilities
    return render_template("facilities.html", facilities=all_facilities)

# صفحة الحجز
@app.route("/booking", methods=["GET", "POST"])
def booking():
    success = False
    facility_id = request.args.get("facility")
    facility = None
    if facility_id:
        # استخدام all_facilities
        facility = next((f for f in all_facilities if str(f["id"]) == facility_id), None)

    if request.method == "POST":
        # تحقق بسيط من تسجيل الدخول قبل الحجز
        if not session.get('user_id'):
            return redirect(url_for('login')) 
            
        name = request.form.get("fullname")
        phone = request.form.get("phone")
        email = request.form.get("email")
        datetime = request.form.get("datetime")
        facility_name = request.form.get("facility")

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO bookings (name, phone, email, datetime, facility)
            VALUES (?, ?, ?, ?, ?)
        """, (name, phone, email, datetime, facility_name))
        conn.commit()
        conn.close()
        success = True

    return render_template("booking.html", facility=facility, success=success, user_id=session.get('user_id'))

# ----------------- منطق المصادقة -----------------

# تسجيل الدخول
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # 🟢 التعديل الإجباري لتسجيل الدخول
        if username == 'simpleuser' and password == 'simplepass':
            session['user_id'] = 1000 # قيمة ID عشوائية
            return redirect(url_for("home"))
        # 🛑 نهاية التعديل الإجباري

        # ... (بقية كود الاتصال بقاعدة البيانات) ...
        # ...
        
        # ...
        # if user_record:
        #     user_id, password_hash = user_record
            
        #     if check_password_hash(password_hash, password): # ⬅️ أعد التعليق على هذا الجزء
        #         session['user_id'] = user_id
        #         return redirect(url_for("home"))
        
        # فشل تسجيل الدخول
        return render_template("login.html", error="اسم المستخدم أو كلمة المرور غير صحيحة.")

    return render_template("login.html")
# تسجيل حساب
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        # تشفير كلمة المرور قبل حفظها
        hashed_password = generate_password_hash(password) 

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        
        try:
            # إدراج بيانات المستخدم في جدول users
            cur.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
                        (username, hashed_password, email))
            conn.commit()
            conn.close()
            return redirect(url_for("login")) 
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="اسم المستخدم موجود بالفعل.")

    return render_template("register.html")

# تسجيل الخروج
@app.route("/logout")
def logout():
    session.pop('user_id', None) # مسح الـ user_id من الجلسة
    return redirect(url_for('home'))

# ----------------- إنشاء قاعدة البيانات -----------------

# إنشاء قاعدة البيانات وجدول الحجوزات (تم إضافة جدول users)
def init_db():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    
    # 1. إنشاء جدول المستخدمين (الجديد)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            email TEXT
        )
    """)
    
    # 2. جدول الحجوزات (القديم)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            email TEXT,
            datetime TEXT,
            facility TEXT
        )
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    # أعد التعليق هنا
    # init_db()  
    
    # ... (بقية سطر تشغيل التطبيق)
    app.run(debug=False, host='0.0.0.0', port=8081)

# from flask import Flask, render_template, request, redirect, url_for, session
# import sqlite3
# # استيراد أدوات الأمان لتشفير وفك تشفير كلمات المرور
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# # تم تعيين مفتاح سري لضمان أمان الجلسات
# app.config['SECRET_KEY'] = 'A_VERY_LONG_AND_COMPLEX_RANDOM_KEY_1234567890ABCDEF' # تم تحديثه

# # بيانات الأماكن (تم تغيير الاسم لتجنب التعارض)
# all_facilities = [
#     {"id": 1, "name": "صاله مغطاه شبين الكوم"},
#     {"id": 2, "name": "استاد ستي كلوب"},
#     {"id": 3, "name": "ملعب اسكواش منوف"},
#     {"id": 4, "name": "ملعب اسكواش قويسنا"},
#     {"id": 5, "name": "صاله جيم في قويسنا"},
#     {"id": 6, "name": "صاله جيم البور شبين"},
#     {"id": 7, "name": "حمام سباحه شبين 1"},
#     {"id": 8, "name": "حمام سباحه شبين الكوم"},
#     {"id": 9, "name": "ملعب كرة قدم الشهداء"},
#     {"id": 10,"name": "ملعب الكبتانو بنها"},
#     {"id": 11,"name": "ملعب الجمهوريه"}
# ]

# # الصفحة الرئيسية
# @app.route("/")
# def home():
#     # تمرير حالة تسجيل الدخول للقالب
#     return render_template("index.html", user_id=session.get('user_id'))

# # صفحة الأماكن
# @app.route("/facilities")
# def facilities_page():
#     # استخدام all_facilities
#     return render_template("facilities.html", facilities=all_facilities)

# # صفحة الحجز
# @app.route("/booking", methods=["GET", "POST"])
# def booking():
#     success = False
#     facility_id = request.args.get("facility")
#     facility = None
#     if facility_id:
#         # استخدام all_facilities
#         facility = next((f for f in all_facilities if str(f["id"]) == facility_id), None)

#     if request.method == "POST":
#         # تحقق بسيط من تسجيل الدخول قبل الحجز
#         if not session.get('user_id'):
#             return redirect(url_for('login')) 
            
#         name = request.form.get("fullname")
#         phone = request.form.get("phone")
#         email = request.form.get("email")
#         datetime = request.form.get("datetime")
#         facility_name = request.form.get("facility")

#         conn = sqlite3.connect("database.db")
#         cur = conn.cursor()
#         cur.execute("""
#             INSERT INTO bookings (name, phone, email, datetime, facility)
#             VALUES (?, ?, ?, ?, ?)
#         """, (name, phone, email, datetime, facility_name))
#         conn.commit()
#         conn.close()
#         success = True

#     return render_template("booking.html", facility=facility, success=success, user_id=session.get('user_id'))

# # ----------------- منطق المصادقة -----------------

# # تسجيل الدخول (تم تصحيحه لإزالة الكود المؤقت وتفعيل التحقق من الهاش)
# @app.route("/login", methods=["GET", "POST"])
# def login():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
        
#         conn = sqlite3.connect("database.db")
#         cur = conn.cursor()
        
#         # البحث عن المستخدم
#         cur.execute("SELECT id, password_hash FROM users WHERE username = ?", (username,))
#         user_record = cur.fetchone()
#         conn.close() # إغلاق الاتصال بعد الانتهاء من قاعدة البيانات

#         if user_record:
#             user_id, password_hash = user_record
            
#             # التحقق من كلمة المرور باستخدام الهاش المحفوظ
#             if check_password_hash(password_hash, password):
#                 session['user_id'] = user_id # تسجيل المستخدم في الجلسة
#                 return redirect(url_for("home")) # التحويل الناجح
        
#         # فشل تسجيل الدخول
#         return render_template("login.html", error="اسم المستخدم أو كلمة المرور غير صحيحة.")

#     return render_template("login.html")

# # تسجيل حساب
# @app.route("/register", methods=["GET", "POST"])
# def register():
#     if request.method == "POST":
#         username = request.form.get("username")
#         password = request.form.get("password")
#         email = request.form.get("email")

#         # تشفير كلمة المرور قبل حفظها
#         hashed_password = generate_password_hash(password) 

#         conn = sqlite3.connect("database.db")
#         cur = conn.cursor()
        
#         try:
#             # إدراج بيانات المستخدم في جدول users
#             cur.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
#                         (username, hashed_password, email))
#             conn.commit()
#             conn.close()
#             return redirect(url_for("login")) 
#         except sqlite3.IntegrityError:
#             conn.close()
#             return render_template("register.html", error="اسم المستخدم موجود بالفعل.")

#     return render_template("register.html")

# # تسجيل الخروج
# @app.route("/logout")
# def logout():
#     session.pop('user_id', None) # مسح الـ user_id من الجلسة
#     return redirect(url_for('home'))

# # ----------------- إنشاء قاعدة البيانات -----------------

# # إنشاء قاعدة البيانات وجدول الحجوزات (تم إضافة جدول users)
# def init_db():
#     conn = sqlite3.connect("database.db")
#     cur = conn.cursor()
    
#     # 1. إنشاء جدول المستخدمين (الجديد)
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT NOT NULL UNIQUE,
#             password_hash TEXT NOT NULL,
#             email TEXT
#         )
#     """)
    
#     # 2. جدول الحجوزات (القديم)
#     cur.execute("""
#         CREATE TABLE IF NOT EXISTS bookings (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             name TEXT,
#             phone TEXT,
#             email TEXT,
#             datetime TEXT,
#             facility TEXT
#         )
#     """)
#     conn.commit()
#     conn.close()

# if __name__ == "__main__":
#     # ⚠️ تذكر إعادة تفعيل دالة init_db() في أول تشغيل
#     # init_db()  
    
#     app.run(debug=False, host='0.0.0.0', port=8081)