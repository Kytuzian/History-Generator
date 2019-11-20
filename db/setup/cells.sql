create table cells
(
    id integer primary key,
    type text,
    x integer,
    y integer,
    height real,
    temperature_multiplier real,
    moisture real,
    owner integer,
    building_capacity integer,
    high_temp_range real,
    low_temp_range real
);