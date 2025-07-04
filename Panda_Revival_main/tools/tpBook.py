import random
import copy
from gdpc import editor
import numpy as np

city_name_list=[
    "Baihualin", "Longxicheng", "Xionghua", "Heifeng", "Zhulinshan",
    "Yunxi", "Huanjing", "Fengmao", "Lianxi", "Xingbai",
    "Meilin", "Qingshan", "Baoxiang", "Chonglin", "Moxia",
    "Huashan", "Xiongyi", "Beihua", "Tangzhu", "Luyincheng"
]




def tpBook(editor,search_area,area,building_dict_list,height_list,under_entrance):
    coor=[]
    build_list=[]
    page_num=len(search_area)
    print(page_num)
    if(page_num<=len(city_name_list)):
        city_name_cand=random.sample(city_name_list,page_num)
    else:
        city_name_cand=random.choices(city_name_list,k=page_num)
    for i in range(len(building_dict_list)):
        build_list.append(list(building_dict_list[i].values()))
    city_info_list=city_info(build_list)

    base_code=f"give @p written_book[minecraft:written_book_content={{author:\"panda_revival_team\",title:\"City inforation Book\",pages:["
    for i in range(page_num):
        if(i==0):#初めの街(地下のある町)
            city_info_text=f"This city has an entrance to the underground.\\\\nGo to the center of the tower."
            coor=copy.copy(under_entrance)
        else:
            city_info_text=city_info_list[i]
            coor[0]=area[0]+search_area[i][0]+search_area[i][2]/2
            coor[1]=height_list[i]+2
            coor[2]=area[1]+search_area[i][1]+search_area[i][3]/2

        page_1=f"\'[[\"city name:{city_name_cand[i]}\\\\n\","
        page_2=f"{{\"text\":\"city coor:{coor[0]},{coor[1]},{coor[2]}\\\\n\",\"color\":\"#0000ff\",\"underlined\":true,"
        page_3=f"\"clickEvent\":{{\"action\":\"run_command\",\"value\":\"/tp {coor[0]} {coor[1]} {coor[2]}\"}},"
        page_4=f"\"hoverEvent\":{{\"action\":\"show_text\",\"contents\":\"Click for TP\"}}}},"
        page_5=f"\"Cityinfo\\\\n{city_info_text}\""
        page_6=f"]]\'"
        base_code+=page_1+page_2+page_3+page_4+page_5+page_6
        if(i!=page_num-1):
            base_code+=","
    base_code_end=f"]}}]"
    command=base_code+base_code_end
    print(command)
    editor.runCommand(command)
    #用途:テレポートできる本の配布





def city_info(build_list):
    city_info_list=["" for i in range(len(build_list))]
    match_lists=[]
    target_list=["honey","house","store","basement","bracksmith","tower","pavilion","farm"]
    flag_list=[-1,-1,-1,-1,-1,-1,-1,-1]

    for i in range(len(build_list)):
        match_list=[]
        for j in range(len(target_list)):
            target=target_list[j]
            if(target=="farm"):
                matched= [word for word in build_list[i] if target == word]
            else:
                matched= [word for word in build_list[i] if target in word] 
            match_list.append(len(matched))
        match_lists.append(match_list)
    match_lists=np.array(match_lists)
    match_lists_base=match_lists.copy() #コピーを作成
    build_count=[]
    for i in range(len(target_list)):
        column=match_lists[:,i]
        num = np.count_nonzero(column)
        build_count.append(num)
    build_count=np.array(build_count)
    sort_build_count=build_count.argsort()
    for i in range(len(target_list)):
        if(build_count[sort_build_count[i]]!=0):
            for j in range(len(target_list)):
                if(sort_build_count[i]==j and flag_list[j]==-1):
                    max_count =max(match_lists[:,j])
                    if(max_count!=0):
                        for k in range(len(build_list)):
                            if(match_lists[k,j]==max_count):
                                flag_list[j]=k
                                match_lists[k]=0
                                break
                        
    print(flag_list)
    for i in range(len(flag_list)):
        if(flag_list[i]!=-1):
            if(i==0):
                city_info_list[flag_list[i]]=f"Beekeeping is thriving in this town"
            elif(i==1):
                city_info_list[flag_list[i]]=f"Many pandas live in this town"
            elif(i==2):
                city_info_list[flag_list[i]]=f"This town has a wide variety of stores"
            elif(i==3):
                city_info_list[flag_list[i]]=f"There is an underground storage facility at the end of a well somewhere in this town."
            elif(i==4):
                city_info_list[flag_list[i]]=f"High quality iron tools are made in this town."
            elif(i==5):
                city_info_list[flag_list[i]]=f"The tower in this town was built to mourn the pandas who died in the underground city."
            elif(i==6):
                city_info_list[flag_list[i]]=f"The town\\\'s pavilion is a haven for many pandas."
            elif(i==7):
                city_info_list[flag_list[i]]=f"The crops produced on this farm support the livelihood of the pandas."

    for i in range(len(city_info_list)):
        if(len(city_info_list[i])==0): #特色なし
            text=f""
            house_count=match_lists_base[i,1]  
            store_count=match_lists_base[i,2] 
            if(house_count!=0):
                text+=f"house:{house_count}\\\\n"
            if(store_count!=0):
                text+=f"store:{store_count}\\\\n"
            if(len(text)):
                text+=f"There are no pandas in this town!!!"
            city_info_list[i]=text

    return city_info_list
