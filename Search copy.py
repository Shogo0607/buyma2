import time
import pandas as pd
from selenium import webdriver
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.keys import Keys
import datetime
from datetime import datetime as dt
from datetime import timedelta,timezone
import streamlit as st
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager

st.set_page_config(page_title="BUYMA 問い合わせ検索ツール")

# JST = timezone(timedelta(hours=+9), 'JST')
st.title("BUYMA Search tool")

st.sidebar.title("BUYMA Search tool")

max_list =  int(st.sidebar.number_input("1Pageの検索商品数",value=2))
max_page =   int(st.sidebar.number_input("検索ページ数",value=2))
item = st.sidebar.selectbox("ブランド名",['HERMES','CHANEL','CHRISTIAN DIOR','LUIS VUITTON'])

now = dt.now() + datetime.timedelta(hours = 9)
past_day = now - datetime.timedelta(days = 1)
max_day =  int(st.sidebar.number_input("本日から過去遡って検索する日数",value=1))

if item == "HERMES":
    url = 'https://www.buyma.com/r/_HERMES-%E3%82%A8%E3%83%AB%E3%83%A1%E3%82%B9'
elif item == 'CHANEL':
    url = 'https://www.buyma.com/r/_CHANEL-%E3%82%B7%E3%83%A3%E3%83%8D%E3%83%AB'
elif item == 'CHRISTIAN DIOR':
    url = 'https://www.buyma.com/r/_CHRISTIAN-DIOR-%E3%82%AF%E3%83%AA%E3%82%B9%E3%83%81%E3%83%A3%E3%83%B3%E3%83%87%E3%82%A3%E3%82%AA%E3%83%BC%E3%83%AB'
elif item == 'LUIS VUITTON':
    url = 'https://www.buyma.com/r/_LOUIS-VUITTON-%E3%83%AB%E3%82%A4%E3%83%B4%E3%82%A3%E3%83%88%E3%83%B3'

bar = st.progress(0)
if st.sidebar.button("検索開始"):
    
    st.markdown("1. 検索ツールを立ち上げます。")

    with st.spinner("現在検索ツール立ち上げ中"):
        now = dt.now() + datetime.timedelta(hours=9)
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')  
        chrome_options.add_argument('--disable-dev-shm-usage') 
        # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation', 'enable-logging'])
        print('>処理開始')
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.maximize_window()
        driver.implicitly_wait(5)

        item_list = list()
        item_url_list = list()
        inq_url_list = list()
        item_price_list = list()
        item_list_question_time = list()
        item_list_question_questioner = list()
        item_list_question_question = list()
        item_list_answer_time = list()
        item_list_answer_answerer = list()
        item_list_answer_answer = list()
        item_number_list = list()
        # st.success("検索ツール立ち上げ完了")
    
    count = 0
    st.markdown("2. 問い合わせページを検索します。")
    with st.spinner("問い合わせページを検索中..."):
        for page in range(1,max_page+1):  #商品のページ数
            for shop_id in range(1,max_list+1):  #1ページの最大掲載数
                
                count += 1
                progress = int((count) /(max_page * max_list)*100)
                

                if page ==1:
                    driver.get(url+'/')
                else:
                    driver.get(url+'_'+str(page)+'/')

                item_list_xpath = '//*[@id="n_ResultList"]/ul/li['+str(shop_id)+']/div[3]/div[1]/a'
                item_list_text = driver.find_element(By.XPATH, item_list_xpath).text
                # driver.find_element(By.XPATH, item_list_xpath).click()
                element = driver.find_element(By.XPATH, item_list_xpath)
                driver.execute_script("arguments[0].click();", element)
                time.sleep(2)
                with st.spinner(item_list_text+"の問い合わせを検索中..."):
                    bar.progress(progress)
                    item_url = str(driver.current_url)
                    item_number_label_xpath = '//*[@id="s_season"]/dt'
                    
                    try:
                        item_number_label = driver.find_element(By.XPATH, item_number_label_xpath).text
                        item_number_xpath = '//*[@id="s_season"]/dd/span'
                        item_number = driver.find_element(By.XPATH, item_number_xpath).text
                    except:
                        item_number = ""

                    try:
                        item_price_xpath = '//*[@id="abtest_display_pc"]'
                        item_price = driver.find_element(By.XPATH, item_price_xpath).text
                    except:
                        item_price_xpath = '//*[@id="priceWrap"]/div/p[4]/span'
                        item_price = driver.find_element(By.XPATH, item_price_xpath).text

                    inq_url = item_url+'inq'
                    driver.get(inq_url+"/")
                    time.sleep(2)
                    inq_max_num_xpath = '//*[@id="tabmenu_inqcnt"]'
                    inq_max_num = driver.find_element(By.XPATH, inq_max_num_xpath).text
                    inq_max_num = int(int(inq_max_num)//10)+2
                    flag = 0
                    for inq_page in range(1,inq_max_num):
                        if flag == 1:
                            break
                        if inq_page == 1:
                            pass
                        else:
                            try:
                                driver.get(inq_url+"_"+str(inq_page)+"/")
                                time.sleep(2)
                            except:
                                break
                        for inq_num in range(1,11):
                            item_list_question_time_xpath = '//*[@id="color-size-form"]/div[4]/div[3]/div[1]/div[3]/div['+str(inq_num)+']/div[1]/span/div'
                            item_list_question_questioner_xpath = '//*[@id="color-size-form"]/div[4]/div[3]/div[1]/div[3]/div['+str(inq_num)+']/div[1]/div/p[1]/a'
                            item_list_question_question_xpath = '//*[@id="color-size-form"]/div[4]/div[3]/div[1]/div[3]/div['+str(inq_num)+']/div[1]/div/p[2]'
                            item_list_answer_time_xpath = '//*[@id="color-size-form"]/div[4]/div[3]/div[1]/div[3]/div['+str(inq_num)+']/div[2]/span/div'
                            item_list_answer_answerer_xpath = '//*[@id="color-size-form"]/div[4]/div[3]/div[1]/div[3]/div['+str(inq_num)+']/div[2]/div/p[1]/a'
                            item_list_answer_answer_xpath = '//*[@id="color-size-form"]/div[4]/div[3]/div[1]/div[3]/div['+str(inq_num)+']/div[2]/div/p[2]'
                            try:
                                item_list_question_time_text = driver.find_element(By.XPATH, item_list_question_time_xpath).text
                                item_list_question_questioner_text = driver.find_element(By.XPATH, item_list_question_questioner_xpath).text
                                item_list_question_question_text = driver.find_element(By.XPATH, item_list_question_question_xpath).text
                            except:
                                break

                            try:
                                item_list_answer_time_text = driver.find_element(By.XPATH, item_list_answer_time_xpath).text
                                item_list_answer_answerer_text = driver.find_element(By.XPATH, item_list_answer_answerer_xpath).text
                                item_list_answer_answer_text = driver.find_element(By.XPATH, item_list_answer_answer_xpath).text
                            except:
                                item_list_answer_time_text = str("")
                                item_list_answer_answerer_text = str("")
                                item_list_answer_answer_text = str("")

                            if "時間前" in item_list_question_time_text:
                                delta = int(item_list_question_time_text.strip("時間前"))
                                past = now - datetime.timedelta(hours = delta)
                                past = str(now.year)+"/"+str(now.month)+"/"+str(now.day)+" "+str(now.hour)+":"+str(now.minute)
                                item_list.append(item_list_text)
                                item_url_list.append(item_url)
                                inq_url_list.append(inq_url)
                                item_price_list.append(item_price.strip("¥,"))
                                item_number_list.append(item_number)
                                item_list_question_time.append(past)
                                item_list_question_questioner.append(item_list_question_questioner_text)
                                item_list_question_question.append(item_list_question_question_text)
                                item_list_answer_time.append(item_list_answer_time_text)
                                item_list_answer_answerer.append(item_list_answer_answerer_text)
                                item_list_answer_answer.append(item_list_answer_answer_text)

                            elif "分前" in item_list_question_time_text:
                                delta = int(item_list_question_time_text.strip("分前"))
                                past = now - datetime.timedelta(minute = delta)
                                past = str(now.year)+"/"+str(now.month)+"/"+str(now.day)+" "+str(now.hour)+":"+str(now.minute)
                                item_list.append(item_list_text)
                                item_url_list.append(item_url)
                                inq_url_list.append(inq_url)
                                item_price_list.append(item_price.strip("¥,"))
                                item_number_list.append(item_number)
                                item_list_question_time.append(past)
                                item_list_question_questioner.append(item_list_question_questioner_text)
                                item_list_question_question.append(item_list_question_question_text)
                                item_list_answer_time.append(item_list_answer_time_text)
                                item_list_answer_answerer.append(item_list_answer_answerer_text)
                                item_list_answer_answer.append(item_list_answer_answer_text)

                            elif "/" in item_list_question_time_text:
                                past = dt.strptime(item_list_question_time_text, '%Y/%m/%d %H:%M')
                                delta = now - past
                                if delta.days < 0:
                                    break
                                elif delta.days > max_day-1:
                                    flag = 1
                                    break
                                else:
                                    item_list.append(item_list_text)
                                    item_url_list.append(item_url)
                                    inq_url_list.append(inq_url)
                                    item_price_list.append(item_price.strip("¥,"))
                                    item_number_list.append(item_number)
                                    item_list_question_time.append(item_list_question_time_text)
                                    item_list_question_questioner.append(item_list_question_questioner_text)
                                    item_list_question_question.append(item_list_question_question_text)
                                    item_list_answer_time.append(item_list_answer_time_text)
                                    item_list_answer_answerer.append(item_list_answer_answerer_text)
                                    item_list_answer_answer.append(item_list_answer_answer_text)
                            else:
                                break

    with st.spinner("検索結果をCSVファイルにまとめています。"):
        item_list = pd.DataFrame(item_list)
        item_url_list = pd.DataFrame(item_url_list)
        inq_url_list = pd.DataFrame(inq_url_list)
        item_price_list = pd.DataFrame(item_price_list)
        item_number_list = pd.DataFrame(item_number_list)
        item_list_question_time = pd.DataFrame(item_list_question_time)
        item_list_question_questioner = pd.DataFrame(item_list_question_questioner)
        item_list_question_question = pd.DataFrame(item_list_question_question)
        item_list_answer_time = pd.DataFrame(item_list_answer_time)
        item_list_answer_answerer = pd.DataFrame(item_list_answer_answerer)
        item_list_answer_answer = pd.DataFrame(item_list_answer_answer)

        try:
            all_data = pd.concat([item_list,item_price_list,item_url_list,inq_url_list,item_number_list,item_list_question_time,item_list_question_questioner,item_list_question_question,item_list_answer_time,item_list_answer_answerer,item_list_answer_answer],axis=1)
            all_data.columns = ["アイテム名","値段","アイテムURL","問い合わせURL","ブランド型番","問い合わせ時間","問い合わせユーザ名","問い合わせ内容","回答時間","回答者","回答内容"]
            st.dataframe(all_data)
            all_data.to_csv("問い合わせ検索結果.csv",index=False)

            @st.cache()
            def convert_df(df):
                # IMPORTANT: Cache the conversion to prevent computation on every rerun
                return df.to_csv().encode('utf-8-sig')
            csv = convert_df(all_data)
            st.download_button(label="Download",data=csv,file_name='問い合わせ検索結果.csv',mime='text/csv',)
        except:
            st.warning("検索条件に合う結果がありませんでした。")
    driver.close()
    st.success("正常に終了しました。")

else:
    st.warning("検索開始ボタンを押すと、検索を開始します。")