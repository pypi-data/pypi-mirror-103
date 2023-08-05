import click

from . import context
from .input_helpers import get_org_from_input_or_ctx
from .output.table import (
    format_table,
    metadata_column,
    spec_column,
    status_column,
)
import agilicus

resource_type_enum = click.Choice(
    ["application_service", "fileshare", "application", "service_forwarder"]
)


def query_permissions(ctx, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    query_results = apiclient.permissions_api.list_resource_permissions(
        org_id=org_id, **kwargs
    )
    if query_results:
        return query_results.resource_permissions
    return []


def format_permissions(ctx, roles):
    columns = [
        metadata_column("id"),
        spec_column("resource_type", "type"),
        spec_column("user_id", "user id"),
        spec_column("org_id", "org id"),
        spec_column("resource_id", "resource id"),
        spec_column("resource_role_name", "role"),
    ]
    return format_table(ctx, roles, columns)


def add_permission(
    ctx, user_id, resource_id, resource_type, resource_role_name, org_id=None
):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    spec = agilicus.ResourcePermissionSpec(
        org_id=org_id,
        user_id=user_id,
        resource_type=resource_type,
        resource_role_name=resource_role_name,
        resource_id=resource_id,
    )
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    return apiclient.permissions_api.create_resource_permission(
        agilicus.ResourcePermission(spec=spec)
    ).to_dict()


def delete_permission(ctx, id, org_id=None):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    return apiclient.permissions_api.delete_resource_permission(id, org_id=org_id)


def query_resources(ctx, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    query_results = apiclient.resources_api.list_resources(org_id=org_id, **kwargs)
    if query_results:
        return query_results.resources
    return []


def format_resources(ctx, resources):
    columns = [
        metadata_column("id"),
        spec_column("org_id", "org id"),
        spec_column("resource_type", "type"),
        spec_column("name", "name"),
        status_column("resource_stats.overall_status", "status", optional=True),
        status_column(
            "resource_stats.last_warning_message", "last_warning", optional=True
        ),
        status_column(
            "resource_stats.session_stats.total", "good_sessions", optional=True
        ),
        status_column(
            "resource_stats.session_stats.failed", "failed_sessions", optional=True
        ),
    ]
    return format_table(ctx, resources, columns)


def query_roles(ctx, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    query_results = apiclient.permissions_api.list_resource_roles(
        org_id=org_id, **kwargs
    )
    return query_results.resource_roles


def format_roles(ctx, roles):
    columns = [
        spec_column("resource_type", "type"),
        spec_column("role_name", "name"),
    ]
    return format_table(ctx, roles, columns)
