from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pymysql
import time

app = Flask(__name__)
app.secret_key = "Yo0_secret_key"

db_config = {
    "host": "localhost",
    "user": "root",
    "password": "12345678",
    "database": "website",
    "cursorclass": pymysql.cursors.DictCursor
}

connection = pymysql.connect(**db_config)

@app.route("/")
def go_home():
    if "username" in session:
        return redirect(url_for("go_member"))
    return render_template("index.html")

@app.route("/signup", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        name = request.form.get("registerName")
        username = request.form.get("registerUsername")
        password = request.form.get("registerPassword")
        try:
            with connection.cursor() as cursor:
                sql_check = "SELECT * FROM member WHERE username = %s"
                cursor.execute(sql_check, (username,))
                existing_user = cursor.fetchone()
                if existing_user:
                    return redirect("/error?message=Account has been Registered! SorryQQ")
                sql_insert = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
                cursor.execute(sql_insert, (name, username, password))
                connection.commit()
            return redirect(url_for("go_home"))
        except Exception as ex:
            print("Error:", ex)
    return redirect("/error?message=Could not get request! SorryQQ")

@app.route("/signin", methods=["GET", "POST"])
def sign_in():
    username = request.form.get("signinUsername")
    password = request.form.get("signinPassword")
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM member WHERE username = %s AND password = %s"
            cursor.execute(sql, (username, password))
            result = cursor.fetchone()
        if result:
            session["member_id"] = result["id"]
            session["username"] = result["username"]
            session["name"] = result["name"]
            return redirect(url_for("go_member"))
        return redirect("/error?message=Username or Password is not Correct.")
    except Exception as ex:
        print("Error:", ex)

@app.route("/member")
def go_member():
    if "member_id" in session:
        name = session["name"]
        member_id = session["member_id"]
        print(name)
        try:
            with connection.cursor() as cursor:
                sql = """
                SELECT mem.name, msg.content, msg.id, msg.member_id
                FROM member mem
                INNER JOIN message msg ON mem.id = msg.member_id;
                """
                cursor.execute(sql)
                messages = cursor.fetchall()
            return render_template("member.html", name=name, messages=messages,member_id=member_id)
        except Exception as ex:
            print("Error:", ex)
            messages = []
    return redirect(url_for("go_home"))


@app.route("/error")
def get_error():
    error_message = request.args.get("message")
    return render_template("error.html", error_message=error_message)

@app.route("/signout")
def sign_out():
    session.pop("member_id", None)
    session.pop("username", None)
    session.pop("name", None)
    return redirect(url_for("go_home"))

@app.route("/createMessage", methods=["POST"])
def create_Message():
    if "member_id" in session:
        member_id = session["member_id"]
        messageContent = request.form.get("message_content")
        try:
            with connection.cursor() as cursor:
                sql_insert = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
                cursor.execute(sql_insert, (member_id, messageContent))
                connection.commit()
                inserted_message_id = cursor.lastrowid
                print("Message saved successfully.")
                return str(inserted_message_id)
        except Exception as ex:
            print("Error:", ex)
            return "Failed to save message."
    return "Not received message"

@app.route("/deleteMessage", methods=["POST"])
def delete_Message():
    if "member_id" in session:
        message_ID = request.form.get("message_ID")
        print(message_ID)
        try:
            with connection.cursor() as cursor:
                sql_delete = "DELETE FROM message WHERE id = %s"
                cursor.execute(sql_delete, (message_ID,))
                connection.commit()
                print("Deleted message")
                return jsonify({"ok": True})
        except Exception as ex:
            print("Error:", ex)
            return jsonify({"ok": False})
    return jsonify({"ok": False})


@app.route("/api/member", methods=["GET", "PATCH"])
def member_api():
    if "member_id" in session:
        if request.method == "GET":
            try:
                username = request.args.get("username")

                with connection.cursor() as cursor:
                    sql = "SELECT id, name, username FROM member WHERE username = %s"
                    cursor.execute(sql, (username))
                    result = cursor.fetchone()

                if result:
                    return jsonify({"data": result})
                else:
                    return jsonify({"data": None})

            except Exception as ex:
                print("Error:", ex)
                return jsonify({"data": None})

        if request.method == "PATCH":
            try:
                data = request.json
                new_name = data.get("name")
                member_id = session["member_id"]
                session["name"]= new_name

                with connection.cursor() as cursor:
                    sql_update = "UPDATE member SET name = %s WHERE id = %s"
                    cursor.execute(sql_update, (new_name, member_id))
                    connection.commit()
                return jsonify({"ok": True})

            except Exception as ex:
                print("Error:", ex)
                return jsonify({"error": True})
        else:
            return jsonify({"error": True, "message": "Unsupported method"})
    return jsonify({"data": None})


if __name__ == "__main__":
    app.run(port=3000, debug=True)
