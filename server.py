import os
import json
import enum
from typing import Annotated, Any
from pydantic import Field
from fastmcp import FastMCP, Context
import ifcopenshell
from ifcopenshell import entity_instance
from libs import success, fail


class IfcBy(enum.StrEnum):
    ByType = 'by_type'
    ById = 'by_id'
    ByGuid = 'by_guid'


def self_serializer(data):
    return json.dumps(data, ensure_ascii=False)


mcp = FastMCP(
    name='IFC MCP Server',
    instructions="""""",
    tags={'RAG', 'IFC'},
    port=18000,
    host='0.0.0.0',
    # tool_serializer=self_serializer
)


def get_ifc(ctx: Context):
    ifc = getattr(ctx.session, 'ifc', None)
    if ifc is None:
        return None, "IFC文件不存在！请重新设定。"
    return ifc, None


@mcp.prompt(
    name="prompt_set_ifc_file",
    description="""设定IFC文件路径"""
)
async def prompt_set_ifc_file(
        ifc_filename: Annotated[str, Field(description="IFC文件路径")]
):
    return f"设定IFC文件路径为: {ifc_filename}"


@mcp.tool(
    name="set_ifc_file",
    description="""设定IFC文件路径为: {ifc_filename}"""
)
async def set_ifc_file(
        ifc_filename: Annotated[str, Field(description="IFC文件路径")],
        ctx: Context
):
    if not os.path.exists(ifc_filename):
        return "IFC文件不存在！请重新设定。"
    ctx.session.ifc = ifcopenshell.open(ifc_filename)
    return f"设定成功！您可以继续其他任务。"


@mcp.tool(
    name="find_component_by_type",
    description="""通过IFC实体类型在IFC文件中查找构件。"""
)
async def find_component_by_type(
        entity_type: Annotated[str, Field(description="IFC实体类型")],
        ctx: Context
):
    ifc, msg = get_ifc(ctx=ctx)
    if ifc is None:
        return msg
    entities = ifc.by_type(entity_type)
    return success(data={
        'entities': entities
    })


@mcp.tool(
    name="find_component_by_id",
    description="""通过IFC实体唯一ID在IFC文件中查找构件。"""
)
async def find_component_by_id(
        entity_id: Annotated[int, Field(description="IFC实体唯一ID")],
        ctx: Context
):
    ifc, msg = get_ifc(ctx=ctx)
    if ifc is None:
        return msg
    entity = ifc.by_id(entity_id)
    return success(data={
        'entity': entity
    })


@mcp.tool(
    name="find_component_by_guid",
    description="""通过IFC实体全局ID在IFC文件中查找构件。"""
)
async def find_component_by_guid(
        entity_guid: Annotated[str, Field(description="IFC实体全局ID")],
        ctx: Context
):
    ifc, msg = get_ifc(ctx=ctx)
    if ifc is None:
        return msg
    entity = ifc.by_guid(entity_guid)
    return success(data={
        'entity': entity
    })


if __name__ == '__main__':
    mcp.run(transport='streamable-http')
