import os
backend = os.environ['BACKEND'] if 'BACKEND' in os.environ else 'TkAgg'

import matplotlib
matplotlib.use(backend)
