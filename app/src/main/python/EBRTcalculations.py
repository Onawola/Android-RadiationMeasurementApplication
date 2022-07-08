import numpy as np
from scipy import interpolate


def helloworld(fz_a, fz_b, depth, pdose, frac, wedge_value, lead_value, measures, dose_rate, serial_no):
    # This part of the code is used to calculate the equivalent square field
    eqsf = round(float((2 * fz_a * fz_b) / (fz_a + fz_b)), 2)
    # This part of the code is used to calculate the dose per fraction
    fracdose = round((pdose / frac), 3)
    # This part of the code uses dictionary to chose wedge angles
    wedge = round(wedge_value, 3)
    # This part of the code uses dictionary to chose type of lead
    pb = round(lead_value, 3)
    sad_factor = 1.0125
    dr_x = [3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30, 35]
    dr_y = [(0.3505 * dose_rate), (0.5344 * dose_rate), (0.7254 * dose_rate), (0.8286 * dose_rate),
            (0.8987 * dose_rate), (0.9450 * dose_rate), (0.9730 * dose_rate), (1.0000 * dose_rate),
            (1.0339 * dose_rate), (1.0741 * dose_rate), (1.1164 * dose_rate), (1.1429 * dose_rate),
            (1.1606 * dose_rate), (1.1680 * dose_rate)]
    dr_factor = interpolate.interp1d(dr_x, dr_y, kind='linear', fill_value='none')
    dr = float(dr_factor(eqsf))
    calc_method = measures.lower()
    str_one = ""
    str_two = ""
    if calc_method == "sad":
        tmr_x = [0, 4, 5, 6, 7, 8, 10, 12, 15, 20, 25, 30]
        tmr_y = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12,
                 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18]
        tmr_z = np.array([
            (1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000),
            (0.966, 0.980, 0.982, 0.986, 0.988, 0.990, 0.994, 0.995, 0.996, 0.996, 1.000, 1.000),
            (0.935, 0.960, 0.964, 0.969, 0.973, 0.976, 0.981, 0.983, 0.985, 0.986, 0.990, 0.990),
            (0.904, 0.939, 0.946, 0.952, 0.957, 0.961, 0.967, 0.970, 0.973, 0.975, 0.980, 0.980),
            (0.875, 0.919, 0.927, 0.935, 0.941, 0.945, 0.952, 0.956, 0.960, 0.963, 0.970, 0.965),
            (0.845, 0.898, 0.908, 0.917, 0.924, 0.929, 0.937, 0.942, 0.947, 0.951, 0.960, 0.950),
            (0.819, 0.878, 0.889, 0.899, 0.906, 0.912, 0.921, 0.927, 0.933, 0.938, 0.945, 0.945),
            (0.792, 0.857, 0.870, 0.880, 0.888, 0.895, 0.905, 0.911, 0.919, 0.925, 0.930, 0.940),
            (0.767, 0.836, 0.850, 0.861, 0.870, 0.877, 0.888, 0.895, 0.904, 0.912, 0.915, 0.920),
            (0.741, 0.815, 0.829, 0.841, 0.851, 0.858, 0.870, 0.879, 0.889, 0.898, 0.900, 0.900),
            (0.718, 0.793, 0.809, 0.821, 0.831, 0.839, 0.852, 0.861, 0.872, 0.883, 0.890, 0.890),
            (0.694, 0.771, 0.788, 0.801, 0.811, 0.820, 0.834, 0.843, 0.855, 0.867, 0.880, 0.880),
            (0.672, 0.750, 0.767, 0.780, 0.791, 0.801, 0.815, 0.826, 0.838, 0.851, 0.865, 0.860),
            (0.649, 0.728, 0.745, 0.759, 0.771, 0.781, 0.796, 0.808, 0.820, 0.835, 0.850, 0.840),
            (0.629, 0.707, 0.724, 0.738, 0.751, 0.761, 0.777, 0.789, 0.803, 0.820, 0.830, 0.835),
            (0.608, 0.685, 0.702, 0.717, 0.730, 0.741, 0.757, 0.770, 0.786, 0.804, 0.810, 0.830),
            (0.589, 0.665, 0.683, 0.697, 0.710, 0.721, 0.738, 0.752, 0.768, 0.788, 0.800, 0.810),
            (0.570, 0.645, 0.663, 0.677, 0.690, 0.701, 0.719, 0.733, 0.750, 0.772, 0.790, 0.790),
            (0.552, 0.626, 0.644, 0.658, 0.671, 0.682, 0.701, 0.712, 0.734, 0.756, 0.775, 0.780),
            (0.534, 0.607, 0.624, 0.638, 0.651, 0.662, 0.682, 0.690, 0.717, 0.740, 0.760, 0.770),
            (0.518, 0.589, 0.606, 0.620, 0.633, 0.645, 0.664, 0.677, 0.700, 0.725, 0.745, 0.755),
            (0.501, 0.571, 0.588, 0.602, 0.615, 0.627, 0.646, 0.663, 0.683, 0.709, 0.730, 0.740),
            (0.485, 0.554, 0.571, 0.585, 0.598, 0.610, 0.630, 0.647, 0.667, 0.694, 0.715, 0.725),
            (0.469, 0.537, 0.553, 0.567, 0.581, 0.592, 0.613, 0.630, 0.651, 0.679, 0.700, 0.710),
            (0.454, 0.521, 0.537, 0.551, 0.564, 0.576, 0.597, 0.614, 0.636, 0.664, 0.685, 0.700),
            (0.439, 0.504, 0.520, 0.534, 0.547, 0.559, 0.581, 0.598, 0.620, 0.649, 0.670, 0.690),
            (0.426, 0.489, 0.505, 0.518, 0.532, 0.545, 0.566, 0.584, 0.606, 0.635, 0.655, 0.670),
            (0.412, 0.474, 0.489, 0.502, 0.516, 0.530, 0.551, 0.569, 0.592, 0.621, 0.640, 0.650),
            (0.399, 0.460, 0.475, 0.489, 0.502, 0.515, 0.536, 0.555, 0.578, 0.608, 0.625, 0.640),
            (0.386, 0.446, 0.461, 0.476, 0.487, 0.499, 0.521, 0.540, 0.563, 0.594, 0.610, 0.630),
            (0.374, 0.433, 0.448, 0.462, 0.474, 0.485, 0.507, 0.526, 0.550, 0.581, 0.600, 0.615),
            (0.361, 0.420, 0.434, 0.447, 0.460, 0.471, 0.493, 0.512, 0.536, 0.567, 0.590, 0.600),
            (0.350, 0.408, 0.422, 0.435, 0.447, 0.458, 0.480, 0.499, 0.523, 0.554, 0.575, 0.590),
            (0.338, 0.395, 0.409, 0.422, 0.434, 0.445, 0.467, 0.485, 0.510, 0.541, 0.560, 0.580),
            (0.328, 0.384, 0.398, 0.411, 0.422, 0.433, 0.455, 0.473, 0.498, 0.529, 0.545, 0.565),
            (0.317, 0.372, 0.386, 0.399, 0.410, 0.421, 0.442, 0.460, 0.485, 0.517, 0.530, 0.550),
        ])
        tmr_factor = interpolate.interp2d(tmr_x, tmr_y, tmr_z, kind='linear')
        tmr = float((tmr_factor(eqsf, depth)))
        sad_tt = (fracdose * 100) / (tmr * dr * wedge * pb * sad_factor)
        str_one = "The TMR is: {}".format(round(tmr, 3))
        str_two = "The Treatment Time is: {}mins".format(round(sad_tt, 2))
    elif calc_method == "ssd":
        pdd_x = [0, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30]
        pdd_y = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5, 11, 11.5, 12,
                 12.5, 13, 13.5, 14, 14.5, 15, 15.5, 16, 16.5, 17, 17.5, 18, 18.5, 19, 19.5, 20]
        pdd_z = np.array([
            (100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100),
            (95.6, 97.2, 97.5, 97.7, 97.8, 97.9, 98, 98.1, 98.2, 98.3, 98.3, 98.4, 98.5),
            (91.45, 94.3, 94.8, 95.15, 95.4, 95.55, 95.7, 95.9, 96.05, 96.2, 96.3, 96.45, 96.6),
            (87.3, 91.4, 92.1, 92.6, 93, 93.2, 93.4, 93.7, 93.9, 94.1, 94.3, 94.5, 94.7),
            (83.6, 88.4, 89.2, 89.8, 90.3, 90.6, 90.9, 91.2, 91.5, 91.8, 92.2, 92.4, 92.6),
            (79.9, 85.4, 86.3, 87, 87.6, 88, 88.4, 88.7, 89.1, 89.5, 90.1, 90.3, 90.5),
            (76.45, 82.55, 83.5, 84.3, 84.95, 85.4, 85.8, 86.2, 86.7, 87.2, 87.9, 88.2, 88.4),
            (73, 79.7, 80.7, 81.6, 82.3, 82.8, 83.2, 83.7, 84.3, 84.9, 85.6, 86, 86.3),
            (69.85, 76.8, 77.95, 78.9, 79.7, 80.3, 80.75, 81.25, 81.9, 82.6, 83.45, 83.85, 84.2),
            (66.7, 73.9, 75.2, 76.2, 77.1, 77.8, 78.3, 78.8, 79.5, 80.3, 81.3, 81.7, 82.1),
            (63.9, 71.15, 72.45, 73.5, 74.5, 75.2, 75.8, 76.35, 77.2, 78.1, 79.1, 79.6, 80.1),
            (61.1, 68.4, 69.7, 70.8, 71.9, 72.6, 73.3, 73.9, 74.9, 75.9, 76.9, 77.5, 78.1),
            (58.45, 65.85, 67.2, 68.4, 69.45, 70.25, 70.95, 71.6, 72.6, 73.7, 74.75, 75.4, 76),
            (55.8, 63.3, 64.7, 66, 67, 67.9, 68.6, 69.3, 70.3, 71.5, 72.6, 73.3, 73.9),
            (53.45, 60.9, 62.3, 63.6, 64.65, 65.55, 66.3, 67, 68.05, 69.3, 70.6, 71.4, 72),
            (51.1, 58.5, 59.9, 61.2, 62.3, 63.2, 64, 64.7, 65.8, 67.1, 68.6, 69.5, 70.1),
            (48.95, 56.2, 57.7, 59, 60.1, 61, 61.85, 62.6, 63.75, 65.05, 66.6, 67.55, 68.2),
            (46.8, 53.9, 55.5, 56.8, 57.9, 58.8, 59.7, 60.5, 61.7, 63, 64.6, 65.6, 66.3),
            (44.85, 51.8, 53.35, 54.65, 55.85, 56.8, 57.7, 58.45, 59.7, 61.1, 62.7, 63.75, 64.45),
            (42.9, 49.7, 51.2, 52.5, 53.8, 54.8, 55.7, 56.4, 57.7, 59.2, 60.8, 61.9, 62.6),
            (41.1, 47.8, 49.3, 50.6, 51.8, 52.75, 53.65, 54.45, 55.75, 57.25, 59, 60.1, 60.85),
            (39.3, 45.9, 47.4, 48.7, 49.8, 50.7, 51.6, 52.5, 53.8, 55.3, 57.2, 58.3, 59.1),
            (37.65, 44.15, 45.6, 46.85, 48, 48.95, 49.85, 50.7, 52.05, 53.6, 55.45, 56.65, 57.45),
            (36, 42.4, 43.8, 45, 46.2, 47.2, 48.1, 48.9, 50.3, 51.9, 53.7, 55, 55.8),
            (34.5, 40.75, 42.1, 43.3, 44.5, 45.5, 46.4, 47.25, 48.65, 50.25, 52.1, 53.4, 54.3),
            (33, 39.1, 40.4, 41.6, 42.8, 43.8, 44.7, 45.6, 47, 48.6, 50.5, 51.8, 52.8),
            (31.6, 37.6, 38.85, 40.15, 41.25, 42.25, 43.15, 44, 45.35, 47, 48.95, 50.25, 51.3),
            (30.2, 36.1, 37.3, 38.7, 39.7, 40.7, 41.6, 42.4, 43.7, 45.4, 47.4, 48.7, 49.8),
            (28.95, 34.65, 35.9, 37.2, 38.2, 39.15, 40.05, 40.9, 42.25, 43.95, 45.95, 47.3, 48.35),
            (27.7, 33.2, 34.5, 35.7, 36.7, 37.6, 38.5, 39.4, 40.8, 42.5, 44.5, 45.9, 46.9),
            (26.55, 32, 33.2, 34.35, 35.35, 36.3, 37.2, 38.1, 39.45, 41.1, 43.15, 44.55, 45.55),
            (25.4, 30.8, 31.9, 33, 34, 35, 35.9, 36.8, 38.1, 39.7, 41.8, 43.2, 44.2),
            (24.35, 29.55, 30.7, 31.75, 32.75, 33.75, 34.6, 35.45, 36.8, 38.4, 40.5, 41.85, 42.9),
            (23.3, 28.3, 29.5, 30.5, 31.5, 32.5, 33.3, 34.1, 35.5, 37.1, 39.2, 40.5, 41.6),
            (22.35, 27.25, 28.4, 29.4, 30.4, 31.35, 32.1, 32.9, 34.3, 35.9, 37.95, 39.3, 40.4),
            (21.4, 26.2, 27.3, 28.3, 29.3, 30.2, 30.9, 31.7, 33.1, 34.7, 36.7, 38.1, 39.2),
            (20.5, 25.15, 26.2, 27.2, 28.2, 29.1, 29.85, 30.6, 31.95, 33.55, 35.55, 36.95, 38.05),
            (19.6, 24.1, 25.1, 26.1, 27.1, 28, 28.8, 29.5, 30.8, 32.4, 34.4, 35.8, 36.9),
            (18.8, 23.15, 24.15, 25.1, 26.05, 26.9, 27.7, 28.45, 29.75, 31.3, 33.3, 34.65, 35.8),
            (18, 22.2, 23.2, 24.1, 25, 25.8, 26.6, 27.4, 28.7, 30.2, 32.2, 33.5, 34.7),
        ])
        pdd_factor = interpolate.interp2d(pdd_x, pdd_y, pdd_z, kind='linear')
        pdd = float((pdd_factor(eqsf, depth)))
        ssd_tt = (fracdose * 10000) / (pdd * dr * wedge * pb)
        str_one = "The PDD is: {}".format(round(pdd, 2))
        str_two = "The Treatment Time is: {}mins".format(round(ssd_tt, 2))
    return """Serial No.: {}\nWedge factor: {}\nTray factor: {}\nThe equivalent square field is: {}cm^2\nThe dose per fraction is: {}Gy\nThe Doserate is: {}cGy/min\n{}\n{}""".format(serial_no,
                wedge,
                pb,
                eqsf,
                fracdose,
                round(dr, 3),
                str_one,
                str_two)