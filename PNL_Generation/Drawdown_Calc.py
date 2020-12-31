import pandas as pd


def DD_cum(pnl_series):
    DD_cum = ((pnl_series / (pnl_series.shift(1).cummax())) - 1)
    DD_cum[DD_cum > 0] = 0
    DD_cum.fillna(0, inplace=True)

    DD_distribution = DD_breakdown(DD_cum)

    return DD_cum, DD_distribution


def DD_sum(pnl_series, baseamount):
    DD_sum = (pnl_series - (pnl_series.shift(1).cummax()))
    DD_sum=DD_sum/baseamount
    DD_sum[DD_sum > 0] = 0
    DD_sum.fillna(0, inplace=True)
    DD_distribution = DD_breakdown(DD_sum)

    return DD_sum, DD_distribution


def DD_breakdown(DD):
    DD_distribution = []
    DD_number = 0
    counter = 0
    while counter < (len(DD) - 1):

        if DD[counter] == 0:
            counter += 1

        else:
            DD_number += 1
            DD_start_date = DD.index[counter]
            local_list = []
            while (DD[counter] < 0) and (counter < (len(DD.index) - 1)):
                [local_date, local_DD_number] = [DD.index[counter], DD[counter]]
                local_list.append([local_date, local_DD_number])
                counter += 1
            local_DD = pd.DataFrame(local_list, columns=["Dates", "DD"])
            local_DD.set_index("Dates", inplace=True)
            DD_end_date = DD.index[counter]
            Max_dd = local_DD["DD"].min()
            Max_dd_date = local_DD["DD"].idxmin()
            DD_recovery_period = DD_end_date - Max_dd_date
            DD_period = DD_end_date - DD_start_date
            DD_distribution.append(
                [DD_number, DD_start_date, DD_end_date, Max_dd, Max_dd_date, DD_period, DD_recovery_period])
            del local_DD

    DD_distribution = pd.DataFrame(DD_distribution,
                                   columns=["DD_number", "DD_start_date", "DD_end_date", "Max_dd", "Max_dd_date",
                                            "DD_period", "DD_recovery_period"])

    DD_distribution.set_index("DD_number", drop=True, inplace=True)

    return DD_distribution
