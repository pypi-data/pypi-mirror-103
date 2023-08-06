from typing import Dict, Any, Tuple, List

from vtb_authorizer_utils.data_objects import ResourceService, ResourceType, ResourceRule
from vtb_authorizer_utils.gateway import AuthorizerGateway


async def import_service_from_dict(gateway: AuthorizerGateway,
                                   cfg: Dict[str, Any]) -> \
        Tuple[ResourceService, List[ResourceType], List[ResourceRule]]:
    """ Загрузка конфигурации сервиса в авторайзер """
    service = await _create_or_update_service(gateway, cfg)
    resource_types_cfg = cfg.get('resource_types', [])
    resource_types = []
    for resource_type_cfg in resource_types_cfg:
        resource_type = await _create_or_update_resource_type(gateway, service, resource_type_cfg)
        resource_types.append(resource_type)

    resource_rules_cfg = cfg.get('resource_rules', [])
    resource_rules = await gateway.bulk_update_resource_rules(service.name, resource_rules_cfg)

    return service, resource_types, resource_rules


async def _create_or_update_resource_type(gateway: AuthorizerGateway,
                                          service: ResourceService,
                                          cfg: Dict[str, Any]) -> ResourceType:
    name = cfg['name']
    title = cfg.get('title', '')
    description = cfg.get('description', '')
    actions = cfg.get('actions', '')

    resource_type = await gateway.get_resource_type(name)
    if resource_type:
        return await gateway.update_resource_type(f'{service.name}:{name}',
                                                  title=title,
                                                  description=description,
                                                  actions=actions)
    else:
        return await gateway.create_resource_type(resource_service=service.name,
                                                  title=title,
                                                  name=name,
                                                  description=description,
                                                  actions=actions)


async def _create_or_update_service(gateway: AuthorizerGateway, cfg: Dict[str, Any]) -> ResourceService:
    name = cfg['name']
    title = cfg['title']
    url = cfg['url']
    description = cfg.get('description', '')

    service = await gateway.get_resource_service(name)
    if service:
        return await gateway.update_resource_service(name,
                                                     title=title,
                                                     description=description,
                                                     url=url)
    else:
        return await gateway.create_resource_service(name=name,
                                                     title=title,
                                                     description=description,
                                                     url=url)
