-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.users
(
    id bigserial NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.members
(
    id bigserial NOT NULL,
    user_id bigint NOT NULL,
    group_id bigint NOT NULL,
    role character varying(15),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.alerts
(
    id bigserial NOT NULL,
    content character varying(400),
    date_sent timestamp without time zone,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.recipients
(
    id bigserial NOT NULL,
    member_id bigint NOT NULL,
    alert_id bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.groups
(
    id bigserial NOT NULL,
    parent_group bigint,
    name character varying(30) NOT NULL,
    extra_info character varying(100),
    invitation_code character varying(20) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.participations
(
    id bigserial NOT NULL,
    event_id bigint NOT NULL,
    group_id bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.events
(
    id bigserial NOT NULL,
    name character varying(30) NOT NULL,
    date_start timestamp without time zone NOT NULL,
    date_end timestamp without time zone NOT NULL,
    description character varying(100),
    location character varying(50) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.set_lists
(
    id bigserial NOT NULL,
    event_id bigint NOT NULL,
    composition_id bigint NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.compositions
(
    id bigserial NOT NULL,
    name character varying(50) NOT NULL,
    author character varying(40),
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.files
(
    id bigserial NOT NULL,
    name character varying(50) NOT NULL,
    google_drive_id integer,
    composition_id bigint,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.file_ownerships
(
    id bigserial NOT NULL,
    group_id bigint NOT NULL,
    file_id bigint NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS public.members
    ADD CONSTRAINT user_member_fk FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.members
    ADD CONSTRAINT group_member_fk FOREIGN KEY (group_id)
    REFERENCES public.groups (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.recipients
    ADD CONSTRAINT member_recipient_fk FOREIGN KEY (member_id)
    REFERENCES public.members (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.recipients
    ADD CONSTRAINT alert_recipient_fk FOREIGN KEY (alert_id)
    REFERENCES public.alerts (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.participations
    ADD CONSTRAINT group_participation_fk FOREIGN KEY (group_id)
    REFERENCES public.groups (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.participations
    ADD CONSTRAINT event_to_participation_fk FOREIGN KEY (event_id)
    REFERENCES public.events (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

ALTER TABLE IF EXISTS public.set_lists
    ADD CONSTRAINT event_set_list_fk FOREIGN KEY (event_id)
    REFERENCES public.events (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.set_lists
    ADD CONSTRAINT composition_to_set_list_fk FOREIGN KEY (composition_id)
    REFERENCES public.compositions (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.files
    ADD CONSTRAINT file_to_composition_fk FOREIGN KEY (composition_id)
    REFERENCES public.compositions (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.file_ownerships
    ADD CONSTRAINT group_to_file_ownership_fk FOREIGN KEY (group_id)
    REFERENCES public.groups (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;


ALTER TABLE IF EXISTS public.file_ownerships
    ADD CONSTRAINT file_to_file_ownership_fk FOREIGN KEY (file_id)
    REFERENCES public.files (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION
    NOT VALID;

END;