embed
{{err("Please Use <#770071091615629323>", pm_user=False) if ctx.channel.id != 770071091615629323 else None}}

-title "Relentless Adventure"
t,z = "Quest Downtime","Weekly Downtime"
{{c=character().get_cc("Weekly Downtime")}}
{{d=character().get_cc("Quest Downtime")}}
{{err("You do not have any downtime. Use `!questend`", pm_user=False) if c==0 and d==0 else None}}

{{character().set_cc("Weekly Downtime",0)}}
{{character().set_cc("Quest Downtime",0)}}
{{a=character().get_cc("Weekly Downtime")}}
{{e=character().get_cc("Quest Downtime")}}
{{b=vroll("2d100kh1")}} 
{{s=vroll("1d100")}}
{{q=vroll("1d100")}}

<drac2>
C,L = character(),character().levels.total_level
yy = 0
if character().cc_exists("Prestige"):
    if L < 4:
        yy = 0
    elif L < 9:
        yy = 1
    elif L < 14:
        yy = 2
    elif L < 19:
        yy = 3
    elif L < 24:
        yy = 4
    elif L < 30:
        yy = 5
</drac2>
{{bb=b.total+yy}}
{{ss=s.total+yy}}
{{ee=q.total+yy}}

<drac2>
# Calculate Quest Downtime adjustment
f = 1 if L < 13 else 2
character().set_cc("Quest Downtime", f)

# Main roll results collection
results = []
main_tables = [
    (bb, "bf19d252-644b-4fd6-80fc-f088cd5d5f21"),
    (ss, "a7322e72-91ab-45ab-b48b-9cf03e870b1c"),
    (ee, "3f2c36be-58e2-4996-a1ad-6a5bebdc2a84"),
]

for roll_value, gvar_id in main_tables:
    try:
        table = load_json(get_gvar(gvar_id))
        highest = max([int(k) for k in table.keys()])
        diceroll = vroll(f"1d{highest}")
        result = [table[key] for key in table if diceroll.total <= int(key)]
        if result:
            results.append((diceroll, result[0]))
    except Exception:
        pass  # Skip this roll if the table fails

# Guaranteed items rolls based on level
guaranteed_results = []
if L < 5:
    guaranteed_tables = ["2d97cbb6-0bd4-4642-be96-e700fa5cb867"]
elif L < 9:
    guaranteed_tables = ["a7322e72-91ab-45ab-b48b-9cf03e870b1c"]
elif L < 13:
    guaranteed_tables = ["3f2c36be-58e2-4996-a1ad-6a5bebdc2a84"]
elif L < 17:
    guaranteed_tables = [
        "bf19d252-644b-4fd6-80fc-f088cd5d5f21",
        "3f2c36be-58e2-4996-a1ad-6a5bebdc2a84",
    ]
elif L < 21:
    guaranteed_tables = [
        "bf19d252-644b-4fd6-80fc-f088cd5d5f21",
        "370ea648-2264-41fd-abff-5c5f8dac5ff5",
    ]
elif L < 26:
    guaranteed_tables = [
        "bf19d252-644b-4fd6-80fc-f088cd5d5f21",
        "370ea648-2264-41fd-abff-5c5f8dac5ff5",
    ]

for gvar_id in guaranteed_tables:
    try:
        table = load_json(get_gvar(gvar_id))
        highest = max([int(k) for k in table.keys()])
        diceroll = vroll(f"1d{highest}")
        result = [table[key] for key in table if diceroll.total <= int(key)]
        if result:
            guaranteed_results.append((diceroll, result[0]))
    except Exception:
        pass  # Skip this roll if the table fails

# Format roll results
roll_results_text = "\n".join(
    [f"**Result:** {roll.dice} ({roll.total}) = {item}" for roll, item in results]
)

# Format guaranteed item results
guaranteed_results_text = (
    f"**Guaranteed Items:** {', '.join([item for _, item in guaranteed_results])}"
    if guaranteed_results
    else "**Guaranteed Items:** None"
)

output = (
    f"**Rolls:** {b.dice}, {s.dice}, {q.dice} -> {bb}, {ss}, {ee}\n\n"
    f"{roll_results_text}\n\n"
    f"{guaranteed_results_text}"
)
</drac2>

{{zz = f+1}}
{{character().mod_cc("Quest Downtime", +1) if character().cc_exists("War Room") else ''}}
-desc "{{name}} adventures relentlessly!
**Prestige Level {{L if character().cc_exists('Prestige') else '0'}}: +{{yy}} to Loot Roll**
**Rolls:** {{b.dice}}, {{s.dice}}, {{q.dice}} -> {{bb}}, {{ss}}, {{ee}}
{{output}}

Weekly Downtime: **{{c}}** -> **{{a}}**
Quest Downtime: **{{d}}** -> **{{e}}**
New Quest Downtime: **{{zz+' (War Room)' if character().cc_exists('War Room') else f}}**"

-thumb <image>
-footer "For quests above 6 hours. Rolling for loot reduces all your available downtime to 0"
