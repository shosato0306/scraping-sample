import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

# 動作確認用に e-kanagawa 秦野市の施設予約サイトから
# 「スポーツ施設」を選択 →「メタックス体育館はだの」→ 「日時指定」→「時間帯別空き状況」ページに遷移し、
# 「メタックス体育館はだの/メインアリーナの今日の空き情報」を取得するスクレイピング処理を実装

hadano_top_page_url = 'https://yoyaku.e-kanagawa.lg.jp/Hadano/Web/Wg_ModeSelect.aspx'
hadano_top_page_sport_facility_id = 'dlSSCategory_ctl00_btnSSCategory'
hadano_facilities_page_metax_id = 'dgShisetsuList_ctl02_chkSelectLeft'
footer_forward_button_id = 'ucPCFooter_btnForward'


def scrape():
    # WebDriverの設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # ヘッドレスモードを使用

    # WebDriverの起動
    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(10)

    # はだの市施設予約トップページにアクセス
    driver.get(hadano_top_page_url)

    # スポーツ施設ボタンをクリックしてスポーツ施設一覧ページに遷移
    driver.find_element(By.ID, hadano_top_page_sport_facility_id,).click()

    # メタックス体育館はだのをクリック
    driver.find_element(By.ID, hadano_facilities_page_metax_id,).click()

    # フッターの「次へ」ボタンをクリック
    driver.find_element(By.ID, footer_forward_button_id,).click()

    # 現在の日時を取得
    now = datetime.datetime.now()

    # 表示形式を「横表示」に設定
    driver.find_element(By.NAME, "rbYoko").click()

    # 表示開始日を設定（年、月、日）
    driver.find_element(By.NAME, "txtYear").clear()
    driver.find_element(By.NAME, "txtYear").send_keys(str(now.year))
    driver.find_element(By.NAME, "txtMonth").clear()
    driver.find_element(By.NAME, "txtMonth").send_keys(str(now.month))
    driver.find_element(By.NAME, "txtDay").clear()
    driver.find_element(By.NAME, "txtDay").send_keys(str(now.day))

    # 表示期間を「1週間」に設定
    driver.find_element(By.NAME, "rbtnWeek").click()
    # 表示時間帯を「全日」に設定
    driver.find_element(By.NAME, "rbtnAllday").click()

    # フッターの「次へ」ボタンをクリック
    driver.find_element(By.ID, footer_forward_button_id).click()

    # ページの先頭に表示されている施設/日付のセルIDをクリック
    formatted_date = now.strftime('%Y%m%d')
    first_id = f"dlRepeat_ctl00_tpItem_dgTable_ctl02_b{formatted_date}"
    driver.find_element(By.ID, first_id).click()

    # フッターの「次へ」ボタンをクリック
    driver.find_element(By.ID, footer_forward_button_id).click()

    # 行ごとの情報を格納するリスト
    rows_info = []

    # table要素を取得
    rows = driver.find_elements(
        By.XPATH, '//table[@id="dlRepeat_ctl00_tpItem_dgTable"]/tbody/tr')

    for row in rows:
        # 行内の各セルを取得
        cells = row.find_elements(By.TAG_NAME, 'td')

        # 行の情報を格納するための辞書
        row_info = {"name": "", "capacity": "", "availability": []}

        if cells:
            # 施設のエリア名（例：「(全面)」）を取得
            row_info["name"] = cells[0].text if len(cells) > 0 else ""

            # 定員情報を取得
            row_info["capacity"] = cells[1].text if len(cells) > 1 else ""

            # 時間帯別の空き情報を取得
            row_info["availability"] = [cell.text.strip()
                                        for cell in cells[2:]]

        # 行の情報をリストに追加
        rows_info.append(row_info)

    # 現在の日付を取得して指定の形式で文字列に変換
    formatted_date = now.strftime('%Y年%m月%d日(%a)')

    print("時間帯別空き情報: ", formatted_date)
    print("-" * 40)

    for row in rows_info:
        if row["name"].startswith("（") and row["name"].endswith("）"):
            print(f'施設エリア名: {row["name"]}')
            print(f'定員: {row["capacity"]}')

            for i, availability in enumerate(row["availability"]):
                # 時間帯と空き状況を表示
                time_range = rows_info[0]["availability"][i].replace(
                    "\n", " ")
                print(f'{time_range}: {availability}')

            print("-" * 40)

    # WebDriverの終了
    driver.quit()
