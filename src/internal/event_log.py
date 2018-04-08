from Tkconstants import END

from internal import utility
from internal.events import Event

EVENT_LOG_SELECT_SCRIPT = 'db/internal/event/load_event_ids.sql'


class EventLog:
    def __init__(self, parent, db, event_log_box):
        self.parent = parent
        self.db = db
        self.event_log_box = event_log_box

        self.events = []

    def add_event(self, name, data, date):
        dict = {'id': self.parent.get_next_id('event'), 'name': name, 'event_data': data, 'date': date}

        self.events.append(Event.from_dict(dict))

        # self.update_event_log_box(event)

    def save(self, db):
        self.db = db
        map(self.write_to_db, self.events)

    def load(self):
        for event in self.db.query(EVENT_LOG_SELECT_SCRIPT, {}):
            Event.from_db(self.db, event['id'])

    def write_to_db(self, event):
        if self.db is not None:
            event.save(self.db)

    def update_event_log_box(self, event):
        self.event_log_box.insert(END, event.text_version())

        if self.event_log_box.size() > utility.listbox_capacity(self.event_log_box):
            self.event_log_box.delete(0)
