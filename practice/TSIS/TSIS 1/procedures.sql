CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone        VARCHAR,
    p_type         VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    cid INT;
BEGIN
    SELECT id INTO cid
    FROM contacts
    WHERE name = p_contact_name;
    IF cid IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;
    INSERT INTO phones (contact_id, phone, type)
    VALUES (cid, p_phone, p_type);
    RAISE NOTICE 'Phone % (%) added to contact "%".', p_phone, p_type, p_contact_name;
END;
$$;
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name   VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    cid INT;
    gid INT;
BEGIN
    SELECT id INTO cid FROM contacts WHERE name = p_contact_name;
    IF cid IS NULL THEN
        RAISE NOTICE 'Contact "%" not found.', p_contact_name;
        RETURN;
    END IF;
    SELECT id INTO gid FROM groups WHERE name = p_group_name;
    IF gid IS NULL THEN
        INSERT INTO groups (name)
        VALUES (p_group_name)
        RETURNING id INTO gid;
        RAISE NOTICE 'Group "%" created.', p_group_name;
    END IF;
    UPDATE contacts
    SET group_id = gid
    WHERE id = cid;
    RAISE NOTICE 'Contact "%" moved to group "%".', p_contact_name, p_group_name;
END;
$$;
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE (
    contact_name  VARCHAR,
    email         VARCHAR,
    phone         VARCHAR,
    phone_type    VARCHAR,
    group_name    VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT
        c.name       AS contact_name,
        c.email      AS email,
        p.phone      AS phone,
        p.type       AS phone_type,
        g.name       AS group_name
    FROM contacts c
    LEFT JOIN phones p ON c.id = p.contact_id
    LEFT JOIN groups g ON c.group_id = g.id
    WHERE c.name  ILIKE '%' || p_query || '%'
       OR c.email ILIKE '%' || p_query || '%'
       OR p.phone ILIKE '%' || p_query || '%';
END;
$$;
CREATE OR REPLACE FUNCTION get_contacts_page(
    p_limit  INT,
    p_offset INT
)
RETURNS TABLE (
    contact_name VARCHAR,
    email        VARCHAR,
    birthday     DATE,
    group_name   VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$;