# backend/apps/engine/utils/apifox_importer.py

import json
import logging
from typing import Dict, List, Any, Optional

from django.db import transaction
from apps.engine.models import TestInterface

logger = logging.getLogger(__name__)

class ApifoxImporter:
    """Apifox 接口导入器，支持将 Apifox 导出的接口数据转换为 TestInterface 模型"""
    
    def __init__(self):
        self.protocol_map = {
            "http": "HTTP",
            "https": "HTTP",
            "graphql": "GraphQL",
            "grpc": "gRPC",
            "dubbo": "DUBBO"
        }
        
        self.method_map = {
            "get": "GET",
            "post": "POST",
            "put": "PUT",
            "delete": "DELETE",
            "patch": "PATCH"
        }
    
    def import_from_json(self, json_data: Dict[str, Any]) -> List[TestInterface]:
        """
        从 Apifox 导出的 JSON 数据导入接口
        
        Args:
            json_data: Apifox 导出的 JSON 数据
            
        Returns:
            导入的 TestInterface 实例列表
        """
        imported_interfaces = []
        
        try:
            # 检查是否是 Apifox 导出的格式
            if "openapi" in json_data:
                # OpenAPI (Swagger) 格式
                return self._import_from_openapi(json_data)
            elif "api" in json_data:
                # Apifox 自定义格式
                return self._import_from_apifox_format(json_data)
            else:
                logger.error("不支持的导入格式")
                return []
        except Exception as e:
            logger.error(f"导入过程中发生错误: {str(e)}")
            return []
    
    def _import_from_openapi(self, openapi_data: Dict[str, Any]) -> List[TestInterface]:
        """从 OpenAPI (Swagger) 格式导入接口"""
        imported_interfaces = []
        
        try:
            # 获取 API 信息
            info = openapi_data.get("info", {})
            title = info.get("title", "未命名 API")
            
            # 获取服务器信息
            servers = openapi_data.get("servers", [])
            base_url = servers[0].get("url", "") if servers else ""
            
            # 处理路径
            paths = openapi_data.get("paths", {})
            for path, path_data in paths.items():
                for method, method_data in path_data.items():
                    if method.lower() not in self.method_map:
                        continue
                        
                    # 创建接口名称
                    operation_id = method_data.get("operationId", "")
                    summary = method_data.get("summary", "")
                    name = operation_id or summary or f"{method.upper()} {path}"
                    
                    # 创建接口描述
                    description = method_data.get("description", "")
                    
                    # 处理请求参数
                    parameters = method_data.get("parameters", [])
                    query_params = {}
                    headers = {}
                    
                    for param in parameters:
                        param_name = param.get("name", "")
                        param_in = param.get("in", "")
                        param_value = param.get("example", "")
                        
                        if param_in == "query":
                            query_params[param_name] = param_value
                        elif param_in == "header":
                            headers[param_name] = param_value
                    
                    # 处理请求体
                    body = {}
                    request_body = method_data.get("requestBody", {})
                    if request_body:
                        content = request_body.get("content", {})
                        if "application/json" in content:
                            schema = content["application/json"].get("schema", {})
                            body = schema.get("example", {})
                    
                    # 处理响应示例
                    response_example = {}
                    responses = method_data.get("responses", {})
                    if "200" in responses:
                        response_content = responses["200"].get("content", {})
                        if "application/json" in response_content:
                            schema = response_content["application/json"].get("schema", {})
                            response_example = schema.get("example", {})
                    
                    # 创建 TestInterface 实例
                    interface = TestInterface(
                        name=name,
                        description=description,
                        protocol="HTTP",
                        method=self.method_map.get(method.lower(), "GET"),
                        url=path,
                        headers=headers,
                        body=body,
                        query_params=query_params,
                        response_example=response_example
                    )
                    
                    imported_interfaces.append(interface)
            
            # 批量保存
            with transaction.atomic():
                for interface in imported_interfaces:
                    interface.save()
            
            return imported_interfaces
            
        except Exception as e:
            logger.error(f"从 OpenAPI 导入时发生错误: {str(e)}")
            return []
    
    def _import_from_apifox_format(self, apifox_data: Dict[str, Any]) -> List[TestInterface]:
        """从 Apifox 自定义格式导入接口"""
        imported_interfaces = []
        
        try:
            # 获取 API 列表
            apis = apifox_data.get("api", [])
            
            for api in apis:
                # 获取基本信息
                name = api.get("name", "未命名接口")
                description = api.get("description", "")
                
                # 获取请求信息
                method = api.get("method", "GET")
                path = api.get("path", "")
                
                # 获取请求头
                headers = {}
                for header in api.get("headers", []):
                    header_name = header.get("name", "")
                    header_value = header.get("value", "")
                    if header_name:
                        headers[header_name] = header_value
                
                # 获取查询参数
                query_params = {}
                for param in api.get("query", []):
                    param_name = param.get("name", "")
                    param_value = param.get("value", "")
                    if param_name:
                        query_params[param_name] = param_value
                
                # 获取请求体
                body = {}
                body_data = api.get("body", {})
                if body_data:
                    body_type = body_data.get("type", "")
                    if body_type == "json":
                        body = body_data.get("content", {})
                
                # 获取响应示例
                response_example = {}
                response_data = api.get("response", {})
                if response_data:
                    response_example = response_data.get("example", {})
                
                # 创建 TestInterface 实例
                interface = TestInterface(
                    name=name,
                    description=description,
                    protocol="HTTP",
                    method=self.method_map.get(method.lower(), "GET"),
                    url=path,
                    headers=headers,
                    body=body,
                    query_params=query_params,
                    response_example=response_example
                )
                
                imported_interfaces.append(interface)
            
            # 批量保存
            with transaction.atomic():
                for interface in imported_interfaces:
                    interface.save()
            
            return imported_interfaces
            
        except Exception as e:
            logger.error(f"从 Apifox 格式导入时发生错误: {str(e)}")
            return []
    
    def import_from_file(self, file_path: str) -> List[TestInterface]:
        """
        从文件导入接口
        
        Args:
            file_path: Apifox 导出的文件路径
            
        Returns:
            导入的 TestInterface 实例列表
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            return self.import_from_json(json_data)
        except Exception as e:
            logger.error(f"从文件导入时发生错误: {str(e)}")
            return []