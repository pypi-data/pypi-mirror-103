from dataclasses import dataclass, field
from dataclasses_json import dataclass_json, LetterCase, Undefined, config
from dataclasses_json import CatchAll, undefined
from typing import Any, Callable, List, Dict
from urllib import parse

from ..base_client import BaseClient

@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FlowNodeInstancesQuery:
    limit: int = None
    offset: int = None
    flow_node_instance_id: str = None
    flow_node_id: str = None
    flow_node_name: str = None
    flow_node_lane: str = None
    flow_node_type: str = None
    event_type: str = None
    correlation_id: str = None
    process_definition_id: str = None
    process_model_id: str = None
    process_instance_id: str = None
    owner_id: str = None
    state: str = None
    previous_flow_node_instance_id: str = None
    parent_process_instance_id: str = None


@dataclass_json(letter_case=LetterCase.CAMEL, undefined=Undefined.INCLUDE)
@dataclass
class FlowNodeInstanceResponse:
    flow_node_instance_id: str = None
    flow_node_id: str = None
    flow_node_name: str = None
    flow_node_lane: str = None
    flow_node_type: str = None
    event_type: str = None
    previous_flow_node_instance_id: str = None
    parent_process_instance_id: str = None
    state: str = None
    process_definition_id: str = None
    process_model_id: str = None
    process_instance_id: str = None
    correlation_id: str = None
    tokens: List[Dict[str, Any]] = field(default_factory=list)
    owner_id: str = None
    error: Dict[str, Any] = field(default_factory=dict)
    meta_info: List[Dict[str, Any]] = field(default_factory=list)
    place_holder: CatchAll = None
    
class FlowNodeInstanceHandler(BaseClient):

    def __init__(self, url: str, identity: Callable=None):
        super(FlowNodeInstanceHandler, self).__init__(url, identity)

    def get_flow_node_instances(self, query: FlowNodeInstancesQuery, options: dict={}) -> FlowNodeInstanceResponse:

        query_dict = query.to_dict() 

        filtered_query = list(filter(lambda dict_entry: dict_entry[1] is not None, query_dict.items()))

        query_str = parse.urlencode(filtered_query, doseq=False)

        path = f"/atlas_engine/api/v1/flow_node_instances?{query_str}"

        response_list_of_dict = self.do_get(path, options)

        if response_list_of_dict.get('totalCount', 0) > 0:
            json_data = response_list_of_dict['flowNodeInstances']
            response = FlowNodeInstanceResponse.schema().load(json_data, many=True)
        else:
            response = []

        return response
