==================
Compressor support
==================

Adds support for new filters and compressors to add support for UglifyJS.

Filters
-------

``barbeque.compressor.UglifyJSFilter``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A filter that uses UglifyJS to compress JavaScript code.

Integration:

.. code-block:: python

    COMPRESSOR_JS_FILTERS = [
        'barbeque.compressor.UglifyJSFilter',
    ]


Compressors
-----------

``barbeque.compressor.UglifyJSSourcemapCompressor``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A compressor that compiles javascript code using UglifyJS and generates a proper
sourcemap.

Integration:

.. code-block:: python

    COMPRESS_JS_COMPRESSOR = 'barbeque.compressor.UglifyJSSourcemapCompressor'
