# -*- coding: utf-8 -*-
# Copyright (c) 2021 Linh Pham
# do-instances-report is relased under the terms of the Apache License 2.0
"""Flask WSGI startup file"""

from app import app

if __name__ == "__main__":
    app.run(debug=False)
