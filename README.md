# 爬蟲與圖表練習
轉換字典為 DataFrame
df = pd.DataFrame.from_dict(data_Info_Dict, orient='index')

自訂索引值
df.columns = ['1','2','3','4','5','6','特別號']

輸出到 Excel
output_filename = "lotto_results.xlsx"
df.to_excel(output_filename, engine='openpyxl', index=False)

使用全局變數
FILE_PATH = "D:/python/lotto_results.xlsx" 
定義讀取已存儲的 Excel 文件
def load_lotto_results(file_path=FILE_PATH):
    return pd.read_excel(file_path)

用load_lotto_results的函式
df = load_lotto_results() 
對DataFrame 的前六列進行加總
sums = df.iloc[:, 0:6].sum(axis=1)
在第7列中存儲加總結果，
使用 pandas 內建的 plot 方法繪製線形圖，
使用apply方法將前六列組合成逗號分隔的字符串，
取得所有歷史開獎號碼組合，
使用 apply() 函數，給定 axis=1 進行按行操作，將前六列的值組合成逗號分隔的字符串，並保存到一個新的列 'combined' 中。函式set為高效率但是無排序list有排序但是數據大的話會太慢。
定義數組總和，
生成不重複的威力彩號碼， 
def plot_graph():
這個函數用來顯示線型圖表視窗，
創建主視窗zArithmeticError，
創建標籤來顯示號碼，
顯示號碼，
創建按鈕來生成號碼，
在您的主視窗中新增一個按鈕來生成線型圖表視窗，
運行主循環，
