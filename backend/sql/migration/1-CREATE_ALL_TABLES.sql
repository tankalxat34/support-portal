-- Table: public.user_role

-- DROP TABLE IF EXISTS public.user_role;

CREATE TABLE IF NOT EXISTS public.user_role
(
    iid smallint NOT NULL,
    title character varying(20) COLLATE pg_catalog."default" NOT NULL,
    create_incident boolean,
    direct_incident boolean,
    create_alteration boolean,
    create_task boolean DEFAULT false,
    create_order boolean DEFAULT false,
    create_appeal boolean DEFAULT true,
    CONSTRAINT user_role_pkey PRIMARY KEY (iid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_role
    OWNER to postgres;


-- Table: public.portal_user

-- DROP TABLE IF EXISTS public.portal_user;

-- CREATE TABLE IF NOT EXISTS public.portal_user
-- (
--     iid SERIAL PRIMARY KEY,
--     ad_login text COLLATE pg_catalog."default" NOT NULL,
--     ad_name text COLLATE pg_catalog."default" NOT NULL,
--     ad_email text COLLATE pg_catalog."default" NOT NULL,
--     additional_email text COLLATE pg_catalog."default",
--     mobile_phone text COLLATE pg_catalog."default" NOT NULL,
--     --CONSTRAINT portal_role FOREIGN KEY (portal_role)
-- 	portal_role smallint NOT NULL DEFAULT 1,
-- 	FOREIGN KEY (portal_role)
--         REFERENCES public.user_role (iid)
-- 	--CONSTRAINT portal_user_pkey PRIMARY KEY (iid)
-- )

-- TABLESPACE pg_default;

-- ALTER TABLE IF EXISTS public.portal_user
--     OWNER to postgres;

-- COMMENT ON TABLE public.portal_user
--     IS 'Пользователи портала';

-- Table: public.portal_user

-- DROP TABLE IF EXISTS public.portal_user;

CREATE TABLE IF NOT EXISTS public.portal_user
(
    iid SERIAL PRIMARY KEY,
    ad_login text COLLATE pg_catalog."default" NOT NULL,
    ad_name text COLLATE pg_catalog."default" NOT NULL,
    ad_email text COLLATE pg_catalog."default" NOT NULL,
    additional_email text COLLATE pg_catalog."default",
    mobile_phone text COLLATE pg_catalog."default" NOT NULL,
    portal_role smallint NOT NULL DEFAULT 1,
    CONSTRAINT portal_user_pkey PRIMARY KEY (iid),
    CONSTRAINT portal_user_portal_role_fkey FOREIGN KEY (portal_role)
        REFERENCES public.user_role (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.portal_user
    OWNER to postgres;

COMMENT ON TABLE public.portal_user
    IS 'Пользователи портала';

-- Table: public.alteration

-- DROP TABLE IF EXISTS public.alteration;

CREATE TABLE IF NOT EXISTS public.alteration
(
    iid SERIAL PRIMARY KEY,
    iid_user bigint NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    iid_executor bigint NOT NULL,
    --CONSTRAINT alteration_pkey PRIMARY KEY (iid),
    CONSTRAINT iid_executor FOREIGN KEY (iid)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT iid_user FOREIGN KEY (iid_user)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.alteration
    OWNER to postgres;

COMMENT ON TABLE public.alteration
    IS 'Изменение : может быть создано только разработчиком  в рамках существующего Продукта';


-- Table: public.appeal

-- DROP TABLE IF EXISTS public.appeal;

CREATE TABLE IF NOT EXISTS public.appeal
(
    iid SERIAL PRIMARY KEY,
    iid_user bigint NOT NULL DEFAULT '-1'::integer,
    title text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    iid_executor bigint NOT NULL,
    --CONSTRAINT appeal_pkey PRIMARY KEY (iid),
    CONSTRAINT iid_executer FOREIGN KEY (iid_executor)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT iid_user FOREIGN KEY (iid_user)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.appeal
    OWNER to postgres;

COMMENT ON TABLE public.appeal
    IS 'Обращение';


-- Table: public.incident

-- DROP TABLE IF EXISTS public.incident;

CREATE TABLE IF NOT EXISTS public.incident
(
    iid SERIAL PRIMARY KEY,
    title text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL
    --CONSTRAINT incident_pkey PRIMARY KEY (iid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.incident
    OWNER to postgres;

COMMENT ON TABLE public.incident
    IS 'Инцидент';


-- Table: public.order

-- DROP TABLE IF EXISTS public."order";

CREATE TABLE IF NOT EXISTS public."order"
(
    iid SERIAL PRIMARY KEY,
    iid_user bigint NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    iid_executor bigint NOT NULL,
    --CONSTRAINT order_pkey PRIMARY KEY (iid),
    CONSTRAINT iid_executor FOREIGN KEY (iid)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT iid_user FOREIGN KEY (iid_user)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public."order"
    OWNER to postgres;

COMMENT ON TABLE public."order"
    IS 'Заказ : специально для кадровых или иных служб, работающих с предметами, существующими в реале - заказ документов, справок, канцелярии и тд. Создается ответственными пользователями, должность или подразделение которых соответствует условию в системе';


-- Table: public.product

-- DROP TABLE IF EXISTS public.product;

CREATE TABLE IF NOT EXISTS public.product
(
    iid SERIAL PRIMARY KEY,
    short_title text COLLATE pg_catalog."default" NOT NULL,
    long_title text COLLATE pg_catalog."default",
    iid_manager bigint NOT NULL
    --CONSTRAINT iid PRIMARY KEY (iid)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.product
    OWNER to postgres;

COMMENT ON TABLE public.product
    IS 'Продукт : информация по продукту. в рамках него могут создаваться изменения. Продукт может создать только Администратор. К продукту привязан список рабочих групп, который может менять только Админ. Изменения сразу направляются на рабочую группу, которую выберет разработчик.';

-- Table: public.task

-- DROP TABLE IF EXISTS public.task;

CREATE TABLE IF NOT EXISTS public.task
(
    iid SERIAL PRIMARY KEY,
    iid_user bigint NOT NULL,
    title text COLLATE pg_catalog."default" NOT NULL,
    description text COLLATE pg_catalog."default" NOT NULL,
    iid_executor bigint NOT NULL,
    --CONSTRAINT task_pkey PRIMARY KEY (iid),
    CONSTRAINT iid_executor FOREIGN KEY (iid)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT iid_user FOREIGN KEY (iid_user)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.task
    OWNER to postgres;

COMMENT ON TABLE public.task
    IS 'Задача : вариант инцидента, не требующий получения обратной связи от пользователя. Создается автоматически Роботом или Администратором';

-- Table: public.workgroup

-- DROP TABLE IF EXISTS public.workgroup;

CREATE TABLE IF NOT EXISTS public.workgroup
(
    iid SERIAL PRIMARY KEY,
    short_title text COLLATE pg_catalog."default" NOT NULL,
    long_title text COLLATE pg_catalog."default",
    location text COLLATE pg_catalog."default" NOT NULL,
    iid_manager bigint NOT NULL,
    --CONSTRAINT workgroup_pkey PRIMARY KEY (iid),
    CONSTRAINT iid_manager FOREIGN KEY (iid_manager)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.workgroup
    OWNER to postgres;

COMMENT ON TABLE public.workgroup
    IS 'Рабочая группа, которая содержит множество исполнителей';


-- Table: public.alteration_to_product

-- DROP TABLE IF EXISTS public.alteration_to_product;

CREATE TABLE IF NOT EXISTS public.alteration_to_product
(
    iid_product bigint NOT NULL,
    iid_alteration bigint NOT NULL,
    CONSTRAINT alteration_to_product_pkey PRIMARY KEY (iid_product, iid_alteration),
    CONSTRAINT iid_alteration FOREIGN KEY (iid_alteration)
        REFERENCES public.alteration (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT iid_product FOREIGN KEY (iid_product)
        REFERENCES public.product (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.alteration_to_product
    OWNER to postgres;

COMMENT ON TABLE public.alteration_to_product
    IS 'В продукте может быть много изменений';


-- Table: public.incident_to_appeal

-- DROP TABLE IF EXISTS public.incident_to_appeal;

CREATE TABLE IF NOT EXISTS public.incident_to_appeal
(
    iid_appeal bigint NOT NULL,
    iid_incident bigint NOT NULL,
    CONSTRAINT incident_to_appeal_pkey PRIMARY KEY (iid_appeal, iid_incident),
    CONSTRAINT iid_appeal FOREIGN KEY (iid_appeal)
        REFERENCES public.appeal (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT iid_incident FOREIGN KEY (iid_incident)
        REFERENCES public.incident (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.incident_to_appeal
    OWNER to postgres;

COMMENT ON TABLE public.incident_to_appeal
    IS 'Множество инцидентов в одном обращении';

-- Table: public.user_to_workgroup

-- DROP TABLE IF EXISTS public.user_to_workgroup;

CREATE TABLE IF NOT EXISTS public.user_to_workgroup
(
    iid_workgroup bigint NOT NULL,
    iid_user bigint NOT NULL,
    CONSTRAINT user_to_workgroup_pkey PRIMARY KEY (iid_workgroup, iid_user),
    CONSTRAINT iid_user FOREIGN KEY (iid_user)
        REFERENCES public.portal_user (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT iid_workgroup FOREIGN KEY (iid_workgroup)
        REFERENCES public.workgroup (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.user_to_workgroup
    OWNER to postgres;

COMMENT ON TABLE public.user_to_workgroup
    IS 'В рабочей группе много исполнителей';


-- Table: public.workgroup_to_product

-- DROP TABLE IF EXISTS public.workgroup_to_product;

CREATE TABLE IF NOT EXISTS public.workgroup_to_product
(
    iid_workgroup bigint NOT NULL,
    iid_product bigint NOT NULL,
    CONSTRAINT workgroup_to_product_pkey PRIMARY KEY (iid_workgroup, iid_product),
    CONSTRAINT iid_product FOREIGN KEY (iid_product)
        REFERENCES public.product (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT iid_workgroup FOREIGN KEY (iid_workgroup)
        REFERENCES public.workgroup (iid) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.workgroup_to_product
    OWNER to postgres;

COMMENT ON TABLE public.workgroup_to_product
    IS 'Несколько рабочих групп в продукте';


-- INSERTING DATA TO CREATED TABLES

INSERT INTO public.user_role(
	iid, title, create_incident, direct_incident, create_alteration, create_task, create_order, create_appeal)
	VALUES 
(0,'Administrator',TRUE,TRUE,TRUE,TRUE,TRUE,TRUE),
(1,'User',FALSE,FALSE,FALSE,FALSE,FALSE,TRUE),
(2,'Executor',TRUE,FALSE,FALSE,FALSE,FALSE,TRUE),
(3,'Coordinator',TRUE,TRUE,FALSE,FALSE,FALSE,TRUE),
(4,'Developer',TRUE,FALSE,TRUE,FALSE,FALSE,TRUE),
(5,'Product Manager',TRUE,TRUE,TRUE,FALSE,FALSE,TRUE),
(6,'Robot',FALSE,FALSE,FALSE,TRUE,FALSE,FALSE);