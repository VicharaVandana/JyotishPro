import support.globalvariables as gvar
import support.yogadoshas as yd
import support.astrochart as ac
from fpdf import FPDF
from datetime import datetime as dt
from support.balascalculation import BalaNeededValues as need
from scipy.stats import rankdata
import support.lordinhouses as lhpredictions

global mychart
global reportLevel 
reportLevel = "BASIC"


def GetPlanetDataArray(planetdata, lagnadata):
    PlanetsData = []
    PlanetsData = [   ("Planet","Degrees","House","Sign","SignLord","Nak","Nak-Lord")  ]
    PlanetsData.append(("Asc",f'{round(lagnadata["pos"]["dec_deg"], 3)}',"1",str(lagnadata["sign"]),lagnadata["lagna-lord"],lagnadata["nakshatra"],lagnadata["nak-ruler"]))
    l_plt = "Sun"
    PlanetsData.append((l_plt,f'{round(planetdata[l_plt]["pos"]["dec_deg"], 3)}',str(planetdata[l_plt]["house-num"]),str(planetdata[l_plt]["sign"]),planetdata[l_plt]["dispositor"],planetdata[l_plt]["nakshatra"],planetdata[l_plt]["nak-ruler"]))
    l_plt = "Moon"
    PlanetsData.append((l_plt,f'{round(planetdata[l_plt]["pos"]["dec_deg"], 3)}',str(planetdata[l_plt]["house-num"]),str(planetdata[l_plt]["sign"]),planetdata[l_plt]["dispositor"],planetdata[l_plt]["nakshatra"],planetdata[l_plt]["nak-ruler"]))
    l_plt = "Mars"
    PlanetsData.append((l_plt,f'{round(planetdata[l_plt]["pos"]["dec_deg"], 3)}',str(planetdata[l_plt]["house-num"]),str(planetdata[l_plt]["sign"]),planetdata[l_plt]["dispositor"],planetdata[l_plt]["nakshatra"],planetdata[l_plt]["nak-ruler"]))
    l_plt = "Mercury"
    PlanetsData.append((l_plt,f'{round(planetdata[l_plt]["pos"]["dec_deg"], 3)}',str(planetdata[l_plt]["house-num"]),str(planetdata[l_plt]["sign"]),planetdata[l_plt]["dispositor"],planetdata[l_plt]["nakshatra"],planetdata[l_plt]["nak-ruler"]))
    l_plt = "Jupiter"
    PlanetsData.append((l_plt,f'{round(planetdata[l_plt]["pos"]["dec_deg"], 3)}',str(planetdata[l_plt]["house-num"]),str(planetdata[l_plt]["sign"]),planetdata[l_plt]["dispositor"],planetdata[l_plt]["nakshatra"],planetdata[l_plt]["nak-ruler"]))
    l_plt = "Venus"
    PlanetsData.append((l_plt,f'{round(planetdata[l_plt]["pos"]["dec_deg"], 3)}',str(planetdata[l_plt]["house-num"]),str(planetdata[l_plt]["sign"]),planetdata[l_plt]["dispositor"],planetdata[l_plt]["nakshatra"],planetdata[l_plt]["nak-ruler"]))
    l_plt = "Saturn"
    PlanetsData.append((l_plt,f'{round(planetdata[l_plt]["pos"]["dec_deg"], 3)}',str(planetdata[l_plt]["house-num"]),str(planetdata[l_plt]["sign"]),planetdata[l_plt]["dispositor"],planetdata[l_plt]["nakshatra"],planetdata[l_plt]["nak-ruler"]))
    l_plt = "Rahu"
    PlanetsData.append((l_plt,f'{round(planetdata[l_plt]["pos"]["dec_deg"], 3)}',str(planetdata[l_plt]["house-num"]),str(planetdata[l_plt]["sign"]),planetdata[l_plt]["dispositor"],planetdata[l_plt]["nakshatra"],planetdata[l_plt]["nak-ruler"]))
    l_plt = "Ketu"
    PlanetsData.append((l_plt,f'{round(planetdata[l_plt]["pos"]["dec_deg"], 3)}',str(planetdata[l_plt]["house-num"]),str(planetdata[l_plt]["sign"]),planetdata[l_plt]["dispositor"],planetdata[l_plt]["nakshatra"],planetdata[l_plt]["nak-ruler"]))
    return PlanetsData

def getWidthArray(data, IsRowColorGiven):
    rowCount = len(data)
    if (IsRowColorGiven == True):
        colCount = len(data[0]) - 1
    else:
        colCount = len(data[0])
    sizearray = []
    widtharray = []
    totSize = 0
    #compute max length word in each column
    for j in range(0,colCount):
        #for every column
        bigwordsize = len(data[0][j]) + 2
        for i in range(0,rowCount):
            currentwordsize = len(str(data[i][j]))
            if(currentwordsize > bigwordsize):
                bigwordsize = currentwordsize
        sizearray.append(bigwordsize)
        totSize = totSize + bigwordsize

    for item in sizearray:
        item_Percent = (item * 100)/totSize
        widtharray.append(int(item_Percent))
    return(widtharray)
def htmlrow_Shadbala_withoutBase(bala, values, rowclr = "white"):
    htmlcontent = f'''<tr bgcolor={rowclr}>
                            
                            <td align="left">{bala}</td>
                            '''
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        htmlcontent = f'''{htmlcontent} <td align="center"><font color="black">{values[planet]}</font></td> '''

    htmlcontent = f'''{htmlcontent} </tr>'''

    return htmlcontent

def htmlrow_Shadbala_withBase(bala, values, row1clr = "white",row2clr="white"):
    htmlcontent = f'''<tr bgcolor={row1clr}>
                            <td align="left">{bala}(Needed)</td>                            
                            <td align="center">{need[bala]["Sun"]}</td>
                            <td align="center">{need[bala]["Moon"]}</td>
                            <td align="center">{need[bala]["Mars"]}</td>
                            <td align="center">{need[bala]["Mercury"]}</td>
                            <td align="center">{need[bala]["Jupiter"]}</td>
                            <td align="center">{need[bala]["Venus"]}</td>
                            <td align="center">{need[bala]["Saturn"]}</td>
                        </tr>
                        <tr bgcolor={row2clr}>
                            <td align="left">{bala}(Actual)</td>
                            '''
    for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
        if(values[planet] > need[bala][planet]):
            textclr = "green"
        elif(values[planet] < need[bala][planet]):
            textclr = "red"
        else:
            textclr = "black"
        htmlcontent = f'''{htmlcontent} <td align="center"><font color="{textclr}">{values[planet]}</font></td> '''

    htmlcontent = f'''{htmlcontent} </tr>'''

    return htmlcontent

def create_ShadbalaTableHtml():
    shadbalas= mychart["Balas"]["Shadbala"]
    #Update Shadbala Heading
    heading = f'''<tr bgcolor = "black"> <font color="white">
                    <th width="{30}%" align="center">Bala</th>
                    <th width="{10}%" align="center">Sun</th>
                    <th width="{10}%" align="center">Moon</th>
                    <th width="{10}%" align="center">Mars</th>
                    <th width="{10}%" align="center">Mercury</th>
                    <th width="{10}%" align="center">Jupiter</th>
                    <th width="{10}%" align="center">Venus</th>
                    <th width="{10}%" align="center">Saturn</th> </font>
                </tr>'''
    
    shadbalatotal = htmlrow_Shadbala_withBase("Shadbala", shadbalas["Total"],row1clr="white",row2clr="yellow")                    
    sthanabala = htmlrow_Shadbala_withBase("Sthanabala", shadbalas["Sthanabala"]["Total"],row1clr="white",row2clr="yellow")
    uchhabala = htmlrow_Shadbala_withoutBase("Sthana --> Uchhabala",shadbalas["Sthanabala"]["Uchhabala"], "#FFFFCC")
    saptavargajabala = htmlrow_Shadbala_withoutBase("Sthana --> Saptavargajabala",shadbalas["Sthanabala"]["Saptavargajabala"], "#FFFFCC")
    ojhayugmarashiamshabala = htmlrow_Shadbala_withoutBase("Sthana --> Ojhayugmarashiamshabala",shadbalas["Sthanabala"]["Ojhayugmarashiamshabala"], "#FFFFCC")
    kendradhibala = htmlrow_Shadbala_withoutBase("Sthana --> Kendradhibala",shadbalas["Sthanabala"]["Kendradhibala"], "#FFFFCC")
    drekshanabala = htmlrow_Shadbala_withoutBase("Sthana --> Drekshanabala",shadbalas["Sthanabala"]["Drekshanabala"], "#FFFFCC")
    digbala = htmlrow_Shadbala_withBase("Digbala", shadbalas["Digbala"],row1clr="white",row2clr="yellow")
    kaalabala = htmlrow_Shadbala_withBase("Kaalabala", shadbalas["Kaalabala"]["Total"],row1clr="white",row2clr="yellow")
    natonnatabala = htmlrow_Shadbala_withoutBase("Kaala --> Natonnatabala",shadbalas["Kaalabala"]["Natonnatabala"], "#FFFFCC")
    pakshabala = htmlrow_Shadbala_withoutBase("Kaala --> Pakshabala",shadbalas["Kaalabala"]["Pakshabala"], "#FFFFCC")
    tribhagabala = htmlrow_Shadbala_withoutBase("Kaala --> Tribhagabala",shadbalas["Kaalabala"]["Tribhagabala"], "#FFFFCC")
    vmdhbala = htmlrow_Shadbala_withoutBase("Kaala --> VarshMaasDinaHoraBala",shadbalas["Kaalabala"]["Varsha-maasa-dina-horabala"], "#FFFFCC")
    yuddhabala = htmlrow_Shadbala_withoutBase("Kaala --> Yuddhabala",shadbalas["Kaalabala"]["Yuddhabala"], "#FFFFCC")
    ayanabala = htmlrow_Shadbala_withBase("Ayanabala", shadbalas["Kaalabala"]["Ayanabala"],row1clr="white",row2clr="yellow")
    cheshtabala = htmlrow_Shadbala_withBase("Cheshtabala",shadbalas["Cheshtabala"], row1clr="white",row2clr="yellow")
    naisargikabala = htmlrow_Shadbala_withoutBase("Naisargikabala",shadbalas["Naisargikabala"], "yellow")
    drikbala = htmlrow_Shadbala_withoutBase("Drikbala",shadbalas["Drikbala"], "yellow")
    
    
    
    


    html_Table = f'''<table>
                        {heading}
                        {shadbalatotal}
                        {sthanabala}
                        {uchhabala}
                        {saptavargajabala}
                        {ojhayugmarashiamshabala}
                        {kendradhibala}
                        {drekshanabala}
                        {digbala}
                        {kaalabala}
                        {natonnatabala}
                        {pakshabala}
                        {tribhagabala}
                        {vmdhbala}
                        {yuddhabala}
                        {ayanabala}
                        {cheshtabala}
                        {naisargikabala}
                        {drikbala}                         
                     </table>'''
    return html_Table

class PDF(FPDF):
    def render_toc(self, pdf, outline):
        pdf.set_y(35)
        pdf.set_x(pdf.l_margin)
        pdf.set_font('Times', 'B', 16)
        pdf.set_text_color(0, 0, 255)
        pdf.cell(w=0, h=10, txt="Table of Contents", ln=True, align="C")
        pdf.ln(5)
        pdf.set_font('Times', '', 12)
        pdf.set_text_color(0, 0, 0)
        for section in outline:
            link = pdf.add_link()
            pdf.set_link(link, page=section.page_number)
            # Create indent for sub-sections
            indent = "    " * section.level
            text = f"{indent}{section.name}"
            # Fill the middle with dots
            text_width = pdf.get_string_width(text)
            page_num_str = str(section.page_number)
            page_num_width = pdf.get_string_width(page_num_str)
            dots_width = pdf.w - pdf.l_margin - pdf.r_margin - text_width - page_num_width - 5
            dots = "." * max(1, int(dots_width / pdf.get_string_width(".")))
            line_text = f"{text} {dots} {page_num_str}"
            pdf.cell(w=0, h=8, txt=line_text, ln=True, link=link)

    def safe_image(self, name, x=None, y=None, w=0, h=0, type='', link=''):
        import os
        if os.path.exists(name):
            self.image(name, x=x, y=y, w=w, h=h, type=type, link=link)
        else:
            if x is not None and y is not None:
                self.set_xy(x, y)
                self.cell(txt="Image Missing", w=w, h=h if h else w, border=1, align='C')



    def header(self):
        # Logo
        self.safe_image('./images/jyotishyamitra_logo.png', 185, 2, h=20, w=20)
        # Times bold 15
        self.set_font('Times', 'B', 15)
        # Title
        self.cell(170, 10, f'Jyotishyamitra Astrology Report for {mychart["user_details"]["name"]}',ln=True,border=True, align='C')
        # Line break
        #self.ln(20)

    # Page footer
    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        # Times italic 8
        self.set_font('Times', 'I', 8)
        # Page number
        self.cell(0, 10, 'Page ' + str(self.page_no()) + '/{nb}', 0, 0, 'C')
        self.cell(0, 10, 'www.jyotishyamitra.in', 0, 0, 'R', link="https://www.jyotishyamitra.in")

    def loadAllCustomFonts(self):
        self.add_font("Lobster-Regular", "",
                        "./reports/fonts/Lobster-Regular.ttf",
                        uni=True)

    def writeTable(self,data,x,y,IsRowColorGiven):
        widtharray = getWidthArray(data, IsRowColorGiven)
        tabHead = ""
        tabBody = ""
        for rowNum in range(1,len(data)):
            if(IsRowColorGiven == False):
                tabBody = tabBody + f'''\n<tr><td>{'</td><td>'.join(data[rowNum])}</td></tr>'''
                headingcolor = "yellow"
                elements_countInARow = len(data[0])
            else:   #Row colour is last element of every row element
                if (data[rowNum][-1] == ""):
                    data[rowNum][-1] = "white"
                tabBody = tabBody + f'''\n<tr bgcolor={data[rowNum][-1]}><td>{'</td><td>'.join(data[rowNum][0:-1])}</td></tr>'''
                headingcolor = data[0][-1]
                elements_countInARow = len(data[0]) -1

        for colNum in range(0,elements_countInARow):
            tabHead = tabHead + f'''\n<th width="{widtharray[colNum]}%">{data[0][colNum]}</th>'''

        self.set_xy(x,y)
        self.write_html(
            f"""<table border="1"><thead><tr bgcolor={headingcolor}>
            {tabHead}
        </tr></thead>
        <tbody>{tabBody}
        </tbody></table>""",
            table_line_separators=True,
        )                               

    def addFirstPageBasic(self):
        self.set_font('Times', 'BU', 16)
        self.start_section("Jataka Details", level=0)
        self.cell(txt="Jataka Details", w=0, h=10, align='C')
        imageWidth = (self.w / 2.0) - 5
        #put Lagna chart 
        self.safe_image("./images/birthcharts/Lagna_chart.png", x=5, y=30, w=imageWidth)
        #setting caption 
        self.set_font('Courier', 'BI', 10)
        self.set_xy(5,30+imageWidth)    #caption position
        self.cell(txt="Lagna Chart", w=imageWidth, h=3, align='C')

        #planetary data table
        y_for_heading = 30 + imageWidth + 5
        self.set_xy(5, y_for_heading)
        self.set_font('Times', 'BU', 14)
        self.start_section("Planetary Positions", level=0)
        self.cell(txt="Planetery Details of Lagna Chart", w=0, h=10, align='C', ln=1)
        
        y_for_table = self.get_y() + 2
        self.writeTable(GetPlanetDataArray(mychart["D1"]["planets"], mychart["D1"]["ascendant"]), 5, y_for_table, False)

        #User details Box
        self.set_font('Courier', 'B', 12)
        userdetails = f'''Lagna : {mychart["D1"]["ascendant"]["sign"]} / {mychart["D1"]["ascendant"]["rashi"]}
Lagnesh : {mychart["D1"]["ascendant"]["lagna-lord"]}
Rashi : {mychart["D1"]["planets"]["Moon"]["sign"]} / {mychart["D1"]["planets"]["Moon"]["rashi"]}
Nakshatra : {mychart["D1"]["planets"]["Moon"]["nakshatra"]}
NakshatraLord : {mychart["D1"]["planets"]["Moon"]["nak-ruler"]}
Maasa : {mychart["user_details"].get("maasa", "")}
Tithi : {mychart["user_details"].get("tithi", "")}
Vaara : {mychart["user_details"].get("vaara", "")}
Yoga : {mychart["user_details"].get("yoga", "")}
Karana : {mychart["user_details"].get("karana", "")}
'''

        self.set_xy(18+imageWidth,30)
        self.multi_cell(w=(self.w - imageWidth - 23),h=6, txt=userdetails, align='L', border=True)

    def addVargaChartsinaPage(self):
        #title of the page
        self.set_font('Times', 'BU', 12)
        self.start_section("Shodasha Varga Charts", level=0)
        self.cell(txt="Shodasha Varga Charts", w=0, h=10, align='C')
        
        self.set_font('Times', 'BI', 10)
        imageWidth = (self.w / 3.0) - 5
        self.set_fill_color(255,255,0)  #yellow colour

        #first comes Lagna chart
        self.safe_image("./images/birthcharts/Lagna_chart.png", x=5, y=35, w=imageWidth)
        #setting caption 
        self.set_xy(5,35+imageWidth)    #caption position
        self.cell(txt="D1 - Lagna Chart", w=imageWidth, h=3, align='C', ln=1)
        self.multi_cell(txt="Physical appearance, Health, Entire life",w=imageWidth, h=3, fill=1)

        #next comes Navamsa chart
        self.safe_image("./images/birthcharts/Navamsa_chart.png", x=5+imageWidth+2, y=35, w=imageWidth)
        #setting caption 
        self.set_xy(5+imageWidth+2,35+imageWidth)    #caption position
        self.cell(txt="D9 - Navamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+imageWidth+2)
        self.multi_cell(txt="Spouse, Marriage, Business, Second half of life",w=imageWidth, h=3, fill=1)

        #next comes Dasamsa chart
        self.safe_image("./images/birthcharts/Dasamsa_chart.png", x=5+(2*imageWidth)+4, y=35, w=imageWidth)
        #setting caption 
        self.set_xy(5+(2*imageWidth)+4,35+imageWidth)    #caption position
        self.cell(txt="D10 - Dasamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(2*imageWidth)+4)
        self.multi_cell(txt="Matters of great importance, career, honor, awards, fame",w=imageWidth, h=3, fill=1)
    ###############################################################################
        #next comes Hora chart
        self.safe_image("./images/birthcharts/Hora_chart.png", x=5, y=35 + imageWidth + 15, w=imageWidth)
        #setting caption 
        self.set_xy(5,35 + (2*imageWidth) + 15)    #caption position
        self.cell(txt="D2 - Hora Chart", w=imageWidth, h=3, align='C', ln=1)
        self.multi_cell(txt="Wealth, securities, assets",w=imageWidth, h=3, fill=1)

        #next comes Drekkana chart
        self.safe_image("./images/birthcharts/Drekkana_chart.png", x=5+imageWidth+2, y=35 + imageWidth + 15, w=imageWidth)
        #setting caption 
        self.set_xy(5+imageWidth+2,35 + (2*imageWidth) + 15)    #caption position
        self.cell(txt="D3 - Drekkana Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(1*imageWidth)+4)
        self.multi_cell(txt="Happiness through siblings",w=imageWidth, h=3, fill=1)

        #next comes Chaturtamsa chart
        self.safe_image("./images/birthcharts/Chaturtamsa_chart.png", x=5+(2*imageWidth)+4, y=35 + imageWidth + 15, w=imageWidth)
        #setting caption 
        self.set_xy(5+(2*imageWidth)+4,35 + (2*imageWidth) + 15)    #caption position
        self.cell(txt="D4 - Chaturtamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(2*imageWidth)+4)
        self.multi_cell(txt="Fortune, Unmovable Assets",w=imageWidth, h=3, fill=1)

    ###############################################################################
        #next comes Saptamsa chart
        self.safe_image("./images/birthcharts/Saptamsa_chart.png", x=5, y=35 + (2*imageWidth) + 30, w=imageWidth)
        #setting caption 
        self.set_xy(5,35 + (3*imageWidth) + 30)    #caption position
        self.cell(txt="D7 - Saptamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.multi_cell(txt="sons, grandsons, children",w=imageWidth, h=3, fill=1)

        #next comes Dwadasamsa chart
        self.safe_image("./images/birthcharts/Dwadasamsa_chart.png", x=5+imageWidth+2, y=35 + (2*imageWidth) + 30, w=imageWidth)
        #setting caption 
        self.set_xy(5+imageWidth+2,35 + (3*imageWidth) + 30)    #caption position
        self.cell(txt="D12 - Dwadasamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(1*imageWidth)+4)
        self.multi_cell(txt="Parents",w=imageWidth, h=3, fill=1)

        #next comes Shodasamsa chart
        self.safe_image("./images/birthcharts/Shodasamsa_chart.png", x=5+(2*imageWidth)+4, y=35 + (2*imageWidth) + 30, w=imageWidth)
        #setting caption 
        self.set_xy(5+(2*imageWidth)+4,35 + (3*imageWidth) + 30)    #caption position
        self.cell(txt="D16 - Shodasamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(2*imageWidth)+4)
        self.multi_cell(txt="Benefits, and adversities through vehicles",w=imageWidth, h=3, fill=1)

        #add one more page as current page is full
        self.add_page()
        self.set_font('Times', 'BU', 12)
        self.cell(txt="Shodasha Varga Charts - Continued", w=0, h=10, align='C')
        
        self.set_font('Times', 'BI', 10)
    ###############################################################################
        #next comes Vimsamsa chart
        self.safe_image("./images/birthcharts/Vimsamsa_chart.png", x=5, y=35, w=imageWidth)
        #setting caption 
        self.set_xy(5,35+imageWidth)    #caption position
        self.cell(txt="D20 - Vimsamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.multi_cell(txt="Spiritual life, Ishta Devata, Sadhana",w=imageWidth, h=3, fill=1)

        #next comes Chaturvimsamsa chart
        self.safe_image("./images/birthcharts/Chaturvimsamsa_chart.png", x=5+imageWidth+2, y=35, w=imageWidth)
        #setting caption 
        self.set_xy(5+imageWidth+2,35+imageWidth)    #caption position
        self.cell(txt="D24 - Chaturvimsamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(1*imageWidth)+4)
        self.multi_cell(txt="Learning, education",w=imageWidth, h=3, fill=1)

        #next comes Saptavimsamsa chart
        self.safe_image("./images/birthcharts/Saptavimsamsa_chart.png", x=5+(2*imageWidth)+4, y=35, w=imageWidth)
        #setting caption 
        self.set_xy(5+(2*imageWidth)+4,35+imageWidth)    #caption position
        self.cell(txt="D27 - Saptavimsamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(2*imageWidth)+4)
        self.multi_cell(txt="Strength, and weakness",w=imageWidth, h=3, fill=1)
    ###############################################################################
        #next comes Trimsamsa chart
        self.safe_image("./images/birthcharts/Trimsamsa_chart.png", x=5, y=35 + imageWidth + 15, w=imageWidth)
        #setting caption 
        self.set_xy(5,35 + (2*imageWidth) + 15)    #caption position
        self.cell(txt="D30 - Trimsamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.multi_cell(txt="Evil effects",w=imageWidth, h=3, fill=1)

        #next comes Khavedamsa chart
        self.safe_image("./images/birthcharts/Khavedamsa_chart.png", x=5+imageWidth+2, y=35 + imageWidth + 15, w=imageWidth)
        #setting caption 
        self.set_xy(5+imageWidth+2,35 + (2*imageWidth) + 15)    #caption position
        self.cell(txt="D40 - Khavedamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(1*imageWidth)+4)
        self.multi_cell(txt="Auspicious and inauspicious effec",w=imageWidth, h=3, fill=1)

        #next comes Akshavedamsa chart
        self.safe_image("./images/birthcharts/Akshavedamsa_chart.png", x=5+(2*imageWidth)+4, y=35 + imageWidth + 15, w=imageWidth)
        #setting caption 
        self.set_xy(5+(2*imageWidth)+4,35 + (2*imageWidth) + 15)    #caption position
        self.cell(txt="D45 - Akshavedamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(2*imageWidth)+4)
        self.multi_cell(txt="Legacy, Poorva doshas, Pirti doshas",w=imageWidth, h=3, fill=1)

    ###############################################################################
        #next comes Shashtiamsa chart
        self.safe_image("./images/birthcharts/Shashtiamsa_chart.png", x=5, y=35 + (2*imageWidth) + 30, w=imageWidth)
        #setting caption 
        self.set_xy(5,35 + (3*imageWidth) + 30)    #caption position
        self.cell(txt="D60 - Shashtiamsa Chart", w=imageWidth, h=3, align='C', ln=1)
        self.multi_cell(txt="Totality of results",w=imageWidth, h=3, fill=1)

    def createTitlePage(self):
        title = f'JyotishyaMitra Basic Report of {mychart["user_details"]["name"]}'
        self.set_font('Lobster-Regular', '', 25)
        self.set_text_color(255,0,0)
        self.ln(10)
        self.multi_cell(w=0,h=8, txt=title, align='C', border=False)
        self.ln(10)
        self.safe_image('./images/jyotishyamitra.png',  x=40)
        self.ln(5)
        #section for User details -TOB, DOB, POB
        self.set_font('Times', '', 18)
        self.set_text_color(0,0,130)
        creationdetails = f'''Created on: {dt.now().strftime("%d/%b/%Y [%A] - %H:%M:%S")}'''
        userdetail = f'''Date of birth:  {mychart["user_details"]["birthdetails"]["DOB"]["day"]}/{mychart["user_details"]["birthdetails"]["DOB"]["month"]}/{mychart["user_details"]["birthdetails"]["DOB"]["year"]}
Time Of birth:  {mychart["user_details"]["birthdetails"]["TOB"]["hour"]} : {mychart["user_details"]["birthdetails"]["TOB"]["min"]} : {mychart["user_details"]["birthdetails"]["TOB"]["sec"]} 
Place of Birth:  {mychart["user_details"]["birthdetails"]["POB"]["name"]}
{creationdetails}'''
        self.multi_cell(w=0,h=8, txt=userdetail, align='C', border=True)
        self.set_text_color(0,0,0)

    def addYogaDoshasSection(self, config=None):
        #title of the page
        self.set_font('helvetica', 'BU', 14)
        self.set_text_color(0,0,255)
        self.start_section("Yogas and Doshas", level=0)
        self.cell(txt="Yogas and Doshas in Native's Kundali", w=0, h=10, align='C')

        #Enlisting all the Yogas and doshas in natives kundali
        self.ln(10)
        table_html = f"""
        <table border="1" align="center" width="100%">
        <thead>
        <tr bgcolor="#e0e0e0">
            <th width="50%" align="center"><b>Name of Yoga/Dosha</b></th>
            <th width="25%" align="center"><b>Type</b></th>
            <th width="25%" align="center"><b>Status</b></th>
        </tr>
        </thead>
        <tbody>
        """
        for yg_key, yg_data in yd.common.yogadoshas_dict.items():
            yg_name = yg_data.get("name", yg_key)
            yg_type = yg_data.get("type", "Yoga")
            yg_status = "Existing" if yg_data.get("exist", False) else "Cancelled"
            
            # We only list if it's evaluated, meaning it exists or we explicitly want to list it
            # The config check is already done when compiling yogadoshas_dict.
            table_html += f"""
            <tr>
                <td align="left">{yg_name}</td>
                <td align="center">{yg_type}</td>
                <td align="center">{yg_status}</td>
            </tr>
            """
        table_html += "</tbody></table><br>"
        self.write_html(table_html)
        self.ln(5)


        
        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(5)

        self.set_font('Times', 'I', 11)
        self.set_text_color(100, 100, 100)
        self.cell(txt="(Detailed analysis and partial charts for each Yoga and Dosha begin on the next page)", w=0, h=5, align='C')
        self.ln(5)

        #Adding Each Yoga/Dosha details
        self.set_font('Times', '', 10)
        imageWidth = (self.w / 2)
        
        # We need to print details for only those that exist
        for yogadosha_key, yogadosha_data in yd.common.yogadoshas_dict.items():
            if not yogadosha_data.get("exist", False):
                continue
            
            self.add_page()
            yogadosha = yogadosha_data["name"]
            relevant_planets = yogadosha_data.get("relevant_planets", ["Su", "Mo", "Ma", "Me", "Ju", "Ve", "Sa", "Ra", "Ke"])

            # Generate partial chart on the fly
            chart_loc = "./images/yogaImages"
            os.makedirs(chart_loc, exist_ok=True)
            chart_name = yogadosha_key + "_chart"
            
            try:
                c_style = config.get("chartStyle", "north") if config else "north"
                ac.plot_partial_astrochart(chart_loc, chart_name, mychart, relevant_planets, div="D1", firsthousesign="None", language="english", chart_style=c_style)
                
                svg_path = os.path.join(chart_loc, f"{chart_name}.svg")
                png_path = os.path.join(chart_loc, f"{chart_name}.png")
                
                if os.path.exists(svg_path):
                    svg_to_png(svg_path, png_path)
            except Exception as e:
                print("Failed to generate partial chart:", e)

            #Put the image specific to yogadosha to left
            self.ln(10)
            self.safe_image(f"./images/yogaImages/{yogadosha_key}_chart.png", x=5, w=imageWidth)
            imageEnd_ypos = self.get_y()
            ypos= imageEnd_ypos - imageWidth
            
            #put the yogadosha details right to the image
            #Title
            self.start_section(yogadosha, level=1)
            self.set_xy(3 + imageWidth, ypos)
            self.set_font('Times', 'BU', 16)
            self.set_text_color(220,0,0)
            self.multi_cell(txt=yogadosha, w=self.w - imageWidth - 10, h=8, align='C')

            #Yoga dosha name
            self.set_font('Times', 'B', 14)
            self.set_text_color(0,0,0)
            ypos = self.get_y()
            self.set_xy(5 + imageWidth, ypos)
            xpos = self.get_x()
            ydname = f'{yogadosha_data.get("type", "")} : '
            self.cell(txt=ydname, w=5, h=5, align='L', ln=False)

            xpos = self.get_x() + 12
            self.set_font('Times', 'I', 14)
            self.set_text_color(80,50,200)            
            self.set_xy(xpos, ypos)
            ydname = f'{yogadosha_data.get("name", "")} {yogadosha_data.get("type", "")}'
            self.multi_cell(txt=ydname, w=0, h=5, align='L')
            self.ln(5)

            #Yoga/Dosha Rule
            self.set_font('Times', 'B', 14)
            self.set_text_color(0,0,0)
            ypos = self.get_y()
            self.set_xy(5 + imageWidth, ypos)
            xpos = self.get_x()
            ydrule = f'Rule : '
            self.cell(txt=ydrule, w=0, h=5, align='L', ln=False)

            self.set_font('Times', 'I', 14)
            self.set_text_color(0,0,200)            
            self.set_xy(xpos, ypos)
            ydrule = f'              {yogadosha_data.get("Rule", "")}'
            self.multi_cell(txt=ydrule, w=0, h=5, align='L')
            self.ln(5)

            #Yoga/Dosha Notes
            self.set_font('Times', 'B', 14)
            self.set_text_color(0,0,0)
            ypos = self.get_y()
            self.set_xy(5 + imageWidth, ypos)
            xpos = self.get_x()
            ydnote = f'Note : '
            self.cell(txt=ydnote, w=0, h=5, align='L', ln=False)

            self.set_font('Times', 'I', 14)
            self.set_text_color(155,0,155)            
            self.set_xy(xpos, ypos)
            ydnote = f'              {yogadosha_data.get("Note", "")}'
            self.multi_cell(txt=ydnote, w=0, h=5, align='L')
            self.ln(5)

            #Yoga/Dosha Results
            #get the ypositionn whichever is lower as now results will be below image full pdf wide.
            if(imageEnd_ypos >= self.get_y()):
                ypos = imageEnd_ypos + 5
            else:
                ypos = self.get_y() + 5

            self.set_font('Times', 'B', 14)
            self.set_text_color(0,0,0)
            self.set_xy(5, ypos)
            xpos = self.get_x()
            ydresults = f'Results : '
            self.cell(txt=ydresults, w=0, h=5, align='L', ln=False)

            self.set_font('Times', 'I', 14)
            self.set_text_color(50,0,105)            
            self.set_xy(xpos, ypos)
            ydresults = f'                 {yogadosha_data.get("Result", "")}'
            self.multi_cell(txt=ydresults, w=0, h=5, align='L')
            self.ln(5)

            #Dosha Remedies
            if(yogadosha_data.get("type", "") == "Dosha"):
                ypos = self.get_y()
                self.set_font('Times', 'B', 14)
                self.set_text_color(0,0,0)
                self.set_xy(5, ypos)
                xpos = self.get_x()
                ydremedies = f'Remedies : '
                self.cell(txt=ydremedies, w=0, h=5, align='L', ln=False)

                self.set_font('Times', 'I', 14)
                self.set_text_color(51,102,0)            
                self.set_xy(xpos, ypos)
                ydremedies = f'                    {yogadosha_data.get("Remedies", "")}'
                self.multi_cell(txt=ydremedies, w=0, h=5, align='L')
                self.ln(5)

            #End of Yoga Dosha so draw a line
            self.line(5, self.get_y(), self.w-5, self.get_y())
            
    def addLordInHousesSection(self):
        #title of the page
        imgcrossed = False
        self.set_font('helvetica', 'BU', 14)
        self.set_text_color(0,0,255)
        self.cell(txt="Lord in Houses predictions in Native's Kundali", w=0, h=10, align='C')
        imageWidth = (self.w / 2.5) - 5
        #put Lagna chart 
        self.safe_image("./images/birthcharts/Lagna_chart.png", x=5, y=30, w=imageWidth)
        imgend_x = (self.w / 2.5)
        imgend_y = 30 + imageWidth + 5


        #Get the predections
        predictions = mychart.get("lordinhouses", [])
        xpos = imgend_x
        ypos = 30
        self.set_xy(xpos,ypos)
        
        for prediction in predictions:
            #Heading
            self.set_font('Times', 'BU', 12)
            self.set_text_color(200,15,0)
            self.cell(txt=prediction["LordinHouse"], w=0, h=5, align='L', ln=True)

            #Description
            self.set_font('Times', 'B', 12)
            self.set_text_color(0,0,0)
            if ((self.get_y() < imgend_y) and (imgcrossed == False)):
                self.set_x(imgend_x)
            self.cell(txt="Description : ", w=0, h=5, align='L', ln=False)
            self.set_font('Times', 'I', 12)
            self.set_text_color(155,0,155)
            if ((self.get_y() < imgend_y) and (imgcrossed == False)):
                self.set_x(imgend_x)
            else:
                self.set_x(5)
            self.multi_cell(txt=f'                            {prediction["Description"]}', w=0, h=5, align='L')
            self.ln()

            #Results
            self.set_font('Times', 'B', 12)
            self.set_text_color(0,0,0)
            if ((self.get_y() < imgend_y) and (imgcrossed == False)):
                self.set_x(imgend_x)
            self.cell(txt="Result : ", w=0, h=5, align='L', ln=False)
            self.set_font('Times', 'I', 12)
            self.set_text_color(0,0,230)
            if ((self.get_y() < imgend_y) and (imgcrossed == False)):
                self.set_x(imgend_x)
            else:
                self.set_x(5)            
            self.multi_cell(txt=f'                    {prediction["Prediction"]}', w=0, h=5, align='L')
            self.ln(5)

            if ((self.get_y() < imgend_y) and (imgcrossed == False)):
                self.set_x(imgend_x)
            else:
                imgcrossed = True        

        self.add_page()
    

    def addVimshottariDasha(self):
        #title of the page
        self.set_font('helvetica', 'BU', 16)
        self.set_text_color(0,0,255)
        self.cell(txt="Vimshottari Dasha of native", w=0, h=10, align='C')

        self.ln(10)
        self.set_font('Times', '', 12)
        self.set_text_color(0,0,0)
        self.multi_cell(txt=f'''Current Date [yyyy-mm-dd]: {mychart["Dashas"]["Vimshottari"]["current"]["date"].split(" ")[0]}
Current Mahadasha Lord: {mychart["Dashas"]["Vimshottari"]["current"]["dasha"]}
Current Bhukti Lord: {mychart["Dashas"]["Vimshottari"]["current"]["bhukti"]}
Current Paryantardasha Lord: {mychart["Dashas"]["Vimshottari"]["current"]["paryantardasha"]}
Tabulated data for Mahadashas, Bhuktis under current dasha lord and paryantardashas under current Bhukti are given below''',w=0, h=5, border = True, align='L')
        self.ln(7)

        #MahaDashas Table
        #Text for mahadasha Table
        self.set_font('Times', 'BU', 14)
        self.set_text_color(150,0,0)
        self.cell(txt=f"Vimshottari Dasha: Mahadashas of the native", w=0, h=6, align='C')
        #Mahadasha table part
        ypos = self.get_y()-5
        xpos = 5
        self.set_font('Times', '', 12)
        self.set_text_color(100,0,0)
        mahadasha = mychart["Dashas"]["Vimshottari"]["current"]["dasha"]
        tabdata = [   ("Num","DashaLord","Start Date","End Date","Duration","From Age","Till Age", "yellow")  ]
        for entry in mychart["Dashas"]["Vimshottari"]["mahadashas"]:
            num = str(mychart["Dashas"]["Vimshottari"]["mahadashas"][entry]["dashaNum"])
            lord = mychart["Dashas"]["Vimshottari"]["mahadashas"][entry]["lord"]
            startdate = mychart["Dashas"]["Vimshottari"]["mahadashas"][entry]["startDate"].split(" ")[0]
            enddate = mychart["Dashas"]["Vimshottari"]["mahadashas"][entry]["endDate"].split(" ")[0]
            duration = mychart["Dashas"]["Vimshottari"]["mahadashas"][entry]["duration"].replace(" 0yr","").replace(" 0m","").replace(" 0d","")
            fromage = mychart["Dashas"]["Vimshottari"]["mahadashas"][entry]["startage"].replace(" 0yr","").replace(" 0m","").replace(" 0d","")
            if (fromage.replace(" ","") == ""):
                fromage = " Birth"
            tillage = mychart["Dashas"]["Vimshottari"]["mahadashas"][entry]["endage"].replace(" 0yr","").replace(" 0m","").replace(" 0d","")
            #if the current planet is running mahadasha planet then highlight with lime else keep it white
            if(lord == mahadasha):
                row_bgcolor = "#9BFFFF" #rgb(155,255,255)
            else:
                row_bgcolor = "white"
            tabdata.append((num,lord,startdate,enddate,duration,fromage,tillage,row_bgcolor))        
        self.writeTable(tabdata,xpos,ypos,True)
        self.ln(3)

        #Bhukti Table
        #Text for Bhukti Table
        self.set_font('Times', 'BU', 14)
        self.set_text_color(150,0,200)
        antardasha = mychart["Dashas"]["Vimshottari"]["current"]["bhukti"]
        self.cell(txt=f'''Vimshottari Bhuktis: Bhuktis of the native under Mahadasha of {mahadasha}''', w=0, h=6, align='C')
        #Bhukti table part
        ypos = self.get_y()-5
        xpos = 5
        self.set_font('Times', '', 12)
        self.set_text_color(100,0,155)
        tabdata = [   ("Num","BhuktiLord","Start Date","End Date","Duration","From Age","Till Age", "yellow")  ]
        for entry in mychart["Dashas"]["Vimshottari"]["antardashas"]:
            if (mychart["Dashas"]["Vimshottari"]["antardashas"][entry]["dashaLord"] == mahadasha):
                num = str(mychart["Dashas"]["Vimshottari"]["antardashas"][entry]["bhuktiNum"])
                lord = mychart["Dashas"]["Vimshottari"]["antardashas"][entry]["lord"]
                startdate = mychart["Dashas"]["Vimshottari"]["antardashas"][entry]["startDate"].split(" ")[0]
                enddate = mychart["Dashas"]["Vimshottari"]["antardashas"][entry]["endDate"].split(" ")[0]
                duration = mychart["Dashas"]["Vimshottari"]["antardashas"][entry]["duration"].replace(" 0yr","").replace(" 0m","").replace(" 0d","")
                fromage = mychart["Dashas"]["Vimshottari"]["antardashas"][entry]["startage"].replace(" 0yr","").replace(" 0m","").replace(" 0d","")
                if (fromage.replace(" ","") == ""):
                    fromage = " Birth"
                tillage = mychart["Dashas"]["Vimshottari"]["antardashas"][entry]["endage"].replace(" 0yr","").replace(" 0m","").replace(" 0d","")
                if(lord == antardasha):
                    row_bgcolor = "#9BFF64" #rgb(155,255,100)
                else:
                    row_bgcolor = "white"
                tabdata.append((num,lord,startdate,enddate,duration,fromage,tillage,row_bgcolor))        
        self.writeTable(tabdata,xpos,ypos,True)
        self.ln(3)

        #Paryantaradasha Table
        #Text for Bhukti Table
        self.set_font('Times', 'BU', 13)
        self.set_text_color(0,150,75)
        paryantardasha = mychart["Dashas"]["Vimshottari"]["current"]["paryantardasha"]
        self.cell(txt=f'''Paryantaradashas of the native under Dasha-Bhukti of {mahadasha} - {antardasha}''', w=0, h=6, align='C')
        #Paryantaradasha table part
        ypos = self.get_y()-5
        xpos = 5
        self.set_font('Times', '', 12)
        self.set_text_color(0,100,50)
        tabdata = [   ("Num","pari-Lord","Start Date","End Date","Duration","From Age","Till Age", "yellow")  ]
        for entry in mychart["Dashas"]["Vimshottari"]["paryantardashas"]:
            if ((mychart["Dashas"]["Vimshottari"]["paryantardashas"][entry]["dashaLord"] == mahadasha) and
                (mychart["Dashas"]["Vimshottari"]["paryantardashas"][entry]["bhuktiLord"] == antardasha)):
                num = str(mychart["Dashas"]["Vimshottari"]["paryantardashas"][entry]["pariNum"])
                lord = mychart["Dashas"]["Vimshottari"]["paryantardashas"][entry]["lord"]
                startdate = mychart["Dashas"]["Vimshottari"]["paryantardashas"][entry]["startDate"].split(" ")[0]
                enddate = mychart["Dashas"]["Vimshottari"]["paryantardashas"][entry]["endDate"].split(" ")[0]
                duration = mychart["Dashas"]["Vimshottari"]["paryantardashas"][entry]["duration"].replace(" 0yr","").replace(" 0m","").replace(" 0d","")
                fromage = mychart["Dashas"]["Vimshottari"]["paryantardashas"][entry]["startage"].replace(" 0yr","").replace(" 0m","").replace(" 0d","")
                if (fromage.replace(" ","") == ""):
                    fromage = " Birth"
                tillage = mychart["Dashas"]["Vimshottari"]["paryantardashas"][entry]["endage"].replace(" 0yr","").replace(" 0m","").replace(" 0d","")
                if(lord == paryantardasha):
                    row_bgcolor = "#FF9BCD" #rgb(255,155,205)
                else:
                    row_bgcolor = "white"
                tabdata.append((num,lord,startdate,enddate,duration,fromage,tillage,row_bgcolor))       
        self.writeTable(tabdata,xpos,ypos,True)
        self.ln(3)
        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(1)

        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(1)

            

    def addPlanetaryBalas(self):
        #title of the page
        self.set_font('helvetica', 'BU', 16)
        self.set_text_color(0,0,255)
        self.start_section("Strength (Bala) of Planets", level=0)
        self.cell(txt="Strength (Bala) of Planets", w=0, h=10, align='C')
        #Vimshopaka Bala
        #Title
        self.ln(10)
        self.set_font('Times', 'B', 14)
        self.set_text_color(150,0,0)
        self.cell(txt=f"Vimshopaka Bala for planets:", w=0, h=6, align='L')
        #Vimshopaka Table
        self.ln(7)
        vim_data = mychart.get("Balas", {}).get("Vimshopaka", {})
        planets = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
        
        table_html = """
        <table border="1" align="center" width="100%">
        <thead>
        <tr bgcolor="#d3d3d3">
            <th width="20%" align="center"><b>Planet</b></th>
            <th width="20%" align="center"><b>Shadvarga</b></th>
            <th width="20%" align="center"><b>Saptavarga</b></th>
            <th width="20%" align="center"><b>Dashavarga</b></th>
            <th width="20%" align="center"><b>Shodashavarga</b></th>
        </tr>
        </thead>
        <tbody>
        """
        for p in planets:
            shad = vim_data.get("shadvarga", {}).get(p, "-")
            sapta = vim_data.get("saptavarga", {}).get(p, "-")
            dasha = vim_data.get("dashavarga", {}).get(p, "-")
            shodasha = vim_data.get("shodashavarga", {}).get(p, "-")
            table_html += f"""
            <tr>
                <td align="center"><b>{p}</b></td>
                <td align="center">{shad}</td>
                <td align="center">{sapta}</td>
                <td align="center">{dasha}</td>
                <td align="center">{shodasha}</td>
            </tr>
            """
        table_html += "</tbody></table><br>"
        self.write_html(table_html)
        #vimnshopaka bala text
        self.ln(5)
        self.set_font('Times', 'I', 12)
        self.set_text_color(100,0,0)
        
        vimshopakaDetailshtml = f'''<p>Vimshopaka Bala is computed based on planets placements in various divisional charts
This value is couputed out of 20 and values range from 5 to 20. 
<font color="blue">The points allocated are: <B>(Own House - 20)</B> and <B>(House Of Great Friend - 18)</B> and <B>(House Of Friend - 15)</B> and <B>(Neutral House - 10)</B> and <B>(House Of Enemy - 7)</B> and <B>(House Of Great Enemy - 5)</B>.</font></p>
<p>Shadvarga and its weightage are : (D1 or Rashi Chart - 6), (D2 or Hora - 2), (D3 or Drekanna - 4), (D9 or Navamsa - 5), (D12 or Dwadamsa -2), (D30 or Trimsamsa - 1).</p>
<p>Saptavarga and its weightage are: (D1 or Rashi Chart - 5), (D2 or Hora - 2), (D3 or Drekanna - 3), (D7 or Saptamsa - 1), (D9 or Navamsa - 2.5), (D12 or Dwadamsa - 4.5), (D30 or Trimsamsa - 2).</p>
<p>Dashavarga and its weightage are: (D1 or Rashi Chart - 3), (D2 or Hora - 1.5), (D3 or Drekanna - 1.5), (D7 or Saptamsa - 1.5), (D9 or Navamsa - 1.5), (D10 or Dasamamsa - 1.5), (D12 or Dwadamsa - 1.5), (D16 or Kalamsa - 1.5), (D30 or Trimsamsa - 1.5), (D60 or Shastiamsa - 5).</p>
<p>Shodashavarga and its weightage are: (D1 or Rashi Chart - 3.5), (D2 or Hora - 1), (D3 or Drekanna - 1), (D4 or Turyamsa - 0.5), (D7 or Saptamsa - 0.5), (D9 or Navamsa - 3), (D10 or Dasamamsa - 0.5), (D12 or Dwadamsa - 0.5), (D16 or Kalamsa - 2), (D20 or Vimsamsa - 0.5), (D24 or Chatur Vimsamsa - 0.5), (D27 or Bhamsa - 0.5), (D30 or Trimsamsa - 1), (D40 or Khavedamsa - 0.5), (D45 or Akshavedamsa - 0.5), (D60 or Shastiamsa - 4).</p>
<p>Higher the Vimshopaka score - better the results a planet gives in its Vimshottari and other dasas as the planet is well placed to fructify the results of various facets of life that these divisional charts rule.</p>
'''
        #self.multi_cell(w=0,h=4, txt=vimshopakaDetails, align='L', border=False)
        self.write_html(vimshopakaDetailshtml)
        self.ln(3)
        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(1)        

        #Section for Shadbala
        self.add_page()
        #title of the page
        self.set_font('helvetica', 'BU', 16)
        self.set_text_color(0,0,255)
        self.cell(txt="Strength (Bala) of Planets (contd..)", w=0, h=10, align='C')
        #Title
        self.ln(9)
        self.set_font('Times', 'B', 14)
        self.set_text_color(150,0,0)
        self.cell(txt=f"What is ShadBala for planets(Charts)", w=0, h=6, align='L')
        
        self.ln(7)

        shadbala_text = '''<h4><b>Understanding Shadbala (The Six-Fold Strength)</b></h4>
<p>In Vedic Astrology, a planet's mere placement in a sign or house is not enough to determine its true capacity to deliver results. <b>Shadbala</b> (meaning "Six-fold strength") is a highly precise mathematical model used to quantify the exact power, vitality, and effectiveness of the Grahas (planets). By calculating strength from six distinct sources, we can understand which planets will dominate the chart and confidently manifest their significations.</p>
<p>The six sources of planetary strength are detailed below:</p>
<ul>
    <li><b>1. Sthana Bala (Positional Strength):</b> This is the strength a planet gains based on its exact position in the zodiac. A planet is stronger when placed in its exaltation sign (Uccha), its own sign, friendly signs across various divisional charts (Saptavargaja), specific angles (Kendradi), and proper odd or even signs (Ojayugma). It indicates the foundational stability and "comfort" of the planet.</li>
    <br>
    <li><b>2. Dig Bala (Directional Strength):</b> Planets gain tremendous power when placed in specific directions (houses) in the chart. For example, the Sun and Mars are strongest in the 10th house (South), Jupiter and Mercury in the 1st house (East), Saturn in the 7th house (West), and the Moon and Venus in the 4th house (North). This strength shows the planet's ability to guide the native in the right direction.</li>
    <br>
    <li><b>3. Kaala Bala (Temporal Strength):</b> This represents the strength derived from the specific time of birth. It evaluates whether the birth was during the day or night, the lunar phase (Shukla or Krishna Paksha), and the planetary lords of the birth year, month, day, and hour. It reflects how synchronized a planet is with the cosmic timing of the event.</li>
    <br>
    <li><b>4. Cheshta Bala (Motional Strength):</b> This strength arises from the physical movement and speed of the planets. Planets that are Retrograde (Vakri) or moving slowly appear larger and brighter, thus gaining maximum Cheshta Bala. It represents the inherent drive, effort, and active energy the planet possesses to overcome obstacles.</li>
    <br>
    <li><b>5. Naisargika Bala (Natural Strength):</b> Unlike other strengths that change based on the birth chart, this is the fixed, natural luminosity and power of the planets. The Sun is naturally the most powerful, followed by the Moon, Venus, Jupiter, Mercury, Mars, and finally Saturn. It acts as a constant baseline strength.</li>
    <br>
    <li><b>6. Drik Bala (Aspectual Strength):</b> This is the strength gained or lost through the "gaze" or aspect of other planets. When beneficial (shubha) planets aspect a graha, it gains positive strength. Conversely, when malefic (papa) planets aspect it, its strength is diminished. It shows the support or opposition a planet receives from others.</li>
</ul>
<br>
<p><i>Note: The complete Shadbala table with all calculated sub-balas is provided on the next page. Please consider these strengths carefully when analyzing the planetary periods (Dashas) and chart predictions.</i></p>'''

        self.set_font('Courier', '', 10)
        self.set_text_color(100, 0, 0)
        self.write_html(shadbala_text)

        #Shadbala Table
        self.add_page()
        #title of the page
        self.set_font('helvetica', 'BU', 16)
        self.set_text_color(0,0,255)
        self.cell(txt="Strength (Bala) of Planets (contd..)", w=0, h=10, align='C')
        #Title
        self.ln(9)
        self.set_font('Times', 'B', 14)
        self.set_text_color(150,0,0)
        self.cell(txt=f"ShadBala (in virupas) for planets(Table)", w=0, h=6, align='L')
        self.ln(7)
        self.set_font('Times', 'B', 11)
        self.set_text_color(120,100,0)
        self.write_html(create_ShadbalaTableHtml(),table_line_separators=True)
        self.ln(1)
        self.line(5, self.get_y(), self.w-10, self.get_y())
        
        self.ln(2)
        self.set_font('Times', 'B', 14)
        self.set_text_color(100,100,100)
        self.cell(txt=f"ShadBala (in rupas) for planets and rank:", w=0, h=6, align='L')
        shadbala = mychart["Balas"]["Shadbala"]["Total"].copy()
        ordered_shadbala = sorted(shadbala.items(), key=lambda x:x[1])
        rank = 1
        ranktable_shadbala = f'''<table >
  <tr bgcolor = "black"> <font color="white">
    <th width = "10%" align = "center">Rank</th>
    <th width = "50%" align = "center">Planet</th>
    <th width = "20%" align = "center">Shadbala</th>
    <th width = "20%" align = "center">Min Req</th> </font>
  </tr>'''
        for item in [6,5,4,3,2,1,0]:
            shadbalarupa = round((ordered_shadbala[item][1] / 60),2)
            shadbalaminrupa = round((need["Shadbala"][ordered_shadbala[item][0]] / 60),2)
            if (shadbalarupa >=shadbalaminrupa):
                bgclr = "lime"
            else:
                bgclr = "#F77D85"
            ranktable_shadbala = f'''{ranktable_shadbala} 
            <tr bgcolor = "{bgclr}">
                <td align = "center">{rank}</td>
                <td align = "center">{ordered_shadbala[item][0]}</td>
                <td align = "center">{shadbalarupa}</td> 
                <td align = "center">{shadbalaminrupa}</td>              
            </tr>  '''
            rank = rank + 1

        ranktable_shadbala = f'''{ranktable_shadbala}</table>'''
        self.write_html(ranktable_shadbala,table_line_separators=True)
        self.ln(2)
        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(1)

        self.line(5, self.get_y(), self.w-10, self.get_y())

        #Bhavabala Section
        #Shadbala Table
        self.add_page()
        #title of the page
        self.set_font('helvetica', 'BU', 16)
        self.set_text_color(0,0,255)
        self.cell(txt="Strength (Bala) of Houses", w=0, h=10, align='C')
        #Title
        self.ln(9)
        self.set_font('Times', 'B', 14)
        self.set_text_color(150,0,0)
        self.start_section("Bhavabala", level=1)
        self.cell(txt=f"Bhavabala (in virupas and ranks) for Houses", w=0, h=6, align='C')
        #Image of bhavabala (left half: Bhavabala and right half: bhavabala ranks)
        self.ln(8)
        ypos = self.get_y()
        chart_width = (self.w - 20) / 2
        
        self.safe_image(f"./images/balaImages/Bhavabala_values_chart.png", x=5, w=chart_width)
        imageEnd_ypos = self.get_y()
        
        self.safe_image(f"./images/balaImages/Bhavabala_ranks_chart.png", x=5 + chart_width + 10, y=ypos, w=chart_width)
        self.set_y(max(imageEnd_ypos, self.get_y()))
        self.ln(3)
        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(1)

        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(3)
        #Bhavabala Table
        bhavbalas = mychart["Balas"]["BhavaBala"]["Total"].copy()
        bhavadhipathibalas = mychart["Balas"]["BhavaBala"]["BhavaAdhipathibala"].copy()
        bhavdigbalas = mychart["Balas"]["BhavaBala"]["BhavaDigbala"].copy()
        bhavdrishtibalas = mychart["Balas"]["BhavaBala"]["BhavaDrishtibala"].copy()
        bhavnames = ["Tan", "Dhan", "Anuj", "Maata", "Santaan", "Rog",
             "Dampathya", "Aayu", "Bhagya", "Karma", "Laab", "Karch"]
        rankorderofbhavabalas = rankdata(bhavbalas, method='dense')
        maxrank = max(rankorderofbhavabalas)
        bhavabalarank = [(maxrank+1)-x for x in rankorderofbhavabalas]
        table_bhavabala = f'''<table >
  <tr bgcolor = "black"> <font color="white">
    <th width = "8%" align = "center">Num</th>
    <th width = "22%" align = "center">Bhava</th>
    <th width = "15%" align = "center">Adhipathi</th>
    <th width = "15%" align = "center">Dig</th>
    <th width = "15%" align = "center">Drishti</th>
    <th width = "15%" align = "center">Bhava bala</th>
    <th width = "10%" align = "center">Rank</th> </font>
  </tr>'''
        for item in range(12):
            if (bhavabalarank[item] <= 5):
                bgclr = "lime"
            else:
                bgclr = "#F77D85"
            table_bhavabala = f'''{table_bhavabala} 
            <tr bgcolor = "{bgclr}">
                <td align = "center">{item+1}</td>
                <td align = "center">{bhavnames[item]}</td>
                <td align = "center">{bhavadhipathibalas[item]}</td>
                <td align = "center">{bhavdigbalas[item]}</td>
                <td align = "center">{bhavdrishtibalas[item]}</td>
                <td align = "center">{bhavbalas[item]}</td>
                <td align = "center">{bhavabalarank[item]}</td>             
            </tr>  '''

        table_bhavabala = f'''{table_bhavabala}</table>'''
        self.write_html(table_bhavabala,table_line_separators=True)
        self.ln(2)
        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(1)

        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(1)

        self.line(5, self.get_y(), self.w-10, self.get_y())

        return
        
    def addAshtakjavargaChartsinaPage(self):
        #title of the page
        self.set_font('Times', 'BU', 12)
        self.start_section("Ashtaka Varga", level=0)
        self.cell(txt="Ashtaka Varga Charts", w=0, h=10, align='C')
        
        self.set_font('Times', 'BI', 10)
        imageWidth = (self.w / 3.0) - 5
        self.set_fill_color(255,255,0)  #yellow colour

        #first comes Lagna chart
        self.safe_image("./images/ashtakavargaImages/SAV_chart.png", x=5, y=35, w=imageWidth)
        #setting caption 
        self.set_xy(5,35+imageWidth)    #caption position
        self.cell(txt="Sarva Ashtaka Varga", w=imageWidth, h=3, align='C', ln=1)
        #self.multi_cell(txt="Physical appearance, Health, Entire life",w=imageWidth, h=3, fill=1)

        #next comes Sun chart
        self.safe_image("./images/ashtakavargaImages/BAV_Sun_chart.png", x=5+imageWidth+2, y=35, w=imageWidth)
        #setting caption 
        self.set_xy(5+imageWidth+2,35+imageWidth)    #caption position
        self.cell(txt="Sun Bhinna Ashtaka Varga", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+imageWidth+2)
        #self.multi_cell(txt="Spouse, Marriage, Business, Second half of life",w=imageWidth, h=3, fill=1)

        #next comes Moon chart
        self.safe_image("./images/ashtakavargaImages/BAV_Moon_chart.png", x=5+(2*imageWidth)+4, y=35, w=imageWidth)
        #setting caption 
        self.set_xy(5+(2*imageWidth)+4,35+imageWidth)    #caption position
        self.cell(txt="Moon Bhinna Ashtaka Varga", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(2*imageWidth)+4)
        #self.multi_cell(txt="Matters of great importance, career, honor, awards, fame",w=imageWidth, h=3, fill=1)
    ###############################################################################
        #next comes Mars chart
        self.safe_image("./images/ashtakavargaImages/BAV_Mars_chart.png", x=5, y=35 + imageWidth + 15, w=imageWidth)
        #setting caption 
        self.set_xy(5,35 + (2*imageWidth) + 15)    #caption position
        self.cell(txt="Mars Bhinna Ashtaka Varga", w=imageWidth, h=3, align='C', ln=1)
        #self.multi_cell(txt="Wealth, securities, assets",w=imageWidth, h=3, fill=1)

        #next comes Mercury chart
        self.safe_image("./images/ashtakavargaImages/BAV_Mercury_chart.png", x=5+imageWidth+2, y=35 + imageWidth + 15, w=imageWidth)
        #setting caption 
        self.set_xy(5+imageWidth+2,35 + (2*imageWidth) + 15)    #caption position
        self.cell(txt="Mercury Bhinna Ashtaka Varga", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(1*imageWidth)+4)
        #self.multi_cell(txt="Happiness through siblings",w=imageWidth, h=3, fill=1)

        #next comes Jupiter chart
        self.safe_image("./images/ashtakavargaImages/BAV_Jupiter_chart.png", x=5+(2*imageWidth)+4, y=35 + imageWidth + 15, w=imageWidth)
        #setting caption 
        self.set_xy(5+(2*imageWidth)+4,35 + (2*imageWidth) + 15)    #caption position
        self.cell(txt="Jupiter Bhinna Ashtaka Varga", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(2*imageWidth)+4)
        #self.multi_cell(txt="Fortune, Unmovable Assets",w=imageWidth, h=3, fill=1)

    ###############################################################################
        #next comes Venus chart
        self.safe_image("./images/ashtakavargaImages/BAV_Venus_chart.png", x=5, y=35 + (2*imageWidth) + 30, w=imageWidth)
        #setting caption 
        self.set_xy(5,35 + (3*imageWidth) + 30)    #caption position
        self.cell(txt="Venus Bhinna Ashtaka Varga", w=imageWidth, h=3, align='C', ln=1)
        #self.multi_cell(txt="sons, grandsons, children",w=imageWidth, h=3, fill=1)

        #next comes Saturn chart
        self.safe_image("./images/ashtakavargaImages/BAV_Saturn_chart.png", x=5+imageWidth+2, y=35 + (2*imageWidth) + 30, w=imageWidth)
        #setting caption 
        self.set_xy(5+imageWidth+2,35 + (3*imageWidth) + 30)    #caption position
        self.cell(txt="Saturn Bhinna Ashtaka Varga", w=imageWidth, h=3, align='C', ln=1)
        self.set_x(5+(1*imageWidth)+4)
        #self.multi_cell(txt="Parents",w=imageWidth, h=3, fill=1)

        self.ln(2)
        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(1)

        self.line(5, self.get_y(), self.w-10, self.get_y())
        self.ln(1)

        self.line(5, self.get_y(), self.w-10, self.get_y())

        return



             


import os
from PyQt5.QtSvg import QSvgRenderer
from PyQt5.QtGui import QImage, QPainter
from PyQt5.QtCore import QSize, Qt

def svg_to_png(svg_path, png_path, size=500):
    if not os.path.exists(svg_path):
        return
    renderer = QSvgRenderer(svg_path)
    image = QImage(QSize(size, size), QImage.Format_ARGB32)
    image.fill(Qt.white)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    image.save(png_path)

def generate_chart_pngs(charts, config):
    import support.astrochart as chart_module
    import os
    chart_names = {
        "D1": "Lagna_chart", "D9": "Navamsa_chart", "D10": "Dasamsa_chart", "D2": "Hora_chart", 
        "D3": "Drekkana_chart", "D4": "Chaturtamsa_chart", "D7": "Saptamsa_chart", 
        "D12": "Dwadasamsa_chart", "D16": "Shodasamsa_chart", "D20": "Vimsamsa_chart", 
        "D24": "Chaturvimsamsa_chart", "D27": "Saptavimsamsa_chart", "D30": "Trimsamsa_chart", 
        "D40": "Khavedamsa_chart", "D45": "Akshavedamsa_chart", "D60": "Shashtiamsa_chart"
    }
    
    language = config.get("language", "English")
    chartStyle = config.get("chartStyle", "North Indian")
    
    style_val = "south" if chartStyle == "South Indian" else "north"
    lang_val = {"English": "english", "Kannada": "kannada", "Hindi": "hindi"}.get(language, "english")

    for div, c in chart_names.items():
        chart_module.plot_astrochart("./images/birthcharts/", c, charts, div, language=lang_val, chart_style=style_val)
        svg_path = f"./images/birthcharts/{c}.svg"
        png_path = f"./images/birthcharts/{c}.png"
        if os.path.exists(svg_path):
            svg_to_png(svg_path, png_path)

    import support.graphplot as gp
    import copy
    
    # 1. Vimshopaka
    vimshopaka_data = charts.get("Balas", {}).get("Vimshopaka", {})
    # if vimshopaka_data:
    #     gp.barPlot(vimshopaka_data, "VimshopakaBala", "Vimshopaka Bala of planets in various Varga-groups", "Planets", "Vimshopaka Bala")
        
    # 2. Shadbala (virupas and rupas)
    shadbala_data = charts.get("Balas", {}).get("Shadbala", {})
    if shadbala_data:
        if "Total" in shadbala_data:
            gp.barPlot(shadbala_data["Total"], "Shadbala", "ShadBala for planets", "Planets", "Shad Bala(virupas)", index=0)
            
        if "Rupas" in shadbala_data:
            gp.barPlot(shadbala_data["Rupas"], "Shadbala_Rupas", "Shadbala of planets", "Planets", "Shad Bala(rupas)", index=0)
        
        # Sthanabala
        sthana = shadbala_data.get("Sthanabala", {})
        if sthana:
            # Sthanabala dictionary has 'Total' + sub-balas, all with planet values.
            # Passing it as index=999 (default) draws a grouped bar chart.
            gp.barPlot(sthana, "Sthanabala", "Shadbala --> Sthanabala of planets", "Planets", "Sthana Bala(virupas)")
            
        # Kaalabala
        kaala = shadbala_data.get("Kaalabala", {})
        if kaala:
            gp.barPlot(kaala, "Kaalabala", "Shadbala --> Kaalabala of planets", "Planets", "Kaala Bala(virupas)")

    # 3. BhavaBala
    bhavabala_data = charts.get("Balas", {}).get("BhavaBala", {}).get("Total", [])
    if bhavabala_data:
        # Calculate Ranks
        rankorderofbhavabalas = rankdata(bhavabala_data, method='dense')
        maxrank = max(rankorderofbhavabalas)
        bhavabalarank = [(maxrank+1)-x for x in rankorderofbhavabalas]
        
        # Prepare dicts for numerical chart (1 to 12)
        values_dict = {i+1: int(round(float(v))) for i, v in enumerate(bhavabala_data)}
        ranks_dict = {i+1: int(v) for i, v in enumerate(bhavabalarank)}

        chart_loc = "./images/balaImages"
        os.makedirs(chart_loc, exist_ok=True)
        c_style = config.get("chartStyle", "north")

        # Generate Values Chart
        ac.plot_numerical_astrochart(chart_loc, "Bhavabala_values_chart", charts, values_dict, 
                                     div="D1", language="english", chart_style=c_style, default_color="lime")
        if os.path.exists(os.path.join(chart_loc, "Bhavabala_values_chart.svg")):
            svg_to_png(os.path.join(chart_loc, "Bhavabala_values_chart.svg"), os.path.join(chart_loc, "Bhavabala_values_chart.png"))

        # Generate Ranks Chart
        ac.plot_numerical_astrochart(chart_loc, "Bhavabala_ranks_chart", charts, ranks_dict, 
                                     div="D1", language="english", chart_style=c_style, default_color="sky blue")
        if os.path.exists(os.path.join(chart_loc, "Bhavabala_ranks_chart.svg")):
            svg_to_png(os.path.join(chart_loc, "Bhavabala_ranks_chart.svg"), os.path.join(chart_loc, "Bhavabala_ranks_chart.png"))
    # 4. Ashtakavarga Charts
    av_data = charts.get("AshtakaVarga", {})
    if av_data:
        av_loc = "./images/ashtakavargaImages"
        os.makedirs(av_loc, exist_ok=True)
        c_style = config.get("chartStyle", "north")

        # Generate SAV chart
        sav_vals = av_data.get("Total", [])
        if sav_vals:
            sav_dict = {i+1: str(val) for i, val in enumerate(sav_vals)}
            ac.plot_numerical_astrochart(av_loc, "SAV_chart", charts, sav_dict,
                                         div="D1", language="english", chart_style=c_style, default_color="lime")
            if os.path.exists(os.path.join(av_loc, "SAV_chart.svg")):
                svg_to_png(os.path.join(av_loc, "SAV_chart.svg"), os.path.join(av_loc, "SAV_chart.png"))

        # Generate BAV charts
        for p in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"]:
            p_vals = av_data.get(p, [])
            if p_vals:
                p_dict = {i+1: str(val) for i, val in enumerate(p_vals)}
                ac.plot_numerical_astrochart(av_loc, f"BAV_{p}_chart", charts, p_dict,
                                             div="D1", language="english", chart_style=c_style, default_color="lime")
                if os.path.exists(os.path.join(av_loc, f"BAV_{p}_chart.svg")):
                    svg_to_png(os.path.join(av_loc, f"BAV_{p}_chart.svg"), os.path.join(av_loc, f"BAV_{p}_chart.png"))



def GeneratePDFReport(charts, target_path, config):
    generate_chart_pngs(charts, config)
    
    import support.yogadoshas as yd
    import support.astrochart as ac
    import support.lordinhouses as lh
    
    global mychart
    global reportLevel
    mychart = charts.copy()
    
    # Compute YogaDoshas and Lord in Houses dynamically for fresh data
    mychart["yogadoshas"] = yd.ComputeYogaDoshas(mychart)
    mychart["lordinhouses"] = lh.populate_lordinhouses(mychart)

    pdf = PDF()
    pdf.alias_nb_pages()
    pdf.loadAllCustomFonts()
    pdf.add_page()
    pdf.set_font('Times', '', 12)    
    #Set Title page
    pdf.createTitlePage()

    pdf.add_page()
    pdf.insert_toc_placeholder(pdf.render_toc)
    
    pdf.addFirstPageBasic()

    if config.get("divisionalCharts", True):
        pdf.add_page()
        pdf.addVargaChartsinaPage()

    if config.get("vimshottariDasha", True):
        pdf.add_page()
        pdf.addVimshottariDasha()

    if config.get("shadbala", True) or config.get("vimshopakaBala", True) or config.get("bhavaBala", True):
        pdf.add_page()
        pdf.addPlanetaryBalas()

    if config.get("ashtakaVarga", True):
        pdf.add_page()
        pdf.addAshtakjavargaChartsinaPage()

    if config.get("yogasDoshas", True):
        pdf.add_page()
        pdf.addYogaDoshasSection(config)

    if config.get("lordInHouses", True):
        pdf.add_page()
        pdf.addLordInHousesSection()

    pdf.output(target_path, 'F')


if __name__ == '__main__':
    image_path = './images/birthcharts/Lagna_chart.svg'
    GeneratePDFReport(mychart)
    #add_image(image_path)
    
