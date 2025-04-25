from random import randint
import re

# Mapeamento de emojis personalizados usando os IDs fornecidos
DICE_SYSTEM_EMOJIS = {
    1: "*Nada*",
    2: "*Nada*",
    3: "<:Pressao:1357013346968141921>",
    4: "<:Pressao:1357013346968141921> <:Adaptacao:1357013371882438737>",
    5: "<:Pressao:1357013346968141921> <:Adaptacao:1357013371882438737>",
    6: "<:Sucesso:1357013314109964350>",
    7: "<:Sucesso:1357013314109964350> <:Sucesso:1357013314109964350>",
    8: "<:Sucesso:1357013314109964350> <:Adaptacao:1357013371882438737>",
    9: "<:Sucesso:1357013314109964350> <:Adaptacao:1357013371882438737> <:Pressao:1357013346968141921>",
    10: "<:Sucesso:1357013314109964350> <:Sucesso:1357013314109964350> <:Pressao:1357013346968141921>",
    11: "<:Sucesso:1357013314109964350> <:Adaptacao:1357013371882438737> <:Adaptacao:1357013371882438737> <:Pressao:1357013346968141921>",
    12: "<:Pressao:1357013346968141921> <:Pressao:1357013346968141921>"
}

def roll_dice(num_dice: int, num_sides: int) -> list:
    return [randint(1, num_sides) for _ in range(num_dice)]

def process_roll(expression: str, system_mode: bool) -> list | None:
    match = re.match(r'(\d*)d(\d+)([+\-*/]\d+)?', expression)

    num_dice, num_sides, operation = match.groups()
    num_dice = int(num_dice) if num_dice else 1
    num_sides = int(num_sides)

    rolls = roll_dice(num_dice, num_sides)
    roll_total = sum(rolls)
    final_result = roll_total
    operation_str = ""

    if operation:
        operator = operation[0]
        value = int(operation[1:])

        if operator == "+":
            final_result += value
        elif operator == "-":
            final_result -= value
        elif operator == "*":
            final_result *= value
        elif operator == "/":
            final_result = int(final_result / value)

        operation_str = f"🧮 Total inicial: {roll_total} {operator} {value} = {final_result}"

    if system_mode and num_sides in {6, 10, 12}:
        emoji_result = DICE_SYSTEM_EMOJIS.get(final_result, "*Nada*")
        result_str = f"🎲 Resultado = {final_result} → {emoji_result}"
    else:
        result_str = f"🎲 Resultado = {final_result}"

    return [operation_str, result_str] if operation else [result_str]

def get_response(user_input: str) -> str | None:
    lines = user_input.strip().split("\n")
    responses = []

    for line in lines:
        lowered = line.lower().strip()
        if not lowered:
            continue

        system_mode = lowered.startswith('!')
        if system_mode:
            lowered = lowered[1:]

        multiple_match = re.match(r'(\d+)#(.+)', lowered)
        if multiple_match:
            num_repeats, expression = multiple_match.groups()
            num_repeats = int(num_repeats)
            roll_block = []
            for _ in range(num_repeats):
                result = process_roll(expression, system_mode)
                if result:
                    roll_block.extend(result)
            if roll_block:
                responses.append("\n".join(roll_block))
        else:
            result = process_roll(lowered, system_mode)
            if result:
                responses.append("\n".join(result))

    return "\n\n".join(responses) if responses else None
