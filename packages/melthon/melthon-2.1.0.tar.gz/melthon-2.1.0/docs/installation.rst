============
Installation
============

Use Docker (preferred way)::

    # --rm           : Remove container after execution
    # -u ${UID}      : Run container as current user
    # -v"$(pwd):/src": Make source and output accessible inside container
    docker run --rm -u ${UID} -v"$(pwd):/src" jenswbe/melthon

Use pip::

    pip install melthon
