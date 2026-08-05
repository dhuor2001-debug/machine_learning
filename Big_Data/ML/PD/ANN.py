x1 =1
x2 =2
w1 =0.5
w2 =0.3
threshold = 0.7
net_input = x1 * w1 + x2 * w2
if net_input >= threshold:
    print("Output = 1")
else:
    print("Output = 0")
