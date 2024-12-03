from bs4 import BeautifulSoup
from selenium import webdriver
import pytest

class TestGameMaster:
    """
    GameMaster のテスト
    """
    def test_title(self, html: str) -> None:
        """
        title の確認
        """
        soup = BeautifulSoup(html, "html.parser")

        targets = {"title": "Nap CLI"}

        for target_id, tareget_value in targets.items():
            target_element = soup.find(id=target_id)

            if target_element:
                target_text = target_element.get_text()
                assert target_text == tareget_value

            else:
                raise Exception(f"ID '{target_id}' が見つかりませんでした。")
 
        targets = ["VS Takeshi Lv.1", "VS Takeshi Lv.2", "VS Shizuka Lv.1", "VS Shizuka Lv.2"]

        for target_id in targets:
            target_element = soup.find(id=target_id)

            if target_element:
                target_text = target_element.get_text()
                target_value = target_element["value"]
                assert target_text == target_id
                assert target_value == target_id

            else:
                raise Exception(f"ID '{target_id}' が見つかりませんでした。")

    @pytest.mark.parametrize(
        [
            "target_game",
        ],
        [
            pytest.param(
                "VS Takeshi Lv.1"
            ),
            pytest.param(
                "VS Takeshi Lv.1"
            ),
        ]
    )
    def test_start(self, driver: webdriver.Chrome, target_game: str) -> None:
        """
        start_method で作成されたゲームのボタンをクリックする

        Args:
            driver (webdriver.Chrome): web driver
            target_game (str): 実行するゲーム名
        """
        driver.find_element("id", target_game).click()
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")

        targets = {"title": target_game}

        for target_id, tareget_value in targets.items():
            target_element = soup.find(id=target_id)

            if target_element:
                target_text = target_element.get_text()
                assert target_text == tareget_value

            else:
                raise Exception(f"ID '{target_id}' が見つかりませんでした。")
        
        # feild の状態を確認
        feild_element = soup.find(id="feild")
        feild_text = feild_element.get_text()
        assert "山札: 46" in feild_text

        # 表示されているボタンの内容の確認
        button_elements = soup.find(id="buttons")
        for button_element in button_elements:
            button_text = button_element.get_text()
            assert button_text == "Next"

