from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, Undefined, config
#from dataclasses_json import CatchAll, undefined
from typing import Any, Callable, List, Dict
from urllib import parse

from ..base_client import BaseClient

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FormFields:
    id: str
    type: str
    label: str
    default_value: str

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class UserTaskConfig:
    form_fields: List[FormFields]
    custom_form: str = 'DynamicForm' 

@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.EXCLUDE)
#@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.INCLUDE)
@dataclass
class UserTaskResponse:
    user_task_instance_id: str = field(metadata=config(field_name="flowNodeInstanceId"))
    user_task_config: UserTaskConfig
    owner_id: str
    correlation_id: str
    process_instance_id: str
    process_model_id: str
    flow_node_name: str
    actual_owner_id: str = None
    #place_holder: CatchAll

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class ReserveUserTaskRequest:
    actual_owner_id: str
    
class UserTaskHandler(BaseClient):

    BPMN_TYPE = 'bpmn:UserTask'

    def __init__(self, url: str, identity: Callable=None):
        super(UserTaskHandler, self).__init__(url, identity)

    def get_user_tasks(self, state: str='suspended', offset: int=None, limit: int=None, options: dict={}) -> UserTaskResponse:

        query = {
            'flowNodeType': UserTaskHandler.BPMN_TYPE,
            'state': state,
            'offset': offset,
            'limit': limit,
        }

        query_str = parse.urlencode(query, doseq=False)

        path = f"/atlas_engine/api/v1/flow_node_instances?{query_str}"

        response_list_of_dict = self.do_get(path, options)

        if response_list_of_dict.get('totalCount', 0) > 0:
            json_data = response_list_of_dict['flowNodeInstances']
            response = UserTaskResponse.schema().load(json_data, many=True)
        else:
            response = []

        return response

    def reserve_user_task(self, user_task_instance_id: str, request: ReserveUserTaskRequest, options: dict={}):
        path = f"/atlas_engine/api/v1/user_tasks/{user_task_instance_id}/reserve"

        payload = request.to_dict()

        _ = self.do_put(path, payload, options)

        return True

    def finish_user_task(self, user_task_instance_id: str, request: Dict[str, Any], options: dict={}):
        path = f"/atlas_engine/api/v1/user_tasks/{user_task_instance_id}/finish"

        _ = self.do_put(path, request, options)

        return True

    def cancel_reservation(self, user_task_instance_id: str, options: dict={}):
        path = f"/atlas_engine/api/v1/user_tasks/{user_task_instance_id}/cancel-reservation"

        _ = self.do_delete(path, options)

        return True
