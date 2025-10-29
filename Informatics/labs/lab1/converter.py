from decimal import Decimal, getcontext, ROUND_FLOOR

def char_to_value(char):
    digs = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    try:
        return digs.index(char)
    except ValueError:
        raise ValueError(f"Недопустимый символ '{char}' в числе")


def _value_to_char(value):
    digs = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if 0 <= value < len(digs):
        return digs[value]
    raise ValueError(f"Невозможно преобразовать значение {value} в символ")


def convert_from_base_to_decimal(num_str, base):
    if base < 2 or base > 36:
        raise ValueError("Основание системы счисления должно быть от 2 до 36")

    num_str = num_str.strip().upper()
    if not num_str:
        raise ValueError("Число не может быть пустым")

    neg = num_str.startswith('-')
    if neg:
        num_str = num_str[1:]

    if num_str.count('.') > 1:
        raise ValueError("Некорректный формат числа: более одной точки")

    int_part_str, frac_part_str = (num_str.split('.') + [''])[:2]

    int_value = Decimal(0)
    for char in int_part_str:
        if not char:
            continue
        value = char_to_value(char)
        if value >= base:
            raise ValueError(
                f"Символ '{char}' некорректен для системы с основанием {base}"
            )
        int_value = int_value * base + value

    frac_value = Decimal(0)
    power = Decimal(base)
    denominator = power
    for char in frac_part_str:
        value = char_to_value(char)
        if value >= base:
            raise ValueError(
                f"Символ '{char}' некорректен для системы с основанием {base}"
            )
        frac_value += Decimal(value) / denominator
        denominator *= power

    result = int_value + frac_value
    if neg:
        result = -result
    return result

def convert_decimal_to_base(decimal_num, base, precision=15):
    if base < 2 or base > 36:
        raise ValueError("Основание системы счисления должно быть от 2 до 36")

    if isinstance(decimal_num, (int, float)):
        decimal_num = Decimal(str(decimal_num))

    if decimal_num == 0:
        return "0"

    neg = decimal_num < 0
    if neg:
        decimal_num = -decimal_num

    int_part = int(decimal_num.to_integral_value(rounding=ROUND_FLOOR))
    frac_part = decimal_num - Decimal(int_part)

    if int_part == 0:
        integer_str = "0"
    else:
        integer_digs = []
        temp = int_part
        while temp > 0:
            remainder = temp % base
            integer_digs.append(_value_to_char(int(remainder)))
            temp //= base
        integer_str = ''.join(reversed(integer_digs))

    if frac_part == 0:
        frac_str = ""
    else:
        frac_digs = []
        current = frac_part
        for _ in range(max(0, precision)):
            current *= base
            digit = int(current.to_integral_value(rounding=ROUND_FLOOR))
            frac_digs.append(_value_to_char(digit))
            current -= digit
            if current == 0:
                break
        while frac_digs and frac_digs[-1] == '0':
            frac_digs.pop()
        frac_str = ''.join(frac_digs)

    result = integer_str if not frac_str else f"{integer_str}.{frac_str}"
    if neg and result != "0":
        result = "-" + result
    return result

def get_base_name(base):
    base_names = {
        2: "двоичная",
        8: "восьмеричная", 
        10: "десятичная",
        16: "шестнадцатеричная"
    }
    return base_names.get(base, f"система счисления с основанием {base}")

def validate_number_for_base(num_str, base):
    allowed_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"[:base]

    check_number = num_str.strip().upper()
    if not check_number:
        return False

    if check_number[0] == '-':
        check_number = check_number[1:]
    if not check_number:
        return False

    if check_number.count('.') > 1:
        return False

    int_part, frac_part = (check_number.split('.') + [''])[:2]

    def _all_allowed(part):
        for char in part:
            if char not in allowed_chars:
                return False
        return True

    return _all_allowed(int_part) and _all_allowed(frac_part)

def main():
    print("=== КОНВЕРТЕР СИСТЕМ СЧИСЛЕНИЯ ===")
    print("Поддерживаемые системы: от 2 до 36")
    print("Для систем > 10 используются буквы A-Z")
    print("-" * 40)
    
    try:
        number_a = input("Введите число A: ").strip().upper()
        if not number_a:
            print("Ошибка: число не может быть пустым!")
            return
        
        base_b = input("Введите основание системы счисления числа A (например, 2, 8, 10, 16): ").strip()
        try:
            base_b = int(base_b)
        except ValueError:
            print("Ошибка: основание должно быть целым числом!")
            return
            
        if base_b < 2 or base_b > 36:
            print("Ошибка: основание должно быть от 2 до 36!")
            return
        
        if not validate_number_for_base(number_a, base_b):
            print(f"Ошибка: число '{number_a}' некорректно для {get_base_name(base_b)} системы!")
            return
        
        base_c = input("Введите основание целевой системы счисления (например, 2, 8, 10, 16): ").strip()
        try:
            base_c = int(base_c)
        except ValueError:
            print("Ошибка: основание должно быть целым числом!")
            return
            
        if base_c < 2 or base_c > 36:
            print("Ошибка: основание должно быть от 2 до 36!")
            return
        
        print("\nТип числа для вывода (влияет на точность дробной части):")
        print("1) int (без дробной части)")
        print("2) float (~7 знаков точности)")
        print("3) double (~15 знаков точности)")
        type_choice = input("Выберите тип (1/2/3): ").strip()
        if type_choice not in {"1", "2", "3"}:
            print("Ошибка: необходимо выбрать 1, 2 или 3")
            return
        
        if type_choice == "1" and '.' in number_a:
            print("Предупреждение: выбран тип int, дробная часть будет отброшена.")
        
        precision = 0 if type_choice == "1" else (7 if type_choice == "2" else 15)
        getcontext().prec = max(precision + 5, 20)
        
        print("\n" + "="*50)
        print("РЕЗУЛЬТАТ КОНВЕРТАЦИИ:")
        print("="*50)
        
        decimal_value = convert_from_base_to_decimal(number_a, base_b)
        print(f"Исходное число: {number_a} ({get_base_name(base_b)})")
        if precision == 0:
            dec_out = str(int(decimal_value.to_integral_value(rounding=ROUND_FLOOR)))
        else:
            decimal_str = f"{decimal_value.normalize()}"
            if 'E' in decimal_str or 'e' in decimal_str:
                dec_out = f"{+decimal_value:.{precision}g}"
            else:
                if '.' in decimal_str:
                    int_part, frac_part = decimal_str.split('.')
                    dec_out = int_part + ('.' + frac_part[:precision]).rstrip('.')
                else:
                    dec_out = decimal_str
        print(f"В десятичной системе: {dec_out}")
        
        if base_c == 10:
            result = dec_out
        else:
            result = convert_decimal_to_base(decimal_value, base_c, precision)
        
        print(f"В {get_base_name(base_c)} системе: {result}")
        
        if base_c != base_b and decimal_value != 0:
            print("\nДополнительные представления:")
            if base_c != 2:
                binary = convert_decimal_to_base(decimal_value, 2, precision if precision > 0 else 0)
                print(f"Двоичная (2): {binary}")
            if base_c != 8:
                octal = convert_decimal_to_base(decimal_value, 8, precision if precision > 0 else 0) 
                print(f"Восьмеричная (8): {octal}")
            if base_c != 16:
                hexadecimal = convert_decimal_to_base(decimal_value, 16, precision if precision > 0 else 0)
                print(f"Шестнадцатеричная (16): {hexadecimal}")
        
    except ValueError as e:
        print(f"Ошибка: {e}")
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем.")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

def interactive_mode():
    while True:
        main()
        print("\n" + "-"*50)
        choice = input("Выполнить еще одну конвертацию? (y/n): ").strip().lower()
        if choice not in ['y', 'yes', 'д', 'да']:
            break
        print("\n")

if __name__ == "__main__":
    try:
        interactive_mode()
        print("Спасибо за использование конвертера!")
    except KeyboardInterrupt:
        print("\n\nДо свидания!")
