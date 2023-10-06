# 爬蟲與圖表練習
winning_Numbers_Sort_lotto=['Lotto649Control_history_dlQuery_No1_','Lotto649Control_history_dlQuery_No2_',
                            'Lotto649Control_history_dlQuery_No3_','Lotto649Control_history_dlQuery_No4_',
                            'Lotto649Control_history_dlQuery_No5_','Lotto649Control_history_dlQuery_No6_',
                            'Lotto649Control_history_dlQuery_SNo_']


轉換字典為 DataFrame
df = pd.DataFrame.from_dict(data_Info_Dict, orient='index')

#自訂索引值
df.columns = ['1','2','3','4','5','6','特別號']

# 輸出到 Excel
output_filename = "lotto_results.xlsx"
df.to_excel(output_filename, engine='openpyxl', index=False)

#使用全局變數
FILE_PATH = "D:/python/lotto_results.xlsx" 
#定義讀取已存儲的 Excel 文件
def load_lotto_results(file_path=FILE_PATH):
    return pd.read_excel(file_path)

#使用load_lotto_results的函式
df = load_lotto_results() 
#對 DataFrame 的前六列進行加總
sums = df.iloc[:, 0:6].sum(axis=1)

#在第7列中存儲加總結果
df['6顆號碼加總'] = sums  # 新增第7列為Sum


# 使用 pandas 內建的 plot 方法繪製線形圖
#df['6顆號碼加總'].plot(kind='line', title='Sum Over Time', xlabel='Index', ylabel='Sum')
# 設定x軸的刻度為0到9
#plt.xticks(range(10))
# 使用 matplotlib 顯示圖形
#plt.show()

df = load_lotto_results()

# 使用apply方法將前六列組合成逗號分隔的字符串
# 取得所有歷史開獎號碼組合
#使用 apply() 函數，給定 axis=1 進行按行操作，將前六列的值組合成逗號分隔的字符串，並保存到一個新的列 'combined' 中。函式set為高效率但是無排序list有排序但是數據大的話會太慢
history_numbers = list(df['combined'])

#定義數組總和
def get_sum(numbers):
    return sum(map(int, numbers))
# 生成不重複的威力彩號碼       
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

# 創建主視窗zArithmeticError
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

#print(data_Info_Dict)
