#TODO
#1. Limit voltages according to voltage supply range
# Solve this error:
# ----- Finished 3 step -----
# Supply voltage is 0.04
# Actual drain voltage is 0.0459
# Delta is 0.0041
# Traceback (most recent call last):
# ----- Finished 4 step -----
# Supply voltage is 0.04
#   File "D:/#Research/Tools/Python/code/Noise/A0_MAIN_MOS_2ndSetup_woTemp.py", line 101, in <module>
# Actual drain voltage is 0.0457
# Delta is 0.0043
#     setup_drain_voltage(Vd=Vd_noise, Vd_delta=0.001, set_sup_Vd=voltsource.set_voltage_b, measure_Vd=meter.read_voltage, max_steps=5, dbg=True)
#   File "D:\#Research\Tools\Python\code\Noise\setup_drain_voltage.py", line 46, in setup_drain_voltage
#     k = (act_Vd[-1] - act_Vd[-2]) / (sup_Vd[-1] - sup_Vd[-2])
# ZeroDivisionError: float division by zero


from time import sleep


def setup_drain_voltage(Vd, Vd_delta, set_sup_Vd, measure_Vd, max_steps=5, dbg=False):
    """
    Setting up drain voltage with feedback.
    Vd - objective drain voltage
    Vd_delta - allowable divergency of drain voltage
    set_sup_Vd - function to setup supply drain voltage
    measure_Vd - function to measure actual drain voltage
    max_steps - maximum tuning steps, optional, default value is 5,
    dbg - debugging option, provide additional console output, optional, default value is False
    """
    obj_Vd = round(Vd, 2)
    obj_Vd_delta = Vd_delta  # delta between objective drain voltage and actual drain voltage have to be not higher than this value

    # initital values
    act_Vd = []
    sup_Vd = []
    next_sup_Vd = obj_Vd * 8 #estimation of R/rd
    act_Vd_delta = []  # errors list

    # auxiliary functions
    def setup_and_measure():
        set_sup_Vd(next_sup_Vd)  # set supply drain voltage
        sup_Vd.append(next_sup_Vd)  # add current supply drain voltage to the list
        sleep(4)
        act_Vd.append(round(measure_Vd(), 4))  # measure actual drain voltage
        act_Vd_delta.append(round(obj_Vd - act_Vd[-1], 4))
        if dbg:
            print("Supply: %s step: Supply voltage = %s;  Actual drain voltage = %s; Delta is %s " % (len(sup_Vd), sup_Vd[-1], act_Vd[-1], act_Vd_delta[-1]))
            # print("Supply voltage is %s" % sup_Vd[-1])
            # print("Actual drain voltage is %s" % act_Vd[-1])
            # print("Delta is %s" % act_Vd_delta[-1])
        return None

    # First voltage setup and measurement
    setup_and_measure()    
    next_sup_Vd = round(sup_Vd[-1] * obj_Vd / act_Vd[-1], 2)

    while len(act_Vd) <= max_steps and obj_Vd_delta < abs(act_Vd_delta[-1]):
        setup_and_measure()
        k = (act_Vd[-1] - act_Vd[-2]) / (sup_Vd[-1] - sup_Vd[-2])
        b = (sup_Vd[-1] * act_Vd[-2] - sup_Vd[-2] * act_Vd[-1]) / (sup_Vd[-1] - sup_Vd[-2])
        next_sup_Vd = round((obj_Vd - b) / k, 2)

    print("Final drain voltage is %sV, supply voltage is %sV" % (act_Vd[-1], sup_Vd[-1]))
    if not dbg:
        return None
    else:
        return sup_Vd, act_Vd_delta


def setup_drain_voltage_2d(Vd, Vd_delta, set_sup_Vd, measure_Vd, max_steps=5, dbg=False):
    """
    Version for 2d transistors with unusually low drain voltages
    Setting up drain voltage with feedback.
    Vd - objective drain voltage
    Vd_delta - allowable divergency of drain voltage
    set_sup_Vd - function to setup supply drain voltage
    measure_Vd - function to measure actual drain voltage
    max_steps - maximum tuning steps, optional, default value is 5,
    dbg - debugging option, provide additional console output, optional, default value is False
    """
    # obj_Vd = round(Vd, 2)
    obj_Vd = Vd
    obj_Vd_delta = Vd_delta  # delta between objective drain voltage and actual drain voltage have to be not higher than this value

    # initital values
    act_Vd = []
    sup_Vd = []
    next_sup_Vd = obj_Vd * 8 #estimation of R/rd
    act_Vd_delta = []  # errors list

    # auxiliary functions
    def setup_and_measure():
        set_sup_Vd(next_sup_Vd)  # set supply drain voltage
        sup_Vd.append(next_sup_Vd)  # add current supply drain voltage to the list
        sleep(4)
        act_Vd.append(round(measure_Vd(), 8))  # measure actual drain voltage
        act_Vd_delta.append(round(obj_Vd - act_Vd[-1], 8))
        if dbg:
            print("Supply: %s step: Supply voltage = %s;  Actual drain voltage = %s; Delta is %s " % (len(sup_Vd), sup_Vd[-1], act_Vd[-1], act_Vd_delta[-1]))
            # print("Supply voltage is %s" % sup_Vd[-1])
            # print("Actual drain voltage is %s" % act_Vd[-1])
            # print("Delta is %s" % act_Vd_delta[-1])
        return None

    # First voltage setup and measurement
    setup_and_measure()    
    next_sup_Vd = round(sup_Vd[-1] * obj_Vd / act_Vd[-1], 8)

    while len(act_Vd) <= max_steps and obj_Vd_delta < abs(act_Vd_delta[-1]):
        setup_and_measure()
        k = (act_Vd[-1] - act_Vd[-2]) / (sup_Vd[-1] - sup_Vd[-2])
        b = (sup_Vd[-1] * act_Vd[-2] - sup_Vd[-2] * act_Vd[-1]) / (sup_Vd[-1] - sup_Vd[-2])
        next_sup_Vd = round((obj_Vd - b) / k, 8)

    print("Final drain voltage is %sV, supply voltage is %sV" % (act_Vd[-1], sup_Vd[-1]))
    if not dbg:
        return None
    else:
        return sup_Vd, act_Vd_delta