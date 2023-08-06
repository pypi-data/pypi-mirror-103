from dcim.forms import DeviceFilterForm
from dcim.models import RackRole
from utilities.forms import DynamicModelMultipleChoiceField, APISelectMultiple


class SPDeviceFilterForm(DeviceFilterForm):
    field_order = [
        "q",
        "region_id",
        "site_id",
        "location_id",
        "rack_role",
        "rack_id",
        "status",
        "role_id",
        "tenant_group_id",
        "tenant_id",
        "manufacturer_id",
        "device_type_id",
        "asset_tag",
        "mac_address",
        "has_primary_ip",
    ]

    rack_role = DynamicModelMultipleChoiceField(
        queryset=RackRole.objects.all(),
        required=False,
        label="Rack role",
    )
