def get_spn(toponym):
    low_cor = toponym["boundedBy"]["Envelope"]["lowerCorner"].split()
    up_cor = toponym["boundedBy"]["Envelope"]["upperCorner"].split()

    delta1 = abs(float(low_cor[0]) - float(up_cor[0]))
    delta2 = abs(float(low_cor[1]) - float(up_cor[1]))

    return ",".join([str(delta1), str(delta2)])