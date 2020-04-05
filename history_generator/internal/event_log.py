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
        d = {'id': self.parent.get_next_id('event'), 'name': name, 'event_data': data, 'date': date}
        new_event = Event.from_dict(d)

        self.events.append(new_event)

        self.update_event_log_box(new_event)

    def save(self, db):
        self.db = db
        for event in self.events:
            event.save(db)

    def load(self):
        self.events = []

        for event in self.db.query(EVENT_LOG_SELECT_SCRIPT, {}):
            self.events.append(Event.from_db(self.db, event['id']))

    def update_event_log_box(self, event):
        self.event_log_box.insert(END, event.text_version())

        if self.event_log_box.size() > utility.listbox_capacity(self.event_log_box):
            self.event_log_box.delete(0)

