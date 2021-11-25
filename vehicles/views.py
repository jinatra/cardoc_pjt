import re
import json
import requests

from django.http.response import JsonResponse
from django.views         import View
from django.db            import transaction

from users.models    import User
from users.decorator import login_decorator
from vehicles.models import Vehicle, FrontTire, RearTire
from vehicles.regex  import tire_validator

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

            if len(datas) > 5:
                return JsonResponse({'MESSAGE':'please request datas equal or less than 5'}, status=400)

            results = []

            for data in datas:
                user_email = data['id']
                trim_id    = data['trimId']

                if not User.objects.filter(email=user_email).exists():
                    return JsonResponse({'MESSAGE':f'non-existing user: {user_email}'}, status=404)

                user = User.objects.get(email=user_email)

                url = f'https://dev.mycar.cardoc.co.kr/v1/trim/{trim_id}'

                response     = requests.get(url).text
                results_dict = json.loads(response)

                model_name = results_dict['modelName']

                front_tire_format = results_dict['spec']['driving']['frontTire']['value']
                rear_tire_format  = results_dict['spec']['driving']['rearTire']['value']

                front_tire = Tire(front_tire_format)
                rear_tire  = Tire(rear_tire_format)

                if not tire_validator.match(str(front_tire_format)):
                    return JsonResponse({'MESSAGE':'invalid front tire spec format'}, status=400)

                if not tire_validator.match(str(rear_tire_format)):
                    return JsonResponse({'MESSAGE':'invalid rear tire spec format'}, status=400)

                with transaction.atomic():
                    front_tire_object, is_front_created = FrontTire.objects.select_for_update().get_or_create(
                        width=front_tire.width, aspect_ratio=front_tire.aspect_ratio, wheel_size=front_tire.wheel_size
                    )
                    if is_front_created:
                        pass
                    else:
                        pass

                with transaction.atomic():
                    rear_tire_object, is_rear_created = RearTire.objects.select_for_update().get_or_create(
                        width=rear_tire.width, aspect_ratio=rear_tire.aspect_ratio, wheel_size=rear_tire.wheel_size
                    )
                    if is_rear_created:
                        pass
                    else:
                        pass

                vehicle, is_vehicle_created = Vehicle.objects.get_or_create(
                    model_name    = model_name,
                    user_id       = user.id,
                    front_tire_id = front_tire_object.id,
                    rear_tire_id  = rear_tire_object.id
                )
                if is_vehicle_created:
                    vehicle_info = {
                        'model_name'      : vehicle.model_name,
                        'ownew_nickname'  : user.nickname,
                        'front_tire_info' : str(front_tire_format),
                        'rear_tire_info'  : str(rear_tire_format),
                    }
                else:
                    vehicle_info = {
                        'MESSAGE' : f'already registered vehicle for customer \'{user.nickname}\''
                    }

                results.append(vehicle_info)

            return JsonResponse({'MESSAGE' : results}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

    @login_decorator
    def get(self, request):
        try:
            data = json.loads(request.body)
            user_email = data['id']
            user       = request.user

            if not User.objects.filter(email=user_email).exists():
                return JsonResponse({'MESSAGE':f'non-existing user: {user_email}'}, status=404)

            vehicles = Vehicle.objects.filter(user_id=user.id)

            result = [
                {
                    'model_name'      : vehicle.model_name,
                    'front_tire_info' : f'{vehicle.front_tire.width}/{vehicle.front_tire.aspect_ratio}R{vehicle.front_tire.wheel_size}',
                    'rear_tire_info'  : f'{vehicle.rear_tire.width}/{vehicle.rear_tire.aspect_ratio}R{vehicle.rear_tire.wheel_size}',
                } for vehicle in vehicles
            ]

            return JsonResponse({'MESSAGE':result}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

