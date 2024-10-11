#!/usr/bin/env python3

import pandas as pd

vantage_file = "azure_vms_from_vantage.csv"
benchmark_file_linux = "instances_azure_linux.csv"
benchmark_file_windows = "instances_azure_windows.csv"

def main():
    v_csv_data = pd.read_csv(vantage_file)
    b_csv_data_win = pd.read_csv(benchmark_file_windows)
    b_csv_data_lin = pd.read_csv(benchmark_file_linux)
    found_v_in_b = 0
    found_b_in_v = 0
    items_found_in_v = []
    for d in v_csv_data["Name"]:
        d = d.replace(" ", "_")
        #print("d: {}".format(d))
        res_lin = [ i for i in b_csv_data_lin["Name"] if i == d ]
        if len(res_lin) > 0:
            print("Found {} in Benchmark data for Linux: {}".format(d, res_lin))
            found_v_in_b += 1
        else:
            res_win = [ i for i in b_csv_data_win["Name"] if i == d ]
            if len(res_win) > 0:
                print("Found {} in Benchmark data for Windows: {}".format(d, res_win))
                found_v_in_b += 1
            else:
                print("{} NOT FOUND IN ANY BENCH".format(d))
    for d in b_csv_data_win["Name"]:
        res_v = [ i for i in v_csv_data["Name"] if i.replace(" ", "_") == d ]
        if len(res_v) > 0 and d not in items_found_in_v:
            print("Found {} from bench windows in vantage data: {}".format(d, res_v))
            found_b_in_v += 1
            items_found_in_v += d
    for d in b_csv_data_lin["Name"]:
        res_v = [ i for i in v_csv_data["Name"] if i.replace(" ", "_") == d ]
        if len(res_v) > 0 and d not in items_found_in_v:
            print("Found {} from bench linux in vantage data: {}".format(d, res_v))
            found_b_in_v += 1
            items_found_in_v += d

    print("Found {} items from benchmarks in vantage data. Vantage data contains {}".format(found_b_in_v, len(v_csv_data)))
    print("Found {} items from vantage data in benchmarks. Benchmarks contains {}".format(found_v_in_b, len(b_csv_data_lin)+len(b_csv_data_win)))

if __name__ == "__main__":
    main()
