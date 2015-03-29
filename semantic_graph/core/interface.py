
class Interface:

    def getMainMenu(self):
        return (
            '1 - Load data.\n'
            '2 - Apply Inference Rule "specie belongs to class".\n'
            '3 - Apply Inference Rule "specie belongs to order".\n'
            '4 - Apply Inference Rule "family belongs to class".\n'
            '5 - List "belongs to class" inference.\n'
            '6 - Show graph\n'
            '0 - Sair.'
        )