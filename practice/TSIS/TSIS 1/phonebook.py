import json
import csv
import os
from connect import connect

# Глобальное подключение
conn = connect()
cur = conn.cursor()
PAGE_SIZE = 5


def get_or_create_group(name):
    if not name:
        return None
    cur.execute("SELECT id FROM groups WHERE name=%s", (name,))
    g = cur.fetchone()
    if g:
        return g[0]
    cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (name,))
    return cur.fetchone()[0]


def add_contact():
    name = input("Name: ").strip()
    email = input("Email: ").strip() or None
    birthday = input("Birthday (YYYY-MM-DD): ").strip() or None
    group = input("Group: ").strip()
    phone = input("Phone: ").strip()
    ptype = input("Type (home/work/mobile): ").strip()

    gid = get_or_create_group(group)
    cur.execute(
        "INSERT INTO contacts(name,email,birthday,group_id) VALUES(%s,%s,%s,%s) RETURNING id",
        (name, email, birthday, gid)
    )
    cid = cur.fetchone()[0]
    if phone:
        cur.execute("INSERT INTO phones(contact_id,phone,type) VALUES(%s,%s,%s)",
                    (cid, phone, ptype))
    conn.commit()
    print("Contact added successfully.")


def add_phone():
    name = input("Name: ").strip()
    phone = input("Phone: ").strip()
    ptype = input("Type (home/work/mobile): ").strip()
    try:
        cur.execute("CALL add_phone(%s,%s,%s)", (name, phone, ptype))
        conn.commit()
        print("Phone added.")
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")


def show_all():
    cur.execute("""
        SELECT c.name, c.email, c.birthday, g.name,
               STRING_AGG(p.phone || ' (' || COALESCE(p.type,'?') || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.id
    """)
    rows = cur.fetchall()
    if not rows:
        print("No contacts found.")
        return
    for r in rows:
        print(r)


def search():
    query = input("Search query: ").strip()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    for r in rows:
        print(r)


def filter_by_group():
    group = input("Group: ").strip()
    cur.execute("""
        SELECT c.name, c.email, STRING_AGG(p.phone, ', ')
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        WHERE g.name = %s 
        GROUP BY c.id, c.name, c.email
    """, (group,))
    for r in cur.fetchall():
        print(r)


def search_by_email():
    keyword = input("Email keyword: ").strip()
    cur.execute(
        "SELECT name, email FROM contacts WHERE email ILIKE %s",
        (f"%{keyword}%",)
    )
    for r in cur.fetchall():
        print(r)


def sort_filter():
    g = input("Group (blank=all): ").strip()
    sort_key = input("Sort (name/birthday/date): ").strip().lower()
    sort_column = {
        "name": "c.name",
        "birthday": "c.birthday",
        "date": "c.created_at"
    }.get(sort_key, "c.name")

    q = """
        SELECT c.name, c.email, c.birthday, g.name 
        FROM contacts c 
        LEFT JOIN groups g ON c.group_id = g.id
    """
    params = []
    if g:
        q += " WHERE g.name = %s"
        params.append(g)

    q += f" ORDER BY {sort_column}"
    cur.execute(q, params)
    for r in cur.fetchall():
        print(r)


def pagination():
    page = 0
    while True:
        cur.execute(
            """
            SELECT c.name, c.email, c.birthday, g.name 
            FROM contacts c 
            LEFT JOIN groups g ON c.group_id = g.id 
            ORDER BY c.id 
            LIMIT %s OFFSET %s
            """,
            (PAGE_SIZE, page * PAGE_SIZE)
        )
        rows = cur.fetchall()
        print(f"\n--- Page {page + 1} ---")
        if not rows:
            print("No more contacts.")
        for r in rows:
            print(r)
        
        cmd = input("\nnext / prev / quit: ").strip().lower()
        if cmd == "next" and rows:
            page += 1
        elif cmd == "prev" and page > 0:
            page -= 1
        elif cmd == "quit":
            break


def move_to_group():
    name = input("Name: ").strip()
    group = input("New group: ").strip()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error: {e}")


def delete_contact():
    name = input("Name to delete: ").strip()
    cur.execute("DELETE FROM contacts WHERE name = %s", (name,))
    conn.commit()
    print(f"Deleted {cur.rowcount} contact(s).")


def export_json():
    cur.execute("""
        SELECT 
            c.name, 
            c.email, 
            c.birthday::TEXT, 
            g.name,
            COALESCE(
                JSON_AGG(
                    JSON_BUILD_OBJECT('phone', p.phone, 'type', p.type)
                ) FILTER (WHERE p.id IS NOT NULL), 
                '[]'::json
            )
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        LEFT JOIN phones p ON c.id = p.contact_id
        GROUP BY c.id, c.name, c.email, c.birthday, g.name
        ORDER BY c.id
    """)
    data = [
        {
            "name": r[0],
            "email": r[1],
            "birthday": r[2],
            "group": r[3],
            "phones": r[4]
        }
        for r in cur.fetchall()
    ]
    
    with open("contacts_export.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Exported {len(data)} contacts to contacts_export.json")


def import_json():
    filename = input("JSON file (default: contacts.json): ").strip() or "contacts.json"
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    try:
        with open(filename, encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"Error reading JSON: {e}")
        return

    for item in data:
        name = item.get("name")
        if not name:
            continue

        cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
        existing = cur.fetchone()
        if existing:
            if input(f"Contact '{name}' exists. Skip/overwrite? ").strip().lower() != "overwrite":
                continue
            cur.execute("DELETE FROM contacts WHERE id = %s", (existing[0],))

        gid = get_or_create_group(item.get("group"))
        cur.execute(
            "INSERT INTO contacts(name, email, birthday, group_id) "
            "VALUES(%s, %s, %s, %s) RETURNING id",
            (name, item.get("email"), item.get("birthday"), gid)
        )
        cid = cur.fetchone()[0]

        for p in item.get("phones", []):
            cur.execute(
                "INSERT INTO phones(contact_id, phone, type) VALUES(%s, %s, %s)",
                (cid, p.get("phone"), p.get("type"))
            )
    conn.commit()
    print("JSON import completed.")


def import_csv():
    filename = input("CSV file (default: contacts.csv): ").strip() or "contacts.csv"
    if not os.path.exists(filename):
        print(f"File not found: {filename}")
        return

    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("name")
                if not name:
                    continue

                cur.execute("SELECT id FROM contacts WHERE name = %s", (name,))
                if cur.fetchone():
                    print(f"Skipped (already exists): {name}")
                    continue

                gid = get_or_create_group(row.get("group"))
                cur.execute(
                    "INSERT INTO contacts(name,email,birthday,group_id) "
                    "VALUES(%s,%s,%s,%s) RETURNING id",
                    (name, row.get("email"), row.get("birthday"), gid)
                )
                cid = cur.fetchone()[0]

                phone = row.get("phone")
                if phone:
                    ptype = row.get("type", "mobile")
                    cur.execute(
                        "INSERT INTO phones(contact_id,phone,type) VALUES(%s,%s,%s)",
                        (cid, phone, ptype)
                    )
        conn.commit()
        print("CSV import completed.")
    except Exception as e:
        conn.rollback()
        print(f"CSV import error: {e}")


MENU = {
    "1":  ("Add contact",     add_contact),
    "2":  ("Add phone",       add_phone),
    "3":  ("Show all",        show_all),
    "4":  ("Search",          search),
    "5":  ("Filter by group", filter_by_group),
    "6":  ("Search by email", search_by_email),
    "7":  ("Sort + filter",   sort_filter),
    "8":  ("Pagination",      pagination),
    "9":  ("Move to group",   move_to_group),
    "10": ("Delete",          delete_contact),
    "11": ("Export JSON",     export_json),
    "12": ("Import JSON",     import_json),
    "13": ("Import CSV",      import_csv),
}

try:
    while True:
        print("\n" + "\n".join(f"{k}. {v[0]}" for k, v in MENU.items()) + "\n0. Exit")
        c = input("> ").strip()
        if c == "0":
            break
        if c in MENU:
            try:
                MENU[c][1]()
            except Exception as e:
                conn.rollback()
                print(f"Error: {e}")
except KeyboardInterrupt:
    print("\nProgram terminated by user.")
finally:
    cur.close()
    conn.close()