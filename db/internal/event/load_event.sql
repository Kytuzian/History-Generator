select e.id as event_id,
       e.event_date,
       et.name as event_type,
       ed.field_name,
       ed.field_value
from events as e
inner join event_types as et on e.event_type_id = et.id
inner join event_data as ed on e.id = ed.event_id
where e.id = :event_id;
