import commands_parser
import app_logger
import config_parser
# TODO: cut down lower part of the code from this module


def main():
    """
    usr = config_parser.run_config()['user']
    usr.say_hi()
    """
    app_logger.custom_logger('root').info('Entering the program.')
    commands_parser.run()
    app_logger.custom_logger('root').info('Leaving the program.')


if __name__ == "__main__":
    main()
