"""base class for all models"""

class BasePicture:
    """画像化のための基底クラス
    """
    def draw_url(self):
        """URLから画像を描画する
        """
        raise NotImplementedError
    
    def draw(self):
        """画像を描画する
        """
        raise NotImplementedError