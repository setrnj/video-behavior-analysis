import sys
import os
try:
    import lzma
except ImportError:
    from backports import lzma
    sys.modules['lzma'] = lzma
    os.environ['LZMA_NATIVE'] = 'true'
