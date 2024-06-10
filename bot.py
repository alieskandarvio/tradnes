from flask import Flask, request
from telebot import TeleBot

API_TOKEN = '7470808038:AAHotHSsCWY46SQLOsAfYVdvEuHbCalJ3NY'
bot = TeleBot(API_TOKEN)
app = Flask(__name__)

user_data = {}

def generate_random_password(length=8):
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/' + API_TOKEN, methods=['POST'])
def webhook():
    update = TeleBot.process_new_updates([TeleBot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/set_webhook', methods=['GET', 'POST'])
def set_webhook():
    bot.remove_webhook()
    s = bot.set_webhook(url='https://your-app-name.herokuapp.com/' + API_TOKEN)
    if s:
        return "Webhook was set"
    else:
        return "Webhook setting failed"

def start(message):
    bot.send_message(message.chat.id, "Welcome! Please enter your first name:")
    bot.register_next_step_handler(message, get_first_name)

def get_first_name(message):
    user_data['first_name'] = message.text
    bot.send_message(message.chat.id, "Please enter your last name:")
    bot.register_next_step_handler(message, get_last_name)

def get_last_name(message):
    user_data['last_name'] = message.text
    bot.send_message(message.chat.id, "Please enter your email:")
    bot.register_next_step_handler(message, get_email)

def get_email(message):
    user_data['email'] = message.text
    bot.send_message(message.chat.id, "Please enter your phone number:")
    bot.register_next_step_handler(message, get_phone_number)

def get_phone_number(message):
    user_data['phone_number'] = message.text
    user_data['password'] = generate_random_password()
    bot.send_message(message.chat.id, f"Your password is: {user_data['password']}")
    bot.send_message(message.chat.id, "Please enter your birthdate (YYYY-MM-DD):")
    bot.register_next_step_handler(message, get_birthdate)

def get_birthdate(message):
    user_data['birthdate'] = message.text
    bot.send_message(message.chat.id, "Please enter your city:")
    bot.register_next_step_handler(message, get_city)

def get_city(message):
    user_data['city'] = message.text
    bot.send_message(message.chat.id, "Please enter your state/province:")
    bot.register_next_step_handler(message, get_state)

def get_state(message):
    user_data['state'] = message.text
    bot.send_message(message.chat.id, "Please enter your neighborhood:")
    bot.register_next_step_handler(message, get_neighborhood)

def get_neighborhood(message):
    user_data['neighborhood'] = message.text
    fill_form(message.chat.id)

def fill_form(chat_id):
    options = Options()
    options.headless = True
    service = Service('/nix/store/.../geckodriver')  # تحديث المسار الصحيح هنا
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://inzo.co/open-live-account?ib=2969946")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "first_name"))
        )

        driver.find_element(By.NAME, "first_name").send_keys(user_data['first_name'])
        driver.find_element(By.NAME, "last_name").send_keys(user_data['last_name'])
        driver.find_element(By.NAME, "email").send_keys(user_data['email'])
        driver.find_element(By.NAME, "password").send_keys(user_data['password'])
        driver.find_element(By.NAME, "password_confirmation").send_keys(user_data['password'])
        driver.find_element(By.NAME, "phone").send_keys(user_data['phone_number'])
        driver.find_element(By.NAME, "birthdate").send_keys(user_data['birthdate'])
        driver.find_element(By.NAME, "city").send_keys(user_data['city'])
        driver.find_element(By.NAME, "state").send_keys(user_data['state'])
        driver.find_element(By.NAME, "neighborhood").send_keys(user_data['neighborhood'])

        # اختيار الخيارات المحددة
        language_select = Select(driver.find_element(By.NAME, "language"))
        language_select.select_by_visible_text("اللغة العربية")

        trading_experience_select = Select(driver.find_element(By.NAME, "trading_experience"))
        trading_experience_select.select_by_visible_text("أقل من سنة")

        leverage_select = Select(driver.find_element(By.NAME, "leverage"))
        leverage_select.select_by_visible_text("1:100")

        account_size_select = Select(driver.find_element(By.NAME, "account_size"))
        account_size_select.select_by_visible_text("أقل من 5,000 دولار")

        # هنا يمكنك استكمال باقي الحقول والتحديدات

        bot.send_message(chat_id, "Registration complete! Please check your email to confirm your account.")

    except Exception as e:
        bot.send_message(chat_id, f"An error occurred: {str(e)}")
    finally:
        driver.quit()

if __name__ == '__main__':
    set_webhook()
    app.run(debug=True)
