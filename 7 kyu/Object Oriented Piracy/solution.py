54fe05c4762e2e3047000add


class Ship:
    def __init__(self, draft, crew):
        self.draft = draft
        self.crew = crew
    def is_worth_it(self):
        return self.draft > 20 + (1.5 * self.crew)
__________________________________
class Ship:
    def __init__(self, draft, crew):
        self.draft = draft
        self.crew  = crew
        self.worth = 20 < draft - 1.5 * crew
        
    def is_worth_it(self): return self.worth
__________________________________
class Ship:
    def __init__(self, draft, crew):
        self.draft = draft
        self.crew = crew
        self.is_worth_it = lambda: self.draft - self.crew * 1.5 > 20
__________________________________
class Ship:
    def __init__(self, draft, crew):
        self.draft = draft
        self.crew = crew
    def is_worth_it(self):
        draft_after_ppl_subbed = (self.draft - (self.crew * 1.5)) >= 20
        return draft_after_ppl_subbed
__________________________________
class Ship:
    def __init__(self, draft, crew):
        self.draft = draft
        self.crew = crew
    def is_worth_it(self):    
        if (self.draft-self.crew*1.5) >20:
            return 1
        else:
            return 0
