-- 1. Поиск по паттерну
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_search TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT contact_id, first_name, phone_number 
    FROM contacts 
    WHERE first_name ILIKE '%' || p_search || '%' 
       OR phone_number LIKE '%' || p_search || '%';
END;
$$ LANGUAGE plpgsql;

-- 2. Пагинация (Задание 3.2.4)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT contact_id, first_name, phone_number 
    FROM contacts 
    ORDER BY contact_id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;