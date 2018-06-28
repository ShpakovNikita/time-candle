from main_system import logger
from main_system import shortcuts


def startup_page_init(*f_args):
    """
    This decorator wraps view function and init on the pages all fields for
    searching (search by default)
    :param f_args: field id's
    """
    fields = list(f_args)
    logger.debug('fields: %s', fields)

    def func_wrapper(func):

        def decorator_func(request, *args, **kwargs):
            logger.debug('in')
            for link in fields:
                redirect_link = shortcuts.search_user_forms(request, link)
                if redirect_link:
                    return redirect_link

            return func(request, *args, **kwargs)

        logger.debug('func name: %s', func)

        return decorator_func

    return func_wrapper
