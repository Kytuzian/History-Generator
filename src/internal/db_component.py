class DBComponent:
    def __init__(self, component_id, save_script, load_script):
        self.component_id = component_id
        self.save_script = save_script
        self.load_script = load_script

    def save(self):
        pass

    def load(self):
        pass
