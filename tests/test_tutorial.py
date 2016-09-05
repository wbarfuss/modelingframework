"""Test the ipython notebook tutorials.

Inspiration
-----------
https://gist.github.com/minrk/2620876
"""
import os
import sys
# import time
# from Queue import Empty
from IPython.kernel import KernelManager
from IPython.nbformat.current import reads


def run_notebook(nb):
    """Run notebook."""
    km = KernelManager()
    km.start_kernel(stderr=open(os.devnull, 'w'))
    kc = km.client()
    kc.start_channels()
    kc.execute("pass")
    kc.get_shell_msg()

    cells = 0
    failures = 0
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type != 'code':
                continue
            kc.execute(cell.input)
            # wait for finish, maximum 20s
            reply = kc.get_shell_msg(timeout=20)['content']
            if reply['status'] == 'error':
                failures += 1
                print "\nFAILURE:"
                print cell.input
                print '-----'
                print "raised:"
                print '\n'.join(reply['traceback'])
            cells += 1
            sys.stdout.write('.')
    # print "ran notebook %s" % nb.metadata.name
    print "    ran %3i cells" % cells
    if failures:
        print "    %3i cells raised exceptions" % failures
    kc.stop_channels()
    km.shutdown_kernel()
    del km
    return failures


def test_tutorials():
    """Test tutorial notebooks."""
    ipynbs = ["tutorial/01_tutorial.ipynb"]
    for ipynb in ipynbs:
        print "running %s" % ipynb
        with open(ipynb) as f:
            nb = reads(f.read(), 'json')
        fails = run_notebook(nb)
        assert fails == 0