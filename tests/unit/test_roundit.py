import boaviztapi.utils.roundit as rd


def test_sigfig_():
    assert rd.significant_number(1.0) == 1
    assert rd.significant_number(0.1) == 1
    assert rd.significant_number(0.01) == 1
    assert rd.significant_number(10) == 2
    assert rd.significant_number(10.0) == 2
    assert rd.significant_number(1.1) == 2
    assert rd.significant_number(2.02) == 3
    assert rd.significant_number(22.1) == 3
    assert rd.significant_number(22.10) == 3
    assert rd.significant_number(0.245) == 3
    assert rd.significant_number(0.2450) == 3
    assert rd.significant_number(0.0245) == 3
    assert rd.significant_number(4.32E-04) == 3
    assert rd.significant_number(4.32001E-04) == 6


def test_remove_unsignificant_zeros():
    assert rd.remove_unsignificant_zeros(0.0001) == 1
    assert rd.remove_unsignificant_zeros(0.00201) == 201
    assert rd.remove_unsignificant_zeros(0.0000201) == 201


def test_round_to_sigfig():
    assert rd.round_to_sigfig(1.0521, 1) == 1
    assert rd.round_to_sigfig(1.0521, 2) == 1.1
    assert rd.round_to_sigfig(1.0521, 3) == 1.05
    assert rd.round_to_sigfig(0.0251, 1) == 0.03
    assert rd.round_to_sigfig(0.0251, 2) == 0.025
    assert rd.round_to_sigfig(0.0251, 3) == 0.0251
    # this case is not supported as the return float value is 0.2
    # assert rd.round_to_sigfig(0.202, 2) == '0.20'
