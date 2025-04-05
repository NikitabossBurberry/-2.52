import telebot
from bot_logic import detect_trash

bot = telebot.TeleBot("7428097385:AAH17N0Vuij__A_aFm9HeugQ3o87aH8kHHA")

@bot.message_handler(commands=['start'])
def send_1(message):
    bot.reply_to(message, "Я бот-помощник, который может подсказать как помочь природе и не вредить ей, что-бы не было таких проблем как ГЛОБАЛЬНОЕ ПОТЕПЛЕНИЕ! ")
    bot.reply_to(message, "Доступные команды: /start - Начать общение с ботом,Показать это сообщение, ")
    bot.reply_to(message, "/Rinfo - новости, ")
    bot.reply_to(message, "/calculate - Калькулятор (обычный, Чтобы тебе не выдавало ошибку надо писать например вот так - /calculate 2 + 2), ")
    bot.reply_to(message, "/fuel - Узнать сколько топлива на 100 км израсходовал за всю поездку (/fuel [расстояние] [расход] - вот так надо писать только без скобочек.)")
    bot.reply_to(message, "/engine_fuel - Узнать сколько машина тратит топлива на 100 км по её характеристикам (/engine_fuel [объем] [мощность] [вес] - вот так надо писать только без скобочек, например - /engine_fuel 5.0 500 2800.) ")
    bot.reply_to(message, "/WHAT - О глобальном потеплении")
    bot.reply_to(message, "/EASY - О решении проблемы с глобальным потеплением")
    bot.reply_to(message, "/Zakl - Заключение о Глобальном потеплении")
    bot.reply_to(message, "/Energy - Расчитает сколько энергии потратит тот или иной прибор (/energy [мощность] [часы] - вот так надо писать только без скобочек, например - /energy 60 4.)")

@bot.message_handler(commands=['Rinfo'])
def website_command(message):
    markup = telebot.types.InlineKeyboardMarkup()
    button = telebot.types.InlineKeyboardButton(text='Перейти на сайт', url='https://www.vesti.ru/')
    markup.add(button)
    bot.send_message(message.chat.id, "Нажмите кнопку, чтобы перейти на сайтRinfo:", reply_markup=markup)

@bot.message_handler(commands=['calculate'])
def calculate_command(message):
    try:

        expression = message.text.replace('/calculate ', '')

        # Безопасное вычисление (с ограничениями на операции)
        result = safe_eval(expression)

        bot.reply_to(message, f"Результат: {result}")

    except Exception as e:
        bot.reply_to(message, f"Ошибка: {e}")


def safe_eval(expression):
    import ast
    import operator

    operators = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
                 ast.Div: operator.truediv, ast.Pow: operator.pow, ast.USub: operator.neg}

    def eval_(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            try:
                return operators[type(node.op)](eval_(node.left), eval_(node.right))
            except KeyError:  # Если оператор не разрешен
                raise ValueError("Разрешены только +, -, *, / и **")
        elif isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](eval_(node.operand))
        else:
            raise ValueError("Недопустимое выражение")

    try:
        tree = ast.parse(expression, mode='eval')
        return eval_(tree.body)
    except (SyntaxError, ValueError) as e:
        raise ValueError(f"Недопустимое выражение: {e}")
    
@bot.message_handler(commands=['fuel'])
def fuel_consumption_command(message):
    try:
        # Извлекаем аргументы из сообщения, разделяя по пробелам
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "Неверный формат команды. Используйте: /fuel расстояние расход (например, /fuel 200 15)")
            return

        try:
            distance = float(parts[1])  # Пройденное расстояние (км)
            fuel_used = float(parts[2])   # Израсходованное топливо (литры)
        except ValueError:
            bot.reply_to(message, "Расстояние и расход должны быть числами.")
            return

        # Проверяем, что значения положительные
        if distance <= 0 or fuel_used <= 0:
            bot.reply_to(message, "Расстояние и расход должны быть положительными числами.")
            return

        # Вычисляем расход топлива на 100 км
        consumption_per_100km = (fuel_used / distance) * 100

        # Форматируем результат
        result_message = f"Расход топлива на 100 км: {consumption_per_100km:.2f} литров"
        bot.reply_to(message, result_message)


    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

def calculate_fuel_consumption(engine_displacement, engine_power, vehicle_weight):

    displacement_factor = 0.8
    power_factor = 0.05
    weight_factor = 0.0005

    consumption = (engine_displacement * displacement_factor) + \
                  (engine_power * power_factor) + \
                  (vehicle_weight * weight_factor)

    return consumption

@bot.message_handler(commands=['engine_fuel'])
def engine_fuel_command(message):
    """
    Вычисляет примерный расход топлива на 100 км на основе характеристик двигателя.
    Команда должна быть в формате: /engine_fuel объем мощность вес
    где:
        объем - объем двигателя в литрах (например, 1.6)
        мощность - мощность двигателя в лошадиных силах (например, 100)
        вес - вес автомобиля в кг (например, 1200)
    """
    try:
        # Извлекаем аргументы из сообщения
        parts = message.text.split()
        if len(parts) != 4:
            bot.reply_to(message, "Неверный формат команды. Используйте: /engine_fuel объем мощность вес (например, /engine_fuel 1.6 100 1200)")
            return

        try:
            engine_displacement = float(parts[1])  # Объем двигателя
            engine_power = int(parts[2])       # Мощность двигателя
            vehicle_weight = int(parts[3])    # Вес автомобиля
        except ValueError:
            bot.reply_to(message, "Объем, мощность и вес должны быть числами.")
            return

        # Вычисляем расход топлива
        fuel_consumption = calculate_fuel_consumption(engine_displacement, engine_power, vehicle_weight)

        # Форматируем результат
        result_message = f"Приблизительный расход топлива: {fuel_consumption:.2f} литров на 100 км"
        bot.reply_to(message, result_message)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

def calculate_energy_consumption(power, hours_per_day):
    """
    Рассчитывает энергопотребление прибора за месяц.

    Параметры:
        power (float): Мощность прибора в ваттах.
        hours_per_day (float): Количество часов работы прибора в день.

    Возвращает:
        float: Энергопотребление за месяц (30 дней) в киловатт-часах (кВт*ч).
    """
    days_in_month = 30
    energy_consumption_wh = power * hours_per_day * days_in_month  # Ватт-часы
    energy_consumption_kwh = energy_consumption_wh / 1000  # Киловатт-часы
    return energy_consumption_kwh


@bot.message_handler(commands=['Energy'])
def energy_command(message):
    """
    Вычисляет энергопотребление прибора за месяц.
    Команда должна быть в формате: /energy мощность часы
    где:
        мощность - мощность прибора в ваттах (например, 100)
        часы - количество часов работы в день (например, 2.5)
    """
    try:
        # Извлекаем аргументы из сообщения
        parts = message.text.split()
        if len(parts) != 3:
            bot.reply_to(message, "Неверный формат команды. Используйте: /energy мощность часы (например, /energy 60 4)")
            return

        try:
            power = float(parts[1])  # Мощность прибора
            hours_per_day = float(parts[2])  # Часы работы в день
        except ValueError:
            bot.reply_to(message, "Мощность и часы должны быть числами.")
            return

        # Вычисляем энергопотребление
        energy_consumption = calculate_energy_consumption(power, hours_per_day)

        # Форматируем результат
        result_message = f"Энергопотребление за месяц: {energy_consumption:.2f} кВт*ч"
        bot.reply_to(message, result_message)

    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

@bot.message_handler(commands=['WHAT'])
def send_1(message):
    bot.reply_to(message, "Глобальное потепление – это долгосрочное повышение средней температуры климатической системы Земли, вызванное преимущественно деятельностью человека, в частности, выбросами парниковых газов.  Это не просто незначительное потепление, а масштабное и сложное явление, которое несет в себе серьезные последствия для нашей планеты и человечества.Что вызывает глобальное потепление?Основной причиной глобального потепления является антропогенный парниковый эффект.  Парниковые газы, такие как углекислый газ (CO2), метан (CH4), закись азота (N2O) и другие, естественным образом присутствуют в атмосфере и удерживают тепло, необходимое для поддержания жизни на Земле. Однако, с началом индустриальной эпохи, деятельность человека, а именно:")
    bot.reply_to(message, "Продолжение --------} /WHAT2")

@bot.message_handler(commands=['WHAT2'])
def send_1(message):
    bot.reply_to(message, "Сжигание ископаемого топлива (уголь, нефть, газ): является крупнейшим источником выбросов CO2. Используется для производства энергии, транспорта и промышленности. Вырубка лесов: леса поглощают CO2 из атмосферы. Их уничтожение приводит к увеличению концентрации CO2 и снижению способности планеты к его поглощению.Сельское хозяйство:  вызывает выбросы метана (животноводство, рисоводство) и закиси азота (удобрения).Промышленные процессы: некоторые промышленные процессы также выделяют парниковые газы.В результате концентрация парниковых газов в атмосфере значительно возросла, что привело к усилению парникового эффекта и удержанию большего количества тепла, тем самым нагревая планету. Последствия глобального потепления:")
    bot.reply_to(message, "Продолжение --------} /WHAT3")

@bot.message_handler(commands=['WHAT3'])
def send_1(message):
    bot.reply_to(message, "Повышение температуры:  Средняя температура на планете повышается, что приводит к увеличению количества и интенсивности тепловых волн, засух и лесных пожаров.Таяние ледников и полярных льдов:  Таяние ледников и полярных льдов приводит к повышению уровня моря, затоплению прибрежных территорий и утрате пресной воды.Изменение климата:  Глобальное потепление приводит к изменению погодных условий, увеличению количества и интенсивности экстремальных погодных явлений, таких как ураганы, наводнения и засухи.Изменение экосистем:  Изменение климата оказывает негативное влияние на экосистемы, приводя к вымиранию видов, распространению инвазивных видов и нарушению баланса в природе.Влияние на сельское хозяйство:  Изменение климата может привести к снижению урожайности сельскохозяйственных культур, что может вызвать проблемы с продовольственной безопасностью.Влияние на здоровье человека:  Повышение температуры, загрязнение воздуха и распространение болезней, переносимых насекомыми, могут оказывать негативное влияние на здоровье человека.Экономические последствия:  Ущерб от стихийных бедствий, связанных с изменением климата, может привести к значительным экономическим потерям.")
    bot.reply_to(message, "Решение --------} /EASY")

@bot.message_handler(commands=['EASY'])
def send_1(message):
    bot.reply_to(message, "Решение проблемы глобального потепления требует комплексного подхода и совместных усилий со стороны правительств, бизнеса и каждого человека:Переход на возобновляемые источники энергии: необходимо активно переходить на возобновляемые источники энергии, такие как солнечная, ветровая и гидроэнергия, для снижения выбросов CO2 от сжигания ископаемого топлива.Повышение энергоэффективности: необходимо повышать энергоэффективность зданий, транспорта и промышленности для снижения потребления энергии.Защита и восстановление лесов: необходимо защищать существующие леса и восстанавливать утраченные лесные массивы для увеличения поглощения CO2 из атмосферы.Устойчивое сельское хозяйство: необходимо внедрять устойчивые методы ведения сельского хозяйства, направленные на сокращение выбросов метана и закиси азота.Разработка и внедрение новых технологий: необходимо разрабатывать и внедрять новые технологии, которые позволяют улавливать и хранить CO2, а также разрабатывать альтернативные виды топлива.")
    bot.reply_to(message, "Продолжение --------} /EASY2")

@bot.message_handler(commands=['EASY2'])
def send_1(message):
    bot.reply_to(message, "Международное сотрудничество: необходимо международное сотрудничество для разработки и реализации глобальных стратегий по борьбе с изменением климата. Изменение образа жизни: каждый человек может внести свой вклад в борьбу с изменением климата, например, путем сокращения потребления энергии, использования общественного транспорта или велосипеда, сортировки мусора и выбора экологически чистых продуктов.")
    bot.reply_to(message, "Продолжение --------} /Zakl")

@bot.message_handler(commands=['Zakl'])
def send_1(message):
    bot.reply_to(message, "Заключение:Глобальное потепление – это серьезная угроза для нашей планеты и человечества.  Решение этой проблемы требует немедленных и решительных действий со стороны всех.  Переход на возобновляемые источники энергии, повышение энергоэффективности, защита лесов, устойчивое сельское хозяйство и международное сотрудничество – это лишь некоторые из мер, которые необходимо принять для снижения выбросов парниковых газов и смягчения последствий изменения климата. От наших действий сегодня зависит будущее нашей планеты и будущих поколений. Нельзя игнорировать эту проблему и откладывать ее решение. Действовать нужно сейчас! /start")

# Запускаем бота
bot.polling()