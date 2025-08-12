import sys
import os
try:
    import lzma
except ImportError:
    try:
        from backports import lzma
    except ImportError:
        import subprocess
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'backports.lzma'])
        from backports import lzma
    sys.modules['lzma'] = lzma
    os.environ['LZMA_NATIVE'] = 'true'
