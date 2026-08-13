import string
def delivery_scheme(m, s):
  if m == "premium" and s>500  :
    return "Delivery Charge: 0, Delivery Tier: Express"
  elif m == "premium" and s < 500 :
    return "Delivery Charge: 10, Delivery Tier: Priority"
  elif m == "standard" and s > 500:
    return "Delivery Charge: 0, Delivery Tier: Standard"
  elif m == "standard" and s < 500:
    return "Delivery Charge: 20, Delivery Tier: Economy"
  else:
    return "Invalid delivery scheme selected."

user_input_m = input("Enter membership type (premium/standard): ")
user_input_s = float(input("Enter the shopping cost: "))  
print(delivery_scheme(user_input_m, user_input_s))