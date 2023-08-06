#!/bin/bash
rm -rvf plots_Bd_data; python ./test_bd_data.py
rm -rvf plots_Bd;  python ./test_bd_mc.py
rm -rvf plots_Bu_data;  python ./test_bu_data.py
rm -rvf plots_Bu; python ./test_bu_mc.py
