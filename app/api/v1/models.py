
incident_list = []

class IncidentModel():

    def __init__(self):
        self.incidences = incident_list

    def all(self):
        return self.incidences

    def save(self, data):
        
        data['id'] = self.__generate_user_id()

        self.incidences.append(data)

    
    def find(self, id):

        for incident in self.incidences:
            if incident['id'] == id:
                return incident
        
        return None

    def delete(self, id):
        incident = self.find(id)

        if not incident:
            return False
        else:
            self.incidences.remove(incident)
            return True

    def __generate_user_id(self):
        
        if len(self.incidences):
            return self.incidences[-1]['id'] + 1
        else:
            return 1