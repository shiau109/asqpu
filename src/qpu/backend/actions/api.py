from qpu.backend.actions.basic_action import PhysicalAction, RXYOperation, RZOperation


def action_from_dict( a_dict:dict ):
    if a_dict["type"]=="RXYOperation": 
        actionObj = RXYOperation(a_dict["id"])
    if a_dict["type"]=="RZOperation": 
        actionObj = RZOperation(a_dict["id"])
    actionObj.duration = float(a_dict["duration"])
    return actionObj