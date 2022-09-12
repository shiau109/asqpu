from numpy import array

# def singleQ_compile( self, qubit_id:str, action_id:str, pars:List ):

#         base_circuit = self.base_circuit

#         qubit = base_circuit.get_qComp(qubit_id)
#         action = base_circuit.get_action(action_id)
#         action.pars = pars
#         action.t0 = self.t0_element

#         new_pulse = action.to_pulse(qubit)
#         port = base_circuit.get_port(action_id)
        
#         if action!=None:

#             return new_pulse

def xy_control( coeffs_map, target_index ):
    sx_exist = False
    sy_exist = False
    for label in coeffs_map.keys():
        label_index = int(label[2:])
        label_action = label[:2]
        if label_index == target_index:
            match label_action:
                    case "sx":
                        sx_exist = True
                        sx_coeff = array(coeffs_map[label])
                    case "sy": 
                        sy_exist = True
                        sy_coeff = array(coeffs_map[label])
                    case _: pass
    if sx_exist and sy_exist:
        rf_envelop = sx_coeff +1j*sy_coeff
        return rf_envelop



def coeff_to_driving( coeff_label ):

    pass

    return None


if __name__ == '__main__':
    coeffs_map = {"sx0":array([0,1]),"sy0":array([0,1])}
    rf_envelope = xy_control(coeffs_map, 0)
    print(rf_envelope)
