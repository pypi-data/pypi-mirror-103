
import sys
import analytics
analytics.write_key = '6I7ptc5wcIGC4WZ0N1t0NXvvAbjRGUgX' 

from mitoinstaller.user_install import get_static_user_id_install

static_user_id_install = get_static_user_id_install()

def log_failed_upgrade(reason):
    log(
        'failed_upgrade',
        {
            'reason': reason, 
            'error': str(sys.exc_info()[1])
        }
    )

def log_failed_install(reason):
    log(
        'failed_install',
        {
            'reason': reason, 
            'error': str(sys.exc_info()[1])
        }
    )

def log(event, params=None):
    """
    A utility that all logging should pass through
    """
    if params is None:
        params = {}

    analytics.track(
        static_user_id_install, 
        event, 
        params
    )
