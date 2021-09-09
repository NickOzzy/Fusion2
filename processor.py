import amjuel_tables as ajt


def get_H2plus_H2_ratio(ne, Te):
    ratio = (ajt.amjuel_tables('h2', "H2_3_2_3", ne, Te) + ajt.amjuel_tables('h4', "H4_2_2_9", ne, Te))\
            / (ajt.amjuel_tables('h4', "H4_2_2_14", ne, Te) + ajt.amjuel_tables('h4', "H4_2_2_11", ne, Te)
               + ajt.amjuel_tables('h4', "H4_2_2_12", ne, Te))
    return ratio

def get_H2plus_H2_from_single_poly(ne, Te):
    return ajt.amjuel_tables('h11', "H11_2_0c", ne, Te)

# returns the H2 density according to Stangeby paper
# def find_nh2(T):
#    return(1.8911e20 / ((T ** 1.4705)))
# def find_nh2ii(T):
#     return(2e18 / (T ** 1.7))

def get_H3plus_H2_ratio(ne, Te):
    return ajt.amjuel_tables('h11', "H11_4_0a", ne, Te)

def get_Hminus_H2_ratio(ne, Te):
    return ajt.amjuel_tables('h11', "H11_7_0a", ne, Te)

def h2plush2_from_h12(ne, Te):
    return ajt.amjuel_tables('h12', "H12_2_0c", ne, Te)







