

def singleQ_comp( self, qubit_id:str, action_id:str, pars:List ):

        base_circuit = self.base_circuit

        qubit = base_circuit.get_qComp(qubit_id)
        action = base_circuit.get_action(action_id)
        action.pars = pars
        action.t0 = self.t0_element

        new_pulse = action.to_pulse(qubit)
        port = base_circuit.get_port(action_id)
        
        if action!=None:

            return new_pulse
        
