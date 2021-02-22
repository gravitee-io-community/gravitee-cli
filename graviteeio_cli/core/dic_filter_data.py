EXCLUDED_API_VALUES = [
    'owner',
    'picture_url',
    'deployed_at',
    'created_at',
    'updated_at',
    'lifecycle_state',
    'id',
    'state',
    'entrypoints',
    'workflow_state',
    'picture'
]

EXLUDED_API_PLAN_VALUES = [
    'id',
    'apis',
    'created_at',
    'updated_at',
    'published_at'
]

EXLUDED_API_METADATA_VALUES = [
    'apiId',
    'defaultValue'
]

EXLUDED_APP_VALUES = [
    'id',
    'created_at',
    'disable_membership_notifications',
    'groups',
    'owner',
    'status',
    'type',
    'updated_at'
]

EXLUDED_APP_METADATA_VALUES = [
    'applicationId',
    'key'
]


def filter_api_values(api_data):
    filter_dic_values(api_data, EXCLUDED_API_VALUES)

    if 'plans' in api_data:
        for plan in api_data['plans']:
            filter_dic_values(plan, EXLUDED_API_PLAN_VALUES)

    if 'metadata' in api_data:
        for metadata in api_data['metadata']:
            filter_dic_values(metadata, EXLUDED_API_METADATA_VALUES)


def filter_app_values(app_data):
    filter_dic_values(app_data, EXLUDED_APP_VALUES)

    if 'metadata' in app_data:
        for metadata in app_data['metadata']:
            filter_dic_values(metadata, EXLUDED_APP_METADATA_VALUES)


def filter_dic_values(data, exclude_value):
    for key in exclude_value:
        if key in data:
            del data[key]
