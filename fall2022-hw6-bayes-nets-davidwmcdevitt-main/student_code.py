import itertools 

def ask(var, value, evidence, bn):
    
    # Evidence if True
    evidence_value = evidence.copy()
    evidence_value[var] = value
    
    # Evidence if False
    negate_value = evidence.copy()
    negate_value[var] = not value
    
    net_variables = bn.variable_names
    evidence_nodes = list(evidence.keys())
    evidence_outcomes = list(evidence.values())
    
    not_given = list(net_variables - evidence_value.keys())
    
    joint_prob = recursive_ask(evidence_value,not_given,bn,net_variables.copy())
    print("Joint",joint_prob)
    
    norm_constant = recursive_ask(evidence_value,not_given,bn,net_variables.copy()) + recursive_ask(negate_value,not_given,bn,net_variables.copy())
    print("Norm",norm_constant)
    
    answer = joint_prob/norm_constant
    
    return answer

def recursive_ask(evidence,not_given,bn,net_variables):
    var = net_variables.pop(0)
    
    if var in not_given:
        if len(net_variables) > 0:
            
            index = bn.variable_names.index(var)
            evidence_true = evidence.copy()
            evidence_false = evidence.copy()
            evidence_true[var] = True
            evidence_false[var] = False
            
            prob_true = bn.variables[index].probability(True,evidence_true)
            prob_false = bn.variables[index].probability(False,evidence_false)
            #print("True",prob_true)
            #print("False",prob_false)
            
            calc = (prob_true * recursive_ask(evidence_true,not_given,bn,net_variables.copy())) +(prob_false * recursive_ask(evidence_false,not_given,bn,net_variables.copy()))
            return calc
        if len(net_variables) == 0:
            return 1
    if var not in not_given:
        index = bn.variable_names.index(var)
        prob = bn.variables[index].probability(evidence[var],evidence)
        if len(net_variables) > 0:
            calc = prob * recursive_ask(evidence,not_given,bn,net_variables.copy())
            return calc
        if len(net_variables) == 0:
            return prob
