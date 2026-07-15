"""
Demo: 变量与格式化输出
"""

name = "传智播客"
stock_code = "003032"
stock_price = 19.99
daily_growth = 1.2
growth_days = 7
present_price = stock_price * daily_growth ** growth_days

print(f"公司: {name}  股票代码: {stock_code}  当前股价: {present_price:.2f}")
