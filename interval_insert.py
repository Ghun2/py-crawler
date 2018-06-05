import thatactor_f as ta

lat = ta.latest_Data_ex()

# print(lat)
for i in range(1,20):
    if ta.parse_flim_web(i,lat) == 0 :
        break
# print(ta.new)

if len(ta.new) == 10:
    ta.latest_Data_in(ta.new)
else :
    for v in range(len(ta.new)-1,-1,-1):
        # print("ta.new = ",v)
        lat.pop()
        lat.insert(0,ta.new[v])
    ta.latest_Data_in(lat)

# print(len(ta.new))
ta.logging("page = "+str(i)+" srl = "+str(lat[0]))
# print(ta.new)
# lat = ta.latest_Data_ex()
# print(lat)
