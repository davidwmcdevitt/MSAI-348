import read, copy
from util import *
from logical_classes import *

verbose = 0

class KnowledgeBase(object):
    def __init__(self, facts=[], rules=[]):
        self.facts = facts
        self.rules = rules
        self.ie = InferenceEngine()

    def __repr__(self):
        return 'KnowledgeBase({!r}, {!r})'.format(self.facts, self.rules)

    def __str__(self):
        string = "Knowledge Base: \n"
        string += "\n".join((str(fact) for fact in self.facts)) + "\n"
        string += "\n".join((str(rule) for rule in self.rules))
        return string

    def _get_fact(self, fact):
        """INTERNAL USE ONLY
        Get the fact in the KB that is the same as the fact argument

        Args:
            fact (Fact): Fact we're searching for

        Returns:
            Fact: matching fact
        """
        for kbfact in self.facts:
            if fact == kbfact:
                return kbfact

    def _get_rule(self, rule):
        """INTERNAL USE ONLY
        Get the rule in the KB that is the same as the rule argument

        Args:
            rule (Rule): Rule we're searching for

        Returns:
            Rule: matching rule
        """
        for kbrule in self.rules:
            if rule == kbrule:
                return kbrule

    def kb_add(self, fact_rule):
        """Add a fact or rule to the KB
        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be added
        Returns:
            None
        """
        printv("Adding {!r}", 1, verbose, [fact_rule])
        if isinstance(fact_rule, Fact):
            if fact_rule not in self.facts:
                self.facts.append(fact_rule)
                for rule in self.rules:
                    self.ie.fc_infer(fact_rule, rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.facts.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.facts[ind].supported_by.append(f)
                else:
                    ind = self.facts.index(fact_rule)
                    self.facts[ind].asserted = True
        elif isinstance(fact_rule, Rule):
            if fact_rule not in self.rules:
                self.rules.append(fact_rule)
                for fact in self.facts:
                    self.ie.fc_infer(fact, fact_rule, self)
            else:
                if fact_rule.supported_by:
                    ind = self.rules.index(fact_rule)
                    for f in fact_rule.supported_by:
                        self.rules[ind].supported_by.append(f)
                else:
                    ind = self.rules.index(fact_rule)
                    self.rules[ind].asserted = True

    def kb_assert(self, fact_rule):
        """Assert a fact or rule into the KB

        Args:
            fact_rule (Fact or Rule): Fact or Rule we're asserting
        """
        printv("Asserting {!r}", 0, verbose, [fact_rule])
        self.kb_add(fact_rule)

    def kb_ask(self, fact):
        """Ask if a fact is in the KB

        Args:
            fact (Fact) - Statement to be asked (will be converted into a Fact)

        Returns:
            listof Bindings|False - list of Bindings if result found, False otherwise
        """
        print("Asking {!r}".format(fact))
        if factq(fact):
            f = Fact(fact.statement)
            bindings_lst = ListOfBindings()
            # ask matched facts
            for fact in self.facts:
                binding = match(f.statement, fact.statement)
                if binding:
                    bindings_lst.add_bindings(binding, [fact])

            return bindings_lst if bindings_lst.list_of_bindings else []

        else:
            print("Invalid ask:", fact.statement)
            return []

    def kb_retract(self, fact_rule):
        """Retract a fact or a rule from the KB

        Args:
            fact_rule (Fact or Rule) - Fact or Rule to be retracted

        Returns:
            None
        """
        printv("Retracting {!r}", 0, verbose, [fact_rule])
        ####################################################
        
        if read.parse_input(fact_rule).name == 'fact':
            """Represents a fact in our knowledge base. Has a statement containing the
                content of the fact, e.g. (isa Sorceress Wizard) and fields tracking
                which facts/rules in the KB it supports and is supported by.

            Attributes:
                name (str): 'fact', the name of this class
                statement (Statement): statement of this fact, basically what the fact actually says
                asserted (bool): boolean flag indicating if fact was asserted instead of
                    inferred from other facts and rules in the KB
                supported_by (listof listof Fact|Rule): Facts/Rules that allow inference of
                    the statement
                supports_facts (listof Fact): Facts that this fact supports
                supports_rules (listof Rule): Rules that this fact supports
            """
            name = read.parse_input(fact_rule).name
            statement =read.parse_input(fact_rule).statement
            asserted = read.parse_input(fact_rule).asserted
            supported_by = read.parse_input(fact_rule).supported_by
            supports_facts = read.parse_input(fact_rule).supports_facts
            supports_rules = read.parse_input(fact_rule).supports_rules
            
                   
            for i in self.facts:
                if i.statement == statement:
                    self.facts.remove(i)
            
            if len(supports_facts) > 0 :
                for i in self.facts:
                    if i in supports_facts:
                        i.supported_by.remove(fact_rule)
                        if len(i.supported_by) ==0 and i.asserted == False:
                            self.kb_retract(i)
            if len(supports_rules > 0):
                for i in self.rules:
                    if i in supports_rules:
                        i.supported_by.remove(fact_rule)
                        if len(i.supported_by) ==0 and i.asserted == False:
                            self.kb_retract(i)
                
        elif read.parse_input(fact_rule).name == 'rule':
            
            """Represents a rule in our knowledge base. Has a list of statements (the LHS)
                containing the statements that need to be in our KB for us to infer the
                RHS statement. Also has fields tracking which facts/rules in the KB it
                supports and is supported by.

            Attributes:
                name (str): 'rule', the name of this class
                lhs (listof Statement): LHS statements of this rule
                rhs (Statement): RHS statment of this rule
                asserted (bool): boolean flag indicating if rule was asserted instead of
                    inferred from other facts and rules in the KB
                supported_by (listof listof Fact|Rule): Facts/Rules that allow inference of
                    the statement
                supports_facts (listof Fact): Facts that this rule supports
                supports_rules (listof Rule): Rules that this rule supports
            """
            name = parse_input(fact_rule).name
            lhs = parse_input(fact_rule).lhs
            rhs = parse_input(fact_rule).rhs
            statement =parse_input(fact_rule).statement
            asserted = parse_input(fact_rule).asserted
            supported_by = parse_input(fact_rule).supported_by
            supports_facts = parse_input(fact_rule).supports_facts
            supports_rules = parse_input(fact_rule).supports_rules
            
            for i in self.rules:
                if i.statement == statement:
                    self.rules.remove(i)
                    
            if len(supports_facts) > 0 :
                for i in self.facts:
                    if i in supports_facts:
                        i.supported_by.remove(fact_rule)
                        if len(i.supported_by) ==0 and i.asserted == False:
                            self.kb_retract(i)
            if len(supports_rules > 0):
                for i in self.rules:
                    if i in supports_rules:
                        i.supported_by.remove(fact_rule)
                        if len(i.supported_by) ==0 and i.asserted == False:
                            self.kb_retract(i)
        else:
            return None


class InferenceEngine(object):
    def fc_infer(self, fact, rule, kb):
        """Forward-chaining to infer new facts and rules

        Args:
            fact (Fact) - A fact from the KnowledgeBase
            rule (Rule) - A rule from the KnowledgeBase
            kb (KnowledgeBase) - A KnowledgeBase

        Returns:
            Nothing
        """
        printv('Attempting to infer from {!r} and {!r} => {!r}', 1, verbose,
            [fact.statement, rule.lhs, rule.rhs])
        ####################################################
        bindings = match(rule.lhs[0],fact.statement)
        if bindings == False:
            return None
        else:
            new= Fact(instantiate(rule.rhs,bindings))
            rule.supports_facts.append(new)
            fact.supports_facts.append(new)
            kb.kb_add(new)
                
            