from riscemv.ReservationStations import ReservationStations
from riscemv.gui.ResStationsViewer import ResStationsViewer


def test_add_status(qtbot):
    RS = ReservationStations(1, 1, 1, 1, 1, 1, 1, 1)
    rs_v = ResStationsViewer(RS)

    fu = RS.get_first_free("ADD")
    fu.busy = True
    fu.thread_id = 0
    fu.instruction = "ADD x1, x0, 3"
    fu.time_remaining = 3

    rs_v.load_contents()

    assert rs_v.rs_table.item(0, 0).text() == '3', "Wrong cycles left"
    assert rs_v.rs_table.item(0, 1).text() == "ADD0", "Wrong tag"
    assert rs_v.rs_table.item(0, 2).text() == 'Yes', "Wrong busy"
    assert rs_v.rs_table.item(0, 3).text() == "ADD x1, x0, 3", "Wrong instruction"
