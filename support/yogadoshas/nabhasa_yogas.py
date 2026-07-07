import support.generic as gen
import support.yogadoshas.common as common

def ParivarthanaYoga(charts):
    global IsParivarthanaYogaPresent
    IsParivarthanaYogaPresent = False
    
    Name = ""
    yogatype = ""
    Rule = ""
    Results = ""
    Note = ""
    cnt = 0
    #Check for existance of Parivarthana Yoga 
    plist = []
    for focusPlanet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if ((focusPlanet in plist) == False):
            focusDispositor = charts["D1"]["planets"][focusPlanet]["dispositor"]
            dispositor_of_Dispositor = charts["D1"]["planets"][focusDispositor]["dispositor"]
            if (dispositor_of_Dispositor == focusPlanet) and (focusDispositor != focusPlanet):
                IsParivarthanaYogaPresent = True 
                cnt = cnt + 1
                plist.append(focusPlanet)
                plist.append(focusDispositor)
                planethouse = charts["D1"]["planets"][focusPlanet]["house-num"]
                dispohouse = charts["D1"]["planets"][focusDispositor]["house-num"]
                #Find type of parivarthana yoga
                #if both houses belong to group [1,2,4,5,7,9,10,11] then its maha yoga
                if ((planethouse in [1,2,4,5,7,9,10,11]) and (dispohouse in [1,2,4,5,7,9,10,11])):
                    yogatype = "Maha"
                    Results = f'''According to Phaladeepika, the person born with Mahayoga will have the beneficence of the Goddess Sri and will be adorned with expensive and beautiful clothes and ornaments. He is reverred and honoured by the king. He will hold a high position and will be rewarded of authority by the king, He will be blessed with sons and fully enjoy wealth and conveyances.'''
                #if one house belong to group [1,2,4,5,7,9,10,11] and otrher house is 3 then its kahala yoga
                elif(((planethouse in [1,2,4,5,7,9,10,11]) and (dispohouse == 3)) or
                    ((dispohouse in [1,2,4,5,7,9,10,11]) and (planethouse == 3))):
                    yogatype = "Kahala"
                    Results = f'''According to Phaladeepika, the native with Kahala Yoga will occasionally be haughtly and sometimes sweet in his speech. There will be occasions when he will be very prosperous and then will be driven to poverty, unhappiness and misery.'''
                else:
                    yogatype = "Dainya"
                    Results = f'''According to Phaladeepika, the person with Dainya Yoga at birth will be a fool, will revile others and indulge in sinful deeds. He is always in trouble from his enemies. He will speak harshly and will not have a stable mind. He will encounter obstacles in all his ventures.'''
                
                #form the name
                Name = f'''{yogatype} Parivarthana Yoga - {focusPlanet}[{planethouse}] with {focusDispositor}[{dispohouse}]'''
                Rule = f'''{focusPlanet} and  {focusDispositor} are placed in each others Sign. This forms a Parivarthana Yoga. Since the House owners of houses {planethouse} and {dispohouse} have exchanged positions, it is a {yogatype} Yoga.'''
                Note = f'''Due to this parivarthana yoga house - {planethouse} and house - {dispohouse} has formed a relationship. So deduce the results of that accordingly additional to results given here.'''

                relevant_planets = [focusPlanet[0:2], focusDispositor[0:2]]
                colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
                colorlist[planethouse-1] = "yellow"
                colorlist[dispohouse-1] = "yellow"
                Title = f'''PARIVARTHANA YOGA {cnt}'''


                #Update the yogadosha sections
                common.yogadoshas_dict[Title] = {}
                common.yogadoshas_dict[Title]["name"] = Name
                common.yogadoshas_dict[Title]["type"] = "Yoga"
                common.yogadoshas_dict[Title]["exist"] = IsParivarthanaYogaPresent
                common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
                common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
                common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
                common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
                common.yogadoshas_dict[Title]["Source"] = ""

                common.parivarthanaYogas.append(Name)

    return IsParivarthanaYogaPresent

#Nabhasa Yogas - All planetary positions
#Aashraya Yogas -  Depending on if all planets are in Movable(1,4,7,10), Fixed(2,5,8,11) or Dual(3,6,9,12) signs
def AashrayaYoga(charts):
    
    global IsAshrayaYogaPresent
    IsAshrayaYogaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Title = ""
    relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa"]
    colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        
    planetnatures = []
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        planet_signnature = gen.sign_nature[charts["D1"]["planets"][planet]["sign"]]
        colorlist[charts["D1"]["planets"][planet]["house-num"]-1] = "yellow"
        if (planet_signnature not in planetnatures):
            planetnatures.append(planet_signnature)
    
    if (len(planetnatures) == 1):
        IsAshrayaYogaPresent = True
        if ("Movable" in planetnatures):
            #this is Rajju Yoga (All planets are in Movable signs)
            Title = "RAJJU"
            Name = "Rajju Aashraya Nabhasa"
            common.AshrayaYogas.append("Rajju Aashraya Nabhasa Yoga")
            Rule = f'''All 7 planets from Sun to Saturn are in Movable Signs [Chara]. Hence Rajju Yoga is formed which is one of 3 types of Ashraya yogas in Nabhasa yogas.'''
            Results = f'''According to Parashara, One born in Rajju Yog will be fond of wandering, be charming, will earn in foreign countries. He will be cruel and mischievous.
            You may travel a lot due to the effects of this Yoga. You may even go on long journeys and might desire a change in your life always. With the presence of Rajju Yoga, you may be very fortunate. But, you may not be comfortable in most of the places. You may feel restless all the time. 
            Rajju Yoga also makes you jealous of others. You may even try to imitate them'''
            
        elif ("Fixed" in planetnatures):
            #this is Musala Yoga (All planets are in Fixed signs)
            Title = "MUSALA"
            Name = "Musala Aashraya Nabhasa"
            common.AshrayaYogas.append("Musala Aashraya Nabhasa Yoga")
            Rule = f'''All 7 planets from Sun to Saturn are in Fixed Signs [Sthira]. Hence Musala Yoga is formed which is one of 3 types of Ashraya yogas in Nabhasa yogas.'''
            Results = f'''According to Parashara, One born in Musala Yog will be endowed with honour, wisdom, wealth etc., be dear to king, famous, will have many sons and be firm in disposition.
            With the presence of Moosal Yoga, you are likely to achieve success at your place of birth. You might have a stable source of income. You may achieve success in your own country if you are born in Moosal Yoga.
            A person born in this Yoga usually has clear and stable thoughts. He may even be stubborn and determined to achieve his goals.'''
            
        else:
            #this is Nala Yoga (All planets are in Dual signs)
            Title = "NALA"
            Name = "Nala Aashraya Nabhasa"
            common.AshrayaYogas.append("Nala Aashraya Nabhasa Yoga")
            Rule = f'''All 7 planets from Sun to Saturn are in Dual Signs [Dwi-Svabhava]. Hence Nala Yoga is formed which is one of 3 types of Ashraya yogas in Nabhasa yogas.'''
            Results = f'''According to Parashara, One born in Nala Yog will have uneven physique, be interested in accumulating money, very skilful, helpful to relatives and charming.
            According to scholars, a child born in this Yoga may be missing a limb. He may also have an extra limb in the body. In the absence of these conditions, the child might have some sort of weakness.
            A child born in this Yoga receives high education in the future since Nal Yoga is related to Mercury and Jupiter. Mercury is the Karak planet for intelligence while Jupiter is the Karak planet for knowledge. He may be very good in his studies and might be interested in going for higher studies.
            You might try to earn your livelihood through the fields related to education, if you are born in Nal Yoga. You may be a good analyst also.
            You may notice some changes in the course of your life due to the presence of dual-natured signs in your Kundali. Some scholars believe that a person born in this Yoga should not be involved in decision-making. He would achieve success if he refrains himself from taking any decisions
            '''
            
        Note = f'''One born with an Asraya will obtain the good effects, viz., happiness, advantages and qualities, provided there is no other kind of (Nabhasa) yoga present in the horoscope. 
        If other (Nabhasa) yoga is present in addition to an Asraya Yoga then the effects ofAsraya yoga do not come to pass, but the other (Nabhasa) yoga prevails.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAshrayaYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = "https://astrobix.com/webcasts/114-effects-and-formation-of-ashray-yoga-and-dal-yoga.html"

    return IsAshrayaYogaPresent

#Dala Yogas -  Depending on if all only benefic planets or only malefic planets are in kendra.
def DalaYoga(charts):
    
    global IsDalaYogaPresent
    IsDalaYogaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = "None"
    Title = ""
    relevant_planets = ["Su", "Ma", "Me", "Ju", "Ve", "Sa"]
    colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
    #Get house numbers of all relevant planets
    #Malefics
    hno_su = charts["D1"]["planets"]["Sun"]["house-num"]
    hno_sa = charts["D1"]["planets"]["Saturn"]["house-num"]
    hno_ma = charts["D1"]["planets"]["Mars"]["house-num"]
    #Benefics
    hno_me = charts["D1"]["planets"]["Mercury"]["house-num"]
    hno_ve = charts["D1"]["planets"]["Venus"]["house-num"]
    hno_ju = charts["D1"]["planets"]["Jupiter"]["house-num"]

    #Check for Mala Dala Yoga
    #All benefics in 3 seperate kendra houses and none of malefics are in kendra
    if((hno_ju in [1,4,7,10]) and       #Ju in kendra
       (hno_ve in [1,4,7,10]) and       #Ve in kendra
       (hno_me in [1,4,7,10]) and       #Me in kendra
       (hno_su not in [1,4,7,10]) and   #Su not in kendra
       (hno_sa not in [1,4,7,10]) and   #Sa not in kendra
       (hno_ma not in [1,4,7,10]) and   #Ma not in kendra
       ((hno_ju != hno_ve) and (hno_ve != hno_me) and (hno_me != hno_ju))):     #All benefics are in different kendra houses
       IsDalaYogaPresent = True
       #Highlight benefic houses
       colorlist[hno_ju-1] = "yellow"
       colorlist[hno_ve-1] = "yellow"
       colorlist[hno_me-1] = "yellow"
       #Update Mala Yoga elements
       Title = "MAALA"
       Name = "Maala Dala Nabhasa"
       common.DalaYogas.append("Maala Dala Nabhasa Yoga")
       Rule = f'''All 3 natural benefics(Jupiter, Venus and Mercury) are placed in 3 Kendra houses and none of the malefics are in Kendra. Hence forming Maala Dala Nabhasa Yoga.'''
       Results = f'''According to Parashara, One born in Maal Yog will be ever happy, endowed with conveyances, robes, food and pleasures, be splendourous and endowed with many females.
       '''

       #Update the yogadosha sections
       common.yogadoshas_dict[Title] = {}
       common.yogadoshas_dict[Title]["name"] = Name
       common.yogadoshas_dict[Title]["type"] = "Yoga"
       common.yogadoshas_dict[Title]["exist"] = IsDalaYogaPresent
       common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
       common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
       common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
       common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
       common.yogadoshas_dict[Title]["Source"] = "https://www.futuresamachar.com/en/nabhasa-yogas-1013"
    #All malefics in 3 seperate kendra houses and none of benefics are in kendra
    elif((hno_ju not in [1,4,7,10]) and       #Ju not in kendra
       (hno_ve not in [1,4,7,10]) and       #Ve not in kendra
       (hno_me not in [1,4,7,10]) and       #Me not in kendra
       (hno_su in [1,4,7,10]) and   #Su in kendra
       (hno_sa in [1,4,7,10]) and   #Sa in kendra
       (hno_ma in [1,4,7,10]) and   #Ma in kendra
       ((hno_su != hno_sa) and (hno_sa != hno_ma) and (hno_ma != hno_su))):     #All malefics are in different kendra houses
       IsDalaYogaPresent = True
       #Highlight Malefic houses
       colorlist[hno_su-1] = "yellow"
       colorlist[hno_sa-1] = "yellow"
       colorlist[hno_ma-1] = "yellow"
       #Update Sarpa Yoga elements
       Title = "SARPA"
       Name = "Sarpa Dala Nabhasa"
       common.DalaYogas.append("Sarpa Dala Nabhasa Yoga")
       Rule = f'''All 3 natural Malefics (Mars, Saturn and Sun) are placed in 3 Kendra houses and none of the Benefics are in Kendra. Hence forming Sarpa Dala Nabhasa Yoga.'''
       Results = f'''According to Parashara, One born in Sarpa Yog will be crooked, cruel, poor, miserable and will depend on others for food and drinks
       '''

       #Update the yogadosha sections
       common.yogadoshas_dict[Title] = {}
       common.yogadoshas_dict[Title]["name"] = Name
       common.yogadoshas_dict[Title]["type"] = "Yoga"
       common.yogadoshas_dict[Title]["exist"] = IsDalaYogaPresent
       common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
       common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
       common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
       common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
       common.yogadoshas_dict[Title]["Source"] = "https://www.futuresamachar.com/en/nabhasa-yogas-1013"
    else:
        IsDalaYogaPresent = False

    return IsDalaYogaPresent
    
#Sankhya Yogas -  Depending on if all planets are in Movable(1,4,7,10), Fixed(2,5,8,11) or Dual(3,6,9,12) signs
def SankhyaYoga(charts):
    
    global IsSankhyaYogaPresent
    IsSankhyaYogaPresent = True
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Title = ""
    relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa"]
    colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        
    planethouses = []
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        planet_house = (charts["D1"]["planets"][planet]["house-num"])
        colorlist[planet_house-1] = "yellow"
        if (planet_house not in planethouses):
            planethouses.append(planet_house)
    
    if (len(planethouses) == 7):
        Title = "VEENA"
        Name = "Veena Sankhya Nabhasa"
        common.SankhyaYogas.append("Veena Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 7 seperate signs. Hence Veena Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Veena Yog will be fond of songs, dance and musical instruments, be skilful, happy, wealthy and be a leader of men.
        '''
    elif (len(planethouses) == 6):
        Title = "DAAMINI"
        Name = "Daamini Sankhya Nabhasa"
        common.SankhyaYogas.append("Daamini Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 6 seperate signs. Hence Daamini Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Daamini Yog will be helpful to others, will have righteously earned wealth, be very affluent, famous, will have many sons and gems, be courageous and red-lettered.
        '''
    elif (len(planethouses) == 5):
        Title = "PAASHA"
        Name = "Paasha Sankhya Nabhasa"
        common.SankhyaYogas.append("Paasha Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 5 seperate signs. Hence Paasha Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Paash Yog will be liable to be imprisoned, be skilful in work, be deceiving in disposition, will talk much, be bereft of good qualities and will have many servants.
        '''
    elif (len(planethouses) == 4):
        Title = "KEDARA"
        Name = "Kedara Sankhya Nabhasa"
        common.SankhyaYogas.append("Kedara Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 4 seperate signs. Hence Kedara Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Kedara Yog will be useful to many, be an agriculturist, be truthful, happy, fickle-minded and wealthy.
        '''
    elif (len(planethouses) == 3):
        Title = "SHOOLA"
        Name = "Shoola Sankhya Nabhasa"
        common.SankhyaYogas.append("Shoola Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 3 seperate signs. Hence Shoola Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Shoola Yog will be sharp, indolent, bereft of wealth, be tortuous, prohibited, valiant and famous through war.
        '''
    elif (len(planethouses) == 2):
        Title = "YUGA"
        Name = "Yuga Sankhya Nabhasa"
        common.SankhyaYogas.append("Yuga Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 2 seperate signs. Hence Yuga Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Yuga Yog will be heretic, be devoid of wealth, be discarded by others and be devoid of sons, mother and virtues.
        '''
    else:
        Title = "GOLA"
        Name = "Gola Sankhya Nabhasa"
        common.SankhyaYogas.append("Gola Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in same sign. Hence Gola Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Gola Yog will be strong, be devoid of wealth, learning and intelligence, be dirty, sorrowful and miserable.
        '''
    
    Note = f'''If other (Nabhasa) yoga is present in addition to an Sankhya Yoga then the effects of Sankhya yoga do not come to pass, but the other (Nabhasa) yoga prevails.
    '''
    if(IsAshrayaYogaPresent == True):
        Note = f'''{Note}In your case Ashraya Nabhasa Yoga is present meaning this sankhya yoga may not give results.'''
    elif(IsDalaYogaPresent == True):
        Note = f'''{Note}In your case Dala Nabhasa Yoga is present meaning this sankhya yoga may not give results.'''
    elif(IsAakritiYogaPresent == True):
        Note = f'''{Note}In your case Aakriti Nabhasa Yoga is present meaning this sankhya yoga may not give results.'''
    else:
        Note = f'''{Note}In your case No other Nabhasa Yoga is present meaning this sankhya yoga will surely give results.'''

    #Update the yogadosha sections
    common.yogadoshas_dict[Title] = {}
    common.yogadoshas_dict[Title]["name"] = Name
    common.yogadoshas_dict[Title]["type"] = "Yoga"
    common.yogadoshas_dict[Title]["exist"] = IsSankhyaYogaPresent
    common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
    common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
    common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
    common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
    common.yogadoshas_dict[Title]["Source"] = ""

    return(IsSankhyaYogaPresent)

#Aakriti Yogas -  Depending on if all only benefic planets or only malefic planets are in kendra.
def AakritiYoga(charts):
    
    global IsAakritiYogaPresent
    IsAakritiYogaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Title = ""
    relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa"]
    benefichouses = []
    malefichouses = []
    planethouses = []
    colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
    #Get house numbers of all relevant planets
    #Malefics
    hno_su = charts["D1"]["planets"]["Sun"]["house-num"]
    hno_sa = charts["D1"]["planets"]["Saturn"]["house-num"]
    hno_ma = charts["D1"]["planets"]["Mars"]["house-num"]
    malefichouses.append(hno_su)
    malefichouses.append(hno_sa)
    malefichouses.append(hno_ma)
    
    #Benefics
    hno_me = charts["D1"]["planets"]["Mercury"]["house-num"]
    hno_ve = charts["D1"]["planets"]["Venus"]["house-num"]
    hno_ju = charts["D1"]["planets"]["Jupiter"]["house-num"]
    hno_mo = charts["D1"]["planets"]["Moon"]["house-num"]
    benefichouses.append(hno_me)
    benefichouses.append(hno_ve)
    benefichouses.append(hno_ju)
    benefichouses.append(hno_mo)

    #All planet houses
    planethouses.append(hno_su)
    planethouses.append(hno_sa)
    planethouses.append(hno_ma)
    planethouses.append(hno_me)
    planethouses.append(hno_ve)
    planethouses.append(hno_ju)
    planethouses.append(hno_mo)

    for h in planethouses:
        colorlist[h-1] = "yellow"

    #check for various Aakriti Yogas
    #Gada Yoga - All planets are in 2 successive kendras
    if( (gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,4]) == True) or      #all planets in 1,4
        (gen.check_ifAllNumInSetA_in_SetB(planethouses, [4,7]) == True) or      #all planets in 4,7
        (gen.check_ifAllNumInSetA_in_SetB(planethouses, [7,10]) == True) or     #all planets in 7,10
        (gen.check_ifAllNumInSetA_in_SetB(planethouses, [10,1]) == True) ):     #all planets in 10,1
        #Gada Yoga formed
        IsAakritiYogaPresent = True
        Title = "GADA"
        Name = "Gada Aakriti Nabhasa"
        common.AakritiYogas.append("Gada Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Successive Kendras. Hence Gada Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Gada Yog will always make efforts to earn wealth, will perform sacrificial rites, be skilful in Shastras and songs and endowed with wealth, gold and precious stones.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    #Sakata Yoga - All planets are in kendra houses 1 and 7
    if( (gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,7]) == True) ):     
        #Sakata Yoga formed
        IsAakritiYogaPresent = True
        Title = "SAKATA"
        Name = "Sakata Aakriti Nabhasa"
        common.AakritiYogas.append("Sakata Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Kendra houses[1 and 7] [Tanu and Dhampathya Bhav]. Hence Sakata Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Sakata Yog will be afflicted by diseases, will have diseased, or ugly nails, be foolish, will live by pulling carts, be poor and devoid of friends and relatives.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Vihag Yoga - All planets are in kendra houses 4 and 10
    if( (gen.check_ifAllNumInSetA_in_SetB(planethouses, [4,10]) == True) ):     
        #Vihag Yoga formed
        IsAakritiYogaPresent = True
        Title = "VIHAG"
        Name = "Vihag Aakriti Nabhasa"
        common.AakritiYogas.append("Vihag Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Kendra houses[4 and 10] [Bhandu and Karma Bhav]. Hence Vihag Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Vihag Yog will be fond of roaming, be a messenger, will live by sexual dealings, be shameless and interested in quarrels.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Shringatak Yoga - All planets are in trikona [Dharma]
    if( (gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,5,9]) == True) ):     
        #Shringatak Yoga formed
        IsAakritiYogaPresent = True
        Title = "SHRINGATAK"
        Name = "Shringatak Aakriti Nabhasa"
        common.AakritiYogas.append("Shringatak Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Dharma Trikona houses[1,5 and 9] [Tanu, Santaan and Bhagya Bhav]. Hence Shringatak Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Shringatak Yog will be fond of quarrels and battles, be happy, dear to king, endowed with an auspicious wife, be rich and will hate women.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Hala Yoga - All planets are in trikona [Artha, Kama or Moksha]
    if( (gen.check_ifAllNumInSetA_in_SetB(planethouses, [2,6,10]) == True) or
        (gen.check_ifAllNumInSetA_in_SetB(planethouses, [3,7,11]) == True) or
        (gen.check_ifAllNumInSetA_in_SetB(planethouses, [4,8,12]) == True)):     
        #Hala Yoga formed
        IsAakritiYogaPresent = True
        Title = "HALA"
        Name = "Hala Aakriti Nabhasa"
        common.AakritiYogas.append("Hala Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Trikona houses[apart from dharma]. Hence Hala Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Hala Yog will eat a lot, will be very poor, will be miserable, gitated, given up by friends and relatives. He will be a servant.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Vajra Yoga 
    if( (gen.check_ifAllNumInSetA_in_SetB(benefichouses, [1,7]) == True)):     
        #Vajra Yoga formed
        IsAakritiYogaPresent = True
        Title = "VAJRA"
        Name = "Vajra Aakriti Nabhasa"
        common.AakritiYogas.append("Vajra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All natural benefic planets in houses 1 and 7. Hence Vajra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Vajra Yog will be happy in the beginning and at the end of life, be valorous, charming, devoid of desires and fortunes and be inimical.
        '''
        relevant_planets2 = ["Ju", "Mo", "Ve", "Me"]
        colorlist2 = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist2[hno_ju - 1] = "yellow"
        colorlist2[hno_mo - 1] = "yellow"
        colorlist2[hno_ve - 1] = "yellow"
        colorlist2[hno_me - 1] = "yellow"

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Vajra Yoga 
    if( (gen.check_ifAllNumInSetA_in_SetB(malefichouses, [4,10]) == True)):     
        #Vajra Yoga formed
        IsAakritiYogaPresent = True
        Title = "VAJRA"
        Name = "Vajra Aakriti Nabhasa"
        common.AakritiYogas.append("Vajra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All natural malefic planets in houses 4 and 10. Hence Vajra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Vajra Yog will be happy in the beginning and at the end of life, be valorous, charming, devoid of desires and fortunes and be inimical.
        '''
        relevant_planets2 = ["Su", "Ma", "Sa"]
        colorlist2 = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist2[hno_su - 1] = "yellow"
        colorlist2[hno_ma - 1] = "yellow"
        colorlist2[hno_sa - 1] = "yellow"

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Yav Yoga 
    if( (gen.check_ifAllNumInSetA_in_SetB(benefichouses, [4,10]) == True)):     
        #Yav Yoga formed
        IsAakritiYogaPresent = True
        Title = "YAV"
        Name = "Yav Aakriti Nabhasa"
        common.AakritiYogas.append("Yav Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All natural benefic planets in houses 4 and 10. Hence Yav Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Yav Yog will observe fasts and other religious rules, will do auspicious acts, will obtain happiness, wealth and sons in his mid-life. He will be charitable and firm.
		'''
        relevant_planets2 = ["Ju", "Mo", "Ve", "Me"]
        colorlist2 = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist2[hno_ju - 1] = "yellow"
        colorlist2[hno_mo - 1] = "yellow"
        colorlist2[hno_ve - 1] = "yellow"
        colorlist2[hno_me - 1] = "yellow"

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Yav Yoga 
    if( (gen.check_ifAllNumInSetA_in_SetB(malefichouses, [1,7]) == True)):     
        #Yav Yoga formed
        IsAakritiYogaPresent = True
        Title = "YAV"
        Name = "Yav Aakriti Nabhasa"
        common.AakritiYogas.append("Yav Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All natural malefic planets in houses 1 and 7. Hence Yav Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Yav Yog will observe fasts and other religious rules, will do auspicious acts, will obtain happiness, wealth and sons in his mid-life. He will be charitable and firm.
		'''
        relevant_planets2 = ["Su", "Ma", "Sa"]
        colorlist2 = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist2[hno_su - 1] = "yellow"
        colorlist2[hno_ma - 1] = "yellow"
        colorlist2[hno_sa - 1] = "yellow"

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Kamala Yoga - All planets are in kendra
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,4,7,10]) == True):     
        #Kamala Yoga formed
        IsAakritiYogaPresent = True
        Title = "KAMALA"
        Name = "Kamala Aakriti Nabhasa"
        common.AakritiYogas.append("Kamala Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in kendra houses[1,4,7,10]. Hence Kamala Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Kamala Yog will be rich and virtuous, be long lived, very famous and pure. He will perform hundreds of auspicious acts and he will be a king.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Vapi Yoga - No planets are in kendra
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [2,3,5,6,8,9,11,12]) == True):     
        #Vapi Yoga formed
        IsAakritiYogaPresent = True
        Title = "VAPI"
        Name = "Vapi Aakriti Nabhasa"
        common.AakritiYogas.append("Vapi Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''None of 7 planets from Sun to Saturn are in kendra houses[1,4,7,10]. Hence Vapi Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Vapi Yog will be capable of accumulating wealth, be endowed with lasting wealth and happiness and sons, be free from eye afflictions and will be a king.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Yupa Yoga - No planets are in kendra
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,2,3,4]) == True):     
        #Yupa Yoga formed
        IsAakritiYogaPresent = True
        Title = "YUPA"
        Name = "Yupa Aakriti Nabhasa"
        common.AakritiYogas.append("Yupa Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[1,2,3,4]. Hence Yupa Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Yupa Yog will have spiritual knowledge and will be interested in sacrificial rites. He will be endowed with a wife, be strong, interested in fasts and other religious observations and be distinguished.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    #Shara Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [4,5,6,7]) == True):     
        #Shara Yoga formed
        IsAakritiYogaPresent = True
        Title = "SHARA"
        Name = "Shara Aakriti Nabhasa"
        common.AakritiYogas.append("Shara Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[4,5,6,7]. Hence Shara Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Shara Yog will make arrows, be head of a prison, will earn through animals, will eat meat, will indulge in torture and mean handiworks.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Shakti Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [7,8,9,10]) == True):     
        #Shakti Yoga formed
        IsAakritiYogaPresent = True
        Title = "SHAKTI"
        Name = "Shakti Aakriti Nabhasa"
        common.AakritiYogas.append("Shakti Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[7,8,9,10]. Hence Shakti Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Shakti Yog will be bereft of wealth, be unsuccessful, miserable, mean, lazy, long lived, interested and skilful in war, firm and auspicious.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    #Danda Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [10,11,12,1]) == True):     
        #Danda Yoga formed
        IsAakritiYogaPresent = True
        Title = "DANDA"
        Name = "Danda Aakriti Nabhasa"
        common.AakritiYogas.append("Danda Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[10,11,12,1]. Hence Danda Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Danda Yog will lose sons and wife, will be indigent, unkind, away from his men and will serve mean people.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    
    #Nauka Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,2,3,4,5,6,7]) == True):     
        #Nauka Yoga formed
        IsAakritiYogaPresent = True
        Title = "NAUKA"
        Name = "Nauka Aakriti Nabhasa"
        common.AakritiYogas.append("Nauka Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[1,2,3,4,5,6,7]. Hence Nauka Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Nauka Yog will derive his livelihood through water, be wealthy, famous, wicked, wretched, dirty and miserly.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    #Koota Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [4,5,6,7,8,9,10]) == True):     
        #Koota Yoga formed
        IsAakritiYogaPresent = True
        Title = "KOOTA"
        Name = "Koota Aakriti Nabhasa"
        common.AakritiYogas.append("Koota Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[4,5,6,7,8,9,10]. Hence Koota Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Koota Yog will be a liar, will head a jail, be poor, crafty, cruel and will live in hills and fortresses.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    #Chatra Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [7,8,9,10,11,12,1]) == True):     
        #Chatra Yoga formed
        IsAakritiYogaPresent = True
        Title = "CHATRA"
        Name = "Chatra Aakriti Nabhasa"
        common.AakritiYogas.append("Chatra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[7,8,9,10,11,12,1]. Hence Chatra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Chatra Yog will help his own men, be kind, dear to many kings, very intelligent, happy at the beginning and end of his life and be long-lived.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    #Dhanushi Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [10,11,12,1,2,3,4]) == True):     
        #Dhanushi Yoga formed
        IsAakritiYogaPresent = True
        Title = "DHANUSHI"
        Name = "Dhanushi Aakriti Nabhasa"
        common.AakritiYogas.append("Dhanushi Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[10,11,12,1,2,3,4]. Hence Dhanushi Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Dhanushi Yog will be liar, will protect secrets, be a thief, be fond of wandering, forests, be devoid of luck and be happy in the middle of the life.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""
    else:
        pass

    #Ardha-Chandra Yoga 
    #print(planethouses)
    planetshousesorted = list(set(planethouses))
    #print(planetshousesorted)
    firsthouse = planetshousesorted[0]
    lasthouse = planetshousesorted[-1] 
    if((len(planetshousesorted) == 7) and (gen.housediff(firsthouse,lasthouse) == 7)):
        #Ardha-Chandra Yoga formed
        IsAakritiYogaPresent = True
        Title = "ARDHA-CHANDRA"
        Name = "Ardha-Chandra Aakriti Nabhasa"
        common.AakritiYogas.append("Ardha-Chandra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in continuous 7 signs forming half moon shape. Hence Ardha-Chandra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Ardha-Chandra Yog will lead an Army, will possess a splendourous body, be dear to king, be strong and endowed with gems, gold and ornaments.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    #Chakra Yoga 
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,3,5,7,9,11]) == True): 
        #Chakra Yoga formed
        IsAakritiYogaPresent = True
        Title = "CHAKRA"
        Name = "Chakra Aakriti Nabhasa"
        common.AakritiYogas.append("Chakra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[1,3,5,7,9,11]. Hence Chakra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Chakra Yog will be an emperor, at whose feet will be the prostrating kings, heads, adoring gem studded diadems.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    #Samudra Yoga 
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [2,4,6,8,10,12]) == True): 
        #Samudra Yoga formed
        IsAakritiYogaPresent = True
        Title = "SAMUDRA"
        Name = "Samudra Aakriti Nabhasa"
        common.AakritiYogas.append("Samudra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[2,4,6,8,10,12]. Hence Samudra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Samudra Yog will have many precious stones and abundant wealth, be endowed with pleasures, dear to people, will have firm wealth and be well disposed.
        '''

        #Update the yogadosha sections
        common.yogadoshas_dict[Title] = {}
        common.yogadoshas_dict[Title]["name"] = Name
        common.yogadoshas_dict[Title]["type"] = "Yoga"
        common.yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        common.yogadoshas_dict[Title]["relevant_planets"] = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]
        common.yogadoshas_dict[Title]["Rule"] = common.iterativeReplace(Rule,"\n ", "\n")
        common.yogadoshas_dict[Title]["Result"] = common.iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        common.yogadoshas_dict[Title]["Note"] = common.iterativeReplace(Note,"\n ", "\n")
        common.yogadoshas_dict[Title]["Source"] = ""

    return IsAakritiYogaPresent

