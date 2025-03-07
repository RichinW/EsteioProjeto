import re

def process_message(message, activity):
    date = re.search(r"Data:\s*(\d{2}/\d{2}/\d{4})", message)
    audit = re.search(r"Auditoria:\s*(\d+)", message)
    team = re.search(r"Equipe:\s*(.+)", message)
    regional = re.search(r"Regional:\s*(.+)", message)
    obs = re.search(r"\(Obs:\s*(.*?)\)", message)
    total_data = []

    activity_pattern = re.findall(
        r"Tipo:\s*(.+?)\s*(Rodovias\s*inspecionadas:.*?)(?=(Tipo:|$))",
        message,
        re.DOTALL
    )

    if not activity_pattern:
        print("⚠️ Nenhuma atividade encontrada! Verifique a formatação da mensagem.")
        return []

    for activity_info in activity_pattern:
        type_activity = activity_info[0].strip()
        highway_info = activity_info[1]

        highway_pattern = re.findall(
            r"(SP_[A-Z]*\d{3}(?:/\d{3})?)\s*do\s*Km\s*(\d{3}\+\d{3})\s*ao\s*Km\s*(\d{3}\+\d{3})\s*"
            r"Total de elementos:\s*(\d+)\s*"
            r"Situação:\s*([^\n\r]+)",
            highway_info,
            re.MULTILINE
        )

        if not highway_pattern:
            print(f"⚠️ Nenhuma rodovia encontrada para o tipo de atividade '{type_activity}'!")
            continue

        for highway in highway_pattern:
            total_data.append({
                'date': date.group(1) if date else '',
                'activity': activity,
                'audit': int(audit.group(1)) if audit else 0,
                'type': type_activity,
                'team': team.group(1).strip() if team else '',
                'regional': regional.group(1).strip() if regional else '',
                'highway': highway[0],
                'km_start': highway[1],
                'km_end': highway[2],
                'total_elements': int(highway[3]),
                'state_highway': highway[4].strip(),
                'observation': obs.group(1).strip() if obs else ''

            })

    return total_data
