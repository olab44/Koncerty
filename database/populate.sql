DO $$
        -- 4 uzytkownikow 2 alerty  1 grupa 1 podgrupa 4 pliki 2 eventy 3 adresy 1 kompozycja
DECLARE
    user_id1 bigint;
    user_id2 bigint;
    user_id3 bigint;
    user_id4 bigint;

    alert_id1 bigint;
    alert_id2 bigint;

    member_id1 bigint;
    member_id2 bigint;
    member_id3 bigint;
    member_id4 bigint;
    member_id5 bigint;
    member_id6 bigint;

    group_id1 bigint;
    group_id2 bigint;

    file_id1 bigint;
    file_id2 bigint;
    file_id3 bigint;
    file_id4 bigint;


    event_id1 bigint;
    event_id2 bigint;

    composition_id1 bigint;

    today_timestamp TIMESTAMP WITHOUT TIME ZONE;
    tommorow_timestamp TIMESTAMP WITHOUT TIME ZONE;

BEGIN

    tommorow_timestamp := (CURRENT_TIMESTAMP + INTERVAL '1 day')::timestamp;
    today_timestamp := (CURRENT_TIMESTAMP + INTERVAL '1 hour')::timestamp;

    -- 4 uzytkownikow
    INSERT INTO users (username, email)
    VALUES ('Bilb', 'megalodony.pzsp2@gmail.com')
    RETURNING id INTO user_id1;

    INSERT INTO users (username, email)
    VALUES ('Franek', 'f@gmail.com')
    RETURNING id INTO user_id2;

    INSERT INTO users (username, email)
    VALUES ('Kasia', 'k@gmail.com')
    RETURNING id INTO user_id3;

    INSERT INTO users (username, email)
    VALUES ('Wik', 'w@gmail.com')
    RETURNING id INTO user_id4;
    -- 2 alerty
    INSERT INTO alerts (content, date_sent)
    VALUES ('Wszyscy jestescie super', (CURRENT_TIMESTAMP - INTERVAL '1 day')::timestamp)
    RETURNING id INTO alert_id1;

    INSERT INTO alerts (content, date_sent)
    VALUES ('Super poszlo', (CURRENT_TIMESTAMP - INTERVAL '1 hour')::timestamp)
    RETURNING id INTO alert_id2;
    -- 2 grupy
    INSERT INTO groups (parent_group, name, extra_info, invitation_code)
    VALUES (-1, 'Grajkowie', 'Polub nas na instagramie LINK', 'ASD12')
    RETURNING id INTO group_id1;

    INSERT INTO groups (parent_group, name, extra_info, invitation_code)
    VALUES (-1, 'Kumple', 'Szukaj nas', '123');
    -- 1 podgrupa
    INSERT INTO groups (parent_group, name, extra_info, invitation_code)
    VALUES (group_id1, 'Grajkowie:Strunowe', 'Polub nas na facebooku LINK', 'ABBA')
    RETURNING id INTO group_id2;
    -- 4 czlonkow grupy 1 i 2 podgrupy 2
    INSERT INTO members (user_id, group_id, role)
    VALUES (user_id1, group_id1, 'Kapelmistrz')
    RETURNING id INTO member_id1;

    INSERT INTO members (user_id, group_id, role)
    VALUES (user_id2, group_id1, 'Muzyk')
    RETURNING id INTO member_id2;

    INSERT INTO members (user_id, group_id, role)
    VALUES (user_id3, group_id1, 'Koordynator')
    RETURNING id INTO member_id3;

    INSERT INTO members (user_id, group_id, role)
    VALUES (user_id4, group_id1, 'Muzyk')
    RETURNING id INTO member_id4;

    INSERT INTO members (user_id, group_id, role)
    VALUES (user_id4, group_id2, 'Kapelmistrz')
    RETURNING id INTO member_id5;

    INSERT INTO members (user_id, group_id, role)
    VALUES (user_id1, group_id2, 'Muzyk')
    RETURNING id INTO member_id6;
    -- widomosc 1 do grupy 1, wiadomosc 2 do grupy 2
    INSERT INTO recipients (member_id, alert_id)
    VALUES (member_id1, alert_id1);

    INSERT INTO recipients (member_id, alert_id)
    VALUES (member_id2, alert_id1);

    INSERT INTO recipients (member_id, alert_id)
    VALUES (member_id3, alert_id1);

    INSERT INTO recipients (member_id, alert_id)
    VALUES (member_id4, alert_id1);
    -- do podgrupy
    INSERT INTO recipients (member_id, alert_id)
    VALUES (member_id5, alert_id2);

    INSERT INTO recipients (member_id, alert_id)
    VALUES (member_id6, alert_id2);
    -- 2 eventy
    INSERT INTO events (name, date_start, location, date_end, extra_info, parent_group, type)
    VALUES ('Charetatywne granie', today_timestamp, 'Mariot', (today_timestamp + INTERVAL '1 hour')::timestamp, 'Badzcie', group_id1, 'proba')
    RETURNING id INTO event_id1;

    INSERT INTO events (name, date_start, location, date_end, extra_info, parent_group, type)
    VALUES ('Playing in the pub', tommorow_timestamp, 'Bar', (tommorow_timestamp + INTERVAL '1 hour')::timestamp, 'Zapraszamy', group_id2, 'koncert')
    RETURNING id INTO event_id2;

    INSERT INTO participations (event_id, user_id)
    VALUES (event_id1, user_id1);

    INSERT INTO participations (event_id, user_id)
    VALUES (event_id2, user_id1);

    INSERT INTO participations (event_id, user_id)
    VALUES (event_id1, user_id4);
    
    INSERT INTO participations (event_id, user_id)
    VALUES (event_id1, user_id3);
    -- 1 kompozycja
    INSERT INTO compositions (name, author)
    VALUES ('Symphony no. 5', 'Ludwig van Beethoven')
    RETURNING id INTO composition_id1;
    -- taka sama (1 utwor) setlista dla obu eventow
    INSERT INTO set_lists (event_id, composition_id)
    VALUES (event_id1, composition_id1);

    INSERT INTO set_lists (event_id, composition_id)
    VALUES (event_id2, composition_id1);
    -- 2 pliki
    INSERT INTO files (name, google_drive_id, composition_id)
    VALUES ('Symphony no. 5 notes 1', 123, composition_id1)
    RETURNING id INTO file_id1;

    INSERT INTO files (name, google_drive_id, composition_id)
    VALUES ('Symphony no. 5 notes 2', 1234, composition_id1)
    RETURNING id INTO file_id2;

    INSERT INTO file_ownerships (group_id, file_id)
    VALUES (group_id2, file_id1);

    INSERT INTO file_ownerships (group_id, file_id)
    VALUES (group_id2, file_id2);
END $$;

