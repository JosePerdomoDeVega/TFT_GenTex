from domain.prompts.manager_1 import debt_prompt, devs_prompt, stock_prompt, conclusion_prompt, recetas_prompt, cp_prompt, pvp_prompt


class PromptManager1:
    def __init__(self):
        self.debt_prompt = debt_prompt
        self.devs_prompt = devs_prompt
        self.stock_prompt = stock_prompt
        self.conclusion_prompt = conclusion_prompt
        self.recetas_prompt = recetas_prompt
        self.cp_prompt = cp_prompt
        self.pvp_prompt = pvp_prompt

    def get_prompt(self, indicator):

        if indicator == "deuda":
            return self.debt_prompt
        elif indicator == "devoluciones":
            return self.devs_prompt
        elif indicator == "stock":
            return self.stock_prompt
        elif indicator == "conclusion":
            return self.conclusion_prompt
        elif indicator == "recetas":
            return self.recetas_prompt
        elif indicator == "codigos_propios":
            return self.cp_prompt
        elif indicator == "pvp":
            return self.pvp_prompt

        return None
