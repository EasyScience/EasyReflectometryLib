from numpy.testing import assert_almost_equal

from easyreflectometry.data.data_store import DataSet1D


class TestDataStore:
    def test_constructor(self):
        # When
        data = DataSet1D(
            x=[1, 2, 3], y=[4, 5, 6], ye=[7, 8, 9], xe=[10, 11, 12], x_label='label_x', y_label='label_y', name='MyDataSet1D'
        )

        # Then Expect
        assert data.name == 'MyDataSet1D'
        assert_almost_equal(data.x, [1, 2, 3])
        assert data.x_label == 'label_x'
        assert_almost_equal(data.xe, [10, 11, 12])
        assert_almost_equal(data.y, [4, 5, 6])
        assert data.y_label == 'label_y'
        assert_almost_equal(data.ye, [7, 8, 9])

    def test_repr(self):
        # When
        data = DataSet1D(
            x=[1, 2, 3], y=[4, 5, 6], ye=[7, 8, 9], xe=[10, 11, 12], x_label='label_x', y_label='label_y', name='MyDataSet1D'
        )

        # Then
        repr = str(data)

        # Expect
        assert repr == r"1D DataStore of 'label_x' Vs 'label_y' with 3 data points"

    def test_data_points(self):
        # When
        data = DataSet1D(
            x=[1, 2, 3], y=[4, 5, 6], ye=[7, 8, 9], xe=[10, 11, 12], x_label='label_x', y_label='label_y', name='MyDataSet1D'
        )

        # Then
        points = data.data_points()

        # Expect
        assert list(points) == [(1, 4, 7, 10), (2, 5, 8, 11), (3, 6, 9, 12)]
