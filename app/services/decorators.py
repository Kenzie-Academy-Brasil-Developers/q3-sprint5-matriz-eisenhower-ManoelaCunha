from flask import request
from functools import wraps
from http import HTTPStatus


def verify_values(func):
    @wraps(func)

    def value_is_valid():
        data = request.get_json()

        value_urgency = data.get('urgency')
        value_importance = data.get('importance')
        
        try:
            if 0 < value_importance < 3 and 0 < value_urgency < 3:  
                return func()
            else:
                raise ValueError

        except ValueError:
                return dict(
                    msg=dict(
                        valid_options=dict(importance=[1,2],urgency=[1,2]),
                        recieved_options=dict(importance=value_importance,urgency=value_urgency)
                        )
                    ), HTTPStatus.BAD_REQUEST

    return value_is_valid
