import requests
import json
import settings
import datetime
import time

class AVObject(object):
    base = r'https://leancloud.cn' #cn.avoscloud.com
    # The operation about class
    # - create class obj: /1.1/classes/<className>            [POST]
    # - get class obj   : /1.1/classes/<className>/<objectId> [GET]
    # - update class obj: /1.1/classes/<className>/<objectId> [PUT]
    # - query class obj : /1.1/classes/<className>            [GET]
    # - delete class obj: /1.1/classes/<className>/<objectId> [DELETE]
    base_classes = base+r'/1.1/classes/'
    base_cql = base+r'/1.1/cloudQuery'
    # The operation about users in IM system
    # - Here we have not use this func
    Users = base+r'/1.1/users'
    # Useless
    base_patch = base+r'/1.1/batch'
    app_settings = [settings.avos_app_id, settings.avos_app_key]

    def __init__(self):
        pass

    # --- PRIVATE METHOD ---
    @classmethod
    def headers(cls):
        # Since properties only work on instances, need define headers property in meta class
        return {
            "X-AVOSCloud-Application-Id": cls.app_settings[0],
            "X-AVOSCloud-Application-Key": cls.app_settings[1],
            "Content-Type": "application/json"
        }

    @classmethod
    def _save_to_avos(cls, cls_name, data):
        # get_url = "http://httpbin.org/post"
        if type(data) == list:
            # save many object
            patch_ob_list = [{"method": "POST",
                              "path": "/1.1/classes/"+cls_name,
                              "body": ob} for ob in data]
            return AVObject._patch_avos(
                patch_ob_list
            )
        else:
            # save single object
            return requests.post(
                # get_url,
                AVObject.base_classes+cls_name,
                data=json.dumps(data),
                headers=cls.headers(),
                verify=False
            )

    @classmethod
    def _get_avos(cls, cls_name, ob_id=None, **kwargs):
        get_url = AVObject.base_classes+cls_name
        get_url = get_url + '/' + ob_id if ob_id else get_url
        # get_url = "http://httpbin.org/get"

        with_params = {}
        # Extract the condition from kwargs
        # kpara = include, where, limit, order
        for kparam, vparam in kwargs.items():
            # Transfer vparam from json to string
            # And store the string as value, kparam as key into dict named with_params
            # with_params[kparam] = json.dumps(vparam)
            if type(vparam) in [str, unicode]:
                with_params[kparam] = vparam
            else:
                with_params[kparam] = json.dumps(vparam)

        return requests.get(
            get_url,
            headers=cls.headers(),
            params=with_params,
            verify=False
        )

    @classmethod
    def _update_avos(cls, cls_name, data, plus_ob={}):
        if type(data) == list:
            # update many object
            patch_ob_list = [{"method": "PUT",
                              "path": "/1.1/classes/"+cls_name+"/"+ob['objectId'],
                              "body": ob} for ob in data]
            return AVObject._patch_avos(
                patch_ob_list
            )

        elif type(data) == dict or type(data) == str:
            ob_id = data['objectId'] if type(data) == dict else data

            # check plus_ob
            if type(plus_ob) != dict:
                return None

            put_url = AVObject.base_classes + cls_name + '/' + ob_id
            return requests.put(
                put_url,
                data=json.dumps(plus_ob),
                headers=cls.headers(),
                verify=False
            )
        else:
            return None

    @classmethod
    def _remove_avos(cls, cls_name, data):
        if type(data) == list:
            # remove many objects
            patch_ob_list = [{"method": "DELETE",
                              "path": "/1.1/classes/"+cls_name+"/"+ob['objectId']}
                             for ob in data]
            return AVObject._patch_avos(
                patch_ob_list
            )
        elif type(data) == dict or type(data) == str:
            # remove single object
            ob_id = data['objectId'] if type(data) == dict else data
            remove_url = AVObject.base_classes + cls_name + '/' + ob_id
            return requests.delete(
                remove_url,
                headers=cls.headers(),
                verify=False
            )
        else:
            return None

    # Post a list of data to leancloud.
    @classmethod
    def _patch_avos(cls, patch_ob_list):
        return requests.post(
            AVObject.base_patch,
            data=json.dumps({'requests': patch_ob_list}),
            headers=cls.headers(),
            verify=False
        )

    # --- PUBLIC METHOD ---
    @staticmethod
    def pointer(ob, cls_name):
        if type(ob) == dict and ob.get('objectId', None) \
                and type(cls_name) == str:
            pt_ob = {
                "__type": "Pointer",
                "className": cls_name,
                "objectId": ob['objectId']
            }
            return pt_ob
        else:
            return None

    @staticmethod
    def in_query(where_ob, cls_name):
        if type(where_ob) == dict and type(cls_name) == str:
            in_query_ob = {"$inQuery": {"where": where_ob, "className": cls_name}}
            return in_query_ob
        else:
            return None

    @staticmethod
    def re_pointer(ob, cls_name, key_pt):
        if type(ob) == dict and type(cls_name) == str:
            return {
                "$relatedTo": {
                    "object": {
                        "__type": "Pointer",
                        "className": cls_name,
                        "objectId": ob['objectId']
                    },
                    "key": key_pt
                }
            }

    @staticmethod
    def or_query(where_ob_list):
        # `where={"$or":[{"wins":{"$gt":150}},{"wins":{"$lt":5}}]}`
        return {"$or": where_ob_list}

    # --- CLASS METHOD ---
    @classmethod
    def save(cls, ob):
        """
        Save single object `ob` to `/classes/cls`
        :param ob:
        :return:
            `response` like { "createdAt": "...", "objectId": "..."}
        """
        return cls._save_to_avos(cls.__name__, ob)

    @classmethod
    def get(cls, ob_id=None, **kwargs):
        """
        :param ob_id:
            if None, get list of objects
            if ob_id is an object, automatically extract proper ob_id #todo
        :param kwargs:
            `include=post, post.author` result including a complete relation object
            `where=` filters
            `order=score,-name` descended order
            `limit=` limit default to 100, max to 1000
            `skip=N` skip first N result
            `count=1`  return `{"results": [], "count": 1337 }`
            `keys=score,playerName` only return fields
            `where={"arrayKey":2}` array contains value 2
            `where={"arrayKey":{"$all":[2,3,4]}}` matches all
            `where={"field_common": AVObject.pointer(ob, cls_name) }` pointer: point to
            `where={"field_common": AVObject.in_query(where_ob, cls_name) }` inQuery
            `where= AVObject.re_pointer(ob, cls_name, field_likes_arr)` reverse pointer: point from
            'where= AVObject.or_query(where_ob_list)
        :return:
            `RESPONSE.content.results` : list of results
        """
        return cls._get_avos(cls.__name__, ob_id, **kwargs)

    @classmethod
    def update(cls, ob, plus_ob):
        """
        Update single object
        :param ob: Object or list of objects containing `objectId` attribute
        :param plus_ob: -d json.dumps(plus_ob)
                        -d '{"score":73453}' \
                        -d '{"opponents":{"__op":"Delete"}}' \
                        -d '{"score":{"__op":"Increment","amount":1}}' \
                        -d '{"skills":{"__op":"AddUnique/ Add/ Remove","objects":["flying","kungfu"]}}' \
                        -d '{"opponents":{
                                "__op":"AddRelation/ RemoveRelation",
                                "objects":[{"__type":"Pointer","className":"Player","objectId":"51b0f0e851c16221"}]}
                            }' \
        :return: {"updatedAt":"...","objectId":"..."}
        """
        return cls._update_avos(cls.__name__, ob, plus_ob)

    @classmethod
    def remove(cls, ob):
        """
        Remove object from '/classes/cls'
        :param ob: Object or ob_id
        :return:
        """
        return cls._remove_avos(cls.__name__, ob)

    @classmethod
    def patch(cls, patch_ob_list):
        """
        Raw patch function. See also `save_all`, `update_all`, and `remove_all`
        :param patch_ob_list: Posted as `{"requests":patch_ob_list}`
        :return: List of separate response object containing `success` or `error` attr
        """
        return cls._patch_avos(patch_ob_list)

    @classmethod
    def save_all(cls, ob_list):
        return cls._save_to_avos(cls.__name__, ob_list)

    @classmethod
    def update_all(cls, ob_list):
        return cls._update_avos(cls.__name__, ob_list)

    @classmethod
    def remove_all(cls, ob_list):
        """
        :param ob_list:
        :return: return list of response object containing status `[{"success":{}}]`
        """
        return cls._remove_avos(cls.__name__, ob_list)



    # --- By Woodie ---
    # The following method used to generate the data,
    # which type is defined in LeanCloud.
    @classmethod
    def Date(cls, on_this=None):
        # Get the current time.
        now = datetime.datetime.now()
        # setting time is current time.
        if on_this is None:
            setting_datetime = now
        # setting time is the beginning of this (day/week/month/year).
        elif on_this is 0: # Day
            setting_datetime = now.replace(hour=0, minute=0, second=0, microsecond=1)
        elif on_this is 1: # Week
            delta = datetime.timedelta(now.weekday())
            setting_datetime = now - delta
            setting_datetime = setting_datetime.replace(hour=0, minute=0, second=0, microsecond=1)
        elif on_this is 2: # Month
            setting_datetime = now.replace(day=1, hour=0, minute=0, second=0, microsecond=1)
        elif on_this is 3: # Year
            setting_datetime = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=1)
        # Generate LeanCloud's date
        _date = {
            "__type": "Date",
            "iso":    (setting_datetime.isoformat())[0:-3]+"Z"
        }
        return _date

    @classmethod
    def Pointer(cls, obId):
        _pointer = {
            "__type":    "Pointer",
            "className": "UserInfo",
            "objectId":  obId
        }
        return _pointer

    @classmethod
    def iso2timestamp(cls, iso_time): #avos date type {u'__type': u'Date', u'iso': u'2015-05-23T11:15:00.000Z'}
        t = time.strptime(iso_time, "%Y-%m-%dT%H:%M:%S.000Z")
        return long(time.mktime(t))