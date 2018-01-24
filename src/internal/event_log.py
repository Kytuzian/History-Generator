from Tkconstants import END

from internal import utility

GEN_LOG_INSERT_SCRIPT = "db/gen_log_insert.sql"


class EventLog:
    def __init__(self, parent, db, event_log_box):
        self.parent = parent
        self.db = db
        self.event_log_box = event_log_box

        self.events = []

    def add_event(self, event):
        self.events.append(event)

        # self.update_event_log_box(event)

    def save(self):
        map(self.write_to_db, self.events)

    def write_to_db(self, event):
        if self.db is not None:
            self.db.execute(GEN_LOG_INSERT_SCRIPT, {'date': self.parent.get_real_date(), 'message': event.text_version()})

    def update_event_log_box(self, event):
        self.event_log_box.insert(END, event.text_version())

        if self.event_log_box.size() > utility.listbox_capacity(self.event_log_box):
            self.event_log_box.delete(0)
