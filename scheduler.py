def converter(score:int) -> int:
    new_score = score/20
    return int(new_score)


def scheduling(quality:int,repetition:int,ease_factor:float,interval:int) ->  tuple[int, float, int]: 
    if quality < 3:
        repetition = 0
        interval = 1
    else:    
       if repetition == 0:
           interval = 1
       elif repetition == 1:
           interval = 6
       else:
           interval = round(interval * ease_factor)    
       repetition +=1
    ease_factor = ease_factor + (0.1 -(5-quality) *(0.08 + (5-quality) *0.02))   
    if ease_factor < 1.3:
        ease_factor = 1.3
    return repetition,ease_factor,interval     
 