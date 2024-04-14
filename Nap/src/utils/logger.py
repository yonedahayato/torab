import logging

class Logger:
    """
    ロギングを行うクラス
    """
    def __init__(self, is_use_print = True):
        """
        
        Args:
            is_use_print: print 構文 を使うかどうか
        """
        self.is_use_print = is_use_print
        
    def log_print(self, message):
        """
        標準出力への表示
        """
        print(message)