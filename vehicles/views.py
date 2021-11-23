import re
import json
from django.db.models.fields import NullBooleanField
import requests

from django.http.response import JsonResponse
from django.views         import View

from vehicles.models import Vehicle, FrontTire, RearTire
from users.models    import User

class Tire:
    def __init__(self, tire_type):
        tire_info         = re.split('/|R', tire_type)
        self.width        = tire_info[0]
        self.aspect_ratio = tire_info[1]
        self.wheel_size   = tire_info[2]

class TireView(View):
    def post(self, request):
        try:
            datas = json.loads(request.body)

            for data in datas:
                user_email = data['id']
                trim_id    = data['trimId']

                user = User.objects.filter(email = user_email)

                if not user.exists():
                    return JsonResponse({'MESSAGE':'non-existing user'}, status=404)

                url = f'https://dev.mycar.cardoc.co.kr/v1/trim/{trim_id}'

                response = requests.get(url).text
                results_dict = json.loads(response)

                model_name = results_dict['modelName']

                front_tire = Tire(results_dict['spec']['driving']['frontTire']['value'])
                rear_tire  = Tire(results_dict['spec']['driving']['rearTire']['value'])

                

                return JsonResponse({'MESSAGE1' : rear_tire.width}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

