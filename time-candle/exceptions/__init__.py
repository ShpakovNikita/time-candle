def custom_excepthook(exc_type, exc_value, tb):
    # Uncomment it for detailed exception explanation

    # print('Traceback (most recent call last):')
    # while tb:
    #     filename = tb.tb_frame.f_code.co_filename
    #     name = tb.tb_frame.f_code.co_name
    #     lineno = tb.tb_lineno
    #     print('   File "%.500s", line %d, in %.500s' % (filename, lineno, name))
    #     tb = tb.tb_next

    # Exception type and value
    print(' %s: %s' % (exc_type.__name__, exc_value))
