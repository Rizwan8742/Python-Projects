 for i in json:
                    if i['country'] == 'IN':
                        self.latitude = round(i['latitude'],2)  
                        self.longitude = round(i['longitude'],2)
                 