# coding=utf-8
import json
import requests


class YClientsAPI:

    def __init__(self, token, company_id, form_id, language='ua-UA'):
        self.company_id = company_id
        self.form_id = form_id
        self.headers = {
            'Accept-Language': language,
            'Authorization': "Bearer {}".format(token),
            'Cache-Control': "no-cache"
        }

    def book(self, booking_id, fullname, phone, email, service_id, date_time, staff_id=None, comment=None):
        """ Make booking """
        url = "https://n{}.yclients.com/api/v1/book_record/{}/".format(self.form_id, self.company_id)

        payload = {
            "phone": phone,
            "email": email,
            "fullname": fullname,
            "appointments": [{
                "id": booking_id,
                "services": [int(service_id)],
                "staff_id": int(staff_id or 0),
                "events":[],
                "datetime": date_time,
                "chargeStatus": "",
                "comment": comment or ''

            }]
        }
        response = requests.request("POST", url, data=json.dumps(payload), headers=self.headers)
        res = json.loads(response.text)

        if isinstance(res, dict) and res.get('errors'):
            return False, res.get('errors', {}).get('message', '')
        return True, ''

    def get_staff_info(self, staff_id):
        """ Return dict with info about specific staff"""
        url = "https://n{}.yclients.com/api/v1/staff/{}/{}".format(self.form_id, self.company_id, staff_id)
        response = requests.request("GET", url, headers=self.headers)
        return json.loads(response.text)

    def get_service_info(self, service_id):
        """ Return dict with info about specific service"""
        url = "https://n{}.yclients.com/api/v1/services/{}/{}".format(self.form_id, self.company_id, service_id)
        response = requests.request("GET", url, headers=self.headers)
        return json.loads(response.text)

    def get_staff(self, service_id=None, date_time=None):
        """ Return list of staff for specific service and date"""
        url = "https://n{}.yclients.com/api/v1/book_staff/{}".format(self.form_id, self.company_id)
        querystring = {"service_ids[]": int(service_id)} if service_id else {}
        querystring.update({"datetime": date_time} if date_time else {})
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return json.loads(response.text)

    def get_services(self, staff_id=None, date_time=None):
        """ Return list of services for specific staff and date"""
        url = "https://n{}.yclients.com/api/v1/book_services/{}".format(self.form_id, self.company_id)
        querystring = {"staff_id": int(staff_id)} if staff_id else {}
        querystring.update({"datetime": date_time} if date_time else {})
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return json.loads(response.text)

    def get_available_days(self, staff_id=None, service_id=None):
        """ Return all available days for specific staff and service"""
        url = "https://n{}.yclients.com/api/v1/book_dates/{}".format(self.form_id, self.company_id)
        querystring = {"staff_id": int(staff_id)} if staff_id else {}
        querystring.update({"service_ids[]": service_id} if service_id else {})
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return json.loads(response.text).get('booking_dates')

    def get_available_times(self, staff_id, service_id=None, day=None):
        """ Return all available time slots on specific day staff and service"""
        url = "https://n{}.yclients.com/api/v1/book_times/{}/{}/{}".format(self.form_id, self.company_id, staff_id, day)
        querystring = {}
        if service_id:
            querystring.update({"service_ids[]": service_id})
        response = requests.request("GET", url, headers=self.headers, params=querystring)
        return json.loads(response.text)
