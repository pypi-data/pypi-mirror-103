import json
from typing import List, Union
from requests import request, Response
from ovomaltino.datatype.social_fact_type import SocialFactType


class Database():

    def __init__(self, url, endpoint):
        self.endpoint = f'{url}{endpoint}'

    def get(self, filters: dict = {}, fields: str = '', sort: str = '',
            offset: int = -1, limit: int = -1) -> Response:
        """
        Get objects in a collection
        :param filters: `{<str>:<value>,<str>:<value>}` all filters to find the objects
        :param fields: `<str>,<str>` all fields to take
        :param sort: `<campo>:<asc | desc>` how to order the objects
        :param offset: `int` index to start to get the objects
        :param limit: `int` how many objects get from offset
        :return: `Response` response
        """

        def complete_url(splits: List[str], validations: List[bool],
                         nValidations: int, res='') -> Union[str, bool]:

            if len(splits) == len(validations):

                if nValidations > 0:

                    index = nValidations - 1

                    if validations[index] == True:
                        return complete_url(splits, validations,
                                            index, str(res + splits[index]))
                    else:
                        return complete_url(splits, validations, index, res)
                else:
                    return res

            else:
                return False

        params: list = [f'&fields={fields}',
                        f'&sort={sort}',
                        f'&offset={str(offset)}&limit={str(limit)}']

        validations: list = [fields != '',
                             sort != '',
                             offset != -1 and limit != -1]

        url: Union[str, bool] = complete_url(params, validations, len(params),
                                             f'{self.endpoint}?filters={json.dumps(filters)}')

        if type(url) == str:

            response: Response = request('GET', url)

            if response.status_code is 200:
                return response
            else:
                raise SystemError

        else:
            raise SystemError

    def create(self, obj: Union[SocialFactType]) -> Response:
        """
        Insert a object in a collection
        :param obj: `list` List of objects
        :return: `Response` response
        """

        head = {'Content-Type': 'application/json',
                'cache-control': 'no-cache'}

        response: Response = request('POST', self.endpoint,
                                     data=json.dumps(obj),
                                     headers=head)

        if response.status_code is 200:
            return response
        else:
            raise SystemError

    def update(self, object_id: str, obj: Union[SocialFactType]) -> Response:
        """
        Update a object in a collection
        :param object_id: `str` ObjectId
        :param obj: `dict` Object
        :return: `dict` lastest object version
        """

        head = {'Content-Type': 'application/json',
                'cache-control': 'no-cache'}

        response: Response = request('PUT', f'{self.endpoint}/{str(object_id)}',
                                     data=json.dumps(obj), headers=head)

        if response.status_code is 200:
            return response
        else:
            raise SystemError

    def delete(self, object_id: str) -> Response:
        """
        Delete a object in a collection
        :param object_id: `str` ObjectId
        :return: `dict` lastest object version
        """

        head = {'Content-Type': 'application/json',
                'cache-control': 'no-cache'}

        response: Response = request('DELETE',
                                     f'{self.endpoint}{str(object_id)}',
                                     headers=head)

        if response.status_code is 200:
            return response
        else:
            raise SystemError
