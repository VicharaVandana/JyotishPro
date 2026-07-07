import support.generic as gen
yogadoshas_dict = {}
#imports



def iterativeReplace(s, old, new):
    while old in s:
        s = s.replace(old, new)
    return s


#Global variables
parivarthanaYogas = []
IsAshrayaYogaPresent = False
AshrayaYogas = []
IsDalaYogaPresent = False
DalaYogas = []
IsAakritiYogaPresent = False
AakritiYogas = []
IsSankhyaYogaPresent = False
SankhyaYogas = []


#Function definitions
#function to check for Sasa Panchamahapurusha yoga - Saturn
def SasaYoga(charts):
    IsSasaYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for Sasa yoga to be present
        #cond1 -> Saturn must be in own rashi (Capricorn or Aquarius) OR Saturn must be exhalted(Libra)
        #cond2 -> Saturn must be in Kendra (either from ascendant or from moon)

    #check for Sasa yoga with lagna D1 chart
    lagnasaturn = charts["D1"]["planets"]["Saturn"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnasaturn["sign"] == "Libra"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Saturn is exhalted [Libra]"
    elif (lagnasaturn["sign"] == "Capricorn"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Saturn is in Own sign [Capricorn]'
    elif (lagnasaturn["sign"] == "Aquarius"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Saturn is in Own sign [Aquarius]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for Sasa yoga kendra condition from ascendant
    kendranum_4mlagna = lagnasaturn["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnasaturn["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for Sasa yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnasaturn["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsSasaYogaPresent = lagna_cond1 and lagna_cond2

    #detection part of yoga is over. Now if present then update the other details
    if(IsSasaYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Sasa Panchamahapurusha yoga is formed.'

        #Update the results
        Results = f'''Sasa Yoga makes the native practical, realistic, responsible and hardworking. They also develop exceptional mass communication skills and bear an air of authority. Embracing the effects of Saturn wholeheartedly is said to be the mark of a successful person. Saturn can bless people under Sasa Yoga with exceptional abilities to produce positive results.
        Persons with Sasa Yoga in their kundali are well placed in society, often in senior bureaucratic positions. They possess superlative intelligence and leadership qualities. The financial benefits are many; they are blessed with every creature comfort known to man. The effects Sasa yoga may become more pronounced as one grows in years when it is time for the hard work to pay off.
        Natives with Sasa Yoga in their horoscope will be elevated to positions of power. They will enjoy success and riches, and their fame will spread far and wide. They are pragmatic by nature. They are hardworking, conscientious and self-made.
        The native is blessed with the good qualities of Saturn. They are devoted to their mothers and often engage in charitable activities.
        Sasa Yoga enables the natives to draw benefits from spiritualism and meditation. Such people have heightened intuition and can become good spiritual healers and yoga teachers.
        '''           
        
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Saturn"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Saturn"]["conjuncts"]
        benefics_aspectingSaturn = list(set(benefics).intersection(aspectedby))
        benefics_conjunctSaturn = list(set(benefics).intersection(conjuncts))
        malefics_aspectingSaturn = list(set(malefics).intersection(aspectedby))
        malefics_conjunctSaturn = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Sa"]
        if (lagna_cond1_exhaltation  == True):
            relevant_planets.append(lagnasaturn["dispositor"][0:2])
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Sasa Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the saturn is in kendra.
        Benefic planets aspecting Saturn: {benefics_aspectingSaturn} and conjunct benefics: {benefics_conjunctSaturn}.
        Malefic planets aspecting Saturn: {malefics_aspectingSaturn} and conjunct malefics: {malefics_conjunctSaturn}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        yogadoshas_dict["SASA"] = {}
        yogadoshas_dict["SASA"]["name"] = "Sasa Panchamahapurusha"
        yogadoshas_dict["SASA"]["type"] = "Yoga"
        yogadoshas_dict["SASA"]["exist"] = IsSasaYogaPresent
        yogadoshas_dict["SASA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["SASA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["SASA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["SASA"]["Source"] = "https://www.astroyogi.com/kundli/yog/sasa/"
        if 'relevant_planets' in locals():
            yogadoshas_dict["SASA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["SASA"]["relevant_planets"] = relevant_planets2
    
    return IsSasaYogaPresent

#function to check for Bhadra Panchamahapurusha yoga - Mercury
def BhadraYoga(charts):
    IsBhadraYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for Bhadra yoga to be present
        #cond1 -> Mercury must be in own rashi (Gemini) OR Mercury must be exhalted(Virgo)
        #cond2 -> Mercury must be in Kendra (either from ascendant or from moon)

    #check for Bhadra yoga with lagna D1 chart
    lagnamercury = charts["D1"]["planets"]["Mercury"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnamercury["sign"] == "Virgo"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Mercury is exhalted [Virgo]"
    elif (lagnamercury["sign"] == "Gemini"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Mercury is in Own sign [Gemini]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for Bhadra yoga kendra condition from ascendant
    kendranum_4mlagna = lagnamercury["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnamercury["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for Bhadra yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnamercury["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsBhadraYogaPresent = lagna_cond1 and lagna_cond2

    #detection part of yoga is over. Now if present then update the other details
    if(IsBhadraYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Bhadra Panchamahapurusha yoga is formed.'

        #Update the results
        Results = f'''Bhadra Yoga makes you stand out from the crowd and helps you advance steadily towards the highest level of success. It is believed that if the planet Mercury holds a favourable position in your birth chart and forms the Bhadra Yoga, it will enhance your intelligence and ensure that you achieve success in all your endeavours.
        The native is blessed with superlative intelligence and wisdom to make the right decisions at the right time. Also, it blesses the native with advanced communication skills which enables them to have a deep and lasting influence on people around them.
        This yoga blesses you with a long and healthy life. With the help of Bhadra Yoga, you will have a great career as a journalist, speaker, political person or reformer.
        Bhadra Yoga will improve your mental faculties and make you intelligent and wise. It also gives you a pleasing personality and a flexible mind. You are approachable and easily become a trusted confidant to many.
        '''           
        
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Mercury"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Mercury"]["conjuncts"]
        benefics_aspectingMercury = list(set(benefics).intersection(aspectedby))
        benefics_conjunctMercury = list(set(benefics).intersection(conjuncts))
        malefics_aspectingMercury = list(set(malefics).intersection(aspectedby))
        malefics_conjunctMercury = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Me"]
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Bhadra Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the mercury is in kendra.
        Benefic planets aspecting Mercury: {benefics_aspectingMercury} and conjunct benefics: {benefics_conjunctMercury}.
        Malefic planets aspecting Mercury: {malefics_aspectingMercury} and conjunct malefics: {malefics_conjunctMercury}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        yogadoshas_dict["BHADRA"] = {}
        yogadoshas_dict["BHADRA"]["name"] = "Bhadra Panchamahapurusha"
        yogadoshas_dict["BHADRA"]["type"] = "Yoga"
        yogadoshas_dict["BHADRA"]["exist"] = IsBhadraYogaPresent
        yogadoshas_dict["BHADRA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["BHADRA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["BHADRA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["BHADRA"]["Source"] = "https://www.astroyogi.com/kundli/yog/bhadra/"
        if 'relevant_planets' in locals():
            yogadoshas_dict["BHADRA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["BHADRA"]["relevant_planets"] = relevant_planets2
    
    return IsBhadraYogaPresent

#function to check for Ruchaka Panchamahapurusha yoga - Mars
def RuchakaYoga(charts):
    IsRuchakaYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for ruchaka yoga to be present
        #cond1 -> Mars must be in own rashi (Aries or Scorpio) OR Mars must be exhalted(Capricorn)
        #cond2 -> Mars must be in Kendra

    #check for ruchaka yoga with lagna D1 chart
    lagnamars = charts["D1"]["planets"]["Mars"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnamars["sign"] == "Capricorn"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Mars is exhalted [Capricorn]"
    elif (lagnamars["dispositor"] == "Mars"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Mars is in Own sign [{lagnamars["sign"]}]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for ruchaka yoga kendra condition from ascendant
    kendranum_4mlagna = lagnamars["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnamars["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for ruchaka yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnamars["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsRuchakaYogaPresent = lagna_cond1 and lagna_cond2


    if(IsRuchakaYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Ruchaka Panchamahapurusha yoga is formed.'

        #Update the results
        if(lagnamoon["house-num"] == 1): #if moon is in lagna thenruchaka is formed with both and same house distance
            #here ruchaka from ascendant is formed and moon also is in lagna so both are covered
            if (kendranum_4mlagna == 1):
                Results = f'''The  native shall become brave and courageous. His personality will be strong, and he would love to say their point straightforwardly. However, sometimes they might speak in a way that their words may hurt people unknowingly.
                Ruchaka yoga would provide immense physical energy. Their physical well-being would be a treat to watch. Therefore, a career in sports shall enhance their personality and make them successful people. Also, joining forces and being in police work would be good domains for them, career-wise.They will be good leaders.
                Ruchaka Yoga in 1st house comes with a con. With Mars in the first house, the native becomes a victim of the Kuja Dosha or Mangal Dosha. It may bring adversities in the person's life. Specifically, he/she may use all its positive points for attaining wrong deeds. Also, it shall lead to problems in the marital life of the person.
                '''
            elif (kendranum_4mlagna == 4):
                Results = f'''This Ruchaka Yoga provides natives with multiple lands and properties. The person might take birth with property in hand. Along with it, he/she shall possess all comforts and luxuries and true and pure love from mother and other family members.
                Natives shall also possess immense opportunities and growth in their professional world. From here, planet Mars forms a direct aspect with the 10th house. It shall help him grow and become successful in the workplace and grab a good job for himself.
                If the native ever faces hard times, he/she may effortlessly earn money and seek the benefit of wealth. Planet Mars acts as a Karak Grah for real estate and lands. Thus, it is a perfect Yoga to attain success in real estate matters.
                Natives would possess qualities like physical appearance, high energy levels, bravery, and courage. There wont be any shortage of support from people.
                On negative side, Mars in the fourth house makes the native Manglik. However, performing remedies for Mangal dosha can wear off the ill impacts of Kuja Dosha in the chart. With the Mangal Dosha, you may get into quarrelsome behavior and possess the same in the house.
                '''
            elif (kendranum_4mlagna == 7):
                Results = f'''This Ruchaka Yoga makes the person a serial entrepreneur. Native shall be fully driven and possess the energy to grow the business.
                The native is utterly competitive and very active in work. They grab jobs and careers that get them success immensely. However, there are chances that these natives wouldnt take criticism positively. It becomes their behavior to defend themselves as much as possible.
                Ruchaka Yoga leads to natives possessing support from external sources. He/she shall get into partnerships and seek a helping hand from his co-workers and employees. Also, during the Mars Mahadasha, his/her career flourishes to heights. Furthermore, it helps the natives in terms of wealth and business.
                Natives energy also uplifts others. The person becomes a great orator and holds the quality to influence the masses with words and speeches.
                On negative side, Mars in 7th house causes Mangal Dosha. The native becomes utterly aggressive, especially towards the spouse. Also, nature turns possessive around the partner. If the spouse is emotional, the native might deem the attitude of the person as angry.
                '''
            elif (kendranum_4mlagna == 10):
                Results = f'''The benefits of Ruchaka Yoga here are maximum. One because, planet Mars does not form a Mangal Dosha here, second because, in the 10th house, it gains the natural strength of the tenth house. Thus, it also forms a Maha Raj Yoga in the Kundli of the native.
                It helps natives enjoy career growth at an active rate. He/she shall be great as a leader and enjoy successful times and steady growth in her professional life. Moreover, Mars positioning here can create high possibilities for government jobs and politics. Natives would enjoy all sorts of comforts and seek many opportunities in the professional sector of life.
                The physical endurance of the native will be noteworthy and stamina unmatched. So, such people wont be afraid of bearing any sort of physical pain and love using their strengths more than anybody. Along with all this, the placement of Mars in the tenth house shall also make the native achieve utter fame and wealth.
                On negative side, Mars here may make the natives lack patience. He/she shall have to put the effort in excess to make things work. And the hasty decision-making skills will highlight with Mars placement in the 10th house. All this might make natives confront problems in the professional environment and lose important and worth taking opportunities too often. 
                However, on the other hand, natives will definitely be intelligent, and wisdom would be something he/she shall use at its best. Along with it, the energy of Mars will be maximum here. Thus, the person would be courageous and daring to do anything in life. Moreover, with their efforts and energy, natives would achieve greatness and success in life, for sure.
                '''
            else:
                Results = "It should not reach here. Something wrong in computation. Dont trust this analysis."
        
        else:
            #Here ruchaka is formed by either ascendant or/and moon position but not common house.
            if (lagna_cond2_4mAsc  == True):
                #Here ruchak is formed from lagna then
                if (kendranum_4mlagna == 1):
                    Results = f'''The  native shall become brave and courageous. His personality will be strong, and he would love to say their point straightforwardly. However, sometimes they might speak in a way that their words may hurt people unknowingly.
                    Ruchaka yoga would provide immense physical energy. Their physical well-being would be a treat to watch. Therefore, a career in sports shall enhance their personality and make them successful people. Also, joining forces and being in police work would be good domains for them, career-wise.They will be good leaders.
                    Ruchaka Yoga in 1st house comes with a con. With Mars in the first house, the native becomes a victim of the Kuja Dosha or Mangal Dosha. It may bring adversities in the person's life. Specifically, he/she may use all its positive points for attaining wrong deeds. Also, it shall lead to problems in the marital life of the person.
                    '''
                elif (kendranum_4mlagna == 4):
                    Results = f'''This Ruchaka Yoga provides natives with multiple lands and properties. The person might take birth with property in hand. Along with it, he/she shall possess all comforts and luxuries and true and pure love from mother and other family members.
                    Natives shall also possess immense opportunities and growth in their professional world. From here, planet Mars forms a direct aspect with the 10th house. It shall help him grow and become successful in the workplace and grab a good job for himself.
                    If the native ever faces hard times, he/she may effortlessly earn money and seek the benefit of wealth. Planet Mars acts as a Karak Grah for real estate and lands. Thus, it is a perfect Yoga to attain success in real estate matters.
                    Natives would possess qualities like physical appearance, high energy levels, bravery, and courage. There wont be any shortage of support from people.
                    On negative side, Mars in the fourth house makes the native Manglik. However, performing remedies for Mangal dosha can wear off the ill impacts of Kuja Dosha in the chart. With the Mangal Dosha, you may get into quarrelsome behavior and possess the same in the house.
                    '''
                elif (kendranum_4mlagna == 7):
                    Results = f'''This Ruchaka Yoga makes the person a serial entrepreneur. Native shall be fully driven and possess the energy to grow the business.
                    The native is utterly competitive and very active in work. They grab jobs and careers that get them success immensely. However, there are chances that these natives wouldnt take criticism positively. It becomes their behavior to defend themselves as much as possible.
                    Ruchaka Yoga leads to natives possessing support from external sources. He/she shall get into partnerships and seek a helping hand from his co-workers and employees. Also, during the Mars Mahadasha, his/her career flourishes to heights. Furthermore, it helps the natives in terms of wealth and business.
                    Natives energy also uplifts others. The person becomes a great orator and holds the quality to influence the masses with words and speeches.
                    On negative side, Mars in 7th house causes Mangal Dosha. The native becomes utterly aggressive, especially towards the spouse. Also, nature turns possessive around the partner. If the spouse is emotional, the native might deem the attitude of the person as angry.
                    '''
                elif (kendranum_4mlagna == 10):
                    Results = f'''The benefits of Ruchaka Yoga here are maximum. One because, planet Mars does not form a Mangal Dosha here, second because, in the 10th house, it gains the natural strength of the tenth house. Thus, it also forms a Maha Raj Yoga in the Kundli of the native.
                    It helps natives enjoy career growth at an active rate. He/she shall be great as a leader and enjoy successful times and steady growth in her professional life. Moreover, Mars positioning here can create high possibilities for government jobs and politics. Natives would enjoy all sorts of comforts and seek many opportunities in the professional sector of life.
                    The physical endurance of the native will be noteworthy and stamina unmatched. So, such people wont be afraid of bearing any sort of physical pain and love using their strengths more than anybody. Along with all this, the placement of Mars in the tenth house shall also make the native achieve utter fame and wealth.
                    On negative side, Mars here may make the natives lack patience. He/she shall have to put the effort in excess to make things work. And the hasty decision-making skills will highlight with Mars placement in the 10th house. All this might make natives confront problems in the professional environment and lose important and worth taking opportunities too often. 
                    However, on the other hand, natives will definitely be intelligent, and wisdom would be something he/she shall use at its best. Along with it, the energy of Mars will be maximum here. Thus, the person would be courageous and daring to do anything in life. Moreover, with their efforts and energy, natives would achieve greatness and success in life, for sure.
                    '''
                else:
                    Results = "It should not reach here. Something wrong in computation. Dont trust this analysis. "
            
            if (lagna_cond2_4mMoon  == True):
                #Here ruchak is formed from Moon then
                if (kendranum_4mmoon == 1):
                    Results = f'''{Results}The  native shall become brave and courageous. His personality will be strong, and he would love to say their point straightforwardly. However, sometimes they might speak in a way that their words may hurt people unknowingly.
                    Ruchaka yoga would provide immense physical energy. Their physical well-being would be a treat to watch. Therefore, a career in sports shall enhance their personality and make them successful people. Also, joining forces and being in police work would be good domains for them, career-wise.They will be good leaders.
                    Ruchaka Yoga in 1st house comes with a con. With Mars in the first house, the native becomes a victim of the Kuja Dosha or Mangal Dosha. It may bring adversities in the person's life. Specifically, he/she may use all its positive points for attaining wrong deeds. Also, it shall lead to problems in the marital life of the person.'''
                elif (kendranum_4mmoon == 4):
                    Results = f'''{Results}This Ruchaka Yoga provides natives with multiple lands and properties. The person might take birth with property in hand. Along with it, he/she shall possess all comforts and luxuries and true and pure love from mother and other family members.
                    Natives shall also possess immense opportunities and growth in their professional world. From here, planet Mars forms a direct aspect with the 10th house. It shall help him grow and become successful in the workplace and grab a good job for himself.
                    If the native ever faces hard times, he/she may effortlessly earn money and seek the benefit of wealth. Planet Mars acts as a Karak Grah for real estate and lands. Thus, it is a perfect Yoga to attain success in real estate matters.
                    Natives would possess qualities like physical appearance, high energy levels, bravery, and courage. There wont be any shortage of support from people.
                    On negative side, Mars in the fourth house makes the native Manglik. However, performing remedies for Mangal dosha can wear off the ill impacts of Kuja Dosha in the chart. With the Mangal Dosha, you may get into quarrelsome behavior and possess the same in the house.'''
                elif (kendranum_4mmoon == 7):
                    Results = f'''{Results}This Ruchaka Yoga makes the person a serial entrepreneur. Native shall be fully driven and possess the energy to grow the business.
                    The native is utterly competitive and very active in work. They grab jobs and careers that get them success immensely. However, there are chances that these natives wouldnt take criticism positively. It becomes their behavior to defend themselves as much as possible.
                    Ruchaka Yoga leads to natives possessing support from external sources. He/she shall get into partnerships and seek a helping hand from his co-workers and employees. Also, during the Mars Mahadasha, his/her career flourishes to heights. Furthermore, it helps the natives in terms of wealth and business.
                    Natives energy also uplifts others. The person becomes a great orator and holds the quality to influence the masses with words and speeches.
                    On negative side, Mars in 7th house causes Mangal Dosha. The native becomes utterly aggressive, especially towards the spouse. Also, nature turns possessive around the partner. If the spouse is emotional, the native might deem the attitude of the person as angry.'''
                elif (kendranum_4mmoon == 10):
                    Results = f'''{Results}The benefits of Ruchaka Yoga here are maximum. One because, planet Mars does not form a Mangal Dosha here, second because, in the 10th house, it gains the natural strength of the tenth house. Thus, it also forms a Maha Raj Yoga in the Kundli of the native.
                    It helps natives enjoy career growth at an active rate. He/she shall be great as a leader and enjoy successful times and steady growth in her professional life. Moreover, Mars positioning here can create high possibilities for government jobs and politics. Natives would enjoy all sorts of comforts and seek many opportunities in the professional sector of life.
                    The physical endurance of the native will be noteworthy and stamina unmatched. So, such people wont be afraid of bearing any sort of physical pain and love using their strengths more than anybody. Along with all this, the placement of Mars in the tenth house shall also make the native achieve utter fame and wealth.
                    On negative side, Mars here may make the natives lack patience. He/she shall have to put the effort in excess to make things work. And the hasty decision-making skills will highlight with Mars placement in the 10th house. All this might make natives confront problems in the professional environment and lose important and worth taking opportunities too often. 
                    However, on the other hand, natives will definitely be intelligent, and wisdom would be something he/she shall use at its best. Along with it, the energy of Mars will be maximum here. Thus, the person would be courageous and daring to do anything in life. Moreover, with their efforts and energy, natives would achieve greatness and success in life, for sure.'''
                else:
                    Results = f"{Results}It should not reach here. Something wrong in computation. Dont trust this analysis."
                     
        
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Mars"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Mars"]["conjuncts"]
        benefics_aspectingMars = list(set(benefics).intersection(aspectedby))
        benefics_conjunctMars = list(set(benefics).intersection(conjuncts))
        malefics_aspectingMars = list(set(malefics).intersection(aspectedby))
        malefics_conjunctMars = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Ma"]
        if (lagna_cond1_exhaltation  == True):
            relevant_planets.append(lagnamars["dispositor"][0:2])
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Ruchaka Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the mars is in kendra.
        Benefic planets aspecting Mars: {benefics_aspectingMars} and conjunct benefics: {benefics_conjunctMars}.
        Malefic planets aspecting Mars: {malefics_aspectingMars} and conjunct malefics: {malefics_conjunctMars}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        yogadoshas_dict["RUCHAKA"] = {}
        yogadoshas_dict["RUCHAKA"]["name"] = "Ruchaka Panchamahapurusha"
        yogadoshas_dict["RUCHAKA"]["type"] = "Yoga"
        yogadoshas_dict["RUCHAKA"]["exist"] = IsRuchakaYogaPresent
        yogadoshas_dict["RUCHAKA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["RUCHAKA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["RUCHAKA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["RUCHAKA"]["Source"] = "https://astrotalk.com/astrology-blog/ruchaka-yoga-in-astrology-impacts-and-benefits-in-different-houses/"
        if 'relevant_planets' in locals():
            yogadoshas_dict["RUCHAKA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["RUCHAKA"]["relevant_planets"] = relevant_planets2
    
    return IsRuchakaYogaPresent

#function to check for Hamsa Panchamahapurusha yoga - Jupiter
def HamsaYoga(charts):
    IsHamsaYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for Hamsa yoga to be present
        #cond1 -> Jupiter must be in own rashi (Saggitarius or Pisces) OR Jupiter must be exhalted(Cancer)
        #cond2 -> Jupiter must be in Kendra (either from ascendant or from moon)

    #check for Hamsa yoga with lagna D1 chart
    lagnajupiter = charts["D1"]["planets"]["Jupiter"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnajupiter["sign"] == "Cancer"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Jupiter is exhalted [Cancer]"
    elif (lagnajupiter["sign"] == "Saggitarius"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Jupiter is in Own sign [Saggitarius]'
    elif (lagnajupiter["sign"] == "Pisces"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Jupiter is in Own sign [Pisces]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for Hamsa yoga kendra condition from ascendant
    kendranum_4mlagna = lagnajupiter["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnajupiter["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for Hamsa yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnajupiter["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsHamsaYogaPresent = lagna_cond1 and lagna_cond2

    #detection part of yoga is over. Now if present then update the other details
    if(IsHamsaYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Hamsa Panchamahapurusha yoga is formed.'

        #Update the results
        Results = f'''Incredible Emotional Intelligence & Knowledge for the Welfare of Masses.
        This yoga in your horoscope blesses you with incredible emotional Intelligence and knowledge that brings about the welfare of the masses and underprivileged, drawing great respect for you in society.
        Hamsa Yoga confers respect in society with great knowledge, high rank in educational institution. This yoga has the power to bless you with an incredible amount of emotional intelligence, which can give you strong social connectivity. 
        Hamsa Yoga will help you get support from Jupiter to acquire a good amount of wisdom and knowledge that can lead you towards growth and success with great achievements. It helps the person write great books, accumulate great amount of knowledge for the welfare of society and the underprivileged.
        It is very difficult to stand against a person with Hamsa Yoga and win. Some famous people with Hamsa Yoga are Jayalalitha, Dr APJ Abdul Kalam, Farooq Abdullah etc.'''           
        
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Jupiter"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Jupiter"]["conjuncts"]
        benefics_aspectingJupiter = list(set(benefics).intersection(aspectedby))
        benefics_conjunctJupiter = list(set(benefics).intersection(conjuncts))
        malefics_aspectingJupiter = list(set(malefics).intersection(aspectedby))
        malefics_conjunctJupiter = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Ju"]
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Hamsa Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the jupiter is in kendra.
        Benefic planets aspecting Jupiter: {benefics_aspectingJupiter} and conjunct benefics: {benefics_conjunctJupiter}.
        Malefic planets aspecting Jupiter: {malefics_aspectingJupiter} and conjunct malefics: {malefics_conjunctJupiter}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        yogadoshas_dict["HAMSA"] = {}
        yogadoshas_dict["HAMSA"]["name"] = "Hamsa Panchamahapurusha"
        yogadoshas_dict["HAMSA"]["type"] = "Yoga"
        yogadoshas_dict["HAMSA"]["exist"] = IsHamsaYogaPresent
        yogadoshas_dict["HAMSA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["HAMSA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["HAMSA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["HAMSA"]["Source"] = "https://www.indastro.com/astrology-reports/hamsa-yoga.php"
        if 'relevant_planets' in locals():
            yogadoshas_dict["HAMSA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["HAMSA"]["relevant_planets"] = relevant_planets2
    
    return IsHamsaYogaPresent

#function to check for Malavya Panchamahapurusha yoga - Venus
def MalavyaYoga(charts):
    IsMalavyaYogaPresent = False   #initially assume the yoga is not present
    Rule = ""
    Results = ""
    Note = ""
    #two conditions for Malavya yoga to be present
        #cond1 -> Venus must be in own rashi (Taurus or Libra) OR Venus must be exhalted(Pisces)
        #cond2 -> Venus must be in Kendra (either from ascendant or from moon)

    #check for Malavya yoga with lagna D1 chart
    lagnavenus = charts["D1"]["planets"]["Venus"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    #For condition 1
    lagna_cond1_exhaltation = False
    lagna_cond1_swarashi = False
    if(lagnavenus["sign"] == "Pisces"):
        lagna_cond1_exhaltation = True
        Rule = Rule + "In Lagna chart, Venus is exhalted [Pisces]"
    elif (lagnavenus["sign"] == "Taurus"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Venus is in Own sign [Taurus]'
    elif (lagnavenus["sign"] == "Libra"):
        lagna_cond1_swarashi = True
        Rule = Rule + f'In Lagna chart, Venus is in Own sign [Libra]'
    else:
        lagna_cond1_exhaltation = False
        lagna_cond1_swarashi = False
    lagna_cond1 = lagna_cond1_exhaltation or lagna_cond1_swarashi

    #For condition 2
    lagna_cond2_4mAsc = False
    lagna_cond2_4mMoon = False
    #check for Malavya yoga kendra condition from ascendant
    kendranum_4mlagna = lagnavenus["house-num"]
    if((kendranum_4mlagna % 3) == 1):
        lagna_cond2_4mAsc = True
        Rule = Rule + f' and in Kendra [house number:{lagnavenus["house-num"]}]'
    else:
        lagna_cond2_4mAsc = False

    #check for Malavya yoga kendra condition from moon
    kendranum_4mmoon = gen.housediff(lagnamoon["house-num"], lagnavenus["house-num"])
    if((kendranum_4mmoon % 3) == 1):
        lagna_cond2_4mMoon = True
        Rule = Rule + f' and in Kendra with respect to Moon [house number:{kendranum_4mmoon} from moon]'
    else:
        lagna_cond2_4mMoon = False

    lagna_cond2 = lagna_cond2_4mAsc or lagna_cond2_4mMoon
    IsMalavyaYogaPresent = lagna_cond1 and lagna_cond2

    #detection part of yoga is over. Now if present then update the other details
    if(IsMalavyaYogaPresent == True):
        #finish the rule. 
        Rule = Rule + f' Hence Malavya Panchamahapurusha yoga is formed.'

        #Update the results
        Results = f'''The natives having Malavya Yoga in a horoscope will possess a charming and magnetic personality that attracts other people very easily and especially the people from the opposite sex.
        The natives will be good looking, artistic, intelligent, famous, a powerful sense of humor, and possess all materialistic pleasures and richness in life. The natives are praiseworthy, open-minded, determined, powerful, and lucky.
        The natives will be renowned, successful, own many vehicles, highly educated, and lives a life full of luxury and happiness. They will enjoy happiness through life-partner and children along with materialistic happiness.
        Malavya yoga blesses the native with a beautiful and loving wife, success in business, a life full of luxuries and comforts, and fame on the national or international level. It also gives a good home, vehicles, luxury and comfort, and beauty.
        The natives having Malavya yoga can become successful in the professional fields like modeling, cinema, movies and other such fields that require beauty and charm in order to be successful. The natives can excel in the fields of acting, dancing, singing, cosmetics, and fashion.
        Your artistic skills are greatly advanced due to the powerful influence of this yoga in your life. It makes you a visionary and enables you to find solutions to situations with a high level of creativity. The aesthetic part of you shows up in everything you do.
        Some famous persons with this yoga are: Jayalalitha, Sania Mirza, Sonia Gandhi, Jawaharlal Nehru, Mahatma Gandhi etc
        '''           
        
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"]["Venus"]["Aspected-by"]
        conjuncts = charts["D1"]["planets"]["Venus"]["conjuncts"]
        benefics_aspectingVenus = list(set(benefics).intersection(aspectedby))
        benefics_conjunctVenus = list(set(benefics).intersection(conjuncts))
        malefics_aspectingVenus = list(set(malefics).intersection(aspectedby))
        malefics_conjunctVenus = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = ["Ve"]
        if (lagna_cond1_exhaltation  == True):
            relevant_planets.append(lagnavenus["dispositor"][0:2])
        if (lagna_cond2_4mMoon  == True):
            relevant_planets.append("Mo")
        if (lagna_cond2_4mAsc  == True):
            relevant_planets.append(charts["D1"]["ascendant"]["lagna-lord"][0:2])
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]


        Note = f'''The Malavya Yoga is strengthened by association with Benefics and weakened by association with malefics. Also the results are subject to strength of ascendant or moon with which the venus is in kendra.
        Benefic planets aspecting Venus: {benefics_aspectingVenus} and conjunct benefics: {benefics_conjunctVenus}.
        Malefic planets aspecting Venus: {malefics_aspectingVenus} and conjunct malefics: {malefics_conjunctVenus}.
        Consider all these points carefully before concluding the results of this panchamahapurusha yoga.'''

        #Update the yogadosha sections
        yogadoshas_dict["MALAVYA"] = {}
        yogadoshas_dict["MALAVYA"]["name"] = "Malavya Panchamahapurusha"
        yogadoshas_dict["MALAVYA"]["type"] = "Yoga"
        yogadoshas_dict["MALAVYA"]["exist"] = IsMalavyaYogaPresent
        yogadoshas_dict["MALAVYA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["MALAVYA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["MALAVYA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["MALAVYA"]["Source"] = "https://www.ganeshaspeaks.com/learn-astrology/yogas/malavya-yoga/"
        if 'relevant_planets' in locals():
            yogadoshas_dict["MALAVYA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["MALAVYA"]["relevant_planets"] = relevant_planets2
    
    return IsMalavyaYogaPresent

#Functions to check for Vipareeta Raja Yogas - Harsha, Sarala , Vimala
#function to check for Harsha Vipareeta Raja Yoga - 6th/8th/12th Lord in 6th house in lagna
def HarshaYoga(charts):
    IsHarshaYogaPresent = False   #initially assume the yoga is not present
    cnt = 0
    Rule = ""
    Results = ""
    Note = "The Harsha Yoga is impacted by association with Benefics and malefics. Also the results are subject to strength of ascendant and combustion with Sun\n"

    #Section for checking if Yoga is formed
    #Condition for formation of Harsha Yoga is When 6th, 8th or 12th house lords occupy 6th house
    #initially assume the Yoga Doesnt exist
    cond_SixthlordInSixth = False
    cond_EighthlordInSixth = False
    cond_TwelfthlordInSixth = False
    colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
    colorlist[6-1] = "yellow"
    #check if 6th lord is in 6th
    lord = gen.get_nthLord(charts["D1"], 6)
    if (gen.get_planetPlacedHousenum(charts["D1"],lord) == 6):
        cond_SixthlordInSixth = True
        colorlist[6-1] = "yellow"
        cnt = cnt + 1
        lordsdetails = charts["D1"]["planets"][lord]
        Rule = f'''{Rule}Lord of sixth house {lord} is placed in sixth house. '''
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
        conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
        benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
        benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
        malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
        malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = [lord[0:2]]
        relevant_planets.append(lordsdetails["dispositor"][0:2])        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        Note = f'''{Note}Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}.
        Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}.
        '''

    #check if 8th lord is in 6th
    lord = gen.get_nthLord(charts["D1"], 8)
    if (gen.get_planetPlacedHousenum(charts["D1"],lord) == 6):
        cond_EighthlordInSixth = True
        colorlist[8-1] = "yellow"
        cnt = cnt + 1
        lordsdetails = charts["D1"]["planets"][lord]
        Rule = f'''{Rule}Lord of eighth house {lord} is placed in sixth house. '''
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
        conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
        benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
        benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
        malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
        malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = [lord[0:2]]
        relevant_planets.append(lordsdetails["dispositor"][0:2])        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        Note = f'''{Note}Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}.
        Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}.
        '''

    #check if 12th lord is in 6th
    lord = gen.get_nthLord(charts["D1"], 12)
    if (gen.get_planetPlacedHousenum(charts["D1"],lord) == 6):
        cond_TwelfthlordInSixth = True
        colorlist[12-1] = "yellow"
        cnt = cnt + 1
        lordsdetails = charts["D1"]["planets"][lord]
        Rule = f'''{Rule}Lord of Twelfth house {lord} is placed in sixth house. '''
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
        conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
        benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
        benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
        malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
        malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = [lord[0:2]]
        relevant_planets.append(lordsdetails["dispositor"][0:2])        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        Note = f'''{Note}Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}.
        Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}.
        '''

    IsHarshaYogaPresent = (cond_SixthlordInSixth or cond_EighthlordInSixth or cond_TwelfthlordInSixth)
    #If yoga is present then update the details and results etc
    if(IsHarshaYogaPresent == True):
        Rule = f'''{Rule}Hence {cnt} count of Harsha yoga is formed in Natives Lagna chart\n'''
        Note = f'''{Note}Consider all these points carefully before concluding the results of this Vipareeta rajayoga.'''


        #Update the Results of Harsha Yoga
        Results = f'''Harsha Yoga is a Vipreeta Raja Yoga. As its name suggests, it is made up of two words - <Vipreeta> which means reverse and <Raja> which means a ruler. This presents a condition in the kundali of a person where the negatives add up to a positive outcome that can be life-altering. Fortunes are reversed wherein you receive benefits after a spate of bad luck.
        Vipreeta Raj Yoga is a contradictory yoga where you get the positive results from the paapi grahas. These grahas are notorious for causing malice and ill-will with their effects. But they face an advantageous position when they are in each other's houses and this results in positive outcomes.
        According to Phaladeepika, Harsha yoga native will be blessed with happiness, good fortune, and have a strong constitution. He will conquer his enemies and will not do sinful deeds. He will become a friend of illustrious, wealthy, splendorous, famous, and will have many friends.
        Harsha Vipreet Raj Yoga blesses the native with health and wealth. He or she is considered a leader who wins over enemies, earning much fame and glory
        '''

        #Update the yogadosha sections
        yogadoshas_dict["HARSHA"] = {}
        yogadoshas_dict["HARSHA"]["name"] = "Harsha Vipareeta Raja"
        yogadoshas_dict["HARSHA"]["type"] = "Yoga"
        yogadoshas_dict["HARSHA"]["exist"] = IsHarshaYogaPresent
        yogadoshas_dict["HARSHA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["HARSHA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["HARSHA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["HARSHA"]["Source"] = "https://www.sanatanveda.com/astrology/vipareeta-raja-yoga-in-vedic-astrology/"
        if 'relevant_planets' in locals():
            yogadoshas_dict["HARSHA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["HARSHA"]["relevant_planets"] = relevant_planets2
    
    return IsHarshaYogaPresent

#function to check for Sarala Vipareeta Raja Yoga - 6th/8th/12th Lord in 8th house in lagna
def SaralaYoga(charts):
    IsSaralaYogaPresent = False   #initially assume the yoga is not present
    cnt = 0
    Rule = ""
    Results = ""
    Note = "The Sarala Yoga is impacted by association with Benefics and malefics. Also the results are subject to strength of ascendant and combustion with Sun\n"

    #Section for checking if Yoga is formed
    #Condition for formation of Sarala Yoga is When 6th, 8th or 12th house lords occupy 8th house
    #initially assume the Yoga Doesnt exist
    cond_SixthlordInEighth = False
    cond_EighthlordInEighth = False
    cond_TwelfthlordInEighth = False
    colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
    colorlist[8-1] = "yellow"
    #check if 6th lord is in 8th
    lord = gen.get_nthLord(charts["D1"], 6)
    if (gen.get_planetPlacedHousenum(charts["D1"],lord) == 8):
        cond_SixthlordInEighth = True
        colorlist[6-1] = "yellow"
        cnt = cnt + 1
        lordsdetails = charts["D1"]["planets"][lord]
        Rule = f'''{Rule}Lord of sixth house {lord} is placed in eighth house. '''
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
        conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
        benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
        benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
        malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
        malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = [lord[0:2]]
        relevant_planets.append(lordsdetails["dispositor"][0:2])        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        Note = f'''{Note}Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}.
        Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}.
        '''

    #check if 8th lord is in 8th
    lord = gen.get_nthLord(charts["D1"], 8)
    if (gen.get_planetPlacedHousenum(charts["D1"],lord) == 8):
        cond_EighthlordInEighth = True
        colorlist[8-1] = "yellow"
        cnt = cnt + 1
        lordsdetails = charts["D1"]["planets"][lord]
        Rule = f'''{Rule}Lord of eighth house {lord} is placed in eighth house. '''
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
        conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
        benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
        benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
        malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
        malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = [lord[0:2]]
        relevant_planets.append(lordsdetails["dispositor"][0:2])        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        Note = f'''{Note}Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}.
        Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}.
        '''

    #check if 12th lord is in 8th
    lord = gen.get_nthLord(charts["D1"], 12)
    if (gen.get_planetPlacedHousenum(charts["D1"],lord) == 8):
        cond_TwelfthlordInEighth = True
        colorlist[12-1] = "yellow"
        cnt = cnt + 1
        lordsdetails = charts["D1"]["planets"][lord]
        Rule = f'''{Rule}Lord of Twelfth house {lord} is placed in eighth house. '''
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
        conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
        benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
        benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
        malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
        malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = [lord[0:2]]
        relevant_planets.append(lordsdetails["dispositor"][0:2])        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        Note = f'''{Note}Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}.
        Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}.
        '''

    IsSaralaYogaPresent = (cond_SixthlordInEighth or cond_EighthlordInEighth or cond_TwelfthlordInEighth)
    #If yoga is present then update the details and results etc
    if(IsSaralaYogaPresent == True):
        Rule = f'''{Rule}Hence {cnt} count of Sarala yoga is formed in Natives Lagna chart\n'''
        Note = f'''{Note}Consider all these points carefully before concluding the results of this Vipareeta rajayoga.'''


        #Update the Results of Sarala Yoga
        Results = f'''Sarala Yoga is a Vipreeta Raja Yoga. As its name suggests, it is made up of two words - <Vipreeta> which means reverse and <Raja> which means a ruler. This presents a condition in the kundali of a person where the negatives add up to a positive outcome that can be life-altering. Fortunes are reversed wherein you receive benefits after a spate of bad luck.
        Vipreeta Raj Yoga is a contradictory yoga where you get the positive results from the paapi grahas. These grahas are notorious for causing malice and ill-will with their effects. But they face an advantageous position when they are in each other's houses and this results in positive outcomes.
        According to Phaladeepika, Sarala yoga enables the natives to be long-lived, resolute, fearless, prosperous, learned, blessed with children, and wealth. The native with this yoga will achieve success in all his ventures, will be victorious over his enemies, and will be a great celebrity.
        Sarala Vipreeta Raja Yoga blesses the person with wisdom and power. It infuses the native with an air of authority and the sagacity to solve problems
        '''

        #Update the yogadosha sections
        yogadoshas_dict["SARALA"] = {}
        yogadoshas_dict["SARALA"]["name"] = "Sarala Vipareeta Raja"
        yogadoshas_dict["SARALA"]["type"] = "Yoga"
        yogadoshas_dict["SARALA"]["exist"] = IsSaralaYogaPresent
        yogadoshas_dict["SARALA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["SARALA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["SARALA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["SARALA"]["Source"] = "https://www.sanatanveda.com/astrology/vipareeta-raja-yoga-in-vedic-astrology/"
        if 'relevant_planets' in locals():
            yogadoshas_dict["SARALA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["SARALA"]["relevant_planets"] = relevant_planets2
    
    return IsSaralaYogaPresent

#function to check for Vimala Vipareeta Raja Yoga - 6th/8th/12th Lord in 12th house in lagna
def VimalaYoga(charts):
    IsVimalaYogaPresent = False   #initially assume the yoga is not present
    cnt = 0
    Rule = ""
    Results = ""
    Note = "The Vimala Yoga is impacted by association with Benefics and malefics. Also the results are subject to strength of ascendant and combustion with Sun\n"

    #Section for checking if Yoga is formed
    #Condition for formation of Vimala Yoga is When 6th, 8th or 12th house lords occupy 12th house
    #initially assume the Yoga Doesnt exist
    cond_SixthlordInTwelfth = False
    cond_EighthlordInTwelfth = False
    cond_TwelfthlordInTwelfth = False
    colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
    colorlist[12-1] = "yellow"
    #check if 6th lord is in 12th
    lord = gen.get_nthLord(charts["D1"], 6)
    if (gen.get_planetPlacedHousenum(charts["D1"],lord) == 12):
        cond_SixthlordInTwelfth = True
        colorlist[6-1] = "yellow"
        cnt = cnt + 1
        lordsdetails = charts["D1"]["planets"][lord]
        Rule = f'''{Rule}Lord of sixth house {lord} is placed in twelfth house. '''
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
        conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
        benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
        benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
        malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
        malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = [lord[0:2]]
        relevant_planets.append(lordsdetails["dispositor"][0:2])        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        Note = f'''{Note}Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}.
        Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}.
        '''

    #check if 8th lord is in 12th
    lord = gen.get_nthLord(charts["D1"], 8)
    if (gen.get_planetPlacedHousenum(charts["D1"],lord) == 12):
        cond_EighthlordInTwelfth = True
        colorlist[8-1] = "yellow"
        cnt = cnt + 1
        lordsdetails = charts["D1"]["planets"][lord]
        Rule = f'''{Rule}Lord of eighth house {lord} is placed in twelfth house. '''
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
        conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
        benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
        benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
        malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
        malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = [lord[0:2]]
        relevant_planets.append(lordsdetails["dispositor"][0:2])        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        Note = f'''{Note}Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}.
        Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}.
        '''

    #check if 12th lord is in 12th
    lord = gen.get_nthLord(charts["D1"], 12)
    if (gen.get_planetPlacedHousenum(charts["D1"],lord) == 12):
        cond_TwelfthlordInTwelfth = True
        colorlist[12-1] = "yellow"
        cnt = cnt + 1
        lordsdetails = charts["D1"]["planets"][lord]
        Rule = f'''{Rule}Lord of Twelfth house {lord} is placed in twelfth house. '''
        #update the notes 
        benefics = charts["D1"]["classifications"]["benefics"]
        malefics = charts["D1"]["classifications"]["malefics"]
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = charts["D1"]["planets"][lord]["Aspected-by"]
        conjuncts = charts["D1"]["planets"][lord]["conjuncts"]
        benefics_aspectinglord = list(set(benefics).intersection(aspectedby))
        benefics_conjunctlord = list(set(benefics).intersection(conjuncts))
        malefics_aspectinglord = list(set(malefics).intersection(aspectedby))
        malefics_conjunctlord = list(set(malefics).intersection(conjuncts))
        #getting full list of relevant planets for this yoga
        relevant_planets = [lord[0:2]]
        relevant_planets.append(lordsdetails["dispositor"][0:2])        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        Note = f'''{Note}Benefic planets aspecting {lord}: {benefics_aspectinglord} and conjunct benefics: {benefics_conjunctlord}.
        Malefic planets aspecting {lord}: {malefics_aspectinglord} and conjunct malefics: {malefics_conjunctlord}.
        '''

    IsVimalaYogaPresent = (cond_SixthlordInTwelfth or cond_EighthlordInTwelfth or cond_TwelfthlordInTwelfth)
    #If yoga is present then update the details and results etc
    if(IsVimalaYogaPresent == True):
        Rule = f'''{Rule}Hence {cnt} count of Vimala yoga is formed in Natives Lagna chart\n'''
        Note = f'''{Note}Consider all these points carefully before concluding the results of this Vipareeta rajayoga.'''


        #Update the Results of Vimala Yoga
        Results = f'''Vimala Yoga is a Vipreeta Raja Yoga. As its name suggests, it is made up of two words - <Vipreeta> which means reverse and <Raja> which means a ruler. This presents a condition in the kundali of a person where the negatives add up to a positive outcome that can be life-altering. Fortunes are reversed wherein you receive benefits after a spate of bad luck.
        Vipreeta Raja Yoga is a contradictory yoga where you get the positive results from the paapi grahas. These grahas are notorious for causing malice and ill-will with their effects. But they face an advantageous position when they are in each other's houses and this results in positive outcomes.
        According to Phaladeepika, The native with Vimala yoga will be clever in saving money, frugal in his expenses, equipped with good behavior towards others, will enjoy happiness, will be independent, will follow a respectable profession or conduct, and will be well known for his good qualities.
        The native with Vimala yoga will be good at accumulating wealth, good in financial management, spend less, enjoy the pleasures, he also charitable in nature, will be famous in the circle. On the other side, he will also spend on hospitalization, hostile to learned people, will get into unnecessary arguments, short-lived. This yoga also blesses the person with a positive attitude, an honourable career and a spiritual approach to life.
        '''

        #Update the yogadosha sections
        yogadoshas_dict["VIMALA"] = {}
        yogadoshas_dict["VIMALA"]["name"] = "Vimala Vipareeta Raja"
        yogadoshas_dict["VIMALA"]["type"] = "Yoga"
        yogadoshas_dict["VIMALA"]["exist"] = IsVimalaYogaPresent
        yogadoshas_dict["VIMALA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["VIMALA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["VIMALA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["VIMALA"]["Source"] = "https://www.sanatanveda.com/astrology/vipareeta-raja-yoga-in-vedic-astrology/"
        if 'relevant_planets' in locals():
            yogadoshas_dict["VIMALA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["VIMALA"]["relevant_planets"] = relevant_planets2
    
    return IsVimalaYogaPresent

#Functions to detect Kaal Sarpa Doshas
#function to identify if kaal sarpa dosha exist or not and if yes then is it ascending or descending
def kaalSarpaDosha(charts):
    #Check if kaal sarpa dosha exists. 
    #return value can be ABSENT, ASCENDPRESENT, DESCENDPRESENT

    #For Kaal sarpa dosha to be present, All 7 planets must be on the same side of Rahu Ketu Axis in D1 chart
    #If planets are present right side of Rahu-Ketu axis then its ascending kaala sarpa dosha else its descending

    IsKaalSarpaDoshaPresent = True  #initially assume the dosha is present. 
    #Check distance between Rahu and Sun
    baseplanet = "Rahu"
    dist = gen.get_distancebetweenplanets(charts["D1"], baseplanet, "Sun")
    if (dist > (180*3600)): #If sun is greater than sun is in the right side of rahu ketu axis. so lets make Ketu as base planet
        baseplanet = "Ketu"
    
    #now lets check if all other 6 planets are also same side of rahu ketu axis as sub. 
    #So now distance between any of 6 remaining planets from baseplanet must not be more than 180 degrees for kaal sarpa dosha to exist
    for planet in ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        dist = gen.get_distancebetweenplanets(charts["D1"], baseplanet, planet)
        if (dist > (180*3600)): #Rahu ketu axis is broken
            IsKaalSarpaDoshaPresent = False
            break   #end for loop once kaal sarpa dosha is broken
    
    if(IsKaalSarpaDoshaPresent == True):
        if (baseplanet == "Rahu"):
            retval = "DESCENDPRESENT"
        else:
            retval = "ASCENDPRESENT"
    else:
         retval = "ABSENT"
    
    return retval

#Ananta Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Tan bhav
def AnantaKaalSarpaDosha(charts):
    IsAnantaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 1):
        IsAnantaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[1-1] = "yellow"
        colorlist[7-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Ananta Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 1st house and Ketu is in 7th house this is Ananta Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Ananta Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Ananta Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 1st house and Ketu is in 7th house this is Ananta Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Ananta Kaala Sarpa Dosha.
            '''
        #Update the Results of Ananta Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The natives with Ananta kaala sarpa dosha will have to struggle for longer to find success. Although you will work very hard in order to succeed, but the results will come to you after a delay. The Anant Kaalsarp dosh will likely test your patience by introducing you to constant obstacles and challenges. Due to this dosha, a person faces problems in all aspects of their lives, but if you don't lose hope, you will find success later. 
        Also, don't indulge in ill deeds such as gambling, lust, etc.
        '''
        #Update the Note
        Note = "The effect of Ananta Kaala Sarpa Dosha will decrease after the age of 27 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically for Ananta Kaal Sarpa dosha can be solved or atleast impact be reduced by Reading Hanuman Chalisa five times a day for 40 days. If you are a student, you should chant the 'Saraswati Mantra' and 'Saraswatye Namah' for 10-15 minutes daily.'''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["ANANTAKAALSARPA"] = {}
        yogadoshas_dict["ANANTAKAALSARPA"]["name"] = Name
        yogadoshas_dict["ANANTAKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["ANANTAKAALSARPA"]["exist"] = IsAnantaKaalSarpaDoshaPresent
        yogadoshas_dict["ANANTAKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["ANANTAKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["ANANTAKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["ANANTAKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["ANANTAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["ANANTAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["ANANTAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsAnantaKaalSarpaDoshaPresent

#Kulika Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Tan bhav
def KulikaKaalSarpaDosha(charts):
    IsKulikaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 2):
        IsKulikaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[2-1] = "yellow"
        colorlist[8-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Kulika Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 2nd house and Ketu is in 8th house this is Kulika Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Kulika Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Kulika Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 2nd house and Ketu is in 8th house this is Kulika Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Kulika Kaala Sarpa Dosha.
            '''
        #Update the Results of Kulika Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Kulika kaala sarpa dosha is believed to bring economic losses, humiliation, debt and various other obstacles in the native's life. Hence astrologers suggest that you don't form bondings with people without careful scrutiny. If you are into business, make sure you do it with 100% honesty, especially during the Kulik dosh period. 
        When it comes to married life, it is to remain normal for the native dealing with Kulika dosh. You however may feel that you are getting old before time, thus you must invest in taking care of your health. Do not use intoxicants such as cigarettes, tobacco, etc
        Defamations, scandals, unstable marital life, problems from inheritance, financial issues, etc. are connected with this Dosha.
        '''
        #Update the Note
        Note = "The effect of Kulika Kaala Sarpa Dosha will decrease after the age of 33 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Kulika Kaal Sarpa dosha can be solved or atleast impact be reduced by lighting a lamp of mustard oil in front of the Hanuman idol on every saturday evening. Hold energised Silver Rahu Yantra on Saturday'''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["KULIKAKAALSARPA"] = {}
        yogadoshas_dict["KULIKAKAALSARPA"]["name"] = Name
        yogadoshas_dict["KULIKAKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["KULIKAKAALSARPA"]["exist"] = IsKulikaKaalSarpaDoshaPresent
        yogadoshas_dict["KULIKAKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["KULIKAKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["KULIKAKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["KULIKAKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["KULIKAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["KULIKAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["KULIKAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsKulikaKaalSarpaDoshaPresent

#Vasuki Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Tan bhav
def VasukiKaalSarpaDosha(charts):
    IsVasukiKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 3):
        IsVasukiKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[3-1] = "yellow"
        colorlist[9-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Vasuki Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 3rd house and Ketu is in 9th house this is Vasuki Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Vasuki Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Vasuki Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 3rd house and Ketu is in 9th house this is Vasuki Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Vasuki Kaala Sarpa Dosha.
            '''
        #Update the Results of Vasuki Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Vasuki kaala sarpa dosha doesn't only hamper the life of the native but also of the ones related to him, such as his siblings, parents, spouse, etc. You have to face the fact that your family members may cheat on you. There will likely be a lack of peace in the family, and the peace will further shatter with inflating economic problems as the Vasuki Kaalsarp dosh continues. 
        However, the good thing is that the person will have economic success as he continues to put in the hard work in making sure things work out for him. 
        The individual would not get the desired results of their hard work and receive their rewards late in life. This Dosha may cause losses in business too.
        '''
        #Update the Note
        Note = "The effect of Vasuki Kaala Sarpa Dosha will decrease after the age of 36 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Vasuki Kaal Sarpa dosha can be solved or atleast impact be reduced by reading Hanuman Chalisa and Bajrang Baan 5 times for 40 days. Hold energised Silver Rahu Yantra on Saturday. 
        Also every Wednesday keep a handful of Urad dal in a black cloth, and chant the Rahu spell mantra and flow the Urad in the water.'''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["VASUKIKAALSARPA"] = {}
        yogadoshas_dict["VASUKIKAALSARPA"]["name"] = Name
        yogadoshas_dict["VASUKIKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["VASUKIKAALSARPA"]["exist"] = IsVasukiKaalSarpaDoshaPresent
        yogadoshas_dict["VASUKIKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["VASUKIKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["VASUKIKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["VASUKIKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["VASUKIKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["VASUKIKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["VASUKIKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsVasukiKaalSarpaDoshaPresent

#Shankhapala Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Tan bhav
def ShankhapalaKaalSarpaDosha(charts):
    IsShankhapalaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 4):
        IsShankhapalaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[4-1] = "yellow"
        colorlist[10-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Shankhapala Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 4th house and Ketu is in 10th house this is Shankhapala Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Shankhapala Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Shankhapala Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 4th house and Ketu is in 10th house this is Shankhapala Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Shankhapala Kaala Sarpa Dosha.
            '''
        #Update the Results of Shankhapala Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Shankhapala kaala sarpa dosha is the signal of incoming financial hardship, disease and disorder in the native's life. Hence, he/she should prepare for it. During this period, the happiness in the native's family will plunge to new lows. This may further hamper elements such as love, child's education, etc. 
        If a youngster, the native will find it tough to make the right choices, due to which he or she may find it difficult to settle early in life. The people of this yoga have to face difficulties related to land and property, thus any such deals must be done after proper scrutiny.
        '''
        #Update the Note
        Note = "The effect of Shankhapala Kaala Sarpa Dosha will decrease after the age of 43 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Shankhapala Kaal Sarpa dosha can be solved or atleast impact be reduced by hanging Hanuman Bahuk in red cloth on any Tuesday on the wall towards the south side of the house. On any Friday, flush the water coconut in water during the day. 
        you can also hang Hanuman Bahuk in red cloth on any Tuesday on the wall towards the south side of the house.'''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["SHANKHAPALAKAALSARPA"] = {}
        yogadoshas_dict["SHANKHAPALAKAALSARPA"]["name"] = Name
        yogadoshas_dict["SHANKHAPALAKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["SHANKHAPALAKAALSARPA"]["exist"] = IsShankhapalaKaalSarpaDoshaPresent
        yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["SHANKHAPALAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["SHANKHAPALAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["SHANKHAPALAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsShankhapalaKaalSarpaDoshaPresent

#Padam Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def PadamKaalSarpaDosha(charts):
    IsPadamKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 5):
        IsPadamKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[5-1] = "yellow"
        colorlist[11-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Padam Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 5th house and Ketu is in 11th house this is Padam Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Padam Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Padam Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 5th house and Ketu is in 11th house this is Padam Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Padam Kaala Sarpa Dosha.
            '''
        #Update the Results of Padam Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Padam kaala sarpa dosha is especially harmful to students as they may lose concentration in studies and indulge in detrimental deeds. Hence, parents must keep an eye on their children during this period. You also need to ensure you help your child make the right choices in education or it will simply cost you and him a loss of money and time. 
        For grown-ups, the dosh may hamper your progress in your career. If you are looking for new opportunities or taking risks, you must do it with a partner. Also, health should be a priority as the Padam Kaalsarp dosh progresses.
        The 5th house indicates Purva Punya so this clearly shows the lack of Purva Punya. There will be hindrances in the field of education and career, but the individual could cross all barriers and succeed eventually. Ill health and secret enemies are the biggest adversaries.
        '''
        #Update the Note
        Note = "The effect of Padam Kaala Sarpa Dosha will decrease after the age of 48 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Padam Kaal Sarpa dosha can be solved or atleast impact be reduced by wering a triangular Coral gemstone of seven and a quarter with copper in the middle finger of the right hand on any Tuesday. Keep a Peacock feather in the books on Saturday.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["PADAMKAALSARPA"] = {}
        yogadoshas_dict["PADAMKAALSARPA"]["name"] = Name
        yogadoshas_dict["PADAMKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["PADAMKAALSARPA"]["exist"] = IsPadamKaalSarpaDoshaPresent
        yogadoshas_dict["PADAMKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["PADAMKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["PADAMKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["PADAMKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["PADAMKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["PADAMKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["PADAMKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsPadamKaalSarpaDoshaPresent

#Mahapadma Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Rog bhav
def MahapadmaKaalSarpaDosha(charts):
    IsMahapadmaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 6):
        IsMahapadmaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[6-1] = "yellow"
        colorlist[12-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Mahapadma Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 6th house and Ketu is in 12th house this is Mahapadma Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Mahapadma Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Mahapadma Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 6th house and Ketu is in 12th house this is Mahapadma Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Mahapadma Kaala Sarpa Dosha.
            '''
        #Update the Results of Mahapadma Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Mahapadma kaala sarpa dosha is special as its more of a partial-yoga than a Dosha. The native finds himself the luck to win over all his enemies with ease. There is an enhancement in wisdom and a thrust of will to do something worthwhile and big in life. 
        However, as the dosh period continues, the native tends to lose peace of mind and may make thoughtless choices. In the dosh period, the person earns profit from business from abroad. 
        '''
        #Update the Note
        Note = "The effect of Mahapadma Kaala Sarpa Dosha will decrease after the age of 54 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Mahapadma Kaal Sarpa dosha can be solved or atleast impact be reduced by visiting the Hanuman idol in the morning on Tuesday. Recite Hanuman Chalisa once in a day for 40 days. 
        Also you can recite Sunderkand of Ramcharitmanas on Tuesday or Saturday 108 times.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["MAHAPADMAKAALSARPA"] = {}
        yogadoshas_dict["MAHAPADMAKAALSARPA"]["name"] = Name
        yogadoshas_dict["MAHAPADMAKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["MAHAPADMAKAALSARPA"]["exist"] = IsMahapadmaKaalSarpaDoshaPresent
        yogadoshas_dict["MAHAPADMAKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["MAHAPADMAKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["MAHAPADMAKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["MAHAPADMAKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["MAHAPADMAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["MAHAPADMAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["MAHAPADMAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsMahapadmaKaalSarpaDoshaPresent

#Takshaka Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def TakshakaKaalSarpaDosha(charts):
    IsTakshakaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 7):
        IsTakshakaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[7-1] = "yellow"
        colorlist[1-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Takshaka Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 7th house and Ketu is in 1st house this is Takshaka Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Takshaka Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Takshaka Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 7th house and Ketu is in 1st house this is Takshaka Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Takshaka Kaala Sarpa Dosha.
            '''
        #Update the Results of Takshaka Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Takshaka kaala sarpa dosha impacts mainly the marriage. he or she may have to face a delay in marriage. The marriage delay may become the reason for tension and stress for your parents too. If married, there may be disturbances due to the nature of the in-laws. There may also arise situations when you might think of divorce. 
        Also, the ones dealing with Kaalsarp dosh must not consider love marriage during the dosh period. Doing so will hamper the love you share after marriage, and you will have to put extra effort to make things work.
        You find romance difficult and also have trouble receiving their share of ancestral property. They may have good achievements but would show the tendency to renounce everything.
        '''
        #Update the Note
        Note = "The effect of Takshaka Kaala Sarpa Dosha will decrease after the age of 60 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Takshaka Kaal Sarpa dosha can be solved or atleast impact be reduced by reciting Sunderkand of Ramcharitmanas on Tuesday or Saturday 108 times. Read Ganapati Atharvashirsha on every full moon.
        Wear an energized Silver Rahu Yantra around your neck.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["TAKSHAKAKAALSARPA"] = {}
        yogadoshas_dict["TAKSHAKAKAALSARPA"]["name"] = Name
        yogadoshas_dict["TAKSHAKAKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["TAKSHAKAKAALSARPA"]["exist"] = IsTakshakaKaalSarpaDoshaPresent
        yogadoshas_dict["TAKSHAKAKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["TAKSHAKAKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["TAKSHAKAKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["TAKSHAKAKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["TAKSHAKAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["TAKSHAKAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["TAKSHAKAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsTakshakaKaalSarpaDoshaPresent

#Karkotak Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def KarkotakKaalSarpaDosha(charts):
    IsKarkotakKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 8):
        IsKarkotakKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[8-1] = "yellow"
        colorlist[2-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Karkotak Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 8th house and Ketu is in 2nd house this is Karkotak Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Karkotak Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Karkotak Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 8th house and Ketu is in 2nd house this is Karkotak Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Karkotak Kaala Sarpa Dosha.
            '''
        #Update the Results of Karkotak Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Karkotak kaala sarpa dosha is responsible for causing hindrance in acquiring a fortune. The dosh may also hamper career progress as you may witness several hindrances in acquiring a job and getting a well-deserved promotion. 
        People dealing with Karkotak Kaalsarp dosha also acquire the habit of speaking the truth. This may seem like a good thing, but this habit may bar the native from acquiring good deals for himself. This doesn't mean that you shouldn't speak the truth, but you must surely think before speaking to anyone.
        This Dosha affects mental wellbeing. An irritable nature and outspoken character work detrimentally for individuals who receive no success despite hard work. They would also face ups and downs in finance, legal issues, etc
        '''
        #Update the Note
        Note = "The effect of Karkotak Kaala Sarpa Dosha will decrease after the age of 33 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Karkotak Kaal Sarpa dosha can be solved or atleast impact be reduced by wearing Shiva Yantra made of silver around the neck. 
        Starting from Saturday, feed Boondi Laddoos to the ants for 27 days. Also wear a triangular Coral gemstone in copper on the middle finger of the right hand.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["KARKOTAKKAALSARPA"] = {}
        yogadoshas_dict["KARKOTAKKAALSARPA"]["name"] = Name
        yogadoshas_dict["KARKOTAKKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["KARKOTAKKAALSARPA"]["exist"] = IsKarkotakKaalSarpaDoshaPresent
        yogadoshas_dict["KARKOTAKKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["KARKOTAKKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["KARKOTAKKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["KARKOTAKKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["KARKOTAKKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["KARKOTAKKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["KARKOTAKKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsKarkotakKaalSarpaDoshaPresent

#Shankhachur Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def ShankhachurKaalSarpaDosha(charts):
    IsShankhachurKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 9):
        IsShankhachurKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[9-1] = "yellow"
        colorlist[3-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Shankhachur Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 9th house and Ketu is in 3rd house this is Shankhachur Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Shankhachur Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Shankhachur Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 9th house and Ketu is in 3rd house this is Shankhachur Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Shankhachur Kaala Sarpa Dosha.
            '''
        #Update the Results of Shankhachur Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Shankhachur kaala sarpa dosha good thing is that the desires of people born in this dosh are usually fulfilled. However, the bad thing is that there may be a delay in fulfilling such desires, which may leave you frustrated. 
        In the family and home of the native dealing with Shankhachur Kaalsarp dosh, there may be a lot of pain and suffering. In this period, it is suggested that you focus on your family and don't indulge in dealings that you will have to regret in the near future.
        The individuals with this Yoga would face troubles in business and sudden downfall from power and position. They may have to fight for their rights. Upon enduring these troubles, these individuals can become increasingly selfish
        '''
        #Update the Note
        Note = "The effect of Shankhachur Kaala Sarpa Dosha will decrease after the age of 36 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Shankhachur Kaal Sarpa dosha can be solved or atleast impact be reduced by reciting Hanuman Chalisa daily
        Regularly recite Mahamrityunjaya Mantra and observe fasting every Monday. Also Wear an energised Silver Rahu Yantra around your neck on Saturday.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["SHANKACHURKAALSARPA"] = {}
        yogadoshas_dict["SHANKACHURKAALSARPA"]["name"] = Name
        yogadoshas_dict["SHANKACHURKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["SHANKACHURKAALSARPA"]["exist"] = IsShankhachurKaalSarpaDoshaPresent
        yogadoshas_dict["SHANKACHURKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["SHANKACHURKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["SHANKACHURKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["SHANKACHURKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["SHANKACHURKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["SHANKACHURKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["SHANKACHURKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsShankhachurKaalSarpaDoshaPresent

#Ghatak Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Santaan bhav
def GhatakKaalSarpaDosha(charts):
    IsGhatakKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 10):
        IsGhatakKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[10-1] = "yellow"
        colorlist[4-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Ghatak Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 10th house and Ketu is in 4th house this is Ghatak Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Ghatak Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Ghatak Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 10th house and Ketu is in 4th house this is Ghatak Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Ghatak Kaala Sarpa Dosha.
            '''
        #Update the Results of Ghatak Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        Since you have Ghatak kaala sarpa dosha, it is highly recommended that you serve your mother, take care of her and never cause her any harm. This will help in bettering your life conditions. However, it has been noticed that in return, you may not get the same kind of affection from your mother. 
        Due to Ghatak Kaalsarp dosha, the person becomes arrogant even if he or she does not have anything to be proud of. Your ego is at the top of your head, which may hamper not only your personal but your professional bondings too.
        Despite the achieved success, the individuals with this Dosha would find it hard to be happy. There would be problems in professional and family lives. Excessive interference from family members may make their life miserable.
        '''
        #Update the Note
        Note = "The effect of Ghatak Kaala Sarpa Dosha will decrease after the age of 42 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Ghatak Kaal Sarpa dosha can be solved or atleast impact be reduced by always reading the Hanuman Chalisa and observe fast each Tuesday.
        Read Ganapati Atharvashirsha on every full moon. Also on Friday, donate coconut, blanket etc. along with epilogue, oil, black cloth, and peel.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["GHATAKKAALSARPA"] = {}
        yogadoshas_dict["GHATAKKAALSARPA"]["name"] = Name
        yogadoshas_dict["GHATAKKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["GHATAKKAALSARPA"]["exist"] = IsGhatakKaalSarpaDoshaPresent
        yogadoshas_dict["GHATAKKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["GHATAKKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["GHATAKKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["GHATAKKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["GHATAKKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["GHATAKKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["GHATAKKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsGhatakKaalSarpaDoshaPresent

#Vishadhara Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Laab bhav
def VishadharaKaalSarpaDosha(charts):
    IsVishadharaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 11):
        IsVishadharaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[11-1] = "yellow"
        colorlist[5-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Vishadhara Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 11th house and Ketu is in 5th house this is Vishadhara Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Vishadhara Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Vishadhara Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 11th house and Ketu is in 5th house this is Vishadhara Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Vishadhara Kaala Sarpa Dosha.
            '''
        #Update the Results of Vishadhara Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Vishadhara kaala sarpa dosha is fatal for the one trying to acquire education, especially higher education. There will be a lot of obstacles for such a person to get higher education. However, despite all odds, their patience and commitment will help them in moving forward. 
        These people do better in their professional life if they pursue their career from abroad than from their own country. Their fortune trends in foreign countries. In the family, the person has to suffer from property loss even after the possibility of benefiting from grandparents.
         The issues corresponding to this Dosha begin with memory loss, poor educational experience, and plenty of domestic issues on property and wealth. The individuals with this Dosha may also suffer on account of their child.
        '''
        #Update the Note
        Note = "The effect of Vishadhara Kaala Sarpa Dosha will decrease after the age of 48 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Vishadhara Kaal Sarpa dosha can be solved or atleast impact be reduced by feeding barley grains to the needy for 27 days on Saturday.
        On Saturday, circumambulate the raw coal anti-clockwise around your head 8 times, then throw the coal in the running water. Also dont forget to recite Hanuman Chalisa daily.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["VISHADHARAKAALSARPA"] = {}
        yogadoshas_dict["VISHADHARAKAALSARPA"]["name"] = Name
        yogadoshas_dict["VISHADHARAKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["VISHADHARAKAALSARPA"]["exist"] = IsVishadharaKaalSarpaDoshaPresent
        yogadoshas_dict["VISHADHARAKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["VISHADHARAKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["VISHADHARAKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["VISHADHARAKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["VISHADHARAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["VISHADHARAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["VISHADHARAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsVishadharaKaalSarpaDoshaPresent

#Sheshanaga Kaal sarpa dosha - Kaalsarpa dosha with Rahu in Karch bhav
def SheshanagaKaalSarpaDosha(charts):
    IsSheshanagaKaalSarpaDoshaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    Remedies = ""

    KaalSarpDoshaSts = kaalSarpaDosha(charts)
    if (KaalSarpDoshaSts != "ABSENT") and (charts["D1"]["planets"]["Rahu"]["house-num"] == 12):
        IsSheshanagaKaalSarpaDoshaPresent = True
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[12-1] = "yellow"
        colorlist[6-1] = "yellow"
        #Update the Name and Rule
        if (KaalSarpDoshaSts == "ASCENDPRESENT"):
            Name = "Ascending Sheshanaga Kaala Sarpa"
            typ = "Ascending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 12th house and Ketu is in 6th house this is Sheshanaga Kaala Sarpa Dosha. All the planets are right side of Rahu-Ketu Axis heading towards Rahu So its Ascending Sheshanaga Kaala Sarpa Dosha.
            '''
        else:
            Name = "Descending Sheshanaga Kaala Sarpa"
            typ = "Descending"
            Rule = f'''All the remaining 7 planets are in the same side of Rahu-Ketu Axis forming Kaala Sarpa Dosha. Since Rahu is in 12th house and Ketu is in 6th house this is Sheshanaga Kaala Sarpa Dosha. All the planets are left side of Rahu-Ketu Axis heading towards Ketu So its Descending Sheshanaga Kaala Sarpa Dosha.
            '''
        #Update the Results of Sheshanaga Kaala Sarpa Dosha
        Results = f'''Kaal Sarp Dosha is a frightful astrological event that affects a person severely with multifaceted catastrophes. It is a result of bad karma done by the native in the previous lives.
        As Kaalsarp dosh veils the planets, the aspects other planets represent may get hampered, which may lead to problems in the life of the native. So the results from aspects of other planets will be blocked by Rahu-Ketu axis and the native will not be ble to get full results of other planets in his kundali.
        The Sheshanaga kaala sarpa dosha always fulfils natives desires, however, with a slight delay. The native under the presence of this dosh may develop a habit of spending more than his income. This is why he may usually find himself indebted. After 42 years of age, there is a time in his life when he may find himself a prestigious place in society. This, however, will require your constant hard work and commitment.
        This dosha has debilitating effects, both physically and mentally. The individuals face a life of defamation and find it hard to get rid of the same. They will have a lot of hidden enemies, and will never feel satisfied with their lives.
        '''
        #Update the Note
        Note = "The effect of Sheshanaga Kaala Sarpa Dosha will decrease after the age of 54 if other strong Yogas are present in Native's Kundali."
        #update Remedies for Dosha
        Remedies = f'''One of the most effective remedies to reduce the effects of the Kala Sarpa Dosha is visiting shrines of higher spiritual beings. The popular places to visit include Srikalahasti temple, Trimbakeshwar temple, Rameswaram, and Thirunageswaram. The Kalasarpa Dosha Nivaran Puja at Sri Kalahasti mandir, Rameswaram, and Thirunageswaram, is considered the best remedy for Kala Sarpa Dosha. This Dosha can also be remedied by Kal Rudra Yagna performed in these temples.
        Rudra Avisek of Shiva, in any Shiva Temple, and chanting of powerful mantras like the Mrityunjay Mantra, Vishnu Panchakshari Mantra, and Sarp Mantra are the other popular remedies for this Dosha.
        Specifically, Sheshanaga Kaal Sarpa dosha can be solved or atleast impact be reduced by hanging Hanuman Bahuk wrapped in red cloth on any Tuesday on the wall towards the south side of the house
        Feed the raw bread of barley flour to the birds for 3 months. Also you can wear an energised Shiva Yantra made of silver around the neck.
        '''
        
        relevant_planets = ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"]



        #Update the yogadosha sections
        yogadoshas_dict["SHESHANAGAKAALSARPA"] = {}
        yogadoshas_dict["SHESHANAGAKAALSARPA"]["name"] = Name
        yogadoshas_dict["SHESHANAGAKAALSARPA"]["type"] = "Dosha"
        yogadoshas_dict["SHESHANAGAKAALSARPA"]["exist"] = IsSheshanagaKaalSarpaDoshaPresent
        yogadoshas_dict["SHESHANAGAKAALSARPA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["SHESHANAGAKAALSARPA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["SHESHANAGAKAALSARPA"]["Remedies"] = iterativeReplace(Remedies,"\n ", "\n").replace("\n","\n        ")
        yogadoshas_dict["SHESHANAGAKAALSARPA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["SHESHANAGAKAALSARPA"]["Source"] = "https://astrotalk.com/kaal-sarp-dosh-12-types"
        if 'relevant_planets' in locals():
            yogadoshas_dict["SHESHANAGAKAALSARPA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["SHESHANAGAKAALSARPA"]["relevant_planets"] = relevant_planets2
    
    return IsSheshanagaKaalSarpaDoshaPresent

#Gajakesari Yoga - Jupiter is in Kendra with respect to Moon in D1 chart
def GajaKesariYoga(charts):
    IsGajaKesariYogaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    cnt = 0
    good_cnt = 0
    relevant_planets = ["Ju", "Mo"]
    #Check for existance of Gajakesari Yoga
    lagnaJupiter = charts["D1"]["planets"]["Jupiter"]
    lagnaMoon = charts["D1"]["planets"]["Moon"]
    #If Jupiter and Moon are in kendra with respect to each other then Gajakesari is formed. Jupiter must not be Retrograde.
    if(gen.housediff(lagnaJupiter["house-num"], lagnaMoon["house-num"]) in [1,4,7,10]) and (lagnaJupiter["retro"] == 0):
        IsGajaKesariYogaPresent = True
        #update the Rule
        Name = "GajaKesari"
        Rule = f'''Jupiter [House number : {lagnaJupiter["house-num"]}] is in kendra from Moon[House number : {lagnaMoon["house-num"]}] in Native's Kundali. And Jupiter is not retrograde.'''

        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = lagnaJupiter["Aspected-by"]
        conjuncts = lagnaJupiter["conjuncts"]
        benefics_aspectingJupiter = list(set(benefics).intersection(aspectedby))
        benefics_conjunctJupiter = list(set(benefics).intersection(conjuncts))
        malefics_aspectingJupiter = list(set(malefics).intersection(aspectedby))
        malefics_conjunctJupiter = list(set(malefics).intersection(conjuncts))

        if (len(benefics_aspectingJupiter)>0) or (len(benefics_conjunctJupiter)>0):
            Rule = f'''{Rule}Jupiter is associated by Benefics by conjunction or aspect.'''
            good_cnt = good_cnt + 1
        
        #If any malefic is aspecting or conjunct with Jupiter then Gajakesari yoga is weakened
        if (len(malefics_aspectingJupiter)>0) or (len(malefics_conjunctJupiter)>0):
            Name = "Weak GajaKesari"
            Rule = f'''{Rule}But Jupiter is afflicted by Malefics.'''
            cnt = cnt + 1
        
        Rule = f'''{Rule}Hence a {Name} Yoga is formed.'''

        #Moon should not be present in the 6th, 8th & 12th houses. it weakens the yoga
        if ((lagnaMoon["house-num"] == 6) or (lagnaMoon["house-num"] == 8) or (lagnaMoon["house-num"] == 12)):
            Note = f'''Moon is present in dushtana House which weakens the yoga. '''
            cnt = cnt + 1

        #The Moon should be at least four houses away from the Sun. Else effects of this yoga weakens
        lagnaSunHouse = charts["D1"]["planets"]["Sun"]["house-num"]
        lagnaMoonHouse = lagnaMoon["house-num"]
        sunToMoon = gen.housediff(lagnaSunHouse, lagnaMoonHouse)
        if (sunToMoon < 4) or (sunToMoon > 9):
            Note = f'''{Note}Moon is present within 4 houses with respect to the Sun which weakens the yoga. '''
            cnt = cnt + 1
            relevant_planets.append("Su")

        #Moon should not be debilitated (Scorpio)
        if(lagnaMoon["sign"] == "Scorpio"):
            Note = f'''{Note}Moon is debilitated, which weakens this yoga. '''
            cnt = cnt + 1

        #Gaja Kesari Yoga should not be formed in Makara as Jupiter acts debilitated in Makara Rashi.
        if(lagnaJupiter["sign"] == "Capricorn"):
            Note = f'''{Note}Jupiter is debilitated, which weakens this yoga. '''
            cnt = cnt + 1
        
        #If Jupiter or Moon is in Pushkar Navamsa or Bhag, the good results of Gajakesari will increase significantly.
        #Check Pushkara navamsha for Jupiter
        if(True == gen.isPushkaraNavamsha(lagnaJupiter["nakshatra"], lagnaJupiter["pada"])):
            Note = f'''{Note}Jupiter is in Pushkara Navamsa, which strengthens this yoga. '''
            good_cnt = good_cnt + 1
        #Check Pushkara navamsha for Moon
        if(True == gen.isPushkaraNavamsha(lagnaMoon["nakshatra"], lagnaMoon["pada"])):
            Note = f'''{Note}Moon is in Pushkara Navamsa, which strengthens this yoga. '''
            good_cnt = good_cnt + 1
        #Check Pushkara Bhag for Jupiter
        if(True == gen.isPushkaraBhaga(lagnaJupiter["sign-tatva"], lagnaJupiter["pos"]["deg"])):
            Note = f'''{Note}Jupiter is in Pushkara Bhaga, which strengthens this yoga. '''
            good_cnt = good_cnt + 1
        #Check Pushkara Bhag for Moon
        if(True == gen.isPushkaraBhaga(lagnaMoon["sign-tatva"], lagnaMoon["pos"]["deg"])):
            Note = f'''{Note}Moon is in Pushkara Bhaga, which strengthens this yoga. '''
            good_cnt = good_cnt + 1

        if(lagnaMoon["sign"] == "Taurus"):
            Note = f'''{Note}Moon is exhalted, which strengthens this yoga. '''
            good_cnt = good_cnt + 1

        if(lagnaJupiter["sign"] == "Cancer"):
            Note = f'''{Note}Jupiter is exhalted, which strengthens this yoga. '''
            good_cnt = good_cnt + 1

        Note = f'''{Note}Benefic planets aspecting Jupiter: {benefics_aspectingJupiter} and conjunct benefics: {benefics_conjunctJupiter}. Malefic planets aspecting Jupiter: {malefics_aspectingJupiter} and conjunct malefics: {malefics_conjunctJupiter}.
        Consider all these points [{good_cnt} positive and {cnt} negative] carefully before concluding the results of this Gajakesari yoga.'''

        #getting full list of relevant planets for this yoga        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[lagnaJupiter["house-num"]-1] = "yellow"
        colorlist[lagnaMoon["house-num"]-1] = "yellow"


        #Update the results of Gajakesari Yoga
        Results = f'''The word Gajakesari means Gaja for Elephant, and Kesari means Lion. Both Elephant and Lion are powerful and represent authority and intelligence. 
        People with Gaja Kesari Yoga seek good wealth, courage, respect from others and are generally good speakers.
        You will never have to worry about money if you have a strong Gajakesari Yoga in your horoscope chart. Even when there are anxious moments and finances are unstable, you will receive last-minute monetary help, putting an end to your anxiety.
        The effects of Gajakesari Yoga are not just limited to monetary gains. ith this yoga, you will be a courageous and happy person who is full of life and vigour. This yoga will make you a leader who can motivate people and change their lives through your inspirational speeches.'''

        #Update the yogadosha sections
        yogadoshas_dict["GAJAKESARI"] = {}
        yogadoshas_dict["GAJAKESARI"]["name"] = Name
        yogadoshas_dict["GAJAKESARI"]["type"] = "Yoga"
        yogadoshas_dict["GAJAKESARI"]["exist"] = IsGajaKesariYogaPresent
        yogadoshas_dict["GAJAKESARI"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["GAJAKESARI"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["GAJAKESARI"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["GAJAKESARI"]["Source"] = "https://astrotalk.com/astrology-blog/know-who-can-seek-benefits-of-gajakesari-yoga-as-per-astrology/"   
        if 'relevant_planets' in locals():
            yogadoshas_dict["GAJAKESARI"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["GAJAKESARI"]["relevant_planets"] = relevant_planets2
    
    return IsGajaKesariYogaPresent


#ChandraMangala Yoga - Mars and  Moon conjunct in D1 chart
def ChandraMangalaYoga(charts):
    IsChandraMangalaYogaPresent = False
    Name = ""
    Rule = ""
    Results = ""
    Note = ""
    bad_cnt = 0
    good_cnt = 0
    relevant_planets = ["Ma", "Mo"]

    #Check for existance of this yoga
    lagnamars = charts["D1"]["planets"]["Mars"]
    lagnamoon = charts["D1"]["planets"]["Moon"]

    if(lagnamars["sign"] == lagnamoon["sign"]):
        IsChandraMangalaYogaPresent = True
        Name = "Chandra Mangala"
        Rule = "In native's chart Moon is conjunct with Mars. So Chandra Mangala Yoga is formed."

        #if Moon is debilitated then Effects reduce
        if(lagnamoon["sign"] == "Scorpio"):
            Note = f'''{Note}Moon is debilitated, which weakens this yoga. '''
            bad_cnt = bad_cnt + 1

        if(lagnamoon["sign"] == "Taurus"):
            Note = f'''{Note}Moon is exhalted, which strengthens this yoga. '''
            good_cnt = good_cnt + 1

        #If Mars is debilitates. then Effects reduce
        if(lagnamars["sign"] == "Cancer"):
            Note = f'''{Note}Mars is debilitated, which weakens this yoga. '''
            bad_cnt = bad_cnt + 1

        if(lagnamars["sign"] == "Capricorn"):
            Note = f'''{Note}Mars is exhalted, which strengthens this yoga. '''
            good_cnt = good_cnt + 1

        benefics = charts["D1"]["classifications"]["benefics"].copy()
        malefics = charts["D1"]["classifications"]["malefics"].copy()
        malefics.append("Rahu")
        malefics.append("Ketu")
        aspectedby = lagnamars["Aspected-by"]
        conjuncts = lagnamars["conjuncts"]
        benefics_aspectingMars = list(set(benefics).intersection(aspectedby))
        benefics_conjunctMars = list(set(benefics).intersection(conjuncts))
        malefics_aspectingMars = list(set(malefics).intersection(aspectedby))
        malefics_conjunctMars = list(set(malefics).intersection(conjuncts))

        if (len(benefics_aspectingMars)>0) or (len(benefics_conjunctMars)>0):
            Note = f'''{Note}Moon and Mars are associated by Benefics by conjunction or aspect.'''
            good_cnt = good_cnt + 1
        
        #If any malefic is aspecting or conjunct with Mars
        if (len(malefics_aspectingMars)>0) or (len(malefics_conjunctMars)>0):
            Note = f'''{Note}Moon and Mars is afflicted by Malefics.'''
            bad_cnt = bad_cnt + 1

        #if mars or moon is a malefic in this chart then this yoga weakens and if benefics then it strengthens
        if("Mars" in benefics):
            Note = f'''{Note}In this chart Mars is a benefic planet and '''
            good_cnt = good_cnt + 1
        elif("Mars" in malefics):
            Note = f'''{Note}In this chart Mars is a malefic planet and '''
            bad_cnt = bad_cnt + 1
        else:
            Note = f'''{Note}In this chart Mars is a neutral planet and '''
        
        if("Moon" in benefics):
            Note = f'''{Note}Moon is a benefic planet. '''
            good_cnt = good_cnt + 1
        elif("Moon" in malefics):
            Note = f'''{Note}Moon is a malefic planet. '''
            bad_cnt = bad_cnt + 1
        else:
            Note = f'''{Note}Moon is a neutral planet. '''

        Note = f'''{Note}Benefic planets aspecting Moon and Mars: {benefics_aspectingMars} and conjunct benefics: {benefics_conjunctMars}. Malefic planets aspecting Moon and Mars: {malefics_aspectingMars} and conjunct malefics: {malefics_conjunctMars}.
        Consider all these points [{good_cnt} positive and {bad_cnt} negative] carefully before concluding the results of this Chandra Mangala yoga.'''

        #getting full list of relevant planets for this yoga        
        for planet in aspectedby:
            relevant_planets.append(planet[0:2])
        for planet in conjuncts:
            relevant_planets.append(planet[0:2])
        colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]
        colorlist[lagnamars["house-num"]-1] = "yellow"

        
        #Update the results of Gajakesari Yoga
        Results = f'''Chandra Mangal Yoga is significant in many ways. Apart from financial gains, the native gains a great deal of respect and fame in society. The Moon is associated with riches, happiness and mental strength, whereas Mars is associated with the ability to work hard and achieve all of your life's objectives.
        This Yoga gives birth to a person who is immensely wealthy, clever, and powerful. He has a high level of self-assurance, which allows him to operate effectively in even the most difficult conditions. Because this is a wealth-related Yoga, a person born under this sign is capable of making money on his own. The native is also likely to feel irritable as a result of this Yoga. The native may become obstinate due to the relationship between Mars and the Moon. The native will be brave and capable of solving issues more effectively. Others will not be able to assist the native. The native will make his or her own way in life. This Yoga has a bad impact on the local mother.
        '''

        if(lagnamars["house-num"] == 1):
            Results = f'''{Results}The Chandra Mangal Yoga in the first house will bring the best results in terms of name, popularity, stature, and success in public life and politics. At a higher level, natives may be involved in administrative or defence services.
            '''
        elif(lagnamars["house-num"] == 2):
            Results = f'''{Results}The Moon-Mars conjunction in the second house has the potential to make the native a millionaire and provide them with a life of luxury and riches.
            '''
        elif(lagnamars["house-num"] == 3):
            Results = f'''{Results}Chandra-Mangal yoga in the third house bestows the highest levels of valour, vigour and courage on the inhabitants, enabling them to attain any life goals or ambitions.
            '''
        elif(lagnamars["house-num"] == 4):
            Results = f'''{Results}This Yoga combination in the fourth house brings amenities such as automobiles, property, and more than one house, as well as a large number of agricultural products.
            '''
        elif(lagnamars["house-num"] == 5):
            Results = f'''{Results}The Moon-Mars conjunction in the 5th house bestows pleasure and success in creative endeavours, artistic careers, and love affairs.
            '''
        elif(lagnamars["house-num"] == 6):
            Results = f'''{Results}Moon-Mars in the 6th house brings enmity, lawsuits, legal issues, divorces and other problems. It can, however, help you win competitions in sports, academics or examinations.
            '''
        elif(lagnamars["house-num"] == 7):
            Results = f'''{Results}The Chandra-Mangal yoga in the 7th house is likely to provide positive outcomes and benefits from marriage, but there will be some health issues for the husband, as well as a lack of mutual trust and understanding.
            '''
        elif(lagnamars["house-num"] == 8):
            Results = f'''{Results}This conjunction in the 8th house indicates gains from in-laws, as well as riches and property received through inheritance or as a gift from the government.
            '''
        elif(lagnamars["house-num"] == 9):
            Results = f'''{Results}They will strive to make money in a noble and honest manner. They will pose a serious challenge to their rivals.
            This conjunction in the 9th house brings Raj Yog to dignitaries with a rich culture and class, making natives renowned and occasionally famous in their line of work.
            '''
        elif(lagnamars["house-num"] == 10):
            Results = f'''{Results}They will strive to make money in a noble and honest manner. They will pose a serious challenge to their rivals.
            In the 10th house, the Moon-Mars conjunction is favourable for becoming a doctor or surgeon. It provides a significant boost to native's careers, particularly in public or mass transactions.
            '''
        elif(lagnamars["house-num"] == 11):
            Results = f'''{Results}They will strive to make money in a noble and honest manner. They will pose a serious challenge to their rivals.
            If the Moon-Mars conjunction happens in the 11th house, you can become exceedingly wealthy from a young age after the age of 28. With a lot of wealth and power in life, you'll have a lot of money every day.
            '''
        elif(lagnamars["house-num"] == 12):
            Results = f'''{Results}Chandra Mangal Yoga in the 12th house leads to religious enlightenment and salvation in old age, but it also provides earnings from foreign resources or foreign places in the early and intermediate stages of life, particularly in the import-export business.
            '''
        else:
            Results = f'''{Results}It should not come here. The results are not valid. 
            '''


        #Update the yogadosha sections
        yogadoshas_dict["CHANDRAMANGALA"] = {}
        yogadoshas_dict["CHANDRAMANGALA"]["name"] = Name
        yogadoshas_dict["CHANDRAMANGALA"]["type"] = "Yoga"
        yogadoshas_dict["CHANDRAMANGALA"]["exist"] = IsChandraMangalaYogaPresent
        yogadoshas_dict["CHANDRAMANGALA"]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict["CHANDRAMANGALA"]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict["CHANDRAMANGALA"]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict["CHANDRAMANGALA"]["Source"] = "https://www.mypandit.com/kundli/yoga/chandra-mangal/"  
        if 'relevant_planets' in locals():
            yogadoshas_dict["CHANDRAMANGALA"]["relevant_planets"] = relevant_planets
        elif 'relevant_planets2' in locals():
            yogadoshas_dict["CHANDRAMANGALA"]["relevant_planets"] = relevant_planets2
    
    return IsChandraMangalaYogaPresent

def ParivarthanaYoga(charts):
    global IsParivarthanaYogaPresent
    IsParivarthanaYogaPresent = False
    global parivarthanaYogas
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
                yogadoshas_dict[Title] = {}
                yogadoshas_dict[Title]["name"] = Name
                yogadoshas_dict[Title]["type"] = "Yoga"
                yogadoshas_dict[Title]["exist"] = IsParivarthanaYogaPresent
                yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
                yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
                yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
                yogadoshas_dict[Title]["Source"] = ""

                parivarthanaYogas.append(Name)

    return IsParivarthanaYogaPresent

#Nabhasa Yogas - All planetary positions
#Aashraya Yogas -  Depending on if all planets are in Movable(1,4,7,10), Fixed(2,5,8,11) or Dual(3,6,9,12) signs
def AashrayaYoga(charts):
    global AshrayaYogas
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
            AshrayaYogas.append("Rajju Aashraya Nabhasa Yoga")
            Rule = f'''All 7 planets from Sun to Saturn are in Movable Signs [Chara]. Hence Rajju Yoga is formed which is one of 3 types of Ashraya yogas in Nabhasa yogas.'''
            Results = f'''According to Parashara, One born in Rajju Yog will be fond of wandering, be charming, will earn in foreign countries. He will be cruel and mischievous.
            You may travel a lot due to the effects of this Yoga. You may even go on long journeys and might desire a change in your life always. With the presence of Rajju Yoga, you may be very fortunate. But, you may not be comfortable in most of the places. You may feel restless all the time. 
            Rajju Yoga also makes you jealous of others. You may even try to imitate them'''
            
        elif ("Fixed" in planetnatures):
            #this is Musala Yoga (All planets are in Fixed signs)
            Title = "MUSALA"
            Name = "Musala Aashraya Nabhasa"
            AshrayaYogas.append("Musala Aashraya Nabhasa Yoga")
            Rule = f'''All 7 planets from Sun to Saturn are in Fixed Signs [Sthira]. Hence Musala Yoga is formed which is one of 3 types of Ashraya yogas in Nabhasa yogas.'''
            Results = f'''According to Parashara, One born in Musala Yog will be endowed with honour, wisdom, wealth etc., be dear to king, famous, will have many sons and be firm in disposition.
            With the presence of Moosal Yoga, you are likely to achieve success at your place of birth. You might have a stable source of income. You may achieve success in your own country if you are born in Moosal Yoga.
            A person born in this Yoga usually has clear and stable thoughts. He may even be stubborn and determined to achieve his goals.'''
            
        else:
            #this is Nala Yoga (All planets are in Dual signs)
            Title = "NALA"
            Name = "Nala Aashraya Nabhasa"
            AshrayaYogas.append("Nala Aashraya Nabhasa Yoga")
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
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAshrayaYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = "https://astrobix.com/webcasts/114-effects-and-formation-of-ashray-yoga-and-dal-yoga.html"

    return IsAshrayaYogaPresent

#Dala Yogas -  Depending on if all only benefic planets or only malefic planets are in kendra.
def DalaYoga(charts):
    global DalaYogas
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
       DalaYogas.append("Maala Dala Nabhasa Yoga")
       Rule = f'''All 3 natural benefics(Jupiter, Venus and Mercury) are placed in 3 Kendra houses and none of the malefics are in Kendra. Hence forming Maala Dala Nabhasa Yoga.'''
       Results = f'''According to Parashara, One born in Maal Yog will be ever happy, endowed with conveyances, robes, food and pleasures, be splendourous and endowed with many females.
       '''

       #Update the yogadosha sections
       yogadoshas_dict[Title] = {}
       yogadoshas_dict[Title]["name"] = Name
       yogadoshas_dict[Title]["type"] = "Yoga"
       yogadoshas_dict[Title]["exist"] = IsDalaYogaPresent
       yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
       yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
       yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
       yogadoshas_dict[Title]["Source"] = "https://www.futuresamachar.com/en/nabhasa-yogas-1013"
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
       DalaYogas.append("Sarpa Dala Nabhasa Yoga")
       Rule = f'''All 3 natural Malefics (Mars, Saturn and Sun) are placed in 3 Kendra houses and none of the Benefics are in Kendra. Hence forming Sarpa Dala Nabhasa Yoga.'''
       Results = f'''According to Parashara, One born in Sarpa Yog will be crooked, cruel, poor, miserable and will depend on others for food and drinks
       '''

       #Update the yogadosha sections
       yogadoshas_dict[Title] = {}
       yogadoshas_dict[Title]["name"] = Name
       yogadoshas_dict[Title]["type"] = "Yoga"
       yogadoshas_dict[Title]["exist"] = IsDalaYogaPresent
       yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
       yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
       yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
       yogadoshas_dict[Title]["Source"] = "https://www.futuresamachar.com/en/nabhasa-yogas-1013"
    else:
        IsDalaYogaPresent = False

    return IsDalaYogaPresent
    
#Sankhya Yogas -  Depending on if all planets are in Movable(1,4,7,10), Fixed(2,5,8,11) or Dual(3,6,9,12) signs
def SankhyaYoga(charts):
    global SankhyaYogas
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
        SankhyaYogas.append("Veena Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 7 seperate signs. Hence Veena Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Veena Yog will be fond of songs, dance and musical instruments, be skilful, happy, wealthy and be a leader of men.
        '''
    elif (len(planethouses) == 6):
        Title = "DAAMINI"
        Name = "Daamini Sankhya Nabhasa"
        SankhyaYogas.append("Daamini Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 6 seperate signs. Hence Daamini Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Daamini Yog will be helpful to others, will have righteously earned wealth, be very affluent, famous, will have many sons and gems, be courageous and red-lettered.
        '''
    elif (len(planethouses) == 5):
        Title = "PAASHA"
        Name = "Paasha Sankhya Nabhasa"
        SankhyaYogas.append("Paasha Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 5 seperate signs. Hence Paasha Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Paash Yog will be liable to be imprisoned, be skilful in work, be deceiving in disposition, will talk much, be bereft of good qualities and will have many servants.
        '''
    elif (len(planethouses) == 4):
        Title = "KEDARA"
        Name = "Kedara Sankhya Nabhasa"
        SankhyaYogas.append("Kedara Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 4 seperate signs. Hence Kedara Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Kedara Yog will be useful to many, be an agriculturist, be truthful, happy, fickle-minded and wealthy.
        '''
    elif (len(planethouses) == 3):
        Title = "SHOOLA"
        Name = "Shoola Sankhya Nabhasa"
        SankhyaYogas.append("Shoola Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 3 seperate signs. Hence Shoola Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Shoola Yog will be sharp, indolent, bereft of wealth, be tortuous, prohibited, valiant and famous through war.
        '''
    elif (len(planethouses) == 2):
        Title = "YUGA"
        Name = "Yuga Sankhya Nabhasa"
        SankhyaYogas.append("Yuga Sankhya Nabhasa Yoga")
        Rule = f'''All 7 planets from Sun to Saturn are in 2 seperate signs. Hence Yuga Yoga which is a part of Sankhya yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Yuga Yog will be heretic, be devoid of wealth, be discarded by others and be devoid of sons, mother and virtues.
        '''
    else:
        Title = "GOLA"
        Name = "Gola Sankhya Nabhasa"
        SankhyaYogas.append("Gola Sankhya Nabhasa Yoga")
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
    yogadoshas_dict[Title] = {}
    yogadoshas_dict[Title]["name"] = Name
    yogadoshas_dict[Title]["type"] = "Yoga"
    yogadoshas_dict[Title]["exist"] = IsSankhyaYogaPresent
    yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
    yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
    yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
    yogadoshas_dict[Title]["Source"] = ""

    return(IsSankhyaYogaPresent)

#Aakriti Yogas -  Depending on if all only benefic planets or only malefic planets are in kendra.
def AakritiYoga(charts):
    global AakritiYogas
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
        AakritiYogas.append("Gada Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Successive Kendras. Hence Gada Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Gada Yog will always make efforts to earn wealth, will perform sacrificial rites, be skilful in Shastras and songs and endowed with wealth, gold and precious stones.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    #Sakata Yoga - All planets are in kendra houses 1 and 7
    if( (gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,7]) == True) ):     
        #Sakata Yoga formed
        IsAakritiYogaPresent = True
        Title = "SAKATA"
        Name = "Sakata Aakriti Nabhasa"
        AakritiYogas.append("Sakata Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Kendra houses[1 and 7] [Tanu and Dhampathya Bhav]. Hence Sakata Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Sakata Yog will be afflicted by diseases, will have diseased, or ugly nails, be foolish, will live by pulling carts, be poor and devoid of friends and relatives.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Vihag Yoga - All planets are in kendra houses 4 and 10
    if( (gen.check_ifAllNumInSetA_in_SetB(planethouses, [4,10]) == True) ):     
        #Vihag Yoga formed
        IsAakritiYogaPresent = True
        Title = "VIHAG"
        Name = "Vihag Aakriti Nabhasa"
        AakritiYogas.append("Vihag Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Kendra houses[4 and 10] [Bhandu and Karma Bhav]. Hence Vihag Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Vihag Yog will be fond of roaming, be a messenger, will live by sexual dealings, be shameless and interested in quarrels.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Shringatak Yoga - All planets are in trikona [Dharma]
    if( (gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,5,9]) == True) ):     
        #Shringatak Yoga formed
        IsAakritiYogaPresent = True
        Title = "SHRINGATAK"
        Name = "Shringatak Aakriti Nabhasa"
        AakritiYogas.append("Shringatak Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Dharma Trikona houses[1,5 and 9] [Tanu, Santaan and Bhagya Bhav]. Hence Shringatak Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Shringatak Yog will be fond of quarrels and battles, be happy, dear to king, endowed with an auspicious wife, be rich and will hate women.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Hala Yoga - All planets are in trikona [Artha, Kama or Moksha]
    if( (gen.check_ifAllNumInSetA_in_SetB(planethouses, [2,6,10]) == True) or
        (gen.check_ifAllNumInSetA_in_SetB(planethouses, [3,7,11]) == True) or
        (gen.check_ifAllNumInSetA_in_SetB(planethouses, [4,8,12]) == True)):     
        #Hala Yoga formed
        IsAakritiYogaPresent = True
        Title = "HALA"
        Name = "Hala Aakriti Nabhasa"
        AakritiYogas.append("Hala Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in Trikona houses[apart from dharma]. Hence Hala Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Hala Yog will eat a lot, will be very poor, will be miserable, gitated, given up by friends and relatives. He will be a servant.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Vajra Yoga 
    if( (gen.check_ifAllNumInSetA_in_SetB(benefichouses, [1,7]) == True)):     
        #Vajra Yoga formed
        IsAakritiYogaPresent = True
        Title = "VAJRA"
        Name = "Vajra Aakriti Nabhasa"
        AakritiYogas.append("Vajra Aakriti Nabhasa Yoga")
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
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Vajra Yoga 
    if( (gen.check_ifAllNumInSetA_in_SetB(malefichouses, [4,10]) == True)):     
        #Vajra Yoga formed
        IsAakritiYogaPresent = True
        Title = "VAJRA"
        Name = "Vajra Aakriti Nabhasa"
        AakritiYogas.append("Vajra Aakriti Nabhasa Yoga")
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
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Yav Yoga 
    if( (gen.check_ifAllNumInSetA_in_SetB(benefichouses, [4,10]) == True)):     
        #Yav Yoga formed
        IsAakritiYogaPresent = True
        Title = "YAV"
        Name = "Yav Aakriti Nabhasa"
        AakritiYogas.append("Yav Aakriti Nabhasa Yoga")
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
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Yav Yoga 
    if( (gen.check_ifAllNumInSetA_in_SetB(malefichouses, [1,7]) == True)):     
        #Yav Yoga formed
        IsAakritiYogaPresent = True
        Title = "YAV"
        Name = "Yav Aakriti Nabhasa"
        AakritiYogas.append("Yav Aakriti Nabhasa Yoga")
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
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Kamala Yoga - All planets are in kendra
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,4,7,10]) == True):     
        #Kamala Yoga formed
        IsAakritiYogaPresent = True
        Title = "KAMALA"
        Name = "Kamala Aakriti Nabhasa"
        AakritiYogas.append("Kamala Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All 7 planets from Sun to Saturn are in kendra houses[1,4,7,10]. Hence Kamala Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Kamala Yog will be rich and virtuous, be long lived, very famous and pure. He will perform hundreds of auspicious acts and he will be a king.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Vapi Yoga - No planets are in kendra
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [2,3,5,6,8,9,11,12]) == True):     
        #Vapi Yoga formed
        IsAakritiYogaPresent = True
        Title = "VAPI"
        Name = "Vapi Aakriti Nabhasa"
        AakritiYogas.append("Vapi Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''None of 7 planets from Sun to Saturn are in kendra houses[1,4,7,10]. Hence Vapi Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Vapi Yog will be capable of accumulating wealth, be endowed with lasting wealth and happiness and sons, be free from eye afflictions and will be a king.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Yupa Yoga - No planets are in kendra
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,2,3,4]) == True):     
        #Yupa Yoga formed
        IsAakritiYogaPresent = True
        Title = "YUPA"
        Name = "Yupa Aakriti Nabhasa"
        AakritiYogas.append("Yupa Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[1,2,3,4]. Hence Yupa Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Yupa Yog will have spiritual knowledge and will be interested in sacrificial rites. He will be endowed with a wife, be strong, interested in fasts and other religious observations and be distinguished.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    #Shara Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [4,5,6,7]) == True):     
        #Shara Yoga formed
        IsAakritiYogaPresent = True
        Title = "SHARA"
        Name = "Shara Aakriti Nabhasa"
        AakritiYogas.append("Shara Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[4,5,6,7]. Hence Shara Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Shara Yog will make arrows, be head of a prison, will earn through animals, will eat meat, will indulge in torture and mean handiworks.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Shakti Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [7,8,9,10]) == True):     
        #Shakti Yoga formed
        IsAakritiYogaPresent = True
        Title = "SHAKTI"
        Name = "Shakti Aakriti Nabhasa"
        AakritiYogas.append("Shakti Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[7,8,9,10]. Hence Shakti Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Shakti Yog will be bereft of wealth, be unsuccessful, miserable, mean, lazy, long lived, interested and skilful in war, firm and auspicious.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    #Danda Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [10,11,12,1]) == True):     
        #Danda Yoga formed
        IsAakritiYogaPresent = True
        Title = "DANDA"
        Name = "Danda Aakriti Nabhasa"
        AakritiYogas.append("Danda Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[10,11,12,1]. Hence Danda Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Danda Yog will lose sons and wife, will be indigent, unkind, away from his men and will serve mean people.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
    
    #Nauka Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,2,3,4,5,6,7]) == True):     
        #Nauka Yoga formed
        IsAakritiYogaPresent = True
        Title = "NAUKA"
        Name = "Nauka Aakriti Nabhasa"
        AakritiYogas.append("Nauka Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[1,2,3,4,5,6,7]. Hence Nauka Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Nauka Yog will derive his livelihood through water, be wealthy, famous, wicked, wretched, dirty and miserly.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    #Koota Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [4,5,6,7,8,9,10]) == True):     
        #Koota Yoga formed
        IsAakritiYogaPresent = True
        Title = "KOOTA"
        Name = "Koota Aakriti Nabhasa"
        AakritiYogas.append("Koota Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[4,5,6,7,8,9,10]. Hence Koota Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Koota Yog will be a liar, will head a jail, be poor, crafty, cruel and will live in hills and fortresses.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    #Chatra Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [7,8,9,10,11,12,1]) == True):     
        #Chatra Yoga formed
        IsAakritiYogaPresent = True
        Title = "CHATRA"
        Name = "Chatra Aakriti Nabhasa"
        AakritiYogas.append("Chatra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[7,8,9,10,11,12,1]. Hence Chatra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Chatra Yog will help his own men, be kind, dear to many kings, very intelligent, happy at the beginning and end of his life and be long-lived.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    #Dhanushi Yoga 
    elif(gen.check_ifAllNumInSetA_in_SetB(planethouses, [10,11,12,1,2,3,4]) == True):     
        #Dhanushi Yoga formed
        IsAakritiYogaPresent = True
        Title = "DHANUSHI"
        Name = "Dhanushi Aakriti Nabhasa"
        AakritiYogas.append("Dhanushi Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[10,11,12,1,2,3,4]. Hence Dhanushi Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Dhanushi Yog will be liar, will protect secrets, be a thief, be fond of wandering, forests, be devoid of luck and be happy in the middle of the life.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""
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
        AakritiYogas.append("Ardha-Chandra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in continuous 7 signs forming half moon shape. Hence Ardha-Chandra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Ardha-Chandra Yog will lead an Army, will possess a splendourous body, be dear to king, be strong and endowed with gems, gold and ornaments.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    #Chakra Yoga 
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [1,3,5,7,9,11]) == True): 
        #Chakra Yoga formed
        IsAakritiYogaPresent = True
        Title = "CHAKRA"
        Name = "Chakra Aakriti Nabhasa"
        AakritiYogas.append("Chakra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[1,3,5,7,9,11]. Hence Chakra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Chakra Yog will be an emperor, at whose feet will be the prostrating kings, heads, adoring gem studded diadems.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    #Samudra Yoga 
    if(gen.check_ifAllNumInSetA_in_SetB(planethouses, [2,4,6,8,10,12]) == True): 
        #Samudra Yoga formed
        IsAakritiYogaPresent = True
        Title = "SAMUDRA"
        Name = "Samudra Aakriti Nabhasa"
        AakritiYogas.append("Samudra Aakriti Nabhasa Yoga")
        Note = "None"
        Rule = f'''All of 7 planets from Sun to Saturn are in houses[2,4,6,8,10,12]. Hence Samudra Yoga which is a part of Aakriti yogas in Nabhasa yogas is formed.'''
        Results = f'''According to Parashara, One born in Samudra Yog will have many precious stones and abundant wealth, be endowed with pleasures, dear to people, will have firm wealth and be well disposed.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAakritiYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    return IsAakritiYogaPresent

def AmalaYoga(charts):
    IsAmalaYogaPresent = False
    Name = ""
    Rule = ""
    Title = ""
    Results = ""
    Note = ""

    relevant_planets = []
    colorlist = ["pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink","pink"]

    IsAmalaYogaPresent_lagna = False
    IsAmalaYogaPresent_moon = False

    #Only benefic is present in 10th house from lagna or from moon then Amala yoga is formed.
    moonhouse = charts["D1"]["planets"]["Moon"]["house-num"]
    tenthHouse4mMoon = gen.compute_nthsign(moonhouse,10)    
    planets_tenthfromlagna = charts["D1"]["houses"][10-1]["planets"]
    planets_tenthfrommoon = charts["D1"]["houses"][tenthHouse4mMoon-1]["planets"]
    Aspecingplanets_tenthfromlagna = charts["D1"]["houses"][10-1]["aspect-planets"]
    Aspecingplanets_tenthfrommoon = charts["D1"]["houses"][tenthHouse4mMoon-1]["aspect-planets"]
    naturalBenefics = charts["D1"]["classifications"]["natural-benefics"]
    naturalMalefics = charts["D1"]["classifications"]["natural-malefics"]
    #print(f'''moon house = {moonhouse} and 10th from moon : {tenthHouse4mMoon}
    #Planets in 10thfrom moon : {planets_tenthfrommoon} and natural benefics are {naturalBenefics}''')
    

    #Check if Amala yoga exists with respect to Lagna
    beneficsInTenth4mLagna = gen.list_intersection(naturalBenefics,planets_tenthfromlagna)
    maleficsInTenth4mLagna = gen.list_intersection(naturalMalefics,planets_tenthfromlagna)
    beneficsAspectingTenth4mLagna = gen.list_intersection(naturalBenefics,Aspecingplanets_tenthfromlagna)
    maleficsAspectingTenth4mLagna = gen.list_intersection(naturalMalefics,Aspecingplanets_tenthfromlagna)

    if((len(beneficsInTenth4mLagna)>0) and (len(maleficsInTenth4mLagna)==0)):
        IsAmalaYogaPresent_lagna = True
        Title = "AMALA"
        Name = "Amala"
        Rule = f'''The benefics {beneficsInTenth4mLagna} are placed in 10th house and are not conjoint with any malefics.
        '''
        colorlist[0] = "yellow"
        colorlist[9] = "yellow"
        for p in beneficsInTenth4mLagna:
            relevant_planets.append(p[0:2])
        #Check if any benefic aspects are there
        if(len(beneficsAspectingTenth4mLagna)>0):
            Note = f'''{Note}There is benefic aspect on 10th house from lagna by {beneficsAspectingTenth4mLagna} which strengthens this Yoga.
            '''
            for p in beneficsAspectingTenth4mLagna:
                relevant_planets.append(p[0:2])
        else:
            Note = f'''{Note}There is no benefic aspect on 10th house from lagna.
            '''
        #Check if any malefic aspects are there
        if(len(maleficsAspectingTenth4mLagna)>0):
            Note = f'''{Note}There is malefic aspect on 10th house from lagna by {maleficsAspectingTenth4mLagna} which weakens this Yoga.
            '''
            for p in maleficsAspectingTenth4mLagna:
                relevant_planets.append(p[0:2])
        else:
            Note = f'''{Note}There is no malefic aspect on 10th house from lagna.
            '''

    #Check if Amala yoga exists with respect to Moon
    beneficsInTenth4mMoon = gen.list_intersection(naturalBenefics,planets_tenthfrommoon)
    maleficsInTenth4mMoon = gen.list_intersection(naturalMalefics,planets_tenthfrommoon)
    beneficsAspectingTenth4mMoon = gen.list_intersection(naturalBenefics,Aspecingplanets_tenthfrommoon)
    maleficsAspectingTenth4mMoon = gen.list_intersection(naturalMalefics,Aspecingplanets_tenthfrommoon)

    if((len(beneficsInTenth4mMoon)>0) and (len(maleficsInTenth4mMoon)==0)):
        IsAmalaYogaPresent_moon = True
        Title = "AMALA"
        Name = "Amala"
        Rule = f'''{Rule}The benefics {beneficsInTenth4mMoon} are placed in 10th house from Moon and are not conjoint with any malefics.
        '''
        colorlist[moonhouse-1] = "yellow"
        colorlist[tenthHouse4mMoon-1] = "yellow"
        relevant_planets.append("Mo")
        for p in beneficsInTenth4mMoon:
            relevant_planets.append(p[0:2])
        #Check if any benefic aspects are there
        if(len(beneficsAspectingTenth4mMoon)>0):
            Note = f'''{Note}There is benefic aspect on 10th house from Moon by {beneficsAspectingTenth4mMoon} which strengthens this Yoga.
            '''
            for p in beneficsAspectingTenth4mMoon:
                relevant_planets.append(p[0:2])
        else:
            Note = f'''{Note}There is no benefic aspect on 10th house from Moon.
            '''
        #Check if any malefic aspects are there
        if(len(maleficsAspectingTenth4mMoon)>0):
            Note = f'''{Note}There is malefic aspect on 10th house from Moon by {maleficsAspectingTenth4mLagna} which weakens this Yoga.
            '''
            for p in maleficsAspectingTenth4mMoon:
                relevant_planets.append(p[0:2])
        else:
            Note = f'''{Note}There is no malefic aspect on 10th house from Moon.
            '''
    
    IsAmalaYogaPresent = IsAmalaYogaPresent_moon or IsAmalaYogaPresent_lagna
    
    if (IsAmalaYogaPresent == True):   
        Rule = f'''{Rule}Hence Amala Yoga is formed.''' 
        Results = f'''According to Parashara, Amal Yog will confer long lasting fame  and will make the native honoured by the king, enjoy abundant pleasures, charitable, fond of relatives, helpful to others, pious and virtuous.
        According to Phaladeepika, The person born with Amala Yoga at birth will be virtuous, will have faith in religion, will be happy, fortunate, will be honoured by the king, have an amiable nature and will always have a smile on his face.
        '''

        #Update the yogadosha sections
        yogadoshas_dict[Title] = {}
        yogadoshas_dict[Title]["name"] = Name
        yogadoshas_dict[Title]["type"] = "Yoga"
        yogadoshas_dict[Title]["exist"] = IsAmalaYogaPresent
        yogadoshas_dict[Title]["Rule"] = iterativeReplace(Rule,"\n ", "\n")
        yogadoshas_dict[Title]["Result"] = iterativeReplace(Results,"\n ", "\n").replace("\n","\n        ") 
        yogadoshas_dict[Title]["Note"] = iterativeReplace(Note,"\n ", "\n")
        yogadoshas_dict[Title]["Source"] = ""

    return IsAmalaYogaPresent


#Main function to load and compute all yogas and doshas and update the json file
def ComputeYogaDoshas(charts):
    global yogadoshas_dict
    yogadoshas_dict = {}
    #Empty previous added yogas as it may be for previous person
    global parivarthanaYogas 
    global AshrayaYogas 
    global DalaYogas 
    global AakritiYogas 
    global SankhyaYogas 

    parivarthanaYogas = []
    AshrayaYogas = []
    DalaYogas = []
    AakritiYogas = []
    SankhyaYogas = []
    #Get the existing Data from Yogadosha json file.
    #js.load_yogadoshas()
    charts["yogadoshas"] = []

    #Lets check for various Yogas
    #Pancha-mahapurusha yogas
    if(RuchakaYoga(charts)==True): #Ruchaka by Mars
        charts["yogadoshas"].append("Ruchaka Panchamahapurusha Yoga")    
    if(BhadraYoga(charts)==True):  #Bhadra by Mercury
        charts["yogadoshas"].append("Bhadra Panchamahapurusha Yoga") 
    if(HamsaYoga(charts)==True):    #Hamsa by Jupiter
        charts["yogadoshas"].append("Hamsa Panchamahapurusha Yoga")
    if(MalavyaYoga(charts)==True):    #Malavya by Venus
        charts["yogadoshas"].append("Malavya Panchamahapurusha Yoga")   
    if(SasaYoga(charts)==True):    #Sasa by Saturn
        charts["yogadoshas"].append("Sasa Panchamahapurusha Yoga")

    #Vipareeta Raja yogas
    if(HarshaYoga(charts)==True): #HarshaYoga by Dusthana Lord in 6th house
        charts["yogadoshas"].append("Harsha Vipareeta RajaYoga")
    if(SaralaYoga(charts)==True): #SaralaYoga by Dusthana Lord in 8th house
        charts["yogadoshas"].append("Sarala Vipareeta RajaYoga")
    if(VimalaYoga(charts)==True): #VimalaYoga by Dusthana Lord in 12th house
        charts["yogadoshas"].append("Vimala Vipareeta RajaYoga")
    
    #Gaja Kesari Yoga
    if(GajaKesariYoga(charts)==True): #GajaKesari by Moon and Jupiter
        charts["yogadoshas"].append("GajaKesari Yoga")

    #Amala Yoga
    if(AmalaYoga(charts)==True): #Amala by benefic planet in the 10th house from the Lagna or the Moon.
        charts["yogadoshas"].append("Amala Yoga")

    #Chandra Mangala Yoga
    if(ChandraMangalaYoga(charts)==True): #Chandramangala by Moon and Mars
        charts["yogadoshas"].append("ChandraMangala Yoga")

    #Parivarthana Yogas
    if(ParivarthanaYoga(charts)==True): #Exchange of sign placements between 2 planets
        for yoga in parivarthanaYogas:
            charts["yogadoshas"].append(yoga)

    #Nabhasa Yogas
    #Aashraya Yogas
    if(AashrayaYoga(charts)==True): #All planets in same swabhava signs - chara, sthira, dwi
        for yoga in AshrayaYogas:
            charts["yogadoshas"].append(yoga)
    #Dala Yogas
    if(DalaYoga(charts)==True): #All Benefic and Malefic planets have formed dala and one category is in kendra and other is not
        for yoga in DalaYogas:
            charts["yogadoshas"].append(yoga)
    #Aakriti Yogas 
    if(AakritiYoga(charts)==True): #All Benefic and Malefic planets have formed dala and one category is in kendra and other is not
        for yoga in AakritiYogas:
            charts["yogadoshas"].append(yoga)
    #Sankhya Yogas
    if(SankhyaYoga(charts)==True): #Depending on how many signs are all 7 planets occupying
        for yoga in SankhyaYogas:
            charts["yogadoshas"].append(yoga)

    
    #Kaal Sarpa Doshas
    if(AnantaKaalSarpaDosha(charts)==True): #AnantaKaalSarpaDosha Rahu ketu axis (1-7)
        charts["yogadoshas"].append("Ananta Kaala Sarpa Dosha")
    elif(KulikaKaalSarpaDosha(charts)==True): #KulikaKaalSarpaDosha Rahu ketu axis (2-8)
        charts["yogadoshas"].append("Kulika Kaala Sarpa Dosha")
    elif(VasukiKaalSarpaDosha(charts)==True): #VasukiKaalSarpaDosha Rahu ketu axis (3-9)
        charts["yogadoshas"].append("Vasuki Kaala Sarpa Dosha")
    elif(ShankhapalaKaalSarpaDosha(charts)==True): #ShankhapalaKaalSarpaDosha Rahu ketu axis (4-10)
        charts["yogadoshas"].append("Shankhapala Kaala Sarpa Dosha")
    elif(PadamKaalSarpaDosha(charts)==True): #PadamKaalSarpaDosha Rahu ketu axis (5-11)
        charts["yogadoshas"].append("Padam Kaala Sarpa Dosha")
    elif(MahapadmaKaalSarpaDosha(charts)==True): #MahapadmaKaalSarpaDosha Rahu ketu axis (6-12)
        charts["yogadoshas"].append("Mahapadma Kaala Sarpa Dosha")
    elif(TakshakaKaalSarpaDosha(charts)==True): #TakshakaKaalSarpaDosha Rahu ketu axis (7-1)
        charts["yogadoshas"].append("Takshaka Kaala Sarpa Dosha")
    elif(KarkotakKaalSarpaDosha(charts)==True): #KarkotakKaalSarpaDosha Rahu ketu axis (8-2)
        charts["yogadoshas"].append("Karkotak Kaala Sarpa Dosha")
    elif(ShankhachurKaalSarpaDosha(charts)==True): #ShankhachurKaalSarpaDosha Rahu ketu axis (9-3)
        charts["yogadoshas"].append("Shankachur Kaala Sarpa Dosha")
    elif(GhatakKaalSarpaDosha(charts)==True): #GhatakKaalSarpaDosha Rahu ketu axis (10-4)
        charts["yogadoshas"].append("Ghatak Kaala Sarpa Dosha")
    elif(VishadharaKaalSarpaDosha(charts)==True): #VishadharaKaalSarpaDosha Rahu ketu axis (11-5)
        charts["yogadoshas"].append("Vishadhara Kaala Sarpa Dosha")
    elif(SheshanagaKaalSarpaDosha(charts)==True): #SheshanagaKaalSarpaDosha Rahu ketu axis (12-6)
        charts["yogadoshas"].append("Sheshanaga Kaala Sarpa Dosha")
    else:
        pass

    return yogadoshas_dict   
    return
    


if __name__ == "__main__":
    ComputeYogaDoshas(charts)
    #print(yogadoshas)