def make_a_word(b1,b2,b3,b4,b5,b6):
    if b6 == "0":    
        if b5 == "0":    
            if b4 == "0":
                if b3 == "0":
                    if b2 == "0":
                        if b1 == "0":
                            ba = "0"
                        else:ba = b1
                    else:ba = b1 + " " + b2
                else:ba = b1 + " "+ b2 + " " + b3
            else:ba = b1 +" "+b2+" "+b3+" "+b4
        else:ba = b1 +" "+b2+" "+b3+" "+b4 + " " + b5
    else:ba = b1 +" "+b2+" "+b3+" "+b4 + " " + b5 + " " + b6
    return ba