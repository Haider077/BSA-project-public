
#class event 

class Event():
    def __init__(self, id, name, description):
        self.id = id 
        self.name = name
        self.description = description
       
    # getters
    def get_event_id(self): 
        return self.id

    def get_event_name(self):
        return self.name

    def get_event_description(self):
        return self.description

    def get_event_date(self):
        return self.date

    # setters 
    def set_event_id(self, id): 
        self.id = id

    def set_event_name(self, name):
        self.name = name

    def set_event_description(self, description):
        self.description = description

    def set_event_date(self, date): 
        self.date = date
