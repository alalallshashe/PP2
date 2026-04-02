-- 1. Upsert: Вставить или обновить (Задание 3.2.2)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE first_name = p_name) THEN
        UPDATE contacts SET phone_number = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO contacts(first_name, phone_number) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 2. Удаление (Задание 3.2.5)
CREATE OR REPLACE PROCEDURE delete_contact_by_data(p_identifier VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE first_name = p_identifier OR phone_number = p_identifier;
END;
$$;