import krippendorff
import pandas as pd
import numpy as np

def test_krippendorff_alpha():
    df = pd.DataFrame({'rater1': ["N/A", "N/A", "N/A", "N/A", "N/A",3,4,1,2,1,1,3,3,"N/A",3],
                    'rater2': [1, "N/A", 2, 1, 3,3,4,3,"N/A","N/A","N/A","N/A","N/A","N/A","N/A"],
                    'rater3': ["N/A", "N/A", 2, 1, 3,4,4,"N/A",2,1,1,3,3,"N/A",4]})

    data = df.T.values.tolist()

    data_tuple = tuple(' '.join(map(str, row)) for row in data)

    reliability_data_str = (
            "3    0.5    0.5    1    0.5    0.25    0.25    0.25    0.25    0.3333    2    0.5    3    2    0.3333",  # coder A
            "1    0.5    0.3333    0.5    1    0.5    3    1    1    2    3    4    1    1    1",  # coder B
            "2    0.3333    0.1667    1    2    2    0.2    0.3333    0.3333    0.3333    1    0.3333    3    3    1",  # coder C
        )

    print(reliability_data_str)
    print(data_tuple)
    newlistconvert =[[np.nan if (v == "*" or v=="N/A") else v for v in coder.split()] for coder in data_tuple]
    reliability_data = [[np.nan if (v == "*" or v=="N/A") else v for v in coder.split()] for coder in reliability_data_str]


    #assert newlistconvert ==reliability_data

    print("Krippendorff's alpha for nominal metric: ", krippendorff.alpha(reliability_data=reliability_data,
                                                                            level_of_measurement="nominal"))
    #assert (krippendorff.alpha(reliability_data=newlistconvert,level_of_measurement="nominal"))== (krippendorff.alpha(reliability_data=reliability_data, level_of_measurement="nominal"))

