from .player import Player

class Takeshi(Player):
    """
    たけしは、手札公開の際に、マークの情報をくれる
    """
    def __init__(self):
        super().__init__(name = "たけし", cpu = True)

    def show_hand(self):
        """Show hand.
        手札を開示する

        Return
            list[Card]: 開示する情報
        """
        return super().show_hand(hint="mark-1")
