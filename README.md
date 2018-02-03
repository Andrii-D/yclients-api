# YClients API on Python
This is __unofficial__ YClients API on Python based on official [documentation](https://yclients.docs.apiary.io/)

# Usage examples

```
from yclients import YClientsAPI

api = YClientsAPI(token='your-token', company_id='company id', form_id='form id')



all_staff = api.get_staff()

print all_staff

staff_d = all_staff[0].get('id')

services = api.get_services(staff_id=staff_id)
print services

service_id = services[0].get('id')

booking_days = api.get_available_days(staff_id=staff_id, service_id=service_id):
print booking_days

day = booking_days[0]

time_slots = api.get_available_times(staff_id=staff_id, service_id=service_id, day=day)
print time_slots

date_time = time_slots[0].get('datetime')

booked, message = api.book(booking_id=0, 
                           fullname='my name', 
                           phone='53425345', 
                           email='myemail@email.com, 
                           service_id=service_id, 
                           date_time=date_time, 
                           staff_id=staff_id, 
                           comment='some comment')
```
