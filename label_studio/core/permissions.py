"""This file and its contents are licensed under the Apache License 2.0. Please see the included NOTICE for copyright information and LICENSE for a copy of the license.
"""
import logging   # noqa: I001
from typing import Optional

from pydantic import BaseModel

import rules

logger = logging.getLogger(__name__)


# Define a custom predicate
@rules.predicate
def is_veg3_admin(user):
    return user.is_authenticated and user.email.endswith('@veg3.ai')

# Apply the custom rule to delete permissions
admin_permissions = [
    'annotations.delete',
    'labels.delete',
    'models.delete',
    'model_provider_connection.delete',
    'projects.delete',
    'projects.create',
]

class AllPermissions(BaseModel):
    organizations_create = 'organizations.create'
    organizations_view = 'organizations.view'
    organizations_change = 'organizations.change'
    organizations_delete = 'organizations.delete'
    organizations_invite = 'organizations.invite'
    projects_create = 'projects.create'
    projects_view = 'projects.view'
    projects_change = 'projects.change'
    projects_delete = 'projects.delete'
    tasks_create = 'tasks.create'
    tasks_view = 'tasks.view'
    tasks_change = 'tasks.change'
    tasks_delete = 'tasks.delete'
    annotations_create = 'annotations.create'
    annotations_view = 'annotations.view'
    annotations_change = 'annotations.change'
    annotations_delete = 'annotations.delete'
    actions_perform = 'actions.perform'
    predictions_any = 'predictions.any'
    avatar_any = 'avatar.any'
    labels_create = 'labels.create'
    labels_view = 'labels.view'
    labels_change = 'labels.change'
    labels_delete = 'labels.delete'
    models_create = 'models.create'
    models_view = 'models.view'
    models_change = 'models.change'
    models_delete = 'models.delete'
    model_provider_connection_create = 'model_provider_connection.create'
    model_provider_connection_view = 'model_provider_connection.view'
    model_provider_connection_change = 'model_provider_connection.change'
    model_provider_connection_delete = 'model_provider_connection.delete'


all_permissions = AllPermissions()


class ViewClassPermission(BaseModel):
    GET: Optional[str] = None
    PATCH: Optional[str] = None
    PUT: Optional[str] = None
    DELETE: Optional[str] = None
    POST: Optional[str] = None


def make_perm(name, pred, overwrite=False):
    if rules.perm_exists(name):
        if overwrite:
            rules.remove_perm(name)
        else:
            return
    rules.add_perm(name, pred)

for _, permission_name in all_permissions:
    make_perm(permission_name, rules.is_authenticated)

# These override the default 'is_authenticated' permissions
# To prevent unauthorized access, the permissions are only granted to users with the email domain '@veg3.ai'
for perm in admin_permissions:
    make_perm(perm, is_veg3_admin, True)