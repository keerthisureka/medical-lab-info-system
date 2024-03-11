import mysql.connector

def initialize_connection():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "abcd123",
        database = "mlis"
    )
    conn.autocommit = True

    cursor = conn.cursor()
    return conn, cursor

conn, cursor = initialize_connection()

def login(cursor, d):
    cursor.execute(f"""SELECT UserType FROM user WHERE Email='{d[0]}' And Password='{d[1]}';""")
    # rows = cursor.fetchall()
    # for row in rows:
    #     current_username, current_password = row
    #     if current_username == d[0] and current_password == d[1]:
    #         return True
    # return False
    usertype = [item[0] for item in cursor][0]
    return usertype

def register(cursor, data):
    cursor.execute("""SELECT UserID FROM user ORDER BY UserID DESC LIMIT 1""")
    userid = [item[0] for item in cursor]
    userid = int(userid[0]) + 1
    cursor.execute(f"""INSERT INTO user VALUES (
                   '{userid}',
                   '{data["Name"]}',
                   '{data["Email"]}',
                   '{data["Password"]}',
                   '{data["UserType"]}',
                   {data["Age"]},
                   '{data["Gender"]}'
                   )""")

# Admin
cursor.execute("SELECT LabName, LabID FROM lab;")
labnames = [item[0] for item in cursor]

cursor.execute("SELECT TestName, TestID FROM test;")
testnames = [item[0] for item in cursor]

def lab_add(data):
    cursor.execute("""SELECT LabID FROM lab ORDER BY LabID DESC LIMIT 1""")
    labid = [item[0] for item in cursor]
    labid = int(labid[0]) + 1
    cursor.execute(f"""INSERT INTO lab VALUES (
                   '{labid}',
                   '{data["LabName"]}',
                   '{data["ContactNo"]}',
                   '{data["Location"]}',
                   {data["OpenHrs"]},
                   {data["YrsOfExp"]}
    )""")
    return cursor

def test_add(data):
    cursor.execute("""SELECT TestID FROM test ORDER BY TestID DESC LIMIT 1""")
    testid = [item[0] for item in cursor]
    testid = int(testid[0]) + 1
    cursor.execute(f"""INSERT INTO test VALUES (
                   '{testid}',
                   '{data["TestName"]}',
                   '{data["Description"]}',
                   '{data["SampleType"]}',
                   '{data["TestDuration"]}',
                   '{data["NormalRange"]}'
    )""")
    return cursor

def efficiency_add(data):
    cursor.execute(f"""SELECT LabID FROM lab WHERE LabName='{data["Lab"]}'""")
    for item in cursor:
        labid = item[0]
    cursor.execute(f"""SELECT TestID FROM test WHERE TestName='{data["Test"]}'""")
    for item in cursor:
        testid = item[0]
    cursor.execute(f"""INSERT INTO efficiency VALUES (
                   '{labid}',
                   '{testid}',
                   {data["Price"]},
                   {data["TestsPerDay"]},
                   '{data["Sensitivity"]}',
                   '{data["Specificity"]}'
    )""")
    return cursor

def lab_update(data):
    cursor.execute(f"""SELECT LabID FROM lab WHERE LabName='{data["LabName"]}'""")
    labid = [item[0] for item in cursor][0]
    cursor.execute(f"""UPDATE lab SET
                    LabName='{data["LabName"]}',
                    ContactNo={data["ContactNo"]},
                    Location='{data["Location"]}',
                    OpenHrs={data["OpenHrs"]},
                    YrsOfExp={data["YrsOfExp"]} 
                    WHERE LabID='{labid}'
    """)
    return cursor

def test_update(data):
    cursor.execute(f"""SELECT TestID FROM test WHERE TestName='{data["TestName"]}'""")
    testid = [item[0] for item in cursor][0]
    cursor.execute(f"""UPDATE test SET
                    TestName='{data["TestName"]}',
                    Description='{data["Description"]}',
                    SampleType='{data["SampleType"]}',
                    TestDuration='{data["TestDuration"]}',
                    NormalRange='{data["NormalRange"]}'
                    WHERE TestID='{testid}'
    """)
    return cursor

def efficiency_update(data):
    cursor.execute(f"""SELECT LabID FROM lab WHERE LabName='{data["Lab"]}'""")
    for item in cursor:
        labid = item[0]
    cursor.execute(f"""SELECT TestID FROM test WHERE TestName='{data["Test"]}'""")
    for item in cursor:
        testid = item[0]
    cursor.execute(f"""UPDATE efficiency SET
                    LabID='{labid}',
                    TestID='{testid}',
                    Price={data["Price"]},
                    TestsPerDay='{data["TestsPerDay"]}',
                    Sensitivity='{data["Sensitivity"]}',
                    Specificity='{data["Specificity"]}'
                    WHERE TestID='{testid}' AND LabID='{labid}'
    """)
    return cursor

def lab_delete(data):
    cursor.execute(f"""DELETE FROM lab WHERE LabName='{data["LabName"]}'""")
    return cursor

def test_delete(data):
    cursor.execute(f"""DELETE FROM test WHERE TestName='{data["TestName"]}'""")
    return cursor

def efficiency_delete(data):
    cursor.execute(f"""SELECT LabID FROM lab WHERE LabName='{data["Lab"]}'""")
    for item in cursor:
        labid = item[0]
    cursor.execute(f"""SELECT TestID FROM test WHERE TestName='{data["Test"]}'""")
    for item in cursor:
        testid = item[0]
    cursor.execute(f"""DELETE FROM efficiency WHERE LabID='{labid}' AND TestID='{testid}'""")


def lab_details():
    cursor.execute("SELECT LabName, ContactNo, Location, OpenHrs, YrsOfExp FROM lab;")
    return cursor.fetchall()

def test_details():
    cursor.execute("SELECT TestName, Description, SampleType, TestDuration, NormalRange FROM test;")
    return cursor.fetchall()

def efficiency_details():
    cursor.execute("SELECT l.LabName, t.TestName, Price, TestsPerDay, Sensitivity, Specificity FROM test t, lab l, efficiency e WHERE t.TestID=e.TestID AND l.LabID=e.LabID;")
    return cursor.fetchall()


# Patient
def search(t):
    cursor.execute(f"""SELECT t.TestName, l.LabName, l.ContactNo, l.Location, e.Price, l.OpenHrs, l.YrsOfExp, t.Description, t.SampleType, t.TestDuration, e.TestsPerday, e.Sensitivity, e.Specificity FROM lab l, test t, efficiency e WHERE t.TestID IN(SELECT TestID FROM test WHERE TestName='{t}') AND t.TestID=e.TestID AND l.LabID=e.LabID;
                   """)
    details_view = cursor.fetchall()
    return details_view

def book(a, b, c, d):
    cursor.execute("""SELECT ApptID FROM appointment ORDER BY ApptID DESC LIMIT 1""")
    apptid = [item[0] for item in cursor][0]
    apptid = int(apptid) + 1
    cursor.execute(f"""SELECT UserID FROM user WHERE Email='{a}'""")
    for i in cursor:
        userid = i[0]
    cursor.execute(f"""SELECT TestID FROM test WHERE TestName='{b}'""")
    for i in cursor:
        testid = i[0]
    cursor.execute(f"""SELECT LabID FROM lab WHERE LabName='{c}'""")
    for i in cursor:
        labid = i[0]
    cursor.execute(f"""INSERT INTO appointment VALUES ({apptid}, '{userid}', '{labid}', '{testid}', '{d}')""")
    cursor.execute(f"""SELECT
                            t.TestName,
                            l.LabName,
                            a.ApptDate
                        FROM
                            appointment a
                        JOIN
                            test t ON a.TestID = t.TestID
                        JOIN
                            lab l ON a.LabID = l.LabID
                        WHERE
                            a.UserID = '{userid}';""")
    details_view = cursor.fetchall()
    cursor.execute(f"""SELECT ApptID FROM confirmation WHERE ApptID={apptid}""")
    capptid = [item[0] for item in cursor]
    return details_view, capptid


def view_confirm_details(email):
    cursor.execute(f"""SELECT UserID FROM user WHERE Email='{email}'""")
    userid = [item[0] for item in cursor][0]
    cursor.execute(f"""CREATE OR REPLACE VIEW view_confirm_appts AS SELECT t.TestName, l.LabName, c.Confirmed FROM appointment a, confirmation c, test t, lab l WHERE a.ApptID=c.ApptID AND a.LabID=l.LabID AND a.TestID=t.TestID AND a.UserID='{userid}'""")
    cursor.execute("SELECT * FROM view_confirm_appts")
    details_view = cursor.fetchall()
    return details_view

def refresh_appt_details(email):
    cursor.execute(f"""SELECT UserID FROM user WHERE Email='{email}'""")
    userid = [item[0] for item in cursor][0]
    cursor.execute(f"""SELECT
                            t.TestName,
                            l.LabName,
                            a.ApptDate
                        FROM
                            appointment a
                        JOIN
                            test t ON a.TestID = t.TestID
                        JOIN
                            lab l ON a.LabID = l.LabID
                        WHERE
                            a.UserID = '{userid}';""")
    details_view = cursor.fetchall()
    return details_view
