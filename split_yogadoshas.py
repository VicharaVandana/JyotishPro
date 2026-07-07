import os

old_file = r"d:\Project\United_Jyotishya_App_pythonQT\JyotishPro\support\yogadoshas_old.py"
new_dir = r"d:\Project\United_Jyotishya_App_pythonQT\JyotishPro\support\yogadoshas"

with open(old_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

def extract_lines(start_idx, end_idx):
    # start_idx and end_idx are 1-based inclusive, so subtract 1
    content = "".join(lines[start_idx-1:end_idx])
    return content.replace("global yogadoshas_dict", "") \
                  .replace("yogadoshas_dict", "common.yogadoshas_dict") \
                  .replace("iterativeReplace", "common.iterativeReplace") \
                  .replace("global parivarthanaYogas", "") \
                  .replace("global IsParivarthanaYogaPresent", "global IsParivarthanaYogaPresent") \
                  .replace("global AshrayaYogas", "") \
                  .replace("global IsAshrayaYogaPresent", "global IsAshrayaYogaPresent") \
                  .replace("global DalaYogas", "") \
                  .replace("global IsDalaYogaPresent", "global IsDalaYogaPresent") \
                  .replace("global AakritiYogas", "") \
                  .replace("global IsAakritiYogaPresent", "global IsAakritiYogaPresent") \
                  .replace("global SankhyaYogas", "") \
                  .replace("global IsSankhyaYogaPresent", "global IsSankhyaYogaPresent") \
                  .replace("parivarthanaYogas", "common.parivarthanaYogas") \
                  .replace("AshrayaYogas", "common.AshrayaYogas") \
                  .replace("DalaYogas", "common.DalaYogas") \
                  .replace("AakritiYogas", "common.AakritiYogas") \
                  .replace("SankhyaYogas", "common.SankhyaYogas")

common_code = """import support.generic as gen

yogadoshas_dict = {}
parivarthanaYogas = []
AshrayaYogas = []
DalaYogas = []
AakritiYogas = []
SankhyaYogas = []

def iterativeReplace(s, old, new):
    while old in s:
        s = s.replace(old, new)
    return s

def reset_globals():
    global yogadoshas_dict, parivarthanaYogas, AshrayaYogas, DalaYogas, AakritiYogas, SankhyaYogas
    yogadoshas_dict = {}
    parivarthanaYogas = []
    AshrayaYogas = []
    DalaYogas = []
    AakritiYogas = []
    SankhyaYogas = []
"""

pancha_code = "import support.generic as gen\nimport support.yogadoshas.common as common\n\n" + extract_lines(26, 667)
vipareeta_code = "import support.generic as gen\nimport support.yogadoshas.common as common\n\n" + extract_lines(668, 1076)
kaala_code = "import support.generic as gen\nimport support.yogadoshas.common as common\n\n" + extract_lines(1077, 1854)
other_code = "import support.generic as gen\nimport support.yogadoshas.common as common\n\n" + extract_lines(1855, 2136)
nabhasa_code = "import support.generic as gen\nimport support.yogadoshas.common as common\n\n" + extract_lines(2137, 3019)
amala_code = "import support.generic as gen\nimport support.yogadoshas.common as common\n\n" + extract_lines(3020, 3139)

with open(os.path.join(new_dir, "common.py"), "w", encoding="utf-8") as f: f.write(common_code)
with open(os.path.join(new_dir, "panchamahapurusha.py"), "w", encoding="utf-8") as f: f.write(pancha_code)
with open(os.path.join(new_dir, "vipareeta_raja.py"), "w", encoding="utf-8") as f: f.write(vipareeta_code)
with open(os.path.join(new_dir, "kaala_sarpa.py"), "w", encoding="utf-8") as f: f.write(kaala_code)
with open(os.path.join(new_dir, "other_yogas.py"), "w", encoding="utf-8") as f: f.write(other_code)
with open(os.path.join(new_dir, "nabhasa_yogas.py"), "w", encoding="utf-8") as f: f.write(nabhasa_code)
with open(os.path.join(new_dir, "amala_yoga.py"), "w", encoding="utf-8") as f: f.write(amala_code)

# Create placeholders
with open(os.path.join(new_dir, "raja_yogas.py"), "w", encoding="utf-8") as f: f.write("# Placeholder for future Raja Yogas\nimport support.generic as gen\nimport support.yogadoshas.common as common\n")
with open(os.path.join(new_dir, "dhana_yogas.py"), "w", encoding="utf-8") as f: f.write("# Placeholder for future Dhana Yogas\nimport support.generic as gen\nimport support.yogadoshas.common as common\n")

print("Files generated!")
