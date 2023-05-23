from .controllers import (
    get_auth_user_controller,
    get_guardian_controller,
    get_outpass_controller,
)
from .permissions import (
    admin_required,
    auth_required,
    guard_route,
    student_route,
    warden_route,
)
