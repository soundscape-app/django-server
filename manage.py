#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Django's command-line utility for administrative tasks."""
import os
import sys

ENV = 'DEV' # 배포 시 'PROD' / 디버깅 시 'DEV'

def main():
    env_dict = {'DEV': '.dev', 'PROD': '.prod'}
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings' + env_dict[ENV])
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
