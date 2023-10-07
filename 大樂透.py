from bs4 import BeautifulSoup
import requests
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
import random
from openpyxl.cell import _writer


winning_Numbers_Sort_lotto=['Lotto649Control_history_dlQuery_No1_','Lotto649Control_history_dlQuery_No2_',
                            'Lotto649Control_history_dlQuery_No3_','Lotto649Control_history_dlQuery_No4_',
                            'Lotto649Control_history_dlQuery_No5_','Lotto649Control_history_dlQuery_No6_',
                            'Lotto649Control_history_dlQuery_SNo_']

def search_winning_numbers(css_class):
    global winning_Numbers_Sort_lotto
    if(css_class != None):
        for i in range(len(winning_Numbers_Sort_lotto )):
            if winning_Numbers_Sort_lotto [i] in css_class:
                return css_class    
def parse_tw_lotto_html(data_Info,number_count):  
    data_Info_List = []
    data_Info_Dict = {}
    tmp_index = 0
    for index  in range(len(data_Info)) :
        if (index == 0):
            data_Info_List.append(data_Info[index].text)  
        else:
            if(index % number_count != 0):
                data_Info_List.append(data_Info[index].text)
            else:
                data_Info_Dict[str(tmp_index)] = list(data_Info_List)
                data_Info_List= []
                data_Info_List.append(data_Info[index].text)
                tmp_index = tmp_index+1
        data_Info_Dict[str(tmp_index)] = list(data_Info_List)
    # 將 data_Info_Dict 反轉
    reversed_data_Info_Dict = {k: data_Info_Dict[k] for k in reversed(data_Info_Dict.keys())}
    return data_Info_List,reversed_data_Info_Dict

head_Html_lotto='http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'
res = requests.get(head_Html_lotto, timeout=30)
soup = BeautifulSoup(res.text,'lxml')
header_Info = soup.find_all(id=search_winning_numbers)
data_Info_List,data_Info_Dict  = parse_tw_lotto_html(header_Info,7)

# 轉換字典為 DataFrame
df = pd.DataFrame.from_dict(data_Info_Dict, orient='index')

#自訂索引值
df.columns = ['1','2','3','4','5','6','特別號']
#將前六列轉換為整數
df.iloc[:, 0:6] = df.iloc[:, 0:6].astype(int)
#對 DataFrame 的前六列進行加總
sums = df.iloc[:,0:6].sum(axis=1)
#在第7列中存儲加總結果
df['6顆號碼加總'] = sums  # 新增第7列為Sum
# 輸出到 Excel
output_filename = "lotto_results.xlsx"
df.to_excel(output_filename, engine='openpyxl', index=False)

# 使用apply方法將前六列組合成逗號分隔的字符串
df['combined'] = df.iloc[:, 0:6].apply(lambda row: ','.join(row.values.astype(str)), axis=1)
# 取得所有歷史開獎號碼組合
history_numbers = list(df['combined'])#使用 apply() 函數，
                                     #給定 axis=1 進行按行操作，
                                     #將前六列的值組合成逗號分隔的字符串，
                                     #並保存到一個新的列 'combined' 中。
                                     #函式set為高效率但是無排序
                                     #list有排序但是數據大的話會太慢                                    
#print(history_numbers)

#定義數組總和
def get_sum(numbers):
    return sum(map(int, numbers))
# 生成不重複的威力彩號碼
def generate_unique_numbers():
    # 取得最後三期的數據
    last_three_rows = df.iloc[-3:, 0:6]
    print(last_three_rows)
    sums = last_three_rows.apply(get_sum, axis=1)
    
    # 判斷三期總和的條件
    if all(s >= 160 for s in sums):
        target_sum = 160  # 使隨機生成的總和小於167       
    else:
        target_sum = 279
    print("目標總和:", target_sum) #確認
    while True: #如果上述判斷成立
        # 隨機生成六個數字
        numbers = random.sample(range(1, 50), 6)
        numbers_sum = sum(numbers)#確認
        numbers_str = ','.join(map(str, numbers))
        print("生成的號碼:", sorted(numbers), "| 總和:", numbers_sum)#確認
        # 檢查是否滿足總和與歷史開獎號碼的條件
        if numbers_str not in history_numbers and get_sum(numbers) < target_sum:
            return sorted(numbers)
        else:
            print("別買了，認真工作吧!")
# 這個函數用來顯示線型圖表視窗
def plot_graph():
    # 創建一個新的Tkinter視窗
    new_window = tk.Toplevel(app)
    new_window.title("Sum Over Time Graph")
    
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    df['6顆號碼加總'].plot(kind='line', title='Sum Over Time', xlabel='Index', ylabel='Sum', ax=ax)
    ax.set_xticks(range(10))
    
    canvas = FigureCanvasTkAgg(fig, master=new_window)  # 創建canvas將figure添加到Tkinter視窗中
    canvas.draw()
    canvas.get_tk_widget().pack()        

# 創建主視窗
app = tk.Tk()
app.title("大樂透頭獎號碼")
app.geometry("400x100")

# 創建標籤來顯示號碼
label = tk.Label(app, text="想致富嗎? 請按下按鈕!")
label.pack()
        
# 顯示號碼
def show_number():
    numbers = generate_unique_numbers()
    label.config(text=f"大樂透號碼：{numbers[:6]}") 
# 創建按鈕來生成號碼
button = tk.Button(app, text="一鍵致富", command=show_number)
button.place(x=100,y=50)
# 在您的主視窗中新增一個按鈕來生成線型圖表視窗
plot_button = tk.Button(app, text="顯示線型圖表", command=plot_graph)
plot_button.place(x=200,y=50)
# 運行主循環
app.mainloop()       