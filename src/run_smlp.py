#!/usr/bin/env python3
#
# This file is part of smlprover.
# It is a top level script to run smlprover (SMLP)
#

# coding: utf-8
import sys
from smlp_py.smlp_flows import SmlpFlows

sys.set_int_max_str_digits(1000000)


def main(argv):
    smlpInst = SmlpFlows(argv)
    smlpInst.smlp_flow()


if __name__ == "__main__":
    main(sys.argv)
