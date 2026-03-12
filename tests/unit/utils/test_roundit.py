import boaviztapi.utils.roundit as rd
import pytest


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
    assert rd.significant_number(4.32e-04) == 3
    assert rd.significant_number(4.32001e-04) == 6


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


def test_round_based_on_min_max():
    # high difference between min and max:
    assert rd.round_based_on_min_max(20.29217, 10.91891, 81.81527, 10) == 20
    # small difference between min and max:
    assert rd.round_based_on_min_max(20.29217, 18.91891, 22.81527, 10) == 20.3

    # Different precision:
    # 10%
    assert rd.round_based_on_min_max(1.2345, 1.2, 1.3, 10) == 1.23
    # 1%
    assert rd.round_based_on_min_max(1.2345, 1.2, 1.3, 1) == 1.234

    # WHen no rounding is requied :
    assert rd.round_based_on_min_max(60, 10, 90, 10) == 60
    assert rd.round_based_on_min_max(60, 10, 90, 1) == 60

    # Various other tests:
    assert rd.round_based_on_min_max(1.52366871, 1, 2, 1) == 1.52
    assert rd.round_based_on_min_max(1.52366871, 1, 2, 10) == 1.5

    assert rd.round_based_on_min_max(20.29217, 10.91891, 81.81527, 10) == 20
    assert (
        rd.round_based_on_min_max(1819.821672, 110.14710120000001, 5419.285269084, 10)
        == 1800
    )
    assert (
        rd.round_based_on_min_max(
            0.02040328338, 0.020400523740000003, 0.02042139678, 10
        )
        == 0.020403
    )
    assert (
        rd.round_based_on_min_max(
            0.00030760589391948, 0.63406418256e-05, 0.00127183984353, 10
        )
        == 0.0003
    )
    assert rd.round_based_on_min_max(306.0165, 179.92950000000002, 1133.6115, 10) == 310
    assert (
        rd.round_based_on_min_max(61648.853641199996, 62.2570572, 2241972.40986, 10)
        == 100000
    )


def test_round_based_on_min_max_corner_cases():
    #  min == max : must retun the original value without any rounding
    assert rd.round_based_on_min_max(1, 1, 1, 1) == 1
    #  precision == 0 : must raise ValueError
    with pytest.raises(ValueError):
        rd.round_based_on_min_max(1, 1, 1, 0)
    # min > max
    with pytest.raises(ValueError):
        rd.round_based_on_min_max(5, 10, 5, 10)
